from pathlib import Path
from typing import Any

from fastapi import APIRouter

from src.models.model_interface import ModelInterface
from src.schemas.organisms.model_interface import NewModelInterface
from src.services.artefacts import read_ml_model_artefact
from src.utils.database import session_manager

router = APIRouter(tags=["model_interface"])


@router.post("/model-deployment/new")
async def create_new_model_interface(model_interface: NewModelInterface):
    model_interface_db = model_interface.create_db_model()
    with session_manager() as session:
        session.add(model_interface_db)
        session.flush()
        model_interface_db.compute_slug()

    for model in model_interface.models:
        ml_model_artefact = read_ml_model_artefact(model.artefacts_path)

        artefacts_to_package: list[Path]

    # trigger gitlab model_interface


@router.patch("model-interface/{model_interface_id}")
async def update_model_interface(model_interface_id: int, updated_model_interface: Any):
    with session_manager() as session:
        model_interface_db = session.query(ModelInterface).get(model_interface_id)
        session.add(model_interface_db)

    # check if it requires updating remote model_interface (like updating model weights or multi model mode)
    # send request to model_interface (will be a challenge for queue system)
    # update database data only if pipeline succeded in gitlab
