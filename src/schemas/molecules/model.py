from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from src.models.model import Model as ModelDB


class Model(BaseModel):
    friendly_name: Annotated[str, StringConstraints(max_length=100)]

    weight: float = Field(ge=0, le=1)
    """Weight of the model in the deployment."""

    artefacts_path: Path

    def create_db_model(self):
        return ModelDB(friendly_name=self.friendly_name, artefacts_path=self.artefacts_path)
