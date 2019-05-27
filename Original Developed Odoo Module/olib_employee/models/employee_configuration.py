# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class ManagerDetails(models.Model):
    _name = 'manager.details'

    _rec_name ="display_name"

    @api.depends('manager_lname','manager_fname')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s %s' %(record.manager_lname, record.manager_fname)

    image = fields.Binary(string="Image", attachment=True)
    active = fields.Boolean('Active', default=True, track_visibility="onchange")
    registration_id = fields.Char(string="Registration Number")
    manager_lname = fields.Char(string="Last Name")
    manager_fname = fields.Char(string="First Name")
    manager_email = fields.Char(string="Work Email")
    manager_number = fields.Char(string="Work Phone")
    department = fields.Char(string="Department")
    display_name = fields.Char(string='Manager Name', compute='_compute_display_name')




class DriversDetails(models.Model):
    _name = 'drivers.details'

    _rec_name ="display_name"

    @api.depends('drivers_lname','drivers_fname')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s %s' %(record.drivers_lname, record.drivers_fname)


    image = fields.Binary(string="Image", attachment=True)
    active = fields.Boolean('Active', default=True, track_visibility="onchange")
    registration_id = fields.Char(string="Registration Number")
    drivers_lname = fields.Char(string="Last Name")
    drivers_fname = fields.Char(string="First Name")
    licence_number = fields.Char(string="Licence Number")
    licence_type = fields.Selection([('oridinary', 'A-Oridinary'),('chauffeur', 'B-Chauffeur'),('heavyduty', 'C-Heavy Duty')],string="Licence Type")
    licence_date_issues = fields.Date(string="Licence Date Issues")
    licence_date_expires = fields.Date(string="Licence Date Expires")
    permanent_address = fields.Char(string="Permanent Address")
    drivers_email = fields.Char(string="Work Email")
    drivers_number = fields.Char(string="Work Phone")
    display_name = fields.Char(string='Employee Name', compute='_compute_display_name')


class FinanceDetails(models.Model):
    _name = 'finance.details'

    _rec_name ="display_name"

    @api.depends('finance_lname','finance_fname')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s %s' %(record.finance_lname, record.finance_fname)

    image = fields.Binary(string="Image", attachment=True)
    active = fields.Boolean('Active', default=True, track_visibility="onchange")
    registration_id = fields.Char(string="Registration Number")
    finance_lname = fields.Char(string="Last Name")
    finance_fname = fields.Char(string="First Name")
    finance_email = fields.Char(string="Work Email")
    finance_number = fields.Char(string="Work Phone")
    display_name = fields.Char(string='Finance Name', compute='_compute_display_name')


class MechanicDetails(models.Model):
    _name = 'mechanic.details'

    _rec_name ="display_name"

    @api.depends('mechanic_lname','mechanic_fname')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s %s' %(record.mechanic_lname, record.mechanic_fname)



    image = fields.Binary(string="Image", attachment=True)
    active = fields.Boolean('Active', default=True, track_visibility="onchange")
    registration_id = fields.Char(string="Registration Number")
    mechanic_lname = fields.Char(string="Last Name")
    mechanic_fname = fields.Char(string="First Name")
    mechanic_email = fields.Char(string="Work Email")
    mechanic_number = fields.Char(string="Work Phone")
    display_name = fields.Char(string='Mechanic Name', compute='_compute_display_name')


class SecurityDetails(models.Model):
    _name = 'security.details'

    _rec_name ="display_name"

    @api.depends('security_lname','security_fname')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s %s' %(record.security_lname, record.security_fname)

    image = fields.Binary(string="Image", attachment=True)
    active = fields.Boolean('Active', default=True, track_visibility="onchange")
    registration_id = fields.Char(string="Registration Number")
    security_lname = fields.Char(string="Last Name")
    security_fname = fields.Char(string="First Name")
    security_email = fields.Char(string="Work Email")
    security_number = fields.Char(string="Work Phone")
    display_name = fields.Char(string='Security Name', compute='_compute_display_name')


class TransportDetails(models.Model):
    _name = 'transport.details'

    _rec_name ="display_name"

    @api.depends('transport_lname','transport_fname')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s %s' %(record.transport_lname, record.transport_fname)


    image = fields.Binary(string="Image", attachment=True)
    active = fields.Boolean('Active', default=True, track_visibility="onchange")
    registration_id = fields.Char(string="Registration Number")
    transport_lname = fields.Char(string="Last Name")
    transport_fname = fields.Char(string="First Name")
    transport_email = fields.Char(string="Work Email")
    transport_number = fields.Char(string="Work Phone")
    display_name = fields.Char(string='Transport Name', compute='_compute_display_name')


class ProcurementDetails(models.Model):
    _name = 'procurement.details'

    _rec_name ="display_name"

    @api.depends('procurement_lname','procurement_fname')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s %s' %(record.procurement_lname, record.procurement_fname)


    image = fields.Binary(string="Image", attachment=True)
    active = fields.Boolean('Active', default=True, track_visibility="onchange")
    registration_id = fields.Char(string="Registration Number")
    procurement_lname = fields.Char(string="Last Name")
    procurement_fname = fields.Char(string="First Name")
    procurement_email = fields.Char(string="Work Email")
    procurement_number = fields.Char(string="Work Phone")
    display_name = fields.Char(string='Procurement Name', compute='_compute_display_name')


class EmployeeStatus(models.Model):
    _name = 'employee.status'

    _rec_name = 'emp_status'

    emp_status = fields.Char(string="Employee Status")



