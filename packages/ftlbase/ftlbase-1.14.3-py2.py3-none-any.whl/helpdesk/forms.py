# -*- coding: utf-8 -*-

from crispy_forms.bootstrap import InlineField
from crispy_forms.layout import Layout, Div, Hidden, Submit, HTML, Field
from django.forms import inlineformset_factory, Textarea

from common.fields import FormSetField
from common.forms import CommonModelForm
from common.layout import layout_logusuario, LabelFirstDetail, simple_label_line, ReadonlyField
from common.middleware import get_current_user
from table import Table
from table.columns import Column, ActionColumn
from .models import *


def table_queryset_user_helpdesk(request):
    if request.user.is_staff:
        q = Ticket.objects.all().order_by('-pk')
    else:
        q = Ticket.objects.filter(created_by=request.user).order_by('-pk')
    return q


class SubjectTable(Table):
    """
    Definição de ação: 1 - Add, 2 - Edit, 3 - Delete
    """
    id = Column(field='id')
    description = Column(field='description')
    status = Column(field='status')
    action = ActionColumn(vieweditdelete='subjectEditDelete', chave='pk')

    class Meta:
        model = Subject
        std_button_print = False
        std_button_pdf = False
        std_button_excel = False


class SubjectForm(CommonModelForm):

    def layout(self):
        return Layout(
            Div('description', css_class='col-md-12'),
        )

    class Meta:
        model = Subject
        include_hidden = True
        fields = '__all__'
        # exclude = ['created_by', 'created_at', ] #'subject', 'description', 'status']


class FollowUpInlineForm(CommonModelForm):
    # data_inicial = DateField(label='Data Inicial', required=True)
    # data_termino = DateField(label='Data de Término', required=True)

    def layout(self):
        # pass
        return Layout(
            Div(
                Div(LabelFirstDetail("Andamento"), InlineField('followup'), css_class='col-xs-12 col-md-10'),
                # Div(LabelFirstDetail("Status"), InlineField('status'), css_class='col-xs-6 col-md-1'),
                Div(LabelFirstDetail("Quem"),
                    # HTMLInstance('{html}', parms={'html': 'instance.get_created_by_display()'}),
                    Field('created_by', disabled='disabled'),
                    # Field('created_by', disabled=True),
                    ReadonlyField('created_at'),
                    css_class='col-xs-6 col-md-2'),
                Hidden('ticket', 'value'),
                css_class='row'
            ),
        )

    class Meta:
        model = FollowUp
        include_hidden = True
        fields = '__all__'
        widgets = {
            'followup': Textarea(attrs={'rows': 5, }),  # 'cols':15}),
        }
        # exclude = ('participants',)
        # help_texts = {
        #     'order': None,
        #     'time': None,
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['followup'].disabled = True
            self.fields['created_by'].choices = [(e.id, e.email) for e in [instance.created_by]]
        else:
            self.fields['created_by'].choices = [(e.id, e.email) for e in [get_current_user()]]
            # self.fields['created_by'].disabled = True


followup_form_class = inlineformset_factory(parent_model=Ticket, model=FollowUp, form=FollowUpInlineForm, extra=0,
                                            min_num=0)


class TicketInsertForm(CommonModelForm):

    def layout(self):
        return Layout(
            Div('subject',
                'description',
                css_class='col-md-12'
                ),
            # Div(layout_logusuario, css_class='hidden'),
        )

    class Meta:
        model = Ticket
        include_hidden = True
        fields = '__all__'


class TicketForm(CommonModelForm):
    followups = FormSetField(formset_class=followup_form_class)

    def layout(self):
        onclick = 'window.location.href=#{{goto}}'
        return Layout(
            Div(ReadonlyField('subject'),
                ReadonlyField('description'),
                css_class='col-md-12'
                ),
            # Div(ReadonlyField('status'), ReadonlyField('created_by'), ReadonlyField('created_at'),
            Div(ReadonlyField('status'), css_class='col-xs-12 col-md-4'),
            Div(ReadonlyField('created_by'), css_class='col-xs-12 col-md-4'),
            Div(ReadonlyField('created_at'), css_class='col-xs-12 col-md-4'),
            Div(
                simple_label_line('Andamentos', max_width=100),
                Div(InlineField('followups')), css_class='col-xs-12 col-md-12',
            ),
            # Div(layout_logusuario, css_class='hidden'),
            Div(
                Submit('save', Ticket.TICKET_STATUS_MSG_ENCERRAR),
                Submit('save', Ticket.TICKET_STATUS_MSG_RESPONDER),
                Submit('save', Ticket.TICKET_STATUS_MSG_RETORNAR),
                HTML('<input type="button" name="cancel" value="Cancelar" class="btn btn-cancel btn-sm" '
                     'id="button-id-cancel" onclick="window.location.href=\'#{{goto}}\'">'),
                css_class='col-md-11 text-right buttons-do-form',
            )
        )

    class Meta:
        model = Ticket
        include_hidden = True
        fields = '__all__'
        # exclude = ['created_by', 'created_at', ] #'subject', 'description', 'status']
        widgets = {
            'description': Textarea(attrs={'rows': 5    , }),  # 'cols':15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['subject'].disabled = True
        # self.fields['description'].disabled = True
        is_staff = get_current_user().is_staff
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            not_encerrado = instance.status != Ticket.TICKET_STATUS_ENCERRADO
            button_responder = instance.status in [Ticket.TICKET_STATUS_ABERTO,
                                                   Ticket.TICKET_STATUS_RETORNADO] and not_encerrado and is_staff
            button_retornar = (instance.status == Ticket.TICKET_STATUS_RESPONDIDO or not is_staff) and not_encerrado
        else:
            # Se não tem instance, então desabilita tudo
            not_encerrado = button_responder = button_retornar = False
        self.helper.layout[5][0].field_classes = 'btn-primary btn-sm' if not_encerrado else 'sr-only'
        self.helper.layout[5][1].field_classes = 'btn-primary btn-sm' if button_responder else 'sr-only'
        self.helper.layout[5][2].field_classes = 'btn-warning btn-sm' if button_retornar else 'sr-only'
        if instance.status == Ticket.TICKET_STATUS_ENCERRADO:
            self.fields['followups'].set_add_button(False)


class TicketTable(Table):
    """
    Definição de ação: 1 - Add, 2 - Edit, 3 - Delete
    """
    id = Column(field='id')
    subject = Column(header=u'Assunto', field='subject')
    description = Column(field='description')
    created_by = Column(header='Criado Por', field='created_by')
    status = Column(field='status')
    action = ActionColumn(vieweditdelete='ticketEditDelete', chave='id', can_delete=False)

    class Meta:
        model = Ticket
        queryset = table_queryset_user_helpdesk
        ajax = True
        std_button_print = False
        std_button_pdf = False
        std_button_excel = False

    @staticmethod
    def extrajavascript(*args, **kwargs):
        return "$('#helpdesk_pendente')[0]._tag.trigger('updateContent');"
