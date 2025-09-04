import streamlit as st
from utils.auth import authenticate

# Enhanced page configuration
st.set_page_config(
    page_title="KIITOS- Global IT Support Login",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"  # Hide sidebar navigation
)

# Simple CSS for login page
st.markdown("""
<style>
.login-container {
    background: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 2rem;
    margin: 2rem 0;
}

.login-header {
    text-align: center;
    margin-bottom: 2rem;
}

.login-header h1 {
    color: #000;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.eco-stats {
    background: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
    text-align: center;
}

/* Ensure all text is black */
body, .stApp, .main, div, p, span, h1, h2, h3, h4, h5, h6 {
    color: #000 !important;
}

/* Hide the entire sidebar and navigation */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Hide navigation buttons in sidebar */
.css-1d391kg, .css-1rs6os, .css-17ziqus, .css-1lcbmhc, .css-1outpf7 {
    display: none !important;
}

/* Hide any page navigation links */
.css-1v3fvcr, .css-1v0mbdj, .stSidebar {
    display: none !important;
}

/* Modern CSS selectors for hiding sidebar */
[data-testid="stSidebar"] {
    display: none !important;
}

.st-emotion-cache-1cypcdb, .st-emotion-cache-1v0mbdj {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# Simple header
st.markdown("""
<div class="login-header">
    <h1>KIITOS - Global IT Support Assistant</h1>
    <p style="color: #000; font-size: 1.1rem;">Please log in to access IT support services</p>
</div>
""", unsafe_allow_html=True)

# JavaScript to hide navigation
st.markdown("""
<script>
// Function to aggressively hide sidebar and navigation
function hideNavigation() {
    // Hide sidebar completely
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.display = 'none !important';
        sidebar.remove();
    }
    
    // Hide any app navigation link
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        if (link.textContent.toLowerCase().includes('app') || 
            link.href.includes('app.py') ||
            link.textContent.toLowerCase() === 'main') {
            link.style.display = 'none !important';
            link.remove();
        }
    });
}

hideNavigation();
setInterval(hideNavigation, 50);

const observer = new MutationObserver(hideNavigation);
observer.observe(document.body, { childList: true, subtree: true });

// CSS injection
const style = document.createElement('style');
style.textContent = '[data-testid="stSidebar"] { display: none !important; visibility: hidden !important; }';
document.head.appendChild(style);
</script>
""", unsafe_allow_html=True)

# Removed the eco stats box as requested

if st.session_state.get('logged_in', False):
    st.success(f"✅ Already logged in as **{st.session_state.get('username', 'User')}** ({st.session_state.get('user_id', 'unknown')})")
    
    st.markdown("---")
    st.markdown("### 🎯 Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🤖 Go to Chat Assistant", type="primary"):
            st.switch_page("pages/2_Query.py")
    
    with col2:
        if st.button("🎫 Create Support Ticket"):
            st.switch_page("pages/3_Ticket.py")

else:
    st.markdown("### Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        user = authenticate(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user['username']
            st.session_state.user_id = user['id']
            st.session_state.email = user['email']
            st.success("✅ Login successful! Redirecting...")
            st.switch_page("pages/2_Query.py")
        else:
            st.error("❌ Invalid username or password. Please try again.")
    
    st.markdown("---")
    st.markdown("*Need help with login? Contact your IT administrator.*")
