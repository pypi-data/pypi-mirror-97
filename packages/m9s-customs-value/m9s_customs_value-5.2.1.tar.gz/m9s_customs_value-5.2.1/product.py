# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval, Bool, Not


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'

    country_of_origin = fields.Many2One(
        'country.country', 'Country of Origin',
    )
    customs_value = fields.Numeric(
        "Customs Value",
        states={
            'invisible': Bool(Eval('use_list_price_as_customs_value')),
            'required': Not(Bool(Eval('use_list_price_as_customs_value')))
        }, depends=['use_list_price_as_customs_value'],
    )

    use_list_price_as_customs_value = fields.Boolean(
        "Use List Price As Customs Value ?"
    )

    customs_value_used = fields.Function(
        fields.Numeric("Customs Value Used"),
        'get_customs_value_used'
    )
    customs_description = fields.Text(
        "Customs Description",
        states={
            'invisible': Bool(Eval("use_name_as_customs_description")),
            'required': Not(Bool(Eval("use_name_as_customs_description")))
        },
        depends=["use_name_as_customs_description"]
    )

    use_name_as_customs_description = fields.Boolean(
        "Use Name as Customs Description ?"
    )

    customs_description_used = fields.Function(
        fields.Text("Customs Description Used"),
        "get_customs_description_used"
    )

    @classmethod
    def get_customs_description_used(cls, products, name):
        return {
            product.id: (
                product.name if product.use_name_as_customs_description else
                product.customs_description
            )
            for product in products
        }

    @staticmethod
    def default_use_name_as_customs_description():
        return True

    @staticmethod
    def default_use_list_price_as_customs_value():
        return True

    @classmethod
    def get_customs_value_used(cls, products, name):
        return {
            product.id: (
                product.list_price if product.use_list_price_as_customs_value
                else product.customs_value
            )
            for product in products
        }
