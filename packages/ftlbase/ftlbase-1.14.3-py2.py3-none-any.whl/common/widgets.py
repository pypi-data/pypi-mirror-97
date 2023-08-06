# -*- coding: utf-8 -*-
from django.forms import Widget, TextInput, CheckboxInput
from django.template.loader import render_to_string


class FormSetWidget(Widget):
    add_text = None  # Usado na descrição do botão de adicionar ou "Adicionar" se None
    formset_class = None  # Classe do formset a ser mostrado
    show_add_button = True  # Se permite adição de inline formset, independente do workflow
    template_name = 'common/formsetfield.html'

    form = None

    def __init__(self, attrs=None):
        if attrs is not None:
            self.template_name = attrs.pop('template', self.template_name)
            # self.related = attrs.pop('related', self.related)
            self.formset_class = attrs.pop('formset_class', self.formset_class)
            self.show_add_button = attrs.pop('show_add_button', self.show_add_button)
            self.add_text = attrs.pop('add_text', self.add_text)
            self.instance = attrs.get('instance', None)
            self.queryset = attrs.get('queryset', None)
        super().__init__(attrs)

    def set_add_button(self, flag):
        """ Habilita ou desabilita botão de adição do formset """
        self.show_add_button = flag

    def get_formset(self, **kwargs):
        return self.formset_class(**kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = self.formset_class(prefix=name)

        can_add = value.instance.can_add if hasattr(value.instance, 'can_add') else True

        return render_to_string(self.template_name,
                                {'form': self.form, 'formset': value, 'show_add_button': self.show_add_button,
                                 'add_text': self.add_text, 'can_add': can_add})

    def value_from_datadict(self, data, files, name):
        """ Lista as chaves primárias do model, igual a fk """
        field_id = '%s-formset-id' % name
        pk = data[field_id]
        # Se é um formset de um formset (beneficiário de uma nova participação,
        # então ainda não foi salva, o campo vem como 'None' (string) em data[field_id])
        if pk == 'None' or pk == '':
            instance = None
        else:
            instance = self.formset_class.fk.related_model.objects.get(pk=pk)
        return self.get_formset(data=data, files=files, instance=instance, prefix=name)


class PolymorphicWidget(FormSetWidget):
    # related = None  # Não sei para que serve!
    template_name = 'common/polymorphic_field.html'

    def get_formset(self, **kwargs):
        self.instance = kwargs.get('instance', None)
        return self.formset_class(**kwargs)

    def value_from_datadict(self, data, files, name):
        """ Lista as chaves primárias do model, igual a fk """
        field_id = '%s-polymorphic-formset-id' % name
        try:
            pk = data[field_id]
        except Exception:
            pk = 'None'
        # Se é um formset de um formset (fiança de um contrato de locação),
        # então ainda não foi salva, o campo vem como 'None' (string) em data[field_id])
        # Insert/Update vai ser tratado em save_m2m
        if pk == 'None':
            instance = None
        else:
            try:
                instance = self.formset_class.fk.related_model.objects.get(pk=pk)
            except Exception:
                try:
                    instance = self.related.objects.get(pk=pk)
                except Exception:
                    instance = self.related.objects.none()

        return self.get_formset(data=data, files=files, instance=instance, prefix=name)


class MoneyWidget(TextInput):
    template_name = 'common/money_field.html'


class PercentWidget(TextInput):
    template_name = "common/percent_field.html"


def sim_nao_check(value):
    return value == 'S'


class SimNaoCheckboxInputWidget(CheckboxInput):
    """ Usado para campos S/N que serão mostrados como checkbox """

    def __init__(self, attrs=None):
        super().__init__(attrs, check_test=sim_nao_check)

    def format_value(self, value):
        """Only return the 'value' attribute if value isn't empty."""
        # if value is True or value is False or value is None or value == '' or value in ['S', 'N']:
        if value is None or value == '' or value in ['S', 'N']:
            return
        return str(value)

    def value_from_datadict(self, data, files, name):
        """ Retorna S ou N """
        if name not in data:
            # A missing value means False because HTML form submission does not
            # send results for unselected checkboxes.
            return 'N'
        value = data.get(name)
        # Translate true and false strings to boolean values.
        values = {'true': 'S', 'false': 'N', 'on': 'S'}
        if isinstance(value, str):
            value = values.get(value.lower(), value)
        return value
