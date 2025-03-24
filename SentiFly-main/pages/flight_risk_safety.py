import streamlit as st
import base64
import os

st.set_page_config(page_title="Flight risk safety page", layout="wide")
# ✅ Function to set background image
def set_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            bg_image = f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(245, 245, 245, 0.7), rgba(245, 245, 245, 0.7)), 
                        url("data:image/jpg;base64,{encoded_string}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """
        st.markdown(bg_image, unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Background image not found at: {image_path}")

# ✅ Set background with corrected image path
set_background(r"SentiFly-main/Images/bg8.jpeg")


# Custom CSS for Background, Transparent Containers, and Styling
custom_css = """
    <style>
        body {
            background-image: url('Images/bg8.jpg');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }

        .container {
            background: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
            width: 60%;
            margin: auto;
        }

        .stButton>button {
            background-color: #b22222;
            color: white;
            border-radius: 5px;
            font-size: 16px;
        }

        .stButton>button:hover {
            background-color: #8b1a1a;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Include Navbars
# Main Container with Title & Description
with st.container():
    st.markdown("<h1 style='text-align: center;'>Flight risk safety Analyzer</h1>", unsafe_allow_html=True)

# Feature Selection
st.markdown("### Quick Access")

col1, col2 = st.columns(2)

with col1:
    if st.button("🛡 Safety Ratings", use_container_width=True):
        st.switch_page("pages/safety_ratings.py")

with col2:
    if st.button("📊 Risk Prediction", use_container_width=True):
        st.switch_page("pages/risk_prediction.py")

# Overview Stats
st.markdown("### Overview")
col3, col4 = st.columns(2)

with col3:
    st.metric(label="Airlines Covered", value="6")

with col4:
    st.metric(label="Safety Score", value="92/100")

# Include Footer