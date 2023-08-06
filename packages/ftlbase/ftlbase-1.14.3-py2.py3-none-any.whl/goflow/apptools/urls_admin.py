from django.urls import re_path

from . import views

urlpatterns = [
    # (r'^icon/image_update/$', 'image_update'),
    re_path(r'^application/testenv/(?P<action>create|remove)/(?P<id>.*)/$', views.app_env.as_view(), name='app_env'),
    re_path(r'^application/teststart/(?P<id>.*)/$', views.test_start.as_view(), name='test_start'),
]
