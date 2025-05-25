import json
from typing import Any


def parse_config(path: str) -> dict[str, Any]:
    with open(path, "r") as f:
        config = json.load(f)
    return {
        "environment_path": config.get("environment_path", "environment.json"),
        "num_ants": config.get("num_ants", 10),
        "pheromone_strength": config.get("pheromone_strength", 1.0),
        "pheromone_decay": config.get("pheromone_decay", 0.05),
        "seed": config.get("seed", 42),
        "frames": config.get("frames", 300),
        "frame_interval": config.get("frame_interval", 200),
        "video_output": config.get("video_output", "images/ant_simulation.mp4")
    }
