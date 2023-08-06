# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta, Pool
from trytond.rpc import RPC


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    supply_state = fields.Function(fields.Selection(
            'get_supply_state_selection', 'Supply State',
            states={
                'invisible': ~Eval('supply_state'),
                }), 'get_supply_state')

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls.__rpc__.update({
            'get_supply_state_selection': RPC(),
        })

    def get_supply_state(self, name):
        res = ''
        for line in self.lines:
            if line.purchase_request_state:
                res = line.purchase_request_state
                break
        if res and (self.state == 'done' or self.shipment_state == 'sent'):
            res = 'done'
        return res

    @classmethod
    def get_supply_state_selection(cls):
        SaleLine = Pool().get('sale.line')
        field_name = 'purchase_request_state'
        selection = SaleLine.fields_get(
            [field_name])[field_name]['selection']
        return selection
