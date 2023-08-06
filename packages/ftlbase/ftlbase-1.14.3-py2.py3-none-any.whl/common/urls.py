# -*- coding: utf-8 -*-
from django.urls import path, include

from . import forms as common_forms, views as common_views

# from . import form
from .model_views import URLGenerator
from .models import Rota

urlpatterns = [
    *common_views.include_CRUD('rota', table=common_forms.RotaTable, form=common_forms.RotaForm),
    path('', include(URLGenerator(Rota).get_urlpatterns())),
    path('rotas/', common_views.rotas_ajax, name='rotas'),
    path('login/', common_views.loginX, name='loginX'),
    path('logout/', common_views.logoutX, name='logoutX'),

    # Version Compare
    path('version/compare/', common_views.versionViewCompare, name='version_compare'),
    path('version/compare/<int:pk>/', common_views.versionViewCompare, name='versionViewCompare'),

    path('table/', include('table.urls')),

    path('dum/', common_views.download_users_email, name='dum'),
]

# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns = [
#                       path('__debug__/', include(debug_toolbar.urls)),
#                   ] + urlpatterns
