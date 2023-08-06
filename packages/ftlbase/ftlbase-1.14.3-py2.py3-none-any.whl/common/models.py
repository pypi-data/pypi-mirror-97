# -*- coding: utf-8 -*-

# Constantes do módulo
from html import unescape

from django.conf import settings
from django.core import validators
from django.db import models
from django.db.models import Model, DecimalField, CharField
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel
from polymorphic.models import PolymorphicModel
from reversion_compare.mixins import CompareMethodsMixin, CompareMixin

from common.fields import MoneyFormField, SimNaoFormField, PercentFormField
from common.utils import ACAO_EDIT

ESTADOCIVIL_C = (('C', 'Casado'), ('S', 'Solteiro'), ('D', 'Divorciado'), ('', 'União Civil'))
SEXO_C = (('F', 'Feminino'), ('M', 'Masculino'))
ATIVO_C = (('S', 'Ativo'), ('I', 'Inativo'))
SIM_NAO_C = (('S', 'Sim'), ('N', 'Não'))
TIPO_DIAS_C = (('F', 'Dia Fixo'), ('C', 'Dias Corridos'), ('U', 'Dias Úteis'))


class AutoCreatedAtField(models.DateTimeField):
    """ Campo de data e hora automáticos. Para campos modified_at """

    def __init__(self, *args, **kwargs):
        # kwargs.setdefault('editable', False)
        kwargs.setdefault('default', timezone.now)
        super().__init__(*args, **kwargs)


class AutoModifiedAtField(AutoCreatedAtField):
    """ Campo de data e hora automáticos. Para campos modified_at """

    def pre_save(self, model_instance, add):
        value = timezone.now()
        if not model_instance.pk:
            for field in model_instance._meta.get_fields():
                if isinstance(field, AutoCreatedAtField) and getattr(model_instance, field.name):
                    value = getattr(model_instance, field.name)
                    break
        setattr(model_instance, self.attname, value)
        return value


class CommonAbsoluteUrlMixin(object):
    @classmethod
    def get_cancel_url(self):
        try:
            cls_name = self._meta.model_name
            url = reverse(cls_name)
        except Exception as e:
            url = reverse('index')
        return url

    def get_absolute_url(self):
        try:
            cls_name = self._meta.model.__name__
            cls_name = cls_name[0].lower() + cls_name[1:]
            url = reverse("{}EditDelete".format(cls_name), args=(self.pk, ACAO_EDIT))
        except Exception as e:
            try:
                cls_name = self._meta.model.__name__
                cls_name = cls_name[0].lower() + cls_name[1:]
                url = reverse("{}".format(cls_name), args=(self.pk, ACAO_EDIT))
            except Exception as e:
                url = reverse('index')
        return url


class CommonModel(CommonAbsoluteUrlMixin, Model):
    """
    Usado para auditar usuário e datas de criação e modificação
    """
    # Log
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='%(app_label)s_%(class)s_created_by', verbose_name='Cadastrado Por')
    created_at = AutoCreatedAtField(verbose_name='Data de Criação', blank=True, null=True)

    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,
                                    related_name='%(app_label)s_%(class)s_modified_by', verbose_name='Modificado Por')
    modified_at = AutoModifiedAtField(verbose_name='Última Modificação', default=timezone.now, blank=True, null=True)

    class Meta:
        verbose_name = 'Auditoria de Usuário'
        verbose_name_plural = 'Auditoria de Usuários'
        abstract = True

    def __str__(self):
        return 'Criado por {} em {}, modificado por {} em {}'.format(self.created_by, self.created_at,
                                                                     self.modified_by, self.modified_at)


class CommonMPTTModel(MPTTModel, CommonModel):
    """ Common class for tree models. """

    class Meta:
        verbose_name = 'Common MPTT Model'
        verbose_name_plural = 'Common MPTT Models'
        abstract = True


class Configuracao(PolymorphicModel, CommonModel):
    """
    Configuração
    """
    apelido = models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name='Apelido', default='')
    # Status
    ativo = models.CharField(max_length=1, null=True, blank=True, verbose_name='Status', default='S',
                             choices=ATIVO_C)

    class Meta:
        verbose_name = 'Configuracao'
        verbose_name_plural = 'Configurações'
        ordering = ('apelido',)
        # abstract = True
        # managed = False

    def __str__(self):
        return u'%s' % self.apelido


class ValorField(DecimalField):

    def __init__(self, verbose_name=None, name=None, **kwargs):
        _max_digits = kwargs.pop('max_digits', 15)
        _decimal_places = kwargs.pop('decimal_places', 2)
        _blank = kwargs.pop('blank', False)
        _null = kwargs.pop('null', False)
        _default = kwargs.pop('default', 0)
        _validators = kwargs.pop('validators', [validators.MinValueValidator(0)])
        super().__init__(verbose_name=verbose_name, name=name, max_digits=_max_digits, decimal_places=_decimal_places,
                         blank=_blank, null=_null, default=_default, validators=_validators, **kwargs)

    def formfield(self, **kwargs):
        # Devolver o form field default desse tipo de campo
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': MoneyFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class PercentField(DecimalField):

    def __init__(self, verbose_name=None, name=None, **kwargs):
        _max_digits = kwargs.pop('max_digits', 6)
        _decimal_places = kwargs.pop('decimal_places', 2)
        _blank = kwargs.pop('blank', False)
        _null = kwargs.pop('null', False)
        _default = kwargs.pop('default', 0)
        _validators = kwargs.pop('validators', [validators.MinValueValidator(0), validators.MaxValueValidator(100)])
        super().__init__(verbose_name=verbose_name, name=name, max_digits=_max_digits, decimal_places=_decimal_places,
                         blank=_blank, null=_null, default=_default, validators=_validators, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': PercentFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Rota(CommonAbsoluteUrlMixin, Model):
    """
    Rotas do sistema
    """
    modulo = models.CharField(max_length=50, null=False, blank=False, verbose_name='Módulo', default='')
    rota = models.CharField(max_length=50, null=False, blank=False, unique=True, verbose_name='Rota', default='')
    nome = models.CharField(max_length=200, null=False, blank=False, verbose_name='Nome', default='')
    reload = models.BooleanField(verbose_name='Reload', default=True)

    class Meta:
        verbose_name = 'Rota do Sistema'
        verbose_name_plural = 'Rotas do Sistema'
        ordering = ('pk',)

    def __str__(self):
        return f'{self.pk} - {self.rota} - {self.nome}'

    @property
    def url(self):
        try:
            return reverse(self.rota)
        except:
            return 'Erro'

    @classmethod
    def inicializa_rotas(cls, rotas):
        """ Rotina para criar todas as rotas de apps, insere em Rota se não existir, roda em ready de apps """
        for i in rotas:
            try:
                r = Rota.objects.filter(modulo=i['modulo'], rota=i['rota']).first()
                if r:
                    r.nome = i['nome']
                    r.reload = i['reload']
                    r.save()
                else:
                    r = Rota(modulo=i['modulo'], rota=i['rota'], nome=i['nome'], reload=i['reload'])
                    r.save()
            except Exception as e:
                pass


class SimNaoField(CharField):
    """ Field char com checkbox, mas conteúdo S/N no banco de dados """

    def __init__(self, *args, **kwargs):
        default = kwargs.pop('default', 'N')
        super().__init__(*args, default=default, **kwargs)

    def formfield(self, **kwargs):
        # Devolver o widget default desse tipo de campo
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': SimNaoFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class CompareVersion(CompareMethodsMixin, CompareMixin):
    def __init__(self, *args, **kwargs):
        self.compare_exclude = kwargs.pop('compare_exclude', None)
        super().__init__(*args, **kwargs)

    def compare(self, obj, version1, version2):
        diff, has_unfollowed_fields = super().compare(obj, version1, version2)
        for i in diff:
            i['diff'] = mark_safe(unescape(i['diff']))
        return diff, has_unfollowed_fields
