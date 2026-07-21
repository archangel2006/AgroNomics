# Local setup and running guide

This guide helps you run AgroNomics locally and prepare the trained model files the Flask app expects.

## 1. Prerequisites

- Python 3.10+ recommended
- pip
- A terminal with network access to install packages

## 2. Clone and enter the project

```bash
git clone https://github.com/archangel2006/Agronomics
cd AgroNomics
```

## 3. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

## 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

If the install fails, try upgrading pip first:

```bash
python -m pip install --upgrade pip
```

## 5. Prepare the model artifacts

The application loads these files at startup:

- model.pkl
- encoder.pkl

These are created from the notebook workflow in AgroNomics.ipynb. The notebook contains the export logic that saves both files with joblib.

### Option A: Train and export from the notebook

1. Open AgroNomics.ipynb in Jupyter or VS Code Notebook mode.
2. Run the cells in order until the training and export section.
3. Make sure the notebook saves:

```python
import joblib
joblib.dump(rf_model, "model.pkl")
joblib.dump(encoder, "encoder.pkl")
```

4. Keep the generated files in the project root folder.

### Option B: Use the sample notebook outputs

The repository also contains sample model notebooks in the sample_models folder. If the main notebook cannot be executed locally, you can use those as reference for the training pipeline, but you still need a working model.pkl and encoder.pkl in the project root for the Flask app to run.

## 6. Verify required files

From the project root, confirm that these files exist:

```bash
dir model.pkl encoder.pkl
```

## 7. Start the Flask app

```bash
python app.py
```

The app should be available at:

```text
http://127.0.0.1:5000
```

## 8. Common local issues

### Module import errors

If you see missing package errors, reinstall dependencies:

```bash
pip install -r requirements.txt
```

### Model loading errors

If the app fails with a model loading error, confirm that:

- model.pkl exists in the project root
- encoder.pkl exists in the project root
- the files were created with the same preprocessing logic used by app.py

### Port already in use

If port 5000 is busy, either stop the conflicting process or run:

```bash
python app.py
```

If you want to bind to another port in a custom environment, update the Flask run command accordingly.
