import json

import mpyq
from sc2reader.resources import Replay


def load_replay_gamemetadata_json(rep: Replay) -> dict | None:
    """
    Extract "replay.gamemetadata.json" from replay archive.

    Args:
        rep: sc2reader.resources.Replay

    Returns:
        dict | None: replay.gamemetadata.json as dict or None if not found
    """
    archive: mpyq.MPQArchive = rep.archive
    try:
        metadata_json = archive.read_file("replay.gamemetadata.json").decode("utf-8")
        metadata = json.loads(metadata_json)
    except KeyError:
        metadata = None
    return metadata
