# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.transaction import Transaction
from trytond.pyson import Eval, Or


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    available_stock_qty = fields.Function(
        fields.Float(
            'Available Quantity',
            digits=(16, Eval('unit_digits', 2)),
            states={
                'invisible': Or(
                    Eval('type') != 'line',
                    Eval('sale_state') == 'done'
                ),
            },
            depends=['type', 'unit_digits', 'sale_state']
        ),
        'on_change_with_available_stock_qty'
    )

    sale_state = fields.Function(
        fields.Char('Sale State'), 'get_sale_state'
    )

    @fields.depends(
        '_parent_sale.warehouse', '_parent_sale.sale_date',
        'sale', 'product', 'type')
    def on_change_with_available_stock_qty(self, name=None):
        """
        Returns the available stock to process a sale
        """
        pool = Pool()
        Date = pool.get('ir.date')
        Product = pool.get('product.product')

        # If a date is specified on sale, use that. If not, use the
        # current date.
        date = self.sale and self.sale.sale_date or Date.today()

        # If the sales person is taking an order for a date in the past
        # (which tryton allows), the stock cannot be of the past, but of
        # the current date.
        date = max(date, Date.today())

        warehouse_id = self.get_warehouse(None)
        if self.type == 'line' and self.product and warehouse_id:
            with Transaction().set_context(
                    locations=[warehouse_id],       # sale warehouse
                    stock_skip_warehouse=True,      # quantity of storage only
                    stock_date_end=date,            # Stock as of sale date
                    stock_assign=True):             # Exclude Assigned
                product = Product(self.product.id)
                if date <= Date.today():
                    return product.quantity
                else:
                    # For a sale in the future, it is more interesting to
                    # see the forecasted quantity rather than what is
                    # currently in the warehouse.
                    return product.forecast_quantity

    def get_sale_state(self, name):
        """
        Returns the state of the Sale
        """
        return self.sale and self.sale.state
