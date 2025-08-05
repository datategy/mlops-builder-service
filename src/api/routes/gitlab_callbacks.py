import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException
from pydantic import Field

from src.models.deployed_model import DeployedModel
from src.models.model_interface import ModelInterface
from src.schemas.molecules.gitlab_callbacks import (
    ModelInstanceStatusUpdate,
    ModelInterfaceStatusUpdate,
)
from src.utils.database import session_manager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["gitlab"])


@router.get("/gitlab_callbacks/new_deployment/{deployment_id}")
async def new_deployment_callback(
    deployment_id: int,
    status_update: Annotated[
        ModelInstanceStatusUpdate | ModelInterfaceStatusUpdate, Field(discriminator="update_for")
    ],
    gitlab_pipeline_id: int | None = None,
):
    db_model_type: type[DeployedModel] | type[ModelInterface]
    vocab: str
    if isinstance(status_update, ModelInstanceStatusUpdate):
        db_model_type = DeployedModel
        vocab = "model instance"
    elif isinstance(status_update, ModelInterfaceStatusUpdate):
        db_model_type = ModelInterface
        vocab = "model interface"

    with session_manager(autocommit=True) as session:
        db_model: DeployedModel | ModelInterface | None = session.query(db_model_type).get(
            deployment_id
        )

        if db_model is None:
            logger.error(
                f"Could not update {vocab}'s life status to {status_update.status} "
                f"(from pipeline {gitlab_pipeline_id}) because {vocab} "
                f"with ID {deployment_id} was not found in DB."
            )
            return HTTPException(status_code=404, detail=f"{vocab.capitalize()} not found in DB.")

        db_model.life_status = status_update.status
