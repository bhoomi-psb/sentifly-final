import streamlit as st
import importlib
import os

# ✅ Set Streamlit page configuration (ONLY ONCE in app.py)
st.set_page_config(
    page_title="SentiFly - Indian Airlines",
    page_icon="✈️",
    layout="wide"
)

# ✅ Maintain user session state
if "user_type" not in st.session_state:
    st.session_state["user_type"] = None  # Default to None
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Landing Page"  # Default page

# ✅ Load appropriate navbar
navbar = None
if st.session_state["user_type"] == "user":
    navbar = importlib.import_module("navbar")
elif st.session_state["user_type"] == "airline":
    navbar = importlib.import_module("a_navbar")

# ✅ Display navbar if applicable
if navbar:
    navbar.show()

# ✅ Sidebar Navigation
st.sidebar.title("Navigation")

# ✅ Define pages dictionary based on user type
PAGES = {"Landing Page": "pages/landingpage.py"}  # Default page

if st.session_state["user_type"] == "user":
    PAGES.update({
        "User Home": "pages/userhome.py",
        "Insights": "pages/userinsights.py",
        "Flight Risk & Safety": "pages/flight_risk_safety.py",
        "About Us": "pages/aboutus.py",
        "Contact Us": "pages/contactus.py",
        "Sign In": "pages/signin.py",
    })
elif st.session_state["user_type"] == "airline":
    PAGES.update({
        "Airline Home": "pages/airlinehome.py",
        "Airline Insights": "pages/a_insights.py",
        "Flight Risk & Safety": "pages/flight_risk_safety.py",
        "About Us": "pages/aboutus.py",
        "Contact Us": "pages/contactus.py",
        "Sign In": "pages/signin.py",
    })

# ✅ Sidebar Navigation Buttons
selected_page = st.sidebar.radio("Go to", list(PAGES.keys()))
st.session_state["selected_page"] = selected_page

# ✅ Redirect to Sign-in if user_type is None
if not st.session_state["user_type"] and st.session_state["selected_page"] != "Landing Page":
    st.warning("Please log in to continue.")
    st.switch_page("pages/signin.py")

# ✅ Render Selected Page
target_page = PAGES[st.session_state["selected_page"]]
if os.path.exists(target_page):
    with open(target_page, "r", encoding="utf-8") as f:
        exec(f.read(), globals())  # ✅ Dynamically execute the selected page

# ✅ Hide Streamlit default elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
    </style>
""", unsafe_allow_html=True)

# ✅ Display Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>© 2025 SentiFly. All Rights Reserved.</p>", unsafe_allow_html=True)