#!/usr/bin/python3

import smtplib
import sys

sender = 'michal@openremote.io'
# sender = 'monika_neuker@hotmail.com'
# receivers = ['mrutka@mqlservice.net']
# receivers = ['mrutka@openremote.pl']
receivers = ['michal.rutka@gmail.com']
# receivers = ['michal@michalrutka.com']
# receivers = ['monitoring@openremote.io']
# receivers = ['iems@openremote.io']
subject = ' e-mail test'

print(sender, receivers, subject)
message = '\r\n'.join(
    [
        'From: %s' % sender,
        'To: %s' % receivers[0],
        'CC: michal.rutka@gmail.com',
        'Subject: %s' % subject,
        """
This is a test e-mail message from mqlservice.net via AWS
""",
    ]
)

try:
    server = smtplib.SMTP('email-smtp.eu-west-1.amazonaws.com', 587)
    server.ehlo()
    server.starttls()
    # server.login('AKIAYWIEQF7DFDQ6COSY', 'BKAlqfPOqIwqGG+8Uip3/8CGZEH5WlNacYSs8+M6c0aD')
    server.login(sys.argv[1], sys.argv[2])

    server.sendmail(sender, receivers, message)
    print("Successfully sent email")
except Exception as error:
    print(error)
    print("Error: unable to send email")
