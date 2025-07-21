from pathlib import Path

import yaml

from src.utils.storage import fs

ML_MODEL_ARTEFACT_NAME = "MLmodel.yaml"


def read_ml_model_artefact(artefacts_path: Path):
    ml_model_artefact_path = artefacts_path / ML_MODEL_ARTEFACT_NAME
    with fs().open_for_reading(ml_model_artefact_path, mode="r") as file:
        ml_model_data = yaml.safe_load(file)
    return ml_model_data
