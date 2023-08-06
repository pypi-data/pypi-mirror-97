from django.core.management.base import BaseCommand

import settings


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--param',
            # action='setting',
            help='Setting configuration to show',
        )

    def handle(self, *args, **options):
        param =options.get('param')
        if param:
            print('\nSettings:\n')
            # print(vars(settings)[options.get('param')])
            varsettings = vars(settings)
            content = varsettings.get(param, None)
            if content:
                print(param+':',content)
            else:
                print('Error: não existe essa variável no settings:', param)
            # print(vars(settings)[options.get('param')])
        else:
            print('\nINSTALLED_APPS:\n')
            for i in settings.INSTALLED_APPS:
                print(i)
