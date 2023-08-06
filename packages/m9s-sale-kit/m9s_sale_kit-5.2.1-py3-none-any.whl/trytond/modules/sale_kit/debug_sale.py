# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
from itertools import groupby, chain
from functools import partial

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Equal, Eval
from trytond.transaction import Transaction
from trytond.modules.sale.exceptions import (
    SaleValidationError, SaleQuotationError, PartyLocationError)


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    def get_moves_for_line(self, line, shipment_type):
        '''
        Get the moves for a sale line

        - needs patch sale_issue2762_refactor_create_shipment.diff
        '''
        moves = {}
        if line.product and line.product.kit:
            kit_moves = line.get_moves_for_kit(shipment_type)
            if kit_moves:
                i = 0
                for move in kit_moves:
                    # Provide a unique line id to avoid collision of
                    # multiple moves for the same line (must be translated
                    # back later in _group_shipment_key to enable correct
                    # grouping per sale line id)
                    move_id = '%s_%ssale_kit' % (line.id, i)
                    moves[move_id] = move
                    i += 1
        else:
            moves = super(Sale, self).get_moves_for_line(line, shipment_type)
        return moves

    def _group_shipment_key(self, moves, move):
        '''
        Check if the provided line_id was encoded by this module
        and translate it back.
        '''
        line_id, move_obj = move
        if isinstance(line_id, str) and line_id.endswith('sale_kit'):
            line_id = int(line_id.split('_')[0])
            move = (line_id, move_obj)
        return super(Sale, self)._group_shipment_key(moves, move)

    _group_return_key = _group_shipment_key


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'
    kit_depth = fields.Integer('Depth', required=True,
        help='Depth of the line if it is part of a kit.')
    kit_parent_line = fields.Many2One('sale.line', 'Parent Sale Line',
        help='The sale line that contains this product.')
    kit_child_lines = fields.One2Many('sale.line', 'kit_parent_line',
        'Kit Components', help='The components of the kit')

    @classmethod
    def __setup__(cls):
        super(SaleLine, cls).__setup__()
        required = (~(Eval('kit_parent_line', False))
            and (Equal(Eval('type'), 'line')))
        cls.unit_price.states['required'] = required

    @staticmethod
    def default_kit_depth():
        return 0

    @fields.depends('product', 'description', 'sale')
    def on_change_product(self):
        super(SaleLine, self).on_change_product()
        prefix = ' >'
        if self.description and prefix not in self.description:
            if (self.product and self.product.kit and self.product.kit_lines
                    and self.product.components_in_description):
                party = None
                party_context = {}
                if self.sale and self.sale.party:
                    party = self.sale.party
                    if party.lang:
                        party_context['language'] = party.lang.code
                with Transaction().set_context(party_context):
                    desc = ''
                    for component in self.product.kit_lines:
                        desc += '\n' + ' '.join([prefix,
                                str(component.quantity),
                                component.unit.rec_name,
                                component.product.rec_name])
                self.description += '\n' + desc

    def _fill_line_from_kit_line(self, kit_line, line):
        ProductUom = Pool().get('product.uom')

        self.product = kit_line.product
        if kit_line.unit.category.id != line.unit.category.id:
            quantity = kit_line.quantity * line.quantity
        else:
            quantity = ProductUom.compute_qty(
                    kit_line.unit, kit_line.quantity, line.unit
                    ) * line.quantity
        self.quantity = quantity
        self.unit = kit_line.unit
        self.type = 'line'
        self.kit_parent_line = line
        self.description = ''

    @classmethod
    def explode_kit(cls, lines):
        '''
        Walks through the Kit tree in depth-first order and returns
        a sorted list with all the components of the product.
        If no product on Sale Line avoid to try explode kits
        '''
        #def max_sequence(sale_lines):
        #    return max([sl.sequence for sl in sale_lines] +
        #        [max_sequence(sl.kit_child_lines) for sl in sale_lines
        #            if sl.kit_child_lines])

        Product = Pool().get('product.product')

        sale_discount = hasattr(cls, 'gross_unit_price')

        sequence = lines[0].sequence if lines and lines[0].sequence else 1
        to_write, to_create = [], []
        for line in lines:
            if line.sequence != sequence and to_create:
                line.sequence = sequence
            sequence += 1
            depth = line.kit_depth + 1
            if (line.product and line.product.kit and line.product.kit_lines
                    and line.product.explode_kit_in_sales):
                kit_lines = list(line.product.kit_lines)
                kit_lines = list(zip(kit_lines, [depth] * len(kit_lines)))
                while kit_lines:
                    kit_line = kit_lines.pop(0)
                    depth = kit_line[1]
                    kit_line = kit_line[0]
                    product = kit_line.product

                    sale_line = cls()
                    for key, value in sale_line.default_get(
                            list(sale_line._fields.keys()),
                            with_rec_name=False).items():
                        if value is not None:
                            setattr(sale_line, key, value)
                    if hasattr(line, 'party'):
                        sale_line.party = line.party
                    if hasattr(line, 'sid'):
                        sale_line.sid = line.sid
                    sale_line.sale = line.sale
                    sale_line._fill_line_from_kit_line(kit_line, line)
                    sale_line.sequence = sequence
                    sale_line.on_change_product()
                    sale_line.kit_depth = depth
                    sale_line.description = ('%s%s' %
                        ('> ' * depth, sale_line.description)
                        if sale_line.description else ' ')

                    if kit_line.get_sale_price():
                        with Transaction().set_context(
                                sale_line._get_context_sale_price()):
                            prices = Product.get_sale_price(
                                [product], line.quantity)
                            unit_price = prices[product.id]
                            digits = cls.unit_price.digits[1]
                            unit_price = unit_price.quantize(
                                Decimal(1) / 10 ** digits)
                    else:
                        unit_price = Decimal('0.0')

                    # Compatibility with sale_discount module
                    if sale_discount:
                        sale_line.gross_unit_price = unit_price
                        if line.discount:
                            sale_line.discount = line.discount
                        sale_line.on_change_discount()
                    else:
                        sale_line.unit_price = unit_price

                    to_create.append(sale_line._save_values)
                    if product.kit_lines:
                        product_kit_lines = list(product.kit_lines)
                        product_kit_lines = list(zip(product_kit_lines,
                            [depth + 1] * len(product_kit_lines)))
                        kit_lines = product_kit_lines + kit_lines
                    sequence += 1
                if not line.product.kit_fixed_list_price and line.unit_price:
                    line.unit_price = Decimal('0.0')
            elif (line.product and line.product.kit_lines and
                    not line.product.kit_fixed_list_price):
                with Transaction().set_context(
                        line._get_context_sale_price()):
                    prices = Product.get_sale_price(
                        [line.product], line.quantity)
                    unit_price = prices[line.product.id]

                # Compatibility with sale_discount module
                if sale_discount:
                    line.gross_unit_price = unit_price
                    line.on_change_discount()
                else:
                    # Avoid modifing when not required
                    if line.unit_price != unit_price:
                        line.unit_price = unit_price
            if line._save_values:
                to_write.extend(([line], line._save_values))
        if to_write:
            cls.write(*to_write)
        # Call super create to avoid recursion error
        return super(SaleLine, cls).create(to_create)

    def _get_shipped_quantity(self, shipment_type):
        '''
        Override SaleLine._get_shipped_quantity for not exploded kits
        to get correct moves.
        '''
        if (self.type == 'line' and self.product and self.product.kit
                and self.product.kit_lines
                and not self.product.explode_kit_in_sales):
            kit_quantity = self.quantity
            for line in self.product.kit_lines:
                to_ship = kit_quantity * line.quantity
                shipped = self._get_shipped_quantity_for_kit_line(line)
                if shipped < to_ship:
                    kit_quantity = 0
                    break
            return kit_quantity
        else:
            return super(SaleLine, self)._get_shipped_quantity(shipment_type)

    def _get_shipped_quantity_for_kit_line(self, kit_line):
        pool = Pool()
        Uom = pool.get('product.uom')

        skips = set(m for m in self.moves_recreated)
        shipped = 0
        for move in self.moves:
            if move not in skips:
                if kit_line.product == move.product:
                    shipped += Uom.compute_qty(move.uom,
                        move.quantity, kit_line.unit)
        return shipped

    def get_moves_for_kit_org(self, shipment_type):
        '''
        Walk through the kit tree in depth-first order, get
        a sorted list with all the components of the kit and
        create moves for the kit components.

        s.a. sale/sale.py/get_move
        s.a. sale_kit/product.py/KitLine/get_move
        '''
        pool = Pool()
        StockMove = pool.get('stock.move')
        Uom = Pool().get('product.uom')

        if self.type != 'line':
            return
        if (not self.product and not self.product.kit and
                not self.product.kit_lines and
                self.product.explode_kit_in_sales):
            return
        if (shipment_type == 'out') != (self.quantity >= 0):
            return

        quantity = (self._get_move_quantity(shipment_type)
            - self._get_shipped_quantity(shipment_type))

        quantity = self.unit.round(quantity)
        if quantity <= 0:
            return

        if not self.sale.party.customer_location:
            raise PartyLocationError(
                gettext('sale.msg_sale_customer_location_required',
                    sale=self.sale.rec_name,
                    party=self.sale.party.rec_name))

        to_write, to_create = [], []
        depth = self.kit_depth + 1
        kit_lines = list(self.product.kit_lines)
        kit_lines = list(zip(kit_lines, [depth] * len(kit_lines)))
        print(-2, kit_lines)
        while kit_lines:
            kit_line = kit_lines.pop(0)
            depth = kit_line[1]
            kit_line = kit_line[0]
            move = kit_line.get_move(self, shipment_type)
            print(-1, move)
            move.on_change_product()
            move.save()
            print('move saved')
            if move:
                print(0, move._save_values)
                #to_create.append(move._save_values)
                to_create.append(move)
            product = kit_line.product
            print(1, move._save_values)
            print(2, product.default_uom_category.name)
            print(3, product.default_uom.name)
            print(5, move.uom.name)
            #print(6, move.product_uom_category.name)
            #print(7, move.uom.name)
            if product.kit_lines:
                product_kit_lines = list(product.kit_lines)
                product_kit_lines = list(zip(product_kit_lines,
                    [depth + 1] * len(product_kit_lines)))
                kit_lines = product_kit_lines + kit_lines

        print(10,self._save_values)
        if self._save_values:
            to_write.extend(([self], self._save_values))
            self.write(*to_write)
        print(20,StockMove.product.domain)
        #return StockMove.create(to_create)

    def get_moves_for_kit(self, shipment_type):
        '''
        Walk through the kit tree in depth-first order, get
        a sorted list with all the components of the kit and
        create moves for the kit components.

        s.a. sale/sale.py/get_move
        s.a. sale_kit/product.py/KitLine/get_move
        '''
        pool = Pool()
        StockMove = pool.get('stock.move')
        Uom = Pool().get('product.uom')

        if self.type != 'line':
            return
        if (not self.product and not self.product.kit and
                not self.product.kit_lines and
                self.product.explode_kit_in_sales):
            return
        if (shipment_type == 'out') != (self.quantity >= 0):
            return

        quantity = (self._get_move_quantity(shipment_type)
            - self._get_shipped_quantity(shipment_type))

        quantity = self.unit.round(quantity)
        if quantity <= 0:
            return

        if not self.sale.party.customer_location:
            raise PartyLocationError(
                gettext('sale.msg_sale_customer_location_required',
                    sale=self.sale.rec_name,
                    party=self.sale.party.rec_name))

        to_write, to_create = [], []
        depth = self.kit_depth + 1
        kit_lines = list(self.product.kit_lines)
        kit_lines = list(zip(kit_lines, [depth] * len(kit_lines)))
        print(-2, kit_lines)
        while kit_lines:
            kit_line = kit_lines.pop(0)
            depth = kit_line[1]
            kit_line = kit_line[0]
            #with Transaction().new_transaction() as new_transaction:
            #print('Sqlitecursor1', dir(Transaction().connection))
            #print('Sqlitecursor',
            #    dir(Transaction().connection.cursor().connection))
            #for cache in Transaction().connection.cursor().cache.values():
            #    print('cache1', cache)
            print('Trans', dir(Transaction()))
            Transaction().cache.clear()
            for item in to_create:
                print('itemc', item)
                item._local_cache.clear()
            move = kit_line.get_move(self, shipment_type)
            print(-1, move)
            #move.on_change_product()
            print('???',move.on_change_with_product_uom_category())
            if move:
                print(0, move._save_values)
                #to_create.append(move._save_values)
                to_create.append(move)
            #print('move', dir(move))
            print('move1', move._cache)
            move._cache.clear()
            print('move1', move._cache)
            print('move2', move._local_cache)
            for item in move._local_cache:
                print('itemlc', item)
            product = kit_line.product
            print(1, move._save_values)
            print(2, product.default_uom_category.name)
            print(3, product.default_uom.name)
            print(5, move.uom.name)
            move.save()
                #new_transaction.commit()
            print('move saved')
            print(6, move.product_uom_category.name)
            #print(7, move.uom.name)
            if product.kit_lines:
                product_kit_lines = list(product.kit_lines)
                product_kit_lines = list(zip(product_kit_lines,
                    [depth + 1] * len(product_kit_lines)))
                kit_lines = product_kit_lines + kit_lines

        print(10,self._save_values)
        if self._save_values:
            to_write.extend(([self], self._save_values))
            self.write(*to_write)
        print(20,StockMove.product.domain)
        return StockMove.create(to_create)

    @classmethod
    def create(cls, values):
        lines = super(SaleLine, cls).create(values)
        if (Transaction().context.get('explode_kit', True)
                and not Transaction().context.get('standalone', False)):
            lines.extend(cls.explode_kit(lines))
        return lines

    def get_kit_lines(self, kit_line=None):
        res = []
        if kit_line:
            childs = kit_line.kit_child_lines
        else:
            childs = self.kit_child_lines
        for kit_line in childs:
            res.append(kit_line)
            res += self.get_kit_lines(kit_line)
        return res

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        to_write, to_reset, to_delete = [], [], []
        if (Transaction().context.get('explode_kit', True)
                and not Transaction().context.get('standalone', False)):
            for lines, values in zip(actions, actions):
                reset_kit = False
                # TODO Explode kit when add new line from standalone
                if ('product' in values or 'quantity' in values
                        or 'unit' in values):
                    reset_kit = True
                lines = lines[:]
                if reset_kit:
                    for line in lines:
                        to_delete += line.get_kit_lines()
                    lines = list(set(lines) - set(to_delete))
                    to_reset.extend(lines)
                to_write.extend((lines, values))
        else:
            to_write = args
        super(SaleLine, cls).write(*to_write)
        if to_delete:
            cls.delete(to_delete)
        if to_reset:
            cls.explode_kit(to_reset)

    @classmethod
    def copy(cls, lines, default=None):
        if default is None:
            default = {}
        default.setdefault('kit_child_lines', [])
        lines = [x for x in lines if not x.kit_parent_line]
        new_lines = super(SaleLine, cls).copy(lines, default=default)
        return new_lines

    def get_invoice_line(self):
        lines = super(SaleLine, self).get_invoice_line()
        for line in lines:
            line.sequence = self.sequence
        return lines

    def get_move(self, shipment_type):
        # Don't create a move for a kit when the kit is not exploded
        # Happens when shipment_type == 'return', be rather safe than sorry
        if self.type != 'line' or not self.product:
            return
        if self.product.kit and not self.product.explode_kit_in_sales:
            return
        return super(SaleLine, self).get_move(shipment_type)

