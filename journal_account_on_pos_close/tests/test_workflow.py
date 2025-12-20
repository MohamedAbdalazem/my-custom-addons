# -*- coding: utf-8 -*-

from odoo.addons.point_of_sale.tests.common import TestPoSCommon


class TestPoSCommon(TestPoSCommon):

    def setUp(self):
        res = super(TestPoSCommon, self).setUp()
        self.config = self.basic_config
        self.product1 = self.create_product('Product 1', self.categ_basic, 10.0, 5)
        self.product2 = self.create_product('Product 2', self.categ_basic, 20.0, 10)
        self.product3 = self.create_product('Product 3', self.categ_basic, 30.0, 15)

        self.account_product_id = self.env['account.account'].create({
            'name': 'Account Product',
            'code': 'account_product',
            'user_type_id': self.env.ref('account.data_account_type_revenue').id,
        })
        self.account_journal_id = self.env['account.account'].create({
            'name': 'Account Journal',
            'code': 'account_journal',
            'user_type_id': self.env.ref('account.data_account_type_revenue').id,
        })
        self.journal_without_account_id = self.env['account.journal'].create({
            'name': 'Journal without account',
            'type': 'sale',
            'code': 'test',
        })
        self.journal_with_account_id = self.env['account.journal'].create({
            'name': 'Journal with account',
            'type': 'sale',
            'code': 'test2',
            'default_account_id': self.account_journal_id.id,
        })

        self.product3.property_account_income_id = self.account_product_id
        self.config.journal_id = self.journal_with_account_id
        return res

    def test_use_pos_journal_account(self):
        self.open_new_session()

        # create orders
        orders = [
            self.create_ui_order_data(
                [(self.product3, 1), (self.product1, 6), (self.product2, 3)],
                payments=[(self.cash_pm, 150)],
                customer=self.customer,
                is_invoiced=True,
            ),
        ]

        # sync orders
        self.env['pos.order'].create_from_ui(orders)

        # close the session
        self.pos_session.action_pos_session_validate()

        order_move = self.pos_session.order_ids.account_move
        print(order_move.invoice_line_ids.mapped('product_id.name'))
        print(order_move.invoice_line_ids.mapped('account_id.name'))
        product_lines = order_move.line_ids.filtered(lambda l: l.product_id in [self.product1, self.product2, self.product3])
        self.assertEqual(all([l.account_id == self.account_journal_id for l in product_lines]), True)

