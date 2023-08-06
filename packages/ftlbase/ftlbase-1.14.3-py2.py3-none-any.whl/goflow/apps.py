# -*- coding: utf-8 -*-
from importlib import import_module

from django.apps import AppConfig


class GoflowConfig(AppConfig):
    name = 'goflow'
    # module = 'goflow'
    # verbose_name = 'Workflow'

    # def __init__(self, app_name, app_module):
    #     super().__init__(app_name, app_module)
    #     print(app_name)
    #     print(app_module)
    #     print(self.name)
    #     print(self.module)
    #     print(self.label)
    #     print(self.models_module)
    #     print(self.models)

    def ready(self):
        from .workflow.models import Process, State
        assert Process, State
        pass

    def import_models(self):
        # Dictionary of models for this app, primarily maintained in the
        # 'all_models' attribute of the Apps this AppConfig is attached to.
        super().import_models()
        # print(self.models_module)
        self.models_module = import_module('goflow.workflow.models')
        # print(vars(self.models_module))
        from .workflow.models import Process
        assert Process

        # self.models = self.apps.all_models[self.label]
        #
        # if module_has_submodule(self.module, MODELS_MODULE_NAME):
        #     models_module_name = '%s.%s' % (self.name, MODELS_MODULE_NAME)
        #     self.models_module = import_module(models_module_name)
