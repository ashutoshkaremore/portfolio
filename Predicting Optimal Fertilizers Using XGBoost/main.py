import streamlit as st
import requests

api_url = 'http://127.0.0.1:8000'

st.title('Predict Fertilizer')

col1, col2 = st.columns(2)

@st.dialog("Prediction Result")
def get_fertilizer_name(form_data): # post form_data payload and get fertilizer name
    api_path = api_url + '/predict'
    response = requests.post(api_path, json = form_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response JSON: {response.json()}")
        data = response.json() # if response is ok show dialog contents
        st.write('Suitable fertilizer according to your conditions is :')
        st.write(data['fertilizer'])
    else:
        print(f"Error12: {response.text}") # if response is not ok print error


with st.form('conditions_form'):

    with col1:
        Temparature = st.slider("Temparature", 20, 50, 35)
        Humidity = st.slider("Humidity", 50, 75, 58)
        Moisture = st.slider("Moisture", 25, 65, 43)
        Soil = st.pills("Soil Type",['Sandy', 'Black','Clayey','Red','Loamy'],key=15546546)
    
    with col2:
        Nitrogen = st.slider("Nitrogen", 4, 45, 37)
        Potassium = st.slider("Potassium", 0, 20, 2)
        Phosphorous = st.slider("Phosphorous", 0, 45, 16)
        Crop = st.pills("Crop Type",['Paddy', 'Pulses','Cotton','Tobacco','Wheat','Millets','Barley','Sugarcane','Oil seeds','Maize','Ground Nuts'])

    submitted = st.form_submit_button('Predict Fertilizer')
    
    if submitted:
        form_data = {
                'Temparature' : Temparature,
                'Humidity' : Humidity,
                'Moisture' : Moisture,
                'Soil' : Soil,
                'Crop' : Crop,
                'Nitrogen' : Nitrogen,
                'Potassium' : Potassium,
                'Phosphorous' : Phosphorous
            } # converting for json format
        
        get_fertilizer_name(form_data)
        





