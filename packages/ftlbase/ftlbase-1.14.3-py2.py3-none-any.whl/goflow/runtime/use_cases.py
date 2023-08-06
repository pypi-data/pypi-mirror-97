from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import resolve

import mutations
from common.logger import Log
from common.utils import ACAO_WORKFLOW_START, ACAO_WORKFLOW_READONLY, ACAO_WORKFLOW_APPROVE, ACAO_WORKFLOW_RATIFY, \
    ACAO_EDIT
from mutations.fields import build_field_for, StringField, ObjectField, IntField, RequestField, DictField
from .models import ProcessInstance, WorkItem, WorkItemManager, Event
from .signals import workflow_process_instance_created
from ..workflow.models import Process, UserProfile, Activity
from ..workflow.notification import send_mail

log = Log('goflow.runtime.use_case')

ProcessInstanceField = build_field_for("ProcessInstanceField", ProcessInstance)
WorkItemField = build_field_for("WorkItemField", WorkItem)
ActivityField = build_field_for("ActivityField", Activity)


# Todos os Use Cases de GoFlow Runtime

class ProcessStart(mutations.Mutation):
    """
    Process: Start a Workflow

    Returns a workitem given the name of a preexisting enabled Process
    instance, while passing in the id of the user, the contenttype
    object and the title.

    :type process_name: string
    :param process_name: a name of a process. e.g. 'leave'
    :type request: request
    :param request: request object.
    :type obj: ContentType
    :param obj: a content_type object e.g. an instance of LeaveRequest
    :type: priority: integer
    :param priority: default priority (optional)
    :rtype: WorkItem
    :return: a newly configured workitem sent to auto_user,
             a target_user, or ?? (roles).

    usage::

        wi = ProcessStart.run(process_name='leave', user=admin, obj=leaverequest1)

    """
    # process_name, obj
    process_name = StringField(required=True)
    request = RequestField(required=True)
    obj = ObjectField(required=True)
    priority = IntField(required=False, default=None)

    def execute(self):
        """
        """
        # workitem = ProcessInstance.objects.start(process_name=self.process_name, request=self.request, obj=self.obj,
        #                                          priority=self.priority)

        process = Process.objects.get(title=self.process_name, enabled=True)
        if self.priority is None:
            try:
                self.priority = self.obj.get_priority()
            except Exception as v:
                self.priority = process.priority

        user = self.request.user

        title = '%s %s' % (self.process_name, str(self.obj))

        instance = ProcessInstance.objects.create(process=process, user=user, title=title, content_object=self.obj)

        # instance running
        instance.set_status(ProcessInstance.STATUS_PENDING)

        workitem = WorkItem.objects.create(instance=instance, user=user, activity=process.begin, priority=self.priority)

        workflow_process_instance_created.send_robust(sender=instance, user=user, process_name=self.process_name)

        # wi_next = workitem.process(request=self.request)
        result = WorkItemProcess.run(workitem=workitem, request=self.request)
        wi_next = result.return_value

        return wi_next
        # return workitem


class WorkItemProcess(mutations.Mutation):
    """
    Process: Start a Workflow
    """
    # process_name, obj
    workitem = WorkItemField(required=True)
    request = RequestField(required=True)

    def execute(self):
        # workitem = self.workitem
        workitem = self.workitem.process(request=self.request)
        return workitem


class WorkflowProcessTreatment(mutations.Mutation):
    """
    Process: Start a Workflow
    """
    # process_name, obj
    request = RequestField(required=True)
    obj = ObjectField(required=True)
    acao = StringField(required=True)
    process_name = StringField(required=False)
    priority = IntField(required=False, default=None)
    workitem = WorkItemField(required=False, default=None)

    def execute(self):
        if self.acao in (ACAO_WORKFLOW_START) and self.obj:
            # Start Workflow
            # Prioridade é tratada no start
            # workitem = ProcessInstance.objects.start(process_name=process_name, user=request.user, obj=obj)
            result = ProcessStart.run(process_name=self.process_name, request=self.request, obj=self.obj)
        elif self.workitem:
            # workitem.process(request)
            result = WorkItemProcess.run(workitem=self.workitem, request=self.request)
        else:
            result = {}
        return result.return_value if result else None


class WorkflowNotify(mutations.Mutation):
    """ WorkflowNotify: Send email if needed """

    workitem = WorkItemField(required=True)
    fallout = StringField(required=False, default=None)

    def execute(self):
        """ notify user if conditions are fullfilled
            If user is not None and workitem, than send email only to this user.
            If check_notif_to_send, then send all pending emails
            If roles is not None then sent email to all users that belong roles
        """
        # Se tem activity então avalia se é push ou pull
        activity = self.workitem.activity
        if self.fallout:
            # Se deu erro, fall out
            users = Group.objects.filter(name='workflow-admin')
            # users_names = [user.name for user in users]
            subject = 'Workflow Error: fall out workitem ' + self.fallout + ' - users: %s'
            template = 'goflow/mail-fall-out'
        else:
            template = 'goflow/mail-pending'
            if activity.push_application:
                roles = None
                users = [self.workitem.user, ]
                subject = 'Workflow Push - %s'
            else:
                roles = self.workitem.pull_roles.all()
                users = get_user_model().objects.filter(groups__in=roles)
                subject = 'Workflow Pull Roles - %s'

        # Se não tem usuários a enviar email, então retorna
        if not users:
            Event.objects.create(name='WorkflowNotify: Algum erro na notificação por email, usuário vazio',
                                 workitem=self.workitem)
            return None

        users_names = [user.username for user in users]

        subject = subject % users_names

        task = None

        # log.info('notification sent to %s' % users_names)
        # Envia email para o usuário específico
        if activity.sendmail:
            try:
                task = send_mail(workitems=[self.workitem], users=users, subject=subject, template=template)
            except Exception as v:
                log.error('sendmail error: %s' % v)
            Event.objects.create(name=template, workitem=self.workitem, external_task=task)
        else:
            Event.objects.create(name=template + ', no email sent', workitem=self.workitem)

        # Envia email com lista de todas suas pendências para usuário quando ainda não enviou conforme
        # check_notif_to_send.
        # Seria um email geral do dia com todas as pendências
        # Nesse momento ignora sendmail, pois a qtde ultrapassou o limite de notificação definido para o usuário
        for user in users:
            profile = UserProfile.objects.get_or_create(user=user)[0]
            if profile.check_notif_to_send():
                wis = WorkItemManager.list_safe(user=user, withoutrole=False, noauto=False)
                if len(wis) >= profile.nb_wi_notif and wis is not None:
                    try:
                        task = send_mail(workitems=wis, users=[user, ],
                                         subject='Workflow: Pendências',
                                         template='goflow/mail-all-pending')
                        profile.notif_sent()
                        log.info('notification sent all pending workitem to %s' % user.username)
                    except Exception as v:
                        log.error('sendmail error: only %s' % v)

        # if roles is not None:
        #     users = get_user_model().objects.filter(groups=roles)
        #     result = WorkflowNotify.run(workitem=self.workitem, users=users, roles=None)
        #     task = result.return_value

        return task


class WorkItemProcessKind(mutations.Mutation):
    """
    Process: Trata na view o que é
    """
    # request, workitem, goto, dic
    request = RequestField(required=True)
    workitem = WorkItemField(required=True)
    goto = StringField(required=True)
    dic = DictField(required=True)

    def _execute_activity(self, request, workitem, activity, dictionary):
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
                            from common.views import get_class
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

    def execute(self):
        from common.views import commonRender
        request = self.request
        workitem = self.workitem
        goto = self.goto
        dic = self.dic
        activity = workitem.activity

        if workitem.instance.status != ProcessInstance.STATUS_CONCLUDED:
            if request.method == 'POST':
                workitem.activate(request)
            elif request.method == 'GET':
                # Se a atividade é dummy, mas o status é concluído e a instance ainda está pendente, então
                # deu algum erro, tem que tentar acionar o próximo para consertar o workflow
                if activity.kind == 'dummy' and workitem.status == WorkItem.STATUS_CONCLUDED:
                    workitem = workitem.process(request)

            if not activity.process.enabled:
                extrajavascript = 'riot.mount("ftl-error-message", {messages: [{type: \'error\', msg: "Processo %s está desabilitado."}, ]});' % activity.process.title
                dic.update({'extrajavascript': extrajavascript})
                return commonRender(request, 'error.html', dic)

            if activity.kind == 'subflow':
                # subflow
                sub_workitem = workitem.start_subflow(request)
                # return _app_response(request, sub_workitem, goto, dic)
                result = WorkItemProcessKind.run(request=request, workitem=sub_workitem, goto=goto, dic=dic)
                log.info('WorkItemProcessKind: Sub Workflow: '
                         'request={request}, workitem={workitem}, goto={goto}, dic={dic}'.format(request=request,
                                                                                                 workitem=sub_workitem,
                                                                                                 goto=goto, dic=dic))
                return result.return_value

        # # no application: default_app
        # if not activity.application:
        #     url = 'default_app'
        #     # url = '../../../default_app'
        #     # return HttpResponseRedirect('%s/%d/' % (url, id))
        #     return HttpResponseRedirect('/#' + reverse(url, args=[id]))
        #
        if activity.kind == 'dummy':
            return self._execute_activity(request, workitem, activity, dic)

        if activity.kind == 'standard':
            ret = self._execute_activity(request, workitem, activity, dic)
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

        # workitem = self.workitem
        # workitem = self.workitem.process(request=self.request)
        # return workitem
