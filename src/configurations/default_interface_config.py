DEFAULT_MODEL_INTERFACE_CONFIG = {
    "inference_listener": {"service_name": "webapi"},
    "input_data": {
        "structure": [
            {
                "data_type": "TabularData",
                "name": "features",
                "preprocessings": [{"service_name": "uniformize-tabular-data"}],
            }
        ]
    },
    "output_data": {"aggregation": {"type": "polling"}},
    "data_storage_backend": {"type": "database"},
    "feedback": {
        "type": "ground_truth",
        "sample_ids": {
            "generation_algorithm": "base62_uuid",
            "number_of_samples": {"infer_from_tabular_data": True, "structure_name": "features"},
        },
    },
    "stats_backend": {"type": "database"},
}
