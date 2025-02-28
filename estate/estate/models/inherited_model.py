from odoo import api, models, fields

class EstateSalesmanUser(models.Model):
    _inherit='res.users'

    property_id=fields.One2many('estate.property','salesman_id','Property\'s Salesman', domain=['|',('state','=','new'),('state','=','received')])
