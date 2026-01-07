from odoo import models, api

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def create(self, vals):
        payment = super().create(vals)
        payment._auto_reconcile_internal_transfer()
        return payment

    def action_post(self):
        res = super().action_post()
        self._auto_reconcile_internal_transfer()
        return res

    def _auto_reconcile_internal_transfer(self):
        for payment in self:
            if payment.is_internal_transfer and payment.move_id:
                lines = payment.move_id.line_ids.filtered(
                    lambda l: l.account_id.reconcile and not l.reconciled
                )
                if len(lines) >= 2:
                    lines.reconcile()
