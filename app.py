import pickle as pkl
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# Page Config
st.set_page_config(page_title='House Prices Prediction', layout='centered') 

# Display Image & Title
st.image("https://tse4.mm.bing.net/th/id/OIP.rH1yfydJLiq56oXsDzu0yQHaE6?rs=1&pid=ImgDetMain&o=7&rm=3", width=800)
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏡 Estimate Your Dream Home's Price 🏡</h1>", unsafe_allow_html=True)
st.write("Use this tool to estimate the **ideal price range** for your dream home based on your preferences.")

# Load Model
with open('house.pkl', 'rb') as model_file:
    house = pkl.load(model_file)

# Encoding Dictionary
Encodings = {
    'Neighborhood': {'Rural': 0, 'Suburb': 1, 'Urban': 2}
}

# User Input Form
with st.form("prediction_form"):
    SquareFeet = st.slider("📏 Select House Size (Square Feet)", 0, 3000, 100)
    Bedrooms = st.selectbox("🛏️ Choose Number of Bedrooms", options=['1', '2', '3', '4', '5'])
    Bathrooms = st.selectbox("🛁 Choose Number of Bathrooms", options=['1', '2', '3', '4', '5'])
    neighborhood = st.selectbox("📍 Select Your Preferred Neighborhood", options=list(Encodings['Neighborhood'].keys()))
    YearBuilt = st.slider("🏗️ Select Year Built", min_value=2000, max_value=2025, step=1)

    submitted = st.form_submit_button('🔍 Predict Price')

# Function to return inputs
def get_inputs():
    return [
        SquareFeet,
        int(Bedrooms),  # Convert string to int
        int(Bathrooms),  # Convert string to int
        Encodings['Neighborhood'][neighborhood],  # Encoded Neighborhood
        YearBuilt
    ] if submitted else None

# Process user inputs
input_data = get_inputs()

if input_data:
    # Convert to DataFrame
    feature_names = ['SquareFeet', 'Bedrooms', 'Bathrooms', 'Neighborhood', 'YearBuilt']
    input_df = pd.DataFrame([input_data], columns=feature_names)

    # Make Prediction
    predicted_price = house.predict(input_df)

    # Celebration Effect - Confetti & Premium Styling
    st.markdown("<h2 style='color: #008CBA;'>🏡 Estimated House Price:</h2>", unsafe_allow_html=True)
    st.success(f"💰 **${predicted_price[0]:,.2f}**")
    
    # 🎉 Custom Celebration Message
    st.markdown(
        "<h3 style='color: #FF5733;'>🎊 Congratulations! 🎊</h3>"
        "<p style='font-size: 18px;'>You’re one step closer to your dream home. 🏠✨</p>",
        unsafe_allow_html=True
    )