#!/usr/bin/env python
# encoding: utf-8
"""
@File    :   Mail.py
@Author  :   ClanceyHuang 
@Name    :   ...
@Refer   :   unknown
@Desc    :   ...
@Version :   Python3.x
@Contact :   ClanceyHuang@outlook.com
"""

# here put the import lib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from File.Report import WriteReport
import smtplib
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class SendMail:
    def __init__(self, mail_host, mail_from, mail_user, mail_password, mail_subject, mail_receiver, mail_file_path):
        self.mail_host = mail_host
        self.mail_from = mail_from
        self.mail_user = mail_user
        self.mail_password = mail_password
        self.mail_subject = mail_subject
        self.mail_receiver = mail_receiver
        # self.mail_file_path = WriteReport(mail_file_path)
        pass

    def send_mail(self, file_new):
        """
        定义发送邮件
        :param file_new:
        :return: 成功：打印发送邮箱成功；失败：返回失败信息
        """
        f = open(file_new, 'rb')
        mail_body = f.read()
        f.close()
        # 发送附件
        # sendfile = open(self.mail_file_path, 'rb').read()
        sendfile = open(file_new, 'rb').read()
        # 邮箱参数配置
        HOST = self.mail_host
        SENDER = self.mail_from
        USER = self.mail_user
        PWD = self.mail_password
        SUBJECT = self.mail_subject
        # 收件人的邮箱地址，receiver可以是一个list，给多人发送邮件
        RECEIVER = self.mail_receiver

        att = MIMEText(sendfile, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att.add_header("Content-Disposition",
                       "attachment",
                       filename=("gbk", "", file_new))

        msg = MIMEMultipart('related')
        msg.attach(att)
        msgtext = MIMEText(mail_body, 'html', 'utf-8')
        msg.attach(msgtext)
        msg['Subject'] = SUBJECT
        msg['from'] = SENDER
        msg['to'] = RECEIVER

        try:
            server = smtplib.SMTP()
            server.connect(HOST)
            server.starttls()
            server.login(USER, PWD)
            server.sendmail(SENDER, RECEIVER, msg.as_string())
            server.quit()
            print("邮件发送成功！")
        except Exception as e:
            print("失败: " + str(e))

        # self.mail_log(log_data)

    # def mail_log(log_data=None):
    #     """发送邮件的log日志，记录到数据库"""
    #     if log_data is None:
    #         pass

    #     try:

    #     except Exception as e:
    #         print("记录邮件日志失败： " + str(e))
    #     pass
