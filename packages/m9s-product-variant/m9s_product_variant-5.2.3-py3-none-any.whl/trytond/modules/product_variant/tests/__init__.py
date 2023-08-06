# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.product_variant.tests.test_product_variant import suite
except ImportError:
    from .test_product_variant import suite

__all__ = ['suite']
