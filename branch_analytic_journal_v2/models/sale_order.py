from odoo import models, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        journal = self.fiscal_position_id.journal_id or self.company_id.default_journal_id
        if journal and journal.analytic_account_id:
            invoice_vals['invoice_line_ids'] = [
                (0, 0, {
                    'name': line.name,
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'product_id': line.product_id.id,
                    'account_id': line.account_id.id,
                    'analytic_account_id': journal.analytic_account_id.id,
                }) for line in self.order_line
            ]
        return invoice_vals
