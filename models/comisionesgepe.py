# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartnerComisiones(models.Model):
    _inherit = 'res.partner'
    comisiones_id = fields.One2many('comisionesgp','clie_id',string='Vendedores y sus comisiones')

class GPVendedores(models.Model):
    _inherit ='res.users'
    #id_vendedor = fields.Many2one('comisionesgp')
    id_vendedor = fields.One2many('comisionesgp','vend_id')
class GPComisiones(models.Model):
    _name = 'comisionesgp'
    _description = 'Comisiones GP'
    clie_id = fields.Many2one('res.partner')
    #vend_id = fields.One2many('res.users','id_vendedor')
    vend_id = fields.Many2one('res.users',string='Vendedores')
    porc_com = fields.Float(Digits = (0,2),string='% Com sobre Rec.',required=False)
    fijo_com_recibo = fields.Float(Digits = (5,2),string = 'Imp Com por Recibo ',required= False)
    porc_com_factura = fields.Float(Digits = (0,2), string = '% Com sobre Fact', required=False)
    fijo_com_factura = fields.Float(Digits = (5,2), string = 'Importe Com sobre Fact', required=False)



class LineaPresupuesto(models.Model):
    _inherit = 'sale.order.line'
    descuento = fields.Float(Digits = (5,2), string='Descuento', readonly=True, compute='_get_last', store=True)
    total_bruto = fields.Float(Digits = (5,2), string = 'Total' , readonly=True, compute='_get_last', store=True)

    @api.depends('product_uom_qty', 'price_unit', 'discount')
    def _get_last(self):
        for record in self:
            record.descuento = record.product_uom_qty * record.price_unit * record.discount / 100
            record.total_bruto = record.product_uom_qty * record.price_unit
    """
        if self.product_uom_qty and self.price_unit and self.discount:
        self.descuento = self.price_unit * self.product_uom_qty * (self.discount/100)
        self.total_bruto = self.price_unit * self.product_uom_qty
    """

class MontoTotales(models.Model):
    _inherit = 'sale.order'
    total_descuentos = fields.Float(Digits = (5,2),string='Total Descontado', readonly=True, compute='_amount_all_gp', store=True)
    total_sin_descuentos = fields.Float(Digits = (5,2),string='Total Bruto', readonly=True, compute='_amount_all_gp', store=True)

    @api.depends('order_line.price_total')
    def _amount_all_gp(self):
        """
        Calculará el total de los descuentos y el importe bruto
        """
        for order in self:
            total_descuentos = total_descuentos = 0.0
            total_sin_descuentos = total_sin_descuentos = 0.0
            for line in order.order_line:
                total_descuentos += line.descuento
                total_sin_descuentos += line.total_bruto
                """
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                """
            order.update({
                'total_sin_descuentos': total_sin_descuentos,
                'total_descuentos' : total_descuentos,

            })
