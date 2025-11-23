from django.apps import AppConfig

class PubsubConfig(AppConfig):
    name = "djangoapps.pubsub"

    def ready(self):
        import .signals
