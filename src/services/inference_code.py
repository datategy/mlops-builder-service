import logging
from pathlib import Path
from typing import cast

from src.schemas.atoms.use_case_enum import UseCase

from .remote_storage import get_fs

logger = logging.getLogger(__name__)

INFERENCE_CODE_ARTEFACT_FOLDER = Path("serving")
"""Name of the run's artefact folder where inference code is stored."""

DEFAULT_INFERENCE_CODE_PATH = Path("models-inference-code")
REG_CLASS_CLUST_INFERENCE_CODE_PATH = (
    DEFAULT_INFERENCE_CODE_PATH / "papai" / "regression-classification-clustering"
)

REQUIREMENTS_FILE_NAME = "requirements.txt"

map_use_case_to_inference_code_path = {
    UseCase.REGRESSION: REG_CLASS_CLUST_INFERENCE_CODE_PATH,
    UseCase.BINARY_CLASSIFICATION: REG_CLASS_CLUST_INFERENCE_CODE_PATH,
    UseCase.MULTI_CLASSIFICATION: REG_CLASS_CLUST_INFERENCE_CODE_PATH,
}


class InferenceCode:
    def __init__(self, artefact_path: Path, use_case: UseCase):
        """
        Parameters
        ----------
        artefact_path : Path
            path to the remote run's artefacts folder.
        use_case : UseCase
            use case of the model for inference code.
        """
        self.inference_code_folder = artefact_path / INFERENCE_CODE_ARTEFACT_FOLDER
        self.use_case = use_case

    def copy_inference_code(self):
        """Copy inference code from local path to remote storage."""
        fs = get_fs()

        if self.inference_code_exists():
            raise FileExistsError(
                "Inference code artefact already exists. "
                "Please remove it before copying new inference code."
            )

        local_inference_code_path = self.get_inference_code_path()
        fs.put(
            (local_inference_code_path / "**").as_posix(),
            self.inference_code_folder.as_posix(),
            recursive=True,
        )

    def inference_code_exists(self):
        """check if inference code artefact already exists in remote storage."""
        return get_fs().exists(self.inference_code_folder.as_posix())

    def get_remote_requirements_path(self):
        """check if remote requirements artefact already exists in remote storage."""
        requirements_path = self.inference_code_folder / REQUIREMENTS_FILE_NAME
        if not get_fs().exists(requirements_path.as_posix()):
            logger.error(
                f"Remote requirements file not found in the inference code artefact folder {self.inference_code_folder}."
            )
            raise FileNotFoundError(
                "Remote requirements file not found in the root of remote artefact folder."
            )

        return requirements_path

    def get_requirements(self) -> list[str]:
        """Get the requirements from the remote requirements file."""
        requirements_path = self.get_remote_requirements_path()
        with get_fs().open_for_reading(requirements_path.as_posix(), text=True) as file:
            # because text=True, this is a list of strings
            requirements = cast(list[str], file.readlines())
        return requirements

    def get_inference_code_path(self) -> Path:
        """Get the path to one of the default inference code artefacts."""
        if self.use_case not in map_use_case_to_inference_code_path:
            raise ValueError(
                f"Unsupported use case: {self.use_case}. Supported use cases are:"
                f"{list(map_use_case_to_inference_code_path.keys())}"
            )
        return map_use_case_to_inference_code_path[self.use_case]
