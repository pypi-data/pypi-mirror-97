#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render
# from django.template import RequestContext
#
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse, path

from common import empresa as emp
from common.utils import ACAO_WORKFLOW_READONLY, ACAO_WORKFLOW_APPROVE, ACAO_WORKFLOW_RATIFY, ACAO_EDIT, \
    ACAO_WORKFLOW_START
from common.views import commonListaTable, get_class, commonRender, commonCadastro
from .forms import ProcessesInstanceTable
from .models import ProcessInstance, WorkItem, ProcessInstanceManager, WorkItemManager, InvalidWorkflowStatus
#
#
# @login_required
# def mywork(request, template='goflow/mywork.html'):
#     """
#     displays the worklist of the current user.
#
#     parameters:
#
#     template
#         default:'goflow/mywork.html'
#     """
#     workitems = WorkItem.objects.list_safe(user=request.user)
#     return render(request, template, {'workitems': workitems},
#                               context_instance=RequestContext(request))
#
#
# @login_required
# def otherswork(request, template='goflow/otherswork.html'):
#     worker = request.GET['worker']
#     workitems = WorkItem.objects.list_safe(user=worker, noauto=False)
#     return render(request, template, {'worker': worker, 'workitems': workitems},
#                               context_instance=RequestContext(request))
#
#
# @login_required
# def instancehistory(request, template='goflow/instancehistory.html'):
#     id = int(request.GET['id'])
#     inst = ProcessInstance.objects.get(pk=id)
#     return render(request, template, {'instance': inst},
#                               context_instance=RequestContext(request))
#
#
# @login_required
# def myrequests(request, template='goflow/myrequests.html'):
#     inst_list = ProcessInstance.objects.filter(user=request.user)
#     return render(request, template, {'instances': inst_list},
#                               context_instance=RequestContext(request))
#
#
# @login_required
# def activate(request, id):
#     """
#     activates and redirect to the application.
#
#     parameters:
#
#     id
#         workitem id
#     """
#     id = int(id)
#     workitem = WorkItem.objects.get_safe(id=id, user=request.user)
#     workitem.activate(request.user)
#     return _app_response(workitem)
#
#
# @login_required
# def complete(request, id):
#     """
#     redirect to the application.
#
#     parameters:
#
#     id
#         workitem id
#     """
#     id = int(id)
#     workitem = WorkItem.objects.get_safe(id=id, user=request.user)
#     return _app_response(workitem)
#
#
# def _app_response(workitem):
#     id = workitem.id
#     activity = workitem.activity
#     if not activity.process.enabled:
#         return HttpResponse('Processo %s desabilitado.' % activity.process.title)
#
#     if activity.kind == 'subflow':
#         # subflow
#         sub_workitem = workitem.start_subflow()
#         return _app_response(sub_workitem)
#
#     # no application: default_app
#     if not activity.application:
#         url = '../../../default_app'
#         return HttpResponseRedirect('%s/%d/' % (url, id))
#
#     if activity.kind == 'standard':
#         # standard activity
#         return HttpResponseRedirect(activity.application.get_app_url(workitem))
#     return HttpResponse('completion page.')
from .use_cases import WorkItemProcessKind
from ..workflow.models import Process


@login_required
def workflow_table_process(request, table=ProcessesInstanceTable, goto='index', subject=None,
                           filter=ProcessInstanceManager.FILTER_ALL,
                           add=False, disableMe=False):
    query = ProcessInstance.objects.all_safe(user=request.user, subject=subject, filter=filter)

    if add:
        table.opts.std_button_create = {'text': 'Incluir', 'icon': 'fa fa-plus-square fa-fw',
                                        'href': table.opts.std_button_create_href,
                                        "className": 'btn btn-primary btn-sm', }
    else:
        table.opts.std_button_create = False

    if subject and table == ProcessesInstanceTable:
        table.base_columns[0].visible = False  # Column pk is hidden if filtering by subject
        table.base_columns[1].visible = False  # Column Processo is hidden if filtering by subject
    else:
        table.base_columns[0].visible = True
        table.base_columns[1].visible = True

    # Tratamento para workflow ou itens onde tem formset que pode ser adicionado, mas os anteriores ficam desabilitado
    # para não ter alteração.
    dictionary = {'disableMe': disableMe}

    return commonListaTable(request, model=table, queryset=query, goto=goto, dictionary=dictionary)


@login_required
def workflow_history_workitems_table(request, pk, model=None, queryset=None, goto='index', template_name="table.html",
                                     tableScript=None, referencia=None, extrajavascript='', dictionary=None,
                                     permissions=None):
    workitems = WorkItemManager.get_process_workitems(pk, user=request.user)
    return commonListaTable(request, model=model, queryset=workitems, goto=goto, template_name=template_name,
                            tableScript=tableScript, referencia=referencia, dictionary=dictionary,
                            permissions=permissions)
    # extrajavascript=extrajavascript, dictionary=dictionary, permissions=permissions)


@login_required
def workflow_action(request, id=None, goto='workflow_pending', dictionary=None):
    """
    activates and redirect to the application.

    :param request:
    :param id: workitem id
    :param goto: 'workflow_pending' ou 'workflows_all' se workflow concluído
    :param dictionary: parâmetros extras, ex.: {'disableMe': True}
    :return: rendered html
    """

    def _app_response(request, workitem, goto, dictionary):
        """
        Verifica se há subworkflow e executa, senão faz o redirect para a configuração do WF

        :param workitem:
        :return:
        """

        # id = workitem.id
        def _execute_activity(workitem, activity, dictionary):
            # standard activity
            url = activity.application.get_app_url(workitem)
            func, args, kwargs = resolve(url)
            # params has to be an dict ex.: { 'form_class': 'imovel.form.ContratoLocForm', 'goto': 'contratoLoc'}
            params = activity.app_param
            # params values defined in activity override those defined in urls.py
            if params:
                try:
                    params = eval('{' + params.lstrip('{').rstrip('}') + '}')
                    # Carrega o form dos parâmetros form_class e formInlineDetail dinamicamente e faz a substituição
                    forms = ['form_class', 'formInlineDetail']
                    for f in forms:
                        if f in params:
                            # Se form_class existe então deve ser no formado <módulo>.<arquivo>.FormClass
                            #   e faz seu carregamento manualmente abaixo
                            p = params.get(f, None)
                            try:
                                params.update({f: get_class(p)})
                            except:
                                pass
                except Exception as v:
                    pass
                kwargs.update({'dictionary': dictionary})
                kwargs.update(params)

            # Marretada para evitar que o param acao seja injected em kwargs e dê problema no sendmail
            # Opção seria incluir acao no sendmail
            if activity.application.url not in ['apptools/sendmail', ]:
                kwargs.update({'workitem': workitem,
                               'acao': ACAO_WORKFLOW_READONLY if workitem.instance.status == ProcessInstance.STATUS_CONCLUDED
                               else ACAO_WORKFLOW_APPROVE if activity.approve
                               else ACAO_WORKFLOW_RATIFY if activity.ratify
                               else dictionary.get('acao', ACAO_EDIT)})
            ret = func(request, **kwargs)
            return ret

        dic = dictionary.copy()

        # if dic is None:
        #     dic = {}
        #
        # dic.update({'empresa': emp})
        #
        activity = workitem.activity

        if workitem.instance.status != ProcessInstance.STATUS_CONCLUDED:
            if request.method == 'POST':
                workitem.activate(request)

            if not activity.process.enabled:
                extrajavascript = 'riot.mount("ftl-error-message", {messages: [{type: \'error\', msg: "Processo %s está desabilitado."}, ]});' % activity.process.title
                dic.update({'extrajavascript': extrajavascript})
                return commonRender(request, 'error.html', dic)

            if activity.kind == 'subflow':
                # subflow
                sub_workitem = workitem.start_subflow(request)
                return _app_response(request, sub_workitem, goto, dic)

        # # no application: default_app
        # if not activity.application:
        #     url = 'default_app'
        #     # url = '../../../default_app'
        #     # return HttpResponseRedirect('%s/%d/' % (url, id))
        #     return HttpResponseRedirect('/#' + reverse(url, args=[id]))
        #
        if activity.kind == 'dummy':
            return _execute_activity(workitem, activity, dic)

        if activity.kind == 'standard':
            ret = _execute_activity(workitem, activity, dic)
            # Se não retornou nada (ex. sendmail(), então verifica se é autofinish para executar complete do workitem
            if ret is None and \
                    workitem.activity.autofinish and workitem.instance.status != ProcessInstance.STATUS_CONCLUDED:
                workitem.complete(request)
                dic.update({'goto': goto})
                return commonRender(request, 'base.html', dic)
            return ret

        extrajavascript = 'riot.mount("ftl-error-message", {messages: [{type: \'error\', msg: "Erro no Workflow, não há aplicação configurada em %s."}, ]});' % activity.process.title
        dic.update({'extrajavascript': extrajavascript, 'goto': resolve(request.path).view_name})
        return commonRender(request, 'error.html', dic)
        # return HttpResponse('completion page.')

    dic = dictionary.copy()
    if dic is None:
        dic = {}
    dic.update({'empresa': emp})

    try:
        id = int(id)
        workitem = WorkItem.objects.get_safe(id=id, user=request.user)
        # no application: default_app
        if not workitem.activity.application:
            url = 'default_app'
            # url = '../../../default_app'
            # return HttpResponseRedirect('%s/%d/' % (url, id))
            return HttpResponseRedirect('/#' + reverse(url, args=[id]))

    except Exception as v:
        if type(v) == InvalidWorkflowStatus:
            workitem = v.workitem
        else:
            extrajavascript = 'riot.mount("ftl-error-message", {messages: [{type: \'error\', msg: "%s"}, ]});' % str(v)
            dic.update({'extrajavascript': extrajavascript,
                        'goto': resolve(request.path).view_name})  # OR resolve(request.path).url_name ?????
            return commonRender(request, 'error.html', dic)

    # return _app_response(request, workitem, goto, dic)
    result = WorkItemProcessKind.run(request=request, workitem=workitem, goto=goto, dic=dic)
    return result.return_value


@login_required
def workflow_execute(request, **kwargs):
    """
    activates and redirect to the application.

    :param request:
    :param kwargs:
        acao: Ação a ser executada
        form_class: Form a ser usado
        formInlineDetail: Inline detail a ser usado (optional)
        goto: 'workflow_pending' ou 'workflows_all' se workflow concluído
        dictionary: parâmetros extras, ex.: {'disableMe': True}
        extrajavascript: javascript a ser anexado ao form
        workitem: workitem ativo
    :return:
    """
    workitem = kwargs.get('workitem', None)

    acao = kwargs.get('acao', ACAO_EDIT)
    formModel = kwargs.get('form_class')
    formInlineDetail = kwargs.get('formInlineDetail')
    goto = kwargs.get('goto',
                      'workflow_all' if workitem and workitem.status == WorkItem.STATUS_CONCLUDED else 'workflow_pending')
    dictionary = kwargs.get('dictionary', {})
    # submit_name é o nome do form que está sendo gravado
    dictionary.update({'submit_name': request.POST.get('save', '')})
    extrajavascript = kwargs.get('extrajavascript', '')

    pk = workitem.instance.wfobject().pk if workitem else None

    return commonCadastro(request, acao, formModel, goto=goto, formInlineDetail=formInlineDetail, pk=pk,
                          dictionary=dictionary, workitem=workitem, extrajavascript=extrajavascript)


@login_required
def workflow_flag_myworks(request, **kwargs):
    """
    list all my workitems

    parameters:
    template: 'Atendimento'
    """
    template_name = kwargs.get('template_name', 'workflow/workflow_myworks.html')
    workitems = WorkItemManager.list_safe(user=request.user, roles=False, withoutrole=False, noauto=False)
    dictionary = kwargs.get('dictionary', {})
    dictionary.update({'workitems': workitems})

    return commonRender(request, template_name, dictionary)


@login_required
def workflow_flag_news(request, **kwargs):
    """
    list all my workitems

    parameters:
    template: 'Atendimento'
    """
    template_name = kwargs.get('template_name', 'workflow/workflow_news.html')
    workitems = WorkItemManager.list_safe(user=None, roles=True, status=[WorkItem.STATUS_INACTIVE, ],
                                          withoutrole=True, noauto=False)
    dictionary = kwargs.get('dictionary', {})
    dictionary.update({'workitems': workitems})

    return commonRender(request, template_name, dictionary)


@login_required
def workflow_graph(request, pk, template='graph.html'):
    """Gera gráfico do workflow
    pk: process id
    template: template
    """
    instance = ProcessInstance.objects.get(pk=pk)
    mark_pending = set()
    mark_completed = set()
    mark_problem = set()
    for a in instance.workitems.all():
        if a.status in [WorkItem.STATUS_INACTIVE, WorkItem.STATUS_PENDING]:
            mark_pending.add(a.activity.pk)
        elif a.status in [WorkItem.STATUS_CONCLUDED]:
            mark_completed.add(a.activity.pk)
        else:
            mark_problem.add(a.activity.pk)
    args = {'pending': list(mark_pending), 'completed': list(mark_completed), 'problem': list(mark_problem)}
    process = instance.process
    context = {
        'process': process,
        'args': args,
    }
    return commonRender(request, template, context)


@login_required
def workflow_graph_process(request, title, template='graph.html'):
    """Gera gráfico do process
    pk: process id or title
    template: template
    """
    try:
        process = Process.objects.get(id=title)
    except Exception as v:
        process = Process.objects.get(title=title)
    mark_pending = set()
    mark_completed = set()
    mark_problem = set()
    args = {'pending': list(mark_pending), 'completed': list(mark_completed), 'problem': list(mark_problem)}
    context = {
        'process': process,
        'args': args,
    }
    return commonRender(request, template, context)


def include_Workflow(name, table=ProcessesInstanceTable, form=None, subject=None,
                     filter=ProcessInstanceManager.FILTER_ALL, add=True, disableMe=False):
    urls = []
    if table:
        urls.extend([
            path('{0}/'.format(name), workflow_table_process,
                 {'table': table, 'subject': subject, 'filter': filter, 'add': add, 'disableMe': disableMe},
                 name=name)
        ])
    if add:
        urls.extend([
            path('{0}/add/'.format(name), workflow_execute,
                 {'acao': ACAO_WORKFLOW_START, 'form_class': form, 'goto': name},
                 name="{0}Add".format(name)),
            # Não tem Update ou Delete, pois é parte de Workflow
        ])
    return urls


@login_required
def workflow_action_cbv(request, id=None, goto='workflow_pending', dictionary=None):
    """
    activates and redirect to the application.

    :param request:
    :param id: workitem id
    :param goto: 'workflow_pending' ou 'workflows_all' se workflow concluído
    :param dictionary: parâmetros extras, ex.: {'disableMe': True}
    :return: rendered html
    """

    def _app_response(request, workitem, goto, dictionary):
        """
        Verifica se há subworkflow e executa, senão faz o redirect para a configuração do WF

        :param workitem:
        :return:
        """

        # id = workitem.id
        def _execute_activity(workitem, activity, dictionary):
            # standard activity
            url = activity.application.get_app_url(workitem)
            func, args, kwargs = resolve(url)
            # params has to be an dict ex.: { 'form_class': 'imovel.form.ContratoLocForm', 'goto': 'contratoLoc'}
            params = activity.app_param
            # params values defined in activity override those defined in urls.py
            if params:
                try:
                    params = eval('{' + params.lstrip('{').rstrip('}') + '}')
                    # Carrega o form dos parâmetros form_class e formInlineDetail dinamicamente e faz a substituição
                    forms = ['form_class', 'formInlineDetail']
                    for f in forms:
                        if f in params:
                            # Se form_class existe então deve ser no formado <módulo>.<arquivo>.FormClass
                            #   e faz seu carregamento manualmente abaixo
                            p = params.get(f, None)
                            try:
                                params.update({f: get_class(p)})
                            except:
                                pass
                except Exception as v:
                    pass
                kwargs.update({'dictionary': dictionary})
                kwargs.update(params)

            # Marretada para evitar que o param acao seja injected em kwargs e dê problema no sendmail
            # Opção seria incluir acao no sendmail
            if activity.application.url not in ['apptools/sendmail', ]:
                kwargs.update({'workitem': workitem,
                               'acao': ACAO_WORKFLOW_READONLY if workitem.instance.status == ProcessInstance.STATUS_CONCLUDED
                               else ACAO_WORKFLOW_APPROVE if activity.approve
                               else ACAO_WORKFLOW_RATIFY if activity.ratify
                               else dictionary.get('acao', ACAO_EDIT)})
            # params['form_class']._meta.model._meta.model_name
            ret = func(request, **kwargs)
            return ret

        dic = dictionary.copy()

        # if dic is None:
        #     dic = {}
        #
        # dic.update({'empresa': emp})
        #
        activity = workitem.activity

        if workitem.instance.status != ProcessInstance.STATUS_CONCLUDED:
            if request.method == 'POST':
                workitem.activate(request)

            if not activity.process.enabled:
                extrajavascript = 'riot.mount("ftl-error-message", {messages: [{type: \'error\', msg: "Processo %s está desabilitado."}, ]});' % activity.process.title
                dic.update({'extrajavascript': extrajavascript})
                return commonRender(request, 'error.html', dic)

            if activity.kind == 'subflow':
                # subflow
                sub_workitem = workitem.start_subflow(request)
                return _app_response(request, sub_workitem, goto, dic)

        # # no application: default_app
        # if not activity.application:
        #     url = 'default_app'
        #     # url = '../../../default_app'
        #     # return HttpResponseRedirect('%s/%d/' % (url, id))
        #     return HttpResponseRedirect('/#' + reverse(url, args=[id]))
        #
        if activity.kind == 'dummy':
            return _execute_activity(workitem, activity, dic)

        if activity.kind == 'standard':
            ret = _execute_activity(workitem, activity, dic)
            # Se não retornou nada (ex. sendmail(), então verifica se é autofinish para executar complete do workitem
            if ret is None and \
                    workitem.activity.autofinish and workitem.instance.status != ProcessInstance.STATUS_CONCLUDED:
                workitem.complete(request)
                dic.update({'goto': goto})
                return commonRender(request, 'base.html', dic)
            return ret

        extrajavascript = 'riot.mount("ftl-error-message", {messages: [{type: \'error\', msg: "Erro no Workflow, não há aplicação configurada em %s."}, ]});' % activity.process.title
        dic.update({'extrajavascript': extrajavascript, 'goto': resolve(request.path).view_name})
        return commonRender(request, 'error.html', dic)
        # return HttpResponse('completion page.')

    dic = dictionary.copy()
    if dic is None:
        dic = {}
    dic.update({'empresa': emp})

    try:
        id = int(id)
        workitem = WorkItem.objects.get_safe_instance(id=id, user=request.user)
        # no application: default_app
        if not workitem.activity.application:
            url = 'default_app'
            # url = '../../../default_app'
            # return HttpResponseRedirect('%s/%d/' % (url, id))
            return HttpResponseRedirect('/#' + reverse(url, args=[id]))

    except Exception as v:
        if type(v) == InvalidWorkflowStatus:
            workitem = v.workitem
        else:
            extrajavascript = 'riot.mount("ftl-error-message", {messages: [{type: \'error\', msg: "%s"}, ]});' % str(v)
            dic.update({'extrajavascript': extrajavascript,
                        'goto': resolve(request.path).view_name})  # OR resolve(request.path).url_name ?????
            return commonRender(request, 'error.html', dic)

    return _app_response(request, workitem, goto, dic)
    # result = WorkItemProcessKind.run(request=request, workitem=workitem, goto=goto, dic=dic)
    # return result.return_value


