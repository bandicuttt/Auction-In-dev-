import json
from channels.generic.websocket import AsyncWebsocketConsumer

from websockets.helpers import get_authenticated_user
from websockets.queries import get_auction

from auctions.commons.responses import WSAuctionResponses


class BaseConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.connection_name = self.scope['url_route']['kwargs']['auction_id']
        self.connection_group_name = f'websocket_group_{self.connection_name}'

        # Подключение к аукциону
        await self.channel_layer.group_add(
            self.connection_group_name,
            self.connection_name
        )

        if not await get_authenticated_user(self):
            return await self.close(code=403)
        
        auction = await get_auction(self.connection_name)

        if auction:

            await self.accept()
            return await self.send(
                text_data=json.dumps(
                    WSAuctionResponses.success_connect_to_auction(auction)
                ))
        
        return await self.close(code=403)

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

    async def notify_auction_update(self, auction):
        """
        Отправляет уведомление об обновлении Auction всем пользователям в группе.
        
        Args:
            auction: Обновленный объект Auction.
        """
        await self.channel_layer.group_send(
            self.connection_group_name,
            {
                'type': 'auction_update',
                'auction': auction,
            }
        )

class AuctionConsumer(BaseConsumer):
    pass