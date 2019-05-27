# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class EmployeeDetails(models.Model):
    _name = 'employee.details'

    _rec_name ="display_name"

    @api.depends('employee_lname','employee_fname')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s %s' %(record.employee_lname, record.employee_fname)

    image = fields.Binary(string="Image", attachment=True)
    active = fields.Boolean('Active', default=True, track_visibility="onchange")
    registration_id = fields.Char(string="Registration Number")
    employee_lname = fields.Char(string="Last Name")
    employee_fname = fields.Char(string="First Name")
    department = fields.Char(string="Department")
    position = fields.Char(string="Position")
    status = fields.Many2one('employee.status',string="Employee Status")
    employee_email = fields.Char(string="Work Email")
    employee_number = fields.Char(string="Work Phone")
    display_name = fields.Char(string='Employee Name', compute='_compute_display_name')


    
   