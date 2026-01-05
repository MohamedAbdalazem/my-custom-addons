from odoo import models, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def action_manual_reconcile(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manual Reconciliation',
            'res_model': 'account.move.line',
            'view_mode': 'tree',
            'domain': [('reconciled', '=', False)],
            'target': 'current',
        }
