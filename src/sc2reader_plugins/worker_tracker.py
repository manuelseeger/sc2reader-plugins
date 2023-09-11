from collections import defaultdict
from typing import TYPE_CHECKING

from sc2reader_plugins.base_plugin import BasePlugin

if TYPE_CHECKING:
    from sc2reader.data import Unit
    from sc2reader.events import Event, UnitBornEvent, UnitDiedEvent
    from sc2reader.objects import Player
    from sc2reader.resources import Replay


# using this instead of sc2reader.data.Unit.is_worker
# so that Mule is not counted as a worker
def _is_worker(u: "Unit") -> bool:
    return u.name in {"Drone", "Probe", "SCV"}


class WorkerTracker(BasePlugin):
    """
    Track the players worker stats. This includes:
    - `player.worker_count`: a dict of {second: worker_count}
    - `player.worker_trained`: a dict of {second: worker_trained_count}. Note that
        this does not include the initial workers.
    - `player.worker_killed`: a dict of {second: worker_killed_count}
    - `player.worker_lost`: a dict of {second: worker_lost_count}
    - `player.worker_trained_total`: the number of workers trained in total
    - `player.worker_killed_total`: the number of workers killed in total
    - `player.worker_lost_total`: the number of workers lost in total

    Note that the active worker count is NOT tracked by this plugin. This can be
    fount in the `PlayerStatsTracker` plugin.
    """

    name = "WorkerTracker"

    def handleInitGame(self, event: "Event", replay: "Replay"):
        player: "Player"
        for player in replay.players:
            player.worker_count = defaultdict(int)
            player.worker_trained = defaultdict(int)
            player.worker_killed = defaultdict(int)
            player.worker_lost = defaultdict(int)
            player.seconds_played = replay.length.seconds
        self.players = set(replay.players)

    def handleUnitBornEvent(self, event: "UnitBornEvent", replay: "Replay"):
        player: "Player" = event.unit_controller
        if not player or player not in self.players:
            return
        if _is_worker(event.unit):
            player.worker_count[event.second] += 1
            if event.frame > 0:  # to exclude the initial workers
                player.worker_trained[event.second] += 1

    def handleUnitDiedEvent(self, event: "UnitDiedEvent", replay: "Replay"):
        player: "Player" = event.unit.owner
        if player not in self.players:
            return
        if _is_worker(event.unit):
            player.worker_count[event.second] -= 1
            # exclude the morphing drones
            if event.unit.name == "Drone" and event.killing_unit is None:
                pass
            else:
                player.worker_lost[event.second] += 1
                killer_player: "Player" = event.killing_player
                if killer_player is not None:
                    killer_player.worker_killed[event.second] += 1

    def handlePlayerLeaveEvent(self, event: "Event", replay: "Replay"):
        player: "Player" = event.player
        player.seconds_played = event.second

    def handleEndGame(self, event: "Event", replay: "Replay"):
        player: "Player"
        for player in self.players:
            # fill the dicts
            for i in range(0, player.seconds_played):
                if i not in player.worker_count:
                    player.worker_count[i + 1] = player.worker_count[i]
                else:
                    player.worker_count[i + 1] += player.worker_count[i]
                if i not in player.worker_trained:
                    player.worker_trained[i + 1] = player.worker_trained[i]
                else:
                    player.worker_trained[i + 1] += player.worker_trained[i]
                if i not in player.worker_killed:
                    player.worker_killed[i + 1] = player.worker_killed[i]
                else:
                    player.worker_killed[i + 1] += player.worker_killed[i]
                if i not in player.worker_lost:
                    player.worker_lost[i + 1] = player.worker_lost[i]
                else:
                    player.worker_lost[i + 1] += player.worker_lost[i]
            # sort the dicts
            player.worker_count = dict(sorted(player.worker_count.items()))
            player.worker_trained = dict(sorted(player.worker_trained.items()))
            player.worker_killed = dict(sorted(player.worker_killed.items()))
            player.worker_lost = dict(sorted(player.worker_lost.items()))
            # get total counts
            player.worker_trained_total = player.worker_trained[
                max(player.worker_trained.keys())
            ]
            player.worker_killed_total = player.worker_killed[
                max(player.worker_killed.keys())
            ]
            player.worker_lost_total = player.worker_lost[
                max(player.worker_lost.keys())
            ]
