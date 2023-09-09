import sc2reader
from sc2reader_plugins import EventSecondCorrector


def test_plugin():
    factory = sc2reader.factories.SC2Factory()
    engine = sc2reader.engine.GameEngine(plugins=[EventSecondCorrector()])
    replay = factory.load_replay("tests/replays/1v1.SC2Replay", engine=engine)
    assert replay.events[0].second == 0
    assert replay.events[-1].second == replay.length.seconds
