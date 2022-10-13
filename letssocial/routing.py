from django.urls import re_path,path
from . import consumers
websocket_urlpatterns = [
path(f'ws/chat/<str:username>and<str:otherusername>', consumers.MyChatConsumer.as_asgi()),
path(f'ws/chat/<str:otherusername>and<str:username>', consumers.MyChatConsumer.as_asgi()),
]