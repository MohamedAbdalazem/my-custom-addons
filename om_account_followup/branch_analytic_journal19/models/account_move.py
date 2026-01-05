from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        for rec in self:
            branch_analytic = getattr(rec.journal_id, 'branch_analytic_account_id', False)
            if branch_analytic:
                for line in rec.line_ids:
                    line.analytic_account_id = branch_analytic

    @api.model
    def default_get(self, fields_list):
        defaults = super(AccountMove, self).default_get(fields_list)
        branch = getattr(self.env.user, 'branch_id', False)
        if branch:
            journal = self.env['account.journal'].search([
                ('branch_id', '=', branch.id),
                ('type', '=', 'sale')
            ], limit=1)
            if journal:
                defaults['journal_id'] = journal.id
        return defaults
