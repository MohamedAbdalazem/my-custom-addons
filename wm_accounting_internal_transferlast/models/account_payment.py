# -*- coding: utf-8 -*-
# Copyright 2025 Waleed Mohsen. (<https://wamodoo.com/>)
# License OPL-1

from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_internal_transfer = fields.Boolean(
        string="Internal Transfer",
        tracking=True
    )

    destination_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Destination Journal',
        domain="[('type', 'in', ('bank', 'cash')), ('id', '!=', journal_id)]",
        check_company=True,
    )

    use_paired_internal_transfer = fields.Boolean(
        string="Create Paired Internal Transfer",
        default=False,
        help="If enabled, a second payment will be created automatically. "
             "Recommended to disable when using base_accounting_kit."
    )

    # -------------------------------------------------------------------------
    # INTERNAL TRANSFER ACCOUNT (Compatible with base_accounting_kit)
    # -------------------------------------------------------------------------
    def _get_internal_transfer_account(self):
        self.ensure_one()
        company = self.company_id
        return (
            company.transfer_account_id
            or company.account_journal_suspense_account_id
            or self.journal_id.default_account_id
        )

    # -------------------------------------------------------------------------
    # LABELS
    # -------------------------------------------------------------------------
    def _get_aml_default_display_name_list(self):
        self.ensure_one()
        result = super()._get_aml_default_display_name_list()
        if self.is_internal_transfer:
            result[0] = ('label', _("Internal Transfer"))
        return result

    def _get_liquidity_aml_display_name_list(self):
        self.ensure_one()
        if self.is_internal_transfer:
            if self.payment_type == 'outbound':
                return [('transfer_to', _('Transfer to %s', self.destination_journal_id.name))]
            else:
                return [('transfer_from', _('Transfer from %s', self.journal_id.name))]
        return super()._get_liquidity_aml_display_name_list()

    # -------------------------------------------------------------------------
    # COMPUTES
    # -------------------------------------------------------------------------
    @api.depends('partner_id', 'company_id', 'payment_type',
                 'destination_journal_id', 'is_internal_transfer')
    def _compute_available_partner_bank_ids(self):
        super()._compute_available_partner_bank_ids()
        for pay in self:
            if pay.is_internal_transfer:
                pay.available_partner_bank_ids = (
                    pay.destination_journal_id.bank_account_id
                )

    @api.depends('journal_id', 'partner_id', 'partner_type',
                 'is_internal_transfer', 'destination_journal_id')
    def _compute_destination_account_id(self):
        super()._compute_destination_account_id()
        for pay in self:
            if pay.is_internal_transfer:
                pay.destination_account_id = pay._get_internal_transfer_account()

    @api.depends('journal_id', 'is_internal_transfer')
    def _compute_partner_id(self):
        super()._compute_partner_id()
        for pay in self:
            if pay.is_internal_transfer:
                pay.partner_id = pay.company_id.partner_id

    # -------------------------------------------------------------------------
    # MOVE LINES
    # -------------------------------------------------------------------------
    def _prepare_move_line_default_vals(self, write_off_line_vals=None, force_balance=None):
        self.ensure_one()
        line_vals_list = super()._prepare_move_line_default_vals(
            write_off_line_vals=write_off_line_vals,
            force_balance=force_balance
        )

        if self.is_internal_transfer and len(line_vals_list) >= 2:
            liquidity_name = ''.join(x[1] for x in self._get_liquidity_aml_display_name_list())
            counterpart_name = _("Internal Transfer (%s → %s)") % (
                self.journal_id.name,
                self.destination_journal_id.name
            )
            line_vals_list[0]['name'] = liquidity_name
            line_vals_list[1]['name'] = counterpart_name

        return line_vals_list

    # -------------------------------------------------------------------------
    # COPY
    # -------------------------------------------------------------------------
    def copy_data(self, default=None):
        default = dict(default or {})
        vals_list = super().copy_data(default)
        for payment, vals in zip(self, vals_list):
            if not payment.is_internal_transfer:
                vals.update({
                    'journal_id': payment.journal_id.id,
                    'payment_method_line_id': payment.payment_method_line_id.id,
                })
        return vals_list

    # -------------------------------------------------------------------------
    # SYNC
    # -------------------------------------------------------------------------
    @api.model
    def _get_trigger_fields_to_synchronize(self):
        res = super()._get_trigger_fields_to_synchronize()
        res += ('is_internal_transfer',)
        return res

    # -------------------------------------------------------------------------
    # POST
    # -------------------------------------------------------------------------
    def action_post(self):
        res = super().action_post()
        self.filtered(
            lambda p: p.is_internal_transfer
            and p.use_paired_internal_transfer
            and not p.paired_internal_transfer_payment_id
        )._create_paired_internal_transfer_payment()
        return res

    # -------------------------------------------------------------------------
    # PAIRED PAYMENT (OPTIONAL)
    # -------------------------------------------------------------------------
    def _create_paired_internal_transfer_payment(self):
        for payment in self:
            payment_type = 'inbound' if payment.payment_type == 'outbound' else 'outbound'

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
                'paired_internal_transfer_payment_id': payment.id,
                'date': payment.date,
            })

            paired_payment.action_post()
            payment.paired_internal_transfer_payment_id = paired_payment

            body = _("This payment has been created from: ") + payment._get_html_link()
            paired_payment.message_post(body=body)

            body = _("A second payment has been created: ") + paired_payment._get_html_link()
            payment.message_post(body=body)

            lines = (
                payment.move_id.line_ids + paired_payment.move_id.line_ids
            ).filtered(
                lambda l: l.account_id == payment.destination_account_id and not l.reconciled
            )

            if lines and len(lines.mapped('account_id')) == 1:
                lines.reconcile()
