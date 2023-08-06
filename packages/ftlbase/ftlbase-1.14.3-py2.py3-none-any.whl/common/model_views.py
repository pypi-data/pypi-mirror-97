# coding: utf-8
import json
import re

import django
import six
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Button, Submit
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, InvalidPage
from django.forms import models as model_forms
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import re_path, reverse_lazy
from django.views.generic import View
from render_block import render_block_to_string

from common.views import get_class

# Avoid RemovedInDjango40Warning on Django 3.0+
if django.VERSION >= (3, 0):
    from django.utils.translation import gettext as _
else:
    from django.utils.translation import ugettext as _


class GenericModelView(View):
    """
    Base class for all model generic views.
    """
    model = None
    fields = None

    # Object lookup parameters. These are used in the URL kwargs, and when
    # performing the model instance lookup.
    # Note that if unset then `lookup_url_kwarg` defaults to using the same
    # value as `lookup_field`.
    lookup_field = 'pk'
    lookup_url_kwarg = None

    # All the following are optional, and fall back to default values
    # based on the 'model' shortcut.
    # Each of these has a corresponding `.get_<attribute>()` method.
    queryset = None
    form_class = None
    template_name = None
    context_object_name = None

    # Pagination parameters.
    # Set `paginate_by` to an integer value to turn pagination on.
    paginate_by = None
    page_kwarg = 'page'

    #  Suffix that should be appended to automatically generated template names.
    template_name_suffix = None

    # Buttons
    success_url = None
    cancel_url = None
    buttons_css_class = 'col-md-11 text-right buttons-do-form'

    # Javascript
    extrajavascript = ''
    disableMe = None

    # URL ajax or not
    def get_url(self, url):
        return ('#' if self.request.is_ajax() else '') + (url + '')

    # Queryset and object lookup

    def get_queryset(self):
        """
        Returns the base queryset for the view.

        Either used as a list of objects to display, or as the queryset
        from which to perform the individual object lookup.
        """
        if self.queryset is not None:
            return self.queryset._clone()

        if self.model is not None:
            return self.model._default_manager.all()

        msg = "'%s' must either define 'queryset' or 'model', or override 'get_queryset()'"
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def get_lookup(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        try:
            lookup = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        except KeyError:
            msg = "Lookup field '%s' was not provided in view kwargs to '%s'"
            raise ImproperlyConfigured(msg % (lookup_url_kwarg, self.__class__.__name__))

        return lookup

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.get_queryset()

        lookup = self.get_lookup()

        return get_object_or_404(queryset, **lookup)

    # Form instantiation

    def get_form_class(self):
        """
        Returns the form class to use in this view.
        """
        if self.form_class is not None:
            return self.form_class

        if self.model is not None and self.fields is not None:
            return model_forms.modelform_factory(self.model, fields=self.fields)

        msg = "'%s' must either define 'form_class' or both 'model' and " \
              "'fields', or override 'get_form_class()'"
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def get_form(self, data=None, files=None, **kwargs):
        """
        Returns a form instance.
        """
        cls = self.get_form_class()
        form = cls(data=data, files=files, **kwargs)
        return self.set_buttons(form)

    def set_buttons(self, form):
        """ Insert all necessaries buttons in form """
        return form

    def get_cancel_button(self):
        """ Return cancel button to form """
        linkCancel = self.get_url(self.get_cancel_url())
        # TODO: tratar is_ajax
        onclick = linkCancel if linkCancel == 'javascript:history.back()' else "window.location.href='%s'" % linkCancel
        return Button('cancel', 'Cancelar', css_class="btn-cancel btn-sm", onclick=onclick)

    def get_save_button(self):
        """ Insert all necessaries buttons in form """
        return Submit('save', 'Salvar', css_class="btn-primary btn-sm")

    def get_delete_button(self):
        """ Insert all necessaries buttons in form """
        return Submit('DELETE', 'Confirmar exclusão do registro', css_class="btn-danger btn-sm")

    def get_cancel_url(self):
        try:
            return self.cancel_url or self.model.get_cancel_url()
        except AttributeError:
            msg = "No URL to redirect to. '%s' must provide 'cancel_url' " \
                  "or define a 'get_cancel_url()' method on the Model."
            raise ImproperlyConfigured(msg % self.__class__.__name__)
        # return reverse_lazy(self.model._meta.model_name)

    def get_success_url(self):
        try:
            return self.success_url or self.object.get_absolute_url()
        except AttributeError:
            msg = "No URL to redirect to. '%s' must provide 'success_url' " \
                  "or define a 'get_absolute_url()' method on the Model."
            raise ImproperlyConfigured(msg % self.__class__.__name__)

    # Pagination

    def get_paginate_by(self):
        """
        Returns the size of pages to use with pagination.
        """
        return self.paginate_by

    def get_paginator(self, queryset, page_size):
        """
        Returns a paginator instance.
        """
        return Paginator(queryset, page_size)

    def paginate_queryset(self, queryset, page_size):
        """
        Paginates a queryset, and returns a page object.
        """
        paginator = self.get_paginator(queryset, page_size)
        page_kwarg = self.kwargs.get(self.page_kwarg)
        page_query_param = self.request.GET.get(self.page_kwarg)
        page_number = page_kwarg or page_query_param or 1
        try:
            page_number = int(page_number)
        except ValueError:
            if page_number == 'last':
                page_number = paginator.num_pages
            else:
                msg = "Page is not 'last', nor can it be converted to an int."
                raise Http404(_(msg))

        try:
            return paginator.page(page_number)
        except InvalidPage as exc:
            msg = 'Invalid page (%s): %s'
            raise Http404(_(msg) % (page_number, six.text_type(exc)))

    # Response rendering

    def get_context_object_name(self, is_list=False):
        """
        Returns a descriptive name to use in the context in addition to the
        default 'object'/'object_list'.
        """
        if self.context_object_name is not None:
            return self.context_object_name

        elif self.model is not None:
            fmt = '%s_list' if is_list else '%s'
            return fmt % self.model._meta.object_name.lower()

        return None

    def get_extrajavascript(self):
        # Monta javascript a ser usado
        # extrajavascript pode vir via parâmetro na criação de GenericModelView (self.extrajavascript),
        # via parâmetro na criação da View (kwargs.get(['extrajavascript'],'')) ou
        # via function do form self.form_class.extrajavascript(instance=self.object)
        extrajavascript = "\n".join([self.extrajavascript, self.kwargs.get('extrajavascript', '')])
        try:
            script = self.form_class.extrajavascript(instance=self.object if hasattr(self, 'object') else None)
            extrajavascript = "\n".join([extrajavascript, script])
        except Exception as e:
            pass

        return extrajavascript

    def get_context_data(self, **kwargs):
        """
        Returns a dictionary to use as the context of the response.

        Takes a set of keyword arguments to use as the base context,
        and adds the following keys:

        * 'view'
        * Optionally, 'object' or 'object_list'
        * Optionally, '{context_object_name}' or '{context_object_name}_list'
        """
        kwargs['view'] = self

        if getattr(self, 'object', None) is not None:
            kwargs['object'] = self.object
            context_object_name = self.get_context_object_name()
            if context_object_name:
                kwargs[context_object_name] = self.object

        if getattr(self, 'object_list', None) is not None:
            kwargs['object_list'] = self.object_list
            context_object_name = self.get_context_object_name(is_list=True)
            if context_object_name:
                kwargs[context_object_name] = self.object_list

        # Se a resposta seja'ajax/json ou não
        kwargs['ajax'] = self.request.is_ajax()

        # Monta o javascript
        kwargs['extrajavascript'] = self.get_extrajavascript()

        # Tratamento de Erro
        try:
            if kwargs['form'].errors:
                kwargs['form_errors'] = kwargs['form'].errors
        except Exception as e:
            pass

        return kwargs

    def get_template_names(self):
        """
        Returns a list of template names to use when rendering the response.

        If `.template_name` is not specified, then defaults to the following
        pattern: "{app_label}/{model_name}{template_name_suffix}.html"
        """
        if self.template_name is not None:
            return [self.template_name]

        if self.model is not None and self.template_name_suffix is not None:
            return 'cadastroPadrao.html'
            # return ["%s/%s%s.html" % (
            #     self.model._meta.app_label,
            #     self.model._meta.object_name.lower(),
            #     self.template_name_suffix
            # )]

        msg = "'%s' must either define 'template_name' or 'model' and " \
              "'template_name_suffix', or override 'get_template_names()'"
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def response_success(self, *args, **kwargs):
        url = kwargs.pop('url', self.get_success_url()) + ''  # Essa coisa ridícula de somar '' é porque a url é lazy
        if self.request.is_ajax():
            extrajavascript = kwargs.pop('extrajavascript', self.get_extrajavascript())
            ret = {'goto': url, 'extrajavascript': extrajavascript,}
            ret.update(kwargs)
            return JsonResponse(ret)
        else:
            HttpResponseRedirect(url)

    def render_to_response(self, context):
        """
        Given a context dictionary, returns an HTTP response.
        """
        if self.request.is_ajax():
            title = render_block_to_string(self.get_template_names(), "title_html", context=context)
            html = render_block_to_string(self.get_template_names(), "content", context=context)
            html = re.sub('<link(.*?)/>', '', html)
            html = re.sub('<script type="text/javascript" src=(.*?)</script>', '', html)

            script = render_block_to_string(self.get_template_names(), "extrajavascript", context=context)
            # Soma-se '' porque success_url pode ser lazy, e json.dump dá erro, então força-se a avaliar a expressão
            dump = {'title': title, 'html': html, 'extrajavascript': script,
                    'form_errors': context.get('form_errors'), 'formset_errors': context.get('formset_errors'), }
            if self.disableMe:
                dump.update({'disableMe': True})
            try:
                url = self.get_success_url() + ''
                dump.update({'goto': url, })
            except Exception as e:
                pass

            return HttpResponse(json.dumps(dump), content_type='application/json')
            # return HttpResponse(json.dumps(dump, cls=LazyEncoder), content_type='application/json')

        return TemplateResponse(request=self.request, template=self.get_template_names(), context=context)


## The concrete model views

class ListView(GenericModelView):
    template_name_suffix = '_list'
    allow_empty = True

    def get_form(self, data=None, files=None, **kwargs):
        """
        Returns a form instance.
        """
        cls = self.get_form_class()
        form = cls(data=data, **kwargs)
        return self.set_buttons(form)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginate_by = self.get_paginate_by()

        if not self.allow_empty and not queryset.exists():
            raise Http404

        form = self.get_form(data=queryset)

        if paginate_by is None:
            #  Unpaginated response
            self.object_list = queryset
            context = self.get_context_data(objetos=form, page_obj=None, is_paginated=False, paginator=None, )
        else:
            # Paginated response
            page = self.paginate_queryset(queryset, paginate_by)
            self.object_list = page.object_list
            context = self.get_context_data(objetos=form, page_obj=page, is_paginated=page.has_other_pages(),
                                            paginator=page.paginator, )

        return self.render_to_response(context)

    def get_template_names(self):
        # return ['bsct/plain/list.html']
        return ['table.html']


class DetailView(GenericModelView):
    # success_url = None
    template_name_suffix = '_detail'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(instance=self.object)
        context = self.get_context_data(form=form)
        # a = LayoutSlice(form.helper.layout, [form.helper.layout.get_field_names()[10]])
        # form.helper.exclude_by_widget(TextInput)
        # context = self.get_context_data()
        return self.render_to_response(context)

    def set_buttons(self, form):
        """ Insert all necessaries buttons in form """
        form.helper.layout.extend([FormActions(self.get_cancel_button(), css_class=self.buttons_css_class)])
        return form


class CreateView(GenericModelView):
    # success_url = None
    template_name_suffix = '_form'

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return self.response_success()
        # url = self.get_success_url() + ''
        # return JsonResponse({
        #     'goto': url,
        #     'extrajavascript': self.get_extrajavascript()
        # }) if self.request.is_ajax() else HttpResponseRedirect(url)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_success_url(self):
        try:
            return self.success_url or self.object.get_absolute_url()
        except AttributeError:
            msg = "No URL to redirect to. '%s' must provide 'success_url' " \
                  "or define a 'get_absolute_url()' method on the Model."
            raise ImproperlyConfigured(msg % self.__class__.__name__)

    def set_buttons(self, form):
        """ Insert all necessaries buttons in form """
        form.helper.layout.extend([FormActions(self.get_save_button(), self.get_cancel_button(),
                                               css_class=self.buttons_css_class)])
        return form


class UpdateView(GenericModelView):
    # success_url = None
    template_name_suffix = '_form'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(instance=self.object)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(data=request.POST, files=request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return self.response_success()
        # url = self.get_success_url() + ''
        # return JsonResponse({
        #     'goto': url,
        #     'extrajavascript': self.get_extrajavascript()
        # }) if self.request.is_ajax() else HttpResponseRedirect(url)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_success_url(self):
        try:
            return self.success_url or self.object.get_absolute_url()
        except AttributeError:
            msg = "No URL to redirect to. '%s' must provide 'success_url' " \
                  "or define a 'get_absolute_url()' method on the Model."
            raise ImproperlyConfigured(msg % self.__class__.__name__)

    def set_buttons(self, form):
        """ Insert all necessaries buttons in form """
        form.helper.layout.extend([FormActions(self.get_save_button(), self.get_cancel_button(),
                                               css_class=self.buttons_css_class)])
        return form


class DeleteView(GenericModelView):
    # success_url = None
    template_name_suffix = '_confirm_delete'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(instance=self.object)
        context = self.get_context_data(form=form)
        # context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        url = self.get_success_url() + ''
        return JsonResponse({
            'goto': url,
            'extrajavascript': self.get_extrajavascript()
        }) if self.request.is_ajax() else HttpResponseRedirect(url)

    def get_success_url(self):
        if self.success_url is None and self.cancel_url is None:
            msg = "No URL to redirect to. '%s' must define 'success_url' or 'cancel_url'"
            raise ImproperlyConfigured(msg % self.__class__.__name__)
        return self.success_url or self.cancel_url

    def set_buttons(self, form):
        """ Insert all necessaries buttons in form """
        form.helper.layout.extend([FormActions(self.get_delete_button(), self.get_cancel_button(),
                                               css_class=self.buttons_css_class)])
        return form


class URLGenerator(object):
    """
    Constructs and returns CRUD urls for generic views for a given model.

    URL names follow the pattern: <lower case model name>_<action>
        - ``lowercasemodelname``:   For the ListView.
        - ``lowercasemodelname_detail``: For the DetailView.
        - ``lowercasemodelname_create``: For the CreateView.
        - ``lowercasemodelname_update``: For the UpdateView.
        - ``lowercasemodelname_delete``: For the DeleteView.
    """

    def __init__(self, model, form_class=None, form_table=None, view_prefix=None, cancel_url=None, *args, **kwargs):
        """
        Internalize the model and set the view prefix.
        """
        self.model = model
        self.view_prefix = view_prefix or model.__name__.lower()
        # self.cancel_url = cancel_url if cancel_url else self.model._meta.model_name
        self.cancel_url = cancel_url if cancel_url else self.view_prefix
        self.set_form_class(form_class)
        self.set_form_table(form_table)

        lookup_field = kwargs.pop('lookup_field', 'pk')
        self.lookup_field = lookup_field
        # d => int, w => string
        # O reverse não achar a URL quando o parâmetro é string e tem "-", exemplo o CEP,
        # então tem que colocar um "-" no pattern da regex
        lookup_type = kwargs.pop('lookup_type', 'd')
        self.lookup_type = f'{"-" if lookup_type == "w" else ""}\\{lookup_type}'

        self.listview_cls = kwargs.pop('listview_cls', ListView)
        self.createview_cls = kwargs.pop('createview_cls', CreateView)
        self.updateview_cls = kwargs.pop('updateview_cls', UpdateView)
        self.deleteview_cls = kwargs.pop('deleteview_cls', DeleteView)
        self.detailview_cls = kwargs.pop('detailview_cls', DetailView)

    def set_form_class(self, form_class=None):
        """
        Sets the form class to be used by the create and update views.
        """
        if form_class:
            self.form_class = form_class
        else:
            try:
                # Tenta achar o form padrão de criação/edição/deleção no formato: ModelForm
                self.form_class = get_class(f'{self.model._meta.app_label}.forms.{self.model._meta.object_name}Form')
            except Exception as e:
                fields = self.model.get_allowed_fields() if hasattr(self.model, 'get_allowed_fields') else '__all__'
                self.form_class = model_forms.modelform_factory(self.model, fields=fields)

    def set_form_table(self, form_table=None):
        """ Sets the form table to be used by the list views. """
        if form_table:
            self.form_table = form_table
        else:
            try:
                # Tenta achar o form padrão de criação/edição/deleção no formato: ModelTableForm
                self.form_table = get_class(f'{self.model._meta.app_label}.forms.{self.model._meta.object_name}Table')
            except Exception as e:
                msg = "Table for model '%s' does not exists!"
                raise ImproperlyConfigured(msg % (self.model._meta.object_name))
                # fields = self.model.get_allowed_fields() if hasattr(self.model, 'get_allowed_fields') else '__all__'
                # self.form_table = model_forms.modelform_factory(self.model, fields=fields)

    def get_cancel_url(self):
        return reverse_lazy(self.cancel_url) if self.cancel_url else None

    def get_list_path(self, **kwargs):
        """
        Generate the list URL for the model.
        """
        return re_path(
            r'%s/(list/?)?$' % self.view_prefix,
            self.listview_cls.as_view(model=self.model, form_class=self.form_table, **kwargs),
            name='%s' % self.view_prefix,
            # name='%s_list' % self.view_prefix,
        )

    def get_create_path(self, form_class=None, suffix='create', **kwargs):
        """
        Generate the create URL for the model.
        """
        form_class = form_class if form_class else self.form_class

        return re_path(
            r'%s/create/?$' % self.view_prefix,
            self.createview_cls.as_view(model=self.model, form_class=form_class,
                                        success_url=self.get_cancel_url(), cancel_url=self.get_cancel_url(),
                                        **kwargs),
            name=f'{self.view_prefix}_{suffix}',
        )

    def get_update_path(self, form_class=None, suffix='update', **kwargs):
        """
        Generate the update URL for the model.
        """
        form_class = form_class if form_class else self.form_class

        return re_path(
            r'%s/update/(?P<%s>[%s]+)/?$' % (self.view_prefix, self.lookup_field, self.lookup_type),
            self.updateview_cls.as_view(model=self.model, form_class=form_class, lookup_field=self.lookup_field,
                                        success_url=self.get_cancel_url(), cancel_url=self.get_cancel_url(),
                                        **kwargs),
            name=f'{self.view_prefix}_{suffix}',
        )

    def get_delete_path(self, form_class=None, suffix='delete', **kwargs):
        """
        Generate the delete URL for the model.
        """
        form_class = form_class if form_class else self.form_class

        return re_path(
            r'%s/delete/(?P<%s>[%s]+)/?$' % (self.view_prefix, self.lookup_field, self.lookup_type),
            self.deleteview_cls.as_view(model=self.model, form_class=form_class, lookup_field=self.lookup_field,
                                        success_url=self.get_cancel_url(), cancel_url=self.get_cancel_url(),
                                        # success_url=reverse_lazy('%s_delete' % self.view_prefix),
                                        **kwargs
                                        ),
            name=f'{self.view_prefix}_{suffix}',
        )

    def get_detail_path(self, form_class=None, suffix='detail', **kwargs):
        """
        Generate the detail URL for the model.
        """
        form_class = form_class if form_class else self.form_class

        return re_path(
            r'%s/(?P<%s>[%s]+)/?$' % (self.view_prefix, self.lookup_field, self.lookup_type),
            self.detailview_cls.as_view(model=self.model, form_class=form_class, lookup_field=self.lookup_field,
                                        cancel_url=self.get_cancel_url(),
                                        **kwargs),
            name=f'{self.view_prefix}_{suffix}',
        )

    def get_urlpatterns(self, crud_types='crudl', paginate_by=15, **kwargs):
        """
        Generate the entire set URL for the model and return as a patterns
        object.
        Specific CRUD types may be in the string argument crud_types specified, where:
            'c' - Refers to the Create CRUD type
            'r' - Refers to the Read/Detail CRUD type
            'u' - Refers to the Update/Edit CRUD type
            'd' - Refers to the Delete CRUD type
            'l' - Refers to the List CRUD type
        """
        urlpatterns = []
        if 'c' in crud_types:
            urlpatterns.append(self.get_create_path(**kwargs))
        if 'r' in crud_types:
            urlpatterns.append(self.get_detail_path(**kwargs))
        if 'u' in crud_types:
            urlpatterns.append(self.get_update_path(**kwargs))
        if 'l' in crud_types:
            urlpatterns.append(self.get_list_path(paginate_by=paginate_by, **kwargs))
        if 'd' in crud_types:
            urlpatterns.append(self.get_delete_path(**kwargs))

        return urlpatterns
