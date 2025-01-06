from collections import defaultdict
from typing import TYPE_CHECKING

from sc2reader_plugins.base_plugin import BasePlugin
from sc2reader_plugins.utils import load_replay_gamemetadata_json

if TYPE_CHECKING:
    from sc2reader.events import Event
    from sc2reader.objects import Player
    from sc2reader.resources import Replay


class APMTracker(BasePlugin):
    """
    Builds ``player.aps`` and ``player.apm`` dictionaries where an action is
    any Selection, ControlGroup, or Command event.

    Also provides ``player.avg_apm`` which is defined as the sum of all the
    above actions divided by the number of seconds played by the player (not
    necessarily the whole game) multiplied by 60.

    Also provides ``player.official_apm`` which is given by the official APM
    algorithm. This is the APM that is displayed in the game score screen.
    """

    name = "APMTracker"

    def handleInitGame(self, event: "Event", replay: "Replay"):
        # extract official apm from replay metadata
        gamemetadata = load_replay_gamemetadata_json(replay)
        if gamemetadata is None:
            for player in replay.players:
                player.official_apm = None
        else:
            archon_mode = any(p.archon_leader_id is not None for p in replay.players)

            for player in replay.players:
                # players have pid starting from 1, and there may be observers that
                # have pid larger than the number of players, so we need to check
                # if the pid is valid
                try:
                    # pid and team id starts from 1, but index starts from 0
                    p_index = ( player.pid if not archon_mode else player.team_id ) -1
                    player.official_apm = gamemetadata["Players"][p_index]["APM"]
                except ( KeyError, IndexError ):
                    player.official_apm = None
        # build self-calculated apm and aps
        for player in replay.players:
            player.apm = defaultdict(int)
            player.aps = defaultdict(int)
            player.seconds_played = replay.length.seconds
        # record players
        self.players = replay.players

    def handleControlGroupEvent(self, event: "Event", replay: "Replay"):
        player: "Player" = event.player
        if player not in self.players:
            return
        player.aps[event.second] += 1
        player.apm[int(event.second / 60)] += 1

    def handleSelectionEvent(self, event: "Event", replay: "Replay"):
        player: "Player" = event.player
        if player not in self.players:
            return
        player.aps[event.second] += 1
        player.apm[int(event.second / 60)] += 1

    def handleCommandEvent(self, event: "Event", replay: "Replay"):
        player: "Player" = event.player
        if player not in self.players:
            return
        player.aps[event.second] += 1
        player.apm[int(event.second / 60)] += 1

    def handlePlayerLeaveEvent(self, event: "Event", replay: "Replay"):
        player: "Player" = event.player
        if player not in self.players:
            return
        player.seconds_played = event.second

    def handleEndGame(self, event: "Event", replay: "Replay"):
        for player in replay.players:
            if player not in self.players:
                continue
            if len(player.apm.keys()) > 0 and player.seconds_played > 0:
                player.avg_apm = (
                    sum(player.aps.values()) / float(player.seconds_played) * 60
                )
            else:
                player.avg_apm = 0
