#!/usr/bin/env python
# encoding: utf-8

import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from contextlib import closing

from config.config import SMTP_CONFIG
from utils.common_utils import classproperty


class SMTPUtils(object):

    @classmethod
    def send_email(cls, to, subject, msg, attachment=None):
        msg = cls.prepare_msg(to, subject, msg, attachment)
        with cls.smtp_context as ctx:
            cls.login(ctx)
            ctx.sendmail(cls.sender, to, msg)

    @classmethod
    def prepare_msg(cls, to, subject, msg, attachment):
        m = MIMEMultipart("alternative")
        m['Subject'] = subject
        m['From'] = SMTP_CONFIG.FROM
        m['To'] = cls.prepare_target(to)
        m.attach(MIMEText(msg, 'html', 'utf-8'))
        if attachment:
            att1 = MIMEText(open(attachment).read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="%s"' % attachment[len(os.path.dirname(attachment)) + 1:]
            m.attach(att1)
        return m.as_string()

    @classmethod
    def prepare_target(cls, to):
        print to
        if isinstance(to, basestring):
            to = [to]
        return ', '.join(to)

    @classmethod
    def login(cls, smtp_instance):
        smtp_instance.login(cls.sender, SMTP_CONFIG.PASSWORD)

    @classproperty
    def sender(cls):
        return SMTP_CONFIG.USER

    @classproperty
    def smtp_context(cls):
        return closing(smtplib.SMTP(SMTP_CONFIG.HOST))
