from odoo import models, fields

class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    cash_account_id = fields.Many2one('account.account', string='حساب الكاش', help='حساب النقدية الخاص بالفرع')
    bank_account_id = fields.Many2one('account.account', string='حساب البنك', help='حساب البنك الخاص بالفرع')
