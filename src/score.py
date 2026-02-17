import joblib
import pandas as pd
import numpy as np

# Load trained model
model = joblib.load('models/credit_model.pkl')

def calculate_score(user_data: dict) -> dict:
    # Convert to dataframe
    df = pd.DataFrame([user_data])
    
    # Predict default probability
    prob = model.predict_proba(df)[:, 1][0]
    
    # Convert to credit score (300~850)
    score = int(850 - (prob * (850 - 300)))
    
    # Score rating
    if score >= 750:
        rating = 'Excellent'
    elif score >= 700:
        rating = 'Good'
    elif score >= 650:
        rating = 'Fair'
    elif score >= 600:
        rating = 'Poor'
    else:
        rating = 'Very Poor'
    
    return {
        'score': score,
        'rating': rating,
        'default_probability': round(prob * 100, 2)
    }