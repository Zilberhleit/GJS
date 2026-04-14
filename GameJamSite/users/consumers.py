import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        if self.user.is_staff:
            self.group_name = "notification_staff"
        else:
            self.group_name = "notification_all"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # await self.send(
        #     text_data=json.dumps(
        #         {
        #             "type": "connection",
        #             "message": f"Connected to {self.group_name}",
        #             "user": self.user.username,
        #         }
        #     )
        # )

    async def disconnect(self, close_code):
        if hasattr(self, "user") and self.user.is_authenticated and self.user.is_staff:
            await self.channel_layer.group_discard(
                "notification_staff", self.channel_name
            )
        else:
            await self.channel_layer.group_discard(
                "notification_all", self.channel_name
            )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            type = text_data_json.get("type", "message")
            message = text_data_json.get("message", "")

            if type == "ping":
                await self.send(text_data=json.dumps({"type": "pong"}))
            elif type == "message":
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "notify",
                        "message": message,
                        "sender": self.user.username,
                    },
                )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))

    async def notify(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "notification",
                    "message": event["message"],
                    "sender": event.get("sender", "system"),
                    "timestamp": event.get("timestamp"),
                }
            )
        )
