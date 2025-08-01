from pathlib import Path

from pydantic import BaseModel, Field

from src.models.deployed_model import DeployedModel
from src.models.deployed_model_weight import DeployedModelWeight


class Model(BaseModel):
    weight: float = Field(ge=0, le=1)
    """Weight of the model in the deployment."""

    artefacts_folder: Path

    def create_db_model(self):
        return DeployedModel(
            artefacts_folder=self.artefacts_folder,
            deployed_model_weights=[DeployedModelWeight(weight=self.weight)],
        )
