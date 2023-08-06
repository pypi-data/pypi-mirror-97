# coding=utf-8
'''
zx08443 发送邮件，简单做了一个数据分离，配置的数据单独读取data文件获取

'''
import time
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from testdata import email


# 发送邮件，发送测试报告html
def send_email(newfile):
    f = open(newfile, 'rb')
    mail_body = f.read()
    f.close()
    today = time.strftime('%Y-%m-%d')
    smtpserver = email.data['smtpserver']
    title = email.data['title']
    user = email.data['user']
    password = email.data['password']
    sender = email.data['sender']
    receiver = email.data['receiver']
    cc = email.data['cc']

    # 发送邮件主题
    subject = title + 'api测试报告%s' % today
    msg = MIMEMultipart('mixed')
    msg_html1 = MIMEText(mail_body,
                         'html', 'utf-8')  # 邮件内容
    msg.attach(msg_html1)
    msg_html2 = MIMEText('\n' + "<font  size='5' color='red'>注：请点击链接查看详情</font> ", 'html', 'utf-8')
    msg.attach(msg_html2)
    msg_html = MIMEText(mail_body, 'html', 'utf-8')  # 邮件附件
    msg_html['Content-Disposition'] = 'attachment; filename="TestReport.html"'
    msg.attach(msg_html)
    msg['From'] = sender
    msg['To'] = ';'.join(receiver)
    msg['Cc'] = ';'.join(cc)
    receiver = receiver + cc
    msg['Subject'] = Header(subject, 'utf-8');
    # 连接发送邮件
    try:
        smtp = SMTP_SSL(smtpserver)
        smtp.login(user, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print("邮件发送成功！")
    except smtplib.SMTPException:
        print("Error:无法发送邮件！")
