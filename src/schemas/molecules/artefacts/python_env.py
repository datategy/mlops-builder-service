from pydantic import BaseModel


class PythonEnv(BaseModel):
    python: str
    """Python version used to create the virtual environment."""
    build_dependencies: list[str]
    """List of build dependencies required to create the virtual environment."""
    dependencies: list[str]
    """List of dependencies to install in the virtual environment."""
