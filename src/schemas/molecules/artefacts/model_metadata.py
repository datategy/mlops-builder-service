from typing import Literal, TypeAlias

from pydantic import BaseModel, Field, model_serializer, model_validator

from src.utils.pydantic import PathSerializedAsStr

JsonStr: TypeAlias = str


class Signature(BaseModel):
    inputs: JsonStr
    outputs: JsonStr
    params: JsonStr | None = None


class SavedInputExampleInfo(BaseModel):
    artifact_path: PathSerializedAsStr
    """
    Path to a json file that contains the input example.

    For an LLM, it could be : `[{"role": "user", "content": "Hello"}]`
    For Tabular ML : `{"columns": ["sepal length (cm)", "sepal width (cm)"], "data": [[5.1, 3.5]]}`
    """
    serving_input_path: PathSerializedAsStr
    """Path to a json file that contains how the payload must be when served."""
    type: Literal["dataframe", "json_object"]
    """Type of the example data."""


class Environment(BaseModel):
    virtualenv: PathSerializedAsStr
    """Path to the virtual environment file."""


class BaseFlavour(BaseModel):
    pass


class FlavorPythonFunction(BaseFlavour):
    python_version: str
    """Python version used to create the model."""
    env: Environment


class FlavorSklearn(BaseFlavour):
    pickled_model: PathSerializedAsStr
    """Path to the pickled model file."""
    serialization_format: Literal["joblib"] = "joblib"
    """Serialization format of the model."""
    sklearn_version: str
    """Version of scikit-learn used to create the model."""
    artefact_attributes: list[str] = Field(default=["pickled_model"], frozen=True)


class FlavorPytorch(BaseFlavour):
    model_data: PathSerializedAsStr
    """Path to the model data folder."""
    pytorch_version: str
    """Version of PyTorch used to create the model."""
    artefact_attributes: list[str] = Field(default=["model_data"], frozen=True)


class AdditionalFlavor(BaseModel):
    name: str
    """Name of the additional flavor."""
    parameters: FlavorSklearn | FlavorPytorch
    """Parameters of the additional flavor."""


class Flavors(BaseModel):
    python_function: FlavorPythonFunction
    additional_flavor: AdditionalFlavor

    @model_serializer()
    def serialize_additional_flavor(self) -> dict:
        return {
            "python_function": self.python_function.model_dump(),
            self.additional_flavor.name: self.additional_flavor.parameters.model_dump(),
        }

    @model_validator(mode="before")
    @classmethod
    def validate_flavors(cls, obj: dict | object) -> dict | object:
        """Makes the validation compatible with the output of the serializer.

        If the object is a dict, it is assumed to be the output of the serializer.
        It will then be transformed to a format compatible with AdditionalFlavor.

        Parameters
        ----------
        obj : dict | object
            object to validate.
        """
        if isinstance(obj, dict):
            if "additional_flavor" in obj:
                # data already in the right format
                return obj

            for key, value in obj.items():
                if key == "python_function":
                    continue

                obj["additional_flavor"] = {}
                obj["additional_flavor"]["name"] = key
                obj["additional_flavor"]["parameters"] = value

                return obj

        return obj


class ModelMetadata(BaseModel):
    metadata_version: int = 1
    model_size_bytes: int
    """Size of the stored model in bytes."""
    signature: Signature
    """signature of the model's I/O."""
    saved_input_example_info: SavedInputExampleInfo
    """Example of input data that can be used to test the model."""
    flavors: Flavors
