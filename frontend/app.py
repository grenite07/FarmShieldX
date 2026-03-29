import streamlit as st
import requests

st.set_page_config(page_title="FarmShieldX", page_icon="🌿", layout="centered")

st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🌿 FarmShieldX</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>AI-Powered Crop Protection</h4>", unsafe_allow_html=True)
st.write("---")

# Mock GPS Coordinates (Ranchi, Jharkhand)
LAT = 23.3441  
LON = 85.3096  

uploaded_file = st.file_uploader("Upload a clear photo of the affected plant leaf", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, use_column_width=True)
    
    if st.button("🔍 Analyze Crop & Weather", use_container_width=True):
        with st.spinner("Analyzing visual data and fetching live environmental context..."):
            
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            # Send to FastAPI Backend
            try:
                response = requests.post(f"http://127.0.0.1:8000/analyze?lat={LAT}&lon={LON}", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("Analysis Complete!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"🦠 **Detected Condition:**\n\n{data['disease']}")
                    with col2:
                        st.warning(f"⛅ **Local Weather Context:**\n\n{data['weather']}")
                        
                    st.markdown("### 📋 Recommended Action Plan")
                    st.write(data['action_plan'])
                else:
                    st.error(f"Backend Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend server. Is FastAPI running?")