# -*- coding: utf-8 -*-

from django.apps import AppConfig


class HelpdeskConfig(AppConfig):
    name = 'helpdesk'

    def ready(self):
        from .signals import ticket_update_status
        assert ticket_update_status

        from common.models import Rota

        rotas = [
            {'modulo': 'helpdesk', 'rota': 'subject', 'nome': 'Assunto', 'reload': True},
            {'modulo': 'helpdesk', 'rota': 'ticket', 'nome': 'Helpdesk', 'reload': True},
            # {'modulo': 'finan', 'rota': 'mercadopago_home', 'nome': 'Mercado pago', 'reload': True},
        ]
        Rota.inicializa_rotas(rotas)
