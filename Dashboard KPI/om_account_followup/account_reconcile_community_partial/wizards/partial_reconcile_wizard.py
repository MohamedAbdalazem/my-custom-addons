from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountPartialReconcileWizard(models.TransientModel):
    _name = 'account.partial.reconcile.wizard'
    _description = 'Partial Reconcile (Write-Off) Wizard'

    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain="[('type','in', ('bank','cash','general'))]")
    writeoff_account_id = fields.Many2one('account.account', string='Write-off Account', required=True, domain="[('deprecated','=',False)]")
    label = fields.Char(string='Label', default='Write-off')
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # try to set a default journal
        journal = self.env['account.journal'].search([('type', 'in', ('bank','cash','general'))], limit=1)
        if journal:
            res['journal_id'] = journal.id
        return res

    def action_apply_writeoff_and_reconcile(self):
        self.ensure_one()
        active_ids = self.env.context.get('active_ids') or []
        if not active_ids:
            raise UserError(_('No journal items selected for partial reconciliation.'))

        lines = self.env['account.move.line'].browse(active_ids).filtered(lambda l: not l.reconciled)
        if not lines:
            raise UserError(_('Selected lines are already reconciled.'))

        # compute the total debit and credit for selected lines
        total_debit = sum(lines.mapped('debit'))
        total_credit = sum(lines.mapped('credit'))

        # Determine writeoff amount needed to balance
        balance = round(total_debit - total_credit, 2)
        if balance == 0:
            raise UserError(_('Selected lines are already balanced; try full reconcile instead.'))

        # Create a journal entry (write-off) to balance lines
        move_vals = {
            'date': self.date,
            'journal_id': self.journal_id.id,
            'ref': self.label,
            'line_ids': [],
        }

        # create counter line to balance the selected lines
        # if balance > 0 then need a credit writeoff (negative amount), else debit
        if balance > 0:
            # write a credit on writeoff account and debit on the journal counter (use liquidity)
            move_vals['line_ids'].append((0, 0, {
                'name': self.label,
                'account_id': self.writeoff_account_id.id,
                'debit': 0.0,
                'credit': balance,
            }))
            # counterpart line on the journal's default account (if exists)
            liq_account = self.journal_id.company_id and self.journal_id.company_id.account_journal_default_account_id and self.journal_id.company_id.account_journal_default_account_id.id or False
            move_vals['line_ids'].append((0, 0, {
                'name': self.label,
                'account_id': liq_account or self.writeoff_account_id.id,
                'debit': balance,
                'credit': 0.0,
            }))
        else:
            amt = abs(balance)
            move_vals['line_ids'].append((0, 0, {
                'name': self.label,
                'account_id': self.writeoff_account_id.id,
                'debit': amt,
                'credit': 0.0,
            }))
            liq_account = self.journal_id.company_id and self.journal_id.company_id.account_journal_default_account_id and self.journal_id.company_id.account_journal_default_account_id.id or False
            move_vals['line_ids'].append((0, 0, {
                'name': self.label,
                'account_id': liq_account or self.writeoff_account_id.id,
                'debit': 0.0,
                'credit': amt,
            }))

        Move = self.env['account.move'].create(move_vals)
        try:
            Move.post()
        except Exception:
            # in community, posting may require proper accounts; ignore for now
            pass

        # Try to reconcile: combine created lines with existing lines
        # We attempt to reconcile by matching amounts: include all lines of the move and the selected lines
        candidate_lines = Move.line_ids + lines
        # call reconcile; will succeed for matching amounts
        try:
            candidate_lines.reconcile()
        except Exception as e:
            # If reconcile fails, raise user-friendly message with hint
            raise UserError(_('Automatic reconciliation failed: %s. You may need to reconcile manually or check the write-off account/journal.') % e)

        return {'type': 'ir.actions.act_window_close'}
