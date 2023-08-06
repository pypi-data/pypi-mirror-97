from crispy_forms.layout import Div, Layout
from django import forms

from common.forms import CommonModelForm
from common.utils import ACAO_VIEW
from mp import models
from mp.models import Preference
from table import Table
from table.columns import Column, ActionColumn, BooleanColumn, FontAwesomeLink
from table.utils import Accessor


class NotificationForm(forms.Form):
    TOPICS = {
        'merchant_order': models.Notification.TOPIC_ORDER,
        'payment': models.Notification.TOPIC_PAYMENT,
    }

    id = forms.CharField()
    topic = forms.ChoiceField(choices=TOPICS.items())


# Usado em VendaTable para saber se coloca a linha red ou não
def red(obj, field):
    return None if obj.paid else 'danger'


linkPoolPreference = [
    FontAwesomeLink(text=u'Procurar Pagamento', viewname='mp:pool_preference', args=(Accessor('id'),'mp:preference',),
                    span_fa='wifi', span_tip='Procurar pagamento no MP', acao=ACAO_VIEW), ]


class PreferenceTable(Table):
    """
    Definição de ação: 1 - Add, 2 - Edit, 3 - Delete
    """
    id = Column(field='id', attrs={'class': red})
    owner = Column(field='owner', attrs={'class': red})
    mp_id = Column(field='mp_id', attrs={'class': red})
    reference = Column(field='reference', attrs={'class': red})
    paid = BooleanColumn(field='paid', attrs={'class': red})
    action = ActionColumn(vieweditdelete='mp:preferenceEditDelete', chave='id', attrs={'class': red},
                          links=linkPoolPreference)

    class Meta:
        model = Preference


class PreferencesForm(CommonModelForm):
    def layout(self):
        return Layout(
            Div('owner', css_class='col-xs-12 col-md-6'),
            Div('mp_id', css_class='col-xs-12 col-md-6'),
            Div('payment_url', css_class='col-xs-12'),
            Div('sandbox_url', css_class='col-xs-12'),
            Div('reference', css_class='col-xs-12 col-md-6'),
            Div('paid', css_class='col-xs-6 col-md-2'),
        )

    class Meta:
        model = Preference
        include_hidden = True
        fields = '__all__'


class PrefTable(Table):
    id = Column(header='Id', field='id')
    date_created = Column(header='Date Created', field='date_created')
    external_reference = Column(header='External Reference', field='external_reference')
    payer_id = Column(header='Payer ID', field='payer_id')
    payer_email = Column(header='Payer Email', field='payer_email')
    product_id = Column(header='Product ID', field='product_id')
    operation_type = Column(header='Operation Type', field='operation_type')
    items = Column(header='Items', field='items')

    class Meta:
        # model = Cupom
        # data = table_queryset_preferences
        pass
