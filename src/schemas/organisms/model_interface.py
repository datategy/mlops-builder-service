from pydantic import BaseModel

from src.models.model_interface import ModelInterface
from src.models.model_interface_config import ModelInterfaceConfig

from ..atoms.use_case_enum import UseCase
from ..molecules.model import Model


class NewModelInterface(BaseModel):
    use_case: UseCase
    """Use case for the model interface."""
    config: dict
    """Configuration for the model interface."""
    model: Model
    """First model to build and deploy in the model interface."""

    def create_db_model(self):
        """Create a database model from the current model interface."""
        model_interface_config = ModelInterfaceConfig(config=self.config)
        model = self.model.create_db_model()

        return ModelInterface(
            use_case=self.use_case, configs=[model_interface_config], deployed_models=[model]
        )
