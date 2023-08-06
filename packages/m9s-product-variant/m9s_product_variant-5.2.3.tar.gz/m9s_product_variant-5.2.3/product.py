# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal

from trytond import backend
from trytond.pool import PoolMeta, Pool
from trytond.model import ModelSQL, fields
from trytond.pyson import Eval
from trytond.config import config
from trytond.tools.multivalue import migrate_property
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

STATES = {
    'readonly': ~Eval('active', True),
}
DEPENDS = ['active']

price_digits = (16, config.getint('product', 'price_decimal', default=4))


class Template(metaclass=PoolMeta):
    __name__ = "product.template"

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()
        cls.list_price = fields.Function(fields.Numeric("List Price"),
            'get_prices', setter='set_prices')

    def get_prices(self, name):
        '''
        Reached here! Just raise an exception to know what logic is using
        product template's prices?
        '''
        raise NotImplementedError(
            "Product prices must be taken from product.product aka Variant")

    @classmethod
    def set_prices(cls, products, name, value):
        # Prevent NotImplementedError for list_price
        pass


class Product(metaclass=PoolMeta):
    __name__ = "product.product"

    list_price = fields.MultiValue(fields.Numeric(
            "List Price", required=True, digits=price_digits,
            states=STATES, depends=DEPENDS))
    list_prices = fields.One2Many(
        'product.variant.list_price', 'product', "List Prices")
    name = fields.Function(fields.Char('Name'),
        getter='on_change_with_name', searcher='search_rec_name')
    variant_name = fields.Char('Variant Name', translate=True,
        select=True, states={
                        'readonly': ~Eval('active', True),
                        }, depends=['active'])

    @classmethod
    def __setup__(cls):
        if not hasattr(cls, '_no_template_field'):
            cls._no_template_field = set()
        cls._no_template_field.update(['list_price', 'name'])
        super(Product, cls).__setup__()

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'list_price':
            return pool.get('product.variant.list_price')
        return super(Product, cls).multivalue_model(field)

    @classmethod
    def default_list_price(cls, **pattern):
        return Decimal(0)

    @property
    def list_price_used(self):
        return self.get_multivalue('list_price')

    @fields.depends('variant_name', 'template')
    def on_change_with_name(self, name=None):
        '''
        Return the variant_name instead of template name
        '''
        return self.variant_name

    def get_rec_name(self, name=None):
        '''
        Return the variant_name` if it is set, else return
        the template name.
        This method changes the name to `[code] variant_name` if they are set,
        else it returns the template name.
        '''
        rec_name = self.variant_name or self.template.name
        if self.code:
            rec_name = '[%s] %s' % (self.code, rec_name)
        return rec_name

    @classmethod
    def search_rec_name(cls, name, clause):
        '''
        Downstream implementation of `search_rec_name` which adds the
        variant_name field to the domain.
        '''
        domain = super(Product, cls).search_rec_name(name, clause)
        domain.append(('variant_name', ) + tuple(clause[1:]))
        return domain

    @classmethod
    def set_template(cls, products, name, value):
        '''
        Provide a generic setter for function fields when using
        template fields on products. (In analogy to get_template,
        search_template for the use in downstream modules)
        '''
        Template = Pool().get('product.template')
        Template.write([p.template for p in products], {
                name: value,
                })


class VariantListPrice(ModelSQL, CompanyValueMixin):
    "Variant List Price"
    __name__ = 'product.variant.list_price'
    product = fields.Many2One(
        'product.product', "Product", ondelete='CASCADE', select=True)
    list_price = fields.Numeric("List Price", digits=price_digits)

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(VariantListPrice, cls).__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.append('list_price')
        value_names.append('list_price')
        fields.append('company')
        migrate_property(
            'product.product', field_names, cls, value_names,
            parent='product', fields=fields)
