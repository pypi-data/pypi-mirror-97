# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Model

from common.models import CommonModel, ATIVO_C
from common.utils import ACAO_ADD


class Subject(Model):
    """ Subject of Ticket """

    description = models.CharField(verbose_name='Descrição', max_length=200, blank=False)
    status = models.CharField(max_length=1, null=True, blank=True, verbose_name=u'Status', default='S',
                             choices=ATIVO_C)

    class Meta:
        verbose_name = 'Assunto'
        # verbose_name_plural = 'Contas Bancárias'
        # ordering = ('banco', 'agencia')
        # managed = False
        # db_table = 'municipio'
        # app_label = 'cliente'

    def __str__(self):
        return self.description



class Ticket(CommonModel):
    """
    Capa do Ticket de chamado
    """
    TICKET_SUPORTE = '1'
    TICKET_FINANCEIRO = '2'
    TICKET_LEI = '3'
    TICKET_LEI_SUGESTAO = '4'
    TICKET_SUGESTAO = '5'

    TICKET_SUBJECT_TYPE = (
        (TICKET_SUPORTE, 'Ajuda'),
        (TICKET_FINANCEIRO, 'Financeiro'),
        (TICKET_LEI, 'Lei desatualizada'),
        (TICKET_LEI_SUGESTAO, 'Sugestão de inclusão de lei'),
        (TICKET_SUGESTAO,'Outras sugestões'),
    )

    TICKET_STATUS_ABERTO = 'A'
    TICKET_STATUS_RESPONDIDO = 'R'
    TICKET_STATUS_RETORNADO = 'T'
    TICKET_STATUS_ENCERRADO = 'X'
    TICKET_STATUS = (
        (TICKET_STATUS_ABERTO, 'Aberto'),
        (TICKET_STATUS_RESPONDIDO, 'Respondido'),
        (TICKET_STATUS_RETORNADO, 'Retornado'),
        (TICKET_STATUS_ENCERRADO, 'Encerrado'),
    )
    TICKET_STATUS_MSG_ABRIR= 'Abrir Chamado'
    TICKET_STATUS_MSG_RESPONDER= 'Responder Chamado'
    TICKET_STATUS_MSG_RETORNAR= 'Retornar Chamado'
    TICKET_STATUS_MSG_ENCERRAR = 'Encerrar Chamado'

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=False,
                               verbose_name='Assunto', related_name='%(class)ss')
    description = models.TextField(verbose_name='Descricao', null=False, blank=False,
                                   help_text='Descreva o assunto')
    status = models.CharField(max_length=1, null=True, blank=True, verbose_name=u'Status',
                              default=TICKET_STATUS_ABERTO, choices=TICKET_STATUS)

    class Meta:
        verbose_name = 'Ticket'
        # verbose_name_plural = 'Contas Bancárias'
        # ordering = ('banco', 'agencia')
        # managed = False
        # db_table = 'municipio'
        # app_label = 'cliente'

    def __str__(self):
        return '%s - %s' % (self.pk, self.subject)

    @property
    def can_add(self):
        return self.status != Ticket.TICKET_STATUS_ENCERRADO

    def _permission(self, request, acao):
        return acao == ACAO_ADD or self.created_by == request.user or request.user.is_staff


class FollowUp(CommonModel):
    """
    Um andamento do Ticket
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, blank=False, null=False,
                               verbose_name='Ticket', related_name='%(class)ss')
    followup = models.TextField(verbose_name='Andamento', null=False, blank=False)
    status = models.CharField(max_length=1, null=True, blank=True, verbose_name=u'Status',
                              default=Ticket.TICKET_STATUS_ABERTO, choices=Ticket.TICKET_STATUS)

    class Meta:
        verbose_name = 'Andamento'
        # verbose_name_plural = 'Produtos'
        # ordering = ('nome',)

    def __str__(self):
        return self.followup  # '%s - %s' % (self.pk, self.nome)

    # def get_created_by_display(self):
    #     if self.pk:
    #         if self.created_by == self.ticket.created_by:
    #             return self.created_by.first_name
    #         return 'EstudeBlue'
    #     return None