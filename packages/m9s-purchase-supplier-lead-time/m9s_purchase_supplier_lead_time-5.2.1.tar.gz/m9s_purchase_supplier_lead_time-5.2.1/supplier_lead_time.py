# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from datetime import timedelta

from trytond.model import ModelView, ModelSQL, fields, Unique
from trytond.pyson import Eval, If
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


class SupplierLeadTime(ModelSQL, ModelView):
    'Supplier Lead Time'
    __name__ = 'purchase.supplier.lead_time'
    company = fields.Many2One('company.company', 'Company', required=True,
        ondelete='CASCADE', select=True,
        domain=[
            ('id', If(Eval('context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', -1)),
            ])
    party = fields.Many2One('party.party', 'Supplier', required=True,
        ondelete='CASCADE', select=True)
    lead_time = fields.TimeDelta('Lead Time', required=True)

    @classmethod
    def __setup__(cls):
        super(SupplierLeadTime, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints = [
            ('supplier_uniq', Unique(t, t.party, t.company),
                'The supplier must be unique by company.')
            ]

    @staticmethod
    def default_company():
        return Transaction().context.get('company')


class ProductSupplier(metaclass=PoolMeta):
    __name__ = 'purchase.product_supplier'

    global_lead_time = fields.Function(fields.TimeDelta('Global Lead Time',
            help='The global lead time defined for the supplier is used '
            'when there is no individual lead time set for this product.',
            depends=['party']),
            'on_change_with_global_lead_time')

    @fields.depends('company', 'party')
    def on_change_with_global_lead_time(self, name=None):
        pool = Pool()
        SupplierLeadTime = pool.get('purchase.supplier.lead_time')
        if self.party:
            global_lead_time = SupplierLeadTime.search([
                    ('party', '=', self.party),
                    ('company', '=', self.company),
                    ])
            if global_lead_time:
                return global_lead_time[0].lead_time
        return None

    def compute_supply_date(self, date=None):
        pool = Pool()
        Date = pool.get('ir.date')

        if not date:
            date = Date.today()
        if self.lead_time is None and self.global_lead_time:
                return date + self.global_lead_time
        return super(ProductSupplier, self).compute_supply_date(
            date=date)

    def compute_purchase_date(self, date):
        if self.lead_time is None and self.global_lead_time:
            return date - self.global_lead_time
        return super(ProductSupplier, self).compute_purchase_date(
            date)
