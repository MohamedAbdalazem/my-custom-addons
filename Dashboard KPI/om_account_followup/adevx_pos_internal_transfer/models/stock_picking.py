from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create_from_pos_ui(self, values, auto_confirm):
        picking = self.create(values)
        if auto_confirm:
            picking.action_assign()
            picking.button_validate()
        return {'name': picking.name, 'id': picking.id}

