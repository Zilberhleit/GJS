from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_realtime_notification(
    user_id, message, notification_id=None, notification_type="info"
):
    channel_layer = get_channel_layer()
    try:
        async_to_sync(channel_layer)(
            f"user_{user_id}",
            {
                "type": "notify",
                "message": message,
                "notification_id": notification_id,
                "notification_type": notification_type,
            },
        )
    except Exception as e:
        print(f"Websocket notification error: {e}")
