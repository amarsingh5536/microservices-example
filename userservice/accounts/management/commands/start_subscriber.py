from django.core.management.base import BaseCommand
from pubsub.factory import PubsubFactory

class Command(BaseCommand):
    help = "Start pubsub Consumer"

    def handle(self, *args, **kwargs):
        """
        Start the pubsub Consumer using the Consumer.start() method
        """
        self.stdout.write("Starting pubsub Consumer...")
        subscriber=PubsubFactory()
        subscriber.start_subscriber()
