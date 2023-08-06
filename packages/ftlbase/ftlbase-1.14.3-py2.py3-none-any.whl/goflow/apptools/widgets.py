# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe

from common.utils import ACAO_WORKFLOW_EDIT, ACAO_VIEW
from goflow.runtime.models import WorkItem, ProcessInstance
from table.columns.modalcolumn import ModalColumn


class WorkflowWhereColumn(ModalColumn):
    def __init__(self, field=None, header=None, goto='workflow_graph', span_text='project-diagram', span_tip='Onde estou?',
                 key='pk', cls='modal-lg', **kwargs):
        super().__init__(field=field, header=header, goto=goto, span_text=span_text, span_tip=span_tip,
                         key=key, cls=cls, **kwargs)


class WorkflowHistoryColumn(ModalColumn):
    def __init__(self, field=None, header=None, goto='workflow_history', span_text='history', span_tip='História',
                 key='pk', cls='modal-lg', acao=ACAO_WORKFLOW_EDIT, **kwargs):
        super().__init__(field=field, header=header, goto=goto, span_text=span_text, span_tip=span_tip, key=key,
                         cls=cls, acao=acao, **kwargs)


class WorkflowColumn(ModalColumn):
    def __init__(self, field=None, header=None, goto='obrigatorio', span_text='obrigatorio', span_tip='obrigatorio',
                 key='pk', cls='modal-lg', acao=ACAO_VIEW, **kwargs):
        super().__init__(field=field, header=header, goto=goto, span_text=span_text, span_tip=span_tip,
                         key=key, cls=cls, acao=acao, **kwargs)

    def render(self, instance):
        part_a = WorkflowWhereColumn(field=self.field, header=self.header).render(instance)
        part_b = WorkflowHistoryColumn(field=self.field, header=self.header).render(instance)

        span_text = 'tasks'
        span_tip = 'Tarefas'
        if hasattr(instance, 'html_to_approve_link'):
            url = '/#' + instance.html_to_approve_link
        elif instance.workitems.last():
            url = '/#' + instance.workitems.last().html_to_approve_link
        else:
            url = '#'
        span = '<i class="far fa-%s" style="font-size:18px;color:#09568d;" data-toggle="tooltip" title="%s"></i>' % (
            span_text, span_tip)
        part_c = mark_safe(u'<a href="%s">%s</a>' % (url, span))

        div = '&nbsp;'

        return part_a + div + part_b + div + part_c + div + div + div + div


class WorkflowColumnCBV(ModalColumn):
    def __init__(self, field=None, header=None, goto='obrigatorio', span_text='obrigatorio', span_tip='obrigatorio',
                 key='pk', cls='modal-lg', acao=ACAO_VIEW, **kwargs):
        super().__init__(field=field, header=header, goto=goto, span_text=span_text, span_tip=span_tip,
                         key=key, cls=cls, acao=acao, **kwargs)

    def render(self, instance):
        if isinstance(instance, ProcessInstance):
            wi = instance.workitems.last()
        else:
            wi = instance.workitem()
        part_a = WorkflowWhereColumn(field=self.field, header=self.header).render(wi)
        part_b = WorkflowHistoryColumn(field=self.field, header=self.header).render(wi)


        span_text = 'tasks'
        span_tip = 'Tarefas'
        if hasattr(instance, 'html_to_approve_link'):
            url = '/#' + instance.html_to_approve_link
        elif wi:
            url = '/#' + wi.html_to_approve_link_cbv
        else:
            url = '#'
        span = '<i class="far fa-%s" style="font-size:18px;color:#09568d;" data-toggle="tooltip" title="%s"></i>' % (
            span_text, span_tip)
        part_c = mark_safe(u'<a href="%s">%s</a>' % (url, span))

        div = '&nbsp;'

        return ((part_a + div) if part_a else '') + ((part_b + div) if part_b else '') + part_c + div + div + div + div
