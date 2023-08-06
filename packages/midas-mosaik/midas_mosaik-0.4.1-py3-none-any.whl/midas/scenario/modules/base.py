"""MIDAS scenario base module.

In this module the base configuration for each scenario is done.

"""
import os
from os.path import abspath, join
import pickle

import mosaik
import numpy as np


def configure(scenario, params, cfg):
    """Create the base configuration for midas scenarios.

    Parameters
    ----------
    scenario : dict
        The scenario *dict* where reference to everything created in
        this module will be stored. Since this is the first module
        to call, the *dict* can be empty (or should at least contain
        the key *scenario_name* with the name of the scenario).
    params : dict
        A *dict* containing the content of the config files.

    """

    scenario["seed_max"] = int(cfg["MISC"].get("seed_max", 1_000_000))
    scenario["output_path"] = cfg["PATHS"]["output_prefix"]
    scenario["data_path"] = params.setdefault(
        "data_path", cfg["PATHS"]["data_path"]
    )
    os.makedirs(scenario["output_path"], exist_ok=True)
    scenario["step_size"] = int(params.setdefault("step_size", 15 * 60))
    scenario["start_date"] = params.setdefault(
        "start_date",
        "2020-01-01 00:00:00+0100",
    )
    scenario["end"] = int(params.setdefault("end", 1 * 24 * 60 * 60))
    scenario["cos_phi"] = params.setdefault("cos_phi", 0.9)
    scenario["with_db"] = params.setdefault("with_db", False)
    scenario["deny_rng"] = params.setdefault("deny_rng", False)
    scenario["mosaik_params"] = params.setdefault("mosaik_params", dict())
    scenario["forecast_horizon_hours"] = params.setdefault(
        "forecast_horizon_hours", 0.25
    )
    scenario["flexibility_horizon_hours"] = params.setdefault(
        "flexibility_horizon_hours", params["forecast_horizon_hours"]
    )
    scenario["use_ict"] = params.setdefault("use_ict", False)
    scenario.setdefault(
        "world",
        mosaik.World(
            sim_config=dict(), mosaik_config=scenario["mosaik_params"]
        ),
    )

    scenario["sensors"] = params.setdefault("sensors", list())
    scenario["actuators"] = params.setdefault("actuators", list())

    # RNG master switch
    if scenario["deny_rng"]:
        # We have random numbers, we just won't use them
        scenario["rng"] = np.random.RandomState()
        return scenario

    if "random_state" in params:
        with open(params["random_state"], "rb") as state_f:
            random_state = pickle.load(state_f)
        scenario["rng"] = np.random.RandomState()
        scenario["rng"].set_state(random_state)
    elif "seed" in params and params["seed"] is not None:
        if isinstance(params["seed"], int):
            scenario["rng"] = np.random.RandomState(params["seed"])
        else:
            scenario["rng"] = np.random.RandomState()

        state_fname = os.path.join(
            scenario["output_path"],
            f"{scenario['scenario_name']}.random_state",
        )
        with open(state_fname, "wb") as state_f:
            pickle.dump(scenario["rng"].get_state(), state_f)

        params["random_state"] = state_fname

    else:
        scenario["rng"] = np.random.RandomState()

    script = {
        "imports": list(),
        "definitions": list(),
        "simconfig": list(),
        "sim_start": ["world = mosaik.World(sim_config)\n"],
        "model_start": list(),
        "connects": list(),
        "world_start": ["world.run(until=end)\n"],
    }
    script["imports"].append("import mosaik\n")
    # script["imports"].append("from mosaik.util import connect_many_to_one\n")
    script["imports"].append("import numpy as np\n")
    for key, value in scenario.items():
        if key in ("world", "rng", "sensors", "actuators"):
            continue

        if isinstance(value, str):
            script["definitions"].append(f'{key} = "{value}"\n')
        else:
            script["definitions"].append(f"{key} = {value}\n")

    script["definitions"].append(
        f'rng = np.random.RandomState({params.get("seed", None)})\n'
    )

    scenario["script"] = script
    return scenario
