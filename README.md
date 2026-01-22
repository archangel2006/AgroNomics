# AgroNomics - Crop Price Prediction Model 🌾

**Empowering Farmers with Data-Driven Insights**

A web-based machine learning application that predicts crop prices to help farmers make informed selling decisions and reduce dependency on middlemen.

![AgroNomics Banner](https://img.shields.io/badge/AgroNomics-Crop%20Price%20Predictor-green)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![License](https://img.shields.io/badge/license-Proprietary-red)

---
## 🎯 Problem 
Farmers face significant financial losses due to unpredictable crop prices, lack of reliable forecasting tools, and decisions based on guesswork rather than data-driven insights.

## 💡 Solution
AgroNomics is a web-based machine learning platform that predicts upcoming crop prices using historical datasets and advanced regression models. It provides a clean, intuitive interface designed for farmers, offering state and district-level insights across multiple crop categories in India.

## ✨ Key Features
- **Accurate Price Prediction**: Forecasts crop prices based on state, district, season, and crop type using advanced ML models.
- **Extensive Crop Database**: Covers 9 major crop categories with 200+ commodities, including grains, pulses, vegetables, fruits, spices, and cash crops.
- **Nationwide Coverage**: Supports all 28 states, 8 union territories, and 700+ districts across India.
- **Seasonal Intelligence**: Considers seasonal variations (Zaid, Kharif, Post-Monsoon, and Rabi) for precise predictions.

## 📈 Market Impact
- **AgriTech Growth**: $30.6B (2024) → $79.7B (2030) globally, with India projected to reach $24-30B by 2027 (~50% CAGR).
- **Key Benefits**:
  - Reduces farmer losses due to price volatility  
  - Promotes data-driven agriculture  
  - Decreases dependency on middlemen
 
    
**Scroll down to see web interface and model details**
---
## 🛠️ Tech Stack

| Technology       | Purpose                          |
|------------------|----------------------------------|
| **Python 3.13**  | Core logic & scripting           |
| **Pandas, NumPy**| Data processing & computation    |
| **scikit-learn** | ML models (Random Forest, DT)    |
| **Flask**        | Web backend & REST API           |
| **Joblib**       | Model serialization              |
| **HTML/CSS/JS**  | Frontend interface               |

- **Dataset**: https://www.kaggle.com/datasets/syedjaferk/agriculture-commodity-data-2019
--- 

## 🚀 Installation & Setup

### Prerequisites:
- Python 3.11+
- `pip` (Python package installer)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AgroNomics.git
   cd AgroNomics
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate       # For Linux/Mac
   venv\Scripts\activate          # For Windows
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
4. **Add Model Files**
   Run Agronomics.ipynb
   Place your model.pkl and encoder.pkl files inside the project directory.
   (Ensure these files are present for predictions to work.)
5. **Run the Flask App**
   python app.py
Your app will be available at: http://127.0.0.1:5000
---

## 📁 Project Structure
        .
        └── AgroNomics/
            ├── assets/
            │   ├── agridata.csv    (original dataset from Kaggle)
            │   ├── cleaned_agridata.csv   (cleaned dataset for model building)
            │   └── crops.docx
            ├── static     (frontend styling & logic)/
            │   ├── css/
            │   │   └── style.css
            │   └── js/
            │       └── script.js
            ├── templates   (frontend structure)/
            │   ├── about.html
            │   ├── copyright.html
            │   ├── home.html
            │   └── result.html
            ├── requirements.txt
            ├── AgroNomics.ipynb  (final model code)
            ├── model.plk      (final model)
            ├── encoder.plk   (encoding for model)
            ├── app.py         (Flask API)
            ├── LICENSE
            └── README.md

---
## 🏗️ System Architecture
User Input → Flask Backend → ML Model → Price Prediction → Web Interface
- **User Input**: State, District, Crop Category, Crop, Month, Season.
- **Backend (Flask)**: Processes input and calls the ML model.
- **ML Model (Random Forest)**: Predicts the crop price using trained data.
- **Price Prediction**: Returns modal price per kilogram.
- **Web Interface**: Displays the results in a clean and user-friendly manner. Print Result.

## 🎮 Usage 
1. Open the homepage.
2. Select State, District, Crop Category, Crop, Month, and Season.
3. Click "Predict Price" to view the estimated price (₹/kg).

   <img width="1920" height="1080" alt="photo-collage png (10)" src="https://github.com/user-attachments/assets/df427b9c-db99-443e-9728-7676f27a551d" />

## 🧠 Model Details
- **Dataset**: https://www.kaggle.com/datasets/syedjaferk/agriculture-commodity-data-2019
- **Algorithm**: Random Forest Regression with fallback prediction system
- **Features**: Category, Crop, State, District, Month, Season
- **Encoding**: Ordinal Encoding for categorical variables
- **Fallback System**: Rule-based predictions when ML models unavailable
- **Accuracy**:  ~88% on cleaned dataset (~40k entries)

## 📊 Model Performance

| Metric | Value  |
|--------|--------|
| **MAE**   | 3.25   |
| **RMSE**  | 5.64   |
| **R²**    | 0.88   |

**Top Features (by importance):** Crop > Category > State > District > Month > Season

- <img width="960" height="540" alt="image" src="https://github.com/user-attachments/assets/b867ce23-e230-4f34-9f8f-2395b6e5b14f" />

---
## 🔧 Troubleshooting
- **Model Loading Error**: Ensure `model.pkl` and `encoder.pkl` are in the project directory.  
- **Missing Templates**: All HTML files must be in the `templates/` folder. 
- **Port in Use**: Stop other processes or use `python app.py --port=5001`.

---
## 👥 Team Celebi

| Name | Role | Contact |
|------|------|---------|
| **Vaibhavi Srivastava** | ML Developer | [GitHub](https://github.com/archangel2006) |
| **Sangini Garg** | Web Developer |  [GitHub](https://github.com/Sanginiux) |








