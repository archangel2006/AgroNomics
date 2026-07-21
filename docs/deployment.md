# Deployment and hosting guide

This document explains how to host AgroNomics in a production-style environment, including the model, backend API, and frontend flow.

## 1. Deployment architecture

A working deployment needs three pieces:

1. Frontend UI
   - The Flask templates in the templates folder render the web form.
   - The app serves the UI from the main Flask app.

2. Backend API
   - app.py handles form submission and prediction requests.
   - The backend loads model.pkl and encoder.pkl on startup.

3. Model hosting
   - The trained Random Forest model and encoder must be available to the backend at runtime.
   - If the model is too large for the app instance, use a separate model service or object storage plus a lightweight API.

## 2. Model hosting options

### Option A: Keep the model beside the app

This is the simplest setup for local development and small deployments.

- Put model.pkl and encoder.pkl in the project root.
- Ensure the app can read them from the same directory as app.py.

Good for:
- small demos
- hobby deployments
- low-traffic proof-of-concept apps

### Option B: Host the model as a separate API

For larger deployments, expose the model as a dedicated service.

Recommended flow:

- Backend service receives the prediction request.
- Backend sends the feature payload to the model API.
- Model API returns the price prediction.

This is better when:
- the model size is large
- you want to scale the model independently
- multiple apps need the same model

### Option C: Use cloud storage for model artifacts

Store model.pkl and encoder.pkl in cloud storage such as:

- AWS S3
- Azure Blob Storage
- Google Cloud Storage

Then download or mount them in your runtime environment before starting the app.

## 3. Recommended deployment setup

For a simple production deployment, use:

- Flask backend for web UI and prediction endpoint
- A Linux server or container host
- A persistent volume or mounted storage for model files
- Environment variables for model paths if you want flexible deployment

## 4. Deployment checklist

Before deploying, verify:

- Python dependencies are installed
- model.pkl exists in the runtime environment
- encoder.pkl exists in the runtime environment
- app.py can load the model files successfully
- the frontend form is sending the expected fields

## 5. Example deployment flow

### Step 1: Prepare the model files

Export the artifacts from the notebook:

```python
import joblib
joblib.dump(rf_model, "model.pkl")
joblib.dump(encoder, "encoder.pkl")
```

### Step 2: Upload the project files

Deploy the repository contents including:

- app.py
- templates/
- static/
- requirements.txt
- model.pkl
- encoder.pkl

### Step 3: Install dependencies on the server

```bash
pip install -r requirements.txt
```

### Step 4: Start the app

```bash
python app.py
```

For a production-style deployment, use a process manager or container runtime instead of running the dev server directly.

## 6. Important note about the notebook model

The big AgroNomics.ipynb notebook contains the full training workflow and the code that saves the model and encoder. If the notebook cannot be loaded in your deployment environment, the app still needs the exported artifacts to work.

In that case, you should:

- run the notebook on a machine with enough memory
- export model.pkl and encoder.pkl
- copy those files into the deployed app directory

## 7. Frontend and backend integration

The current frontend flow is:

1. User loads the form from the Flask route /
2. User submits category, crop, state, district, month, and season
3. app.py transforms the categorical values using encoder
4. The trained model predicts a price
5. The result page displays the output

This means the deployment must keep the Flask backend and the templates together. If you split the frontend and backend later, the prediction endpoint should remain compatible with the same payload structure.

## 8. Suggested production hardening

To make deployment more reliable:

- use a proper WSGI server such as Gunicorn
- set environment variables for the model paths
- add health checks
- log prediction errors clearly
- keep model files in a mounted volume or object storage
- add a fallback response if the model is unavailable
