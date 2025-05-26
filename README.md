# Project 3

For the final project of Computational Physics we encourage you to define your
own project!

The only requirement we ask for is that it should be a simulation of a
physics-related project (but we consider physics-related rather broad, and e.g.
simulation of biological systems or an engineering problem are also absolutely
ok).
We do advise you though to start from a project where there is some existing literature.
in this way you have a starting point as well as something to compare your simulation to
for validation.

We encourage you to discuss your project idea with us during the time of class, 
or remotely via the planning issue #1. 

In any case, you need to fill in a short plan (a few lines) together with a
reference to literature in the planning issue, *and* have it agreed by us before
May 21 (i.e. latest two weeks before the presentation).

If you have problems to come up with a good project, we can provide you with
proven project ideas. But we first want you to try coming up with your own project!
Having designed your own project will also give a small bonus for the grade.

## Config file layout

The configuration file uses the json format. The options are listed below with their default value and meaning. Please note that setup.py needs to be run first to create the environment json file

| Option | Default | Description |
| ------ | ------- | ----------- |
| environment_path | `environment.json` | The path to grid layout with locations of food, colony and obstacles created by setup.py |
| num_ants | `10` | The total number of ants |
| pheromone_decay | `0.01` | The pheromone decay rate |
| seed | `42` | The seed to use for replication of results |
| frames | `1000` | The amount of timesteps to simulate |
| frame_interval | `200` | The delay between frames(in milliseconds) in the animation |
| video_output | `images/ant_simulation.mp4` | The path to store animation |
| exploration_desire | `0.01` | The base weight of the ants to just go randomly |
