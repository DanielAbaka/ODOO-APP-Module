# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class LeaveTypeConfiguration(models.Model):
    _name = 'leave.type'

    _rec_name = 'leave_type'

    leave_type = fields.Char(required=True, translate=True)

    _sql_constraints = [('name_uniq', 'unique (leave_type)', "Tag leave Type already exists !")]

   