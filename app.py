import os
import joblib
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Paths for model and encoder
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
ENCODER_PATH = os.path.join(os.path.dirname(__file__), "encoder.pkl")

# Load model and encoder
rf_model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

# Define feature and categorical columns (must match training)
FEATURE_COLUMNS = ['category', 'crop', 'state', 'district', 'month', 'season']
CATEGORICAL_COLS = ['category', 'crop', 'state', 'district', 'season']

# Complete commodity categories based on your uploaded document
COMMODITY_CATEGORIES = {
    'Grains': ['Wheat', 'Rice', 'Maize', 'Jowar(Sorghum)', 'Millets', 'Ragi (Finger Millet)', 'Rajgir',
             'Barley (Jau)', 'Broken Rice', 'Maida Atta', 'Wheat Atta', 'Kodo Millet(Varagu)', 'Beaten Rice',
             'Sooji', 'Sajje','Hybrid Cumbu', 'T.V. Cumbu', 'Lak(Teora)']
,
    'Pulses': ['Arhar Dal(Tur Dal)', 'Masur Dal', 'Moath Dal', 'Chennangi Dal', 'Green Avare (W)', 'Avare Dal',
             'Peas(Dry)', 'Peas cod', 'Peas Wet', 'Alasande Gram', 'Field Pea', 'Indian Beans (Seam)',
             'Kulthi(Horse Gram)', 'Same/Savi', 'Gram Raw(Chholia)', 'White Peas', 'Arhar (Tur/Red Gram)(Whole)',
             'Mataki','Duster Beans', 'Guar']
,
    'Oilseeds': ['Soyabean', 'Castor Seed', 'Sunflower', 'Groundnut', 'Ground Nut Seed', 'Linseed',
             'Groundnut (Split)', 'Groundnut pods (raw)', 'Safflower', 'Taramira', 'Niger Seed (Ramtil)',
             'Gurellu']
,
    'Vegetables': ['Onion', 'Potato', 'Tomato', 'Cabbage', 'Brinjal', 'Beans', 'Beetroot', 'Bitter gourd',
             'Bottle gourd', 'Capsicum', 'Cauliflower', 'Cluster beans', 'Colacasia', 'Cucumber',
             'Drumstick', 'Green Peas', 'Pumpkin', 'Raddish', 'Ridgeguard(Tori)', 'Ridge gourd(Tori)',
             'Round gourd', 'Snakeguard', 'Snake gourd', 'Sponge gourd', 'Spinach', 'Knool Khol',
             'Leafy Vegetable', 'Turnip', 'Ashgourd', 'Carrot', 'Cowpea(Veg)', 'Green Chilli',
             'Elephant Yam (Suran)', 'Suvarna Gadde', 'Tinda', 'Chow Chow', 'Season Leaves', 'Amaranthus',
             'Mashrooms', 'Mint(Pudina)', 'Methi(Leaves)', 'Thondekai', 'Seemebadnekai', 'Bunch Beans','Sweet Potato', 
             'Sweet Pumpkin', 'Yam', 'Yam (Ratalu)', 'Tapioca','Green Onion', 'Surat Beans (Papadi)', 'White Pumpkin', 'Kartali (Kantola)']
,
    'Fruits': ['Banana', 'Mango', 'Papaya', 'Guava', 'Pomegranate', 'Apple', 'Chikoos(Sapota)', 'Grapes',
             'Litchi', 'Plum', 'Peach', 'Jamun(Narale Hannu)', 'Water Melon', 'Mousambi(Sweet Lime)',
             'Karbuja(Musk Melon)', 'Pear(Marasebu)', 'Banana - Green', 'Papaya (Raw)', 'Mango (Raw-Ripe)',
             'Pineapple', 'Orange', 'Lemon', 'Lime', 'Long Melon(Kakri)', 'Jack Fruit', 'Seetapal',
             'Persimon(Japani Fal)', 'Seetafal', 'Amla(Nelli Kai)', 'Balekai', 'Galgal(Lemon)',
             'Almond(Badam)', 'Walnut', 'Cherry', 'Kinnow']
,
    'Flowers': ['Marigold(loose)', 'Marigold(Calcutta)', 'Chrysanthemum(Loose)', 'Jasmine', 'Tube Rose(Loose)',
             'Rose(Local)','Anthorium']
,
    'Fodder/Fiber/Utility Crop': ['Dry Fodder', 'Green Fodder', 'Dhaincha', 'Sunhemp', 'Lukad', 'Siddota']
    ,
    
    'Spices and Oil': ['Turmeric', 'Turmeric (raw)', 'Ginger(Dry)', 'Ginger(Green)', 'Cummin Seed(Jeera)', 'Garlic',
             'Mustard', 'Mustard Oil', 'Coconut Oil', 'Gingelly Oil', 'Black pepper', 'Cardamoms', 'Cloves',
             'Nutmeg', 'Pepper garbled', 'Pepper ungarbled', 'Tamarind Seed', 'Tamarind Fruit',
             'Dry Chillies', 'Soanf', 'Suva (Dill Seed)', 'Coriander(Leaves)', 'Coriander seed',
             'Ajwan', 'Chili Red', 'Chilli Capsicum', 'Mint(Pudina)', 'Methi Seeds', 'Isabgul (Psyllium)',
             'Betal Leaves','Mace','Toria']
,
    'Cash Crops': ['Coffee', 'Cotton', 'Cotton Seed', 'Rubber', 'Cashewnuts', 'Copra', 'Jute', 'Tobacco',
             'Sugarcane', 'Lint', 'Paddy(Dhan)(Basmati)', 'Paddy(Dhan)(Common)','Tender Coconut', 
             'Arecanut(Betelnut/Supari)', 'Honge seed', 'Bamboo']
,
    'Processed/Value - Added Products' : ['Gur(Jaggery)', 'Sugar', 'Dry Grapes', 'Bran', 'Gramflour']
    
,    
    'Others': ['Amphophalus', 'Antawala', 'Chapparad Avare', 'Cocoa', 'Coconut', 'Coconut Seed', 'Mahua',
             'Myrobolan(Harad)', 'Neem Seed', 'Lotus Sticks', 'Alsandikai', 'Mahedi', 'Thogrikai', 'Ambada Seed',
             'Indian Colza(Sarson)', 'Sabu Dan', 'Sabu Dana', 'Coca', 'Hippe Seed', 'Rose(Loose)'] 

}

# Indian agricultural seasons based on climate and monsoon patterns
SEASONS = {
    'Summer': {
        'name': 'Summer Season (Zaid)',
        'months': ['March', 'April', 'May', 'June'],
        'description': 'Hot, dry conditions with irrigation-dependent crops',
        'characteristics': 'High temperatures, low rainfall, requires artificial irrigation'
    },
    'Monsoon': {
        'name': 'Monsoon Season (Kharif)',
        'months': ['June', 'July', 'August', 'September'],
        'description': 'Southwest monsoon season with heavy rainfall',
        'characteristics': 'High humidity, substantial rainfall, hot and humid conditions'
    },
    'Post-Monsoon': {
        'name': 'Post-Monsoon Season (Late Kharif)',
        'months': ['October', 'November'],
        'description': 'Transition period after monsoon withdrawal',
        'characteristics': 'Moderate temperatures, residual soil moisture, harvesting period'
    },
    'Winter': {
        'name': 'Winter Season (Rabi)',
        'months': ['December', 'January', 'February', 'March'],
        'description': 'Cool, dry winter season with moderate irrigation',
        'characteristics': 'Cool temperatures (15-20°C), minimal rainfall, requires some irrigation'
    }
}

# Complete Indian States with Districts (same as before)
STATES_DISTRICTS = {
    'Andhra Pradesh': [
        'Anantapur', 'Chittoor', 'East Godavari', 'Guntur', 'Krishna', 'Kurnool', 
        'Nellore', 'Prakasam', 'Srikakulam', 'Visakhapatnam', 'Vizianagaram', 
        'West Godavari', 'YSR Kadapa', 'Others'
    ],
    'Arunachal Pradesh': [
        'Anjaw', 'Changlang', 'Dibang Valley', 'East Kameng', 'East Siang', 
        'Kamle', 'Kra Daadi', 'Kurung Kumey', 'Lepa Rada', 'Lohit', 'Longding', 
        'Lower Dibang Valley', 'Lower Siang', 'Lower Subansiri', 'Namsai', 
        'Pakke Kessang', 'Papum Pare', 'Shi Yomi', 'Siang', 'Tawang', 
        'Tirap', 'Upper Siang', 'Upper Subansiri', 'West Kameng', 'West Siang', 'Others'
    ],
    'Assam': [
        'Baksa', 'Barpeta', 'Biswanath', 'Bongaigaon', 'Cachar', 'Charaideo', 
        'Chirang', 'Darrang', 'Dhemaji', 'Dhubri', 'Dibrugarh', 'Goalpara', 
        'Golaghat', 'Hailakandi', 'Hojai', 'Jorhat', 'Kamrup', 'Kamrup Metropolitan', 
        'Karbi Anglong', 'Karimganj', 'Kokrajhar', 'Lakhimpur', 'Majuli', 
        'Morigaon', 'Nagaon', 'Nalbari', 'Dima Hasao', 'Sivasagar', 'Sonitpur', 
        'South Salmara-Mankachar', 'Tinsukia', 'Udalguri', 'West Karbi Anglong', 'Others'
    ],
    'Bihar': [
        'Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 'Bhagalpur', 
        'Bhojpur', 'Buxar', 'Darbhanga', 'East Champaran', 'Gaya', 'Gopalganj', 
        'Jamui', 'Jehanabad', 'Kaimur', 'Katihar', 'Khagaria', 'Kishanganj', 
        'Lakhisarai', 'Madhepura', 'Madhubani', 'Munger', 'Muzaffarpur', 'Nalanda', 
        'Nawada', 'Patna', 'Purnia', 'Rohtas', 'Saharса', 'Samastipur', 'Saran', 
        'Sheikhpura', 'Sheohar', 'Sitamarhi', 'Siwan', 'Supaul', 'Vaishali', 
        'West Champaran', 'Others'
    ],
    'Chhattisgarh': [
        'Balod', 'Baloda Bazar', 'Balrampur', 'Bastar', 'Bemetara', 'Bijapur', 
        'Bilaspur', 'Dantewada', 'Dhamtari', 'Durg', 'Gariaband', 'Gaurela-Pendra-Marwahi', 
        'Janjgir-Champa', 'Jashpur', 'Kabirdham', 'Kanker', 'Kondagaon', 'Korba', 
        'Koriya', 'Mahasamund', 'Mungeli', 'Narayanpur', 'Raigarh', 'Raipur', 
        'Rajnandgaon', 'Sukma', 'Surajpur', 'Surguja', 'Others'
    ],
    'Goa': [
        'North Goa', 'South Goa', 'Others'
    ],
    'Gujarat': [
        'Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 
        'Bhavnagar', 'Botad', 'Chhota Udepur', 'Dahod', 'Dang', 'Devbhoomi Dwarka', 
        'Gandhinagar', 'Gir Somnath', 'Jamnagar', 'Junagadh', 'Kheda', 'Kutch', 
        'Mahisagar', 'Mehsana', 'Morbi', 'Narmada', 'Navsari', 'Panchmahal', 
        'Patan', 'Porbandar', 'Rajkot', 'Sabarkantha', 'Surat', 'Surendranagar', 
        'Tapi', 'Vadodara', 'Valsad', 'Others'
    ],
    'Haryana': [
        'Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Gurugram', 
        'Hisar', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh', 
        'Nuh', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 
        'Sonipat', 'Yamunanagar', 'Others'
    ],
    'Himachal Pradesh': [
        'Bilaspur', 'Chamba', 'Hamirpur', 'Kangra', 'Kinnaur', 'Kullu', 'Lahaul Spiti', 
        'Mandi', 'Shimla', 'Sirmaur', 'Solan', 'Una', 'Others'
    ],
    'Jharkhand': [
        'Bokaro', 'Chatra', 'Deoghar', 'Dhanbad', 'Dumka', 'East Singhbhum', 
        'Garhwa', 'Giridih', 'Godda', 'Gumla', 'Hazaribagh', 'Jamtara', 'Khunti', 
        'Koderma', 'Latehar', 'Lohardaga', 'Pakur', 'Palamu', 'Ramgarh', 'Ranchi', 
        'Sahibganj', 'Seraikela Kharsawan', 'Simdega', 'West Singhbhum', 'Others'
    ],
    'Karnataka': [
        'Bagalkot', 'Bangalore Rural', 'Bangalore Urban', 'Belgavi', 'Ballari', 
        'Bidar', 'Chamarajanagar', 'Chikkaballapur', 'Chikkamagaluru', 'Chitradurga', 
        'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Kalaburagi', 'Hassan', 
        'Haveri', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru', 'Raichur', 
        'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayapura', 
        'Yadgir', 'Others'
    ],
    'Kerala': [
        'Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 
        'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 'Pathanamthitta', 
        'Thiruvananthapuram', 'Thrissur', 'Wayanad', 'Others'
    ],
    'Madhya Pradesh': [
        'Agar Malwa', 'Alirajpur', 'Anuppur', 'Ashoknagar', 'Balaghat', 'Barwani', 
        'Betul', 'Bhind', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 
        'Damoh', 'Datia', 'Dewas', 'Dhar', 'Dindori', 'Guna', 'Gwalior', 'Harda', 
        'Hoshangabad', 'Indore', 'Jabalpur', 'Jhabua', 'Katni', 'Khandwa', 
        'Khargone', 'Mandla', 'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch', 
        'Niwari', 'Panna', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 
        'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shajapur', 'Sheopur', 'Shivpuri', 
        'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain', 'Umaria', 'Vidisha', 'Others'
    ],
    'Maharashtra': [
        'Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara', 
        'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 
        'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai City', 'Mumbai Suburban', 
        'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad', 'Palghar', 
        'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 
        'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal', 'Others'
    ],
    'Manipur': [
        'Bishnupur', 'Chandel', 'Churachandpur', 'Imphal East', 'Imphal West', 
        'Jiribam', 'Kakching', 'Kamjong', 'Kangpokpi', 'Noney', 'Pherzawl', 
        'Senapati', 'Tamenglong', 'Tengnoupal', 'Thoubal', 'Ukhrul', 'Others'
    ],
    'Meghalaya': [
        'East Garo Hills', 'East Jaintia Hills', 'East Khasi Hills', 'North Garo Hills', 
        'Ri Bhoi', 'South Garo Hills', 'South West Garo Hills', 'South West Khasi Hills', 
        'West Garo Hills', 'West Jaintia Hills', 'West Khasi Hills', 'Others'
    ],
    'Mizoram': [
        'Aizawl', 'Champhai', 'Hnahthial', 'Kolasib', 'Khawzawl', 'Lawngtlai', 
        'Lunglei', 'Mamit', 'Saiha', 'Saitual', 'Serchhip', 'Others'
    ],
    'Nagaland': [
        'Dimapur', 'Kiphire', 'Kohima', 'Longleng', 'Mokokchung', 'Mon', 'Peren', 
        'Phek', 'Tuensang', 'Wokha', 'Zunheboto', 'Others'
    ],
    'Odisha': [
        'Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 
        'Deogarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur', 
        'Jharsuguda', 'Kalahandi', 'Kandhamal', 'Kendrapara', 'Kendujhar', 'Khordha', 
        'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangpur', 'Nayagarh', 'Nuapada', 
        'Puri', 'Rayagada', 'Sambalpur', 'Subarnapur', 'Sundargarh', 'Others'
    ],
    'Punjab': [
        'Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 
        'Fazilka', 'Ferozepur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 
        'Kapurthala', 'Ludhiana', 'Mansa', 'Moga', 'Muktsar', 'Nawanshahr', 
        'Pathankot', 'Patiala', 'Rupnagar', 'Sangrur', 'Tarn Taran', 'Others'
    ],
    'Rajasthan': [
        'Ajmer', 'Alwar', 'Banswara', 'Baran', 'Barmer', 'Bharatpur', 'Bhilwara', 
        'Bikaner', 'Bundi', 'Chittorgarh', 'Churu', 'Dausa', 'Dholpur', 'Dungarpur', 
        'Sri Ganganagar', 'Hanumangarh', 'Jaipur', 'Jaisalmer', 'Jalore', 'Jhalawar', 
        'Jhunjhunu', 'Jodhpur', 'Karauli', 'Kota', 'Nagaur', 'Pali', 'Pratapgarh', 
        'Rajsamand', 'Sawai Madhopur', 'Sikar', 'Sirohi', 'Tonk', 'Udaipur', 'Others'
    ],
    'Sikkim': [
        'East Sikkim', 'North Sikkim', 'South Sikkim', 'West Sikkim', 'Others'
    ],
    'Tamil Nadu': [
        'Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 
        'Dindigul', 'Erode', 'Kallakurichi', 'Kanchipuram', 'Kanyakumari', 'Karur', 
        'Krishnagiri', 'Madurai', 'Mayiladuthurai', 'Nagapattinam', 'Namakkal', 
        'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 
        'Salem', 'Sivaganga', 'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukudi', 
        'Tiruchirappalli', 'Tirunelveli', 'Tirupattur', 'Tiruppur', 'Tiruvallur', 
        'Tiruvannamalai', 'Tiruvarur', 'Vellore', 'Viluppuram', 'Virudhunagar', 'Others'
    ],
    'Telangana': [
        'Adilabad', 'Bhadradri Kothagudem', 'Hyderabad', 'Jagtial', 'Jangaon', 
        'Jayashankar Bhupalpally', 'Jogulamba Gadwal', 'Kamareddy', 'Karimnagar', 'Khammam', 
        'Komaram Bheem Asifabad', 'Mahabubabad', 'Mahbubnagar', 'Mancherial', 'Medak', 
        'Medchal Malkajgiri', 'Mulugu', 'Nagarkurnool', 'Nalgonda', 'Narayanpet', 'Nirmal', 
        'Nizamabad', 'Peddapalli', 'Rajanna Sircilla', 'Ranga Reddy', 'Sangareddy', 
        'Siddipet', 'Suryapet', 'Vikarabad', 'Wanaparthy', 'Warangal Rural', 
        'Warangal Urban', 'Yadadri Bhuvanagiri', 'Others'
    ],
    'Tripura': [
        'Dhalai', 'Gomati', 'Khowai', 'North Tripura', 'Sepahijala', 'South Tripura', 
        'Unakoti', 'West Tripura', 'Others'
    ],
    'Uttar Pradesh': [
        'Agra', 'Aligarh', 'Ambedkar Nagar', 'Amethi', 'Amroha', 'Auraiya', 
        'Ayodhya', 'Azamgarh', 'Baghpat', 'Bahraich', 'Ballia', 'Balrampur', 
        'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Bhadohi', 'Bijnor', 'Budaun', 
        'Bulandshahr', 'Chandauli', 'Chitrakoot', 'Deoria', 'Etah', 'Etawah', 
        'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 
        'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras', 
        'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 
        'Kasganj', 'Kaushambi', 'Kheri', 'Kushinagar', 'Lalitpur', 'Lucknow', 
        'Maharajganj', 'Mahoba', 'Mainpuri', 'Mathura', 'Mau', 'Meerut', 'Mirzapur', 
        'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'Prayagraj', 
        'Raebareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Sant Kabir Nagar', 
        'Shahjahanpur', 'Shamli', 'Shravasti', 'Siddharthnagar', 'Sitapur', 
        'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi', 'Others'
    ],
    'Uttarakhand': [
        'Almora', 'Bageshwar', 'Chamoli', 'Champawat', 'Dehradun', 'Haridwar', 
        'Nainital', 'Pauri Garhwal', 'Pithoragarh', 'Rudraprayag', 'Tehri Garhwal', 
        'Udham Singh Nagar', 'Uttarkashi', 'Others'
    ],
    'West Bengal': [
        'Alipurduar', 'Bankura', 'Birbhum', 'Cooch Behar', 'Dakshin Dinajpur', 
        'Darjeeling', 'Hooghly', 'Howrah', 'Jalpaiguri', 'Jhargram', 'Kalimpong', 
        'Kolkata', 'Malda', 'Murshidabad', 'Nadia', 'North 24 Parganas', 
        'Paschim Bardhaman', 'Paschim Medinipur', 'Purba Bardhaman', 'Purba Medinipur', 
        'Purulia', 'South 24 Parganas', 'Uttar Dinajpur', 'Others'
    ],
    'Delhi': [
        'Central Delhi', 'East Delhi', 'New Delhi', 'North Delhi', 'North East Delhi', 
        'North West Delhi', 'Shahdara', 'South Delhi', 'South East Delhi', 
        'South West Delhi', 'West Delhi', 'Others'
    ],
    'Jammu and Kashmir': [
        'Anantnag', 'Bandipora', 'Baramulla', 'Budgam', 'Doda', 'Ganderbal', 
        'Jammu', 'Kathua', 'Kishtwar', 'Kulgam', 'Kupwara', 'Poonch', 'Pulwama', 
        'Rajouri', 'Ramban', 'Reasi', 'Samba', 'Shopian', 'Srinagar', 'Udhampur', 'Others'
    ],
    'Ladakh': [
        'Kargil', 'Leh', 'Others'
    ],
    'Chandigarh': [
        'Chandigarh', 'Others'
    ],
    'Dadra and Nagar Haveli and Daman and Diu': [
        'Dadra and Nagar Haveli', 'Daman', 'Diu', 'Others'
    ],
    'Lakshadweep': [
        'Lakshadweep', 'Others'
    ],
    'Puducherry': [
        'Karaikal', 'Mahe', 'Puducherry', 'Yanam', 'Others'
    ]
}

@app.route('/')
def home():
    return render_template('home.html', 
                         categories=COMMODITY_CATEGORIES, 
                         states=list(STATES_DISTRICTS.keys()),
                         seasons=SEASONS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/copyright')
def copyright():
    return render_template('copyright.html')

@app.route('/get_crops/<category>')
def get_crops(category):
    crops = COMMODITY_CATEGORIES.get(category, [])
    return jsonify(crops)

@app.route('/get_districts/<state>')
def get_districts(state):
    districts = STATES_DISTRICTS.get(state, ['Others'])
    return jsonify(districts)



@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        category = request.form['category']
        crop = request.form['crop']
        state = request.form['state']
        district = request.form['district']
        month_value = request.form['month']  # Could be '2025-07' from date picker
        season = request.form['season']

        # Convert month (e.g., '2025-07') into numeric month
        try:
            month_num = int(month_value.split('-')[1])  # Extract month (07 -> 7)
        except:
            month_num = 1  # Default fallback

        # Prepare input DataFrame
        input_df = pd.DataFrame([{
            "category": category,
            "crop": crop,
            "state": state,
            "district": district,
            "month": month_num,
            "season": season
        }], columns=FEATURE_COLUMNS)

        # Encode categorical columns
        input_df[CATEGORICAL_COLS] = encoder.transform(input_df[CATEGORICAL_COLS])

        # Predict using Random Forest model
        predicted_price = rf_model.predict(input_df)[0]

        return render_template('result.html',
                               category=category,
                               crop=crop,
                               state=state,
                               district=district,
                               month=month_value,
                               season=season,
                               predicted_price=f"{predicted_price:.2f}")

    except Exception as e:
        return render_template('result.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
