# -*- coding:utf-8 -*-

from odoo import fields, models, api
import logging
from odoo.exceptions import UserError


class UpdateWizard(models.TransientModel):
    _name = "update.wizard"

    name = fields.Text(string="Nueva descripción")

    def update_desc(self):
        presupuesto_obj = self.env['presupuesto']
        # presupuesto_id = presupuesto_obj.search([('id', '=', self._context['active_id'])])
        presupuesto_id = presupuesto_obj.browse(self._context['active_id'])
        presupuesto_id.desc = self.name
