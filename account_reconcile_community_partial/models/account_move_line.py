from odoo import models, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def action_manual_reconcile(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manual Reconciliation',
            'res_model': 'account.move.line',
            'view_mode': 'tree,form',
            'domain': [('reconciled', '=', False)],
            'target': 'current',
        }

    def action_open_partial_reconcile_wizard(self):
        # Open wizard with selected lines
        context = dict(self.env.context or {})
        active_ids = self.ids
        return {
            'name': 'Partial Reconcile (Write-Off)',
            'type': 'ir.actions.act_window',
            'res_model': 'account.partial.reconcile.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': dict(context, active_ids=active_ids),
        }
