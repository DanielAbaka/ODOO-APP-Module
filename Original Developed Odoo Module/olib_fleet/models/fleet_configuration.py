# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class FleetConfiguration(models.Model):
    _name = 'fleet.vehicle.make'

    _rec_name = 'name'

    name = fields.Char('Make', required=True)
    image = fields.Binary("Logo", attachment=True)


    

class FleetConfigurationModel(models.Model):
    _name = 'fleet.vehicle.model'

    _rec_name = 'name'

    name = fields.Char('Model', required=True)
    brand = fields.Many2one('fleet.vehicle.make', required=True)
    image_id = fields.Binary(related='brand.image', required=True)


class FleetConfigurationTags(models.Model):
    _name = 'fleet.vehicle.tags'

    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    color = fields.Integer('Color Index', default=10)

    _sql_constraints = [('name_uniq', 'unique (name)', "Tag name already exists !")]


class FleetConfigurationServiceType(models.Model):
    _name = 'fleet.vehicle.services.type'

    name = fields.Char(required=True, translate=True)
    