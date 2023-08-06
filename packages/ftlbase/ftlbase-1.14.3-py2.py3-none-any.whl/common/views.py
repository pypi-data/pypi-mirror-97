# -*- coding: utf-8 -*-

import itertools
import json
import re

from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Button
from django import forms
from django.contrib import messages
from django.contrib.auth import logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import Context, RequestContext
from django.urls import path, reverse
from django.utils.crypto import get_random_string
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from render_block import render_block_to_string
from reversion.models import Version

from common import empresa as emp
from common.logger import Log
from common.utils import has_permission, get_goto_url, ACAO_ADD, ACAO_EDIT, ACAO_DELETE, ACAO_VIEW, ACAO_REPORT, \
    ACAO_REPORT_EXPORT, ACAO_WORKFLOW_START, ACAO_WORKFLOW_TO_APPROVE, ACAO_WORKFLOW_APPROVE, ACAO_WORKFLOW_RATIFY, \
    ACAO_WORKFLOW_READONLY, ACAO_EMAIL, ACAO_EXEC, export_users
from goflow.runtime.models import ProcessInstance, WorkItem
from goflow.runtime.use_cases import WorkflowProcessTreatment
from goflow.workflow.models import Process
from .forms import PeriodoForm
from .models import Rota, CompareVersion
from .reports import montaURLjasperReport

log = Log('commom.views')


def get_class(path):
    """
    if path is a string, then import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    Else return itself.
    """
    if path and isinstance(path, str):
        # Se form_class existe então deve ser no formado <módulo>.<arquivo>.FormClass
        #   e faz seu carregamento manualmente abaixo
        # p = path.split('.')
        # if len(p) == 3:
        try:
            the_form = import_string(path)  # Função do Django para importar Class, view, etc.
            # the_module = importlib.import_module(f'{p[0]}.{p[1]}')
            # the_form = getattr(the_module, p[2])
            # the_module = __import__(p[0] + '.' + p[1])
            # the_class = getattr(the_module, p[1])
            # the_form = getattr(the_class, p[2])
            return the_form
        except:
            # else:
            raise ImportError(f'Module "{path}" does not define a attribute/class')
    return path


def configuraButtonsNoForm(form, acao, goto, *args, **kwargs):
    """
    Configura botões padrões de save ou delete e cancel no final do form
    """
    url = get_goto_url(form.instance if hasattr(form, 'instance') else None, goto)
    linkCancel = url if url == 'javascript:history.back()' else "window.location.href='#%s'" % url
    linkWorkflow = "ftltabs.trigger('closeTab', 'Workflow', '#%s');" % url
    css_class = 'col-md-11 text-right buttons-do-form'
    if acao in (ACAO_WORKFLOW_START, ACAO_WORKFLOW_TO_APPROVE, ACAO_WORKFLOW_APPROVE,
                ACAO_WORKFLOW_RATIFY, ACAO_WORKFLOW_READONLY):
        cancel = Button('cancel', 'Cancelar', css_class="btn-cancel btn-sm", onclick=linkWorkflow)
    else:
        cancel = Button('cancel', 'Cancelar', css_class="btn-cancel btn-sm", onclick=linkCancel)

    workitem = kwargs.get('workitem', None)
    onclick = kwargs.get('onclick', None)

    # onde = mark_safe("<i class='fa fa-map-marker' style='font-size:18px;color:#09568d;' data-toggle='tooltip' " +
    #                  "title='Onde estou?'>Onde estou?</i>")

    # form.helper['save'].update_attributes(css_class="hello")
    if acao in (ACAO_ADD, ACAO_EDIT, ACAO_WORKFLOW_START, ACAO_EXEC):
        form.helper.layout.extend([
            FormActions(
                Submit('save', 'Salvar', css_class="btn-primary btn-sm", onclick=onclick),
                cancel,
                css_class=css_class)
        ])
    elif acao == ACAO_DELETE:
        form.helper.layout.extend([
            FormActions(
                Submit('DELETE', 'Confirmar exclusão do registro', css_class="btn-danger btn-sm", aria_hidden="true"),
                cancel,
                css_class=css_class)
        ])
    elif acao == ACAO_REPORT:
        form.helper.layout.extend([
            FormActions(
                Submit('save', 'Consultar', css_class="btn-primary btn-sm"),
                Button('cancel', 'Cancelar', css_class="btn-cancel btn-sm", onclick=linkCancel),
                css_class='col-md-11 text-right')
        ])
    elif acao == ACAO_REPORT_EXPORT:
        form.helper.layout.extend([
            FormActions(
                Submit('save', 'Consultar', css_class="btn-primary btn-sm"),
                Submit('save', 'Exportar', css_class="btn-success btn-sm"),
                cancel,
                css_class=css_class)
        ])
    elif acao == ACAO_WORKFLOW_TO_APPROVE:
        fields = [Submit('save', i.condition, css_class="btn-danger btn-sm") for i in
                  workitem.activity.transition_inputs.all()]
        form.helper.layout.extend([
            FormActions(
                Submit('save', 'Salvar', css_class="btn-primary btn-sm"),
                # Submit('save', 'Salvar e Continuar Editando', css_class="btn-primary btn-sm"),
                *fields,
                cancel,
                css_class=css_class)
        ])
    elif acao == ACAO_WORKFLOW_APPROVE:
        form.helper.layout.extend([
            FormActions(
                Submit('save', 'Aprovar', css_class="btn-primary btn-sm"),
                Submit('save', 'Rejeitar', css_class="btn-danger btn-sm"),
                cancel,
                css_class=css_class)
        ])
    elif acao == ACAO_WORKFLOW_RATIFY:
        form.helper.layout.extend([
            FormActions(
                Submit('save', 'Salvar e Continuar Editando', css_class="btn-primary btn-sm"),
                Submit('save', 'Homologar e Concluir', css_class="btn-danger btn-sm"),
                cancel,
                css_class=css_class)
        ])
    else:
        form.helper.layout.extend([FormActions(cancel, css_class='col-md-11 text-right')])
    return form


def commonRender(request, template_name, dictionary):
    """
    Executa o render do template normal para html ou se a requisição é Ajax, então executa separadamente cada parte para JSON
    """
    dic = dictionary.copy()
    goto = dic.get('goto', 'index')
    form = dic.get('form', None)
    try:
        url = get_goto_url(form.instance if form else None, goto)
        dic.update({'goto': url})
        linkCancel = "window.location.href='#%s'" % url
    except Exception as e:  # NOQA
        linkCancel = "window.location.href='#%s'" % goto

    try:
        ctx = RequestContext(request, dic)
        ctx.update({'ajax': request.is_ajax()})
    except Exception as e:
        ctx = Context(dic)

    ctx.update({'linkCancel': linkCancel})
    # ctx = {k: v for d in ctx for k, v in d.items() if d}
    ctx = ctx.flatten()

    if dic.get('acao', ACAO_VIEW) == ACAO_EMAIL:
        html = render_block_to_string(template_name, "content", context=ctx)
        return HttpResponse(html)

    if request.is_ajax():
        title = render_block_to_string(template_name, "title_html", context=ctx)
        html = render_block_to_string(template_name, "content", context=ctx)
        html = re.sub('<link(.*?)/>', '', html)
        html = re.sub('<script type="text/javascript" src=(.*?)</script>', '', html)

        script = render_block_to_string(template_name, "extrajavascript", context=ctx)
        dump = {'title': title, 'html': html, 'extrajavascript': script, 'goto': goto,
                'form_errors': dic.get('form_errors'), 'formset_errors': dic.get('formset_errors'), }

        return HttpResponse(json.dumps(dump), content_type='application/json')

    return render(request, template_name, ctx)


def commonProcess(form, formset, request, acao, goto, process_name=None, workitem=None,
                  extrajavascript=''):
    # print('commonProcess')
    regs = 10
    if acao in (ACAO_ADD, ACAO_EDIT, ACAO_WORKFLOW_START, ACAO_WORKFLOW_TO_APPROVE,
                ACAO_WORKFLOW_APPROVE, ACAO_WORKFLOW_RATIFY):
        # from django.db import transaction
        obj = None
        # Não faz o try pois as exceptions serão tratadas na view, para que os erros sejam mostrados
        with transaction.atomic():
            try:
                obj = form.save()
            except Exception as e:
                print(e)
                raise e
            if formset:
                if isinstance(formset, forms.formsets.BaseFormSet):
                    formset.save()
                else:
                    # Senão, é list de formsets
                    for d in formset:
                        if d['formset']:
                            d['formset'].save()
            # Ainda dentro da transaction.atomic, faz o tratamento do start do processo ou resolve o próximo
            WorkflowProcessTreatment.run(process_name=process_name, request=request, obj=obj, acao=acao,
                                         workitem=workitem)

    elif acao == ACAO_DELETE:
        try:
            form.instance.delete()
        except Exception as e:
            if hasattr(e, 'protected_objects') and e.protected_objects:
                itens = []
                for item in e.protected_objects[:regs]:
                    itens.append({'msg': '{}: {}'.format(item._meta.model._meta.verbose_name.title(), item.__str__())})
                return JsonResponse({'msg': [{'type': 'danger',
                                              'msg': 'Desculpe, mas há {} registro(s) dependente(s) desse {}:'.format(
                                                  len(e.protected_objects),
                                                  form._meta.model._meta.verbose_name.title()),
                                              'itens': itens,
                                              'total': len(e.protected_objects) - regs}, ],
                                     'goto': request.get_full_path()})
            else:
                return JsonResponse({'msg': [{'type': 'danger',
                                              'msg': 'Desculpe, mas houve erro na exclusão {}:'.format(e)}],
                                     'goto': request.get_full_path()})

    return JsonResponse({'goto': goto,
                         'extrajavascript': extrajavascript if request.POST else None}) if request.is_ajax() else redirect(
        goto)


def commom_detail_handler(clsMaster, formInlineDetail, can_delete=True, isTree=False):
    # fs = []
    detail = []

    if formInlineDetail:
        if isinstance(formInlineDetail, list):
            for f in formInlineDetail:
                detail.append({'prefix': formInlineDetail.index(f), 'clsDetail': f._meta.model, 'formInlineDetail': f})
        else:
            if hasattr(formInlineDetail, '_meta'):
                clsDetail = formInlineDetail._meta.model
            elif hasattr(formInlineDetail, 'Meta'):
                clsDetail = formInlineDetail.Meta.model
            else:
                clsDetail = formInlineDetail.form.Meta.model
            detail = [{'prefix': '', 'clsDetail': clsDetail, 'formInlineDetail': formInlineDetail}]

        if isinstance(isTree, list):
            for i, d in enumerate(detail):
                d['isTree'] = isTree[i]
        else:
            detail[0]['isTree'] = isTree

        for d in detail:
            d['tituloDetail'] = d['clsDetail']._meta.verbose_name.title()
            # forms = django.forms
            d['Detail'] = (
                d['clsDetail'] if d['isTree'] else forms.inlineformset_factory(parent_model=clsMaster,
                                                                               model=d['clsDetail'],
                                                                               form=d['formInlineDetail'],
                                                                               extra=0, min_num=0,
                                                                               can_delete=can_delete)) if issubclass(
                d['formInlineDetail'], forms.BaseModelForm) else d['formInlineDetail']
    # return fs, detail
    return detail


@login_required
def commonCadastro(request, acao=ACAO_VIEW, formModel=None, **kwargs):
    """
    Cadastro genérico.
        Parâmetros são:
            pk: chave principal
            acao: common_forms.ACAO_ADD, common_forms.ACAO_EDIT ou common_forms.ACAO_DELETE
            formModel: form de cadastro do Model
            goto: nome da url para onde será redirecionado após submmit
            template_name: nome do template a ser usado, default o template padrão
    """
    upload_field = kwargs.get('upload_field', None)

    goto = kwargs.get('goto', 'index')
    formInlineDetail = get_class(kwargs.get('formInlineDetail', None))
    pk = kwargs.get('pk', None)
    template_name = kwargs.get('template_name', 'cadastroPadraoUpload.html' if upload_field else 'cadastroPadrao.html')
    # can_add = kwargs.get('can_add', True)
    can_edit = kwargs.get('can_edit', True)
    if not can_edit and acao == ACAO_EDIT:
        acao = ACAO_VIEW
    can_delete = kwargs.get('can_delete', True)
    configuraButtons = kwargs.get('configuraButtons', True)
    extrajavascript = kwargs.get('extrajavascript', '')
    permissions = kwargs.get('permissions', None)
    isTree = kwargs.get('isTree', False)
    idTree = kwargs.get('idTree', 'masterTreeManager')
    acaoURL = kwargs.get('acaoURL', None)
    dataUrl = kwargs.get('dataUrl', None)
    updateParent = kwargs.get('updateParent', None)
    dictionary = kwargs.get('dictionary', {})
    workitem = kwargs.get('workitem', None)

    formM = get_class(formModel)

    clsModel = formM._meta.model
    titulo = clsModel._meta.verbose_name.title()

    if pk and acao not in (ACAO_ADD, ACAO_REPORT, ACAO_WORKFLOW_START):
        mymodel = get_object_or_404(clsModel, pk=pk)
        titulo = '{0} - {1}'.format(titulo, mymodel.__str__())
    else:
        mymodel = clsModel()

    has_permission(request=request, model=clsModel, acao=acao, permissions=permissions, instance=mymodel)

    form_errors = None
    formset_errors = None

    pref = 'nested-' + clsModel._meta.label_lower.replace('.', '-')

    dataTreeURL = dataUrl % pk if dataUrl and pk else ""

    detail = commom_detail_handler(clsMaster=clsModel, formInlineDetail=formInlineDetail, can_delete=can_delete,
                                   isTree=isTree)

    script = formM.extrajavascript(instance=mymodel)
    extrajavascript = "\n".join([extrajavascript, script])

    if workitem:
        # disableMe vem da configuração da atividade
        disableMe = not workitem.activity.enabled
        readonly = ((workitem.status == WorkItem.STATUS_CONCLUDED and acao != ACAO_WORKFLOW_RATIFY)
                    or workitem.activity.readonly)
        if (acao == ACAO_WORKFLOW_RATIFY) and (request.method == 'POST'):
            # Força close do Tab e ignora extrajavascript configurado
            script = 'ftltabs.trigger("closeTab", "Workflow");'
        else:
            # Javascript para buscar se há formset com classe disableMe e faz o disable (inclusão de andamento)
            script = 'configuraCampos("%s" == "True", "%s" == "True");' % (disableMe, readonly)
        extrajavascript = "\n".join([extrajavascript, script])

        # Se status é concluído então não pode inserir nem deletar
        ok = (workitem.instance.status != ProcessInstance.STATUS_CONCLUDED)
        # Também não pode se a activity for readonly
        ok = ok and (not workitem.activity.readonly)
        # can_add &= ok
    else:
        # Prevenção contra adulteração:
        #   para evitar que alguém use uma tela onde não tem permissão de gravação e force um post
        disableMe = dictionary.get('disableMe', False)
        ok = acao not in [ACAO_VIEW, ACAO_EMAIL, ACAO_REPORT, ACAO_REPORT_EXPORT, ]
        if acao == ACAO_VIEW:
            extrajavascript = "\n".join([extrajavascript,
                                         'configuraCampos("%s" == "True", "%s" == "True");' % (disableMe, disableMe)])

    if request.method == 'POST' and ok:
        form = formM(request.POST, request.FILES, instance=mymodel, acao=acao, prefix="main")
        for d in detail:
            d['formset'] = None if d['isTree'] else d['Detail'](request.POST, request.FILES, instance=mymodel,
                                                                prefix=pref + d['prefix'])
        # Cria campo detail no form master para posterior validação do form e dos formset em conjunto quando há dependência.
        # Exemplo, a soma dos percentuais de participação dos proprietários num contrato de adm deve ser 100%
        form.detail = detail
        # como form_tag é variável de classe, tem que forçar para ter <form na geração do html
        form.helper.form_tag = True

        if all(True if d['isTree'] else d['formset'].is_valid() for d in detail) and form.is_valid():
            if acao == ACAO_WORKFLOW_START:
                process_name = form.process_name()
                Process.objects.check_can_start(process_name=process_name, user=request.user)
            else:
                process_name = None
            if acao == ACAO_ADD and upload_field:
                files = request.FILES.getlist(f'{form.prefix}-{upload_field}')
                for f in files[:-1]:
                    fields = model_to_dict(form.instance, exclude=['id'])
                    fields.update({upload_field: f})
                    new_instance = clsModel.objects.create(**fields)
                    # file_instance = clsModel(**fields)
                    # file_instance.save()

            return commonProcess(form=form, formset=detail, request=request, acao=acao,
                                 goto=get_goto_url(form.instance, goto),
                                 process_name=process_name, workitem=workitem, extrajavascript=extrajavascript)
        else:
            form_errors = form.errors
            errors = []

            for d in detail:
                errors.append([] if d['isTree'] else d['formset'].errors)
            # Flattening errors, transforma várias listas de erros em um única lista
            formset_errors = list(itertools.chain(*errors))
            # context['formset_errors'] = formset_errors
            messages.error(request, mark_safe('Erro no processamento'), fail_silently=True)
    else:
        form = formM(instance=mymodel, prefix="main", acao=acao)
        if acao in [ACAO_VIEW, ACAO_EXEC]:
            for i in form.fields:
                form.fields[i].disabled = True
        for d in detail:
            d['formset'] = d['formInlineDetail'] if d['isTree'] else d['Detail'](instance=mymodel,
                                                                                 prefix=pref + d['prefix'])
    if configuraButtons:
        configuraButtonsNoForm(form=form, acao=acao, goto=goto, workitem=workitem)

    # monta modal do help do workflow
    # print(idTree, pk, acao, acaoURL)
    if idTree and pk and acao and acaoURL and updateParent:
        # extrajavascriptTree = ("""ftl_form_modal = riot.mount('div#ftl-form-modal', 'ftl-form-modal', {
        #   'modal': {isvisible: false, contextmenu: false, idtree: '%s'},
        #   'data': {pk: %s, action: %s, acaoURL: '%s', updateParent: '%s', modaltitle: '%s'},
        # })
        # """ % (idTree, pk, acao, acaoURL, reverse(updateParent), mymodel.__str__()))
        extrajavascriptTree = ("""$('#{0}').attr('data-url','{1}');
        ftl_form_modal = riot.mount('div#ftl-form-modal', 'ftl-form-modal', {{
          'modal': {{isvisible: false, contextmenu: false, idtree: '{0}'}},
          'data': {{pk: {2}, action: {3}, acaoURL: '{4}', updateParent: '{5}', modaltitle: '{6}'}},
        }});
        """.format(idTree, dataTreeURL, pk, acao, acaoURL, reverse(updateParent), mymodel.__str__()))
        extrajavascript = "\n".join([extrajavascript, extrajavascriptTree])
    # else:
    #     extrajavascriptTree = None

    dictionary.update(
        {'empresa': emp, 'goto': goto, 'title': titulo, "form": form, 'form_errors': form_errors, "detail": detail,
         # "can_add": can_add, "delecao": (acao == ACAO_DELETE),
         'formset_errors': formset_errors, "idTree": idTree, "pk": pk, "isTree": True, "acaoURL": acaoURL, "acao": acao,
         "dataUrl": dataTreeURL, "updateParent": reverse(updateParent) if updateParent else None,
         "extrajavascript": extrajavascript})  # if extrajavascript else extrajavascriptTree})

    # template_name = 'cadastroMasterDetail.html'

    return commonRender(request, template_name, dictionary)


@login_required
def commonListaTable(request, model=None, *args, **kwargs):
    """
    Lista padrão no formato tabela.
        Parâmetros são:
            model: form de cadastro do Model Master
            queryset: queryset para seleção dos registros a serem listados. Pode ser function para tratar request
            template_name: nome do template a ser usado, default o template padrão de tabela
            tableScript: script a ser injetado dinamicamente no html para tratamento da tabela (totalização de campos, etc.)
    """
    queryset = kwargs.get('queryset', None)
    goto = kwargs.get('goto', 'index')
    template_name = kwargs.get('template_name', "table.html")
    tableScript = kwargs.get('tableScript', None)
    referencia = kwargs.get('referencia', None)
    dictionary = kwargs.get('dictionary', None)
    permissions = kwargs.get('permissions', None)
    data = kwargs.get('data', None)
    title = kwargs.get('title', None)

    # queryset passou a ser opcional para filtrar um table, porque ele não é usado num ajax
    # foi feita uma alteração para que o queryset seja colocado no Meta do form
    # queryset pode ser uma função, um queryset ou uma expressão para eval
    # TODO 2020-03-07: Excluir parâmetro queryset de commonListaTable, pois passou a ser usado no Meta do form.
    #                  Só não foi excluído ainda porque workflow usa esse parâmetro para filtrar e terá que ter revisao.
    if queryset is None and model.opts.queryset is not None:
        queryset_local = model.opts.queryset
    else:
        queryset_local = queryset

    if queryset_local is not None:
        if callable(queryset_local):
            objetos = model(queryset_local(request))
        else:
            objetos = model(queryset_local)
    else:
        if model:
            if data:
                objetos = model(data(request))
            else:
                objetos = model()
        else:
            return "z"
    # objetos = model.queryset.exclude(codtaxa__gte =10000)
    # objetos = objetos.exclude(codtaxa__gte=10000).order_by('codtaxa')
    clsTable = model.opts.model
    if clsTable:
        title = clsTable._meta.verbose_name.title()
    # token =  Token.objects.get(user=request.user)

    has_permission(request=request, model=clsTable, acao=ACAO_VIEW, permissions=permissions)

    dic = dictionary

    if dic is None:
        dic = {}

    extrajavascript = mark_safe(model.extrajavascript())

    dic.update({'empresa': emp, 'goto': goto, 'objetos': objetos, 'title': title, 'tableScript': tableScript,
                'referencia': referencia, "extrajavascript": extrajavascript,
                # 'queryset': queryset,
                })

    # update id of datatables to random name
    model.opts.id = get_random_string(length=10)

    return commonRender(request, template_name, dic)


def commonRelatorioTable(model=None, queryset=None, template_name="table.html", tableScript=None, extrajavascript='',
                         dictionary=None):
    """
    Lista padrão no formato tabela.
        Parâmetros são:
            model: form de cadastro do Model Master
            queryset: queryset para seleção dos registros a serem listados
            template_name: nome do template a ser usado, default o template padrão de tabela
            tableScript: script a ser injetado dinamicamente no html para tratamento da tabela (totalização de campos, etc.)
    """
    if queryset:
        objetos = model(queryset)
    else:
        if model:
            objetos = model()
        else:
            return "z"

    clsTable = model.opts.model
    titulo = clsTable._meta.verbose_name.title()

    dic = dictionary

    if dic is None:
        dic = {}

    dic.update({'empresa': emp, 'objetos': objetos, 'title': titulo, 'tableScript': tableScript,
                'extrajavascript': extrajavascript})

    return commonRender(request=None, template_name=template_name, dictionary=dic)


# Autenticação
# @csrf_protect
def loginX(request, template_name='login.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           authentication_form=AuthenticationForm,
           extra_context=None, redirect_authenticated_user=False):
    return LoginView.as_view(
        template_name=template_name,
        redirect_field_name=redirect_field_name,
        form_class=authentication_form,
        extra_context=extra_context,
        redirect_authenticated_user=redirect_authenticated_user,
    )(request)


def logoutX(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginX'))


def include_CRUD(name, table=None, form=None, *args, **kwargs):
    add = kwargs.get('add', True)
    edit = kwargs.get('edit', True)

    extrajavascript = kwargs.get('extrajavascript', '')
    goto = kwargs.get('goto', name)

    view_cadastro = kwargs.get('view_cadastro', commonCadastro)
    view_table = kwargs.get('view_table', commonListaTable)

    configuraButtons = kwargs.get('configuraButtons', True)
    disableMe = kwargs.get('disableMe', True)

    upload_field = kwargs.get('upload_field', None)

    # Tree
    isTree = kwargs.get('isTree', False)
    idTree = kwargs.get('idTree', 'masterTreeManager')
    acaoURL = kwargs.get('acaoURL', None)
    dataUrl = kwargs.get('dataUrl', None)
    permissions = kwargs.get('permissions', None)
    updateParent = kwargs.get('updateParent', None)

    dic = {'formModel': form, 'goto': goto, 'extrajavascript': extrajavascript,
           'configuraButtons': configuraButtons, 'disableMe': disableMe,
           'isTree': isTree, 'idTree': idTree, 'acaoURL': acaoURL, 'dataUrl': dataUrl, 'updateParent': updateParent}

    if permissions:
        dic.update({'permissions': permissions})

    if upload_field:
        dic.update({'upload_field': upload_field})

    dic_add = dic.copy()
    dic_add.update({'acao': ACAO_ADD})

    urls = []

    if table:
        urls.extend([
            path('{0}/'.format(name), view_table, {'model': table}, name=name)
        ])
    if add:
        urls.extend([
            path('{0}/add/'.format(name), view_cadastro, dic_add, name="{0}Add".format(name)),
        ])
    if edit:
        urls.extend([
            path('{0}/<pk>/<str:acao>/'.format(name), view_cadastro, dic, name="{0}EditDelete".format(name)),
        ])
    return urls


@login_required
def relatorio(request, *args, **kwargs):
    """
    Report genérico.
        Parâmetros são:
            formRel: form do filtro do relatório
            # model: form dos dados do relatório
            goto: nome da url para onde será redirecionado após submit
            report_name: caminho e nome do relatório no servidor Jasper (/Imobiliar/Relatorios/Razao_por_Periodo)
            fields: campos adicionais que serão passado para a view de report
            titulo: título do relatório
            template_name: nome do template a ser usado para entrada de dados do relatório, default é cadastroPadrao.html
            # template_list: nome do template a ser usado para exibição do relatório, default é table.html
            template_report: nome do template a ser usado para exibição de relatório, default é report.html
    """
    formRel = kwargs.pop('formRel', PeriodoForm)
    # model = kwargs.pop('model', None)
    goto = kwargs.pop('goto', 'index')
    report_name = kwargs.pop('report_name', None)
    fields = kwargs.pop('fields', [])
    titulo = kwargs.pop('titulo', 'Relatório')

    template_name = kwargs.pop('template_name', 'cadastroPadrao.html')
    # template_list = kwargs.pop('template_list', 'table.html')
    template_report = kwargs.pop('template_report', 'report.html')

    home = 'index'

    configuraButtons = True

    form = formRel(request.POST or None)  # , request.FILES or None) #File uploads
    form_errors = None

    # form.helper.form_tag = True # como é variável de classe, tem que forçar para ter <form na geração do html

    if request.method == 'POST':
        if form.is_valid():
            dataini = form.cleaned_data['dataini']
            datafin = form.cleaned_data['datafin']
            # dataini = datetime(dataini.year,dataini.month,dataini.day,tzinfo=utc)
            # datafin = datetime(datafin.year,datafin.month,datafin.day, 23, 59, 59,tzinfo=utc)
            params = {'year_ini': dataini.year, 'month_ini': dataini.month, 'day_ini': dataini.day,
                      'year_fin': datafin.year, 'month_fin': datafin.month, 'day_fin': datafin.day, }

            # Prepara campos adicionais
            for f in fields:
                try:
                    params.update({f: form.cleaned_data[f]})
                except:
                    params.update({f: request.session.get(f, None)})

            if request.POST['save'] == 'Consultar' and redirect:
                params.update({'acao': ACAO_REPORT})
                url = reverse(goto, kwargs=params)
                return commonRender(request, template_report,
                                    {'empresa': emp, 'title': titulo, 'goto': url})
                # url = reverse(goto, **params)
                # return HttpResponseRedirect(url)
                # return redirect(goto, **params)
            elif request.POST['save'] == 'Exportar' and report_name:
                # dataini = dataini.isoformat()
                # datafin = datafin.isoformat()
                params.update({'acao': ACAO_REPORT_EXPORT})
                relatorio = montaURLjasperReport(report_name=report_name, params=params)
                return commonRender(request, template_report,
                                    {'empresa': emp, 'title': titulo, 'goto': goto, 'form_errors': form.errors,
                                     'relatorio': relatorio})
            else:
                pass
            return redirect('periodo')
        else:
            context = RequestContext(request)
            # context['form_errors'] = form.errors
            form_errors = form.errors

    if configuraButtons:
        configuraButtonsNoForm(form, ACAO_REPORT, goto=home)
    return commonRender(request, template_name,
                        {'empresa': emp, 'title': titulo, 'goto': home, 'form': form, 'form_errors': form_errors})


@login_required
def versionViewCompare(request, pk=None, *args, **kwargs):
    """ Tratamento especial de view de send/receive json """
    template_name = kwargs.get('template_name', 'reversion-compare/versionCompare.html')
    titulo = kwargs.get('titulo', 'Comparar Versões')
    goto = kwargs.get('goto', 'index')
    permissions = kwargs.get('permissions', None)
    name = None

    has_permission(request, model=Version, acao=ACAO_VIEW, permissions=permissions)
    # if not has_permission(request, model=Version, acao=ACAO_VIEW, permissions=permissions):
    #     return http.HttpResponseForbidden()

    compare_data = []
    has_unfollowed_fields = False

    if pk:
        v_new = Version.objects.get(pk=pk)
        obj = v_new.object
        v_old = Version.objects.get_for_object(obj).filter(revision__id__lt=v_new.revision.id).first()

        if v_old:
            # v_new.revision.version_set.all()[4]
            compare_mixin = obj.compare_version if hasattr(obj, 'compare_version') else CompareVersion
            compare_exclude = obj.compare_exclude() if hasattr(obj, 'compare_exclude') else None
            cmp = compare_mixin(compare_exclude=compare_exclude)
            compare_data, has_unfollowed_fields = cmp.compare(obj, v_old, v_new)

        # titulo = v_new.object._meta.verbose_name
        try:
            titulo = str(v_new)
            name = obj._meta.verbose_name
            goto = obj.get_absolute_url()
        except Exception as e:
            pass

    # Tratamentos das FKs follweds
    compare_data_fk = []
    diff = ''
    ctx = {'empresa': emp, 'title': titulo, 'goto': goto, 'form': None, }
    fkv_all_new = v_new.revision.version_set.all().exclude(object_id=v_new.object_id,
                                                           content_type=v_new.content_type)  # Versions de FK
    if v_old:
        fkv_all_old = v_old.revision.version_set.all().exclude(object_id=v_old.object_id,
                                                               content_type=v_old.content_type)  # Versions de FK
    else:
        fkv_all_old = Version.objects.none()
    # procura pelos que existem no new
    for fkv_new in fkv_all_new:
        fkv_old = fkv_all_old.filter(content_type=fkv_new.content_type, object_id=fkv_new.object_id).first()
        # Se existe nos dois então compara
        if fkv_old:
            compare_data_fk_i, has_unfollowed_fields_fk = cmp.compare(fkv_new.object, fkv_old, fkv_new)
            # Render diff
            ctx.update({'v_new': fkv_new, 'v_old': fkv_old, 'name': name,
                        'compare_data': compare_data_fk_i, 'has_unfollowed_fields': has_unfollowed_fields_fk, })
            diff += render_block_to_string(template_name, "content", context=ctx)
            # Acumula para mostrar de uma vez todas as FKs
            compare_data_fk += [{'v_new': fkv_new, 'v_old': fkv_old,
                                 'compare_data': compare_data_fk_i,
                                 'has_unfollowed_fields': has_unfollowed_fields_fk, }]
        else:
            # É novo, então mostra que foi inserido
            pass

    # procura pelos que só existem no f_old
    # procura pelos que só existem no f_new
    # fkv_old = [i for i in fv_old if i.object != obj]  # Versions de FK
    # fkv_new = [i for i in fv_new if i.object != obj]  # Versions de FK
    a = [i.pk for i in fkv_all_old]
    b = [i.pk for i in fkv_all_new]
    f_union = fkv_all_old.union(fkv_all_new)
    f_intersection = fkv_all_old.intersection(fkv_all_new)
    f_difference = fkv_all_old.difference(fkv_all_new)
    # k_union = set(v_old).union(set(fkv_new))
    # k_intersection = set(fkv_old).intersection(set(fkv_new))
    # k_difference = set(fkv_old).difference(set(fkv_new))

    ctx.update({'v_new': v_new, 'v_old': v_old, 'name': name,
                'compare_data': compare_data, 'has_unfollowed_fields': has_unfollowed_fields,
                'compare_data_fk': compare_data_fk})
    return commonRender(request, template_name, ctx)


@login_required
def executeUseCase(request, pk=None, formModel=None, use_case=None, goto='', *args, **kwargs):
    """
    View para confirmação de execução de um use case

    :param formModel: form que irá ser mostrado, passa parâmetro com a mensagem que será mostrada na tela
    :param use_case: use case
    :param goto: pra onde vai após o post
    :param goto_error: pra onde vai após o post e há erro, default = goto
    :param permissions: list de permissões que o usuário deve ter para executar o use case
    :param msg(optional): mensagem que poderá aparecer na tela com uma observação qualquer
    """
    clsModel = formModel._meta.model
    titulo = clsModel._meta.verbose_name.title()
    acao = kwargs.get('acao', ACAO_EXEC)
    permissions = kwargs.get('permissions', None)

    msg = kwargs.get('msg', 'ERROR')
    goto_error = kwargs.get('goto_error', goto)

    mymodel = get_object_or_404(clsModel, pk=pk)
    form = formModel(request.POST or None, instance=mymodel, msg=msg)
    titulo = '{0} - {1}'.format(titulo, mymodel.__str__())

    has_permission(request=request, model=clsModel, acao=acao, permissions=permissions, instance=mymodel)

    form.helper.form_tag = True  # como é variável de classe, tem que forçar para ter <form na geração do html
    form_errors = None
    extrajavascript = kwargs.get('extrajavascript', '')

    if request.method == 'POST':
        if form.is_valid():
            if acao == ACAO_EXEC:
                # Publica versão do documento atual
                with transaction.atomic():
                    result = use_case.run(obj=mymodel)
                    if result.errors.has_error:
                        transaction.set_rollback(True)
                        messages.error(request, mark_safe('Erro na Execução'), fail_silently=True)
                        text = result.errors.as_alert()
                        extrajavascript = 'riot.mount("ftl-error-message", {});'.format(text).replace('\n', '')
                        goto = reverse(goto_error, args=([form.instance.pk]))
                    else:
                        # Se é necessário fazer um redirect para outro local, mas é complexo,
                        # então pode retornar um dict, onde um dos elementos seria o "goto"
                        if isinstance(result.return_value, dict) and result.return_value.get('goto', None):
                            goto = result.return_value.get('goto', None)
                        else:
                            goto = get_goto_url(result.return_value, goto)
                        # Força o fechamento do tab associado a execução do use case
                        extrajavascript += "closeActiveTab();"
        else:
            form_errors = form.errors
            text = ''
            for i in form_errors:
                txt = ', '.join([str(j.message) for j in form_errors[i].data])
                text += 'Campo {}: {}'.format(i.capitalize(), txt)
                if len(form_errors) > 1:
                    text += ', '
            errors = []
            mnt = 'riot.mount("ftl-error-message", {{messages: [{{type: \'error\', msg: \'{}: {}\'}}, ]}});'
            extrajavascript = mnt.format('Erro no Caderno de Treinamento', mark_safe(text))

            messages.error(request, mark_safe('Erro no processamento'), fail_silently=True)
    else:
        for i in form.fields:
            form.fields[i].disabled = True

    template_name = 'cadastroPadrao.html'

    configuraButtonsNoForm(form, acao, goto)

    dictionary = {'goto': goto, 'title': titulo, "form": form, "pk": pk, 'form_errors': form_errors,
                  'messages': messages, 'extrajavascript': extrajavascript}

    return commonRender(request, template_name, dictionary)


@login_required
def executeUseCaseForm(request, form=None, use_case=None, goto='', *args, **kwargs):
    """
    View para confirmação de execução de um use case QUE NÃO TEM MODEL ASSOCIADO

    :param form: form que irá ser mostrado, passa parâmetro com a mensagem que será mostrada na tela
    :param use_case: use case
    :param goto: pra onde vai após o post
    :param goto_error: pra onde vai após o post e há erro, default = goto
    :param permissions: list de permissões que o usuário deve ter para executar o use case
    :param pk(optional): pk a ser tratada pelo use case
    :param msg(optional): mensagem que poderá aparecer na tela com uma observação qualquer
    """
    permissions = kwargs.get('permissions', None)

    pk = kwargs.get('pk', None)
    msg = kwargs.get('msg', 'ERROR')
    goto_error = kwargs.get('goto_error', goto)
    titulo = kwargs.get('titulo', '')
    model_permission = kwargs.get('model_permission', '')

    form = form(request.POST or None, msg=msg, pk=pk)

    if model_permission:
        has_permission(request=request, model=model_permission, acao=ACAO_EXEC, permissions=permissions)

    form.helper.form_tag = True  # como é variável de classe, tem que forçar para ter <form na geração do html
    form_errors = None
    extrajavascript = kwargs.get('extrajavascript', '')

    messages = []

    if request.method == 'POST':
        if form.is_valid():
            # Publica versão do documento atual
            with transaction.atomic():
                result = use_case.run(form=form)
                if result.errors.has_error:
                    transaction.set_rollback(True)
                    messages.error(request, mark_safe('Erro na Execução'), fail_silently=True)
                    text = result.errors.as_alert()
                    extrajavascript = 'riot.mount("ftl-error-message", {});'.format(text).replace('\n', '')
                    goto = reverse(goto_error, args=([pk]))
                else:
                    # Se é necessário fazer um redirect para outro local, mas é complexo,
                    # então pode retornar um dict, onde um dos elementos seria o "goto"
                    if isinstance(result.return_value, dict) and result.return_value.get('goto', None):
                        goto = result.return_value.get('goto', None)
                    else:
                        goto = get_goto_url(result.return_value, goto)
                    # Força o fechamento do tab associado a execução do use case
                    extrajavascript += "closeActiveTab();"
        else:
            form_errors = form.errors
            text = ''
            for i in form_errors:
                txt = ', '.join([str(j.message) for j in form_errors[i].data])
                text += 'Campo {}: {}'.format(i.capitalize(), txt)
                if len(form_errors) > 1:
                    text += ', '
            errors = []
            mnt = 'riot.mount("ftl-error-message", {{messages: [{{type: \'error\', msg: \'{}: {}\'}}, ]}});'
            extrajavascript = mnt.format('Erro no Caderno de Treinamento', mark_safe(text))

            messages.error(request, mark_safe('Erro no processamento'), fail_silently=True)

    template_name = 'cadastroPadrao.html'

    configuraButtonsNoForm(form, ACAO_EXEC, goto)

    dictionary = {'goto': goto, 'title': titulo, "form": form, 'form_errors': form_errors,
                  'messages': messages, 'extrajavascript': extrajavascript}

    return commonRender(request, template_name, dictionary)


def rotas_ajax(request, *args, **kwargs):
    """ Lista todas as rotas configuradas para o base.html """
    rotas = []
    try:
        for i in Rota.objects.all():
            rotas.append({'rota': i.url, 'nome': i.nome, 'url': i.url, 'reload': i.reload})
    except Exception as e:
        pass

    return JsonResponse(rotas, safe=False)


@login_required
def simple_html_page(request, template):
    # return JsonResponse(json.dumps(schedule))
    ctx = {}
    return commonRender(request, template, ctx)


@login_required
def download_users_email(request):
    # Só podem fazer download da lista de emails de usuários quem é superuser
    if not request.user.is_superuser:
        raise PermissionDenied
    file_name = export_users()
    file_open = open(file_name, 'rb')
    response = FileResponse(file_open, as_attachment=True, filename='users.cvs')
    return response
