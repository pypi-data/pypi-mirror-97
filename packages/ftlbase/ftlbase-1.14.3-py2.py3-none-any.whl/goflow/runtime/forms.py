from django.urls import reverse_lazy

from goflow.apptools.widgets import WorkflowColumnCBV
from goflow.runtime.models import WorkItem, ProcessInstance, ProcessInstanceManager
from table import Table
from table.columns import DatetimeColumn, Column


class ProcessWorkItemTable(Table):
    # id = Column(field='instance.pk')
    date = DatetimeColumn(field='date')
    user = Column(field='user')
    descricao = Column(header='Descrição', field='instance.content_object')
    activity = Column(field='activity')
    priority = Column(field='priority')
    status = Column(field='status')

    class Meta:
        model = WorkItem
        # ajax = True
        # sort = [(0, 'asc'), ]
        std_button = False
        search = False
        pagination = False
        totals = False
        info = False
        std_button_create = {'text': 'Incluir novo atendimento', 'icon': 'fa fa-plus-square fa-fw',
                             'href': reverse_lazy('atendimentoAdd'),
                             "className": 'btn btn-primary btn-sm', }


def table_queryset_processinstance(request, filter):
    subject = None
    qs = ProcessInstance.objects.all_safe(user=request.user, subject=subject, filter=filter)
    return qs


def table_queryset_processinstance_myworks(request):
    return table_queryset_processinstance(request=request, filter=ProcessInstanceManager.FILTER_MY)


def table_queryset_processinstance_news(request):
    return table_queryset_processinstance(request=request, filter=ProcessInstanceManager.FILTER_NEWS)


def table_queryset_processinstance_pending(request):
    return table_queryset_processinstance(request=request, filter=ProcessInstanceManager.FILTER_PENDING)


def table_queryset_processinstance_all(request):
    return table_queryset_processinstance(request=request, filter=ProcessInstanceManager.FILTER_ALL)


class ProcessesInstanceTable(Table):
    id = Column(header='#', field='pk')
    process = Column(header='Processo', field='process.subject')
    descricao = Column(header='Descrição', field='content_object')
    status = Column(header='Status', field='status')
    activity = Column(header='Atividade', field='activity')
    status2 = Column(header='Status Ativ', field='activity_status')
    # priority = Column(header='Prioridade', field='priority')
    user = Column(field='user')  # OU É user_name??????????????????????
    creationTime = DatetimeColumn(field='creationTime')
    # action = WorkflowColumn(header='Ação', field='instance')
    action = WorkflowColumnCBV(header='Ação', field='instance')

    class Meta:
        model = ProcessInstance
        ajax = True
        # sort = [(0, 'asc'), ]
        # std_button = False
        std_button_create = False
        queryset = table_queryset_processinstance_all


class ProcessesInstanceTableMyworks(ProcessesInstanceTable):
    class Meta:
        model = ProcessInstance
        ajax = True
        std_button_create = False
        queryset = table_queryset_processinstance_myworks


class ProcessesInstanceTableNews(ProcessesInstanceTable):
    class Meta:
        model = ProcessInstance
        ajax = True
        std_button_create = False
        queryset = table_queryset_processinstance_news


class ProcessesInstanceTablePending(ProcessesInstanceTable):
    class Meta:
        model = ProcessInstance
        ajax = True
        std_button_create = False
        queryset = table_queryset_processinstance_pending
