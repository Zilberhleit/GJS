import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated and self.user.is_staff:
            await self.channel_layer.group_add("notification_staff", self.channel_name)
        else:
            await self.channel_layer.group_add("notification_all", self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_authenticated and self.user.is_staff:
            await self.channel_layer.group_discard(
                "notification_staff", self.channel_name
            )
        else:
            await self.channel_layer.group_discard(
                "notification_all", self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.send(text_data=json.dumps({"message": message}))

    async def notify(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
