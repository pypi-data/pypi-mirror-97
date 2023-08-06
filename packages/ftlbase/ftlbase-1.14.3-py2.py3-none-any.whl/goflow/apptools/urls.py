from django.urls import path, re_path

from . import views

urlpatterns = [
    # path('start/(?P<app_label>.*)/(?P<model_name>.*)/$', start_application),
    # path('start_proto/(?P<process_name>.*)/$', start_application,
    #     {'form_class': forms.DefaultAppStartForm, 'template': 'goflow/start_proto.html'}),
    # path('view_application/<int:id>\d+)/$', view_application),
    path('choice_application/<int:id>/', views.choice_application),
    # path('process/<int:id>/', choice_application),
    path('sendmail/', views.sendmail),
    re_path(r'^application/testenv/(?P<action>create|remove)/(?P<id>.*)/$', views.app_env, name='app_env'),
    re_path(r'^application/teststart/(?P<id>.*)/$', views.test_start, name='test_start'),
]
