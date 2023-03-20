# -*- coding:utf-8 -*-
from odoo import fields, models, api
import logging
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class Presupuesto(models.Model):
    _name = "presupuesto"
    _inherit = ['image.mixin']  # Hereda modelo de binarios

    name = fields.Char(string='Película')
    desc = fields.Text(
        string='Description',
        required=False)
    premier = fields.Date(string='Estreno')
    age_class = fields.Selection(selection=[
        ('', ''),  # Primer valor bd, segundo se muestra al usuario
        ('TP', 'Todos los Públicos'),  # Primer valor bd, segundo se muestra al usuario
        ('+7', 'Mayores de 7 años'),
        ('+13', 'Mayores de 13 años'),
        ('+18', 'Mayores de 18 años'),
    ], string='Clasificación')
    dsc_age_class = fields.Char()
    active = fields.Boolean(default='True')
    score = fields.Integer(string='Puntuación', related='score2')
    score2 = fields.Integer(string='Puntuación2')
    director_id = fields.Many2one(  # relaciona la tabla res_partner(la de los contactos) con presupuesto.
        comodel_name="res.partner"
    )
    category_director_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoría Director',
        default=lambda self: self.env.ref('peliculas.category_director')

        #default=lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')])
    )
    gender_ids = fields.Many2many(
        comodel_name="gender",
        string='Género'
    )
    is_book = fields.Boolean(string='Es un libro')
    book = fields.Binary(string='Libro')
    libro_filename = fields.Char(string='Nombre del libro')
    link_trailer = fields.Char()
    state = fields.Selection(selection=[
        ('B', 'Borrador'),  # Primer valor bd, segundo se muestra al usuario, copy es para que cuando dupliques un presupuesto no dupliques el estado
        ('A', 'Aprobado'),
        ('C', 'Cancelado')
    ], default='B', string='Estados', copy=False)
    f_aprobado = fields.Date(
        string='Fecha aprobación',
        copy=False)
    f_creacion = fields.Datetime(string='Fecha creación', copy=False, default=lambda self: fields.Datetime.now())
    n_presupuesto = fields.Char(string='Nº Presupuesto', copy=False)
    actor_ids = fields.Many2many(  # relaciona la tabla res_partner(la de los contactos) con presupuesto.
        comodel_name="res.partner",
        string="Actores"
    )
    category_actor_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoría Actor',
        default=lambda self: self.env.ref('peliculas.category_actor')
    )
    opinion = fields.Html(string='Críticas')
    detalle_ids = fields.One2many(
        comodel_name='presupuesto.detalle',
        inverse_name='presupuesto_id',
        string='Detalles',
    )
    campos_ocultos = fields.Boolean(string="Campos ocultos")

    def aprobar_presupuesto(self):
        logging.error('+++++++++++++++++++++++++')
        self.state = 'A'
        self.f_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        self.state = 'C'

    def unlink(self):
        logger.error('+++++++++++ENTRA++++++++')
        for rec in self:
            if rec.state != 'C':
                raise UserError('El estado tiene que ser cancelado')
        super(Presupuesto, self).unlink()

    @api.model
    def create(self, variables):
        # Para ver qué data llega a la función
        logging.error('+++++++++++++Variables: {0}'.format(variables))
        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('peliculas.presupuesto.seq')
        variables['n_presupuesto'] = correlativo
        return super(Presupuesto, self).create(variables)

    # Evitar que el usuario pueda editar la clasificación de una película
    def write(self, variables):
        # Para ver qué data llega a la función
        logging.error('+++++++++++++Variables: {0}'.format(variables))
        if 'age_class' in variables:
            raise UserError('No puedes cambiar la clasificación una vez creada')
        return super(Presupuesto, self).write(variables)

    # Poner (Copia) en el nombre de la peli copiada, primero creamos un dic con las variables default o creando un dic
    # vacío si no hay variables. Definimos que la variable nombre se le va a añadior (copia) y la puntuación en 1.
    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (Copia)'
        default['score2'] = 1
        return super(Presupuesto, self).copy(default)

    #En OnChange tienes que poner la variable que tiene que escuchar para ver cuando cambie su valor
    @api.onchange('age_class')
    def _onchange_age_class(self):
        #Si existe clasificación
        if self.age_class:
            if self.age_class == 'TP':
                self.dsc_age_class = 'Todos los públicos'
            if self.age_class == '+7':
                self.dsc_age_class = 'Mayores de 7 años'
            if self.age_class == '+13':
                self.dsc_age_class = 'Mayores de 13 años'
            if self.age_class == '+18':
                self.dsc_age_class = 'Mayores de 18 años'
        else:
            self.age_class = False


class PresupuestoDetalle(models.Model):
    _name = "presupuesto.detalle"

    presupuesto_id = fields.Many2one(
        comodel_name="presupuesto",
        string="Presupuesto",
    )

    name = fields.Many2one(
        comodel_name="recursos.cine",
        string="Recurso",
    )
    des_r_cine = fields.Char(string="Descripción", related="name.description")
    prize_r_cine = fields.Float(string="Precio")
    contact_r_cine = fields.Many2one(
        comodel_name='res.partner',
        string="Contacto",
        related="name.contacto_id")
    image_r_cine = fields.Binary(string="Imagen", related="name.image")
    quantity = fields.Float(string="Cantidad",default=1.0, digits=(4, 1))# 1 decimales y un max total de 4 digitos contando con los decimales si colocamos 0, 0 será ilimitado
    total_amount = fields.Float(string='Importe total')

    @api.onchange('name')
    def _onchange_price(self):
        if self.name:
            self.prize_r_cine = self.name.prize

    @api.onchange('quantity', 'prize_r_cine')
    def _onchange_total_prize(self):
        if self.name:
            self.total_amount = self.quantity * self.prize_r_cine