from odoo import models, fields, _
from odoo.exceptions import UserError

class InternalTransferWizard(models.TransientModel):
    _name = 'internal.transfer.wizard'
    _description = 'Internal Transfer Wizard'

    source_journal_id = fields.Many2one('account.journal', string="من الحساب", required=True,
                                        domain=[('type','in',('cash','bank'))])
    destination_journal_id = fields.Many2one('account.journal', string="إلى الحساب", required=True,
                                             domain=[('type','in',('cash','bank'))])
    amount = fields.Monetary(string="المبلغ", required=True)
    currency_id = fields.Many2one('res.currency', string="العملة", required=True,
                                  default=lambda self: self.env.company.currency_id)
    date = fields.Date(string="التاريخ", required=True, default=fields.Date.context_today)
    note = fields.Text(string="البيان")

    def action_post(self):
        for rec in self:
            if rec.source_journal_id == rec.destination_journal_id:
                raise UserError(_("الحساب المصدر والوجهة يجب أن يكونا مختلفين."))

            transfer_account = rec.source_journal_id.company_id.transfer_account_id
            if not transfer_account:
                raise UserError(_("الرجاء تفعيل حساب Liquidity Transfer في إعدادات الشركة."))

            move_vals = {
                'date': rec.date,
                'ref': _('تحويل داخلي %s → %s') % (
                    rec.source_journal_id.name,
                    rec.destination_journal_id.name
                ),
                'line_ids': [
                    (0,0,{'account_id': rec.source_journal_id.default_account_id.id,'credit': rec.amount,'name': _('تحويل داخلي')}),
                    (0,0,{'account_id': rec.destination_journal_id.default_account_id.id,'debit': rec.amount,'name': _('تحويل داخلي')}),
                ]
            }

            move = self.env['account.move'].create(move_vals)
            move.action_post()
        return {'type': 'ir.actions.act_window_close'}
