from odoo import models, api

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        res = super().action_post()
        self._safe_auto_reconcile_internal_transfer()
        return res

    def _safe_auto_reconcile_internal_transfer(self):
        for payment in self:
            if not payment.is_internal_transfer or not payment.move_id:
                continue

            lines = payment.move_id.line_ids.filtered(
                lambda l: l.account_id.reconcile and not l.reconciled
            )

            if not lines or len(lines) < 2:
                continue

            account_ids = set(lines.mapped('account_id').ids)
            if len(account_ids) != 1:
                continue

            try:
                lines.reconcile()
            except Exception:
                continue
