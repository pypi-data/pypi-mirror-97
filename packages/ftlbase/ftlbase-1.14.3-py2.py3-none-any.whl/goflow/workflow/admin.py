from django.contrib import admin

from .models import *


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'label', 'description')
    search_fields = ('slug', 'label')
    fields = ['label', 'description', ]


class TransitionInline(admin.StackedInline):
    model = Transition
    fieldsets = ((None, {'fields': ('description', ('input', 'output'), 'condition', 'precondition')}),)

    def get_formset(self, request, obj=None, **kwargs):
        form = super().get_formset(request, obj, **kwargs)
        form.form.base_fields['input'].queryset = Activity.objects.filter(process=obj)
        form.form.base_fields['output'].queryset = Activity.objects.filter(process=obj)
        return form


class SubjectAdmin(admin.ModelAdmin):
    # list_display = ('name', 'description', )
    # inlines = [
    #     TransitionInline,
    # ]
    pass


admin.site.register(Subject, SubjectAdmin)


class ProcessAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled', 'summary', 'priority')
    inlines = [
        TransitionInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['begin'].queryset = Activity.objects.filter(process=obj)
        form.base_fields['end'].queryset = Activity.objects.filter(process=obj)
        return form


admin.site.register(Process, ProcessAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('url', 'documentation', 'test')


admin.site.register(Application, ApplicationAdmin)


class PushApplicationAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('url', 'documentation', 'test')


admin.site.register(PushApplication, PushApplicationAdmin)


class ActivityAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('process', 'title', 'description', 'kind', 'application', 'join_mode', 'split_mode',
                    'autostart', 'autofinish', 'graph_order', 'state_new')
    list_filter = ('process', 'kind')
    fieldsets = (
        (None, {'fields': (('kind', 'subflow'), ('title', 'process', 'graph_order'), 'description')}),
        ('Push application', {'fields': (('push_application', 'pushapp_param'),)}),
        ('Application', {'fields': (('application', 'app_param'),)}),
        ('I/O modes', {'fields': (('join_mode', 'split_mode'),)}),
        ('Execution modes', {'fields': (('autostart', 'autofinish', 'sendmail', 'approve', 'ratify',
                                         'enabled', 'readonly'),)}),
        ('Object Status Update', {'fields': (('state_update', 'state_field', 'state_new'),)}),
        ('Permission', {'fields': ('roles',)}),
    )


admin.site.register(Activity, ActivityAdmin)


class TransitionAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('__str__', 'process', 'input', 'output', 'condition', 'description')
    list_filter = ('process',)
    fieldsets = (
        (None, {'fields': (('name', 'description'), 'process', ('input', 'output'), 'condition', 'precondition')}),
    )


admin.site.register(Transition, TransitionAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'web_host', 'notified', 'last_notif', 'nb_wi_notif', 'notif_delay')
    list_filter = ('web_host', 'notified')


admin.site.register(UserProfile, UserProfileAdmin)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
