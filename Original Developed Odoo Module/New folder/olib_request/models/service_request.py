# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import Warning

class RequestVehicle(models.Model):
	
    _name = "request.service"

    _rec_name ="name"

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('request.service')
        return super(RequestVehicle, self).create(vals)

    
    state = fields.Selection([('new', 'NEW'), ('chief_mechanic', 'CHIEF MECHANIC'),('dept_head', 'DEPT HEAD'),('finance', 'FINANCE'),('procurement', 'PROCUREMENT'),('delivered', 'DELIVERED'),('start_work', 'START WORK'),('end_work', 'END WORK'), ('refused', 'REFUSED')], default='new')
    
    name = fields.Char(string='Request Number', copy=False)
    emp_name = fields.Many2one('employee.details',string='Requester Name',required=True)
    emp_number = fields.Char(related='emp_name.employee_number',string='Mobile',readonly=True)
    license_plate = fields.Many2one('fleet.vehicle.details',string='Licence Plate', required=True)
    vehicles_type = fields.Selection([('jeep', 'JEEP'), ('sedan', 'SEDAN'), ('pickup(4X4)', 'Pickup(4X4)'), ('truck', 'TRUCK'), ('forklift', 'FORKLIFT'), ('Station Wagon', 'STATION WAGON'), ('MiniBus(15 Seated)', 'MINI BUS (15 Seated)'), ('BigBus(32 Seated)', 'BIG BUS (32 SEATED)')] ,string="Vehicle Type", required=True)
    service_type = fields.Many2one('fleet.vehicle.services.type',string='Service Type', required=True)
    date = fields.Date(string='Requested Date',default=lambda *a: datetime.now(), readonly=True)
    mechanic_head_name = fields.Many2one('mechanic.details',string="Mechanic Head", required=True)
    mechanic_head_number = fields.Char(related='mechanic_head_name.mechanic_number',string="Mobile", readonly=True)
    note = fields.Text(string="Note", copy=False, required=True)
    comment = fields.Text(string="List all material needed to be purchased")
    order_date = fields.Datetime(string='Date')
    dept_head_name = fields.Many2one('manager.details',string="Manager")
    dept_head_number = fields.Char(related='dept_head_name.manager_number',string="Mobile")
    dept_approve_date = fields.Datetime(string='Date')
    dept_opinion = fields.Selection([('agree','AGREE')], default='agree', string="Opinion")
    dept_comment = fields.Text(string="Comments")
    finance_head_name = fields.Many2one('finance.details',string="Finance Head")
    finance_head_number = fields.Char(related='finance_head_name.finance_number',string="Mobile")
    fin_approve_date = fields.Datetime(string='Date')
    finance_opinion = fields.Selection([('agree','AGREE')], default='agree', string="Opinion")
    finance_comment = fields.Text(string="Comment")
    procurement_head_name = fields.Many2one('procurement.details',string="Procurement Head")
    procurement_head_number = fields.Char(related='procurement_head_name.procurement_number',string="Mobile")
    proc_delivered_date = fields.Datetime(string='Date')
    procurement_opinion = fields.Selection([('delivered','DELIVERED')], default='delivered', string="Opinion")
    procurement_comment = fields.Text(string="Comments")
    mechanic_head_name = fields.Many2one('mechanic.details',string="Mechanic Head")
    mechanic_head_number = fields.Char(related='mechanic_head_name.mechanic_number',string="Mobile", readonly=True)
    start_comment_date = fields.Datetime(string='Date')
    start_comment = fields.Text(string="Comments")
    end_comment_date = fields.Datetime(string='Date')
    end_comment = fields.Text(string="Comments")
    return_opinion = fields.Selection([('disagree','DISAGREE')], default='disagree', string="Opinion") 
    return_date =fields.Datetime(string="Refused Date") 
    return_reason =fields.Text(string="Comments")
    

    @api.multi
    def button_submit(self):
        for record in self:
            record.write({'state': 'chief_mechanic'})

        #Maintenance request sms notification starts here
        method_name = 'send_sms'
        sendSMS = getattr(SMS,method_name)
        emp_number=record["emp_number"]
        mechanic_head_number=record["mechanic_head_number"]
        employee = str(self.emp_name.employee_lname)+" "+str(self.emp_name.employee_fname)
        license_plate = str(self.license_plate.plate_number)
        

        sendSMS([mechanic_head_number],employee+" is requesting a maintenance for Vehicle "+license_plate+" need your approval for maintenance.")
        
        sendSMS([emp_number],"Your request has been sent to Chief Mechanic for Vehicle Maintenance thanks for using OLIB-FMS")


class ManagerOrder(models.Model):
    _name = "order.parts"

    comment = fields.Text(string="List all material needed to be purchased", required=True)
    order_date = fields.Datetime(default=lambda *a: datetime.now(),string='Date', readonly=True)
    dept_head_name = fields.Many2one('manager.details',string="Manager", required=True)
    dept_head_number = fields.Char(related='dept_head_name.manager_number',string="Mobile", readonly=True)

    
    @api.multi
    def button_send(self):
        if self.env.context.get('request_id'):
            request = self.env['request.service'].browse(self.env.context.get('request_id'))
            request.write({'state': 'dept_head', 'comment': self.comment, 'dept_head_name': self.dept_head_name.id, 'dept_head_number': self.dept_head_number})
            

            #Manager_Order request sms notification starts here
           
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            field="mechanic_head_number"
            mechanic_head_number=request[field]

            field="emp_number"
            emp_number=request[field]

            field="dept_head_number"
            dept_head_number=request[field]


            field="mechanic_head_name"
            mechanic_head_name=request[field]
            mechanic_head_name = str(mechanic_head_name.mechanic_lname)+" "+str(mechanic_head_name.mechanic_fname)
            # mechanic_head_name = str(mechanic_head_name.mechanic_head_name)

          
            
             
            sendSMS([dept_head_number],mechanic_head_name+", The chief Mechanic is requesting an order of vehicle parts for vehicle maintenance and need your approval")
                
            sendSMS([emp_number],"Your request has been Approved by Chief Mechanic for Vehicle Maintenance and sent for Manager approval thanks for using OLIB-FMS")
            
            sendSMS([mechanic_head_number],"Vehicle order material request has been sent to Manager for Approval thanks for using OLIB-FMS")


class DeptHead(models.Model):
    _name = "dept.head"

    dept_approve_date = fields.Datetime(default=lambda *a: datetime.now(),string='Date', readonly=True)
    dept_opinion = fields.Selection([('agree','AGREE')], default='agree', string="Opinion", readonly=True)
    dept_comment = fields.Text(string="Comments", required=True)
    finance_head_name = fields.Many2one('finance.details',string="Finance Head", required=True)
    finance_head_number = fields.Char(related='finance_head_name.finance_number',string="Mobile", readonly=True)

    def dept_button_send(self):
        if self.env.context.get('request_id'):
            request = self.env['request.service'].browse(self.env.context.get('request_id'))
            request.write({'state': 'finance', 'dept_approve_date': self.dept_approve_date,'dept_opinion': self.dept_opinion, 'dept_comment': self.dept_comment, 'finance_head_name': self.finance_head_name.id, 'finance_head_number': self.finance_head_number})

            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            # finance_head_number=record["finance_head_number"]
            field="mechanic_head_number"
            mechanic_head_number=request[field]

            field="finance_head_number"
            finance_head_number=request[field]

            field="dept_head_name"
            dept_head_name=request[field]
            dept_head_name = str(dept_head_name.manager_lname)+" "+str(dept_head_name.manager_fname)
            # dept_head_name = str(dept_head_name.dept_head_name)

            sendSMS([finance_head_number],dept_head_name+",Manager has approved vehicle materials order request, Need your approval for order of materials thanks for using OLIB-FMS")
            
            sendSMS([mechanic_head_number],"Manager has approved vehicle material order request and sent to Finance Head for final approval thanks for using OLIB-FMS")
            


class FinanceHead(models.Model):
    _name = "finance.head.approve"

    fin_approve_date = fields.Datetime(default=lambda *a: datetime.now(),string='Date', readonly=True)
    finance_opinion = fields.Selection([('agree','AGREE')], default='agree', string="Opinion", readonly=True)
    finance_comment = fields.Text(string="Comment", required=True)
    procurement_head_name = fields.Many2one('procurement.details',string="Procurement Head", required=True)
    procurement_head_number = fields.Char(related='procurement_head_name.procurement_number',string="Mobile",readonly=True)

    def finance_button_send(self):
        if self.env.context.get('request_id'):
            request = self.env['request.service'].browse(self.env.context.get('request_id'))
            request.write({'state': 'procurement', 'fin_approve_date': self.fin_approve_date,'finance_opinion': self.finance_opinion, 'finance_comment': self.finance_comment, 'procurement_head_name': self.procurement_head_name.id, 'procurement_head_number': self.procurement_head_number})

            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)

            field="procurement_head_number"
            procurement_head_number=request[field]

            field="mechanic_head_number"
            mechanic_head_number=request[field]

            field="finance_head_number"
            finance_head_number=request[field]

            field="finance_head_name"
            finance_head_name=request[field]
            finance_head_name = str(finance_head_name.finance_lname)+" "+str(finance_head_name.finance_fname)
            # finance_head_name = str(finance_head_name.finance_head_name)

            field="dept_head_number"
            dept_head_number=request[field]

            sendSMS([procurement_head_number],finance_head_name+", Finance Head has approved vehicle materials order request, Please order materials and deliver for vehicle maintenances thanks for using OLIB-FMS")
            
            sendSMS([dept_head_number],"Finance Head has approved vehicle material order request and sent to Procurement Head for material order thanks for using OLIB-FMS")
            
            sendSMS([mechanic_head_number],"Finance Head has approved vehicle material order request and sent to Procurement Head for material order thanks for using OLIB-FMS")
            



class ProcurementHead(models.Model):
    _name = "procurement.head.delivered"

    proc_delivered_date = fields.Datetime(default=lambda *a: datetime.now(),string='Date', readonly=True)
    procurement_opinion = fields.Selection([('delivered','DELIVERED')], default='delivered', string="Opinion", readonly=True)
    procurement_comment = fields.Text(string="Comments", required=True)
    mechanic_head_name = fields.Many2one('mechanic.details',string="Mechanic Head", required=True)
    mechanic_head_number = fields.Char(related='mechanic_head_name.mechanic_number',string="Mobile",readonly=True)
    
    
    @api.multi
    def procurement_button_send(self):
        if self.env.context.get('request_id'):
            request = self.env['request.service'].browse(self.env.context.get('request_id'))
            request.write({'state': 'delivered', 'proc_delivered_date': self.proc_delivered_date,'procurement_opinion': self.procurement_opinion, 'procurement_comment': self.procurement_comment, 'mechanic_head_name': self.mechanic_head_name.id, 'mechanic_head_number': self.mechanic_head_number})

            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)

            field="mechanic_head_number"
            mechanic_head_number=request[field]

            sendSMS([mechanic_head_number],"Vehicle order material requested item has been delivered to start work thanks for using OLIB-FMS")



class StartWork(models.Model):
    _name = "start.service.work"

    start_comment_date = fields.Datetime(default=lambda *a: datetime.now(),string='Date', readonly=True)
    start_comment = fields.Text(string="Comments", required=True)
    
    @api.multi
    def button_start_work(self):
        if self.env.context.get('request_id'):
            request = self.env['request.service'].browse(self.env.context.get('request_id'))
            request.write({'state': 'start_work', 'start_comment_date': self.start_comment_date,'start_comment': self.start_comment})

            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            field="emp_number"
            emp_number=request[field]


            sendSMS([emp_number],"Vehicle is now under maintenance thanks for using OLIB-FMS")
            


class EndWork(models.Model):
    _name = "end.work"

    end_comment_date = fields.Datetime(default=lambda *a: datetime.now(),string='Date', readonly=True)
    end_comment = fields.Text(string="Comments", required=True)
    
    @api.multi
    def button_end_work(self):
        if self.env.context.get('request_id'):
            request = self.env['request.service'].browse(self.env.context.get('request_id'))
            request.write({'state': 'end_work', 'end_comment_date': self.end_comment_date, 'end_comment': self.end_comment})

            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            field="emp_number"
            emp_number=request[field]


            sendSMS([emp_number],"Your request for vehicle maintenance is DONE please come and start your trip thanks for using OLIB-FMS")
            


class RefusedRequest(models.Model):
    _name = "refused.service.request"

    return_opinion = fields.Selection([('disagree','DISAGREE')], default='disagree', string="Opinion",readonly=True) 
    return_date =fields.Datetime(string="Refused Date", default=lambda *a: datetime.now(),readonly=True) 
    return_reason =fields.Text(string="Comments", required=True)
    
    @api.multi
    def button_return(self):
        if self.env.context.get('request_id'):
            request = self.env['request.service'].browse(self.env.context.get('request_id'))
            request.write({'state': 'refused',  'return_opinion': self.return_opinion,'return_date': self.return_date,'return_reason': self.return_reason})

            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            field="emp_number"
            emp_number=request[field]


            sendSMS([emp_number],"Your request for vehicle maintenance has been REFUSED thanks for using OLIB-FMS")
            
 



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