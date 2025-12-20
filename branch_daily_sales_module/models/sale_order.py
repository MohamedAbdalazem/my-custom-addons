from odoo import models, fields, api
from datetime import date

class BranchDailySales(models.TransientModel):
    _name = 'branch.daily.sales'
    _description = 'تقرير المبيعات اليومي لكل فرع'

    branch_id = fields.Many2one('account.analytic.account', string='الفرع')
    date_from = fields.Date(string='من تاريخ', default=date.today)
    date_to = fields.Date(string='إلى تاريخ', default=date.today)
    total_sales = fields.Float(string='إجمالي المبيعات', compute='_compute_total_sales')

    @api.depends('branch_id', 'date_from', 'date_to')
    def _compute_total_sales(self):
        for record in self:
            record.total_sales = record._calculate_sales()

    def _calculate_sales(self):
        """حساب إجمالي المبيعات"""
        self.ensure_one()
        if not self.branch_id:
            return 0.0
        domain = [
            ('analytic_account_id', '=', self.branch_id.id),
            ('state', 'in', ['sale', 'done']),
            ('date_order', '>=', self.date_from),
            ('date_order', '<=', self.date_to)
        ]
        orders = self.env['sale.order'].search(domain)
        return sum(orders.mapped('amount_total'))

    def action_update_sales(self):
        """زر لتحديث المبيعات"""
        for record in self:
            record.total_sales = record._calculate_sales()
        return True
