    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        category = request.form['category']
        crop = request.form['crop']
        state = request.form['state']
        district = request.form['district']
        month = request.form['month']
        season = request.form['season']
        
        # Call ML API endpoint
        predicted_price = call_ml_prediction_api(category, crop, state, district, month, season)
        
        return render_template('result.html', 
                             category=category,
                             crop=crop,
                             state=state,
                             district=district,
                             month=month,
                             season=season,
                             predicted_price=predicted_price)
    
    except Exception as e:
        return render_template('result.html', error=str(e))

def call_ml_prediction_api(category, crop, state, district, month, season):
    """
    This function will call your ML API
    Replace this with the actual API endpoint provides
    """
    try:
        # Example API call to your ML service
        ml_api_url = "http://localhost:5001/predict"
        
        payload = {
            "category": category,
            "crop": crop,
            "state": state,
            "district": district,
            "month": month,
            "season": season
        }
        
        response = requests.post(ml_api_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('predicted_price', 'N/A')
        else:
            return get_fallback_prediction(category, crop, state, district, month, season)
            
    except requests.exceptions.RequestException:
        return get_fallback_prediction(category, crop, state, district, month, season)

def get_fallback_prediction(category, crop, state, district, month, season):
    """
    Fallback prediction logic with seasonal variations
    """
    base_prices = {
        'Grains': 2500,
        'Vegetables': 1800,
        'Fruits': 3200,
        'Oilseeds': 4500,
        'Pulses': 3800,
        'Flowers': 1200,
        'Fodder/Fiber': 2800,
        'Spices': 8000,
        'Others': 2000
    }
    
    # Seasonal price multipliers based on Indian agricultural patterns
    seasonal_multipliers = {
        'Summer': 1.2,      # Higher prices due to lower supply, irrigation costs
        'Monsoon': 0.9,     # Lower prices during harvest season
        'Post-Monsoon': 1.1, # Moderate prices after harvest
        'Winter': 1.0       # Baseline prices
    }
    
    base_price = base_prices.get(category, 2000)
    seasonal_factor = seasonal_multipliers.get(season, 1.0)
    
    # Add month-specific variation
    month_num = int(month.split('-')[1])
    monthly_factor = 1 + 0.05 * np.sin(2 * np.pi * month_num / 12)
    
    # Add random variation for demo
    variation = np.random.uniform(0.95, 1.05)
    
    predicted_price = int(base_price * seasonal_factor * monthly_factor * variation)
    
    return predicted_price
