from pydantic import BaseModel


class ArtefactDataset(BaseModel):
    original_dataset_number_of_samples: int
    number_of_samples_dropped_from_original_dataset: int
    train_dataset_number_of_samples: int
    test_dataset_number_of_samples: int
