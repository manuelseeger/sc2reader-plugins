import sc2reader
from sc2reader.engine.plugins import ContextLoader
from sc2reader_plugins import EventSecondCorrector, SQTracker


def test_1v1():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), SQTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1.SC2Replay", engine=engine)
    p1, p2 = replay.players
    assert p1.avg_sq > 10
    assert p2.avg_sq > 10
    assert len(p1.sq) > 0
    assert len(p2.sq) > 0


def test_1v1_obs():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), SQTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1_obs.SC2Replay", engine=engine)
    p1, p2 = replay.players
    assert p1.avg_sq > 10
    assert p2.avg_sq > 10
    assert len(p1.sq) > 0
    assert len(p2.sq) > 0


def test_1v1_computer():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), SQTracker()]
    )
    replay = factory.load_replay("tests/replays/1v1_computer.SC2Replay", engine=engine)
    p1, p2 = replay.players
    # human player
    assert p1.is_human
    assert p1.avg_sq > 10
    assert len(p1.sq) > 0
    # computer player also have sq
    assert not p2.is_human
    assert p2.avg_sq is not None
    assert len(p2.sq) > 0


def test_2v2():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(
        plugins=[EventSecondCorrector(), ContextLoader(), SQTracker()]
    )
    replay = factory.load_replay("tests/replays/2v2.SC2Replay", engine=engine)
    p1, p2, p3, p4 = replay.players
    assert p1.avg_sq > 10
    assert p2.avg_sq > 10
    assert p3.avg_sq > 10
    assert p4.avg_sq > 10
    assert len(p1.sq) > 0
    assert len(p2.sq) > 0
    assert len(p3.sq) > 0
    assert len(p4.sq) > 0
