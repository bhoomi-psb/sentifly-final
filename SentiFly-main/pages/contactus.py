import streamlit as st
import base64
import os

# ✅ Set page title and layout (Must be first command)

st.set_page_config(page_title="Contact US", layout="wide")

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

# Apply custom CSS styles
custom_css = """
   <style>
    /* Center the form container */
    div[data-testid="stForm"] {
        background: rgba(255, 231, 231, 0.8); /* Light pink with slight transparency */
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(255, 0, 0, 0.3); /* Light red border */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        width: 100%;
        text-align: center;
        margin: auto;
    }
    
    /* Center the form heading */
    h2 {
        text-align: center;
        color: #b22222; /* Dark Red */
    }

    /* Style inputs & textareas */
    input, textarea {
        width: 100%;
        padding: 12px;
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 5px;
        background: rgba(255, 230, 230, 0.4);
        color: #303030;
        font-size: 16px;
    }

    /* Style the submit button */
    div[data-testid="stFormSubmitButton"] button {
        background: #ff2f2f !important;
        color: white !important;
        font-size: 18px !important;
        border-radius: 8px !important;
        padding: 12px 20px !important;
        width: 100%;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: #d90000 !important;
    }

    * {
        font-family: Arial, sans-serif;
    }
    body {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        animation: fadeIn 1s forwards;
        width:700px;
    }
    .container {
        background: rgba(255, 255, 255, 0.8); /* Soft white with transparency */
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(255, 0, 0, 0.3); /* Light red border */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        width: 800px;
        text-align: center;
        margin: auto;
    }
    h2 {
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
        text-transform: uppercase;
        color: #b22222; /* Dark Red */
    }
    .contact-info p, .contact-info a {
        color: #2c2c2c;
        margin-bottom: 10px;
        text-decoration: none;
        font-size: 16px;
    }
    input, textarea {
        width: 100%;
        padding: 12px;
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 5px;
        background: rgba(255, 230, 230, 0.4);
        color: #303030;
        font-size: 16px;
    }
    input::placeholder, textarea::placeholder {
        color: rgba(127, 127, 127, 0.7);
    }
    button {
        background: #ff2f2f;
        color: #fff;
        padding: 12px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 18px;
        transition: 0.3s;
        width: 100%;
    }
    button:hover {
        background: #d90000;
    }
    .map {
        margin-top: 20px;
        border-radius: 10px;
        overflow: hidden;
    }
    iframe {
        width: 100%;
        height: 250px;
        border: none;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>

"""

# Inject CSS styles
st.markdown(custom_css, unsafe_allow_html=True)

# Include the navbar



# Contact Us Header
st.markdown("<h2>Contact Us</h2>", unsafe_allow_html=True)

# Contact Info
st.markdown(
    """
    <div class="contact-info">
        <p>Email: <a href="mailto:support@sentifly.com">support@sentifly.com</a></p>
        <p>Phone: +91 98765 43210</p>
        <p>Address: 456, SentiFly HQ, Bangalore, India</p>
        <p>Website: <a href="https://www.sentifly.com" target="_blank">www.sentifly.com</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Contact Form
with st.form("contact_form"):
    name = st.text_input("Your Name", "")
    email = st.text_input("Your Email", "")
    subject = st.text_input("Subject", "")
    message = st.text_area("Your Message", "")

    submitted = st.form_submit_button("Send Message")
    if submitted:
        st.success("✅ Your message has been sent successfully!")

# Map Section
st.markdown("<h3>Our Location</h3>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="map">
        <iframe src="https://maps.google.com/maps?q=Bangalore,India&t=&z=13&ie=UTF8&iwloc=&output=embed" allowfullscreen></iframe>
    </div>
    """,
    unsafe_allow_html=True,
)

# Include the footer