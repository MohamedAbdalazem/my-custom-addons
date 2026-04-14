
from odoo import models, fields, api

class AccountPartialReconcileWizard(models.TransientModel):
    _name = 'account.partial.reconcile.wizard'
    _description = 'Partial Reconcile Wizard'

    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    writeoff_account_id = fields.Many2one('account.account', string='Write-off Account', required=True)
    label = fields.Char(string='Label', default='Partial Reconcile Write-off')
    date = fields.Date(string='Date', default=fields.Date.context_today)

    def action_partial_reconcile(self):
        active_ids = self.env.context.get('active_ids', [])
        lines = self.env['account.move.line'].browse(active_ids).filtered(lambda l: not l.reconciled)
        if not lines:
            return
        # إنشاء قيد تسوية جزئية
        amount_residual = sum(lines.mapped('amount_residual'))
        if not amount_residual:
            return

        move = self.env['account.move'].create({
            'ref': self.label,
            'journal_id': self.journal_id.id,
            'line_ids': [
                (0, 0, {
                    'account_id': self.writeoff_account_id.id,
                    'debit': amount_residual if amount_residual > 0 else 0,
                    'credit': -amount_residual if amount_residual < 0 else 0,
                    'name': self.label,
                }),
                (0, 0, {
                    'account_id': lines[0].account_id.id,
                    'credit': amount_residual if amount_residual > 0 else 0,
                    'debit': -amount_residual if amount_residual < 0 else 0,
                    'name': self.label,
                })
            ]
        })
        move.action_post()
        (lines | move.line_ids).reconcile()
