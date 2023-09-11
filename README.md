# sc2reader-plugins

Nice plugins for [sc2reader](https://github.com/ggtracker/sc2reader).

The plugins are designed to be simple, easy to understand and use, yet versatile enough to provide a wide range of functionalities. It is worth noting that these plugins are designed with decoupling in mind, allowing selectively loading and using only the ones required for your sc2 replay job.

## Installation

**Using pip:**

```shell
pip install git+https://github.com/NumberPigeon/sc2reader-plugins.git
```

**Using [rye](https://github.com/mitsuhiko/rye):**

```shell
rye add --git https://github.com/NumberPigeon/sc2reader-plugins.git sc2reader-plugins
```

## Usage

A simple example that using `APMTracker` plugin to get the players' apm:

```python
>>> import sc2reader
>>> from sc2reader_plugins import EventSecondCorrector, APMTracker
>>> sc2reader.engine.register_plugin(EventSecondCorrector()) #Recommended for lotv reps
>>> sc2reader.engine.register_plugin(APMTracker())
>>> replay = sc2reader.load_replay("tests/replays/1v1.SC2Replay")
>>> p1, p2 = replay.players
>>> p1.official_apm
305.0
>>> p1.avg_apm
276.69565217391306
```

The `official_apm`, which is the apm value shown in the after game summary, and the `avg_apm` which is calculated based on a naive algorithm.

## Full list of Plugins

- **APMTracker**: track players' apm and official apm.
- **EventSecondCorrector**: align `event.second` to `replay.game_length` under lotv. See [issue](https://github.com/ggtracker/sc2reader/pull/186#issuecomment-1687326764).
- **PlayerStatsTracker**: extract infos from `PlayersStatsEvent` and build `player.stats` for easier data extraction.
- **SQTracker:** track players' [sq](https://liquipedia.net/starcraft2/Spending_quotient).
- **WorkerTracker:** track players' worker stats.

## TBD

More plugins, better documents...

Any suggestions and contributions are welcomed!
