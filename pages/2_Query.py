import streamlit as st
from utils.simple_steps import match_query
from utils.language_support import language_support
try:
    from utils.grok_ai import is_grok_available
except ImportError:
    def is_grok_available():
        return False
from datetime import datetime

# Check authentication - redirect to login if not logged in
if not st.session_state.get('logged_in', False):
    st.switch_page("pages/1_Login.py")

# Professional page configuration
st.set_page_config(
    page_title="IT Helpdesk Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"  # Show sidebar for language selection
)

# Simple CSS for clean interface
st.markdown("""
<style>
/* Hide sidebar navigation except language selector */
.css-1d391kg .css-1v0mbdj .stSidebar {
    width: 200px !important;
}

/* Modern CSS selectors for sidebar */
[data-testid="stSidebar"] {
    width: 200px !important;
    display: block !important;
}

.st-emotion-cache-1cypcdb, .st-emotion-cache-1v0mbdj {
    display: block !important;
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

/* Clean chat message styling */
.user-message, .assistant-message {
    background-color: #f8f9fa;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 8px;
    border-left: 4px solid #007bff;
}

.assistant-message {
    border-left-color: #28a745;
}

/* Professional Send Button Styling */
button[kind="primary"] {
    background-color: #2563eb !important;
    color: white !important;
    border: 1px solid #2563eb !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    min-height: 38px !important;
    margin: 0 !important;
}

button[kind="primary"]:hover {
    background-color: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
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
</style>
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
<div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border: 1px solid #dee2e6;">
    <h2 style="margin: 0; color: #333; display: inline-block;">🤖 IT Helpdesk Assistant</h2>
    <span style="float: right; color: #666; font-size: 0.9rem;">Language: {current_lang_display}</span>
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

# Language selector in sidebar (if visible)
with st.sidebar:
    st.markdown("### � Language Settings")
    
    selected_language = st.selectbox(
        "Choose your language:",
        options=list(language_options.keys()),
        format_func=lambda x: language_options[x],
        index=list(language_options.keys()).index(st.session_state.user_language),
        key="language_selector"
    )
    
    if selected_language != st.session_state.user_language:
        st.session_state.user_language = selected_language
        st.rerun()
    
    # Language info
    st.markdown("---")
    st.markdown("**Current Language:**")
    st.markdown(f"{language_options[st.session_state.user_language]}")
    
    # Language detection help
    st.markdown("---")
    st.markdown("**💡 Tip:** The system can auto-detect your language from your messages!")

# Chat interface - Display chat history
chat_container = st.container()
with chat_container:
    for i, chat in enumerate(st.session_state.chat_history):
        if chat["role"] == "user":
            # Display user message - simple and clean
            st.markdown(f"""
            <div class="user-message">
                <strong>👤 You</strong> ({chat['timestamp']})
                <div style="margin-top: 0.5rem;">{chat['message']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        else:  # assistant message
            # Display assistant message - simple and clean
            st.markdown(f"""
            <div class="assistant-message">
                <strong>🤖 Assistant</strong> ({chat['timestamp']})
                <div style="margin-top: 0.5rem;">{chat['message']}</div>
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
                                    submit_follow_up = st.form_submit_button("Send", type="primary", use_container_width=True)
                            
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
                    
                    elif feedback_type == "not_helpful":
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
            send_btn = st.form_submit_button("Send", type="primary", use_container_width=True)
    
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
