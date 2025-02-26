from enum import StrEnum, auto


class MultiModelMode(StrEnum):
    RANDOM = auto()
    """Use a random model for each prediction."""
    AVERAGE = auto()
    """Average the predictions of all models."""
    POLL = auto()
    """
    Poll all models and take the most frequent answer. If multiple models have
    the same frequency, the first one is taken.
    """
    SINGLE = auto()
    """Use a single model. Weights should be a one-hot vector."""
