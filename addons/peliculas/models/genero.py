# -*- coding:utf-8 -*-
from odoo import fields, models, api


class Genero(models.Model):
    _name = "gender"

    name = fields.Char()
