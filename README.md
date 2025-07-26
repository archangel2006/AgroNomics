# AgroNomics - Crop Price Prediction Model 🌾

**Empowering Farmers with Data-Driven Insights**

A web-based machine learning application that predicts crop prices to help farmers make informed selling decisions and reduce dependency on middlemen.

![AgroNomics Banner](https://img.shields.io/badge/AgroNomics-Crop%20Price%20Predictor-green)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![License](https://img.shields.io/badge/license-Proprietary-red)


## 🎯 Problem Statement

- Farmers suffer significant losses due to unpredictable crop prices
- Lack of forecasting tools tailored to local agriculture
- Decisions based on guesswork instead of data-driven insights
- Heavy dependency on middlemen for price information

## 💡 Solution

AgroNomics provides a comprehensive web-based ML tool that:
- Forecasts crop prices for upcoming periods
- Uses historical datasets and regression models
- Offers a simple, intuitive interface accessible to farmers
- Covers multiple crop categories across Indian states

## ✨ Key Features

### 🔮 **Price Prediction**
- Predicts crop prices based on location, season, and commodity type
- Covers 9 major crop categories with 200+ commodities
- State and district-wise predictions across India

### 📊 **Comprehensive Database**
- **Grains**: Wheat, Rice, Maize, Millets, Barley, etc.
- **Pulses**: Arhar Dal, Masur Dal, Green Peas, etc.
- **Vegetables**: Onion, Potato, Tomato, Cabbage, etc.
- **Fruits**: Banana, Mango, Apple, Orange, etc.
- **Spices**: Turmeric, Ginger, Garlic, Black Pepper, etc.
- **Cash Crops**: Cotton, Sugarcane, Coffee, Tobacco, etc.

### 🌍 **Geographic Coverage**
- All 28 Indian states and 8 Union Territories
- District-level granularity for precise predictions
- 700+ districts covered

### 🌦️ **Seasonal Intelligence**
- **Summer (Zaid)**: March-June
- **Monsoon (Kharif)**: June-September  
- **Post-Monsoon**: October-November
- **Winter (Rabi)**: December-March

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.13** | Core application logic & scripting |
| **Pandas** | Data handling, aggregation & transformation |
| **scikit-learn** | Machine learning models (Random Forest, Decision Trees) |
| **Flask** | Web framework & REST API |
| **NumPy** | Numerical computations |
| **Joblib** | Model serialization |
| **HTML/CSS/JS** | Frontend interface |

## 🏗️ System Architecture

User Input → Flask Backend → ML Model → Price Prediction → Web Interface
↓ ↓ ↓ ↓ ↓
Location, Data Processing Random Forest Predicted Visual Display
Commodity, & Validation Regression Price & Results
Season


## 🚀 Installation & Setup

### Prerequisites:
- Python 3.11+
- `pip` (Python package installer)


## 📁 Project Structure
.
└── AgroNomics/
    ├── assets/
    │   ├── agridata.csv   # (original dataset from Kaggle)
    │   ├── cleaned_agridata.csv   # (cleaned dataset for model building)
    │   └── crops.docx
    ├── sample_models #(rough models built)/
    │   ├── model1
    │   ├── model2
    │   ├── model3
    │   └── delete.py 
    ├── static   # (frontend styling & logic)/
    │   ├── css/
    │   │   └── style.css
    │   └── js/
    │       └── script.js
    ├── templates  # (frontend structure)/
    │   ├── about.html
    │   ├── copyright.html
    │   ├── home.html
    │   └── result.html
    ├── requirements.txt
    ├── AgroNomics.ipynb  # (final model code)
    ├── model.plk      # (final model)
    ├── encoding.plk   # (encoding for model)
    ├── app.py         # (Flask API)
    ├── LICENSE
    └── README.md

## 🎮 Usage

### Web Interface
1. Visit the homepage
2. Select your **State** and **District**
3. Choose **Commodity Category** and specific **Crop**
4. Select **Month** and **Season**
5. Click **"Predict Price"**
6. View predicted modal price in ₹/quintal

### API Endpoint

**Response:**

## 🧠 Model Details

- **Algorithm**: Random Forest Regression with fallback prediction system
- **Features**: Category, Crop, State, District, Month, Season
- **Encoding**: Ordinal Encoding for categorical variables
- **Fallback System**: Rule-based predictions when ML models unavailable
- **Accuracy**:  ~88% on cleaned dataset (~40k entries)

<img width="341" height="148" alt="image" src="https://github.com/user-attachments/assets/9b7e8410-3903-498d-9d90-1db0df808567" />
<img width="526" height="453" alt="image" src="https://github.com/user-attachments/assets/599efe3f-2da0-4482-abb9-fa417bcd93a6" />


## 📈 Market Impact

### Target Market Size
- **Global AgriTech**: $30.6B (2024) → $79.7B (2030)
- **India AgriTech**: $2B (2023) → $24-30B (2027)
- **Growth Rate**: ~50% CAGR in India

### Benefits
- ✅ Reduces farmer losses from price volatility
- ✅ Enables data-driven selling decisions
- ✅ Decreases dependency on middlemen
- ✅ Promotes precision agriculture adoption

## 🔧 Troubleshooting

### Common Issues
**Model Loading Error**
**Missing Templates**
- Ensure all HTML files are in the `templates/` directory
**Port Already in Use**


## 👥 Team Celebi

| Name | Role | Contact |
|------|------|---------|
| **Vaibhavi Srivastava** | ML Developer |  [GitHub](https://github.com/archangel2006) |
| **Sangini Garg** | Web Developer | [GitHub](https://github.com/Sanginiux) |





