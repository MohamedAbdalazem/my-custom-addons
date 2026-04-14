from odoo import models, fields

class ResBranch(models.Model):
    _name = 'res.branch'
    _description = 'Company Branch'

    name = fields.Char(string='Branch Name', required=True)
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        help='Analytic account assigned to this branch.'
    )