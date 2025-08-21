import streamlit as st

# Configure page with minimal visibility
st.set_page_config(
    page_title="IT Helpdesk",
    page_icon="🔧",
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# Redirect to login page immediately - no app page needed
if not st.session_state.get('logged_in', False):
    st.switch_page("pages/1_Login.py")

# If we reach here, user is logged in but we don't want this page
# Redirect to chat page instead
st.switch_page("pages/2_Query.py")
