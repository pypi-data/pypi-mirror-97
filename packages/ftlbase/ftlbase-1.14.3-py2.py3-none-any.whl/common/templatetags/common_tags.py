#!/usr/bin/env python
# coding: utf-8
import logging
import re
from decimal import Decimal

import readtime
from django import template
from django.apps import apps

logger = logging.getLogger(__name__)
register = template.Library()


class CommonMenuMensagens(template.Node):
    template_name = "menu_mensagens.html"

    # def __init__(self, usuario):
    #     self.usuario = template.Variable(usuario)

    def render(self, context):
        t = template.loader.get_template(self.template_name)
        # atendimentos = Atendimento.get_atendimentos_novos()
        # return t.render({'atendimentos': atendimentos})
        menu_mensagens = {}
        return t.render({'menu_mensagens': menu_mensagens})


@register.tag
def common_menu_mensagens(parser, token):
    return CommonMenuMensagens()


USER_AGENT_REGEX = re.compile(
    r'randroid|avantgo|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|'
    r'ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|opera m(ob|in)i|palm( os)?|'
    r'phone|p(ixi|re)\\/|plucker|pocket|psp|symbian|treo|up\\.(browser|link)|'
    r'vodafone|wap|indows (ce|phone)|xda|xiino', re.M)


@register.filter()
def is_mobile(request):
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    if USER_AGENT_REGEX.search(ua):
        return True
    return False


def read(html):
    """
    Calcula o tempo de leitura de um texto em html.
    Pode ser usado no template {{post.body|readtime}}
    """
    r = readtime.of_html(html)
    return '{} minuto'.format(r.minutes) + ('s' if r.minutes > 1 else '')


register.filter('readtime', read)


def valid_numeric(arg):
    if isinstance(arg, (int, float, Decimal)):
        return arg
    try:
        return int(arg)
    except ValueError:
        return float(arg)


def handle_float_decimal_combinations(value, arg, operation):
    if isinstance(value, float) and isinstance(arg, Decimal):
        logger.warning('Unsafe operation: {0!r} {1} {2!r}.'.format(value, operation, arg))
        value = Decimal(str(value))
    if isinstance(value, Decimal) and isinstance(arg, float):
        logger.warning('Unsafe operation: {0!r} {1} {2!r}.'.format(value, operation, arg))
        arg = Decimal(str(arg))
    return value, arg


@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        nvalue, narg = handle_float_decimal_combinations(valid_numeric(value), valid_numeric(arg), '-')
        return nvalue - narg
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ''


@register.filter
def mul(value, arg):
    """Multiply the arg with the value."""
    try:
        nvalue, narg = handle_float_decimal_combinations(valid_numeric(value), valid_numeric(arg), '*')
        return nvalue * narg
    except (ValueError, TypeError):
        try:
            return value * arg
        except Exception:
            return ''


@register.filter
def div(value, arg):
    """Divide the arg by the value."""
    try:
        nvalue, narg = handle_float_decimal_combinations(valid_numeric(value), valid_numeric(arg), '/')
        return nvalue / narg
    except (ValueError, TypeError):
        try:
            return value / arg
        except Exception:
            return ''


@register.filter
def intdiv(value, arg):
    """Divide the arg by the value. Use integer (floor) division."""
    try:
        nvalue, narg = handle_float_decimal_combinations(valid_numeric(value), valid_numeric(arg), '//')
        return nvalue // narg
    except (ValueError, TypeError):
        try:
            return value // arg
        except Exception:
            return ''


@register.filter
def moneydiv(value, arg):
    """Divide the arg by the value and round to 2 decimal places."""
    try:
        nvalue, narg = handle_float_decimal_combinations(valid_numeric(value), valid_numeric(arg), '/')
        return round(nvalue / narg, 2)
    except (ValueError, TypeError):
        try:
            return value / arg
        except Exception:
            return ''


@register.filter(name='abs')
def absolute(value):
    """Return the absolute value."""
    try:
        return abs(valid_numeric(value))
    except (ValueError, TypeError):
        try:
            return abs(value)
        except Exception:
            return ''


@register.filter
def mod(value, arg):
    """Return the modulo value."""
    try:
        nvalue, narg = handle_float_decimal_combinations(valid_numeric(value), valid_numeric(arg), '%')
        return nvalue % narg
    except (ValueError, TypeError):
        try:
            return value % arg
        except Exception:
            return ''


@register.filter(name='addition')
def addition(value, arg):
    """Float-friendly replacement for Django's built-in `add` filter."""
    try:
        nvalue, narg = handle_float_decimal_combinations(valid_numeric(value), valid_numeric(arg), '+')
        return nvalue + narg
    except (ValueError, TypeError):
        try:
            return value + arg
        except Exception:
            return ''


@register.simple_tag
def model_count(app, model):
    """
    Retorna empresa.apelido
    """
    cls = apps.get_model(app, model)
    return cls.objects.all().count()


@register.simple_tag
def define(val=None):
    """ Define uma variável no template e pode ser usada assim:
    {% if item %}
       {% define "Edit" as action %}
    {% else %}
       {% define "Create" as action %}
    {% endif %}
    Would you like to {{action}} this item?
    """
    return val
