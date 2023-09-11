from collections import defaultdict
from typing import TYPE_CHECKING

from sc2reader_plugins.base_plugin import BasePlugin

if TYPE_CHECKING:
    from sc2reader.events import Event, PlayerStatsEvent
    from sc2reader.objects import Player
    from sc2reader.resources import Replay


class PlayerStatsTracker(BasePlugin):
    """
    Builds ``player.stats`` dictionary. Mainly extracted from PlayerStatsEvent.

    ## The dictionary contains the following keys as a dict:
    - worker_active: a dict of {second: workers_active_count}
    - income_minerals: a dict of {second: minerals_collection_rate}
    - income_vespene: a dict of {second: vespene_collection_rate}
    - income_resources: a dict of {second: resources_collection_rate}
    - unspent_minerals: a dict of {second: minerals_current}
    - unspent_vespene: a dict of {second: vespene_current}
    - unspent_resources: a dict of {second: resources_current}
    - minerals_used_active_forces: a dict of {second: minerals_used_active_forces}
    - vespene_used_active_forces: a dict of {second: vespene_used_active_forces}
    - resources_used_active_forces: a dict of {second: resources_used_active_forces}
    - minerals_used_technology: a dict of {second: minerals_used_current_technology}
    - vespene_used_technology: a dict of {second: vespene_used_current_technology}
    - resources_used_technology: a dict of {second: resources_used_current_technology}
    - minerals_lost: a dict of {second: minerals_lost}
    - vespene_lost: a dict of {second: vespene_lost}
    - resources_lost: a dict of {second: resources_lost}

    ## The following keys are not dicts:
    - avg_income_minerals: average of minerals_collection_rate
    - avg_income_vespene: average of vespene_collection_rate
    - avg_income_resources: average of resources_collection_rate
    - avg_unspent_minerals: average of minerals_current
    - avg_unspent_vespene: average of vespene_current
    - avg_unspent_resources: average of resources_current
    - minerals_lost_total: the last item in minerals_lost
    - vespene_lost_total: the last item in vespene_lost
    - resources_lost_total: the last item in resources_lost
    """

    name = "PlayerStatsTracker"

    def __init__(self) -> None:
        super().__init__()
        self.player_has_left = defaultdict(bool)

    def handleInitGame(self, event: "Event", replay: "Replay"):
        player: "Player"
        for player in replay.players:
            player.stats = defaultdict(dict)
            self.player_has_left[player.pid] = False

    def handlePlayerStatsEvent(self, event: "PlayerStatsEvent", replay: "Replay"):
        player: "Player" = event.player
        if player.pid == 16 or self.player_has_left[player.pid]:
            return

        player.stats["worker_active"][event.second] = event.workers_active_count

        player.stats["income_minerals"][event.second] = event.minerals_collection_rate
        player.stats["income_vespene"][event.second] = event.vespene_collection_rate
        player.stats["income_resources"][event.second] = (
            event.minerals_collection_rate + event.vespene_collection_rate
        )

        player.stats["unspent_minerals"][event.second] = event.minerals_current
        player.stats["unspent_vespene"][event.second] = event.vespene_current
        player.stats["unspent_resources"][event.second] = (
            event.minerals_current + event.vespene_current
        )

        player.stats["minerals_used_active_forces"][
            event.second
        ] = event.minerals_used_active_forces
        player.stats["vespene_used_active_forces"][
            event.second
        ] = event.vespene_used_active_forces
        player.stats["resources_used_active_forces"][event.second] = (
            event.minerals_used_active_forces + event.vespene_used_active_forces
        )

        player.stats["minerals_used_technology"][
            event.second
        ] = event.minerals_used_current_technology
        player.stats["vespene_used_technology"][
            event.second
        ] = event.vespene_used_current_technology
        player.stats["resources_used_technology"][event.second] = (
            event.minerals_used_current_technology
            + event.vespene_used_current_technology
        )

        player.stats["minerals_lost"][event.second] = event.minerals_lost
        player.stats["vespene_lost"][event.second] = event.vespene_lost
        player.stats["resources_lost"][event.second] = event.resources_lost

    def handlePlayerLeaveEvent(self, event: "Event", replay: "Replay"):
        player: "Player" = event.player
        self.player_has_left[player.pid] = True

    def handleEndGame(self, event: "Event", replay: "Replay"):
        player: "Player"
        for player in replay.players:
            player.stats["avg_income_minerals"] = sum(
                player.stats["income_minerals"].values()
            ) / len(player.stats["income_minerals"])
            player.stats["avg_income_vespene"] = sum(
                player.stats["income_vespene"].values()
            ) / len(player.stats["income_vespene"])
            player.stats["avg_income_resources"] = sum(
                player.stats["income_resources"].values()
            ) / len(player.stats["income_resources"])

            player.stats["avg_unspent_minerals"] = sum(
                player.stats["unspent_minerals"].values()
            ) / len(player.stats["unspent_minerals"])
            player.stats["avg_unspent_vespene"] = sum(
                player.stats["unspent_vespene"].values()
            ) / len(player.stats["unspent_vespene"])
            player.stats["avg_unspent_resources"] = sum(
                player.stats["unspent_resources"].values()
            ) / len(player.stats["unspent_resources"])

            # resource lost total should be the last item in the dict
            player.stats["minerals_lost_total"] = player.stats["minerals_lost"][
                max(player.stats["minerals_lost"].keys())
            ]
            player.stats["vespene_lost_total"] = player.stats["vespene_lost"][
                max(player.stats["vespene_lost"].keys())
            ]
            player.stats["resources_lost_total"] = player.stats["resources_lost"][
                max(player.stats["resources_lost"].keys())
            ]
