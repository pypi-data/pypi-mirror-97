# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import supplier_lead_time

__all__ = ['register']


def register():
    Pool.register(
        supplier_lead_time.ProductSupplier,
        supplier_lead_time.SupplierLeadTime,
        module='purchase_supplier_lead_time', type_='model')
