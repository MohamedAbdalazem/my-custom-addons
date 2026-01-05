from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        user_branch = self.env.user.branch_id
        if user_branch and not vals.get('analytic_account_id'):
            vals['analytic_account_id'] = user_branch.id
        return super(AccountMove, self).create(vals)
