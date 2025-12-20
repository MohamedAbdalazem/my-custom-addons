from odoo import models, fields

class ResBranch(models.Model):
    _inherit = 'res.branch'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='الحساب التحليلي للفرع',
        help='الحساب التحليلي الافتراضي المرتبط بهذا الفرع.'
    )
