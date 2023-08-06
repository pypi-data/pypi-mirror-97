import datetime
import decimal

from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest

from . import validators


class FieldBase(object):
    def __init__(self, name=None, **kwargs):
        self.name = name
        self._add_validators(**kwargs)

    def _add_validators(self, **kwargs):
        self.required = kwargs.pop('required', True)
        self.blank = kwargs.pop('blank', False)
        self.saved = kwargs.pop('saved', False)
        self.has_default = 'default' in kwargs
        self.default = kwargs.pop('default', None)
        self.saved = kwargs.pop('saved', False)
        self.instance_of = kwargs.pop('instance_of', None)

    @property
    def validators(self):
        _ = []
        if self.required:
            _.append(validators.RequiredValidator())
        if not self.blank:
            _.append(validators.NotBlankValidator())
        if self.saved:
            _.append(validators.SavedObjectValidator())
        if self.instance_of:
            _.append(validators.InstanceValidator(self.instance_of, required=self.required))
        if self.extra_validators:
            _.append(self.extra_validators)
        return _

    @property
    def extra_validators(self):
        raise NotImplementedError("implement in subclass")


def build_field_for(name, type_obj):
    """Shortcut to define a field for a primitive. """

    class DynamicField(FieldBase):
        @property
        def extra_validators(self):
            return validators.InstanceValidator(type_obj, required=self.required)

    DynamicField.__name__ = name
    return DynamicField


ObjectField = build_field_for("ObjectField", object)
BooleanField = build_field_for("BooleanField", bool)
CharField = build_field_for("CharField", str)
StringField = build_field_for("StringField", str)
DictField = build_field_for("DictField", dict)
ListField = build_field_for("ListField", list)
DecimalField = build_field_for("DecimalField", decimal.Decimal)
NumericField = build_field_for("NumericField", (int, float, decimal.Decimal))
IntField = build_field_for("DecimalField", int)
DatetimeField = build_field_for("DatetimeField", datetime.datetime)
DateField = build_field_for("DateField", datetime.date)
UserField = build_field_for("UserField", get_user_model())
RequestField = build_field_for("RequestField", WSGIRequest)


class DuckField(FieldBase):
    """Use this for duck-typing. """

    def __init__(self, instance_of, *args, **kwargs):
        self.instance_of = instance_of
        super().__init__(*args, **kwargs)

    @property
    def extra_validators(self):
        return validators.InstanceValidator(instance_of=self.instance_of, required=self.required)


class StatusField(FieldBase):
    def __init__(self, valid_statuses, *args, **kwargs):
        self.valid_statuses = valid_statuses
        super().__init__(*args, **kwargs)

    @property
    def extra_validators(self):
        return validators.StatusValidator(valid_statuses=self.valid_statuses, required=self.required)
