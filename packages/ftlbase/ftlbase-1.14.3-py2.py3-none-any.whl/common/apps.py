from django.apps import AppConfig
from django.conf import settings


class CommonConfig(AppConfig):
    name = 'common'
    label = 'common'

    def ready(self):
        super().ready()

        from common.models import Configuracao
        import common

        try:
            common.empresa = Configuracao.objects.get(pk=settings.EMPRESA_CORRENTE)
        except Exception as v:
            common.empresa = Configuracao(pk=settings.EMPRESA_CORRENTE, apelido='Exemplo Ltda.')
            common.empresa.save()

        rotas = [
            {'modulo': 'common', 'rota': 'rota', 'nome': 'Rota', 'reload': False},
            {'modulo': 'common', 'rota': 'configuracao', 'nome': 'Configuração', 'reload': False},
            {'modulo': 'common', 'rota': 'workflow_myworks', 'nome': 'Meus Workflows', 'reload': False},
            {'modulo': 'common', 'rota': 'workflow_news', 'nome': 'Workflows Novos', 'reload': False},
            {'modulo': 'common', 'rota': 'workflow_pending', 'nome': 'Workflows Pendentes', 'reload': False},
            {'modulo': 'common', 'rota': 'workflow_all', 'nome': 'Todos os Workflows', 'reload': False},
            {'modulo': 'common', 'rota': 'workflow_action_home', 'nome': 'Workflow', 'reload': True},
            {'modulo': 'common', 'rota': 'version_compare', 'nome': 'Comparar Versões', 'reload': True},
        ]

        from common.models import Rota
        Rota.inicializa_rotas(rotas)
