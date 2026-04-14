from odoo import models, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def create(self, vals):
        company = self.env.company
        if company.analytic_account_id and not vals.get('analytic_account_id'):
            vals['analytic_account_id'] = company.analytic_account_id.id
        return super(AccountMoveLine, self).create(vals)
