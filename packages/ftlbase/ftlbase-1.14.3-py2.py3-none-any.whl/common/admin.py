# -*- coding: utf-8 -*-
from django.contrib import admin

from common.models import Rota


@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'rota', 'modulo', 'nome', 'url', 'reload')
    list_filter = ('reload',)
