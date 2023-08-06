#!/usr/bin/env python
# coding: utf-8

from django.db.models import QuerySet
from django.db.models.manager import BaseManager
from django.utils.html import escape
from django.utils.safestring import mark_safe


class Accessor(str):
    """ A string describing a path from one object to another via attribute/index
        accesses. For convenience, the class has an alias `.A` to allow for more concise code.

        Relations are separated by a "." character.
    """
    SEPARATOR = '.'

    def resolve(self, context, quiet=True):
        """
        Return an object described by the accessor by traversing the attributes
        of context.

        """
        try:
            obj = context
            for level in self.levels:
                if isinstance(obj, dict):
                    obj = obj[level]
                elif isinstance(obj, list) or isinstance(obj, tuple):
                    obj = obj[level]
                else:
                    # Quando era para campo que não existia no model, mas tinha função, dava erro no getattr
                    if hasattr(obj, level) and callable(getattr(obj, level)) and not isinstance(getattr(obj, level),
                                                                                                BaseManager):
                        try:
                            obj = getattr(obj, level)()
                        except KeyError:
                            obj = getattr(obj, level)
                    else:
                        # for model field that has choice set
                        # use get_xxx_display to access
                        display = 'get_%s_display' % level
                        obj = getattr(obj, display)() if hasattr(obj, display) else getattr(obj, level)
                    # if callable(getattr(obj, level)):
                    #     try:
                    #         obj = getattr(obj, level)()
                    #     except KeyError:
                    #         obj = getattr(obj, level)
                    # else:
                    #     # for model field that has choice set
                    #     # use get_xxx_display to access
                    #     display = 'get_%s_display' % level
                    #     obj = getattr(obj, display)() if hasattr(obj, display) else getattr(obj, level)
                if not obj:
                    break
            return obj
        except Exception as e:
            print(self)
            print('5')
            print(e)
            if quiet:
                return ''
            else:
                raise e

    @property
    def levels(self):
        if self == '':
            return ()
        return self.split(self.SEPARATOR)


A = Accessor


class AttributesDict(dict):
    """
    A `dict` wrapper to render as HTML element attributes.
    """

    def render(self):
        return mark_safe(' '.join([
            '%s="%s"' % (attr_name, escape(attr))
            for attr_name, attr in self.items()
        ]))


# Retorna um queryset, aceitando como parâmetro tanto uma função como um queryset real
def get_callable_or_not_queryset(request, model, queryset):
    if queryset is not None:
        if callable(queryset):
            q = queryset(request)
        elif isinstance(queryset, QuerySet):
            q = queryset
        else:
            q = eval(queryset)
    else:
        if model:
            q = model.objects.all()
        else:
            return "deu zebra"
    return q
