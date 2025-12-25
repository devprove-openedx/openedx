from google.cloud import pubsub_v1
from django.dispatch import receiver
from django.conf import settings

from django.contrib.auth.signals import user_logged_in

import base64
import json

try:
    decoded = base64.b64decode(settings.PUBSUB_KEY)
    pubsub_key = json.loads(decoded.decode("utf-8"))

    publisher = pubsub_v1.PublisherClient.from_service_account_info(pubsub_key)
    topic_path = publisher.topic_path(settings.PUBSUB_PROJECT_ID, settings.PUBSUB_TOPIC_NAME)
except:
    publisher = None

def publish_event(event: dict):
    if not publisher: return
        
    try:
        data = json.dumps(event).encode("utf-8")
        
        publisher.publish(topic_path, data=data)
    except: return

@receiver(user_logged_in)
def send_login_event(sender, request, user, **kwargs):
    if not publisher: return None
        
    ip = (
        request.META.get("CF-Connecting-IP")
        or request.META.get("REMOTE_ADDR")
    )
    
    event = {
        "event_type": "login",
        "user_id": user.id,
        "username": user.username,
        "ip": ip
    }

    publish_event(event)
