"""
- M represents the number of features
- N represents the number of samples.
- T represents the number of targets (if it applies).
"""

from typing import Annotated

type Length[T] = Annotated[int, T]
type NSamples = type
type MFeatures = type
type TTargets = type


type ListOfLengthNSamples[T] = Annotated[list[T], Length[NSamples]]
type ListOfLengthTTargets[T] = Annotated[list[T], Length[TTargets]]
type DictOfLengthMFeatures[T, V] = Annotated[dict[T, V], Length[MFeatures]]

type FeatureType = str | int | float | bool | None

type TabularMLData = DictOfLengthMFeatures[str, ListOfLengthNSamples[FeatureType]]

type BinaryClassificationPrediction = ListOfLengthNSamples[float] | ListOfLengthNSamples[str]

type RegressionPrediction = ListOfLengthNSamples[float]

type MultiClassificationPrediction = ListOfLengthNSamples[float] | ListOfLengthNSamples[str]

type MultiOutputRegressionPrediction = ListOfLengthNSamples[ListOfLengthTTargets[float]]

type ClusteringPrediction = ListOfLengthNSamples[float] | ListOfLengthNSamples[str]
