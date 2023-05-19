from channels.generic.websocket import AsyncWebsocketConsumer
from websockets.helpers import get_auction


class BaseConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.connection_name = self.scope['url_route']['kwargs']['auction_id']
        self.connection_group_name = f'websocket_group_{self.connection_name}'

        # Подключение к аукциону
        await self.channel_layer.group_add(
            self.connection_group_name,
            self.connection_name
        )

        get_auction(self.connection_name)
        return await self.accept()

    async def disconnect(self, close_code: int):
        """
        Осуществляет выход из группы

        Args:
            close_code (int): код выхода
        """

        await self.channel_layer.group_discard(
            self.connection_group_name,
            self.channel_name
        )

class AuctionConsumer(BaseConsumer):
    pass