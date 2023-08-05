#!/usr/bin/env python3

import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mail_statement(
        target_email: str,
        email_subject: str,
        email_text: str,
        attach_file_name_absolute_path: str,
        mail_server_host: str,
        mail_server_port: int,
        source_email: str = None,
) -> None:
    if not os.path.exists(attach_file_name_absolute_path):
        raise Exception(f"Soubor přílohy neexistuje {attach_file_name_absolute_path}")

    # TODO testing value, delete
    target_email = "marek.sebera@gmail.com"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = source_email
    msg['To'] = target_email

    part1 = MIMEText(email_text, 'plain')
    msg.attach(part1)

    with open(attach_file_name_absolute_path, 'rb') as attachment_file:
        attachment_name = os.path.basename(attach_file_name_absolute_path)

        part = MIMEApplication(attachment_file.read(), _subtype='pdf')
        part.add_header(_name="Content-Disposition", _value="attachment", filename=attachment_name)
        msg.attach(part)

    with smtplib.SMTP(host=mail_server_host, port=mail_server_port) as smtp_session:
        smtp_session.ehlo()
        smtp_session.sendmail(source_email, target_email, msg.as_string())
        smtp_session.quit()
