# PapAI Models Inference Code

This folder holds the inference code for the models trained in PapAI.

When deployed with our deployment solution, this code will handle:

- model loading
- model prediction
- model unloading (optional, could be used for memory optimization when there is no prediction to make).

It is kept very basic to avoid bugs as much as possible since a bug at that level is quite hard to fix. Indeed, model instances are built in a particular context (requirements, weights, etc.) so doing a fix in there would mean we would have to rebuild and redeploy everything.

## Requirements system

All the files matching the regex `requirements-*.txt` will be installed.

For models trained in PapAI, there are three level of requirements:

- requirements for running the webserver (common for all models)
- requirements for loading the model (common for all models)
- requirements for running the model (specific for all models)

## Run a built model

If you want to run a deployed model:

- you need to build it first with `docker build -f models-inference-code/papai/regression-classification-clustering/Dockerfile models-inference-code/ -t image_name:tag`
- Then you can launch the command `docker run -p host_port:8000 -d image-name:tag`
