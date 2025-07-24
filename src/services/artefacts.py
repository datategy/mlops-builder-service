"""Read main artefact file (MLmodel.yaml and extract required info from it."""

from functools import cached_property
from pathlib import Path

import yaml

from src.schemas.molecules.artefacts.model_metadata import ModelMetadata
from src.schemas.molecules.artefacts.python_env import PythonEnv

from .remote_storage import get_fs

MAIN_MODEL_ARTEFACT_NAME = "MLmodel.yaml"

REQUIREMENTS_FILE_NAME = "requirements.txt"


class RunArtefacts:
    def __init__(self, artefact_path: Path):
        self.artefact_path = artefact_path
        self.ml_model_artefact_path = self.artefact_path / MAIN_MODEL_ARTEFACT_NAME

    @cached_property
    def model_metadata(self) -> ModelMetadata:
        with get_fs().open_for_reading(self.ml_model_artefact_path, text=True) as file:
            ml_model_data = yaml.safe_load(file)

        return ModelMetadata.model_validate(ml_model_data)

    @cached_property
    def python_env(self) -> PythonEnv:
        virtualenv_path = self.model_metadata.flavors.python_function.env.virtualenv

        with get_fs().open_for_reading(virtualenv_path, text=True) as file:
            virtualenv_data = yaml.safe_load(file)

        return PythonEnv.model_validate(virtualenv_data)

    def get_artefact_paths(self) -> list[Path]:
        artifact_path = self.model_metadata.saved_input_example_info.artifact_path
        serving_input_path = self.model_metadata.saved_input_example_info.serving_input_path
        virtualenv = self.model_metadata.flavors.python_function.env.virtualenv

        additional_flavor_artefact_attributes = (
            self.model_metadata.flavors.additional_flavor.parameters.artefact_attributes
        )
        additional_flavor_artefact_paths = [
            getattr(self.model_metadata.flavors.additional_flavor.parameters, attr)
            for attr in additional_flavor_artefact_attributes
        ]

        return [
            self.ml_model_artefact_path,
            artifact_path,
            serving_input_path,
            virtualenv,
            *additional_flavor_artefact_paths,
        ]

    def get_requirements_path(self) -> Path:
        requirements_path = self.artefact_path / REQUIREMENTS_FILE_NAME
        if not requirements_path.exists():
            raise FileNotFoundError("Requirements file not found in the run's artefacts.")
        return requirements_path

    def get_requirements(self) -> list[str]:
        requirements = []
        requirements.extend(self.python_env.build_dependencies)
        requirements.extend(self.python_env.dependencies)
        return requirements

    def get_python_version(self) -> str:
        return self.python_env.python
