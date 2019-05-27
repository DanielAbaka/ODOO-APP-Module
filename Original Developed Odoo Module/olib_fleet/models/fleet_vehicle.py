# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class FleetVehicleDetails(models.Model):
    _name = 'fleet.vehicle.details'

    _rec_name = 'plate_number'

    model_name = fields.Many2one('fleet.vehicle.model',string="Model", required=True)
    active = fields.Boolean('Active', default=True, track_visibility="onchange")
    make_name = fields.Many2one(related='model_name.brand',string="Make", readonly=True)
    tags_name = fields.Many2one('fleet.vehicle.tags',string="Tags")
    plate_number = fields.Char(string="License Plate", required=True)
    image = fields.Binary(related='model_name.image_id', string="Image", readonly=True)
    driver_id = fields.Many2one('drivers.details',string="Driver")
    registration_start_date = fields.Date(string="Registration Start Date")
    enginee_number = fields.Char(string="Enginee Number")
    model_year = fields.Char(string="Model Year")
    vehicles_type = fields.Char(string="Vehicle Type", required=True)
    vehicles_mileage = fields.Char(string="Vehicle Mileage")
    registration_end_date = fields.Date(string="Registration End Date")
    fuel_reading= fields.Selection([('6', 'Full Tank'), ('5', '3.4 Quater Tank'), ('4', 'Half Tank'), ('3', '1.2 Quater Tank'), ('2', 'Less 1.2 Quater Tank'),('1', 'Empty Tank')], string='Start Fuel Reading', required=True)
    seats = fields.Integer(string="Seating Capacity")
    doors = fields.Char(string="Doors")
    color = fields.Char(string="Color")
    level = fields.Selection([('excom', 'EXCOM CARS'), ('poolofcars', 'POOL OF CARS'), ('reserved', 'RESERVED CARS')], 'Level',help='Level of the vehicle')
    tracking = fields.Selection([('activated', 'Activated'), ('notactivated', 'Not Activated')], 'GPS Tracking',help='Tracking of the vehicle')
    transmission = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission', help='Transmission Used by the vehicle')
    fuel_type = fields.Selection([('gasoline', 'Gasoline'),('diesel', 'Diesel')], 'Fuel Type', help='Fuel Used by the vehicle')
    mileage_reading = fields.Char(string="Mileage Reading", readonly=True)
    state = fields.Char(string="Vehicle Status", readonly=True)