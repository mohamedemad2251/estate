from datetime import timedelta, datetime

import dateutil.utils
from dateutil.utils import today
from odoo import api,models,fields,exceptions

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Description for Estate Property Model"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False,  default=lambda self: (datetime.today() + timedelta(days=90)).date())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string = 'Orientation',
        selection= [('north','North'),('south','South'),('east','East'),('west','West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string = "State",
        selection = [('new','New'),('received','Offer Received'),('accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],
        required=True,
        copy=False,
        default='new'
    )

    property_type_id=fields.Many2one("estate.property.type", string="Property Type")
    salesman_id=fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id=fields.Many2one("res.partner", string="Buyer", copy="False", readonly=True)

    tag_ids=fields.Many2many("estate.property.tag")

    #estateoffer_id=fields.Many2one("estate.property.offer",string="Offer")
    offer_ids=fields.One2many("estate.property.offer","property_id",string="Offers")

    total_area=fields.Integer(readonly=True, compute="_sum_area", string="Total Area (sqm)")

    best_price=fields.Integer(compute="_get_best_price",readonly=True, default="0", string="Best Offer")

    _sql_constraints = [('positive_expected_price','CHECK (expected_price IS NULL OR expected_price > 0)','The expected price must be strictly positive!')]


    @api.depends("garden_area","living_area")
    def _sum_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _get_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default="0")

    @api.onchange("garden")
    def _garden_onchange(self):
        for record in self:
            if record.garden == True:
                record.garden_orientation = 'north'
                record.garden_area = "10"
            else:
                record.garden_orientation = None
                record.garden_area = None

    @api.ondelete(at_uninstall=False)
    def _validate_delete_new_cancelled(self):
        for record in self:
            if record.state == 'received' or record.state == 'accepted':
                raise exceptions.UserError('Only a new/cancelled property can be deleted!')

    def sold_button_action(self):
        for record in self:
            if record.state == 'accepted':
                record.state = 'sold'
            elif record.state == 'new':
                raise exceptions.UserError('No offers received yet for property to be sold! Please add offers & accept one first!')
            elif record.state == 'received':
                raise exceptions.UserError('Please accept an offer first or add a new one then accept it!')
            elif record.state == 'cancelled':
                raise exceptions.UserError('You cannot sell a cancelled property!')

    def cancel_button_action(self):
        for record in self:
            if record.state == 'new' or record.state == 'received' or record.state == 'accepted':
                record.state = 'cancelled'
            elif record.state == 'sold':
                raise exceptions.UserError("You cannot cancel a sold property!")
