from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        user_branch = self.env.user.branch_id
        if user_branch and not vals.get('analytic_account_id'):
            vals['analytic_account_id'] = user_branch.id
        return super(SaleOrder, self).create(vals)
