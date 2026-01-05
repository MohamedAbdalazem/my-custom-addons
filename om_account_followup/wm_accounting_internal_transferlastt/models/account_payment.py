# -*- coding: utf-8 -*-
# Copyright 2025 Waleed Mohsen
# License OPL-1

from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # ---------------------------------------------------------------------
    # FIELDS
    # ---------------------------------------------------------------------
    is_internal_transfer = fields.Boolean(
        string="Internal Transfer",
        tracking=True
    )

    destination_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Destination Journal',
        domain="[('type', 'in', ('bank','cash')), ('id','!=', journal_id)]",
        check_company=True,
    )

    paired_internal_transfer_payment_id = fields.Many2one(
        'account.payment',
        string='Paired Internal Transfer',
        readonly=True,
        copy=False,
    )

    # ---------------------------------------------------------------------
    # LABELS
    # ---------------------------------------------------------------------
    def _get_aml_default_display_name_list(self):
        self.ensure_one()
        res = super()._get_aml_default_display_name_list()
        if self.is_internal_transfer:
            res[0] = ('label', _("Internal Transfer"))
        return res

    def _get_liquidity_aml_display_name_list(self):
        self.ensure_one()
        if self.is_internal_transfer:
            if self.payment_type == 'outbound':
                return [('transfer_to', _('Transfer to %s', self.destination_journal_id.name))]
            else:
                return [('transfer_from', _('Transfer from %s', self.journal_id.name))]
        return super()._get_liquidity_aml_display_name_list()

    # ---------------------------------------------------------------------
    # COMPUTES
    # ---------------------------------------------------------------------
    @api.depends('journal_id', 'is_internal_transfer')
    def _compute_partner_id(self):
        super()._compute_partner_id()
        for pay in self:
            if pay.is_internal_transfer:
                pay.partner_id = pay.company_id.partner_id

    @api.depends('journal_id', 'partner_id', 'partner_type',
                 'is_internal_transfer', 'destination_journal_id')
    def _compute_destination_account_id(self):
        super()._compute_destination_account_id()
        for pay in self:
            if pay.is_internal_transfer:
                pay.destination_account_id = (
                    pay.company_id.transfer_account_id
                    or pay.company_id.account_journal_suspense_account_id
                )

    # ---------------------------------------------------------------------
    # MOVE LINE LABEL FIX
    # ---------------------------------------------------------------------
    def _prepare_move_line_default_vals(self, write_off_line_vals=None, force_balance=None):
        self.ensure_one()
        lines = super()._prepare_move_line_default_vals(
            write_off_line_vals=write_off_line_vals,
            force_balance=force_balance
        )

        if self.is_internal_transfer and len(lines) >= 2:
            lines[0]['name'] = ''.join(
                x[1] for x in self._get_liquidity_aml_display_name_list()
            )
            lines[1]['name'] = _("Internal Transfer")

        return lines

    # ---------------------------------------------------------------------
    # SYNC
    # ---------------------------------------------------------------------
    @api.model
    def _get_trigger_fields_to_synchronize(self):
        res = super()._get_trigger_fields_to_synchronize()
        return res + ('is_internal_transfer',)

    # ---------------------------------------------------------------------
    # POST
    # ---------------------------------------------------------------------
    def action_post(self):
        res = super().action_post()
        self.filtered(
            lambda p: p.is_internal_transfer
            and not p.paired_internal_transfer_payment_id
        )._create_paired_internal_transfer_payment()
        return res

    # ---------------------------------------------------------------------
    # CREATE PAIRED PAYMENT
    # ---------------------------------------------------------------------
    def _create_paired_internal_transfer_payment(self):
        """
        Creates the inbound/outbound paired payment
        and reconciles both on transfer account
        """
        for payment in self:
            payment_type = (
                'inbound' if payment.payment_type == 'outbound' else 'outbound'
            )

            available_methods = payment.destination_journal_id._get_available_payment_method_lines(
                payment_type
            )
            payment_method_line = (
                available_methods[:1]._origin if available_methods else False
            )

            paired_payment = payment.copy({
                'journal_id': payment.destination_journal_id.id,
                'destination_journal_id': payment.journal_id.id,
                'payment_type': payment_type,
                'payment_method_line_id': payment_method_line.id if payment_method_line else False,
                'move_id': None,
                'date': payment.date,
                'paired_internal_transfer_payment_id': payment.id,
            })

            paired_payment.action_post()
            payment.paired_internal_transfer_payment_id = paired_payment

            # chatter
            payment.message_post(
                body=_("A paired internal transfer has been created: %s")
                % paired_payment._get_html_link()
            )
            paired_payment.message_post(
                body=_("Created from internal transfer: %s")
                % payment._get_html_link()
            )

            # reconciliation on transfer account
            lines = (
                payment.move_id.line_ids
                + paired_payment.move_id.line_ids
            ).filtered(
                lambda l: l.account_id == payment.destination_account_id and not l.reconciled
            )

            if lines:
                lines.reconcile()
