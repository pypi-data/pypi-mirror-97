import json
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import (
    Http404,
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect)
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from . import forms, signals
from .models import Notification, Preference

logger = logging.getLogger(__name__)


def _create_notification(reference, topic, resource_id):
    try:
        preference = Preference.objects.get(reference=reference)
    except Preference.DoesNotExist:
        raise Http404('Invalid slug or reference.')

    notification, created = Notification.objects.update_or_create(topic=topic,
                                                                  resource_id=resource_id,
                                                                  owner=preference.owner,
                                                                  preference=preference,
                                                                  defaults={'status': Notification.STATUS_PENDING, }, )

    if settings.MERCADOPAGO['autoprocess']:
        notification.process()

    signals.notification_received.send(sender=notification)

    return notification, created


class CSRFExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NotificationView(CSRFExemptMixin, View):
    def process(self, request, reference, form):
        if not form.is_valid():
            errors = form.errors.as_json()
            logger.warning('Received an invalid notification: %r, %r', request.GET, errors, extra={'stack': True}, )
            return HttpResponse(errors, status=400, content_type='application/json', )

        notification, created = _create_notification(reference,
                                                     topic=form.TOPICS[form.cleaned_data['topic']],
                                                     resource_id=form.cleaned_data['id'], )

        return JsonResponse({'created': created}, status=201 if created else 200, )

    def get(self, request, reference):
        form = forms.NotificationForm(request.GET)
        return self.process(request, reference, form)

    def post(self, request, reference):
        # The format of notifications when getting a POST differs from the
        # format when getting a GET It can:
        #
        # * Have a JSON with the topic and id in different formats (type and data.id respectively)
        # * Have both in the QueryString
        #
        # application_id = Credentials Client Id
        # user_id = MercadoPago application Id
        # id = reference???? -> NO, reference = external_reference of preference, id = MP ID
        # action = test.created / payment.created / payment.updated
        # api_version = v1
        # date_created
        # live_mode = 'false'???
        # type = test / payment / mp-connect / plan / subscription / invoice

        data = json.loads(request.body)
        topic = data.get('type', data.get('topic'))
        id = data.get('data', data).get('id', request.GET.get('data.id', request.GET.get('id')))

        logger.info('Got POST notification: reference = %s, data = %s', reference, data)
        # print('reference', reference)
        # print('topic', topic)
        # print('id', id)
        form = forms.NotificationForm({'topic': topic, 'id': id, })
        return self.process(request, reference, form)


class PaymentSuccessView(CSRFExemptMixin, View):
    def get(self, request, reference):
        logger.info('Reached payment success view with data: %r', request.GET)
        notification, created = _create_notification(reference,
                                                     topic=Notification.TOPIC_PAYMENT,
                                                     resource_id=request.GET.get('collection_id'), )

        return redirect(settings.MERCADOPAGO['success_url'], pk=notification.pk, )


class PaymentFailedView(CSRFExemptMixin, View):
    def get(self, request, reference):
        logger.info('Reached payment failure view with data: %r', request.GET)
        preference = Preference.objects.get(reference=reference)

        return redirect(settings.MERCADOPAGO['failure_url'], pk=preference.pk, )


class PaymentPendingView(CSRFExemptMixin, View):
    def get(self, request, reference):
        logger.info('Reached payment pending view with data: %r', request.GET)
        preference = Preference.objects.get(reference=reference)

        return redirect(settings.MERCADOPAGO['pending_url'], pk=preference.pk, )


@login_required
def PoolPreferenceView(request, pk=None, goto='mp:preference', *args, **kwargs):
    """ Vai no MP, verifica o status de uma Preference e re-processa. """

    pref = get_object_or_404(Preference, pk=pk)

    pref.poll_status()

    # msg = f'Preference {pref.mp_id}: paid:{pref.paid}'
    msg = None

    url = reverse(goto) + '?' + get_user_model().objects.make_random_password(length=10, allowed_chars='0123456789')
    extrajavascript = "closeActiveTab();"

    if request.is_ajax():
        return JsonResponse(
            {'redirect': request.META['HTTP_REFERER'] + '#' + url, 'extrajavascript': extrajavascript, 'alert': msg})
    else:
        HttpResponseRedirect(url)


class NotificationPreApprovalView(CSRFExemptMixin, View):
    # def process(self, request, reference, form):
    def process(self, request, form):
        if not form.is_valid():
            errors = form.errors.as_json()
            logger.warning('Received an invalid notification: %r, %r', request.GET, errors, extra={'stack': True}, )
            return HttpResponse(errors, status=400, content_type='application/json', )

        notification, created = _create_notification(reference,
                                                     topic=form.TOPICS[form.cleaned_data['topic']],
                                                     resource_id=form.cleaned_data['id'], )

        return JsonResponse({'created': created}, status=201 if created else 200, )

    def get(self, request, reference):
        form = forms.NotificationForm(request.GET)
        return self.process(request, reference, form)

    def post(self, request, reference):
        # The format of notifications when getting a POST differs from the
        # format when getting a GET It can:
        #
        # * Have a JSON with the topic and id in different formats (type and data.id respectively)
        # * Have both in the QueryString
        #
        # application_id = Credentials Client Id
        # user_id = MercadoPago application Id
        # id = reference???? -> NO, reference = external_reference of preference, id = MP ID
        # action = test.created / payment.created / payment.updated
        # api_version = v1
        # date_created
        # live_mode = 'false'???
        # type = test / payment / mp-connect / plan / subscription / invoice

        data = json.loads(request.body)
        topic = data.get('type', data.get('topic'))
        id = data.get('data', data).get('id', request.GET.get('data.id', request.GET.get('id')))

        logger.info('Got POST notification: reference = %s, data = %s', reference, data)
        # print('reference', reference)
        # print('topic', topic)
        # print('id', id)
        form = forms.NotificationForm({'topic': topic, 'id': id, })
        return self.process(request, reference, form)
