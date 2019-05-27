# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import Warning

class RequestVehicle(models.Model):
	
    _name = "request.vehicle"

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('request.vehicle')
        return super(RequestVehicle, self).create(vals)

    
    state = fields.Selection([('new', 'NEW'),('manager', 'MANAGER'), ('wap', 'TRANSPORT DEPT'), ('hold', 'ON HOLD'),('sec', 'SECURITY'),('out', 'CHECK-OUT'),('checkin', 'CHECK-IN'), ('ret', 'REFUSED')], default='new')
    name = fields.Char(string='Request Number', copy=False)
    emp_name = fields.Many2one('employee.details',string='Requester Name',required=True)
    emp_number = fields.Char(related='emp_name.employee_number',string='Mobile',readonly=True)
    department = fields.Char(related='emp_name.department',string='Department',readonly=True)
    position = fields.Char(related='emp_name.position',string='Position',readonly=True)
    vehicle_type = fields.Selection([('PickUp(4X4)', 'PickUp(4X4)'), ('Jeep', 'Jeep'), ('Sedan', 'Sedan'), ('Truck', 'Truck'),('Forklit', 'ForkLit'),('Station Wagon', 'Station Wagon'),('MINI BUS (15 Seated)', 'MINI BUS (15 Seated)'),('BIG BUS (32 Seated)', 'BIG BUS (32 Seated)'),('Availiable Car', 'Availiable Car')], string=' Type Of Vehicle', required=True)
    location = fields.Char(string='Start From', required=True)
    destination = fields.Char(string='Destination', required=True)
    seating_capacity = fields.Char(string="Number Of  Persons", required=True)
    drive_out_by = fields.Selection([('em', 'Employee'), ('dr', 'Driver')],default='dr', string='Drive Out By', required=True)
    employee_out_name = fields.Many2one('employee.details', string="Employee Name")
    req_date_time = fields.Datetime(string='Requested Time', default=lambda *a: datetime.now(),readonly=True)
    reasons = fields.Text(string='Reason', required=True)
    manager_name = fields.Many2one('manager.details',string='Manager', required=True)
    manager_number = fields.Char(related='manager_name.manager_number',string='Mobile', readonly=True)
    opinion = fields.Selection([('AGREE', 'AGREE')],default='AGREE', string='Opinion')
    transport_dept_name = fields.Many2one('transport.details',string='Transport Dept')
    transport_dept_number = fields.Char(related='transport_dept_name.transport_number', string='Mobile Number', readonly=True)
    approved_date = fields.Datetime(string='Date')
    comment = fields.Text(string="Comment")
    license_plate = fields.Many2one('fleet.vehicle.details', string="Plate Number")
    vehicles_type = fields.Char(related='license_plate.vehicles_type',string="Vehicle Type")
    driver_name = fields.Many2one('drivers.details', string="Driver Name")
    drivers_number = fields.Char(related='driver_name.drivers_number', string="Driver Number")
    security_dept_name = fields.Many2one('security.details',string='Security Name')
    security_dept_number = fields.Char(related='security_dept_name.security_number', string='Security Number')
    check_out_date_time = fields.Datetime(string="Check Out Time")
    start_fuel_reading = fields.Selection([('6', 'Full Tank'), ('5', '3.4 Quater Tank'), ('4', 'Half Tank'), ('3', '1.2 Quater Tank'), ('2', 'Less 1.2 Quater Tank'),('1', 'Empty Tank')], string='Start Fuel Reading')
    start_mileage = fields.Char(string="Start Mileage")
    drive_in_by = fields.Selection([('ein', 'Employee'), ('din', 'Driver')],default='', string='Drive In By')
    driver_in_name = fields.Many2one('drivers.details', string="Driver Name")
    employee_in_name = fields.Many2one('employee.details', string="Employee Name")
    check_in_date_time = fields.Datetime(string="Check In Time")
    return_fuel_reading = fields.Selection([('6', 'Full Tank'), ('5', '3.4 Quater Tank'), ('4', 'Half Tank'), ('3', '1.2 Quater Tank'), ('2', 'Less 1.2 Quater Tank'),('1', 'Empty Tank')], string='Return Fuel Reading')
    return_mileage = fields.Char(string="End Mileage")
    return_opinion = fields.Selection([('DISAGREE', 'DISAGREE')],default='DISAGREE', string='Opinion')
    return_date =fields.Datetime(string="Refuse Date") 
    return_reason =fields.Text(string="Comment") 



    @api.multi
    def button_submit(self):
        for record in self:
            record.write({'state': 'manager'})

        #vehicle request sms notification starts here
        method_name = 'send_sms'
        sendSMS = getattr(SMS,method_name)
        emp_number=record["emp_number"]
        manager_number=record["manager_number"]
        employee = str(self.emp_name.employee_lname)+" "+str(self.emp_name.employee_fname)
        vehicle = str(self.vehicle_type)
        destin = str(self.destination)
        time = str(self.req_date_time)

        #SMS Start
        sendSMS([manager_number],employee+" is requesting for "+vehicle+" going "+destin+" at "+time+" need your Approval thanks. From OLIB-FMS")
        
        sendSMS([emp_number],"Your request has been sent to your Manager for Approval thanks for using OLIB-FMS")


class ManagerRequestValidate(models.Model):
    _name = "manager.validate"

    opinion = fields.Selection([('AGREE', 'AGREE')],default='AGREE', string='Opinion', readonly=True)
    transport_dept_name = fields.Many2one('transport.details',string='Transport Dept', required=True)
    transport_dept_number = fields.Char(related='transport_dept_name.transport_number', string='Mobile', readonly=True)
    approved_date = fields.Datetime(default=lambda *a: datetime.now(),string='Date', readonly=True)
    comment = fields.Text(string="Comment", required=True)
    

    @api.multi
    def button_send(self):
        if self.env.context.get('request_id'):
            request = self.env['request.vehicle'].browse(self.env.context.get('request_id'))
            request.write({'state': 'wap', 'approved_date': self.approved_date,'opinion': self.opinion,'comment': self.comment, 'transport_dept_name': self.transport_dept_name.id, 'transport_dept_number': self.transport_dept_number})
            
            #vehicle request sms notification starts here
           
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            field="emp_number"
            emp_number=request[field]
            field="manager_number"
            manager_number=request[field]
            field="transport_dept_number"
            transport_dept_number=request[field]
            # field="vehicles_type"
            # vehicle_req=request[vehicles_type]
            vehicle_type="vehicle_type"
            vehicle_req=str(request[vehicle_type])
            destination="destination"
            destins=request[destination]
            req_date_time="req_date_time"
            time_req=request[req_date_time]
            field="emp_name"
            emp_name=request[field]
            emp_name = str(emp_name.employee_lname)+" "+str(emp_name.employee_fname)

            # field="vehicles_type"
            # vehicles_type=request[field]
            # vehicles_type = str(vehicles_type)

            dob = "drive_out_by"
            drive_out_by=request[dob]

            if drive_out_by=="em":
                sendSMS([transport_dept_number],emp_name+" is requesting for "+vehicle_req+" going "+destins+" at "+time_req+ " and has been Approved")
            else:
                sendSMS([transport_dept_number],emp_name+" is requesting for "+vehicle_req+" and Driver going "+destins+" at "+time_req+ " and has been Approved. From OLIB-FMS")
                
                sendSMS([emp_number],"Your request has been Approved by your Manager and sent to TRANSPORT SECTION thanks for using OLIB-FMS")
                sendSMS([manager_number],"Approved vehicle request has been sent to TRANSPORT SECTION thanks for using OLIB-FMS")


class AssignedVehicle(models.Model):
    _name = "assigned.vehicle"


    license_plate = fields.Many2one('fleet.vehicle.details', string="Select Plate", required=True)
    vehicles_type = fields.Char(related='license_plate.vehicles_type',string="Vehicle Type", readonly=True)
    driver_name = fields.Many2one('drivers.details', string="Select Driver")
    drivers_number = fields.Char(related='driver_name.drivers_number', string="Driver Number", readonly=True)
    security_dept_name = fields.Many2one('security.details',string='Security Name', required=True)
    security_dept_number = fields.Char(related='security_dept_name.security_number', string='Security Number', readonly=True)


    @api.multi
    def button_assign(self):
        if self.env.context.get('request_id'):
            request = self.env['request.vehicle'].browse(self.env.context.get('request_id'))
            request.write({'state': 'sec', 'license_plate': self.license_plate.id, 'vehicles_type': self.vehicles_type, 'driver_name': self.driver_name.id, 'drivers_number': self.drivers_number, 'security_dept_name': self.security_dept_name.id,'security_dept_number': self.security_dept_number})
            
            #vehicle assigned_sms_notification_starts_here
            field="emp_number"
            emp_number=request[field]
            field="name"
            name=request[field]          
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            plate = str(self.license_plate.plate_number)
            driver = str(self.driver_name.drivers_lname)+" "+str(self.driver_name.drivers_fname)
            
            d_number = str(self.drivers_number)
            field="drivers_number"
            drivers_number=request[field]
            
            dob = "drive_out_by"
            drive_out_by=request[dob]

            d_number = str(self.drivers_number)
            field="security_dept_number"
            security_dept_number=request[field]

            field="emp_name"
            emp_name=request[field]
            emp_name = str(emp_name.employee_lname)+" "+str(emp_name.employee_fname)


            if drive_out_by=="dr": #SMS Start
                sendSMS([emp_number],"Vehicle "+plate+" with Driver "+driver+" is assigned to you. Please call this number "+d_number+" to start your trip. Thanks for using OLIB-FMS.")
                sendSMS([drivers_number],"Vehicle "+plate+" with Employee "+emp_name+" is assigned to you. Please call this number "+emp_number+" to start your trip. Request Number: "+name)
                sendSMS([security_dept_number],"Vehicle "+plate+" with Employee "+emp_name+" and Driver "+driver+" is going out please CHECK OUT before leaving. Request Number: "+name+", From TRANSPORT DEPT.")
            else:
                sendSMS([emp_number],"Vehicle "+plate+" is assigned to you. Please pickup the KEY to start your trip. Thanks for using OLIB-FMS. Request Number: "+name)
                sendSMS([security_dept_number],"Vehicle "+plate+" with Employee "+emp_name+" is going out please CHECK OUT using Request Number "+name+" before leaving . From TRANSPORT DEPT.")
           


class HoldRequest(models.Model):
    _name = "hold.request"

    onhold_reason =fields.Text(string="Reason",required=True)
    

    @api.multi
    def button_hold(self):
        if self.env.context.get('request_id'):
            request = self.env['request.vehicle'].browse(self.env.context.get('request_id'))
            request.write({'state': 'hold', 'onhold_reason': self.onhold_reason})

            #vehicle hold request_sms_notification_starts_here
            field="emp_number"
            emp_number=request[field]
            field="manager_number"
            manager_number=request[field]
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            sendSMS([emp_number],self.onhold_reason+".: REQUEST ON-HOLD THANKS.")
            sendSMS([manager_number],self.onhold_reason+".: APPROVED REQUEST IS ON HOLD THANKS.") 

             

class CheckOut(models.Model):
    _name = "check.out"

    check_out_date_time = fields.Datetime(string="Check Out Time",default=lambda *a: datetime.now(), readonly=True)
    start_fuel_reading = fields.Selection([('6', 'Full Tank'), ('5', '3.4 Quater Tank'), ('4', 'Half Tank'), ('3', '1.2 Quater Tank'), ('2', 'Less 1.2 Quater Tank'),('1', 'Empty Tank')], string='Start Fuel Reading', required=True)
    start_mileage = fields.Char(string="Start Mileage", required=True)#,compute=_get_mileage)

   
    @api.multi
    def button__check_out(self):
        if self.env.context.get('request_id'):
            request = self.env['request.vehicle'].browse(self.env.context.get('request_id'))
            request.write({'state': 'out', 'check_out_date_time': self.check_out_date_time, 'start_fuel_reading': self.start_fuel_reading, 'start_mileage': self.start_mileage})

           #vehicle check-out_sms_notification_starts_here
            
            # method_name = 'send_sms'
            # sendSMS = getattr(SMS,method_name)
            

            # field="license_plate"
            # license_plate=request[field]
            # if license_plate>self.return_mileage:
            #         raise Warning(': '+ license_plate)

            

            #driver_sms_function_start_here
            vehicle_type="license_plate"
            vehicle_out=request[vehicle_type].plate_number
            destination="destination"
            destin=request[destination]
            time_out = str(self.check_out_date_time)

            field="transport_dept_number"
            transport_dept_number=request[field]  
            field="drivers_number"
            drivers_number=request[field]
            dob = "drive_out_by"
            drive_out_by=request[dob]
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            field="emp_number"
            emp_number=request[field]

            sendSMS([transport_dept_number],"Vehicle "+vehicle_out+" Going "+destin+" is CHECKED-OUT at "+time_out)

            if drive_out_by=="dr":
                sendSMS([drivers_number],"You have been CHECKED-OUT successfully. Voyage Securise, Safe trip....")
            else:
                sendSMS([emp_number],"You have been CHECKED-OUT successfully. Voyage Securise, Safe trip....")
            

class CheckIn(models.Model):
    _name = "check.vehicle.in"

    drive_in_by = fields.Selection([('ein', 'Employee'), ('din', 'Driver')],default='din', string='Drive In By', required=True)
    driver_in_name = fields.Many2one('drivers.details', string="Driver Name")
    employee_in_name = fields.Many2one('employee.details', string="Employee Name")
    check_in_date_time = fields.Datetime(string="Check In Time" ,default=lambda *a: datetime.now(), readonly=True)
    return_fuel_reading = fields.Selection([('6', 'Full Tank'), ('5', '3.4 Quater Tank'), ('4', 'Half Tank'), ('3', '1.2 Quater Tank'), ('2', 'Less 1.2 Quater Tank'),('1', 'Empty Tank')], string='Return Fuel Reading', required=True)
    return_mileage = fields.Char(string="End Mileage", required=True)
    

    @api.multi
    def button_checkvehicle_in(self):
        if self.env.context.get('request_id'):
            request = self.env['request.vehicle'].browse(self.env.context.get('request_id'))
            request.write({'state': 'checkin','drive_in_by': self.drive_in_by,'driver_in_name': self.driver_in_name.id, 'employee_in_name': self.employee_in_name.id, 'check_in_date_time': self.check_in_date_time, 'return_fuel_reading': self.return_fuel_reading, 'return_mileage': self.return_mileage})

            #vehicle Check-In_sms_notification_starts_here
            drive_out_by="drive_out_by"
            dib = request[drive_out_by]
            field="drivers_number"
            drivers_number=request[field]
            field="emp_number"
            emp_number=request[field]
            field="transport_dept_number"
            transport_dept_number=request[field]

            field="start_mileage"
            start_mileage=request[field]
            if start_mileage>self.return_mileage:
                    raise Warning('End Mileage must be greater than Start Mileage: '+ start_mileage)


            vehicle_type="license_plate"
            vehicle_in=request[vehicle_type].plate_number
            destination="destination"
            destin=request[destination] 

            time_in = str(self.check_in_date_time) 

            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            if dib=="dr":
                sendSMS([drivers_number],"You have been CHECKED-IN successfully. Nous saluons le retour, Welcome Back...")
                sendSMS([transport_dept_number],"Vehicle "+vehicle_in+" From "+destin+" is CHECKED-IN at "+time_in)
            else:
                sendSMS([emp_number],"You have been CHECKED-IN successfully. Nous saluons le retour, Welcome Back...")
                sendSMS([transport_dept_number],"Vehicle "+vehicle_in+" From "+destin+" is CHECKED-IN at "+time_in)
            


class ReturnRequest(models.Model):
    _name = "return.request"

    return_opinion = fields.Selection([('DISAGREE', 'DISAGREE')],default='DISAGREE', string='Opinion', readonly=True)
    return_date =fields.Datetime(string="Refuse Date", default=lambda *a: datetime.now(),readonly=True) 
    return_reason =fields.Text(string="Comment", required=True) 

    @api.multi
    def button_return(self):
        if self.env.context.get('request_id'):
            request = self.env['request.vehicle'].browse(self.env.context.get('request_id'))
            request.write({'state': 'ret', 'return_opinion': self.return_opinion,'return_date': self.return_date, 'return_reason': self.return_reason})

            #vehicle returned request_sms_notification_starts_here
            field="emp_number"
            emp_number=request[field]
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            sendSMS([emp_number],self.return_reason) 



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