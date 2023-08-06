#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.html import escape

from table.utils import Accessor
from .base import Column


class LimitStringColumn(Column):

    def __init__(self, field, header=None, size=80, **kwargs):
        self.size = size
        super().__init__(field, header, **kwargs)

    def render(self, obj):
        text = Accessor(self.field).resolve(obj)
        if not bool(text):
            text = ''
        return escape(text[:self.size or None])
