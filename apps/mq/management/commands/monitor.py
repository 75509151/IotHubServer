from django.core.management.base import BaseCommand, CommandError

from mq.connect_monitor import monitor


class Command(BaseCommand):
    help = "run mqtt connect monitor"


    def handle(self, *args, **options):
        monitor()
