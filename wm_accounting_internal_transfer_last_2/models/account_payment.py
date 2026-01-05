from odoo import models, fields, api, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_internal_transfer = fields.Boolean(string="Internal Transfer")
    destination_journal_id = fields.Many2one(
        'account.journal',
        string="Destination Journal",
        domain=[('type', 'in', ('bank', 'cash'))]
    )

    def action_post(self):
        res = super().action_post()
        for payment in self:
            if payment.is_internal_transfer and payment.destination_journal_id:
                vals = {
                    'payment_type': 'inbound',
                    'partner_type': 'customer',
                    'amount': payment.amount,
                    'journal_id': payment.destination_journal_id.id,
                    'date': payment.date,
                    'ref': _('Internal Transfer from %s') % payment.journal_id.name,
                }
                inbound = self.env['account.payment'].create(vals)
                inbound.action_post()
        return res
