# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.sale_available_stock.tests.test_sale_available_stock import suite
except ImportError:
    from .test_sale_available_stock import suite

__all__ = ['suite']
