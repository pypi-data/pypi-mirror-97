#!/usr/bin/python3
# -*- coding: utf-8 -*-
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import configparser
import smtplib
from email.mime.base import MIMEBase
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.encoders import encode_base64
from getpass import getpass
import time
import os
import sys
import csv

def send_emails(config_file, body_file, student_file='students.csv', dryrun=False):
    config = configparser.ConfigParser()
    config.read(config_file)
    from_address = config['DEFAULT']['FROM_ADDRESS']
    with open( body_file, 'r') as f:
        body_template = f.read()

    ###########################

    if not dryrun:
        smtppass = getpass('email password, please:')
        server = smtplib.SMTP_SSL(config['DEFAULT']['SMTPSERVER'], config['DEFAULT']['SMTPPORT'])
        print( server.ehlo())

        if config['DEFAULT']['AUTHREQUIRED']:
            print (server.login(config['DEFAULT']['SMTPUSER'], smtppass))

    ###########################
    data = list(csv.reader(open(student_file, 'r')))
    fields = data[0]
    student_data = data[1:]
    indices = {field:i for i,field in enumerate(fields)}
    attachment_string = config['DEFAULT'].get('ATTACHMENT')

    for row in student_data:
        if not row: continue
        email = row[indices['email']]
        student_dict = {field:row[indices[field]] for field in fields}
        if attachment_string:
            if attachment_string in ('true', 'True', 'yes', 'Yes'):
                attachment_path = row[indices['attachment']]
            else:
                attachment_path = attachment_string.format(**student_dict)
            try:
                attachment = MIMEApplication(open(attachment_path, 'rb').read(),_subtype="pdf")
            except FileNotFoundError:
                print('Missing file:', attachment_path)
                print('   No email sent to', email)
                continue
        else:
            attachment_path = ''

        toaddrs = [email, from_address]
        body = body_template.format(**student_dict)

        msg = MIMEMultipart()
        msg['Subject'] = config['DEFAULT']['SUBJECT']
        msg['To'] = email
        msg['From'] = from_address
        part2 = MIMEText(body, 'plain', 'utf8')
        msg.attach(part2)
        if attachment_string:
            attachment_name = os.path.split(attachment_path)[-1]
            msg.attach(attachment)
            attachment.add_header('Content-Disposition', 'attachment; filename="%s"'%attachment_name)

        #Send
        try:
            if email.split('@')[1]=='example.com' or dryrun:
                print('example email to', email)
                print(body)
            else:
                smtpresult = server.sendmail(from_address, [email, from_address], msg.as_string())
            print ('ok', email)
        except Exception as e:
            print ('There was an error sending the message to: %s'%email)
            print(e)

        time.sleep(int(config['DEFAULT']['DELAY']))

    if not dryrun:
        server.close()
