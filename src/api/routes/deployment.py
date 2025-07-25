from typing import Any

from fastapi import APIRouter

from models.model_interface import ModelInterface
from schemas.organisms.model_interface import NewModelInterface
from src.configurations import get_build_agent_config
from src.configurations.default_interface_config import DEFAULT_MODEL_INTERFACE_CONFIG
from src.services.artefacts import RunArtefacts
from src.services.gitlab import GitLabAgent
from src.services.inference_code import InferenceCode
from src.utils.database import session_manager

router = APIRouter(tags=["model_interface"])


@router.post("/model-interface")
async def create_new_model_interface(model_interface: NewModelInterface):
    model_interface_db = model_interface.create_db_model()
    with session_manager() as session:
        session.add(model_interface_db)
        session.flush()
        model_interface_db.compute_slug()

    inference_code = InferenceCode(
        model_interface_db.models[0].artefacts_folder, model_interface_db.use_case
    )
    inference_code.copy_inference_code()

    artefacts = RunArtefacts(model_interface_db.models[0].artefacts_folder)
    artefact_paths = artefacts.get_artefact_paths()
    artefact_paths.append(inference_code.inference_code_folder)

    inference_code_requirements = inference_code.get_requirements()
    model_requirements = artefacts.get_requirements()
    requirements = inference_code_requirements + model_requirements

    pipeline_inputs = {
        "response_url": "URL_OF_MLOPS_BUILDER_SERVICE",
        "model_slug": model_interface_db.slug,
        "model_python_version": artefacts.get_python_version(),
        "model_instance_include_remote_artefacts_paths": artefact_paths,
        "model_instance_requirements": requirements,
        "model_instance_python_cmd": "python3 /app/entrypoint.py",
        "model_interface_config_yaml": "",
    }

    model_instance_pipeline_config = get_build_agent_config().model_instance
    gitlab_agent = GitLabAgent(
        url=model_instance_pipeline_config.host,
        project_id=model_instance_pipeline_config.project_id,
        trigger_token=model_instance_pipeline_config.trigger_token,
        ref=model_instance_pipeline_config.ref,
    )
    gitlab_agent.trigger_pipeline(inputs=pipeline_inputs)

    config = DEFAULT_MODEL_INTERFACE_CONFIG | {"model_collection": {"models": [...]}}


@router.patch("model-interface/{model_interface_id}")
async def update_model_interface(model_interface_id: int, updated_model_interface: Any):
    with session_manager() as session:
        model_interface_db = session.query(ModelInterface).get(model_interface_id)
        session.add(model_interface_db)

    # check if it requires updating remote model_interface (like updating model weights or multi model mode)
    # send request to model_interface (will be a challenge for queue system)
    # update database data only if pipeline succeded in gitlab
