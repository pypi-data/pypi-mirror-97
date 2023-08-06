# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from decimal import Decimal
from datetime import datetime
from datetime import date
from datetime import time

from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite
from trytond.tests.test_tryton import with_transaction

from trytond.pool import Pool
from trytond.exceptions import UserError


class ProductAttributeStrictTestCase(ModuleTestCase):
    'Test Product Attribute Strict module'
    module = 'product_attribute_strict'

    def _create_product_template(self, attribute_set=None):
        """
        Create default product template
        """
        pool = Pool()
        Template = pool.get('product.template')
        Uom = pool.get('product.uom')

        return Template.create([{
            'name': 'Test Template 1',
            'default_uom': Uom.search([('name', '=', 'Unit')])[0],
            'list_price': Decimal('10'),
            'attribute_set': attribute_set,
        }])[0]

    @with_transaction()
    def test0010_add_product_attributes(self):
        """
        Check if attributes can be added to product
        """
        pool = Pool()
        Product = pool.get('product.product')
        Attribute = pool.get('product.attribute')
        AttributeSet = pool.get('product.attribute.set')
        SelectionOption = pool.get('product.attribute.selection_option')

        # Create Attributes

        # Char attribute
        char_attr, = Attribute.create([{
            'name': 'Test Char',
        }])

        self.assertEqual(char_attr.type_, 'char')

        # Float attribute
        float_attr, = Attribute.create([{
            'type_': 'float',
            'display_name': 'Float',
            'name': 'Test Float',
        }])

        # Numeric Attribute
        numeric_attr, = Attribute.create([{
            'type_': 'numeric',
            'display_name': 'Numeric',
            'name': 'Test Numeric',
        }])

        # Datetime Attribute
        datetime_attr, = Attribute.create([{
            'type_': 'datetime',
            'display_name': 'Datetime',
            'name': 'Test Datetime',
        }])

        # Date Attribute
        date_attr, = Attribute.create([{
            'type_': 'date',
            'display_name': 'Date',
            'name': 'Test Date',
        }])

        # Selection Attribute
        selection_attr, = Attribute.create([{
            'type_': 'selection',
            'display_name': 'Selection',
            'name': 'Test Selection',
            'selection': [
                ('create', [{
                    'name': 'option1'
                }, {
                    'name': 'option2'
                }])
            ]
        }])

        # Rec name for attribute without display name
        self.assertEqual(char_attr.rec_name, char_attr.name)

        # Rec name for attribute with both name and display name
        self.assertEqual(float_attr.rec_name, float_attr.display_name)

        # Create Attribute sets
        attribute_set1, = AttributeSet.create([{
            'name': 'Test attribute set 1',
            'attributes': [('add', [
                char_attr.id, selection_attr.id, datetime_attr.id,
                date_attr.id
            ])]
        }])

        attribute_set2, = AttributeSet.create([{
            'name': 'Test attribute set 2',
            'attributes': [('add', [numeric_attr.id, float_attr.id])]
        }])

        # Create selection option for selection attribute
        option1, = SelectionOption.create([{
            'name': 'Test Option 1',
            'attribute': selection_attr
        }])

        template = self._create_product_template(attribute_set1)

        # Create product with attributes defined for attribute set 1
        # Attributes to be added must be part of attribute set defined
        # for template
        prod1, = Product.create([{
            'template': template.id,
            'attributes': [
                ('create', [{
                    'attribute': char_attr.id,
                    'value_char': 'Test Char Value',
                }, {
                    'attribute': selection_attr.id,
                    'value_selection': option1.id,
                }, {
                    'attribute': datetime_attr.id,
                    'value_datetime': datetime.now(),
                }, {
                    'attribute': date_attr.id,
                    'value_date': date.today(),
                }])
            ]
        }])

        # Test the value field
        self.assertEqual(
            prod1.attributes[0].value,
            prod1.attributes[0].value_char
        )
        self.assertEqual(
            prod1.attributes[1].value,
            prod1.attributes[1].value_selection.name
        )
        self.assertEqual(
            prod1.attributes[2].value,
            prod1.attributes[2].value_datetime.strftime("%Y-%m-%d %H:%M:%S")
        )
        self.assertEqual(
            prod1.attributes[3].value,
            datetime.combine(
                prod1.attributes[3].value_date,
                time()
            ).strftime("%Y-%m-%d")
        )

        #  Try creating product with attributes defined for attribute
        #  set 2 ( not part of attribute set defined for template), and
        #  error will be raised
        with self.assertRaises(UserError):
            Product.create([{
                'template': template.id,
                'attributes': [
                    ('create', [{
                        'attribute': numeric_attr.id,
                        'value_numeric': Decimal('10'),
                    }])
                ]
            }])
            Product.create([{
                'template': template.id,
                'attributes': [
                    ('create', [{
                        'attribute': float_attr.id,
                        'value_float': 1.23,
                    }])
                ]
            }])

        # check on_change value for attribute type
        prod_attribute = prod1.attributes[0]
        prod_attribute.on_change_attribute()

        self.assertEqual(
            prod_attribute.attribute_type, prod_attribute.attribute.type_
        )

        # check value for attribute set by changing product
        prod_attribute.on_change_product()

        self.assertEqual(
            prod_attribute.attribute_set,
            prod_attribute.product.template.attribute_set
        )


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProductAttributeStrictTestCase))
    return suite
