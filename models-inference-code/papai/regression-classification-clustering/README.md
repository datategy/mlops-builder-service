# How to generate a joblib model

In `papai-ml` repository,

- go to `tests/internal/pipelines/prediction/`
- choose the model of your liking (e.g. `test_classification_binary_pred.py`)
- find the function `make_model_info`
- at the end of the function, add the following code:

```python
    import joblib

    with open("model_info.joblib", "wb") as f:
        joblib.dump(model_info, f)
```

# How to use a joblib model

- copy the joblib file here
- edit the host paths in Dockerfile if required
