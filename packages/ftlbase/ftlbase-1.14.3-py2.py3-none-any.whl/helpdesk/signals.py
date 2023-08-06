from django.db.models.signals import post_save
from django.dispatch import receiver

# @receiver(post_save, sender=PublishedContent, dispatch_uid="update_all_children_content")
from common.middleware import get_current_request
from helpdesk.models import Ticket


@receiver(post_save, sender=Ticket)
def ticket_update_status(sender, instance, **kwargs):
    """
    Atualiza todos os compos content das doc conteúdos filhos (mudança de local na Tree, mudança do campo order)
    """
    request = get_current_request()
    save = request.POST.get('save', None)
    if save == Ticket.TICKET_STATUS_MSG_RETORNAR:
        status = Ticket.TICKET_STATUS_RETORNADO
    elif save == Ticket.TICKET_STATUS_MSG_RESPONDER:
        status = Ticket.TICKET_STATUS_RESPONDIDO
    elif save == Ticket.TICKET_STATUS_MSG_ENCERRAR:
        status = Ticket.TICKET_STATUS_ENCERRADO
    else:
        status = Ticket.TICKET_STATUS_ABERTO
    if instance.status != status:
        Ticket.objects.filter(id=instance.pk).update(status=status)
