# Model hosting and artifact guide

This document explains how to make the AgroNomics model usable when the large notebook cannot be loaded directly in a deployment environment.

## 1. Why the model needs extra artifacts

The Flask app expects two files at runtime:

- model.pkl
- encoder.pkl

These files are produced by the training notebook and are required because the backend uses them to transform input values and run the prediction.

## 2. Where the notebook creates them

In AgroNomics.ipynb, the training workflow saves the artifacts with:

```python
import joblib
joblib.dump(rf_model, "model.pkl")
joblib.dump(encoder, "encoder.pkl")
```

The notebook also includes a download section that exports them from the environment.

## 3. Recommended workflow for hosting

### Option 1: Export locally and copy to the app server

1. Open AgroNomics.ipynb.
2. Run the training cells.
3. Export or download model.pkl and encoder.pkl.
4. Copy both files into the project root of the deployed app.

### Option 2: Train in a notebook environment and upload artifacts

If the notebook is too large to run on the target host:

- train the model in a separate environment
- save the artifacts
- upload them to the deployment environment

### Option 3: Move the model to a dedicated model API

If the model becomes too large or you want better scaling:

- keep model.pkl and encoder.pkl in a separate service
- expose a /predict endpoint there
- let the Flask app call that API

## 4. Encoder requirement

The encoder is essential because the app transforms categorical values like category, crop, state, district, and season before prediction.

If you use a different encoder or a different preprocessing pipeline, the deployed app must use the exact same transformation logic. Otherwise, predictions will fail or become incorrect.

## 5. File placement

The app looks for the files in the same folder as app.py. Keep the structure like this:

```text
AgroNomics/
  app.py
  model.pkl
  encoder.pkl
  templates/
  static/
```

## 6. Deployment note for large notebooks

If the main notebook cannot be loaded because of memory or environment constraints:

- use a machine with more compute
- run only the training cells needed for export
- save the artifacts first
- deploy the artifacts instead of the whole notebook

## 7. Suggested production hosting pattern

A reliable production pattern is:

1. Train and export the model artifacts offline.
2. Store the artifacts in a secure location.
3. Mount or copy them into the app container or server.
4. Start the Flask app so it loads them at runtime.

## 8. Troubleshooting

### The app crashes on startup

Check whether:

- model.pkl is present
- encoder.pkl is present
- both files are readable
- the files were generated with the same version of the preprocessing pipeline

### Predictions fail with encoding errors

This usually means the encoder saved from the notebook does not match the expected input columns or the app is receiving values the encoder did not see during training.

### The model is too large for the app instance

Consider moving the inference logic to a separate service or storing the model artifacts in object storage.
