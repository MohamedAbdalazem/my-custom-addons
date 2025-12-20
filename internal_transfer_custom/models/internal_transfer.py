from odoo import api, fields, models

class InternalTransfer(models.Model):
    _name = 'internal.transfer'
    _description = 'Internal Cash/Bank Transfer'

    name = fields.Char(string='Reference', default='New')
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)

    from_journal_id = fields.Many2one('account.journal', string='From Journal', domain=[('type', 'in', ['bank', 'cash'])], required=True)
    to_journal_id = fields.Many2one('account.journal', string='To Journal', domain=[('type', 'in', ['bank', 'cash'])], required=True)

    amount = fields.Float(string='Amount', required=True)

    move_id = fields.Many2one('account.move', string='Journal Entry')

    def action_transfer(self):
        for record in self:
            move = self.env['account.move'].create({
                'date': record.date,
                'ref': f"Internal Transfer: {record.name}",
                'journal_id': record.from_journal_id.id,
                'line_ids': [
                    (0, 0, {
                        'account_id': record.from_journal_id.default_account_id.id,
                        'credit': record.amount,
                        'debit': 0.0,
                    }),
                    (0, 0, {
                        'account_id': record.to_journal_id.default_account_id.id,
                        'debit': record.amount,
                        'credit': 0.0,
                    }),
                ]
            })

            move.action_post()
            record.move_id = move.id
            record.name = self.env['ir.sequence'].next_by_code('internal.transfer') or 'New'
