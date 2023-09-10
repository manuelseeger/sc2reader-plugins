import math
from collections import defaultdict
from typing import TYPE_CHECKING

from sc2reader_plugins.base_plugin import BasePlugin

if TYPE_CHECKING:
    from sc2reader.events import Event, PlayerStatsEvent
    from sc2reader.objects import Player
    from sc2reader.resources import Replay


def _sq(i: float, u: float) -> float:
    """
    Calculate the sq.
    """
    if u <= 0:
        return 0  # avoid math domain error
    return 35 * (0.00137 * i - math.log(u)) + 240


class SQTracker(BasePlugin):
    """
    Builds ``player.sq`` dictionary where sq is spending quotient, which reflects
    the player's macro ability. The higher the sq is, the better the player's macro
    ability is. See more details at https://liquipedia.net/starcraft2/Spending_quotient.

    Also provides ``player.avg_sq`` which represents the average sq of the player.
    """

    name = "SQTracker"

    def __init__(self) -> None:
        super().__init__()
        self.income_rates = defaultdict(float)
        self.unspent_resources = defaultdict(float)
        self.player_has_left = defaultdict(bool)

    def handleInitGame(self, event: "Event", replay: "Replay"):
        player: "Player"
        for player in replay.players:
            player.sq = defaultdict(float)
            player.seconds_played = replay.length.seconds
            self.income_rates[player.pid] = []
            self.unspent_resources[player.pid] = []
            self.player_has_left[player.pid] = False

    def handlePlayerStatsEvent(self, event: "PlayerStatsEvent", replay: "Replay"):
        player: "Player" = event.player
        if player.pid == 16 or self.player_has_left[player.pid]:
            return

        income_rate = event.minerals_collection_rate + event.vespene_collection_rate
        unspent_resources = event.minerals_current + event.vespene_current
        player.sq[event.second] = _sq(income_rate, unspent_resources)
        # record i and u for calculating avg_sq
        self.income_rates[player.pid].append(income_rate)
        self.unspent_resources[player.pid].append(unspent_resources)

    def handlePlayerLeaveEvent(self, event: "Event", replay: "Replay"):
        player: "Player" = event.player
        player.seconds_played = event.second
        self.player_has_left[player.pid] = True

    def handleEndGame(self, event: "Event", replay: "Replay"):
        player: "Player"
        for player in replay.players:
            if len(self.income_rates[player.pid]) > 0:
                player.avg_sq = _sq(
                    sum(self.income_rates[player.pid])
                    / len(self.income_rates[player.pid]),
                    sum(self.unspent_resources[player.pid])
                    / len(self.unspent_resources[player.pid]),
                )
            else:
                player.avg_sq = 0
