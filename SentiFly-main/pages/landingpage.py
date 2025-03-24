import streamlit as st
import base64
import os

st.set_page_config(page_title="about Us", layout="wide")
# ✅ Set page title and layout
def show():
    st.title("Landing Page")
    st.write("This page displays the landing page.")

# ✅ Function to set background image
def set_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        bg_image = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(bg_image, unsafe_allow_html=True)
    else:
        st.warning(f"⚠ Background image not found at: {image_path}")

# ✅ Set background
set_background(r"SentiFly-main/Images/landing2.jpg")

# ✅ Custom CSS for styling
custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        body {
            font-family: 'Poppins', sans-serif;
            align-items:left;
        }

        .container {
            max-width: 900px;
            margin: 5% auto;
            background: rgba(255, 255, 255, 0.7);
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }

        .hero-title {
            font-size: 60px;
            font-weight: bold;
            color: #222222;
            margin-bottom: 20px;
        }

        .hero-subtitle {
            font-size: 40px;
            font-weight: 500;
            margin-bottom: 20px;
        }

        .highlight-text {
            font-size: 30px;
            font-weight: 400;
            margin-bottom: 30px;
        }

        .bullet-points p {
            font-size: 25px;
            margin-bottom: 20px;
        }

        .cta-button {
            margin-top: 20px;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: 600;
            color: #fff;
            background: #ea5353;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: 0.3s;
        }

        .cta-button:hover {
            background: #ff4545;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ✅ Hero Section with Increased Font Size
st.markdown('<div class="hero-title">Welcome to SentiFly</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Your Flight, Your Feelings, Our Insights!</div>', unsafe_allow_html=True)
st.markdown('<div class="highlight-text">Elevating Air Travel Through Data</div>', unsafe_allow_html=True)

st.markdown('<div style="font-size: 28px;" class="highlight-text">SentiFly is revolutionizing the way airlines and</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size: 28px;" class="highlight-text">passengers engage with flight experiences.</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size: 28px;" class="highlight-text">Our AI-powered platform provides real-time analysis of</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size: 28px;" class="highlight-text">passenger reviews, enabling airlines to enhance service</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size: 28px;" class="highlight-text">quality and travelers to make informed decisions.</div>', unsafe_allow_html=True)

# ✅ Properly Spaced Bullet Points
st.markdown("""
<div class="bullet-points">
    <p><b>Discover the Best Airlines:</b> Compare customer experiences before booking.</p>
    <p><b>Track Airline Performance:</b> Insights based on real traveler feedback.</p>
    <p><b>Detect Fake Reviews:</b> Ensure transparency in airline ratings.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="highlight-text">Join us in reshaping the future of air travel!</div>', unsafe_allow_html=True)

# ✅ Centered Login Button
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("Login", key="login_button", help="Go to Login Page"):
        st.switch_page("pages/signin.py")

# ✅ Footer
st.markdown("<p><b>© 2025 SentiFly. All Rights Reserved.</b></p>", unsafe_allow_html=True)
