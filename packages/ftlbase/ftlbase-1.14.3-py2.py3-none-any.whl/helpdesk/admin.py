# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Ticket, FollowUp


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_by',
        'created_at',
        'modified_by',
        'modified_at',
        'subject',
        'description',
        'status',
    )
    list_filter = ('created_by', 'created_at', 'modified_by', 'modified_at')
    date_hierarchy = 'created_at'


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_by',
        'created_at',
        'modified_by',
        'modified_at',
        'ticket',
        'followup',
        'status',
    )
    list_filter = (
        'created_by',
        'created_at',
        'modified_by',
        'modified_at',
        'ticket',
    )
    date_hierarchy = 'created_at'
