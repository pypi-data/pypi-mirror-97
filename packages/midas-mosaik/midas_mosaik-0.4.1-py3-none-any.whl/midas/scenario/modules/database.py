"""MIDAS scenario upgrade module.

This module adds a mosaikhdf database to the scenario.

"""
import os


def upgrade(scenario, params):
    """Add a mosaikhdf database to the scenario."""
    if scenario["with_db"]:
        _add_db(scenario, params)

    return scenario


def _add_db(scenario, params):
    """Create the database in the mosaik world."""

    # Check params
    db_params = params.setdefault("mosaikdb_params", dict())
    db_params.setdefault("sim_name", "MosaikDB")
    db_params.setdefault("cmd", "python")
    db_params.setdefault("import_str", "mosaik_hdf5:MosaikHdf5")
    db_params.setdefault("step_size", scenario["step_size"])
    db_params.setdefault("filename", "midasmv.hdf5")
    if db_params["filename"] is not None:
        db_params["filename"] = os.path.join(
            scenario["output_path"], db_params["filename"]
        )

    if "mosaik" in db_params["import_str"]:
        scenario["db_restricted"] = True
    else:
        scenario["db_restricted"] = False

    # Some definitions
    world = scenario["world"]
    sim_key = "mosaikdb_sim"
    mod_key = "database"

    # Add to sim config
    world.sim_config[db_params["sim_name"]] = {
        db_params["cmd"]: db_params["import_str"]
    }

    # Start simulator
    scenario[sim_key] = world.start(
        db_params["sim_name"],
        step_size=db_params["step_size"],
        duration=scenario["end"],
    )

    # Start model
    database = scenario[sim_key].Database(filename=db_params["filename"])

    # Save the reference
    scenario["database"] = database

    # Add to auto script
    scenario["script"]["definitions"].append(
        f'{mod_key}_filename = "{db_params["filename"]}"\n'
    )
    scenario["script"]["simconfig"] = f"sim_config = {world.sim_config}\n"

    scenario["script"]["sim_start"].append(
        f'{sim_key} = world.start("{db_params["sim_name"]}", '
        f"step_size=step_size, duration=end)\n"
    )

    scenario["script"]["model_start"].append(
        f"{mod_key} = {sim_key}.Database(filename=database_filename)\n"
    )
