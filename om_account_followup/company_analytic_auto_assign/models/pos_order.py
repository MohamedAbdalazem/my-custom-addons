from odoo import models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create(self, vals):
        user = self.env.user
        if user.branch_id and user.branch_id.analytic_account_id:
            vals['analytic_account_id'] = user.branch_id.analytic_account_id.id
        return super(PosOrder, self).create(vals)
