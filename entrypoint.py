import uvicorn

from src.configurations.webserver import UvicornConfig

config = UvicornConfig()

uvicorn.run(app="src.api.app:app", host=config.host, port=config.port)
