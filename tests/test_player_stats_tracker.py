import sc2reader
from sc2reader.engine.plugins import ContextLoader
from sc2reader_plugins import EventSecondCorrector, PlayerStatsTracker


def _test_player_stats_tracker(p1):
    assert len(p1.stats["worker_active"]) > 0
    assert len(p1.stats["income_minerals"]) > 0
    assert len(p1.stats["income_vespene"]) > 0
    assert len(p1.stats["income_resources"]) > 0
    assert len(p1.stats["unspent_minerals"]) > 0
    assert len(p1.stats["unspent_vespene"]) > 0
    assert len(p1.stats["unspent_resources"]) > 0
    assert len(p1.stats["minerals_used_active_forces"]) > 0
    assert len(p1.stats["vespene_used_active_forces"]) > 0
    assert len(p1.stats["resources_used_active_forces"]) > 0
    assert len(p1.stats["minerals_used_technology"]) > 0
    assert len(p1.stats["vespene_used_technology"]) > 0
    assert len(p1.stats["resources_used_technology"]) > 0
    assert len(p1.stats["minerals_lost"]) > 0
    assert len(p1.stats["vespene_lost"]) > 0
    assert len(p1.stats["resources_lost"]) > 0
    # value attributes
    assert p1.stats["avg_income_minerals"] >= 0
    assert p1.stats["avg_income_vespene"] >= 0
    assert p1.stats["avg_income_resources"] >= 0
    assert p1.stats["avg_unspent_minerals"] >= 0
    assert p1.stats["avg_unspent_vespene"] >= 0
    assert p1.stats["avg_unspent_resources"] >= 0
    assert p1.stats["minerals_lost_total"] >= 0
    assert p1.stats["vespene_lost_total"] >= 0
    assert p1.stats["resources_lost_total"] >= 0


def test_1v1():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), PlayerStatsTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1.SC2Replay", engine=engine)
    p1, p2 = replay.players
    _test_player_stats_tracker(p1)
    _test_player_stats_tracker(p2)


def test_1v1_obs():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), PlayerStatsTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1_obs.SC2Replay", engine=engine)
    p1, p2 = replay.players
    _test_player_stats_tracker(p1)
    _test_player_stats_tracker(p2)


def test_1v1_computer():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), PlayerStatsTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1_computer.SC2Replay", engine=engine)
    p1, p2 = replay.players
    # human player
    assert p1.is_human
    _test_player_stats_tracker(p1)
    # computer player also have stats
    assert not p2.is_human
    _test_player_stats_tracker(p2)


def test_2v2():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), PlayerStatsTracker()]
    )
    replay = factory.load_replay("tests/replays/2v2.SC2Replay", engine=engine)
    p1, p2, p3, p4 = replay.players
    _test_player_stats_tracker(p1)
    _test_player_stats_tracker(p2)
    _test_player_stats_tracker(p3)
    _test_player_stats_tracker(p4)
