#!/usr/bin/env python3

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import smtplib
import os
from email.mime.text import MIMEText

threshold = 80
partition = "/"
cmd = "df -h /"
output = os.popen(cmd).read()

def report_via_email():
    EMAIL_HOST = 'aws-ses-server'
    EMAIL_HOST_USER = "ses-user"
    EMAIL_HOST_PASSWORD = "ses-smtp-pass"
    EMAIL_PORT = 587

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "subject"
    msg['From'] = "sender-email"
    msg['To'] = "receiver-email"

    mime_text = MIMEText(output)
    msg.attach(mime_text)

    s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail("sender-email","receiver-email", msg.as_string())
    s.quit()

def check_once():
    df = subprocess.Popen(["df","-h"], stdout=subprocess.PIPE)
    for line in df.stdout:
        splitline = line.decode().split()
        if splitline[5] == partition:
            if int(splitline[4][:-1]) > threshold:
                report_via_email()
check_once()
