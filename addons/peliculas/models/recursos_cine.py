# -*- coding:utf-8 -*-
from odoo import fields, models, api
import logging


class RecursosCine(models.Model):
    _name = "recursos.cine"

    name = fields.Char(string="Recursos")
    description = fields.Char(string="Descripción")
    prize = fields.Float(string="Precio")
    contacto_id = fields.Many2one(
        comodel_name='res.partner',
        domain="[('is_company', '=', False)]"
    )
    image = fields.Binary(string="Imagen")

