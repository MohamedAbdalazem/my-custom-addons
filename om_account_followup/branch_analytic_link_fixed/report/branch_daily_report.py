from odoo import models, fields, api
from datetime import date
import io
import base64
import xlsxwriter

class BranchDailyReport(models.TransientModel):
    _name = 'branch.daily.report.wizard'
    _description = 'Daily Branch Report Wizard'

    report_date = fields.Date(string='Report Date', default=date.today)
    file_data = fields.Binary('File')
    file_name = fields.Char('Filename')

    def _get_branch_data(self):
        self.ensure_one()
        report_date = self.report_date

        moves = self.env['account.move.line'].search([
            ('date', '=', report_date),
            ('analytic_account_id', '!=', False)
        ])

        data = {}
        for line in moves:
            branch_name = line.analytic_account_id.name or 'غير محدد'
            if branch_name not in data:
                data[branch_name] = {'cash': 0.0, 'bank': 0.0, 'total': 0.0}

            name = line.account_id.name.lower()
            amount = line.debit - line.credit

            if 'cash' in name:
                data[branch_name]['cash'] += amount
            elif 'bank' in name:
                data[branch_name]['bank'] += amount
            else:
                data[branch_name]['total'] += amount

        return data

    def action_generate_report(self):
        data = self._get_branch_data()
        return self.env.ref('branch_analytic_link.action_branch_daily_report_pdf').report_action(
            self, data={'branches': data, 'date': self.report_date}
        )

    def action_export_excel(self):
        data = self._get_branch_data()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Daily Report')

        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        money_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        text_format = workbook.add_format({'border': 1})
        total_format = workbook.add_format({'bold': True, 'bg_color': '#FFFF99', 'border': 1, 'num_format': '#,##0.00'})

        sheet.write(0, 0, 'Branch', header_format)
        sheet.write(0, 1, 'Cash', header_format)
        sheet.write(0, 2, 'Bank', header_format)
        sheet.write(0, 3, 'Total', header_format)

        row = 1
        total_cash = total_bank = total_total = 0.0

        for branch, vals in data.items():
            sheet.write(row, 0, branch, text_format)
            sheet.write(row, 1, vals['cash'], money_format)
            sheet.write(row, 2, vals['bank'], money_format)
            sheet.write(row, 3, vals['total'], money_format)

            total_cash += vals['cash']
            total_bank += vals['bank']
            total_total += vals['total']
            row += 1

        # صف الإجمالي
        sheet.write(row, 0, 'TOTAL', header_format)
        sheet.write(row, 1, total_cash, total_format)
        sheet.write(row, 2, total_bank, total_format)
        sheet.write(row, 3, total_total, total_format)

        sheet.set_column('A:A', 25)
        sheet.set_column('B:D', 15)

        workbook.close()
        output.seek(0)
        xlsx_data = output.read()
        output.close()

        self.write({
            'file_data': base64.b64encode(xlsx_data),
            'file_name': f'Branch_Daily_Report_{self.report_date}.xlsx',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content/?model={self._name}&id={self.id}&field=file_data&download=true&filename={self.file_name}",
            'target': 'self',
        }


class ReportBranchDaily(models.AbstractModel):
    _name = 'report.branch_analytic_link.branch_daily_report_template'
    _description = 'Branch Daily Report Template'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {'data': data or {}}