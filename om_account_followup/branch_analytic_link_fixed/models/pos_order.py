from odoo import models, api, fields

class PosOrder(models.Model):
    _inherit = 'pos.order'

    branch_id = fields.Many2one('res.branch', string='Branch')

    @api.model
    def _prepare_invoice_vals(self):
        vals = super()._prepare_invoice_vals()
        if self.branch_id:
            vals['branch_id'] = self.branch_id.id
            if self.branch_id.analytic_account_id:
                vals['analytic_account_id'] = self.branch_id.analytic_account_id.id
        return vals