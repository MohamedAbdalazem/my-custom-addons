from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='الحساب التحليلي للشركة',
        help='الحساب التحليلي الافتراضي المرتبط بهذه الشركة.'
    )
