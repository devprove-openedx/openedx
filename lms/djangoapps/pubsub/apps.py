from django.apps import AppConfig

class PubsubConfig(AppConfig):
    name = "lms.djangoapps.pubsub"

    def ready(self):
        import .signals
