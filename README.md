# Ant Colony Simulation

## Config file layout

The configuration file uses the json format. The options are listed below with their default value and meaning. Please note that setup.py needs to be run first to create the environment json file

| Option | Default | Description |
| ------ | ------- | ----------- |
| environment_path | `"environment.json"` | The path to grid layout with locations of food, colony and obstacles created by setup.py |
| num_ants | `10` | The total number of ants |
| pheromone_decay | `0.01` | The pheromone decay rate |
| seed | `42` | The seed to use for replication of results |
| frames | `1000` | The amount of timesteps to simulate |
| frame_interval | `200` | The delay between frames(in milliseconds) in the animation |
| video_output | `"images/ant_simulation.mp4"` | The path to store animation |
| exploration_desire | `0.01` | The base weight of the ants to just go randomly |
| mode | `"no_backtracking"` | The constraint on movement of the ant. Can be `"no_backtracking"`, `"yes_backtracking"` or `"self_avoiding"` |
| extension | `"none"` | The extension that affects pheromones. Can be `"none"` or `"elitist"` |
| elitist_ant_count | `0.01` | The weight given to elitist ant|
| pheromone_constant | `0.01` | The value by which the best path is scaled by in elitist extension |


The Final Presentation can be found ![here](./FinalPresentation.pdf).

