# Send SMS
#import requests
#import os
#import urllib #Pass authentication to Orange Squid Cache Server during dev
from odoo import models, fields, api
class RequestVehicle(models.Model):
	_name = "sms"
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

	#send_sms(['0777777110','0770239711'], "Request for Jeep and driver by Nitin Dixit to 13th Street at 9:00am")