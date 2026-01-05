from odoo import models, api, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    branch_id = fields.Many2one('res.branch', string='Branch')

    @api.onchange('branch_id')
    def _onchange_branch(self):
        for rec in self:
            if rec.branch_id and rec.branch_id.analytic_account_id:
                rec.analytic_account_id = rec.branch_id.analytic_account_id.id

    @api.model
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.branch_id:
            invoice_vals['branch_id'] = self.branch_id.id
            if self.branch_id.analytic_account_id:
                invoice_vals['analytic_account_id'] = self.branch_id.analytic_account_id.id
        return invoice_vals