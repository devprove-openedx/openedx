from django.apps import AppConfig

class EventsConfig(AppConfig):
    name = "djangoapps.events"

    def ready(self):
        import .signals
