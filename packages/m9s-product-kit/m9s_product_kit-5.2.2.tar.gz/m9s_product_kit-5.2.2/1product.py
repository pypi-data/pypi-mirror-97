# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import If, Eval, Bool
from trytond.exceptions import UserError
from trytond.i18n import gettext

from nereid import url_for


class ProductKitLine(ModelSQL, ModelView):
    "Kit Line"
    __name__ = 'product.kit.line'
    parent = fields.Many2One('product.product', 'Parent Product',
        required=True, ondelete='CASCADE')
    sequence = fields.Integer('Sequence')
    product = fields.Many2One('product.product', 'Product', required=True,
        ondelete='CASCADE')
    product_uom_category = fields.Function(
        fields.Many2One('product.uom.category', 'Product Uom Category'),
        'on_change_with_product_uom_category')
    quantity = fields.Float('Quantity', digits=(16, Eval('unit_digits', 2)),
        required=True, depends=['unit_digits'])
    unit = fields.Many2One('product.uom', 'Unit', required=True,
        domain=[
            If(Bool(Eval('product_uom_category')),
                ('category', '=', Eval('product_uom_category')),
                ('category', '!=', -1)),
            ],
        depends=['product', 'product_uom_category'])
    unit_digits = fields.Function(fields.Integer('Unit Digits'),
        'on_change_with_unit_digits')

    @staticmethod
    def order_sequence(tables):
        table, _ = tables[None]
        return [table.sequence is None, table.sequence]

    @staticmethod
    def default_sequence():
        return 1

    @fields.depends('product', 'unit', 'quantity')
    def on_change_product(self):
        if not self.product:
            self.unit = None
            self.unit_digits = None
        elif not self.unit:
            self.unit = self.product.default_uom.id
            self.unit.rec_name = self.product.default_uom.rec_name
            self.unit_digits = self.product.default_uom.digits

    @fields.depends('product')
    def on_change_with_product_uom_category(self, name=None):
        if self.product:
            return self.product.default_uom_category.id

    @fields.depends('product', 'quantity', 'unit')
    def on_change_unit(self):
        self.on_change_quantity()

    @fields.depends('unit')
    def on_change_with_unit_digits(self, name=None):
        if self.unit:
            return self.unit.digits
        return 2

    @classmethod
    def __setup__(cls):
        super(ProductKitLine, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))

    @classmethod
    def validate(cls, kits):
        super(ProductKitLine, cls).validate(kits)
        cls.check_recursion_kits(kits)

    @classmethod
    def check_recursion_kits(cls, kits):
        def check_recursion_product(products, all_products):
            Product = Pool().get('product.product')
            if not products:
                return True
            new_products = []
            for product in Product.browse(products):
                if product.kit and product.id in all_products:
                    raise UserError(gettext(
                            'product_kit.recursive_kits'))
                elif not product.kit:
                    continue
                for line in product.kit_lines:
                    new_products.append(line.product.id)
            if new_products:
                return check_recursion_product(new_products,
                        all_products + products)
            return True

        products = []
        for kit_line in kits:
            if kit_line.product.kit:
                products += [kit_line.product.id]
        return check_recursion_product(products, [])


class Product(metaclass=PoolMeta):
    __name__ = "product.product"
    kit = fields.Boolean('Kit')
    kit_lines = fields.One2Many('product.kit.line', 'parent', 'Kit Components',
        states={
            'invisible': Bool(~Eval('kit')),
            },
        depends=['kit'])
    kit_fixed_list_price = fields.Boolean('Kit Fixed List Price',
        states={
            'invisible': Bool(~Eval('kit')),
            },
        depends=['kit'], help='When activated, the list price of the kit '
        'will be taken from the list price field. Otherwise the list price is '
        'calculated as the sum of the prices of the kit components.')

    @classmethod
    def view_attributes(cls):
        return super(Product, cls).view_attributes() + [
            ('//page[@id="kit"]', 'states', {
                    'invisible': ~Bool(Eval('kit')),
                    }),
            ]

    @staticmethod
    def default_kit_fixed_list_price():
        return False

    @classmethod
    def explode_kit(cls, products, quantity, unit, depth=1):
        """
        Walks through the Kit tree in depth-first order and returns
        a sorted list with all the components of the product.
        """
        uom_obj = Pool().get('product.uom')
        result = []
        for product in products:
            for line in product.kit_lines:
                qty = quantity * uom_obj.compute_qty(line.unit, line.quantity,
                        unit)
                result.append({
                        'product': line.product,
                        'quantity': qty,
                        'unit': line.unit,
                        'unit_price': Decimal('0.00'),
                        'depth': depth,
                        })
                result += cls.explode_kit(line.product, quantity,
                        line.unit, depth + 1)
        return result

    def serialize(self, purpose=None):
        '''
        Return serializable dictionary suitable for use with
        components display
        '''
        result = super(Product, self).serialize(purpose)

        result['kit'] = self.kit
        result['kit_lines'] = [
            {
                'id': l.product.id,
                'rec_name': l.product.rec_name,
                'url': url_for('product.product.render', uri=l.product.uri),
                } for l in self.kit_lines
            ]
        return result
