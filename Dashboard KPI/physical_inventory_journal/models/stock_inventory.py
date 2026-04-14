# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    @api.model
    def _create_inventory_journal_entry(self, inventory):
        journal_id = self.env['account.journal'].search([('type','=','general')], limit=1).id
        opening_inventory_account = self.env['account.account'].search([('code','=','1400')], limit=1).id  # عدل حسب حسابك
        inventory_account_id = self.env['account.account'].search([('code','=','1200')], limit=1).id  # عدل حسب حسابك

        for line in inventory.line_ids:
            diff_qty = line.product_qty - line.theoretical_qty
            if diff_qty != 0:
                amount = diff_qty * line.product_id.standard_price
                self.env['account.move'].create({
                    'journal_id': journal_id,
                    'date': fields.Date.today(),
                    'line_ids': [
                        (0, 0, {
                            'account_id': inventory_account_id,
                            'debit': amount if amount > 0 else 0,
                            'credit': -amount if amount < 0 else 0,
                        }),
                        (0, 0, {
                            'account_id': opening_inventory_account,
                            'debit': -amount if amount < 0 else 0,
                            'credit': amount if amount > 0 else 0,
                        }),
                    ]
                })

    def action_validate(self):
        res = super(StockInventory, self).action_validate()
        self._create_inventory_journal_entry(self)
        return res
