from odoo import models, fields, api
from datetime import date

class BranchCashBankReport(models.TransientModel):
    _name = 'branch.cash.bank.report'
    _description = 'تقرير الكاش والبنك لكل فرع'

    date_from = fields.Date(string='من تاريخ', default=lambda self: date.today())
    date_to = fields.Date(string='إلى تاريخ', default=lambda self: date.today())
    branch_ids = fields.Many2many('account.analytic.account', string='الفروع')
    report_lines = fields.One2many('branch.cash.bank.line', 'wizard_id', string='التقرير')

    def generate_report(self):
        self.report_lines.unlink()
        branches = self.branch_ids or self.env['account.analytic.account'].search([])
        lines = []
        for branch in branches:
            # افتراض أن كل فرع له حساب كاش وحساب بنك مرتبطين
            cash_account = branch.cash_account_id
            bank_account = branch.bank_account_id

            cash_total = sum(self.env['account.move.line'].search([
                ('analytic_account_id', '=', branch.id),
                ('account_id', '=', cash_account.id if cash_account else False),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
            ]).mapped('balance'))

            bank_total = sum(self.env['account.move.line'].search([
                ('analytic_account_id', '=', branch.id),
                ('account_id', '=', bank_account.id if bank_account else False),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
            ]).mapped('balance'))

            lines.append((0, 0, {
                'branch_id': branch.id,
                'cash_total': cash_total,
                'bank_total': bank_total,
                'total': cash_total + bank_total
            }))
        self.report_lines = lines

class BranchCashBankLine(models.TransientModel):
    _name = 'branch.cash.bank.line'
    _description = 'سطر تقرير الكاش والبنك'

    wizard_id = fields.Many2one('branch.cash.bank.report')
    branch_id = fields.Many2one('account.analytic.account', string='الفرع')
    cash_total = fields.Monetary(string='كاش')
    bank_total = fields.Monetary(string='بنك')
    total = fields.Monetary(string='إجمالي الفرع')
