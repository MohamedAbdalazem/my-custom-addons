from odoo import models, fields, _
from odoo.exceptions import UserError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_internal_transfer = fields.Boolean(string="تحويل داخلي")
    destination_journal_id = fields.Many2one(
        'account.journal',
        string="إلى الحساب",
        domain=[('type', 'in', ('bank', 'cash'))]
    )

    def action_post(self):
        for payment in self:
            if payment.is_internal_transfer:
                if not payment.destination_journal_id:
                    raise UserError(_("الرجاء اختيار الحساب الوجهة."))

                if payment.journal_id == payment.destination_journal_id:
                    raise UserError(_("الحساب المصدر والوجهة يجب أن يكونا مختلفين."))

                transfer_account = payment.journal_id.company_id.transfer_account_id
                if not transfer_account:
                    raise UserError(_("الرجاء تفعيل حساب Liquidity Transfer في إعدادات الشركة."))

                move_vals = {
                    'date': payment.date,
                    'ref': _('تحويل داخلي %s → %s') % (
                        payment.journal_id.name,
                        payment.destination_journal_id.name
                    ),
                    'line_ids': [
                        (0, 0, {
                            'account_id': payment.journal_id.default_account_id.id,
                            'credit': payment.amount,
                            'name': _('تحويل داخلي'),
                        }),
                        (0, 0, {
                            'account_id': payment.destination_journal_id.default_account_id.id,
                            'debit': payment.amount,
                            'name': _('تحويل داخلي'),
                        }),
                    ],
                }

                move = self.env['account.move'].create(move_vals)
                move.action_post()
                payment.state = 'posted'
            else:
                super(AccountPayment, payment).action_post()
        return True
