from app.blackjack.card_manager import CardManager
from app.blackjack.player import Player
from app.services.game_service import GameService


class BlackJackGame:
    def __init__(self,
                 card_manager: CardManager,
                 game_service: GameService):
        self.card_manager: CardManager = card_manager
        self.dealer_cards: list[str] = []
        self.dealer_stop: int = 17
        self.players: list[Player] = []
        self.game_service: GameService = game_service

    def add_players(self):
        for player_id, url in self.game_service.connected_players.items():
            self.players.append(Player(url=url, points=10))

    def deal_cards(self):
        pass
