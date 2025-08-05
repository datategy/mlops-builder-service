from typing import Literal

from pydantic import BaseModel

from src.schemas.atoms.life_status_enum import PipelineBuildStatuses, PipelineDeployStatuses


class ModelInterfaceStatusUpdate(BaseModel):
    update_for: Literal["model_interface"]
    status: PipelineDeployStatuses


class ModelInstanceStatusUpdate(BaseModel):
    update_for: Literal["model_instance"]
    status: PipelineBuildStatuses | PipelineDeployStatuses
