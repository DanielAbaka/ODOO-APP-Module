# -*- coding: utf-8 -*-
import requests
from odoo import api, fields, models, tools
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import Warning
from odoo.exceptions import  ValidationError



class EmployeeLeaveRequest(models.Model):
    _name = 'leave.request'

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('leave.request')
        return super(EmployeeLeaveRequest, self).create(vals)


    state = fields.Selection([('new', 'NEW REQUEST'), ('manager', 'MANAGER'),('hr', '(HR) HUMAN RESOURCE'),('accepted', 'ACCEPTED'),('reject', 'REJECTED')], default='new')
    # print_b = fields.Boolean('Print', default=True, track_visibility="onchange")
    #Employe Leave Request Starts Here
    name = fields.Char(string='Request Number', copy=False)
    emp_name = fields.Many2one('employee.details',string="Employee", required=True)
    emp_id = fields.Char(related="emp_name.registration_id", string="ID")
    emp_number = fields.Char(related="emp_name.employee_number",string="Number")
    emp_department = fields.Char(related="emp_name.department",string="Department")
    # emp_status = fields.Many2one(string="Status", readonly=True)
    num_days_used = fields.Integer(string="Days Used")
    date_requested = fields.Datetime(string="Request Date",default=lambda *a: datetime.now(), readonly=True)
    manager_name = fields.Many2one('manager.details',string="Manager Name", required=True)
    manager_id = fields.Char(related="manager_name.registration_id",string="Manager ID", readonly=True)
    manager_number = fields.Char(related="manager_name.manager_number",string="Manager Number", readonly=True)
    leave_type = fields.Many2one('leave.type',string="Type Of Leave", required=True)
    depature_date = fields.Date(string="Planned Date of Leave", required=True)
    return_date = fields.Date(string="Planned Date of Return", required=True)
    total_number_of_days = fields.Float(compute="_compute_total_days", string="Total Days")
    #Function 
    def _get_number_of_days(self, depature_date, return_date):
        """Returns a float equals to the timedelta between two dates given as string."""
        DATETIME_FORMAT = "%Y-%m-%d"
        from_dt = datetime.strptime(depature_date, DATETIME_FORMAT)
        to_dt = datetime.strptime(return_date, DATETIME_FORMAT)
        timedelta = to_dt - from_dt
        diff_day = timedelta.days + float(timedelta.seconds) / 86400
        return diff_day

    @api.depends('depature_date','return_date')
    def _compute_total_days(self):
        for record in self:
            if record.depature_date and record.return_date:
                record.total_number_of_days = self._get_number_of_days(record.depature_date, record.return_date)
           

    emp_comment = fields.Text(string="Employee Comment", required=True)
    #Refused Leave Request Starts Here
    reject_opinion = fields.Selection([('DISAGREE', 'DISAGREE')],default='DISAGREE', string='Approval')
    reject_date =fields.Datetime(string="Date") 
    reject_reason =fields.Text(string="Comment") 
    #Manager Approved Leave Request Starts Here
    opinion = fields.Selection([('AGREE', 'AGREE')],default='AGREE', string='Approval', readonly=True)
    approved_date = fields.Datetime(default=lambda *a: datetime.now(),string='Date', readonly=True)
    replacement_name = fields.Many2one('employee.details',string='Replacement Name')
    replacement_number = fields.Char(related='replacement_name.employee_number', string='Mobile', readonly=True)
    human_resource_name = fields.Many2one('manager.details',string='HR Manager')
    human_resource_number = fields.Char(related='human_resource_name.manager_number', string='Mobile', readonly=True)
    comment = fields.Text(string="Comment")
    #Human Resource Approved Leave Request Starts Here
    previous_leave = fields.Integer(string="Previous Leave:")
    current_leave_deduction = fields.Integer(string="Leave Deduction:")
    remaining_leave_balc = fields.Integer(string="Remaining Leave:")
    prev_sick_leave_bal = fields.Integer(string="Previous Sick Leave:")
    prev_sick_leave_dedu = fields.Integer(string="Sick Leave Deduction:")
    remaining_sick_leave_balc = fields.Integer(string="Remaining Sick Leave:")
    hr_opinion = fields.Selection([('ACCEPTED', 'ACCEPTED')],default='ACCEPTED', string='Approval:')
    date = fields.Datetime(string="Date:",default=lambda *a: datetime.now()) 
    hr_comment = fields.Text(string="Comment")

    # @api.multi
    # @api.depends('depature_date','return_date')
    # def _compute_days(self):
    #     for s in self:
    #         if s.depature_date and s.return_date:
    #             a = s.depature_date - s.return_date
    #             s.total_number_of_days = a.days
    #         else:
    #             s.total_number_of_days = 0

    @api.multi
    def button_submit(self):
        for record in self:
            record.write({'state': 'manager'})

    
        #leave request sms notification starts here
        method_name = 'send_sms'
        sendSMS = getattr(SMS,method_name)
        emp_number=record["emp_number"]
        manager_number=record["manager_number"]
        employee = str(self.emp_name.employee_lname)+" "+str(self.emp_name.employee_fname)
        days_num = str(self.total_number_of_days)
        type_leave = str(self.leave_type.leave_type)

        #SMS Start
        sendSMS([manager_number],"Hello "+employee+" is requesting for a "+days_num+" Days "+type_leave+" need your Approval thanks from OLIB LEAVE MANAGEMENT")
        
        sendSMS([emp_number],"Hello your request has been sent to your Manager for Approval thanks for using OLIB LEAVE MANAGEMENT")

   
class ManagerRequestValidate(models.Model):
    _name = "manager.validate.leave"

    opinion = fields.Selection([('AGREE', 'AGREE')],default='AGREE', string='Approval', readonly=True)
    approved_date = fields.Datetime(default=lambda *a: datetime.now(),string='Date', readonly=True)
    replacement_name = fields.Many2one('employee.details',string='Replacement Name', required=True)
    replacement_number = fields.Char(related='replacement_name.employee_number', string='Mobile', readonly=True)
    human_resource_name = fields.Many2one('manager.details',string='HR Manager', required=True)
    human_resource_number = fields.Char(related='human_resource_name.manager_number', string='Mobile', readonly=True)
    comment = fields.Text(string="Manager Comment", required=True)


    @api.multi
    def button_send(self):
        if self.env.context.get('request_id'):
            request = self.env['leave.request'].browse(self.env.context.get('request_id'))
            request.write({'state': 'hr', 'opinion': self.opinion, 'approved_date': self.approved_date, 'replacement_name': self.replacement_name.id, 'replacement_number': self.replacement_number,'human_resource_name': self.human_resource_name.id, 'human_resource_number': self.human_resource_number, 'comment': self.comment})
            
            #leave request sms notification starts here
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            field="emp_number"
            emp_number=request[field]
            field="manager_number"
            manager_number=request[field]
            field="human_resource_number"
            human_resource_number=request[field]
            field="replacement_number"
            replacement_number=request[field]
            field="emp_name"
            emp_name=request[field]
            emp_name = str(emp_name.employee_lname)+" "+str(emp_name.employee_fname)
            # days_num = str(self.total_number_of_days)
            # type_leave = str(self.leave_type.leave_type)

            #SMS Start
            sendSMS([manager_number],"Employee leave request has been sent to HR successfully thanks from OLIB LEAVE MANAGEMENT")
            
            sendSMS([replacement_number],"Hello you will PROXY for " +emp_name+" while on his leave thanks from OLIB LEAVE MANAGEMENT")
            
            sendSMS([human_resource_number],"Hello approved employee leave request has been sent to you for final Approval thanks from OLIB LEAVE MANAGEMENT")
            
            sendSMS([emp_number],"Your leave request has been Approved by your Manager and forward to HR for final Approval thanks for using OLIB LEAVE MANAGEMENT")



class HRApproval(models.Model):
    _name = "hr.approve.leave"

    previous_leave = fields.Integer(string="Previous Leave:", default=0, required=True)
    current_leave_deduction = fields.Integer(string="Leave Deduction:", default=0, required=True)
    remaining_leave_balc = fields.Integer(string="Remaining Leave:", default=0, required=True)
    prev_sick_leave_bal = fields.Integer(string="Previous Sick Leave:", default=0, required=True)
    prev_sick_leave_dedu = fields.Integer(string="Sick Leave Deduction:", default=0, required=True)
    remaining_sick_leave_balc = fields.Integer(string="Remaining Sick Leave:", default=0, required=True)
    hr_opinion = fields.Selection([('ACCEPTED', 'ACCEPTED')],default='ACCEPTED', string='Approval:', readonly=True)
    date = fields.Datetime(string="Date:",default=lambda *a: datetime.now(),readonly=True) 
    hr_comment = fields.Text(string="HR Manager Comment", required=True)

    @api.multi
    def button_aprove(self):
        if self.env.context.get('request_id'):
            request = self.env['leave.request'].browse(self.env.context.get('request_id'))
            request.write({'state': 'accepted', 'previous_leave': self.previous_leave,'current_leave_deduction': self.current_leave_deduction, 'remaining_leave_balc': self.remaining_leave_balc, 'prev_sick_leave_bal': self.prev_sick_leave_bal,'prev_sick_leave_dedu': self.prev_sick_leave_dedu, 'remaining_sick_leave_balc': self.remaining_sick_leave_balc, 'hr_opinion': self.hr_opinion, 'date': self.date, 'hr_comment': self.hr_comment})


            #HRApproval leave request sms notification starts here
            # field="emp_number"
            # emp_number=request[field]         
            # method_name = 'send_sms'
            # sendSMS = getattr(SMS,method_name)
            # sendSMS([emp_number],)

            # method_name = 'send_sms'
            # sendSMS = getattr(SMS,method_name)
            # field="emp_number"
            # emp_number=request[field]
            
            # sendSMS([emp_number],"Your leave request has been finally ACCEPTED & APPROVED by Human Resource Manager thanks for using OLIB LEAVE MANAGEMENT")

            field="emp_number"
            emp_number=request[field]
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            sendSMS([emp_number],self.hr_comment)

    #------------------------------------------------------------------------------------


    # @api.multi
    # def print_leave_request(self):
    #     return self.env.ref('leave.request').report_action(self)



class ReturnRequest(models.Model):
    _name = "return.request.leave"

    reject_opinion = fields.Selection([('DISAGREE', 'DISAGREE')],default='DISAGREE', string='Approval', readonly=True)
    reject_date =fields.Datetime(string="Date", default=lambda *a: datetime.now(),readonly=True) 
    reject_reason =fields.Text(string="Comment", required=True) 


    @api.multi
    def button_return(self):
        if self.env.context.get('request_id'):
            request = self.env['leave.request'].browse(self.env.context.get('request_id'))
            request.write({'state': 'reject', 'reject_opinion': self.reject_opinion,'reject_date': self.reject_date, 'reject_reason': self.reject_reason})

            #Employee Leave reject request_sms_notification_starts_here
            field="emp_number"
            emp_number=request[field]
            method_name = 'send_sms'
            sendSMS = getattr(SMS,method_name)
            sendSMS([emp_number],self.reject_reason)


    # @api.multi
    # def print_quotation(self):
    #     self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
    #     return self.env.ref('.action_report_saleorder').report_action(self)


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
                    <d4p1:OriginatingNumber>OLIB-LEAVE</d4p1:OriginatingNumber>\
                  </c_subs_req>\
                </SubscriberSendNotification>\
              </s:Body>\
            </s:Envelope>\
            " %(recipient_number, message_content)
            response = requests.post(url,data=body,headers=headers)
            print(response.content)

            return response

        return False