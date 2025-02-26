from typing import Any

from fastapi import APIRouter

from models.model_interface import ModelInterface
from schemas.organisms.model_interface import NewModelInterface
from src.utils.database import session_manager

router = APIRouter(tags=["model_interface"])


@router.post("/model-interface")
async def create_new_model_interface(model_interface: NewModelInterface):
    model_interface_db = model_interface.create_db_model()
    with session_manager() as session:
        session.add(model_interface_db)
        session.flush()
        model_interface_db.compute_slug()

    # trigger gitlab model_interface


@router.patch("model-interface/{model_interface_id}")
async def update_model_interface(model_interface_id: int, updated_model_interface: Any):
    with session_manager() as session:
        model_interface_db = session.query(ModelInterface).get(model_interface_id)
        session.add(model_interface_db)

    # check if it requires updating remote model_interface (like updating model weights or multi model mode)
    # send request to model_interface (will be a challenge for queue system)
    # update database data only if pipeline succeded in gitlab
