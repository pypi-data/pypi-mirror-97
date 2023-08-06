=================
Sale Kit Scenario
=================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import config, Model, Wizard, Report
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Install sale_kit::

    >>> config = activate_modules(['sale_kit', 'purchase'])

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> cash = accounts['cash']

Create tax::

    >>> tax = create_tax(Decimal('.10'))
    >>> tax.save()

Create parties::

    >>> Party = Model.get('party.party')
    >>> supplier = Party(name='Supplier')
    >>> supplier.save()
    >>> customer = Party(name='Customer')
    >>> customer.save()

Create account category::

    >>> ProductCategory = Model.get('product.category')
    >>> account_category = ProductCategory(name="Account Category")
    >>> account_category.accounting = True
    >>> account_category.account_expense = expense
    >>> account_category.account_revenue = revenue
    >>> account_category.customer_taxes.append(tax)
    >>> account_category.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> meter, = ProductUom.find([('name', '=', 'Meter')])

    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')
    >>> ProductKitLine = Model.get('product.kit.line')

    >>> tkit1 = ProductTemplate()
    >>> tkit1.name = 'Template1'
    >>> tkit1.default_uom = unit
    >>> tkit1.type = 'goods'
    >>> tkit1.salable = True
    >>> tkit1.list_price = Decimal('10')
    >>> tkit1.cost_price_method = 'fixed'
    >>> tkit1.account_category = account_category
    >>> pkit1, = tkit1.products
    >>> pkit1.code = 'V1'
    >>> pkit1.description = 'Variant1'
    >>> pkit1.cost_price = Decimal('5')
    >>> tkit1.save()
    >>> pkit1, = tkit1.products

    >>> tkit2 = ProductTemplate()
    >>> tkit2.name = 'Template2'
    >>> tkit2.default_uom = unit
    >>> tkit2.type = 'goods'
    >>> tkit2.salable = True
    >>> tkit2.list_price = Decimal('10')
    >>> tkit2.cost_price_method = 'fixed'
    >>> tkit2.account_category = account_category
    >>> pkit2, = tkit2.products
    >>> pkit2.code = 'V2'
    >>> pkit2.description = 'Variant2'
    >>> pkit2.cost_price = Decimal('5')
    >>> tkit2.save()
    >>> pkit2, = tkit2.products

    >>> tkit3 = ProductTemplate()
    >>> tkit3.name = 'Template3'
    >>> tkit3.default_uom = meter
    >>> tkit3.type = 'goods'
    >>> tkit3.salable = True
    >>> tkit3.list_price = Decimal('10')
    >>> tkit3.cost_price_method = 'fixed'
    >>> tkit3.account_category = account_category
    >>> pkit3, = tkit3.products
    >>> pkit3.code = 'V3'
    >>> pkit3.description = 'Variant3'
    >>> pkit3.cost_price = Decimal('5')
    >>> tkit3.save()
    >>> pkit3, = tkit3.products

Create an explodable kit with fixed list price::

    >>> template1 = ProductTemplate()
    >>> template1.name = 'TKitExplodable'
    >>> template1.default_uom = unit
    >>> template1.type = 'goods'
    >>> template1.salable = True
    >>> template1.list_price = Decimal('10')
    >>> template1.cost_price_method = 'fixed'
    >>> template1.account_category = account_category
    >>> product, = template1.products
    >>> product.cost_price = Decimal('5')
    >>> product.kit = True
    >>> product.explode_kit_in_sales = True
    >>> template1.save()
    >>> kit_explodable, = template1.products

    >>> pkit_line1 = ProductKitLine()
    >>> kit_explodable.kit_lines.append(pkit_line1)
    >>> pkit_line1.product = pkit1
    >>> pkit_line1.quantity = 1

    >>> pkit_line2 = ProductKitLine()
    >>> kit_explodable.kit_lines.append(pkit_line2)
    >>> pkit_line2.product = pkit2
    >>> pkit_line2.quantity = 1

    >>> pkit_line3 = ProductKitLine()
    >>> kit_explodable.kit_lines.append(pkit_line3)
    >>> pkit_line3.product = pkit3
    >>> pkit_line3.quantity = 1

    >>> kit_explodable.kit_fixed_list_price = True
    >>> kit_explodable.save()

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Sale with explodable kit::

    >>> Sale = Model.get('sale.sale')
    >>> SaleLine = Model.get('sale.line')
    >>> sale = Sale()
    >>> sale.party = customer
    >>> sale.payment_term = payment_term
    >>> sale.invoice_method = 'order'
    >>> sale_line = SaleLine()
    >>> sale.lines.append(sale_line)
    >>> sale_line.product = kit_explodable
    >>> sale_line.quantity = 2.0
    >>> sale.save()
    >>> sale.click('quote')
    >>> len(sale.lines) == 4
    True
    >>> line1, line2, line3, line4 = sale.lines
    >>> line1.kit_depth
    0
    >>> line2.kit_depth
    1
    >>> line3.kit_depth
    1
    >>> line4.kit_depth
    1
    >>> sale.click('confirm')
    >>> sale.click('process')

Return the sale::

    >>> return_sale = Wizard('sale.return_sale', [sale])
    >>> return_sale.execute('return_')
    >>> returned_sale, = Sale.find([
    ...     ('state', '=', 'draft'),
    ...     ])
    >>> len(returned_sale.lines)
    4
    >>> line1, line2, line3, line4 = returned_sale.lines
    >>> line1.product.kit
    1
    >>> line1.unit_price
    Decimal('10.0000')
    >>> line2.unit_price
    Decimal('0.0')
    >>> line3.unit_price
    Decimal('0.0')
    >>> line4.unit_price
    Decimal('0.0')
    >>> returned_sale.click('quote')

Create an non-exploded kit with calculated list price::

    >>> template2 = ProductTemplate()
    >>> template2.name = 'product'
    >>> template2.default_uom = unit
    >>> template2.type = 'goods'
    >>> template2.salable = True
    >>> template2.list_price = Decimal('0')
    >>> template2.cost_price_method = 'fixed'
    >>> template2.account_category = account_category
    >>> product, = template2.products
    >>> product.cost_price = Decimal('0')
    >>> product.kit = True
    >>> product.explode_kit_in_sales = False
    >>> template2.save()

    >>> kit_non_exploded, = template2.products

    >>> pkit_line1 = ProductKitLine()
    >>> kit_non_exploded.kit_lines.append(pkit_line1)
    >>> pkit_line1.product = pkit1
    >>> pkit_line1.quantity = 1

    >>> pkit_line2 = ProductKitLine()
    >>> kit_non_exploded.kit_lines.append(pkit_line2)
    >>> pkit_line2.product = pkit2
    >>> pkit_line2.quantity = 1

    >>> pkit_line3 = ProductKitLine()
    >>> kit_non_exploded.kit_lines.append(pkit_line3)
    >>> pkit_line3.product = pkit3
    >>> pkit_line3.quantity = 1

    >>> kit_non_exploded.kit_fixed_list_price = False
    >>> kit_non_exploded.components_in_description = True
    >>> kit_non_exploded.save()

Sale with non-exploded kit::

    >>> sale = Sale()
    >>> sale.party = customer
    >>> sale.payment_term = payment_term
    >>> sale.invoice_method = 'order'
    >>> sale_line = SaleLine()
    >>> sale.lines.append(sale_line)
    >>> sale_line.product = kit_non_exploded
    >>> sale_line.quantity = 4.0
    >>> sale.save()
    >>> sale.click('quote')
    >>> sale = Sale(sale.id)
    >>> len(sale.lines)
    1
    >>> line1, = sale.lines
    >>> line1.kit_depth
    0
    >>> line1 = SaleLine(line1.id)
    >>> sale.untaxed_amount
    Decimal('120.00')
    >>> sale.total_amount
    Decimal('132.00')
    >>> sale.click('confirm')
    >>> sale.click('process')

Return the sale::

    >>> return_sale = Wizard('sale.return_sale', [sale])
    >>> return_sale.execute('return_')
    >>> returned_sale, = Sale.find([
    ...     ('state', '=', 'draft'),
    ...     ])
    >>> len(returned_sale.lines) == 1
    True
    >>> line1, = returned_sale.lines
    >>> line1.product.kit
    1
    >>> line1.unit_price
    Decimal('30.0000')
    >>> line1.quantity
    -4.0
