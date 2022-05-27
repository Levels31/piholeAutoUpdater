import smtplib, ssl

message = """\
Subject: Hi there

This message is sent from Python."""


def read_config(file_path):
    with open("config.cfg", "r") as file:
        lines = file.readlines()
        for string in lines:
            key, value = string.split("=")[0].strip(), string.split("=")[1].strip()
            if key == "sender_mail":
                print("found sender mail: " + value)
                sender_mail = value

            if key == "password":
                password = value
            
            if key == "port":
                port = value

            if key == "receiver_mail":
                receiver_mail = value


        file.close()
    return sender_mail, password, port, receiver_mail

sender_mail, password, port, receiver_mail = read_config("config.cfg")
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_mail, password)
    server.sendmail(sender_mail, receiver_mail, "This is a test")
