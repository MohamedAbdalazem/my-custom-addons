# -*- coding: utf-8 -*-
from odoo import models

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        res = super().action_post()

        for payment in self:
            if (
                payment.is_internal_transfer
                and payment.destination_journal_id
                and payment.state == 'posted'
            ):
                company = payment.company_id
                transfer_account = company.transfer_account_id
                if not transfer_account:
                    continue

                move = self.env['account.move'].create({
                    'move_type': 'entry',
                    'journal_id': payment.destination_journal_id.id,
                    'date': payment.date,
                    'ref': f'Internal Transfer from {payment.journal_id.name}',
                    'line_ids': [
                        (0, 0, {
                            'name': 'Internal Transfer In',
                            'account_id': payment.destination_journal_id.default_account_id.id,
                            'debit': payment.amount,
                            'credit': 0.0,
                        }),
                        (0, 0, {
                            'name': 'Internal Transfer Out',
                            'account_id': transfer_account.id,
                            'debit': 0.0,
                            'credit': payment.amount,
                        }),
                    ],
                })
                move.action_post()

        return res
