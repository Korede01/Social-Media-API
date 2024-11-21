from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()
            

async def disconnect(self, close_code):
    if self.user.is_authenticated:
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

async def receive(self, text_data):
    data = json.loads(text_data)
    message = data.get("message", "")
    
    await self.send(text_data=json.dumps({
        "message": message
    }))

async def send_notification(self, event):
    await self.send(text_data=json.dumps({
        "notification": event["notification"]
    }))
