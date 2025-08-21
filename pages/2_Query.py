import streamlit as st
from utils.simple_steps import match_query
from utils.language_support import language_support
try:
    from utils.grok_ai import is_grok_available
except ImportError:
    def is_grok_available():
        return False
from datetime import datetime

# Professional page configuration
st.set_page_config(
    page_title="IT Helpdesk Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar navigation
)

# Simple CSS for clean interface
st.markdown("""
<style>
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 1rem;
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 1rem;
}

.user-message {
    background-color: white;
    border: 1px solid #ddd;
    border-left: 3px solid #000;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    border-radius: 3px;
    margin-left: 2rem;
}

.assistant-message {
    background-color: white;
    border: 1px solid #ddd;
    border-left: 3px solid #666;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    border-radius: 3px;
    margin-right: 2rem;
}

.language-indicator {
    font-size: 0.8rem;
    color: #000;
    font-style: italic;
    margin-bottom: 0.5rem;
}

/* Ensure all text is black */
body, .stApp, .main, div, p, span, h1, h2, h3, h4, h5, h6 {
    color: #000 !important;
}

/* Keep simple white background */
.stApp {
    background-color: white !important;
}

/* Hide the entire sidebar and navigation */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Hide navigation buttons in sidebar */
.css-1d391kg, .css-1rs6os, .css-17ziqus, .css-1lcbmhc, .css-1outpf7 {
    display: none !important;
}

/* Hide any page navigation links that contain "app" */
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

/* Professional Send Button Styling */
button[kind="primary"] {
    background-color: white !important;
    color: #333 !important;
    border: 1px solid #ddd !important;
    border-radius: 4px !important;
    padding: 0.25rem 0.75rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    min-height: 32px !important;
    height: 32px !important;
    width: auto !important;
    max-width: 80px !important;
    margin: 0 !important;
}

button[kind="primary"]:hover {
    background-color: #f8f9fa !important;
    border-color: #ccc !important;
    color: #222 !important;
}

button[kind="primary"]:focus {
    box-shadow: 0 0 0 2px rgba(0,0,0,0.1) !important;
    outline: none !important;
}

/* Remove red background from any buttons */
.stButton > button, button {
    background-color: white !important;
}

/* Specific targeting for form submit button */
div[data-testid="stForm"] button[type="submit"] {
    background-color: white !important;
    color: #333 !important;
    border: 1px solid #ddd !important;
    border-radius: 4px !important;
    padding: 0.25rem 0.75rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    min-height: 32px !important;
    height: 32px !important;
    width: auto !important;
    max-width: 80px !important;
}

div[data-testid="stForm"] button[type="submit"]:hover {
    background-color: #f8f9fa !important;
    border-color: #ccc !important;
}
</style>
""", unsafe_allow_html=True)

# Simple header
st.markdown("""
<div style="text-align: center; padding: 1rem 0; background: white;">
    <h1 style="color: #000; margin-bottom: 0.5rem;">
        🤖 IT Chat Assistant
    </h1>
    <p style="color: #000; font-size: 1.1rem;">
        AI-Powered IT Support
    </p>
</div>
""", unsafe_allow_html=True)

# JavaScript to hide navigation
st.markdown("""
<script>
// Function to hide sidebar and navigation elements
function hideNavigation() {
    // Hide sidebar completely
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.display = 'none !important';
        sidebar.remove();
    }
    
    // Hide navigation section
    const nav = document.querySelector('section[data-testid="stSidebar"]');
    if (nav) {
        nav.style.display = 'none !important';
        nav.remove();
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
    
    // Hide elements with specific text content
    const allElements = document.querySelectorAll('*');
    allElements.forEach(el => {
        if (el.textContent === 'app' || el.textContent === 'main' || el.textContent === 'Main') {
            const parent = el.closest('li, div, section');
            if (parent) {
                parent.style.display = 'none !important';
            }
        }
    });
}

// Run immediately
hideNavigation();

// Run every 100ms to catch dynamic content
setInterval(hideNavigation, 100);

// Observer for dynamic content changes
const observer = new MutationObserver(() => {
    setTimeout(hideNavigation, 10);
});
observer.observe(document.body, { 
    childList: true, 
    subtree: true,
    attributes: true,
    attributeOldValue: true,
    characterData: true,
    characterDataOldValue: true
});

// Additional CSS injection
const style = document.createElement('style');
style.textContent = `
    [data-testid="stSidebar"] { display: none !important; }
    .css-1d391kg { display: none !important; }
    .css-1rs6os { display: none !important; }
    .css-17ziqus { display: none !important; }
    .css-1lcbmhc { display: none !important; }
    .css-1outpf7 { display: none !important; }
    .st-emotion-cache-1cypcdb { display: none !important; }
    .st-emotion-cache-1v0mbdj { display: none !important; }
    .stSidebar { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; visibility: hidden !important; }
`;
document.head.appendChild(style);
</script>
""", unsafe_allow_html=True)

# Removed energy efficiency indicator as requested

if not st.session_state.get('logged_in', False):
    st.warning(language_support.get_text('login_required'))
    st.switch_page("pages/1_Login.py")
else:
    # Language selector
    if 'user_language' not in st.session_state:
        st.session_state.user_language = 'en'
    
    # Language selector in header
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        languages = language_support.get_supported_languages()
        language_options = [f"{info['flag']} {info['name']}" for lang, info in languages.items()]
        language_codes = list(languages.keys())
        
        current_idx = language_codes.index(st.session_state.user_language) if st.session_state.user_language in language_codes else 0
        
        selected_language = st.selectbox(
            language_support.get_text('language_select', st.session_state.user_language),
            language_options,
            index=current_idx,
            key="language_selector"
        )
        
        # Update language if changed
        new_language = language_codes[language_options.index(selected_language)]
        if new_language != st.session_state.user_language:
            st.session_state.user_language = new_language
            st.rerun()
    
    # Show AI status indicator - removed Enhanced AI Mode info as requested
    if not is_grok_available():
        st.warning(language_support.get_text('basic_mode'))
    
    # Initialize chatbot session state variables with multilingual welcome
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        # Get username safely with fallback
        username = st.session_state.get('username', 'User')
        
        # Generate welcome message in user's language
        user_lang = st.session_state.get('user_language', 'en')
        welcome_msg = language_support.get_text('welcome', user_lang)
        welcome_msg = welcome_msg.replace("Hello!", f"Hello {username}!" if user_lang == 'en' else f"{username}!")
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "message": welcome_msg,
            "timestamp": datetime.now().strftime("%H:%M"),
            "language": user_lang
        })
    
    # Reset satisfaction and ticket question states when coming to query page
    if 'show_satisfaction' not in st.session_state:
        st.session_state.show_satisfaction = False
    if 'show_ticket_question' not in st.session_state:
        st.session_state.show_ticket_question = False
    
    if 'chat_active' not in st.session_state:
        st.session_state.chat_active = True
    
    if 'chat_summary' not in st.session_state:
        st.session_state.chat_summary = ""
    
    # Initialize input clearing mechanism
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0

    # Chat interface
    if st.session_state.chat_active:
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for chat in st.session_state.chat_history:
                if chat["role"] == "user":
                    # Display user message
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>👤 You</strong> ({chat['timestamp']})
                        <div>{chat['message']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Display assistant message
                    st.markdown(f"""
                    <div class="assistant-message">
                        <strong>🤖 Assistant</strong> ({chat['timestamp']})
                        <div>{chat['message']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input and buttons with language support
        user_lang = st.session_state.get('user_language', 'en')
        placeholder_text = language_support.get_text('ask_question', user_lang)
        
        # Use form for Enter key functionality and proper button placement
        with st.form("chat_form", clear_on_submit=True):
            col1, col2 = st.columns([5, 1])
            with col1:
                user_input = st.text_input(
                    "Type your message here...", 
                    placeholder=placeholder_text,
                    key=f"chat_input_{st.session_state.input_key}",
                    label_visibility="collapsed"
                )
            with col2:
                # Small professional send button
                send_btn = st.form_submit_button("Send", type="primary")
        
        # End chat and Clear chat buttons (after the chat input form)
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            end_chat_btn = st.button(f"🔚 {language_support.get_text('end_chat')}", type="secondary", key="end_chat_btn")
        with col2:
            clear_chat_btn = st.button("🔄 Clear Chat", key="clear_chat_btn")
        
        # Handle send message
        if send_btn and user_input.strip():
            # Detect language if not already set or if different from current
            detected_lang = language_support.detect_language(user_input)
            if detected_lang != st.session_state.user_language:
                st.session_state.user_language = detected_lang
            
            # Add user message to chat history with language info
            st.session_state.chat_history.append({
                "role": "user", 
                "message": user_input, 
                "timestamp": datetime.now().strftime("%H:%M"),
                "language": st.session_state.user_language
            })
            
            # Get user context for AI with language preference
            user_context = {
                'username': st.session_state.get('username', 'User'),
                'user_id': st.session_state.get('user_id', 'unknown'),
                'email': st.session_state.get('email', 'user@company.com'),
                'language': st.session_state.user_language,
                'language_prompt': language_support.get_language_prompt(st.session_state.user_language)
            }
            
            # Get assistant response
            response = match_query(user_input, user_context, st.session_state.chat_history)
            
            # Format response for the user's language
            formatted_response = language_support.format_multilingual_response(response, st.session_state.user_language)
            
            st.session_state.chat_history.append({
                "role": "assistant", 
                "message": formatted_response, 
                "timestamp": datetime.now().strftime("%H:%M"),
                "language": st.session_state.user_language
            })
            
            # Update session variables for potential ticket creation
            st.session_state.query = user_input
            st.session_state.solution = response
            
            # Clear input field by incrementing the key
            st.session_state.input_key += 1
            
            st.rerun()
        
        elif send_btn and not user_input.strip():
            st.error(language_support.get_text('enter_message'))
        
        # Handle clear chat button
        if clear_chat_btn:
            st.session_state.chat_history = []
            # Get username safely with fallback
            username = st.session_state.get('username', 'User')
            welcome_msg = f"Hello {username}! 👋 I'm your AI-powered IT Helpdesk assistant."
            if is_grok_available():
                welcome_msg += " I can help you with a wide range of IT issues. What can I help you with today?"
            else:
                welcome_msg += " I'm in basic mode but can still help with common issues. How can I assist you?"
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "message": welcome_msg,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            # Reset input key to clear input field
            st.session_state.input_key += 1
            st.rerun()
        
        # Handle end chat
        if end_chat_btn:
            st.session_state.chat_active = False
            st.session_state.show_satisfaction = True
            # Generate chat summary
            chat_summary = "## Chat Summary\n\n"
            for i, chat in enumerate(st.session_state.chat_history):
                if chat["role"] == "user":
                    chat_summary += f"**User ({chat['timestamp']}):** {chat['message']}\n\n"
                elif i > 0:  # Skip the initial greeting
                    chat_summary += f"**Assistant ({chat['timestamp']}):** {chat['message']}\n\n"
            st.session_state.chat_summary = chat_summary
            st.rerun()
    
    # Satisfaction check after ending chat
    elif st.session_state.show_satisfaction:
        st.markdown("### Chat Session Ended")
        st.markdown("---")
        
        # Show chat summary
        if st.session_state.chat_summary:
            with st.expander("📋 View Chat Summary", expanded=True):
                st.markdown(st.session_state.chat_summary)
        
        # Get current language
        user_lang = st.session_state.get('user_language', 'en')
        
        # Satisfaction Survey
        st.markdown("### How was our support today?")
        
        # Horizontal feedback buttons
        col1, col2 = st.columns(2)
        
        with col1:
            helpful_text = f"👍 {language_support.get_text('helpful', user_lang)}"
            if st.button(helpful_text, use_container_width=True, type="primary", key="helpful_feedback"):
                thank_you_msg = language_support.get_text('thank_you', user_lang)
                st.success(f"🎉 {thank_you_msg}")
                # Add option to start new chat
                new_chat_text = f"� {language_support.get_text('new_chat', user_lang)}"
                if st.button(new_chat_text, key="new_chat_after_helpful"):
                    # Reset everything for new chat with user's language
                    st.session_state.chat_history = []
                    username = st.session_state.get('username', 'User')
                    welcome_msg = language_support.get_text('welcome', user_lang)
                    welcome_msg = welcome_msg.replace("Hello!", f"Hello {username}!" if user_lang == 'en' else f"{username}!")
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "message": welcome_msg,
                        "timestamp": datetime.now().strftime("%H:%M"),
                        "language": user_lang
                    })
                    st.session_state.chat_active = True
                    st.session_state.show_satisfaction = False
                    st.session_state.chat_summary = ""
                    st.rerun()
            
            with col2:
                if st.button(f"👎 {language_support.get_text('not_helpful')}", use_container_width=True, type="secondary", key="not_helpful_feedback"):
                    st.session_state.show_ticket_question = True
                    st.rerun()
        
        if st.session_state.show_ticket_question:
            # Show ticket creation question
            st.info(language_support.get_text('ticket_question'))
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button(f"🎫 {language_support.get_text('create_ticket')}", type="primary", key="create_ticket_yes", use_container_width=True):
                    # Prepare summary for ticket
                    st.session_state.summary = st.session_state.chat_summary
                    st.switch_page("pages/3_Ticket.py")
            with col_no:
                if st.button(f"❌ {language_support.get_text('no_thanks')}", type="secondary", key="no_ticket", use_container_width=True):
                    # Show thank you message
                    st.success(language_support.get_text('thank_you'))
                    st.info(language_support.get_text('new_session'))
                    
                    # Reset everything for new chat
                    st.session_state.chat_history = []
                    st.session_state.show_satisfaction = False
                    st.session_state.show_ticket_question = False
                    st.session_state.chat_active = True
                    st.session_state.current_response = ""
                    st.session_state.feedback_given = {}
                    st.session_state.chat_summary = ""
                    
                    # Get welcome message in selected language
                    user_lang = st.session_state.get('user_language', 'en')
                    welcome_msg = language_support.get_welcome_message(st.session_state.get('username', 'User'), is_grok_available(), user_lang)
                    st.session_state.chat_history = [{"role": "assistant", "message": welcome_msg, "timestamp": datetime.now().strftime("%H:%M")}]
                    st.rerun()
    
    # Show restart option if chat ended without satisfaction check
    else:
        # Single centered start new chat button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"🔄 {language_support.get_text('start_new_chat')}", key="start_new_chat_main", use_container_width=True):
                # Reset everything for new chat
                st.session_state.chat_history = []
                # Get welcome message in selected language
                user_lang = st.session_state.get('user_language', 'en')
                welcome_msg = language_support.get_welcome_message(st.session_state.get('username', 'User'), is_grok_available(), user_lang)
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "message": welcome_msg,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                st.session_state.chat_active = True
                st.session_state.show_satisfaction = False
                st.session_state.chat_summary = ""
                # Reset input key to clear input field
                st.session_state.input_key += 1
                st.rerun()
