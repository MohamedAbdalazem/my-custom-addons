from odoo import models, fields, api
from datetime import date

class BranchCashBankLine(models.TransientModel):
    _name = 'branch.cash.bank.line'
    _description = 'سطر تقرير الكاش والبنك لكل فرع / Branch Cash Bank Line'

    wizard_id = fields.Many2one('branch.cash.bank.wizard', string='Wizard')
    branch_id = fields.Many2one('account.analytic.account', string='الفرع / Branch')
    cash_total = fields.Monetary(string='رصيد الكاش / Cash Balance', currency_field='currency_id')
    bank_total = fields.Monetary(string='رصيد البنك / Bank Balance', currency_field='currency_id')
    total = fields.Monetary(string='إجمالي الفرع / Branch Total', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='العملة', default=lambda self: self.env.company.currency_id.id)


class BranchCashBankReport(models.TransientModel):
    _name = 'branch.cash.bank.report'
    _description = 'تقرير الكاش والبنك لكل فرع (تجميعي) / Branch Cash Bank Report'

    date_to = fields.Date(string='حتى تاريخ / Date to', required=True, default=lambda self: date.today())
    branch_ids = fields.Many2many('account.analytic.account', string='الفروع / Branches')
    report_line_ids = fields.One2many('branch.cash.bank.line', 'wizard_id', string='التفاصيل / Lines')
    currency_id = fields.Many2one('res.currency', string='العملة', default=lambda self: self.env.company.currency_id.id)

    def _get_balance_for(self, account_id, analytic_id, date_to):
        if not account_id:
            return 0.0
        domain = [
            ('account_id', '=', account_id.id),
            ('analytic_account_id', '=', analytic_id.id),
            ('date', '<=', date_to),
        ]
        lines = self.env['account.move.line'].search(domain)
        # استخدام الحقل 'balance' (debit - credit)
        return sum(lines.mapped('balance'))

    def generate_report(self):
        # ينتج report_line_ids ويعيد action لفتح العرض
        self.ensure_one()
        # حذف القديمة
        self.report_line_ids.unlink()
        branches = self.branch_ids or self.env['account.analytic.account'].search([])
        lines = []
        total_company_cash = 0.0
        total_company_bank = 0.0
        for br in branches:
            cash_acc = br.cash_account_id
            bank_acc = br.bank_account_id
            cash_balance = self._get_balance_for(cash_acc, br, self.date_to) if cash_acc else 0.0
            bank_balance = self._get_balance_for(bank_acc, br, self.date_to) if bank_acc else 0.0
            total = cash_balance + bank_balance
            total_company_cash += cash_balance
            total_company_bank += bank_balance
            lines.append((0, 0, {
                'branch_id': br.id,
                'cash_total': cash_balance,
                'bank_total': bank_balance,
                'total': total,
                'currency_id': self.currency_id.id
            }))
        # سجّل السطور
        self.report_line_ids = lines
        # نحتفظ بالمجاميع في سجل مؤقت لعرضها في التقرير عبر context
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'branch.cash.bank.report',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
        return action
