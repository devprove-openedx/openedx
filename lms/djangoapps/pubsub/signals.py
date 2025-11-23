from google.cloud import pubsub_v1
from django.dispatch import receiver
from django.conf import settings

from django.contrib.auth.signals import user_logged_in

import json

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(settings.PUBSUB_PROJECT_ID, settings.PUBSUB_TOPIC_NAME)

def publish_event(event: dict):
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    return future.result()

@receiver(user_logged_in)
def send_login_event(sender, request, user, **kwargs):
    event = {
        "event_type": "login",
        "user_id": user.id,
        "username": user.username,
        "ip": request.META.get("REMOTE_ADDR"),
    }

    publish_event(event)
