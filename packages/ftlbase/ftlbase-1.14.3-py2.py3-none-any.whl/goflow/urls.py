from django.urls import path, include, re_path

from common import forms
from common.utils import ACAO_WORKFLOW_TO_APPROVE
from common.views import commonListaTable
from goflow.apptools.views import default_app
from goflow.runtime.forms import ProcessWorkItemTable, ProcessesInstanceTable, ProcessesInstanceTableNews, \
    ProcessesInstanceTableMyworks, ProcessesInstanceTablePending
from goflow.runtime.models import ProcessInstanceManager
from goflow.runtime.views import workflow_action, workflow_execute, workflow_flag_news, \
    workflow_flag_myworks, workflow_table_process, workflow_graph, workflow_history_workitems_table, \
    workflow_graph_process, workflow_action_cbv
from goflow.workflow.views import process_dot, cron

urlpatterns = [
    # path('.*/logout/$', logout),
    # path('.*/accounts/login/$', login, {'template_name': 'goflow/login.html'}),
    path('apptools/', include('goflow.apptools.urls')),
    # path('graph/', include('goflow.graphics.urls')),
]

urlpatterns += [
    # path('$', index),
    path('process/dot/<int:id>', process_dot, name='process_dot'),
    path('cron/', cron, name='cron'),
]

urlpatterns += [
    re_path(r'^default_app/(?P<id>.*)/$', default_app, name='default_app'),
    #     path('start/(?P<app_label>.*)/(?P<model_name>.*)/$', start_application),
    #     path('start_proto/(?P<process_name>.*)/$', start_application,
    #         {'form_class': DefaultAppStartForm,
    #          'redirect': '../../',
    #          'template': 'goflow/start_proto.html'}),
]

urlpatterns += [
    # Workflow
    path('action/', workflow_action,
         {'goto': 'workflow_pending', 'dictionary': {'acao': ACAO_WORKFLOW_TO_APPROVE, 'disableMe': True}},
         name="workflow_action_home"),
    path('action/<int:id>/', workflow_action,
         {'goto': 'workflow_pending', 'dictionary': {'acao': ACAO_WORKFLOW_TO_APPROVE, 'disableMe': True}},
         name="workflow_action"),
    path('action/cbv/<int:id>/', workflow_action_cbv,
         {'goto': 'workflow_pending', 'dictionary': {'acao': ACAO_WORKFLOW_TO_APPROVE, 'disableMe': True}},
         name="workflow_action_cbv"),
    # path('ratify/<int:id>/', common_views.workflow_action,
    #     {'goto': 'workflow_pending',
    #      'dictionary': {'acao': common_forms.ACAO_WORKFLOW_RATIFY, 'disableMe': True}}, name="workflow_to_ratify"),
    path('workflow_execute/<int:id>/', workflow_execute,
         {'goto': 'workflow_pending', 'dictionary': {'disableMe': True}},
         name="workflow_execute_std"),

    path('flag/news/', workflow_flag_news, name='workflow_flag_news'),
    path('flag/myworks/', workflow_flag_myworks, name='workflow_flag_myworks'),

    path('news/', commonListaTable, {'model': ProcessesInstanceTableNews}, name='workflow_news'),
    path('myworks/', commonListaTable, {'model': ProcessesInstanceTableMyworks}, name='workflow_myworks'),
    path('pending/', commonListaTable, {'model': ProcessesInstanceTablePending}, name='workflow_pending'),
    path('all/', commonListaTable, {'model': ProcessesInstanceTable}, name='workflow_all'),
    # path('news/', workflow_table_process, {'filter': ProcessInstanceManager.FILTER_NEWS}, name='workflow_news'),
    # path('myworks/', workflow_table_process, {'filter': ProcessInstanceManager.FILTER_MY}, name='workflow_myworks'),
    # path('pending/', workflow_table_process, {'filter': ProcessInstanceManager.FILTER_PENDING},
    #      name='workflow_pending'),
    # path('all/', workflow_table_process, {'filter': ProcessInstanceManager.FILTER_ALL}, name='workflow_all'),

    path('graph/<int:pk>/', workflow_graph, name='workflow_graph'),
    path('process_graph/<str:title>/', workflow_graph_process, name='workflow_process_graph'),
    path('history/<int:pk>/', workflow_history_workitems_table,
         {'goto': 'workflow_pending', 'model': ProcessWorkItemTable},
         name="workflow_history"),

]

# urlpatterns += [
#     path('otherswork/$', otherswork),
#     path('otherswork/instancehistory/$', instancehistory),
#     path('myrequests/$', myrequests),
#     path('myrequests/instancehistory/$', instancehistory),
#     path('mywork/$', mywork),
#     path('mywork/activate/(?P<id>.*)/$', activate),
#     path('mywork/complete/(?P<id>.*)/$', complete),
# ]
