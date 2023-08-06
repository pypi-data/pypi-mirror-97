#!/usr/bin/env python3

import asyncio
import aiosmtplib
import smtplib
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL_PARAMS = {'TLS': False, 'host': 'smtp.estudeblue.com.br', 'password': 'AdmSbl8', 'user': 'contato@estudeblue.com.br', 'port': 587}

if sys.platform == 'win32':
    loop = asyncio.get_event_loop()
    if not loop.is_running() and not isinstance(loop, asyncio.ProactorEventLoop):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)


async def send_mail_async(sender, to, subject, text, textType='plain', **params):
    """Send an outgoing email with the given parameters.

    :param sender: From whom the email is being sent
    :type sender: str

    :param to: A list of recipient email addresses.
    :type to: list

    :param subject: The subject of the email.
    :type subject: str

    :param text: The text of the email.
    :type text: str

    :param textType: Mime subtype of text, defaults to 'plain' (can be 'html').
    :type text: str

    :param params: An optional set of parameters. (See below)
    :type params; dict

    Optional Parameters:
    :cc: A list of Cc email addresses.
    :bcc: A list of Bcc email addresses.
    """
    print('envia email')
    # return
    # Default Parameters
    cc = params.get("cc", [])
    bcc = params.get("bcc", [])
    mail_params = params.get("mail_params", MAIL_PARAMS)

    # Prepare Message
    msg = MIMEMultipart()
    msg.preamble = subject
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(to)
    if len(cc): msg['Cc'] = ', '.join(cc)
    if len(bcc): msg['Bcc'] = ', '.join(bcc)

    msg.attach(MIMEText(text, textType, 'utf-8'))

    # Contact SMTP server and send Message
    host = mail_params.get('host', 'localhost')
    isSSL = mail_params.get('SSL', False)
    isTLS = mail_params.get('TLS', False)
    port = mail_params.get('port', 465 if isSSL else 25)
    print('mail 1')
    smtp = aiosmtplib.SMTP(hostname=host, port=port, use_tls=isSSL)
    print('mail 2')
    await smtp.connect()
    print('mail 3')
    if isTLS:
        await smtp.starttls()
    print('mail 4')
    if 'user' in mail_params:
        await smtp.login(mail_params['user'], mail_params['password'])
    print('mail 5')
    await smtp.send_message(msg)
    print('mail 6')
    await smtp.quit()
    print('mail 7')


def sendmailasync(**params): #sender, to, subject, text, textType, **params):
    """Send an outgoing email with the given parameters.

    :param sender: From whom the email is being sent
    :type sender: str

    :param to: A list of recipient email addresses.
    :type to: list

    :param subject: The subject of the email.
    :type subject: str

    :param text: The text of the email.
    :type text: str

    :param textType: Mime subtype of text, defaults to 'plain' (can be 'html').
    :type text: str

    :param params: An optional set of parameters. (See below)
    :type params; dict

    Optional Parameters:
    :cc: A list of Cc email addresses.
    :bcc: A list of Bcc email addresses.
    """
    # Default Parameters
    #
    sender ='was@ftl.com.br'
    to = [sender]
    subject= 'Teste 4'
    text='Teste 4 message'
    textType='plain'

    print(sender)


if __name__ == "__main__":
    email = "was@ftl.com.br"
    print('1')
    co1 = send_mail_async(email,
              [email],
              "Test 1",
              'Test 1 Message',
              textType="plain")
    print('2')
    # co2 = send_mail_async(email,
    #           [email],
    #           "Test 2",
    #           'Test 2 Message',
    #           textType="plain")
    print('3')
    loop = asyncio.get_event_loop()
    print('4')
    # loop.run_until_complete(asyncio.gather(co1, co2))
    loop.run_until_complete(asyncio.gather(co1))
    # loop.run_until_complete(co1)
    # loop.run_in_executor(None, sendmailasync, ) #[email, [email], 'Teste 4', 'Teste 4 message', 'plain']) #sender=email, to=[email], subject= 'Teste 3', text= 'Teste 3 message', textType='plain')
    # print('5')
    # loop.run_in_executor(None, sendmailasync, ) #{'sender':email, 'to':[email], 'subject': 'Teste 4', 'text': 'Teste 4 message', 'textType':'plain'})
    # print('5.1')
    # loop.run_in_executor(None, sendmailasync, ) #{'sender':email, 'to':[email], 'subject': 'Teste 5', 'text': 'Teste 5 message', 'textType':'plain'})
    # print('5.2')
    # co3 = send_mail_async(email,
    #           [email],
    #           "Test 3",
    #           'Test 3 Message',
    #           textType="plain")
    # loop.create_task(co3)
    # print('6')
    # loop.run_forever()
    print('7')
    loop.close()
    print('8')


