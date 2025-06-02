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
        "ant_carry_amount": config.get("ant_carry_amount", 130),
        "colony_start_amount": config.get("colony_start_amount", 1000),
        "observables": config.get("observables", []),
        "seed": config.get("seed", None),
        "cycles": config.get("cycles", 1),
        "frames": config.get("frames", 300),
        "frame_interval": config.get("frame_interval", 200),
        "mode": config.get("mode", "no_backtracking"),
        "extension": config.get("extension", "none"),
        "elitist_ant_count": config.get("elitist_ant_count", 5),
        "pheromone_constant": config.get("pheromone_constant", 1.0),
    }
