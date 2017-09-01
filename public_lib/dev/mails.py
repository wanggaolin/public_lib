#!/usr/bin/env python
#encoding=utf-8
import traceback
import os
import re
import sys
import smtplib
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from collections import namedtuple
from error_msg import RaiseVlues
from email import message_from_string

class _send_mail(object):
    def __init__(self,*args,**kwargs):
        self.user = kwargs['user']
        self.passwd = kwargs['passwd']
        self.smtp = kwargs['smtp']
        self.to_list = kwargs['to_list']
        self.subject = kwargs['subject']
        self.status = namedtuple('mail', ['status', "msg"])

    def mail(self,conntext):
        if (float(sys.getsizeof(conntext)) / 1024 / 1024) < 2: #2MB
            msg=MIMEText(conntext,_charset='utf-8')
            msg['Subject'] = self.subject
            msg['From'] = self.user
            msg['To'] = ",".join(self.to_list)
            try:
                server = smtplib.SMTP()
                server.connect(self.smtp,"25")
                # server.starttls()
                server.login(self.user,self.passwd)
                server.sendmail(self.user,self.to_list,msg.as_string())
                server.quit()
                return self.status(True,'')
            except Exception, e:
                return self.status(False, e)
        else:
            return self.file(conntext,file_type='text')

    def file(self,file_list,file_type=list):
        try:
            MailConntent = 'Please see the attachment!!'
            Server = smtplib.SMTP(self.smtp)
            Server.login(self.user,self.passwd)
            main_msg = email.MIMEMultipart.MIMEMultipart()
            text_msg = email.MIMEText.MIMEText(MailConntent, _charset='utf-8')
            main_msg.attach(text_msg)
            contype = 'application/octet-stream'
            maintype, subtype = contype.split('/', 1)
            FileMsg = email.MIMEBase.MIMEBase(maintype, subtype)
            Conntent = ''
            if type(file_type) is type:
                for i in file_list:
                    with open(i) as P:
                        attachment = MIMEApplication(P.read())
                        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(i))
                        main_msg.attach(attachment)
            else:
                attachment = MIMEApplication(file_list)
                attachment.add_header('Content-Disposition', 'attachment', filename="mail_conntent")
                main_msg.attach(attachment)
            main_msg['From'] = self.user
            main_msg['To'] = ",".join(self.to_list)
            main_msg['Subject'] = self.subject
            main_msg['Date'] = email.Utils.formatdate( )
            Server.sendmail(self.user, self.to_list, main_msg.as_string())
            return self.status(True, '')
        except Exception, e:
            return self.status(False, e)


def mail_text(text):
    'fomat mail head or text'
    message = message_from_string(text)
    text = ''.join(re.split(r'\S+: \S+\n\n', text, 1)[1:])
    return {"text":text,"From":message['From'],"To":message['To'],"Date":message['Date'],"Subject":message['Subject'],}


def send_mail(smtp=None,user=None,passwd=None,subject='',text='',to_list=[]):
    """
    send email of text
    :param smtp: email of smtp
    :param user: email of user
    :param passwd: email of password
    :param subject: email of subject
    :param text: send text
    :param to_list: revert user list
    :return:
    """
    if  not type(to_list) is list:
        raise  RaiseVlues("to_list must be list")
    return _send_mail(smtp=smtp,user=user,passwd=passwd,subject=subject,to_list=to_list).mail(text)

def send_file(smtp=None,user=None,passwd=None,subject='',file_list='',to_list=[]):
    """
    send email of file
    :param smtp: email of smtp
    :param user: email of user
    :param passwd: email of password
    :param subject: email of subject
    :param file_list: file list,example:[file1,file2]
    :param to_list: revert user list
    :return:
    """
    if  not type(to_list) is list:
        raise  RaiseVlues("to_list must be list")
    elif  not type(file_list) is list:
        raise  RaiseVlues("file_list must be list")
    return _send_mail(smtp=smtp,user=user,passwd=passwd,subject=subject,to_list=to_list).file(file_list)


