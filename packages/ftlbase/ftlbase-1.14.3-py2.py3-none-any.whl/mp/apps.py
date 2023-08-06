from django.apps import AppConfig


class MercadoPagoConfig(AppConfig):
    name = 'mp'
    label = 'mp'
    verbose_name = 'MercadoPago'

    def ready(self):
        from common.models import Rota
        rotas = [
            {'modulo': 'mp', 'rota': 'mp:preference', 'nome': 'MP Preferences', 'reload': True},
            {'modulo': 'mp', 'rota': 'mp:pool_preference_home', 'nome': 'MP Pool Preference', 'reload': True},
            {'modulo': 'mp', 'rota': 'mp:mp_preferences', 'nome': 'Consulta Preferences Diretamente no MP',
             'reload': True},
            {'modulo': 'mp', 'rota': 'mp:notifications_home', 'nome': 'MP Notifications', 'reload': True},
            {'modulo': 'mp', 'rota': 'mp:payment_success_home', 'nome': 'Pagamento Com Sucesso', 'reload': True},
            {'modulo': 'mp', 'rota': 'mp:payment_failure_home', 'nome': 'Paramento com Falha', 'reload': True},
            {'modulo': 'mp', 'rota': 'mp:payment_pending_home', 'nome': 'Pagamento Pendente', 'reload': True},
        ]
        Rota.inicializa_rotas(rotas)
