from odoo import api, models, fields

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Description for Property Tags"
    _order="name"

    name=fields.Char(string="Tag", required=True)
    color=fields.Integer(string="Color")

    _sql_constraints = [('unique_tag_name','UNIQUE(name)','A property\'s tag name must be unique!')]

