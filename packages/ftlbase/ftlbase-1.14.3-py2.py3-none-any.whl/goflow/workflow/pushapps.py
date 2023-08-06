#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from common.logger import Log

log = Log('goflow.workflow.pushapps')


def route_to_requester(workitem):
    """Simplest possible pushapp
    """
    return workitem.instance.user


def route_to_user(workitem, user):
    """Route to user given a user name
    """
    cls_user = get_user_model()
    return cls_user.objects.get(username=user)
    # return User.objects.get(user=user)


def route_to_superuser(workitem, username='admin'):
    """Route to the superuser
    """
    cls_user = get_user_model()
    user = cls_user.objects.get(username=username)
    if user.is_superuser:
        return user
    log.warning('this user is not a super-user:', username)
    return None


def to_current_superuser(workitem, user_pushed):
    """Should be used in all push applications for testing purposes.

        (**NOT IMPLEMENTED**)

        usage::

            return to_current_superuser(workitem, user_pushed)
    """
    return None


def route_to_object_user(workitem):
    """Route to user defined by object
    """
    user = workitem.instance.wfobject().get_workflow_user()

    return user
