# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import ir
from . import shipment

__all__ = ['register']


def register():
    Pool.register(
        ir.Cron,
        shipment.Configuration,
        shipment.Move,
        shipment.UpdatePlannedDateStart,
        module='stock_update_planned_date', type_='model')
    Pool.register(
        shipment.UpdatePlannedDate,
        module='stock_update_planned_date', type_='wizard')
