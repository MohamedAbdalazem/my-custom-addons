from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    branch_id = fields.Many2one('account.analytic.account', string='Branch Analytic Account')
