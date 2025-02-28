from odoo import fields, models, api, exceptions
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime


class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Description for Property Offers"
    _order="price desc"

    price=fields.Float()
    status=fields.Selection(
        copy=False,
        selection=[('accepted','Accepted'),('refused','Refused')]
    )
    partner_id=fields.Many2one("res.partner",string="Partner",required=True)
    property_id=fields.Many2one("estate.property",string="Property",required=True)

    validity = fields.Integer(default="7", string="Valid After (Days)")
    date_deadline = fields.Date(compute="_get_date_deadline",inverse="_get_validity")

    property_id=fields.Many2one("estate.property",string="Property Attached To Offer")

    property_type_id=fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [('positive_offer_price','CHECK (price IS NULL OR price > 0)','The offer\'s price must be strictly positive!')]

    @api.depends("validity","create_date")
    def _get_date_deadline(self):
       for record in self:
           if not record.create_date or not isinstance(record.create_date, datetime):
               record.date_deadline = False
           else:
               if record.validity:
                   record.date_deadline = (record.create_date + timedelta(days=record.validity)).date()
               else:
                   record.date_deadline = False


    @api.depends("date_deadline","create_date")
    def _get_validity(self):
        for record in self:
            if not record.create_date or not isinstance(record.create_date, datetime):
                record.validity = False
            else:
                if record.create_date and record.date_deadline:
                    record.validity = (record.date_deadline - record.create_date.date()).days
                else:
                    record.validity = False

    def accept_offer_action(self):
        for record in self:
            if record.status is False:
                    record.status = 'accepted'
                    record.property_id.state = 'accepted'
                    record.property_id.selling_price = record.price
                    record.property_id.buyer_id = record.partner_id
            elif record.status == 'refused':
                raise exceptions.UserError('You cannot accept a declined offer!')

    def decline_offer_action(self):
        for record in self:
            if record.status == False:
                record.status = 'refused'
            elif record.status == 'accepted':
                raise exceptions.UserError('You cannot decline an accepted offer!')

    @api.constrains("price")
    def _check_price(self):
        for record in self:
            if record.price < 0.9 * record.property_id.expected_price:
                raise ValidationError("The selling price must be at least 90% of the expected price!")
            if record.property_id.best_price:
                if record.price < record.property_id.best_price:
                    raise exceptions.UserError(f"Price must be higher than {record.property_id.best_price}.")
            record.property_id.state = 'received'