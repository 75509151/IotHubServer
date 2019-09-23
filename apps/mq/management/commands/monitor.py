from django.core.management.base import BaseCommand, CommandError

from mq.connect_monitor import monitor as connect_monitor
from mq.disconnect_monitor import monitor as disconnect_monitor
from mq.publish_monitor import monitor as publish_monitor



class Command(BaseCommand):
    help = "run mqtt monitor: connect disconnect publish"

    def add_arguments(self, parser):
        parser.add_argument("-t", "--type", choices=["connect",
            "disconnect",
            "publish"])

    def handle(self, *args, **options):
        monitor_type = options["type"]
        if monitor_type == "disconnect":
            disconnect_monitor()
        elif monitor_type == "connect":
            connect_monitor()
        else:
            publish_monitor()

        
