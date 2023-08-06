## Concrete model views for Workflow support
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit
from django.core.exceptions import ImproperlyConfigured
from django.forms import models as model_forms

from common.model_views import ListView, CreateView, UpdateView, DeleteView, DetailView, URLGenerator
from common.views import get_class
from .forms import ProcessesInstanceTable
from .models import ProcessInstanceManager, ProcessInstance, WorkItem
from .signals import workflow_process_instance_created


class WorkflowMixin(object):
    # Workflow
    subject = None
    filter = None
    process = None
    workitem = None

    # Queryset and object lookup

    def get_object(self):
        """ Returns the object the view is displaying. """
        obj = super().get_object()
        return obj

    # Form instantiation

    def get_form_class(self, instance=None):
        """
        Returns the form class to use in this view.
        """
        if instance:
            try:
                form_class = instance.workitem().activity.get_form_class(instance=instance if instance else None)
                return get_class(form_class)
            except Exception as e:
                pass

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
        cls = self.get_form_class(instance=kwargs.get('instance', None))
        form = cls(data=data, files=files, **kwargs)
        return self.set_buttons(form)

    def form_valid(self, form):
        # Se for readonly, não aceita salva no POST
        try:
            self.workitem = form.instance.workitem()
            readonly = self.workitem.activity.readonly
        except:
            readonly = False

        if not readonly:
            self.object = form.save()
        self.workitem = self.process_workflow()

        return self.response_success(extrajavascript='')

    # Response rendering

    def get_context_data(self, **kwargs):
        # Se activity é readonly, então seta disableMe
        try:
            if self.object.workitem().activity.readonly:
                self.disableMe = True
        except:
            pass

        return super().get_context_data(**kwargs)

    # Workflow

    def process_workflow(self):
        raise NotImplementedError()


class ListWorkflowView(WorkflowMixin, ListView):
    def get_form(self, data=None, files=None, **kwargs):
        """
        Returns a form instance.
        """
        cls = self.get_form_class()
        form = cls(data=data, **kwargs)
        return self.set_buttons(form)

    def set_buttons(self, form):
        """ Insert all necessaries buttons in form """

        # if add:
        #     form.opts.std_button_create = {'text': 'Incluir', 'icon': 'fa fa-plus-square fa-fw',
        #                                     'href': form.opts.std_button_create_href,
        #                                     "className": 'btn btn-primary btn-sm', }
        # else:
        #     form.opts.std_button_create = False

        if self.subject and isinstance(form, ProcessesInstanceTable):
            form.base_columns[0].visible = False  # Column pk is hidden if filtering by subject
            form.base_columns[1].visible = False  # Column Processo is hidden if filtering by subject
        else:
            form.base_columns[0].visible = True
            form.base_columns[1].visible = True

        return form


class CreateWorkflowView(WorkflowMixin, CreateView):
    def process_workflow(self):
        # process = Process.objects.get(title=self.process_name, enabled=True)
        # if self.priority is None:
        #     try:
        #         self.priority = self.obj.get_priority()
        #     except Exception as v:
        #         self.priority = process.priority

        self.process_name = self.process.title
        self.priority = self.process.priority

        user = self.request.user

        title = ('%s %s' % (self.process_name, str(self.object)))[:100]

        instance = ProcessInstance.objects.create(process=self.process, user=user,
                                                  title=title, content_object=self.object)

        # instance running
        instance.set_status(ProcessInstance.STATUS_PENDING)

        workitem = WorkItem.objects.create(instance=instance, user=user,
                                           activity=self.process.begin, priority=self.priority)

        workflow_process_instance_created.send_robust(sender=instance, user=user, process_name=self.process_name)

        wi_next = workitem.process(request=self.request)

        return wi_next

    # def form_valid(self, form):
    #     # Se for readonly, não aceita salva no POST
    #     try:
    #         readonly = form.instance.workitem().activity.readonly
    #     except:
    #         readonly = False
    #
    #     if not readonly:
    #         self.object = form.save()
    #         wi = self.process_workflow()
    #
    #     return self.response_success(extrajavascript='')


class UpdateWorkflowView(WorkflowMixin, UpdateView):
    def set_buttons(self, form):
        """ Insert all necessaries buttons in form """
        workitem = self.object.workitem()
        if workitem.activity.readonly:
            fields = []
        else:
            fields = [self.get_save_button()]
        for i in workitem.activity.transition_inputs.all():
            fields.append(Submit('save', i.condition, css_class="btn-danger btn-sm"))
        fields.append(self.get_cancel_button())
        form.helper.layout.extend([FormActions(*fields, css_class=self.buttons_css_class)])
        return form

    def process_workflow(self):
        # Se wi está inativo, então ativa
        self.workitem.activate(self.request)
        # Processa o que será feito no wi, se mantém na mesma activity ou faz transição
        wi_next = self.workitem.process(request=self.request)
        return wi_next


class DeleteWorkflowView(WorkflowMixin, DeleteView):
    pass


class DetailWorkflowView(WorkflowMixin, DetailView):
    pass


class URLWorkflowGenerator(URLGenerator):
    """
    Constructs and returns Workflow urls for generic views for a given model.

    URL names follow the pattern: <lower case model name>_<action>
        - ``lowercasemodelname``:   For the ListView.
        - ``lowercasemodelname_detail``: For the DetailView.
        - ``lowercasemodelname_create``: For the CreateView.
        - ``lowercasemodelname_update``: For the UpdateView.
        - ``lowercasemodelname_delete``: For the DeleteView.
    """

    def __init__(self, model, form_class=None, form_table=None, view_prefix=None, cancel_url=None,
                 subject=None, filter=ProcessInstanceManager.FILTER_ALL, process=None,
                 *args, **kwargs):
        self.subject = subject
        self.filter = filter
        self.process = process

        # Inicializa views para Workflow

        listview_cls = kwargs.pop('listview_cls', ListWorkflowView)
        createview_cls = kwargs.pop('createview_cls', CreateWorkflowView)
        updateview_cls = kwargs.pop('updateview_cls', UpdateWorkflowView)
        # deleteview_cls = kwargs.pop('deleteview_cls', DeleteWorkflowView)
        detailview_cls = kwargs.pop('detailview_cls', DetailWorkflowView)

        super().__init__(model, form_class, form_table, view_prefix, cancel_url,
                         listview_cls=listview_cls,
                         createview_cls=createview_cls, updateview_cls=updateview_cls, detailview_cls=detailview_cls,
                         # deleteview_cls=deleteview_cls,
                         *args, **kwargs)

    def set_form_class(self, form_class=None):
        """
        Sets the form class to be used by the create and update views.
        """
        if form_class:
            self.form_class = form_class
        else:
            try:
                # Tenta achar o form padrão de criação/edição/deleção no formato: ModelForm
                self.form_class = get_class(
                    f'{self.model._meta.app_label}.forms.{self.model._meta.object_name}WorkflowForm')
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
                self.form_table = get_class(
                    f'{self.model._meta.app_label}.forms.{self.model._meta.object_name}WorkflowTable')
            except Exception as e:
                self.form_table = ProcessesInstanceTable
                # fields = self.model.get_allowed_fields() if hasattr(self.model, 'get_allowed_fields') else '__all__'
                # self.form_table = model_forms.modelform_factory(self.model, fields=fields)

    def get_urlpatterns(self, crud_types='crul', paginate_by=15, **kwargs):
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
        kwargs.update({'subject': self.subject, 'filter': self.filter, 'process': self.process})
        if 'c' in crud_types:
            urlpatterns.append(self.get_create_path(suffix='create_wf', **kwargs))
        if 'r' in crud_types:
            urlpatterns.append(self.get_detail_path(suffix='detail_wf', **kwargs))
        if 'u' in crud_types:
            urlpatterns.append(self.get_update_path(suffix='update_wf', **kwargs))
        if 'l' in crud_types:
            urlpatterns.append(self.get_list_path(paginate_by=paginate_by, **kwargs))
        # if 'd' in crud_types:
        #     urlpatterns.append(self.get_delete_path(suffix='delete_wf', **kwargs))

        return urlpatterns
