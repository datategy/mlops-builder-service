from typing import Annotated

from pydantic import BaseModel, StringConstraints

from src.models.deployment_version import DeploymentVersion as DeploymentVersionDB
from src.models.model import Model as ModelDB
from src.models.model_interface import ModelInterface as DeploymentDB
from src.models.versioned_model_weights import VersionedModelWeight as VersionedModelWeightDB

from ..atoms.multi_model_mode_enum import MultiModelMode
from ..atoms.use_case_enum import UseCase
from ..molecules.listener import Listener
from ..molecules.model import Model


class NewModelInterface(BaseModel):
    use_case: UseCase
    friendly_name: Annotated[str, StringConstraints(max_length=100)]
    description: Annotated[str, StringConstraints(max_length=255)]
    feature_names: list[str]
    target_names: list[str]

    listener: Listener

    models: list[Model]

    multi_model_mode: MultiModelMode

    def create_db_model(self):
        versioned_model_weights: list[VersionedModelWeightDB] = []
        models: list[ModelDB] = []
        for model in self.models:
            model_db = model.create_db_model()
            models.append(model_db)
            versioned_model_weights.append(
                VersionedModelWeightDB(model=model_db, weight=model.weight)
            )
        deployment_version = DeploymentVersionDB(
            multi_model_mode=self.multi_model_mode, versioned_model_weights=versioned_model_weights
        )

        deployment = DeploymentDB(
            use_case=self.use_case,
            friendly_name=self.friendly_name,
            description=self.description,
            feature_names=self.feature_names,
            target_names=self.target_names,
            listener=self.listener.create_db_model(),
            models=models,
            deployment_versions=[deployment_version],
        )
        return deployment


class UpdateDeployment(BaseModel):
    friendly_name: Annotated[str, StringConstraints(max_length=100)]
    description: Annotated[str, StringConstraints(max_length=255)]
    models: list[Model]
    multi_model_mode: MultiModelMode
