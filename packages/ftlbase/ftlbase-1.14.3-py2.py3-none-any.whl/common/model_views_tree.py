from django.core.exceptions import ImproperlyConfigured
from django.forms import models as model_forms
from django.urls import reverse

from common.model_views import ListView, CreateView, UpdateView, DeleteView, DetailView
from common.utils import ACAO_EDIT


## Concrete model views for Tree support

class TreeMixin(object):
    # Tree
    idTree = 'masterTreeManager'
    dataUrl = None
    # dataTreeURL = None
    acaoURL = None
    updateParent = 'index'

    def get_extrajavascript(self):
        # Para Tree é necessário executar a montagem do modal popup
        extrajavascript = super().get_extrajavascript()

        pk = self.object.pk if hasattr(self, 'object') and self.object and self.object.pk else ""
        title = str(self.object) if hasattr(self, 'object') and self.object else self.model._meta.object_name
        updateParent = reverse(self.updateParent) if self.updateParent else None

        dataTreeURL = self.dataUrl % pk if self.dataUrl else ""

        extrajavascriptTree = ("""$('#{0}').attr('data-url','{1}');
        ftl_form_modal = riot.mount('div#ftl-form-modal', 'ftl-form-modal', {{
          'modal': {{isvisible: false, contextmenu: false, idtree: '{0}'}},
          'data': {{pk: {2}, action: {3}, acaoURL: '{4}', updateParent: '{5}', modaltitle: '{6}'}},
        }});
        """.format(self.idTree, dataTreeURL, pk, ACAO_EDIT, self.acaoURL, updateParent, title))
        extrajavascript = "\n".join([extrajavascript, extrajavascriptTree])

        return extrajavascript


class ListTreeView(TreeMixin, ListView):
    def get_extrajavascript(self):
        # Na List não é necessário javascript, mesmo para Tree
        return ''

    def get_form_class(self):
        """
        Returns the form class to use in this view.
        """
        if self.form_class is not None:
            return self.form_class

        if self.model is not None:
            return model_forms.modelform_factory(self.model, fields=self.fields)
        # if self.model is not None and self.fields is not None:
        #     return model_forms.modelform_factory(self.model, fields=self.fields)

        msg = "'%s' must either define 'form_class' or both 'model' and " \
              "'fields', or override 'get_form_class()'"
        raise ImproperlyConfigured(msg % self.__class__.__name__)


class CreateTreeView(TreeMixin, CreateView):
    pass


class UpdateTreeView(TreeMixin, UpdateView):
    pass


class DeleteTreeView(TreeMixin, DeleteView):
    pass


class DetailTreeView(TreeMixin, DetailView):
    pass
