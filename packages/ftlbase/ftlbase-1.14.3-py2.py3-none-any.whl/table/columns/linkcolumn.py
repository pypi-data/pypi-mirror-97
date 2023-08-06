#!/usr/bin/env python
# coding: utf-8
from django.template import Template, Context
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from common.middleware import get_current_request
from table.columns.base import Column
from table.utils import Accessor

ACAO_ADD = '1'
ACAO_EDIT = '2'
ACAO_DELETE = '3'
ACAO_VIEW = '4'
ACAO_REPORT = '5'

# Retorna a execução da função se é callable ou a própria variável se não é
iscallable = lambda x, *args, **kw: x(*args, **kw) if callable(x) else x


class LinkColumn(Column):
    def __init__(self, header=None, links=None, delimiter='&nbsp', field=None, **kwargs):
        self.links = links
        self.delimiter = delimiter
        kwargs['safe'] = False
        super(LinkColumn, self).__init__(field, header, **kwargs)

    def render(self, obj):
        return self.delimiter.join([link.render(obj) for link in self.links])


class Link(object):
    """
    Represents a html <a> tag.
    """

    def __init__(self, text=None, viewname=None, args=None, kwargs=None, urlconf=None,
                 current_app=None, attrs=None, permission=None, acao=None, ajax=True, new_window=False):
        self.basetext = text
        self.viewname = viewname
        self.args = args or []
        self.kwargs = kwargs or {}
        self.urlconf = urlconf
        self.current_app = current_app
        self.base_attrs = attrs or {}
        self.permission = permission
        self.acao = acao
        self.ajax = ajax
        self.new_window = new_window
        self.obj = None

    @property
    def text(self):
        if isinstance(self.basetext, Accessor):
            basetext = self.basetext.resolve(self.obj)
        else:
            basetext = self.basetext
        return escape(basetext)

    @property
    def url(self):
        if self.viewname is None:
            return ""

        # The following params + if statements create optional arguments to
        # pass to Django's reverse() function.
        params = {}
        if self.args:
            params['args'] = [arg.resolve(self.obj)
                              if isinstance(arg, Accessor) else arg
                              for arg in self.args]
        if self.kwargs:
            params['kwargs'] = {}
            for key, value in self.kwargs.items():
                params['kwargs'][key] = (value.resolve(self.obj)
                                         if isinstance(value, Accessor) else value)
        if self.urlconf:
            params['urlconf'] = (self.urlconf.resolve(self.obj)
                                 if isinstance(self.urlconf, Accessor)
                                 else self.urlconf)
        if self.current_app:
            params['current_app'] = (self.current_app.resolve(self.obj)
                                     if isinstance(self.current_app, Accessor)
                                     else self.current_app)

        return reverse(self.viewname, **params)

    @property
    def attrs(self):
        if self.url:
            self.base_attrs["href"] = self.url
        return self.base_attrs

    def render(self, obj):
        """ Render link as HTML output tag <a>.
        """
        from common.utils import has_permission

        try:
            self.obj = obj
            base = '%s="#%s"' if self.ajax else '%s="%s"'
            attrs = ' '.join([
                base % (attr_name, attr.resolve(obj)) if isinstance(attr, Accessor) \
                    else base % (attr_name, attr) for attr_name, attr in self.attrs.items()
            ])
            if self.permission or self.acao:
                if not has_permission(get_current_request(), self.obj.__class__, self.acao, permissions=self.permission,
                                      instance=obj, raise_exception=False):
                    return mark_safe('')  # se não tem permissão então não gera o link
            new_window = 'target="_blank"' if self.new_window else ''
            return mark_safe('<a {0} {1}>{2}</a>'.format(attrs, new_window, self.text))
        except Exception as e:
            return mark_safe('')


class ImageLink(Link):
    """
    Represents a html <a> tag that contains <img>.
    """

    def __init__(self, image, image_title, *args, **kwargs):
        self.image_path = image
        self.image_title = image_title
        super(ImageLink, self).__init__(*args, **kwargs)

    @property
    def image(self):
        path = self.image_path
        if isinstance(self.image_title, Accessor):
            title = self.image_title.resolve(self.obj)
        else:
            title = self.image_title
        template = Template('{%% load static %%}<img src="{%% static "%s" %%}"'
                            ' title="%s">' % (path, title))
        return template.render(Context())

    @property
    def text(self):
        return self.image


class Span(Link):
    """ Represents a html <span> tag. """
    template = '<span {css_class} {style} {tip} {aria_hidden}>{span_text}</span>'
    span_text = ''
    span_tip = None
    span_size = None
    span_color = None
    aria_hidden = False
    css_class = None

    def __init__(self, *args, **kwargs):
        self.css_class = kwargs.pop('css_class', self.css_class)
        self.span_size = kwargs.pop('span_size', self.span_size)
        self.span_color = kwargs.pop('span_color', self.span_color)
        self.span_tip = kwargs.pop('span_tip', self.span_tip)
        self.aria_hidden = kwargs.pop('aria_hidden', self.aria_hidden)
        self.span_text = kwargs.pop('span_text', self.span_text)
        super().__init__(*args, **kwargs)

    @property
    def text(self):
        css_class = 'class="{}"'.format(iscallable(self.css_class, self)) if self.css_class else ''
        span_size = 'font-size:{}px;'.format(iscallable(self.span_size, self)) if self.span_size else ''
        span_color = 'color:{};'.format(iscallable(self.span_color, self)) if self.span_color else ''
        style = 'style="{0}{1}"'.format(span_size, span_color) if self.span_size or self.span_color else ''
        tip = 'data-toggle="tooltip" data-container="body" title="{}"'.format(self.span_tip) if self.span_tip else ''
        aria_hidden = 'aria-hidden="true"' if self.aria_hidden else ''
        template = Template(self.template.format(css_class=css_class, style=style, tip=tip, aria_hidden=aria_hidden,
                                                 span_text=self.span_text))
        return template.render(Context())


class GlyphiconSpanLink(Span):
    """ Represents a html <a> tag that contains <span> of Glyphicon. """
    css_class = 'glyphicon glyphicon-{glyph}'

    def __init__(self, *args, **kwargs):
        css_class = kwargs.pop('css_class', self.css_class).format(glyph=kwargs.pop('span_glyph', None))
        kw = kwargs.copy()
        kw.update({'css_class': css_class})
        super().__init__(*args, **kw)


class FontAwesomeLink(Span):
    """ Represents a html <a> tag that contains <span> of FontAwesome. """
    span_color = '#09568d'
    css_class = 'fa fa-{fa}'

    # span_size = 18

    def __init__(self, *args, **kwargs):
        css_class = kwargs.pop('css_class', self.css_class).format(fa=kwargs.pop('span_fa', None))
        kw = kwargs.copy()
        kw.update({'css_class': css_class})
        super().__init__(*args, **kw)

    def render(self, obj):
        """ Render link as HTML output tag <a>.
        """
        if getattr(obj, '_action_permission', None) and not obj._action_permission(self, self.acao):
            return mark_safe('')

        return super().render(obj)


def ActionColumn(vieweditdelete, chave, can_delete=True, can_edit=True, can_view=False, can_drill_down=False,
                 can_workflow=False, can_compare=False, report=False, ajax=True, new_window=False, *args, **kwargs):
    """ Cria os botões de ação no final da linha da Table que pode ser para:
            adição, edição, exclusão, visualização, drill down, comparar versão usando reverse ou report.
        Opcionalmente pode passar a view específica de cada ação acima, senão usa a padrão:
            view_edit, view_delete, view_view, view_workflow, view_drill_down
    """

    links = []

    if can_edit:
        links += [FontAwesomeLink(text='Editar', viewname=kwargs.get('view_edit', vieweditdelete),
                                  args=(Accessor(chave), ACAO_EDIT,),
                                  span_fa='pencil-alt', span_tip='Editar', acao=ACAO_EDIT, ajax=ajax), ]
    if can_delete:
        links += [FontAwesomeLink(text='Excluir', viewname=kwargs.get('view_delete', vieweditdelete),
                                  args=(Accessor(chave), ACAO_DELETE,),
                                  span_fa='trash-alt', span_tip='Excluir', acao=ACAO_DELETE, ajax=ajax), ]
    if can_view:
        links += [FontAwesomeLink(text='Consultar', viewname=kwargs.get('view_view', vieweditdelete),
                                  args=(Accessor(chave), ACAO_VIEW,),
                                  span_fa='eye', span_tip='Consultar', acao=ACAO_VIEW, ajax=ajax), ]
    if can_workflow:
        links += [FontAwesomeLink(text='Consultar', viewname=kwargs.get('view_workflow', vieweditdelete),
                                  args=(Accessor(chave),),
                                  span_fa='eye', span_tip='Consultar', acao=ACAO_VIEW, ajax=ajax), ]
    if can_drill_down:
        links += [FontAwesomeLink(text='Drill Down', viewname=kwargs.get('view_drill_down', vieweditdelete),
                                  args=(Accessor(chave), ACAO_VIEW,),
                                  span_fa='level-down',
                                  span_tip='Drill Down - Aperte Ctrl+Left Mouse Click para abrir em outra aba',
                                  acao=ACAO_VIEW, ajax=ajax), ]  # pencil-square
    if can_compare:
        links += [FontAwesomeLink(text='Comparar', viewname=kwargs.get('view_compare', vieweditdelete),
                                  args=(Accessor(chave),),
                                  span_fa='random', span_tip='Comparar Últimas Versões', acao=ACAO_VIEW, ajax=ajax), ]
    if report:
        links += [FontAwesomeLink(text='Imprimir', viewname=kwargs.get('view_report', vieweditdelete),
                                  span_fa='print', args=(Accessor(chave),), ajax=ajax, new_window=new_window), ]

    # Verifica se foi passado parâmetro com novos links
    links_parm = kwargs.get('links', [])

    # não há como saber se é ou não ajax na construção do link externo, então atualiza conforme o que está se passando
    # para os outros links
    for i in links_parm:
        i.ajax = ajax

    # Adiciona aos links padrões
    links += links_parm

    return LinkColumn(header='Ação', links=links, searchable=False, sortable=False)


def ActionCVBColumn(view_name, chave, can_delete=True, can_edit=True, can_view=False, can_drill_down=False,
                    can_workflow=False, can_compare=False, report=False, ajax=True, new_window=False, *args, **kwargs):
    """ Cria os botões de ação no final da linha da Table que pode ser para:
            adição, edição, exclusão, visualização, drill down, comparar versão usando reverse ou report.
        Opcionalmente pode passar a view específica de cada ação acima, senão usa a padrão:
            view_edit, view_delete, view_view, view_workflow, view_drill_down
    """

    links = []

    if can_edit:
        viewname = kwargs.get('view_edit', f'{view_name}_update')
        links += [FontAwesomeLink(text='Editar', viewname=viewname,
                                  args=[Accessor(chave), ],
                                  span_fa='pencil-alt', span_tip='Editar', acao=ACAO_EDIT, ajax=ajax), ]
    if can_delete:
        viewname = kwargs.get('view_edit', f'{view_name}_delete')
        links += [FontAwesomeLink(text='Excluir', viewname=viewname,
                                  args=(Accessor(chave),),
                                  span_fa='trash-alt', span_tip='Excluir', acao=ACAO_DELETE, ajax=ajax), ]
    if can_view:
        viewname = kwargs.get('view_edit', f'{view_name}_detail')
        links += [FontAwesomeLink(text='Consultar', viewname=viewname,
                                  args=(Accessor(chave),),
                                  span_fa='eye', span_tip='Consultar', acao=ACAO_VIEW, ajax=ajax), ]
    # if can_workflow:
    #     links += [FontAwesomeLink(text='Consultar', viewname=kwargs.get('view_workflow', view_name),
    #                               args=(Accessor(chave),),
    #                               span_fa='eye', span_tip='Consultar', acao=ACAO_VIEW, ajax=ajax), ]
    # if can_drill_down:
    #     links += [FontAwesomeLink(text='Drill Down', viewname=kwargs.get('view_drill_down', view_name),
    #                               args=(Accessor(chave), ACAO_VIEW,),
    #                               span_fa='level-down',
    #                               span_tip='Drill Down - Aperte Ctrl+Left Mouse Click para abrir em outra aba',
    #                               acao=ACAO_VIEW, ajax=ajax), ]  # pencil-square
    # if can_compare:
    #     links += [FontAwesomeLink(text='Comparar', viewname=kwargs.get('view_compare', view_name),
    #                               args=(Accessor(chave),),
    #                               span_fa='random', span_tip='Comparar Últimas Versões', acao=ACAO_VIEW, ajax=ajax), ]
    # if report:
    #     links += [FontAwesomeLink(text='Imprimir', viewname=kwargs.get('view_report', view_name),
    #                               span_fa='print', args=(Accessor(chave),), ajax=ajax, new_window=new_window), ]

    # Verifica se foi passado parâmetro com novos links
    links_parm = kwargs.get('links', [])

    # não há como saber se é ou não ajax na construção do link externo, então atualiza conforme o que está se passando
    # para os outros links
    for i in links_parm:
        i.ajax = ajax

    # Adiciona aos links padrões
    links += links_parm

    return LinkColumn(header='Ação', links=links, searchable=False, sortable=False)
