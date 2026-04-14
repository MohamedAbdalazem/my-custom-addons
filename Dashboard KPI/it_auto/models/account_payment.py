# -*- coding: utf-8 -*-
from odoo import models

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        res = super().action_post()

        for payment in self:
            if not (
                payment.is_internal_transfer
                and payment.destination_journal_id
                and payment.state == 'posted'
            ):
                continue

            company = payment.company_id
            transfer_account = company.transfer_account_id
            if not transfer_account:
                continue

            dest_account = payment.destination_journal_id._get_default_account()
            if not dest_account:
                continue

            ref = f'Auto Internal Transfer from {payment.name}'
            if self.env['account.move'].search([
                ('ref', '=', ref),
                ('company_id', '=', company.id),
            ], limit=1):
                continue

            move = self.env['account.move'].create({
                'move_type': 'entry',
                'journal_id': payment.destination_journal_id.id,
                'date': payment.date,
                'ref': ref,
                'line_ids': [
                    (0, 0, {
                        'name': 'Internal Transfer In',
                        'account_id': dest_account.id,
                        'debit': payment.amount,
                        'credit': 0.0,
                    }),
                    (0, 0, {
                        'name': 'Internal Transfer Clear',
                        'account_id': transfer_account.id,
                        'debit': 0.0,
                        'credit': payment.amount,
                    }),
                ],
            })
            move.action_post()

        return res
