from fastapi import APIRouter

from models.model_interface import ModelInterface
from src.models.model import Model
from src.schemas.atoms.life_status_enum import GitLabLifeStatuses
from src.utils.database import session_manager

router = APIRouter(tags=["gitlab"])


@router.get("/gitlab_callbacks/new_deployment/{deployment_id}")
async def new_deployment_callback(
    deployment_id: int, life_status: GitLabLifeStatuses, gitlab_pipeline_id: int | None = None
):
    with session_manager() as session:
        deployment: ModelInterface = session.query(ModelInterface).get(deployment_id)
        deployment.life_status = life_status


@router.get("/gitlab_callbacks/new_model/{model_id}")
async def new_model_callback(
    model_id: int, life_status: GitLabLifeStatuses, gitlab_pipeline_id: int | None = None
):
    with session_manager() as session:
        model: Model = session.query(Model).get(model_id)
        model.life_status = life_status
