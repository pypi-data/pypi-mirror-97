# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from common.views import commonRender
from helpdesk.models import Ticket


@login_required
def helpdesk_pendente(request, **kwargs):
    """ Sinaliza que a avaliação vai vencer 5 dias antes """
    hoje = timezone.now().date()
    template_name = kwargs.get('template_name', 'helpdesk_pendente.html')

    if request.user.is_staff:
        # Procura por tickets que foram abertos ou retornados, independente do usuário responsável
        filtro = [Ticket.TICKET_STATUS_ABERTO, Ticket.TICKET_STATUS_RETORNADO]
        qp = Ticket.objects.filter(status__in=filtro)
    else:
        # Procura por tickets do usuário que foram respondidos
        filtro = [Ticket.TICKET_STATUS_RESPONDIDO]
        qp = Ticket.objects.filter(created_by=request.user, status__in=filtro)

    qtde_pendente = qp.count()

    if qtde_pendente:
        msg = '- Há helpdesk(s) pendente(s) para você'
    else:
        msg = ''

    dictionary = kwargs.get('dictionary', {})
    dictionary.update({'msg': msg, 'qtde_pendente': qtde_pendente})

    return commonRender(request, template_name, dictionary)
