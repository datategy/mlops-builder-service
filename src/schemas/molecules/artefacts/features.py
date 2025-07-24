from typing import Literal

from pydantic import BaseModel

from src.data_models.molecules.artefacts.features_stats import AllStatsT


class ArtefactFeaturesTransformedWithColumnTransformer(BaseModel):
    """Artefact features after transformation with a column transformer."""

    mapping_feature_to_transformer_class: dict[str, str]
    """map a feature name to the name of the transformer class in the column transformer."""
    mapping_feature_to_transformer_name: dict[str, str]
    """map of a feature name to the name of the transformer in the column transformer."""
    mapping_feature_to_transformed_feature_names: dict[str, list[str]]
    """map of a feature name to the list of its transformed feature names."""


class ArtefactFeatures(BaseModel):
    feature_names: list[str]
    mapping_feature_to_type: dict[str, Literal["numerical", "categorical", "text", "datetime"]]
    mapping_feature_to_test_stats: dict[str, AllStatsT] | Literal["No test set used"]
    preprocessing: ArtefactFeaturesTransformedWithColumnTransformer | None = None
