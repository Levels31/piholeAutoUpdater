import smtplib
import ssl
import logging
import datetime
from email.message import EmailMessage
from socket import gaierror

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S Uhr: ', filename='run.log', encoding='utf-8', level=logging.DEBUG)
date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

def sendmail(subject, body):
	context = ssl.create_default_context()
	sender_mail, password, port, receiver_mail = read_config("config.cfg")
	msg = EmailMessage()
	msg['Subject'] = subject
	msg['From'] = sender_mail
	msg['To'] = receiver_mail
	msg.set_content(body)

	for i in range(3):
		try:
			with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
				server.login(sender_mail, password)
				server.send_message(msg)
				#server.sendmail(sender_mail, receiver_mail, final_message)
				logging.info("Email sent")
				server.quit()
				return 
				
		except gaierror:
			logging.info(f"Try {i}: Temporary fail in name resolution")
				
	logging.error("Error: Could not send email after 3 tries. Exiting Programm")
	exit(-1)


def read_config(file_path):
	with open("config.cfg", "r") as file:
		lines = file.readlines()
		for string in lines:
			key, value = string.split("=")[0].strip(), string.split("=")[1].strip()
			if key == "sender_mail":
				sender_mail = value

			if key == "password":
				password = value

			if key == "port":
				port = value

			if key == "receiver_mail":
				receiver_mail = value


	file.close()
	return sender_mail, password, port, receiver_mail