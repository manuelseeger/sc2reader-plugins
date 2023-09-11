import sc2reader
from sc2reader.engine.plugins import ContextLoader
from sc2reader_plugins import EventSecondCorrector, WorkerTracker


def _test_worker_tracker(player):
    assert len(player.worker_count) > 0
    assert len(player.worker_trained) > 0
    assert len(player.worker_killed) > 0
    assert len(player.worker_lost) > 0
    assert player.worker_trained_total >= 0
    assert player.worker_killed_total >= 0
    assert player.worker_lost_total >= 0


def test_1v1():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), WorkerTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1.SC2Replay", engine=engine)
    p1, p2 = replay.players
    _test_worker_tracker(p1)
    _test_worker_tracker(p2)
    # killed and lost should be the same
    assert p1.worker_killed_total == p2.worker_lost_total
    assert p1.worker_lost_total == p2.worker_killed_total


def test_1v1_obs():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), WorkerTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1_obs.SC2Replay", engine=engine)
    p1, p2 = replay.players
    _test_worker_tracker(p1)
    _test_worker_tracker(p2)
    # killed and lost should be the same
    assert p1.worker_killed_total == p2.worker_lost_total
    assert p1.worker_lost_total == p2.worker_killed_total


def test_1v1_computer():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), WorkerTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1_computer.SC2Replay", engine=engine)
    p1, p2 = replay.players
    _test_worker_tracker(p1)
    _test_worker_tracker(p2)
    # killed and lost should be the same
    assert p1.worker_killed_total == p2.worker_lost_total
    assert p1.worker_lost_total == p2.worker_killed_total


def test_2v2():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), WorkerTracker()]
    )
    replay = factory.load_replay("tests/replays/2v2.SC2Replay", engine=engine)
    p1, p2, p3, p4 = replay.players
    _test_worker_tracker(p1)
    _test_worker_tracker(p2)
    _test_worker_tracker(p3)
    _test_worker_tracker(p4)
    # killed and lost should be the same
    assert (
        p1.worker_killed_total
        + p2.worker_killed_total
        + p3.worker_killed_total
        + p4.worker_killed_total
        == p1.worker_lost_total
        + p2.worker_lost_total
        + p3.worker_lost_total
        + p4.worker_lost_total
    )
