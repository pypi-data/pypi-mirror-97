from django.urls import path

from common import views as common_views
from . import views, forms, models

app_name = 'ftl-mp'

urlpatterns = [
    # path('notifications/<str:reference>', views.PoolPreferenceView, name='notifications_home'),
    # path('post_payment/<str:reference>', views.PoolPreferenceView, name='payment_success_home', ),
    # path('payment_failed/<str:reference>', views.PoolPreferenceView, name='payment_failure_home', ),
    # path('payment_pending/<str:reference>', views.PoolPreferenceView, name='payment_pending_home', ),

    path('notifications/', views.NotificationView.as_view(), name='notifications_home'),
    path('post_payment/', views.PaymentSuccessView.as_view(), name='payment_success_home', ),
    path('payment_failed/', views.PaymentFailedView.as_view(), name='payment_failure_home', ),
    path('payment_pending/', views.PaymentPendingView.as_view(), name='payment_pending_home', ),

    path('notifications/<str:reference>', views.NotificationView.as_view(), name='notifications'),
    path('post_payment/<str:reference>', views.PaymentSuccessView.as_view(), name='payment_success', ),
    path('payment_failed/<str:reference>', views.PaymentFailedView.as_view(), name='payment_failure', ),
    path('payment_pending/<str:reference>', views.PaymentPendingView.as_view(), name='payment_pending', ),

    path('notifications_preapproval/', views.NotificationPreApprovalView.as_view(),
         name='notifications_preapproval_home'),
    path('notifications_preapproval/<str:reference>', views.NotificationPreApprovalView.as_view(),
         name='notifications_preapproval'),

    *common_views.include_CRUD('preference', table=forms.PreferenceTable, form=forms.PreferencesForm,
                               goto='mp:preference'),

    path('mp_preferences/', common_views.commonListaTable,
         {'model': forms.PrefTable, 'data': models.Preference.search,
          'title': 'Consulta Preferences Diretamente no MP'},
         name='mp_preferences'),

    path('pool/', views.PoolPreferenceView, name='pool_preference_home', ),
    path('pool/<int:pk>/<str:goto>', views.PoolPreferenceView, name='pool_preference', ),

]
