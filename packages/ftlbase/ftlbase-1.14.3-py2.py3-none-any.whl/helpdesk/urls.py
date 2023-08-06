# -*- coding: utf-8 -*-
from django.urls import path

from common import views as common_views
from common.utils import ACAO_ADD
from . import forms, views


urlpatterns = [
    *common_views.include_CRUD('subject', table=forms.SubjectTable, form=forms.SubjectForm),

    path('ticket/', common_views.commonListaTable, {'model': forms.TicketTable, },
         name='ticket'),
    path('ticket/add/', common_views.commonCadastro,
         {'formModel': forms.TicketInsertForm, 'acao': ACAO_ADD, 'goto': 'ticket',},
         name='ticketAdd'),
    path('ticket/<pk>/<str:acao>/', common_views.commonCadastro,
         {'formModel': forms.TicketForm, 'goto': 'ticket', 'configuraButtons': False,},
         name='ticketEditDelete'),
    path('helpdesk-pendente/', views.helpdesk_pendente, name='helpdesk_pendente'),
]
