from odoo import models, fields

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    x_branch_id = fields.Many2one('res.branch', string='Branch')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_branch_id = fields.Many2one(
        'res.branch',
        string='Branch',
        related='picking_type_id.x_branch_id',
        store=True
    )
