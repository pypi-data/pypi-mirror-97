# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from datetime import timedelta

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Bool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from trytond.i18n import gettext

STATES = {
    'invisible': Bool(~Eval('kit')),
}
DEPENDS = ['kit']


class Product(metaclass=PoolMeta):
    __name__ = "product.product"
    explode_kit_in_sales = fields.Boolean('Expand components in sales',
        states=STATES, depends=DEPENDS,
        help='When activated, the components of the kit will be added as '
        'individual sale lines with their relative unit price and the kit '
        'itself will have set its unit price to 0.')
    components_in_description = fields.Boolean('Components in description',
        states=STATES, depends=DEPENDS,
        help='When activated, the components of the kit will be added to '
        'the sale line description.')

    @staticmethod
    def default_explode_kit_in_sales():
        return False

    @staticmethod
    def default_components_in_description():
        return True

    @classmethod
    def validate(cls, products):
        super(Product, cls).validate(products)
        for product in products:
            product.check_required_salable_products_in_kits()
            product.check_purchasable_in_kit()

    def check_required_salable_products_in_kits(self):
        KitLine = Pool().get('product.kit.line')

        if not self.kit:
            return

        not_salable_lines = KitLine.search_count([
                ('parent', 'in', [self.id]),
                ('product.salable', '=', False),
                ('parent.explode_kit_in_sales', '=', True),
                ])
        if not_salable_lines:
            raise UserError(gettext(
                    'sale_kit.salable_product_required_in_kit',
                    self.rec_name))

    def check_purchasable_in_kit(self):
        if self.kit and self.purchasable:
            raise UserError(gettext(
                    'sale_kit.kit_not_purchasable',
                    self.rec_name))


    @classmethod
    def get_sale_price(cls, products, quantity=0):
        pool = Pool()
        Uom = pool.get('product.uom')

        prices = {}

        uom = None
        if Transaction().context.get('uom'):
            uom = Uom(Transaction().context.get('uom'))

        non_kits = []
        for product in products:
            if not product.kit or product.kit_fixed_list_price:
                non_kits.append(product)
                continue
            if product.explode_kit_in_sales:
                prices[product.id] = Decimal('0.0')
                continue

            product_price = Decimal('0.0')
            for kit_line in product.kit_lines:
                with Transaction().set_context(uom=kit_line.unit):
                    product_price += (cls.get_sale_price([kit_line.product],
                            quantity=kit_line.quantity)[kit_line.product.id] *
                        Decimal(str(kit_line.quantity)))
            prices[product.id] = product_price

            if uom:
                prices[product.id] = Uom.compute_price(
                    product.default_uom, prices[product.id], uom)

        if non_kits:
            prices.update(super(Product, cls).get_sale_price(non_kits,
                    quantity))
        return prices

    def compute_shipping_date(self, date=None):
        Date = Pool().get('ir.date')

        if self.kit and self.components_in_description:
            shipping_date = Date.today()
            for kit_line in self.kit_lines:
                shipping_date = min(shipping_date,
                    kit_line.product.compute_shipping_date(date))
        else:
            shipping_date = super(Product, self).compute_shipping_date(
                date=date)
        return shipping_date


class ProductKitLine(metaclass=PoolMeta):
    __name__ = 'product.kit.line'

    def get_sale_price(self):
        parent = self.parent
        if parent.kit_fixed_list_price:
            return False
        parent_kit_lines = self.search([
                ("product", "=", parent.id),
                ])
        for line in parent_kit_lines:
            if line in [x for x in line.product.kit_lines]:
                return line.get_sale_price()
        return True

    @classmethod
    def validate(cls, lines):
        super(ProductKitLine, cls).validate(lines)
        for line in lines:
            line.check_required_salable_lines()

    def check_required_salable_lines(self):
        if (self.parent.explode_kit_in_sales and
                not self.product.salable):
            raise UserError(gettext('sale_kit.salable_lines_required'))

    def get_move(self, sale_line, shipment_type):
        '''
        Return moves for the kit line according to shipment_type

        Adapted from SaleLine/get_move
        '''
        pool = Pool()
        Move = pool.get('stock.move')
        Product = pool.get('product.product')
        Uom = pool.get('product.uom')

        if sale_line.type != 'line':
            return
        if not sale_line.product:
            return
        if sale_line.product.type == 'service':
            return

        if (shipment_type == 'out') != (sale_line.quantity >= 0):
            return

        to_ship = sale_line.quantity * self.quantity
        shipped = sale_line._get_shipped_quantity_for_kit_line(self)
        quantity = to_ship - shipped

        if quantity <= 0:
            return

        if not sale_line.sale.party.customer_location:
            raise UserError(gettext(
                        'sale_kit.customer_location_required',
                        sale=sale_line.sale.rec_name,
                        line=sale_line.rec_name,
                        ))

        product_price = Decimal('0.0')
        with Transaction().set_context(uom=self.unit):
            product_price += (Product.get_sale_price([self.product],
                    quantity=self.quantity)[self.product.id] *
                    Decimal(str(self.quantity)))

        move = Move()
        move.quantity = quantity
        move.uom = self.product.default_uom
        print('YYYYYYYYYYY', move.uom.name)
        move.product = self.product
        move.from_location = sale_line.from_location
        move.to_location = sale_line.to_location
        move.state = 'draft'
        move.company = sale_line.sale.company
        move.unit_price = product_price
        move.currency = sale_line.sale.currency
        move.planned_date = sale_line.shipping_date
        move.invoice_lines = sale_line.invoice_lines
        move.origin = sale_line
        return move


class ProductSupplier(metaclass=PoolMeta):
    __name__ = 'purchase.product_supplier'

    def compute_supply_date(self, date=None):
        Date = Pool().get('ir.date')

        product = self.product
        if product.kit and product.components_in_description:
            lead_time = timedelta(0)
            for kit_line in product.kit_lines:
                lead_time = max(lead_time, kit_line.product.lead_time)
            if not date:
                date = Date.today()
            lead_time = date + lead_time
        else:
            lead_time = super(ProductSupplier, self).compute_supply_date(
                date=date)
        return lead_time

    def compute_purchase_date(self, date):
        Date = Pool().get('ir.date')

        product = self.product
        if product.kit and product.components_in_description:
            lead_time = timedelta(0)
            for kit_line in product.kit_lines:
                lead_time = max(lead_time, kit_line.product.lead_time)
            if not date:
                date = Date.today()
            lead_time = date - lead_time
        else:
            lead_time = super(ProductSupplier, self).compute_purchase_date(
                date=date)
        return lead_time
