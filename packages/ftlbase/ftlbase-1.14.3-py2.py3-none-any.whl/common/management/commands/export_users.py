from django.core.management.base import BaseCommand

from common.utils import export_users


class Command(BaseCommand):
    def handle(self, *args, **options):
        export_users()