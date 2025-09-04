import streamlit as st
from utils.simple_steps import match_query
from utils.language_support import language_support
try:
    from utils.grok_ai import is_grok_available
except ImportError:
    def is_grok_available():
        return False
from datetime import datetime

# Professional page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="KIITOS - Global IT Support Assistant chat",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar navigation
)

# Check authentication - redirect to login if not logged in
if not st.session_state.get('logged_in', False) or 'username' not in st.session_state:
    st.switch_page("pages/1_Login.py")

# Simple CSS for clean interface
st.markdown("""
<style>
/* Remove ALL possible spacing from root elements */
html, body {
    margin: 0 !important;
    padding: 0 !important;
}

/* Remove ALL default Streamlit spacing and headers */
.main .block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
    margin-top: 0rem !important;
}

/* Completely remove Streamlit header */
header[data-testid="stHeader"] {
    height: 0px !important;
    display: none !important;
    visibility: hidden !important;
}

/* Remove top toolbar */
.stToolbar {
    display: none !important;
}

/* Remove default app view container padding */
.appview-container .main .block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/* Remove any remaining top margins */
.element-container:first-child {
    margin-top: 0rem !important;
}

/* Remove body margins and Streamlit app margins */
.stApp {
    margin-top: 0px !important;
    padding-top: 0px !important;
}

/* Target the root Streamlit container */
div[data-testid="stAppViewContainer"] {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/* Remove any iframe or embed margins */
iframe {
    margin: 0 !important;
    padding: 0 !important;
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

/* Hide any text area labels completely - comprehensive approach */
.stTextArea > label {
    display: none !important;
}

.stTextArea > div > label {
    display: none !important;
}

/* Hide all label elements in text areas */
.stTextArea label {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0 !important;
    width: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Hide any background text or placeholder-like elements */
.stTextArea [data-baseweb="textarea"] + * {
    display: none !important;
}

/* Additional CSS to hide any residual label text */
.stTextArea * {
    background-image: none !important;
}

/* Force textarea to have no background text */
.stTextArea textarea::before,
.stTextArea textarea::after {
    content: none !important;
    display: none !important;
}

/* Target Streamlit's specific textarea wrapper classes */
div[data-testid="stTextArea"] label,
div[data-testid="stTextArea"] > div > label,
div[data-testid="stTextArea"] span {
    display: none !important;
    visibility: hidden !important;
}

/* Hide any floating labels or helper text */
.stTextArea .st-emotion-cache-* label {
    display: none !important;
}

/* Completely remove any label remnants */
.stTextArea > div:first-child {
    display: none !important;
}

/* WhatsApp-style chat container */
.chat-container {
    background: linear-gradient(to bottom, #e5ddd5, #f0f0f0);
    max-height: 60vh;
    overflow-y: auto;
    padding: 0.3rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    margin-top: 0.1rem !important;
    display: flex;
    flex-direction: column;
}

/* Message containers for proper alignment */
.message-container-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.1rem 0;
}

.message-container-assistant {
    display: flex;
    justify-content: flex-start;
    margin: 0.1rem 0;
}

/* WhatsApp-style user messages (right side, green) */
.user-message {
    background: #dcf8c6;
    color: #000;
    padding: 0.4rem 0.6rem;
    border-radius: 18px;
    max-width: 70%;
    width: fit-content;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    position: relative;
    margin-bottom: 0.1rem;
}

.user-message::after {
    content: '';
    position: absolute;
    right: -8px;
    bottom: 8px;
    width: 0;
    height: 0;
    border: 8px solid transparent;
    border-left-color: #dcf8c6;
    border-right: 0;
    margin-top: -8px;
}

/* WhatsApp-style assistant messages (left side, white) */
.assistant-message {
    background: #ffffff;
    color: #000;
    padding: 0.4rem 0.6rem;
    border-radius: 18px;
    max-width: 70%;
    width: fit-content;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    position: relative;
    margin-bottom: 0.1rem;
}

.assistant-message::after {
    content: '';
    position: absolute;
    left: -8px;
    bottom: 8px;
    width: 0;
    height: 0;
    border: 8px solid transparent;
    border-right-color: #ffffff;
    border-left: 0;
    margin-top: -8px;
}

/* Message timestamps */
.message-time {
    font-size: 0.65rem;
    color: #667781;
    text-align: right;
    margin-top: 0.1rem;
    margin-bottom: 0.1rem;
}

/* WhatsApp-style input area */
.chat-input-container {
    background: #f0f2f5;
    padding: 0.5rem;
    border-radius: 20px;
    border: 1px solid #ddd;
    margin: 0.5rem 0;
}

/* WhatsApp-style send button */
button[kind="primary"] {
    background-color: #25d366 !important;
    color: white !important;
    border: none !important;
    border-radius: 50% !important;
    width: 45px !important;
    height: 45px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.2rem !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
}

button[kind="primary"]:hover {
    background-color: #20bd5a !important;
    transform: scale(1.05) !important;
}

/* WhatsApp-style textarea */
.stTextArea textarea {
    border-radius: 20px !important;
    border: 1px solid #ddd !important;
    padding: 0.8rem 1rem !important;
    background: white !important;
    resize: none !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui !important;
}

/* White background feedback buttons with black text */
.stButton > button {
    background-color: white !important;
    color: #333 !important;
    border: 2px solid #dee2e6 !important;
    border-radius: 6px !important;
    padding: 0.3rem 0.8rem !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    min-height: 35px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background-color: #f8f9fa !important;
    border-color: #adb5bd !important;
    color: #212529 !important;
}

/* Ensure helpful button also has white background */
.stButton > button[data-testid*="primary"] {
    background-color: white !important;
    color: #333 !important;
    border: 2px solid #dee2e6 !important;
}

.stButton > button[data-testid*="primary"]:hover {
    background-color: #f8f9fa !important;
    border-color: #adb5bd !important;
    color: #212529 !important;
}

/* Remove any potential extra spacing that could create white rectangles */
.element-container, .stMarkdown, .stButton {
    margin-top: 0 !important;
    margin-bottom: 0rem !important;
}

/* Remove extra spacing from any containers */
div[data-testid="element-container"] {
    margin: 0 !important;
    padding: 0 !important;
}

/* Minimize spacing between elements */
.stMarkdown > div {
    margin-bottom: 0rem !important;
    margin-top: 0rem !important;
}

/* Aggressively remove gaps between consecutive markdown elements */
.stMarkdown:not(:last-child) {
    margin-bottom: 0 !important;
}

/* Force tight spacing for consecutive elements */
.element-container + .element-container {
    margin-top: 0 !important;
}

/* Remove any unwanted background spaces */
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
</style>
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

# Check authentication
if 'username' not in st.session_state:
    st.error("🚫 Please log in first!")
    st.stop()

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = {}

if "current_feedback_msg" not in st.session_state:
    st.session_state.current_feedback_msg = None

if "user_language" not in st.session_state:
    st.session_state.user_language = 'en'

# Header with user info and language indicator
current_lang = st.session_state.get('user_language', 'en')
language_options = {
    'en': '🇺🇸 English',
    'es': '🇪🇸 Spanish', 
    'fr': '🇫🇷 French',
    'de': '🇩🇪 German',
    'it': '🇮🇹 Italian',
    'pt': '🇵🇹 Portuguese',
    'zh': '🇨🇳 Chinese',
    'ja': '🇯🇵 Japanese',
    'ko': '🇰🇷 Korean',
    'ar': '🇸🇦 Arabic',
    'hi': '🇮🇳 Hindi',
    'ru': '🇷🇺 Russian'
}
current_lang_display = language_options.get(current_lang, '🇺🇸 English')

st.markdown(f"""
<div style="background-color: #f8f9fa; padding: 0.4rem 0.6rem; border-radius: 0.3rem; margin-bottom: 0rem; border: 1px solid #dee2e6;">
    <h3 style="margin: 0; color: #333; font-size: 1.1rem; font-weight: 600;">KIITOS - Global IT Support Assistant</h3>
    <p style="margin: 0; color: #666; font-size: 0.8rem; margin-top: 0.1rem;">Get instant help or create a support ticket</p>
</div>
""", unsafe_allow_html=True)

# Add welcome message if no chat history
if not st.session_state.chat_history:
    # Add initial welcome message
    welcome_msg = f"Hello! I'm your IT Helpdesk Assistant. I'm here to help you with technical issues, software problems, and IT questions. How can I assist you today?"
    st.session_state.chat_history.append({
        "role": "assistant",
        "message": welcome_msg,
        "timestamp": datetime.now().strftime("%H:%M")
    })

# WhatsApp-style chat interface (removed extra spacing)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
for i, chat in enumerate(st.session_state.chat_history):
    if chat["role"] == "user":
        # WhatsApp-style user message (right side, green)
        st.markdown(f"""
        <div class="message-container-user">
            <div class="user-message">
                <div>{chat['message']}</div>
                <div class="message-time">{chat['timestamp']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:  # assistant message
        # WhatsApp-style assistant message (left side, white)
        st.markdown(f"""
        <div class="message-container-assistant">
            <div class="assistant-message">
                <div>{chat['message']}</div>
                <div class="message-time">{chat['timestamp']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add feedback buttons ONLY after assistant responses (not welcome message)
        if i > 0:  # Skip welcome message
            feedback_key = f"feedback_{i}"
            
            # Check if feedback already given for this message
            if feedback_key not in st.session_state.feedback_given:
                # Show feedback buttons
                st.markdown("---")
                st.markdown("**🔄 Was this response helpful?**")
                
                # Horizontal buttons using columns with corner positioning
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    helpful_btn = st.button(
                        "👍 Helpful", 
                        key=f"helpful_{i}",
                        use_container_width=True
                    )
                
                with col3:
                    not_helpful_btn = st.button(
                        "👎 Not Helpful", 
                        key=f"not_helpful_{i}",
                        use_container_width=True
                    )
                
                if helpful_btn:
                    st.session_state.feedback_given[feedback_key] = "helpful"
                    st.rerun()
                
                if not_helpful_btn:
                    st.session_state.feedback_given[feedback_key] = "not_helpful"
                    st.session_state.current_feedback_msg = i
                    st.rerun()
            
            else:
                # Show feedback result
                feedback_type = st.session_state.feedback_given[feedback_key]
                
                if feedback_type == "helpful":
                    # Only show follow-up input if no new conversation has started
                    latest_messages = st.session_state.chat_history[i+1:]
                    if not latest_messages:  # No new messages after this feedback
                        # Show new chat input for next question
                        st.markdown("---")
                        st.markdown("**💬 Great! Do you have another question?**")
                        
                        # Create a follow-up input that matches main chat input
                        with st.form(key=f"follow_up_form_{i}", clear_on_submit=True):
                            col1, col2 = st.columns([6, 1])
                            with col1:
                                follow_up_query = st.text_area(
                                    " ",
                                    placeholder="Ask your next question or type 'thank you' to end... (Enter for new line, Ctrl+Enter to send)",
                                    key=f"follow_up_input_{i}",
                                    label_visibility="collapsed",
                                    height=60
                                )
                            with col2:
                                submit_follow_up = st.form_submit_button("➤", type="primary", use_container_width=True)
                            
                            if submit_follow_up and follow_up_query.strip():
                                # Check if user wants to end the chat
                                if follow_up_query.lower().strip() in ['thank you', 'thanks', 'thank you!', 'thanks!', 'ty', 'thx']:
                                    st.success("🙏 Thank you for using our IT Helpdesk! Have a great day!")
                                    # Add farewell message to chat history
                                    st.session_state.chat_history.append({
                                        "role": "user",
                                        "message": follow_up_query,
                                        "timestamp": datetime.now().strftime("%H:%M")
                                    })
                                    st.session_state.chat_history.append({
                                        "role": "assistant", 
                                        "message": "Thank you for using our IT Helpdesk! Have a great day! 👋",
                                        "timestamp": datetime.now().strftime("%H:%M")
                                    })
                                    st.rerun()
                                else:
                                    # Continue with new question
                                    # Always detect language for each follow-up query
                                    detected_lang = language_support.detect_language(follow_up_query)
                                    
                                    # Update session language if changed
                                    if detected_lang != st.session_state.user_language:
                                        st.session_state.user_language = detected_lang
                                    
                                    # Use detected language for this specific follow-up query
                                    current_followup_language = detected_lang
                                    
                                    # Add user message to chat history
                                    st.session_state.chat_history.append({
                                        "role": "user", 
                                        "message": follow_up_query, 
                                        "timestamp": datetime.now().strftime("%H:%M"),
                                        "language": current_followup_language
                                    })
                                    
                                    # Get user context for AI with detected language
                                    user_context = {
                                        'username': st.session_state.get('username', 'User'),
                                        'user_id': st.session_state.get('user_id', 'unknown'),
                                        'email': st.session_state.get('email', 'user@company.com'),
                                        'language': current_followup_language,
                                        'language_prompt': language_support.get_language_prompt(current_followup_language)
                                    }
                                    
                                    # Get assistant response
                                    response = match_query(follow_up_query, user_context, st.session_state.chat_history)
                                    
                                    # Format response for the detected language
                                    formatted_response = language_support.format_multilingual_response(response, current_followup_language)
                                    
                                    st.session_state.chat_history.append({
                                        "role": "assistant", 
                                        "message": formatted_response, 
                                        "timestamp": datetime.now().strftime("%H:%M"),
                                        "language": current_followup_language
                                    })
                                    
                                    st.rerun()
                        # If there are new messages, don't show anything else - the conversation continues
                    
                if feedback_type == "not_helpful":
                    # Show ticket creation question directly
                    st.info("💡 Would you like to create a ticket for a human to assist you?")
                    
                    col_yes, col_middle, col_no = st.columns([1, 2, 1])
                    
                    with col_yes:
                        if st.button("✅ Yes, Create Ticket", key=f"create_ticket_{i}"):
                            # Prepare ticket summary
                            user_message = "General inquiry"
                            if i > 0 and i-1 < len(st.session_state.chat_history):
                                user_message = st.session_state.chat_history[i-1]['message']
                            
                            st.session_state.summary = f"User needed assistance with: {user_message}"
                            st.session_state.query = user_message
                            st.session_state.solution = chat['message']
                            st.session_state.show_satisfaction = True
                            st.session_state.show_ticket_form = True
                            st.switch_page("pages/3_Ticket.py")
                    
                    with col_no:
                        if st.button("❌ No, Thank You", key=f"no_ticket_{i}"):
                            st.session_state.feedback_given[feedback_key] = "completed"
                            st.success("🙏 Thank you for your feedback. We appreciate your time!")
                            st.rerun()
                
                elif feedback_type == "completed":
                        st.success("🙏 Thank you for your feedback. We appreciate your time!")

# Close WhatsApp-style chat container
st.markdown('</div>', unsafe_allow_html=True)

# Check if we should show the main chat input
show_main_chat = True
if len(st.session_state.chat_history) > 1:
    # Get the last assistant message index
    last_assistant_index = None
    for i in range(len(st.session_state.chat_history) - 1, -1, -1):
        if st.session_state.chat_history[i]["role"] == "assistant":
            last_assistant_index = i
            break
    
    if last_assistant_index is not None and last_assistant_index > 0:
        feedback_key = f"feedback_{last_assistant_index}"
        # Don't show main chat if feedback hasn't been given for the last assistant message
        if feedback_key not in st.session_state.feedback_given:
            show_main_chat = False
        # Also don't show if user clicked helpful but hasn't used the follow-up yet
        elif st.session_state.feedback_given.get(feedback_key) == "helpful":
            show_main_chat = False
        # Also don't show if user clicked not helpful (showing ticket options)
        elif st.session_state.feedback_given.get(feedback_key) == "not_helpful":
            show_main_chat = False

# Only show main chat input when appropriate
if show_main_chat:
    # Chat input with Send button
    user_lang = st.session_state.get('user_language', 'en')
    placeholder_text = language_support.get_text('ask_question', user_lang)
    
    # Chat input with Send button using form for proper alignment
    with st.form(key=f"main_chat_form_{st.session_state.input_key}", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            # Using text_area instead of text_input to allow multi-line input
            user_input = st.text_area(
                " ", 
                placeholder="Ask your IT question... (Enter for new line, Ctrl+Enter to send)",
                key=f"chat_input_{st.session_state.input_key}",
                label_visibility="collapsed",
                height=60
            )
        with col2:
            # Send button properly aligned with the input
            send_btn = st.form_submit_button("➤", type="primary", use_container_width=True)
    
    # Handle message sending with Send button
    if send_btn and user_input and user_input.strip():
        # Always detect language for each new query
        detected_lang = language_support.detect_language(user_input)
        
        # Update session language and show notification if changed
        if detected_lang != st.session_state.user_language:
            st.session_state.user_language = detected_lang
            # Show language change notification
            st.info(f"🌐 Language detected: {language_options.get(detected_lang, detected_lang)}")
        
        # Always use the detected language for this specific query
        current_query_language = detected_lang
        
        # Add user message to chat history with language info
        st.session_state.chat_history.append({
            "role": "user", 
            "message": user_input, 
            "timestamp": datetime.now().strftime("%H:%M"),
            "language": current_query_language
        })
        
        # Get user context for AI with the detected language for this query
        user_context = {
            'username': st.session_state.get('username', 'User'),
            'user_id': st.session_state.get('user_id', 'unknown'),
            'email': st.session_state.get('email', 'user@company.com'),
            'language': current_query_language,
            'language_prompt': language_support.get_language_prompt(current_query_language)
        }
        
        # Get assistant response
        response = match_query(user_input, user_context, st.session_state.chat_history)
        
        # Format response for the detected language (not session language)
        formatted_response = language_support.format_multilingual_response(response, current_query_language)
        
        st.session_state.chat_history.append({
            "role": "assistant", 
            "message": formatted_response, 
            "timestamp": datetime.now().strftime("%H:%M"),
            "language": current_query_language
        })
        
        # Update session variables for potential ticket creation
        st.session_state.query = user_input
        st.session_state.solution = response
        
        # Clear input field by incrementing the key
        st.session_state.input_key += 1
        
        st.rerun()