import asyncio
import json
from django.contrib.auth import get_user_model 
from channels.consumer import AsyncConsumer 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Game, Move 
from user.models import Player, Notification

from django.utils import timezone

import chess

class GameConsumer(AsyncConsumer):
    #handles chess games
    async def websocket_connect(self, event):
        game_id = self.scope["url_route"]["kwargs"]["pk"]
        group_name = "game_%s" % game_id
        self.group_name = group_name
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })
        game = await self.get_game(game_id)
        user = self.scope["user"]
        await self.set_online_status(user, True)
        json_response = await self.get_game_update(game, is_initial=True)
        await self.send({
            "type": "websocket.send",
            "text": json_response
        })

    async def websocket_receive(self, event):
        event_json = json.loads(event["text"])
        if type(event_json) is dict and event_json["header-content"]:
            if event_json["header-content"] == "request-result":
                game_id = self.scope["url_route"]["kwargs"]["pk"]
                game = await self.get_game(game_id)
                await self.check_flagging(game)
                json_response = await self.get_game_update(game)
                await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "move_message",
                    "text": json_response
                })
                return

                
        last_move = event_json["last_move"]
        move_count = event_json["move_count"]
        game_id = self.scope["url_route"]["kwargs"]["pk"]
        game = await self.get_game(game_id)
        if game.is_finished:
            return 
        is_valid = await self.is_valid_move(game, move_count)
        if not is_valid:
            #invalid move, can't make chess object
            return
        chess_obj = await  self.get_game_obj(game)
        chess_obj.push_san(last_move)
        user = self.scope["user"]
        color = await self.get_player_color(game, user)
        if not self.is_valid_player(game, user, color):
            #invalid player, doesn't have the required permissions to move
            return
        index = await self.get_move_index(game)
        move_length = await self.get_move_time(game)
        await self.add_move(game, last_move, index, move_length, color)
        if chess_obj.is_game_over():
            result = chess_obj.result 
            if result == "1-0":
                await self.update_game_status(game, 0)
            if result == "0-1":
                await self.update_game_status(game, 1)
            if result == "1/2-1/2":
                await self.update_game_status(game, 2)
        json_response = await self.get_game_update(game)
        await self.channel_layer.group_send(
            self.group_name,
            {
            "type": "move_message",
            "text": json_response
            })

    async def move_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    
    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        user = self.scope["user"]
        await self.set_online_status(user, False)
    
    @database_sync_to_async
    def set_online_status(self, player, status):
        player.online = status 
        player.save()

    @database_sync_to_async
    def get_game(self, pk):
        return Game.objects.get(code=pk)

    @database_sync_to_async
    def check_flagging(self, game):
        return game.check_time()

    @database_sync_to_async
    def get_game_obj(self, game):
        return game.get_game_object()

    @database_sync_to_async
    def get_player_color(self, game, player):
        if game.white_player == player:
            return 0
        elif game.black_player == player:
            return 1

    def is_valid_player(self, game, player, color):
        if color == 0 and game.white_player == player:
            return True 
        if color == 1 and game.black_player == player:
            return True 
        return False

    @database_sync_to_async
    def get_move_index(self, game):
        return int(game.moves.count()/2) + 1

    @database_sync_to_async
    def add_move(self, game, text, index, duration, color):
        game.add_move(text, index, duration, color)

    @database_sync_to_async
    def get_move_time(self, game):
        if game.moves.count() > 2:
            return (timezone.now() - game.get_last_move().date).total_seconds()
        return 0

    @database_sync_to_async
    def is_valid_move(self, game, move_count):
        return game.is_valid_move(move_count)

    @database_sync_to_async
    def update_game_status(game, status):
        game.result = status
        game.is_finished = True
        game.save()

    @database_sync_to_async
    def get_game_update(self, game, is_initial=False):
        response = {"white": game.white_player.username,
                    "black": game.black_player.username,
                    "time_white": float(game.time_remaining_white),
                    "time_black": float(game.time_remaining_black),
                    "is_white_moving": game.is_white_moving,
                    "total_duration": game.total_duration,
                    "increment": game.increment,
                    "is_started": game.started,
                    "start_time": game.start_timer,
                    "result": game.result,
                    "moves": [],
                    "initial": is_initial
                    }
        for move in game.moves.order_by("index", "color"):
            response["moves"].append(move.text)
        return json.dumps(response)
            



class NotificationConsumer(AsyncConsumer):
    #handles notification
    async def websocket_connect(self, event):
        await self.send({
            "type": "weboscket.accept"
        })
    async def webscoket_receive(self, event):
        pass
    async def webscoket_disconnect(self, event):
        pass