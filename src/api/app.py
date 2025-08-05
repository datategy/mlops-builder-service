import traceback

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from .routes.deployment import router as deployment_router
from .routes.gitlab_callbacks import router as gitlab_callbacks_router

app = FastAPI()
app.include_router(deployment_router)
app.include_router(gitlab_callbacks_router)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    traceback_ = "\n".join(traceback.format_exception(exc))
    return PlainTextResponse(traceback_, status_code=500)
