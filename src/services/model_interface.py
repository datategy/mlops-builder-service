from .gitlab import run_pipeline


def deploy_model_interface(model_slug: str):
    variables = {"command": "build-and-deploy-model-interface", "model-interface-slug": model_slug}
    run_pipeline(variables)
