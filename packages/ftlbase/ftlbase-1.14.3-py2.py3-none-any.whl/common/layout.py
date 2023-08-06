# -*- coding: utf-8 -*-
from crispy_forms.layout import LayoutObject, HTML, Layout, Div, Field, Row
from crispy_forms.utils import TEMPLATE_PACK
from django.core.exceptions import ImproperlyConfigured
from django.template import Template
from django.template.loader import get_template
from django.utils.html import conditional_escape
# layout de endereço padrão para a aplicação
from django.utils.safestring import mark_safe
from reversion.models import Version

from common.forms import VersionTable
from common.middleware import get_current_request
from common.utils import get_url_from_parms

glyphicon_calendar = '<span class=\"glyphicon glyphicon-calendar\"></span>'
glyphicon_up_and_down = """<div><span class="glyphicon glyphicon-arrow-up" onclick="formset_up(this);"></span>
<span class="glyphicon glyphicon-arrow-down" onclick="formset_down(this);"></span></div>"""


def format_progress_bar(actual, total):
    s = """<div class="progress">
      <div class="progress-bar" role="progressbar" aria-valuenow="{percentual:.0f}" aria-valuemin="0" aria-valuemax="100" style="min-width: 2em;width: {percentual:.0f}%;">
        {percentual:.0f}%
      </div>
    </div>"""
    if total and total > 0:
        # Caso onde o notebook não tem documento, mas como default o valor de time é 1
        if total == 1 and actual == 1:
            actual = 0
        percentual = 100 * actual / total
    else:
        percentual = 0

    s = s.format(percentual=percentual, actual=actual)
    return s


def Label(label, first=False):
    """
        LabelFirstDetail: Usado nos forms estilo master/detail para colocar título do campo do detail
        somente no primeiro registro dos detalhes
        Não sei porque cargas d'água isso não funciona quando está em REST, só quando está direto.
        Exemplo: os Municípios do Estado não funcionam direito.
        Marretada: passando um array xpto [1,2], forçar um for para a first ficar false e só gerar o detail template
        no segundo item do array.
        Horrível.
    """
    return HTML("%s%s%s" % (
        "<label class=\"control-label " + ("ftl-inlines-first-only" if first else "") + "\">", label, "</label>"))


def LabelFirstDetail(label):
    """
        LabelFirstDetail: Usado nos forms estilo master/detail para colocar título do campo do detail
        somente no primeiro registro dos detalhes
        Não sei porque cargas d'água is
        so não funciona quando está em REST, só quando está direto.
        Exemplo: os Municípios do Estado não funcionam direito.
        Marretada: passando um array xpto [1,2], forçar um for para a first ficar false e só gerar o detail template
        no segundo item do array.
        Horrível.
    """
    return HTML(
        "%s%s%s" % ("<label class=\"{% if not forloop.first %}sr-only {% endif %}control-label\">", label, "</label>"))


class HTMLField(Field):
    """
    Usado para mostrar um field html de forma segura, usando safe no template

    """
    template = "common/html-safe.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        if extra_context is None:
            extra_context = {}
        if hasattr(self, 'wrapper_class'):
            extra_context['wrapper_class'] = self.wrapper_class

        css_classes = self.attrs.get('class', None)

        template = get_template(self.get_template_name(template_pack))

        html = mark_safe('')
        for f in self.fields:
            txt = mark_safe(getattr(form.instance, f))
            if context.get('ajax', False):
                txt = txt.replace('href="/', 'href="#/')
            context.update({'field': mark_safe(txt), 'css_classes': css_classes})
            context = context.flatten()
            html += template.render(context)

        return html


class DateField(Field):
    def __init__(self, *args, **kwargs):
        kwargs['data-ftl'] = 'data'
        super().__init__(*args, **kwargs)


class DatetimeField(Field):
    template = "common/datetime_common.html"


class PercentField(Field):
    template = "common/percent.html"


class DeleteField(Field):
    """ Campo de Delete sem o "Remover" no checkbox """
    template = "common/delete_field.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        request = get_current_request()
        try:
            context['acao'] = request.resolver_match.kwargs['acao']
        except Exception as e:
            pass
        return super().render(form, form_style, context, template_pack, extra_context, **kwargs)


class ButtonLink(LayoutObject):
    """Custom bootstrap layout object to create a button link.
    Example::

        ButtonLink(field='previous', href='contentRead',
                   parms={'pk':'form.instance.previous.pk', 'acao':2, 'document': 'form.instance.document_id'})
        :param parms: é um dict com o valor do parâmetro na URL e o valor que será passado em função do instance do form
                      Se um dos parâmetros der erro no eval, retorna string vazia
    """
    template = """<a role="button" class="{css_class}" href="{href}" style="{style}">{appended_text} {label} {prepended_text}</a>"""
    css_class_default = 'btn btn-default'

    def __init__(self, field, named_url, *args, **kwargs):
        self.field = field
        self.named_url = named_url
        self.css_class = kwargs.pop('css_class', self.css_class_default)
        self.parms = kwargs.pop('parms', None)  # Parâmetros para compor o reverse
        self.appended_text = kwargs.pop('appended_text', '')
        self.prepended_text = kwargs.pop('prepended_text', '')
        style = kwargs.pop('style', '')
        if style:
            style = 'style="{}"'.format(style)
        self.style = style

    def render(self, form, form_style, context, template_pack):
        instance = getattr(form, 'instance', None)
        href = get_url_from_parms(instance, self.named_url, self.parms)
        if href:
            href = ('#' if context['ajax'] else '') + href
            layout_object = HTML(self.template.format(css_class=self.css_class, href=href, label=form[self.field].label,
                                                      style=self.style, appended_text=self.appended_text,
                                                      prepended_text=self.prepended_text))
            return layout_object.render(form, form_style, context, template_pack)
        else:
            return href


class Link(ButtonLink):
    """Custom bootstrap layout object to create a link.
    Example::

        Link(field='previous', href='contentRead',
             parms={'pk':'instance.previous.pk', 'acao':2, 'document': 'instance.document_id'})
        :param parms: é um dict com o valor do parâmetro na URL e o valor que será passado em função do instance do form
                      Se um dos parâmetros der erro no eval, retorna string vazia
    """
    # template = """<a class="{0}" href="{1}">{2}</a>"""
    css_class_default = 'label label-primary'


class AlertLink(ButtonLink):
    """Custom bootstrap layout object to create a link.
    Example::

        Link(field='previous', href='contentRead',
             parms={'pk':'instance.previous.pk', 'acao':2, 'document': 'instance.document_id'})
        :param parms: é um dict com o valor do parâmetro na URL e o valor que será passado em função do instance do form
                      Se um dos parâmetros der erro no eval, retorna string vazia
    """
    template = """<a role="button" href="{href}">{appended_text} {label} {prepended_text}</a>"""
    template_div = """<div class="{alert} {css_class} vertical-align" {style}>{content}</div>"""
    css_class_default = ''

    def __init__(self, field, named_url, *args, **kwargs):
        self.alert = kwargs.pop('alert', 'success')
        super().__init__(field, named_url, *args, **kwargs)

    def render(self, form, form_style, context, template_pack):
        instance = getattr(form, 'instance', None)
        alert = ''
        if callable(self.alert):
            if instance:
                alert = self.alert(instance)
        else:
            alert = self.alert
        if alert:
            alert = 'alert-ftl alert-ftl-{alert}'.format(alert=alert)
        else:
            alert = 'alert-ftl'

        href = get_url_from_parms(instance, self.named_url, self.parms)
        if href:
            href = ('#' if context['ajax'] else '') + href
            content = self.template.format(css_class=self.css_class, href=href, label=form[self.field].label,
                                           style=self.style, alert=alert,
                                           appended_text=self.appended_text, prepended_text=self.prepended_text)
        else:
            content = ''

        html = self.template_div.format(css_class=self.css_class, href=href, label=form[self.field].label,
                                        style=self.style, alert=alert, content=content,
                                        appended_text=self.appended_text, prepended_text=self.prepended_text, )
        layout_object = HTML(html)
        return layout_object.render(form, form_style, context, template_pack)


class HTMLInstance(HTML):
    """ Igual ao HTML do Crispy, porém usa eval para pegar dados da instance atual """

    # HTMLInstance('{html}', parms={'html': 'instance.get_read_display()'}),

    def __init__(self, html, parms):
        super().__init__(html)
        self.params = parms or {}
        if len(self.params) == 0:
            raise ImproperlyConfigured('Quantidade de parâmetros deve ser maior que um ou então use HTML()')

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        instance = getattr(form, 'instance', None)  # NOQA Porque pode ser usado no eval do parametro
        params = {}
        for key, val in self.params.items():
            if callable(val):
                if instance:
                    html = val(instance)
                else:
                    html = 'ERROR'
            else:
                html = eval(val)
            params.update({key: html})
        if hasattr(self.html, 'render'):
            html = self.html.render(form, form_style, context, **kwargs)
        else:
            html = self.html
        html = html.format(**params)
        return Template(str(html)).render(context)


class PRE(object):
    """ Formata um campo com <PRE> """

    def __init__(self, field):
        self.field_name = field
        if not field:
            raise ImproperlyConfigured('Campo não informado.')

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        instance = getattr(form, 'instance', None)  # NOQA Porque pode ser usado no eval do parametro

        txt = mark_safe(getattr(instance, self.field_name, None))
        if txt:
            html = f'<pre>{txt}</pre>'
        else:
            html = ''
        return Template(str(html)).render(context)


def Tree(idTree="masterTreeManager", idModal="ftl-form-modal"):
    """
        Tree: Usado para identificar onde a Tree (plano de contas, conteúdo de documentos, etc.) ficará.
    """
    return HTML('<div id="{0}"></div><div id="{1}"></div>'.format(idTree, idModal))


class M2MSetField(LayoutObject):
    """
    Usado para listar num formato table relações M2M, como por exemplo listar o conjunto de contratos de administração
    ou de locação de um imóvel.

    Pode ser usado também para FK, sem necessidade de passar o parâmetro m2m

    Layout object: It contains one field name, and you can add attributes to it easily.
    For setting class attributes, you need to use `css_class`, as `class` is a Python keyword.

    """
    template = "table-widget.html"

    def __init__(self, *args, **kwargs):
        self.fields = list(args)

        if not hasattr(self, 'attrs'):
            self.attrs = {}

        if 'css_class' in kwargs:
            if 'class' in self.attrs:
                self.attrs['class'] += " %s" % kwargs.pop('css_class')
            else:
                self.attrs['class'] = kwargs.pop('css_class')

        self.wrapper_class = kwargs.pop('wrapper_class', None)
        self.template = kwargs.pop('template', self.template)
        self.table_form = kwargs.pop('table_form', None)  # ContratoAdmImovelTable / ContratoLocImovelTable
        self.m2m = kwargs.pop('m2m', None)  # imoveis

        # We use kwargs as HTML attributes, turning data_id='test' into data-id='test'
        self.attrs.update(dict([(k.replace('_', '-'), conditional_escape(v)) for k, v in kwargs.items()]))

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        if extra_context is None:
            extra_context = {}
        if hasattr(self, 'wrapper_class'):
            extra_context['wrapper_class'] = self.wrapper_class

        template = get_template(self.get_template_name(template_pack))

        if form.instance.pk is not None:
            queryset = getattr(form.instance, self.fields[0]).all()
            if len(self.table_form.opts.sort) > 0:
                ordem = [(('-' if des == 'desc' else '') + self.table_form.base_columns[i].field) for (i, des) in
                         self.table_form.opts.sort]
                queryset = queryset.order_by(*ordem)
        else:
            queryset = form.instance._meta.model.objects.none()

        # request = context['request']

        objetos = self.table_form(queryset)
        context.update({'objetos': objetos})
        # ctx = {k: v for d in context for k, v in d.items() if d}
        ctx = context.flatten()

        html = template.render(ctx)

        return html


class VersionField(LayoutObject):
    """
    Usado para listar num formato table as versões de um model que esteja usando django-reversion.
    """

    def __init__(self, *args, **kwargs):
        self.fields = list(args)

        if not hasattr(self, 'attrs'):
            self.attrs = {}

        if 'css_class' in kwargs:
            if 'class' in self.attrs:
                self.attrs['class'] += " %s" % kwargs.pop('css_class')
            else:
                self.attrs['class'] = kwargs.pop('css_class')

        self.wrapper_class = kwargs.pop('wrapper_class', None)
        self.template = kwargs.pop('template', "table-widget.html")
        self.table_form = kwargs.pop('table_form', VersionTable)

        # We use kwargs as HTML attributes, turning data_id='test' into data-id='test'
        self.attrs.update(dict([(k.replace('_', '-'), conditional_escape(v)) for k, v in kwargs.items()]))

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        if extra_context is None:
            extra_context = {}
        if hasattr(self, 'wrapper_class'):
            extra_context['wrapper_class'] = self.wrapper_class

        template = get_template(self.get_template_name(template_pack))

        if form.instance.pk is not None:
            queryset = Version.objects.get_for_object(
                form.instance)  # .values('pk', 'revision__date_created', 'revision__user__username')
        else:
            queryset = Version.objects.none()

        objetos = self.table_form(queryset)
        context.update({'objetos': objetos})
        ctx = context.flatten()

        html = template.render(ctx)

        return html


class ReadonlyField(Field):
    """
    Layout object for rendering fields as uneditable in bootstrap.
    :param inline: remove label from field render. Default is False.
    :type bool

    """
    template = "common/readonly_input.html"

    def __init__(self, field, *args, inline=False, **kwargs):
        self.attrs = {'class': 'readonly-input'}
        self.inline = inline
        super(ReadonlyField, self).__init__(field, *args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super(ReadonlyField, self).render(form, form_style, context, template_pack=template_pack,
                                                 extra_context={'inline': self.inline, })


def simple_line_message(msg):
    """
    Linha de mensagem simples, apenas html, com espaços antes e depois da mensagem.
    Usada em use case para confirmar execução do processo.
    """
    return Layout(
        Div(Div(HTML('<br>'), css_class='col-xs-12'), css_class='row'),
        Div(Div(HTML(msg), css_class='col-xs-12'), css_class='row'),
        Div(Div(HTML('<br>'), css_class='col-xs-12'), css_class='row'),
    )


def simple_label_line(msg, *args, **kwargs):
    """ Insere uma linha de divisão com um texto no centralizado """
    border_color = kwargs.get('border_color', None)
    style_line = 'border-color:{};'.format(border_color) if border_color else None

    max_width = kwargs.get('max_width', None)
    style = 'max-width:{}px;'.format(max_width) if max_width else None

    return Layout(
        HTML('<p>&nbsp;</p>'),
        Div(css_class='line-div', style=style_line),
        Div(HTML(msg), css_class='line-label', style=style, )
    )


# Layout padrão de endereço
layout_endereco = Layout(
    Div(
        Row(
            Div(Field('cep', data_ftl="cep"), css_class='col-md-3'),
            Div(css_class='col-md-8'),
        ),
        Row(
            Div('endereco', css_class='col-md-8'),
            Div(css_class='col-md-1'),
            Div('enderecoNumero', css_class='col-md-2'),
        ),
        Row(
            Div('complemento', css_class='col-md-11'),
        ),
        Row(
            Div('bairro', 'estado', css_class='col-md-5'),
            Div(css_class='col-md-1'),
            Div('municipio', css_class='col-md-5'),
        ),
    ),
)

# Layout padrão de log de usuário para a aplicação
layout_logusuario = Layout(
    simple_label_line('Log', max_width=55),
    Div(
        Div(ReadonlyField('created_by'), css_class='col-xs-6 col-md-2'),
        Div(DatetimeField('created_at', disabled=True), css_class='col-xs-6 col-md-offset-1 col-md-2'),
        Div(ReadonlyField('modified_by'), css_class='col-xs-6 col-md-offset-1 col-md-2'),
        Div(DatetimeField('modified_at', disabled=True), css_class='col-xs-6 col-md-offset-1 col-md-2'),  # nowrap
        css_class='row',
    ),
)
