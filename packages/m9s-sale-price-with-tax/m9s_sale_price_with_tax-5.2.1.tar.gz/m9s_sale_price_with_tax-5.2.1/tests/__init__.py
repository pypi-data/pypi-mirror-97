# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.sale_price_with_tax.tests.test_sale_price_with_tax import suite
except ImportError:
    from .test_sale_price_with_tax import suite

__all__ = ['suite']
