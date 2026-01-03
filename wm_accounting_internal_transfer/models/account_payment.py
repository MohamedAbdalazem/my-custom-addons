# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_internal_transfer = fields.Boolean(
        string="Internal Transfer",
        default=False
    )

    destination_journal_id = fields.Many2one(
        'account.journal',
        string='Destination Journal',
        domain="[('type', 'in', ('bank','cash')), ('id', '!=', journal_id)]",
        check_company=True
    )

    paired_internal_transfer_payment_id = fields.Many2one(
        'account.payment',
        string='Paired Internal Transfer',
        readonly=True,
        copy=False
    )

    @api.depends('journal_id', 'is_internal_transfer', 'destination_journal_id')
    def _compute_destination_account_id(self):
        super()._compute_destination_account_id()
        for payment in self:
            if (
                payment.is_internal_transfer
                and payment.destination_journal_id
                and payment.destination_journal_id.company_id.transfer_account_id
            ):
                payment.destination_account_id = (
                    payment.destination_journal_id.company_id.transfer_account_id
                )

    @api.depends('partner_id', 'company_id', 'payment_type', 'is_internal_transfer')
    def _compute_partner_id(self):
        super()._compute_partner_id()
        for payment in self:
            if payment.is_internal_transfer:
                payment.partner_id = payment.company_id.partner_id
