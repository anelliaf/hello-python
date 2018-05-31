from email.headerregistry import Address
from email.message import EmailMessage
from email.mime.text import MIMEText
import os
import smtplib
import psutil

# mail server details
mail_server = 'localhost'
mail_server_port = 25

# OS variables
email_address = os.getenv('MAIL_ADDRESS', None)
recipient_address = os.getenv('TO_ADDR', None)
subject_desc = 'Test'
host = os.getenv('HOST', None)
limit = os.getenv('LIMIT', None)

# linux mount points
#
# cast string to integer object with int() function
#
def mounts():
    devs = psutil.disk_partitions()
    for dev in devs:
            part = int(psutil.disk_usage(dev.mountpoint).percent)
            if part > int(limit):
                yield [dev.mountpoint, part]

# converting objects returned from mount() function to a list
list_mounts = list(mounts())

# format list
def list_out(list_in):
    return '\n'.join('Drive: {0:10s} Used Space: {1:5.2f}'.format(*drive) for drive in list_in)

# assign list output to variable for email body
email_body = list_out(list_mounts)
email_string = '''
Please check the following drive(s):
{drive_lines}
'''.format(drive_lines=email_body)

# email function
def create_email_message(from_address, to_address, subject, body):
        msg = EmailMessage()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.set_content(body)
        return msg

# main function
if __name__ == '__main__':
        msg = create_email_message(
                from_address=email_address,
                to_address=recipient_address,
                subject='Warning - Drive Space Usage - {}'.format(host),
                body=email_string
        )

with smtplib.SMTP(mail_server, mail_server_port) as smtp_server:
        smtp_server.ehlo()
        smtp_server.send_message(msg)

#print('Email sent successfully')
