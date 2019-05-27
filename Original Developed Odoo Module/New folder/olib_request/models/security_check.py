# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import Warning

class SecurityCheck(models.Model):
	
    _name = "security.check"

    

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('security.check')
        return super(SecurityCheck, self).create(vals)

    
    state = fields.Selection([('new', 'NEW'), ('out', 'CHECK-OUT'),('in', 'CHECK-IN')], default='new')

    name = fields.Char(string='Check Number ', copy=False)
    drive_out_by = fields.Selection([('dr', 'Driver'),('emp', 'Employee')],default='dr', string="Drive By", required=True)
    employee_name = fields.Many2one('employee.details',string="Employee")
    driver_name = fields.Many2one('drivers.details', string="Driver")
    mobile_number_dr = fields.Char(related='driver_name.drivers_number', string="Mobile", readonly=True)
    mobile_number_emp = fields.Char(related='employee_name.employee_number', string="Mobile", readonly=True)
    department = fields.Char(related='employee_name.department',string='Department', readonly=True)
    number_of_person = fields.Char(string='Number Of Persons', required=True)
    start_from = fields.Char(string='Start From', required=True)
    destination = fields.Char(string='Destination', required=True)
    reason = fields.Text(string='Reason', required=True)
    transport_dept_name = fields.Many2one('transport.details',string='Transport Head', required=True)
    transport_dept_number = fields.Char(related='transport_dept_name.transport_number', string='Mobile', readonly=True)
    license_plate = fields.Many2one('fleet.vehicle.details',string='Plate Number', required=True)
    vehicles_type = fields.Char(related='license_plate.vehicles_type',string='Vehicle Type', readonly=True)
    check_out_date_time = fields.Datetime(string='Start Time',default=lambda *a: datetime.now(),readonly=True)
    start_fuel_reading = fields.Selection([('6', 'Full Tank'), ('5', '3.4 Quater Tank'), ('4', 'Half Tank'), ('3', '1.2 Quater Tank'), ('2', 'Less 1.2 Quater Tank'),('1', 'Empty Tank')], string='Start Fuel Reading', required=True)
    start_mileage = fields.Char(string='Start Mileage', required=True)
    drive_in_by = fields.Selection([('ein', 'Employee'), ('din', 'Driver')],default='', string='Drive In By')
    driver_in_name = fields.Many2one('drivers.details', string="Driver Name")
    employee_in_name = fields.Many2one('employee.details', string="Employee Name")
    check_in_date_time = fields.Datetime(string='Check In Time')
    end_fuel_reading = fields.Selection([('6', 'Full Tank'), ('5', '3.4 Quater Tank'), ('4', 'Half Tank'), ('3', '1.2 Quater Tank'), ('2', 'Less 1.2 Quater Tank'),('1', 'Empty Tank')], string='End Fuel Reading')
    end_mileage = fields.Char(string='End Mileage')
    total_mileage = fields.Char(string="Total Mileage", readonly=True)


    # @api.onchange('start_mileage','end_mileage')
    # def onchange_field(self):
    #     if self.start_mileage or self.end_mileage:
    #         self.total_mileage = self.start_mileage + end_mileage

    # @api.depends('start_mileage','end_mileage')
    # def_get_sum(self):
    #     for rec in self:
    #         rec.update({
    #             'total_mileage':rec.start_mileage+rec.end_mileage
    #             })

    @api.multi
    def button_submit(self):
        for record in self:
            record.write({'state': 'out'})


            #vehicle check-out sms starts here
            transport_dept_number=record["transport_dept_number"]  
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            vehicle_out = str(self.license_plate.plate_number)
            destin = str(self.destination)
            time_out = str(self.check_out_date_time)

            sendSMS([transport_dept_number],"Vehicle "+vehicle_out+" Going "+destin+" is CHECKED-OUT at "+time_out)

            #driver_sms_function_start_here
            mobile_number_dr=record["mobile_number_dr"]
            
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            mobile_number_emp=record["mobile_number_emp"]

            if self.drive_out_by=="dr":
                sendSMS([mobile_number_dr],"You have been CHECKED-OUT successfully. Voyage Securise, Safe trip....")
            else:
                sendSMS([mobile_number_emp],"You have been CHECKED-OUT successfully. Voyage Securise, Safe trip....")
            


class SecurityCheckin(models.Model):

        _name = "checkin.vehicle"

        drive_in_by = fields.Selection([('ein', 'Employee'), ('din', 'Driver')],default='din', string='Drive In By', required=True)
        driver_in_name = fields.Many2one('drivers.details', string="Driver Name")
        employee_in_name = fields.Many2one('employee.details', string="Employee Name")
        check_in_date_time = fields.Datetime(string='Check In Time',default=lambda *a: datetime.now(),readonly=True)
        end_fuel_reading = fields.Selection([('6', 'Full Tank'), ('5', '3.4 Quater Tank'), ('4', 'Half Tank'), ('3', '1.2 Quater Tank'), ('2', 'Less 1.2 Quater Tank'),('1', 'Empty Tank')], string='End Fuel Reading', required=True)
        end_mileage = fields.Char(string='End Mileage', required=True)
        total_mileage = fields.Char(string='Total Mileage', readonly=True)


        @api.multi
        def button_checkin(self):
            if self.env.context.get('request_id'):
                request = self.env['security.check'].browse(self.env.context.get('request_id'))
                request.write({'state': 'in', 'drive_in_by': self.drive_in_by, 'driver_in_name': self.driver_in_name.id, 'check_in_date_time': self.check_in_date_time, 'employee_in_name': self.employee_in_name.id,'end_fuel_reading': self.end_fuel_reading, 'end_mileage': self.end_mileage, 'total_mileage': self.total_mileage})

                #vehicle check-in sms notification starts here
                drive_out_by="drive_out_by"
                dib = request[drive_out_by]
                field="mobile_number_dr"
                mobile_number_dr=request[field]
                field="mobile_number_emp"
                mobile_number_emp=request[field]
                field="transport_dept_number"
                transport_dept_number=request[field]

                field="start_mileage"
                start_mileage=request[field]
                if start_mileage>self.end_mileage:
                        raise Warning('End Mileage must be greater than Start Mileage: '+ start_mileage)

                vehicles_type="license_plate"
                vehicle_in=request[vehicles_type].plate_number
                destination="destination"
                destin=request[destination] 

                time_in = str(self.check_in_date_time) 

                method_name = 'send_sms'
                sendSMS = getattr(SMS,method_name)
                if dib=="din":
                    sendSMS([mobile_number_dr],"You have been CHECKED-IN successfully. Nous saluons le retour, Welcome Back...")
                    sendSMS([transport_dept_number],"Vehicle "+vehicle_in+" From "+destin+" is CHECKED-IN at "+time_in)
                else:
                    sendSMS([mobile_number_emp],"You have been CHECKED-IN successfully. Nous saluons le retour, Welcome Back...")
                    sendSMS([transport_dept_number],"Vehicle "+vehicle_in+" From "+destin+" is CHECKED-IN at "+time_in)
                

class SMS(models.Model):
    _name = "sms"

    @api.multi
    def send_sms(employee_numbers, message_content):
        #_logger.info("Ping -c 1 192.168.15.21")
        # ping = os.system("ping  192.168.15.21")
        #_logger.info(ping)
        for recipient_number in employee_numbers:
            url="http://192.168.15.21:8091/CellcomAPIService"
            headers = {'content-type': 'application/soap+xml'}
            body ="\
            <s:Envelope xmlns:a='http://www.w3.org/2005/08/addressing' xmlns:s='http://www.w3.org/2003/05/soap-envelope'>\
              <s:Header>\
                <a:Action s:mustUnderstand='1'>http://tempuri.org/ISubscribers/SubscriberSendNotification</a:Action>\
                <a:MessageID>urn:uuid:3472a125-74f5-4914-865d-d1037d1dcbd8</a:MessageID>\
                <a:ReplyTo>\
                  <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>\
                </a:ReplyTo>\
              </s:Header>\
              <s:Body>\
                <SubscriberSendNotification xmlns='http://tempuri.org/'>\
                  <c_subs_req xmlns:d4p1='http://schemas.datacontract.org/2004/07/CellcomAPILibrary' xmlns:i='http://www.w3.org/2001/XMLSchema-instance'>\
                    <d4p1:Client>wcf client tool</d4p1:Client>\
                    <d4p1:Password>h1$d/6Hf78(hg</d4p1:Password>\
                    <d4p1:UserName>HIS</d4p1:UserName>\
                    <d4p1:DestinationNumber>%s</d4p1:DestinationNumber>\
                    <d4p1:NotificationText>%s</d4p1:NotificationText>\
                    <d4p1:NotificationType>SMS</d4p1:NotificationType>\
                    <d4p1:OriginatingNumber>FMS OLIB</d4p1:OriginatingNumber>\
                  </c_subs_req>\
                </SubscriberSendNotification>\
              </s:Body>\
            </s:Envelope>\
            " %(recipient_number, message_content)
            response = requests.post(url,data=body,headers=headers)
            print(response.content)

            return response

        return False


