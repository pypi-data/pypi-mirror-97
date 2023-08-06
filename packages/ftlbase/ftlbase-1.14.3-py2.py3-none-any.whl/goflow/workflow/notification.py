#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string

from common.logger import log
from common.celery import email_user


def send_mail(workitems=None, users=None, subject='Workflow - {{ workitems.0 }}', template='goflow/mail-all-pending',
              *args, **kwargs):
    # subject
    # TODO: fazer tratamento do envio de email por grupo no lugar de usuário específico
    task = None

    try:
        subject = settings.EMAIL_SUBJECT_PREFIX + subject
    except Exception:
        pass

    try:
        t = Template(subject)
        dictionary = {'workitems': workitems, 'users': users, 'site': settings.SITE_URL}
        ctx = Context(dictionary)
        subject = t.render(ctx)
        # profile = user[0].userprofile_set.all()[0]  # Porque é FK, deve set O2O
        # profile = user.get_profile()
        try:
            message = render_to_string(template + '.txt', dictionary)
        except Exception as v:
            message = 'send_mail: Erro no render do message'
        try:
            html_message = render_to_string(template + '.html', dictionary)
        except Exception as v:
            html_message = 'send_mail: Erro no render do html_message'

        # user.email_user(subject, message)
        recipient_list = [u.email for u in users]
        task = email_user.delay(recipient_list, subject, message, html_message=html_message)
        # task_description="Envio de email: "+subject)
        # for wi in workitems:
        #     wi.activity.external_task = task
        #     wi.activity.save()
    except Exception as v:
        log.error('send_mail %s %s - %s', workitems, users, v)

    return task
