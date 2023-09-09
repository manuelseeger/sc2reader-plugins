import sc2reader
from sc2reader.engine.plugins import ContextLoader
from sc2reader_plugins import APMTracker, EventSecondCorrector


def test_1v1():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), APMTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1.SC2Replay", engine=engine)
    p1, p2 = replay.players
    assert p1.official_apm > 10
    assert p2.official_apm > 10
    assert len(p1.apm) > 0
    assert len(p2.apm) > 0
    assert p1.avg_apm > 10
    assert p2.avg_apm > 10


def test_1v1_obs():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), APMTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1_obs.SC2Replay", engine=engine)
    p1, p2 = replay.players
    assert p1.official_apm > 10
    print(p2.official_apm)
    assert p2.official_apm > 10
    assert len(p1.apm) > 0
    print((p2.apm))
    assert len(p2.apm) > 0
    assert p1.avg_apm > 10
    print(p2.avg_apm)
    assert p2.avg_apm > 10


def test_1v1_computer():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), APMTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1_computer.SC2Replay", engine=engine)
    p1, p2 = replay.players
    # human player
    assert p1.is_human
    assert p1.official_apm > 10
    assert len(p1.apm) > 0
    assert p1.avg_apm > 0
    # computer player only has official apm
    assert not p2.is_human
    assert p2.official_apm is not None
    assert len(p2.apm) == 0
    assert p2.avg_apm == 0


def test_2v2():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), APMTracker()]
    )
    replay = factory.load_replay("tests/replays/2v2.SC2Replay", engine=engine)
    p1, p2, p3, p4 = replay.players
    assert p1.official_apm > 10
    assert p2.official_apm > 10
    assert p3.official_apm > 10
    assert p4.official_apm > 10
    assert len(p1.apm) > 0
    assert len(p2.apm) > 0
    assert len(p3.apm) > 0
    assert len(p4.apm) > 0
    assert p1.avg_apm > 10
    assert p2.avg_apm > 10
    assert p3.avg_apm > 10
    assert p4.avg_apm > 10
