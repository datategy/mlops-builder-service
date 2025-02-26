from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from src.models.model import Model as ModelDB


class Model(BaseModel):
    friendly_name: Annotated[str, StringConstraints(max_length=100)]

    weight: float = Field(ge=0, le=1)
    """Weight of the model in the deployment."""

    requirements_file: Path
    weight_file: Path
    """Path to the file containing the weights of the model."""
    inference_code_folder: Path

    train_set_parquet_file: Path
    test_set_parquet_file: Path

    def create_db_model(self):
        return ModelDB(
            friendly_name=self.friendly_name,
            requirements_file=self.requirements_file,
            weight_file=self.weight_file,
            inference_code_folder=self.inference_code_folder,
            train_set_parquet_file=self.train_set_parquet_file,
            test_set_parquet_file=self.test_set_parquet_file,
        )

    def get_artifact_paths(self):
        return (
            self.requirements_file,
            self.weight_file,
            self.inference_code_folder,
            self.train_set_parquet_file,
            self.test_set_parquet_file,
        )
