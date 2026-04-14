from odoo import api, fields, models

class DailySalesReportLine(models.TransientModel):
    _name = 'daily.sales.report.line'
    _description = 'Daily Sales Report Line'

    wizard_id = fields.Many2one('daily.sales.report.wizard', string='Wizard', ondelete='cascade')
    date = fields.Date(string='Date')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    customer_id = fields.Many2one('res.partner', string='Customer')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Branch')
    currency_id = fields.Many2one('res.currency', string='Currency')
    total = fields.Monetary(string='Total', currency_field='currency_id')
    paid = fields.Monetary(string='Paid', currency_field='currency_id')
    balance = fields.Monetary(string='Balance', currency_field='currency_id')
    payment_method = fields.Char(string='Payment Method')

class DailySalesReportWizard(models.TransientModel):
    _name = 'daily.sales.report.wizard'
    _description = 'Daily Sales Report Wizard'

    date_from = fields.Date(string='Start Date', required=True, default=fields.Date.context_today)
    date_to = fields.Date(string='End Date', required=True, default=fields.Date.context_today)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Branch', required=True)
    line_ids = fields.One2many('daily.sales.report.line', 'wizard_id', string='Report Lines')

    def compute_report(self):
        self.ensure_one()
        self.line_ids.unlink()
        invoices = self.env['account.move'].search([
            ('move_type','=','out_invoice'),
            ('invoice_date','>=',self.date_from),
            ('invoice_date','<=',self.date_to),
            ('analytic_account_id','=',self.analytic_account_id.id),
            ('state','in',['posted'])
        ])
        lines = []
        for inv in invoices:
            lines.append((0,0,{
                'date': inv.invoice_date,
                'invoice_id': inv.id,
                'customer_id': inv.partner_id.id,
                'analytic_account_id': inv.analytic_account_id.id,
                'currency_id': inv.currency_id.id,
                'total': inv.amount_total,
                'paid': inv.amount_total - inv.amount_residual,
                'balance': inv.amount_residual,
                'payment_method': inv.payment_reference or '',
            }))
        self.line_ids = lines

    def action_view_report(self):
        self.compute_report()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'daily.sales.report.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def export_csv(self):
        import io, base64, csv
        self.compute_report()
        lines = self.line_ids.sorted(key=lambda r: r.date or '')
        fp = io.StringIO()
        writer = csv.writer(fp)
        writer.writerow(['Date','Branch','Invoice','Customer','Total','Paid','Balance','Payment Method'])
        for l in lines:
            writer.writerow([
                l.date or '',
                l.analytic_account_id.display_name or '',
                l.invoice_id.name or '',
                l.customer_id.display_name or '',
                float(l.total or 0.0),
                float(l.paid or 0.0),
                float(l.balance or 0.0),
                l.payment_method or '',
            ])
        csv_data = fp.getvalue().encode('utf-8')
        attachment = self.env['ir.attachment'].create({
            'name': 'daily_sales_report_%s_%s.csv' % (self.date_from, self.date_to),
            'type': 'binary',
            'datas': base64.b64encode(csv_data),
            'mimetype': 'text/csv',
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }
