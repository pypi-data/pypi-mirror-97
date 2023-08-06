import logging

import requests
from django.conf import settings
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mercadopago import MP

from common.utils import ACAO_VIEW
from . import signals

logger = logging.getLogger(__name__)


class MercadoPagoServiceException(Exception):
    pass


class MercadoPagoService(MP):
    """
    MercadoPago service (the same one from the SDK), lazy-initialized on first
    access.
    """

    def __init__(self, account):
        if account.sandbox:
            super().__init__('TEST-3476988363526582-061923-784172ff2b561421cd20deea7d50e6df-587565780')
        else:
            super().__init__(account.app_id, account.secret_key)
        self.sandbox_mode(account.sandbox)


class Account(models.Model):
    """
    A mercadopago account, aka "application".
    """
    name = models.CharField(_('name'), max_length=32, help_text=_('A friendly name to recognize this account.'), )
    slug = models.SlugField(_('slug'), unique=True,
                            help_text=_("This slug is used for this account's notification URL."))
    app_id = models.CharField(_('client id'), max_length=16, help_text=_('The APP_ID given by MercadoPago.'), )
    secret_key = models.CharField(_('secret key'), max_length=32, help_text=_('The SECRET_KEY given by MercadoPago.'), )
    sandbox = models.BooleanField(_('sandbox'), default=True,
                                  help_text=_('Indicates if this account uses the sandbox mode, '
                                              'indicated for testing rather than real transactions.'), )

    def __repr__(self):
        return '<Account {}: {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name

    @property
    def service(self):
        return MercadoPagoService(self)


class Preference(models.Model):
    """
    An MP payment preference.

    Related data is send to MP and not stored locally - it's assumed
    it's part of the model that relates to this one.
    """

    owner = models.ForeignKey(Account, verbose_name='Proprietário', related_name='preferences',
                              on_delete=models.PROTECT, )
    # Doc says it's a UUID. It's not.
    mp_id = models.CharField('Id MP', max_length=46, null=True, help_text='Id atribuído pelo MP')

    payment_url = models.URLField('URL de Pagamento', )
    sandbox_url = models.URLField('URL Sandbox', )
    reference = models.CharField('Referência', max_length=128, unique=True, )
    # excluded_payment_types = models.CharField(_('excluded payment types'), default='' , max_length=128)
    paid = models.BooleanField('Pago', default=False, help_text='Indica se foi pago ou não', )

    class Meta:
        verbose_name = 'Preference'
        ordering = ('-id',)

    @property
    def url(self):
        if self.owner.sandbox:
            return self.sandbox_url
        else:
            return self.payment_url

    def update(self, title=None, price=None, quantity=None):
        """
        Updates the upstream Preference with the supplied title and price.
        """
        if price:
            self.unit_price = price
        if title:
            self.title = title
        if quantity:
            self.quantity = quantity

        service = self.owner.service
        service.update_preference(self.mp_id,
                                  {
                                      'items': [{'title': self.title,
                                                 'quantity': self.quantity,
                                                 'currency_id': 'BRL',
                                                 'unit_price': float(self.unit_price),
                                                 }
                                                ]
                                  })
        self.save()

    def submit(self, extra_fields=None, host=settings.MERCADOPAGO['base_host'], ):
        """
        Submit this preference to MercadoPago's API.

        :param dict extra_fields: Extra infromation to be sent with the
            preference creation (including payer). See the documentation[1] for
            details on avaiable fields.
        :param str host: The host to prepend to notification and return URLs.
            This should be the host for the cannonical URL where this app is
            served.

        [1]: https://www.mercadopago.com.br/developers/pt/guides/payments/web-payment-checkout/configurations
        [2]: https://www.mercadopago.com.br/developers/pt/reference/preferences/resource/
        [3]: https://www.mercadopago.com.br/developers/pt/reference/preferences/_checkout_preferences/post/
        """  # noqa: E501
        if self.mp_id:
            logger.warning('Refusing to send already-sent preference.')
            return

        extra_fields = extra_fields or {}

        # Notification is a post, should not contain #
        notification_url = (host + reverse('mp:notifications',
                                           args=(self.reference,))).replace('/#', '') + '?source_news=webhooks'
        success_url = host + reverse('mp:payment_success', args=(self.reference,), )
        failure_url = host + reverse('mp:payment_failure', args=(self.reference,), )
        pending_url = host + reverse('mp:payment_pending', args=(self.reference,), )

        request = {
            'auto_return': 'all',
            'items': [item.serialize() for item in self.items.all()],
            'external_reference': self.reference,
            'back_urls': {
                'success': success_url,
                'pending': pending_url,
                'failure': failure_url,
            },
            'notification_url': notification_url,
        }
        request.update(extra_fields)

        mercadopago_service = self.owner.service
        pref_result = mercadopago_service.create_preference(request)

        if pref_result['status'] >= 300:
            raise MercadoPagoServiceException('MercadoPago failed to create preference', pref_result)

        self.mp_id = pref_result['response']['id']
        self.payment_url = pref_result['response']['init_point']
        self.sandbox_url = pref_result['response']['sandbox_init_point']
        self.save()

    def poll_status(self):
        """
        Manually poll for the status of this preference.
        """
        url = 'https://api.mercadopago.com/v1/payments/search'

        service = self.owner.service
        access_token = service.get_access_token()  # if not self.owner.sandbox else 'TEST-3476988363526582-061923-784172ff2b561421cd20deea7d50e6df-587565780'

        response = requests.get(url, params={'access_token': access_token, 'external_reference': self.reference, }, )
        response.raise_for_status()
        response = response.json()

        if response['results']:
            logger.info('Polled for %s. Creating Payment', self.pk)
            return Payment.objects.create_or_update_from_raw_data(response['results'][-1])
        else:
            logger.info('Polled for %s. No data', self.pk)

    @classmethod
    def search(cls, filters=None, offset=0, limit=0):
        """
        Search preferences according to filters, with pagination

        @param filters
        @param offset
        @param limit
        @return json
        """

        url = 'https://api.mercadopago.com/checkout/preferences/search'

        service = Account.objects.all().first().service
        access_token = service.get_access_token()
        params = {}
        if filters:
            params.update(filters)
        params["access_token"] = access_token
        params["offset"] = offset
        params["limit"] = limit
        # params.update(filters)

        response = requests.get(url, params=params, )
        response.raise_for_status()
        response = response.json()

        return response['elements']

    def get_absolute_url(self):
        return self.url

    def _action_permission(self, link, acao):
        if acao in [ACAO_VIEW] and link.basetext == 'Procurar Pagamento':
            return not self.paid
        return True

    def __repr__(self):
        return '<Preference {}: mp_id: {}, paid: {}>'.format(self.id, self.mp_id, self.paid)

    def __str__(self):
        return self.mp_id


class Item(models.Model):
    EXPIRATION_TYPE_NONE = ' '
    EXPIRATION_TYPE_DAY = 'D'
    EXPIRATION_TYPE_MONTH = 'M'
    EXPIRATION_TYPE_PERIOD = 'P'
    EXPIRATION_TYPE_CHOICES = (
        (EXPIRATION_TYPE_NONE, 'Sem Expiração'),
        (EXPIRATION_TYPE_DAY, 'Dias'),
        (EXPIRATION_TYPE_MONTH, 'Mês(es)'),
        (EXPIRATION_TYPE_PERIOD, 'Período de Inicio/Término'),
    )

    preference = models.ForeignKey(Preference, verbose_name=_('preference'), related_name='items',
                                   on_delete=models.PROTECT, )
    title = models.CharField(_('title'), max_length=256, )
    currency_id = models.CharField(_('currency id'), default='BRL', max_length=3, )
    description = models.CharField(_('description'), max_length=256, )
    quantity = models.PositiveSmallIntegerField(default=1, )
    unit_price = models.DecimalField(max_digits=9, decimal_places=2, )
    expiration_type = models.CharField(max_length=1, blank=True, null=True, verbose_name='Tipo Expiração',
                                       default=EXPIRATION_TYPE_MONTH, choices=EXPIRATION_TYPE_CHOICES,
                                       help_text='Tipo de prazo de expiração da compra')
    expiration_length = models.PositiveIntegerField(blank=False, null=False, default=0,
                                                    verbose_name='Prazo de Expiração',
                                                    help_text='Prazo de expiração dessa compra.')

    def serialize(self):
        return {
            'category_id': 'services',
            'currency_id': self.currency_id,
            'description': self.description,
            'quantity': self.quantity,
            'title': self.title,
            'unit_price': float(self.unit_price),
        }

    def serialize_preapproval(self):
        # start_date = timezone.now().date().isoformat()
        return {
            'frequency': self.expiration_length,
            'frequency_type': 'months' if self.expiration_type == self.EXPIRATION_TYPE_MONTH else 'error',
            'currency_id': self.currency_id,
            # 'start_date': start_date,
            # 'end_date': self.description,
            'transaction_amount': float(self.unit_price),
        }

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')

    def __str__(self):
        return f'{self.title} - {self.description}'


class PaymentManager(models.Manager):

    def create_or_update_from_raw_data(self, raw_data):
        # Older endpoints will use this formats, newer one won't.
        if 'collection' in raw_data:
            raw_data = raw_data['collection']

        preference = Preference.objects.filter(reference=raw_data['external_reference'], ).first()
        if not preference:
            logger.warning("Got notification for a preference that's not ours.")
            return

        if 'date_approved' in raw_data:
            approved = raw_data['date_approved']
        else:
            approved = None

        payment_data = {
            'status': raw_data['status'],
            'status_detail': raw_data['status_detail'],
            'created': raw_data['date_created'],
            'approved': approved,
        }

        payment, created = Payment.objects.update_or_create(preference=preference, mp_id=raw_data['id'],
                                                            defaults=payment_data, )

        if payment.status == 'approved' and payment.status_detail == 'accredited':
            preference.paid = True
            preference.save()

            signals.payment_received.send(sender=Preference, payment=payment, )

        return payment


class Payment(models.Model):
    """
    A payment received, related to a preference.
    """

    mp_id = models.BigIntegerField(_('mp id'), unique=True, )

    preference = models.ForeignKey(Preference, verbose_name=_('preference'), related_name='payments',
                                   on_delete=models.PROTECT, )
    status = models.CharField(_('status'), max_length=16, )
    status_detail = models.CharField(_('status detail'), max_length=100, )

    created = models.DateTimeField(_('created'), )
    approved = models.DateTimeField(_('approved'), null=True, )

    notification = models.OneToOneField('Notification', verbose_name=_('notification'), related_name='payment',
                                        help_text=_('The notification that informed us of this payment.'),
                                        blank=True, null=True, on_delete=models.PROTECT, )

    def __repr__(self):
        return '<Payment {}: mp_id: {}>'.format(self.id, self.mp_id, )

    def __str__(self):
        return str(self.mp_id)

    objects = PaymentManager()


class Notification(models.Model):
    """
    A notification received from MercadoPago.
    """

    TOPIC_ORDER = 'o'
    TOPIC_PAYMENT = 'p'

    STATUS_PENDING = 'unp'
    STATUS_PROCESSED = 'pro'
    STATUS_IGNORED = 'ign'

    STATUS_OK = 'ok'
    STATUS_404 = '404'
    STATUS_ERROR = 'err'

    owner = models.ForeignKey(Account, verbose_name=_('owner'), related_name='notifications',
                              on_delete=models.PROTECT, )
    status = models.CharField(_('status'),
                              max_length=3,
                              choices=(
                                  (STATUS_PENDING, _('Pending')),
                                  (STATUS_PROCESSED, _('Processed')),
                                  (STATUS_IGNORED, _('Ignored')),
                                  (STATUS_OK, _('Okay')),
                                  (STATUS_404, _('Error 404')),
                                  (STATUS_ERROR, _('Error')),
                              ),
                              default=STATUS_PENDING,
                              )
    topic = models.CharField(max_length=1,
                             choices=(
                                 (TOPIC_ORDER, 'Merchant Order',),
                                 (TOPIC_PAYMENT, 'Payment',),
                             ),
                             )
    resource_id = models.CharField(_('resource_id'), max_length=46, )
    preference = models.ForeignKey(Preference, verbose_name=_('preference'), related_name='notifications',
                                   null=True, on_delete=models.PROTECT, )

    last_update = models.DateTimeField(_('last_update'), auto_now=True, )

    class Meta:
        unique_together = (('topic', 'resource_id',),)

    @property
    def processed(self):
        return self.status == Notification.STATUS_PROCESSED

    @transaction.atomic
    def process(self):
        """
        Processes the notification, and returns the generated payment, if
        applicable.
        """
        if self.topic == Notification.TOPIC_ORDER:
            logger.info("We don't process order notifications yet")
            self.status = Notification.STATUS_IGNORED
            self.save()
            return

        mercadopago_service = self.owner.service
        raw_data = mercadopago_service.get_payment_info(self.resource_id)  # Teoricamente o id não é esse
        # raw_data = mercadopago_service.get_payment_info(self.preference.mp_id) # Teoricamente o id é esse

        if raw_data['status'] != 200:
            logger.warning('Got status code %d for notification %d.', raw_data['status'], self.id)
            if raw_data['status'] == 404:
                self.status = Notification.STATUS_404
            else:
                self.status = Notification.STATUS_ERROR

            self.save()
            return

        response = raw_data['response']

        payment = Payment.objects.create_or_update_from_raw_data(response)
        if payment:
            payment.notification = self
            payment.save()

        self.status = Notification.STATUS_PROCESSED
        self.save()

        return payment

    def __repr__(self):
        return '<Notification {}: {} {}, owner: {}>'.format(self.id, self.get_topic_display(),
                                                            self.resource_id, self.owner_id, )

    def __str__(self):
        return '{} {}'.format(self.get_topic_display(), self.resource_id)


class PreApproval(Preference):
    """
    An MP preapproval.

    Related data is send to MP and not stored locally - it's assumed
    it's part of the model that relates to this one.
    """

    # owner = models.ForeignKey(Account, verbose_name='Proprietário', related_name='preapprovals',
    #                           on_delete=models.PROTECT, )
    # # Doc says it's a UUID. It's not.
    # mp_id = models.CharField('Id MP', max_length=46, null=True, help_text='Id atribuído pelo MP')
    #
    # payment_url = models.URLField('URL de Pagamento', )  # MP init_point
    # sandbox_url = models.URLField('URL Sandbox', )  # MP sandbox_init_point
    # reference = models.CharField('Referência', max_length=128, unique=True, )  # MP external_reference
    # # excluded_payment_types = models.CharField(_('excluded payment types'), default='' , max_length=128)
    # paid = models.BooleanField('Pago', default=False, help_text='Indica se foi pago ou não', )

    class Meta:
        verbose_name = 'Assinaturas'
        ordering = ('-id',)

    @property
    def url(self):
        if self.owner.sandbox:
            return self.sandbox_url
        else:
            return self.payment_url

    def update(self, title=None, price=None, quantity=None):
        """
        Updates the upstream Preference with the supplied title and price.
        """
        if price:
            self.unit_price = price
        if title:
            self.title = title
        if quantity:
            self.quantity = quantity

        service = self.owner.service
        service.update_preference(self.mp_id,
                                  {
                                      'auto_recurring': {
                                          'currency_id': 'BRL',
                                          'transaction_amount': float(self.unit_price),
                                          'frequency': self.quantity,
                                          'frequency_type': 'months',
                                      },
                                  })
        self.save()

    def submit(self, extra_fields=None, host=settings.MERCADOPAGO['base_host'], ):
        """
        Submit this preapproval to MercadoPago's API.

        :param dict extra_fields: Extra information to be sent with the
            preference creation (including payer). See the documentation[1] for
            details on available fields.
        :param str host: The host to prepend to notification and return URLs.
            This should be the host for the canonical URL where this app is
            served.

        https://www.mercadopago.com.br/developers/pt/reference/subscriptions/_preapproval/post/
        """
        if self.mp_id:
            logger.warning('Refusing to send already-sent preference.')
            return

        extra_fields = extra_fields or {}
        # payer = extra_fields['payer']

        # Notification is a post, should not contain #
        # notification_url = (host + reverse('mp:notifications', args=(self.reference,))).replace('/#','')+'?source_news=webhooks'
        # success_url = host + reverse('mp:payment_success', args=(self.reference,), )
        # failure_url = host + reverse('mp:payment_failure', args=(self.reference,), )
        # pending_url = host + reverse('mp:payment_pending', args=(self.reference,), )
        notification_url = (host + reverse('mp:notifications_preapproval', args=(self.reference,))).replace('/#', '')

        """
          "auto_recurring": {
            "currency_id": "ARS",
            "transaction_amount": 10,
            "frequency": 1,
            "frequency_type": "months",
            "end_date": "2022-07-20T11:59:52.581-04:00",           
          },
          "back_url": "https://www.mercadopago.com.ar",
          "collector_id": 555435388,
          "external_reference": "1245AT234562",
          "payer_email": "test_user@testuser.com",
          "reason": "Suscripción particular",
          "status": "pending"
        """
        request = {
            'auto_recurring': self.items.first().serialize_preapproval(),
            # 'auto_return': 'all',
            'back_url': notification_url,
            # "collector_id": 555435388,
            'external_reference': self.reference,
            # 'payer_email': payer['email'], => Está no extra_fields
            # 'reason': self.title,
            "status": "pending"
        }
        request.update(extra_fields)

        mercadopago_service = self.owner.service
        pref_result = mercadopago_service.create_preapproval_payment(request)

        if pref_result['status'] >= 300:
            raise MercadoPagoServiceException('MercadoPago failed to create preapproval preference', pref_result)

        self.mp_id = pref_result['response']['id']
        self.payment_url = pref_result['response']['init_point']
        self.sandbox_url = pref_result['response']['sandbox_init_point']
        self.save()

    def poll_status(self):
        """
        Manually poll for the status of this preference.
        """
        url = 'https://api.mercadopago.com/v1/payments/search'

        service = self.owner.service
        access_token = service.get_access_token()  # if not self.owner.sandbox else 'TEST-3476988363526582-061923-784172ff2b561421cd20deea7d50e6df-587565780'

        response = requests.get(url, params={'access_token': access_token, 'external_reference': self.reference, }, )
        response.raise_for_status()
        response = response.json()

        if response['results']:
            logger.info('Polled for %s. Creating Payment', self.pk)
            return Payment.objects.create_or_update_from_raw_data(response['results'][-1])
        else:
            logger.info('Polled for %s. No data', self.pk)

    @classmethod
    def search(cls, filters=None, offset=0, limit=0):
        """
        Search preferences according to filters, with pagination

        @param filters
        @param offset
        @param limit
        @return json
        """

        url = 'https://api.mercadopago.com/checkout/preferences/search'

        service = Account.objects.all().first().service
        access_token = service.get_access_token()
        params = {}
        if filters:
            params.update(filters)
        params["access_token"] = access_token
        params["offset"] = offset
        params["limit"] = limit
        # params.update(filters)

        response = requests.get(url, params=params, )
        response.raise_for_status()
        response = response.json()

        return response['elements']

    def get_absolute_url(self):
        return self.url

    def _action_permission(self, link, acao):
        if acao in [ACAO_VIEW] and link.basetext == 'Procurar Pagamento':
            return not self.paid
        return True

    def __repr__(self):
        return '<Preference {}: mp_id: {}, paid: {}>'.format(self.id, self.mp_id, self.paid)

    def __str__(self):
        return self.mp_id
