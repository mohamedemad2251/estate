from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Description for Property Types"
    _order="sequence asc, name"

    name=fields.Char(string="Type", required=True)
    property_ids=fields.One2many("estate.property","property_type_id",string="Properties")
    sequence=fields.Integer(default="1", help="Ordering sequence. The less the number, the higher up it is.", string='Sequence')

    offer_ids=fields.One2many("estate.property.offer","property_type_id",string="Offer ID")
    offer_count = fields.Integer(compute="_increment_offer_count", store=True, default=0)

    @api.depends("offer_ids")
    def _increment_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)  # Count the actual number of offers directly

    def offers_stat_button_action(self):
        pass