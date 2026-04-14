from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        user = self.env.user
        if user.branch_id and user.branch_id.analytic_account_id:
            vals['analytic_account_id'] = user.branch_id.analytic_account_id.id
        return super(SaleOrder, self).create(vals)
