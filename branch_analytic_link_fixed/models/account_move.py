from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    branch_id = fields.Many2one('res.branch', string='Branch')
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        help='Analytic account related to this move (branch).'
    )

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        for rec in self:
            if rec.journal_id:
                rec.branch_id = rec.journal_id.branch_id
                if rec.journal_id.branch_analytic_account_id:
                    rec.analytic_account_id = rec.journal_id.branch_analytic_account_id
                    for line in rec.line_ids:
                        line.analytic_account_id = rec.journal_id.branch_analytic_account_id


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('move_id')
    def _onchange_move_branch(self):
        for rec in self:
            if rec.move_id and rec.move_id.analytic_account_id:
                rec.analytic_account_id = rec.move_id.analytic_account_id