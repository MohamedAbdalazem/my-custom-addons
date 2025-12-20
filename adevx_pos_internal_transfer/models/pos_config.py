from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    create_internal_transfer = fields.Boolean(string="Create Internal Transfer")
    internal_transfer_auto_confirm = fields.Boolean(string="Auto Confirm")

    transfer_picking_type_ids = fields.Many2many(
        comodel_name="stock.picking.type", string="Picking Type",
        relation='pos_internal_transfer_transfer_picking_type_ids_rel',
        domain="[('code', '=', 'internal')]")

    transfer_location_dest_ids = fields.Many2many(
        comodel_name="stock.location", string="Location Destination",
        relation='pos_internal_transfer_transfer_location_dest_ids_rel',
        domain="[('usage', '=', 'internal')]")

