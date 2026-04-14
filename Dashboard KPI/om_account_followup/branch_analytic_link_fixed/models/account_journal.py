from odoo import models, fields

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    branch_id = fields.Many2one('res.branch', string='Branch')
    branch_analytic_account_id = fields.Many2one(
        related='branch_id.analytic_account_id',
        string='Branch Analytic Account',
        store=True,
        readonly=False
    )