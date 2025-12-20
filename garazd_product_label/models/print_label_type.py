from odoo import fields, models


class PrintLabelTypePy(models.Model):
    _name = "print.label.type"
    _description = 'Label Types'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)

    _code_unique = models.Constraint('unique (code)', 'Code of a print label type must be unique.')
