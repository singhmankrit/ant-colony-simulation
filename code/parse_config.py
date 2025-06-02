import json
from typing import Any


def parse_config(path: str) -> dict[str, Any]:
    with open(path, "r") as f:
        config = json.load(f)
    return {
        "environment_path": config.get("environment_path", "environment.json"),
        "num_ants": config.get("num_ants", 10),
        "pheromone_decay": config.get("pheromone_decay", 0.05),
        "exploration_desire": config.get("exploration_desire", 0.1),
        "ant_energy": config.get("ant_energy", 100),
        "ant_max_carry_amount": config.get("ant_max_carry_amount", 130),
        "observables": config.get("observables", []),
        "seed": config.get("seed", None),
        "frames": config.get("frames", 300),
        "frame_interval": config.get("frame_interval", 200),
        "video_output": config.get("video_output", "images/ant_simulation.mp4"),
    }
