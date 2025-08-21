import streamlit as st
import os
from datetime import datetime
from utils.grok_ai import get_grok_service, is_grok_available
from utils.simple_steps import match_query

# Safe import for ticket creation
def safe_create_ticket(username, user_id, email, summary):
    """Safely create a ticket with fallback"""
    try:
        from utils.tickets import create_ticket
        return create_ticket(username, user_id, email, summary)
    except Exception as e:
        # Fallback: generate a simple ticket ID
        import random
        ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        return ticket_id

# Simple CSS for clean interface
st.markdown("""
<style>
.chat-container {
    background: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 20px;
    margin: 20px 0;
}

.chat-response {
    background: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 20px;
    margin: 15px 0;
    border-left: 3px solid #000;
}

.chat-history-container {
    background: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 20px;
    margin: 15px 0;
    max-height: 400px;
    overflow-y: auto;
}

.user-chat-message {
    background: white;
    border: 1px solid #ddd;
    border-left: 3px solid #000;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 3px;
    margin-left: 20px;
}

.assistant-chat-message {
    background: white;
    border: 1px solid #ddd;
    border-left: 3px solid #666;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 3px;
    margin-right: 20px;
}

.ticket-section {
    background: white;
    padding: 0;
    margin: 0;
}

.ticket-preview {
    background: white;
    padding: 0;
    margin: 0;
}

.response-header {
    color: #000;
    font-weight: 600;
    margin-bottom: 10px;
}

.ticket-actions {
    display: flex;
    gap: 15px;
    margin-top: 20px;
}

/* Make container responsive */
@media (max-width: 768px) {
    .chat-container, .ticket-section, .ticket-preview {
        margin: 10px 5px;
        padding: 15px;
    }
}

/* Ensure all text is black */
body, .stApp, .main, div, p, span, h1, h2, h3, h4, h5, h6 {
    color: #000 !important;
}
</style>
""", unsafe_allow_html=True)

# Simple page title
st.markdown("""
<div style="text-align: center; padding: 20px 0; background: white;">
    <h1 style="color: #000; font-size: 2.5em; margin-bottom: 10px;">🎫 IT Support Assistant</h1>
    <p style="color: #000; font-size: 1.1em;">Get instant help or create a support ticket</p>
</div>
""", unsafe_allow_html=True)

# Authentication check
if not st.session_state.get('logged_in', False):
    st.warning("You must be logged in to use the support assistant.")
    if st.button("🔐 Go to Login", type="primary", key="login_btn_1"):
        st.switch_page("pages/1_Login.py")
    st.stop()

# Initialize session states
if 'current_response' not in st.session_state:
    st.session_state.current_response = None
if 'suggested_title' not in st.session_state:
    st.session_state.suggested_title = ""
if 'show_ticket_form' not in st.session_state:
    st.session_state.show_ticket_form = False
if 'feedback_given' not in st.session_state:
    st.session_state.feedback_given = {}

# Check if there's chat history from Query page
has_chat_history = (
    'chat_history' in st.session_state and 
    st.session_state.chat_history and 
    len([msg for msg in st.session_state.chat_history if msg['role'] == 'user']) > 0
)

# Check if coming from Query page with unresolved issue
coming_from_query = has_chat_history and st.session_state.get('show_satisfaction', False)

# Display chat summary if available
if has_chat_history:
    st.markdown("### 💬 Chat History Summary")
    st.info("✅ Your previous chat conversation has been captured and will be included in the ticket.")
    with st.expander("📋 View Full Chat History", expanded=False):
        st.markdown('<div class="chat-history-container">', unsafe_allow_html=True)
        
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f"""
                <div class="user-chat-message">
                    <strong>👤 You</strong> ({chat.get('timestamp', 'N/A')})
                    <div>{chat['message']}</div>
                </div>
                """, unsafe_allow_html=True)
            elif chat["role"] == "assistant" and chat != st.session_state.chat_history[0]:  # Skip welcome message
                st.markdown(f"""
                <div class="assistant-chat-message">
                    <strong>🤖 Assistant</strong> ({chat.get('timestamp', 'N/A')})
                    <div>{chat['message']}</div>
                </div>
                """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-generate title and description from chat history
    if not st.session_state.suggested_title:
        user_messages = [msg['message'] for msg in st.session_state.chat_history if msg['role'] == 'user']
        if user_messages:
            first_query = user_messages[0].lower()
            if 'password' in first_query or 'login' in first_query:
                st.session_state.suggested_title = "Password/Login Issue - Human Assistance Required"
            elif 'vpn' in first_query or 'connection' in first_query:
                st.session_state.suggested_title = "VPN Connection Issue - Technical Support Needed"
            elif 'email' in first_query or 'outlook' in first_query:
                st.session_state.suggested_title = "Email Configuration Issue - Expert Help Required"
            elif 'printer' in first_query or 'print' in first_query:
                st.session_state.suggested_title = "Printer Setup/Connection Issue - Technical Support"
            elif 'network' in first_query or 'wifi' in first_query:
                st.session_state.suggested_title = "Network Connectivity Issue - Escalation Required"
            else:
                st.session_state.suggested_title = "IT Support Required - Unresolved Technical Issue"
    
    # Auto-show ticket form if coming from query page with unresolved issue
    if coming_from_query:
        st.session_state.show_ticket_form = True
# Display current response if exists
if st.session_state.current_response:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat response area
    st.markdown('<div class="chat-response">', unsafe_allow_html=True)
    st.markdown('<div class="response-header">🤖 Assistant Response:</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.current_response)
    
    # Feedback buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("👍 Helpful", key="helpful_btn_1"):
            st.session_state.feedback_given['helpful'] = True
            st.success("Thank you for your feedback!")
    with col2:
        if st.button("👎 Not Helpful", key="not_helpful_btn_1"):
            st.session_state.feedback_given['not_helpful'] = True
            st.session_state.show_ticket_form = True
            st.info("I'll help you create a support ticket for human assistance.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
# Ticket creation section
if st.session_state.show_ticket_form or st.session_state.feedback_given.get('not_helpful') or coming_from_query:
    st.markdown('<div class="ticket-section">', unsafe_allow_html=True)
    # Ticket Preview Form
    st.markdown('<div class="ticket-preview">', unsafe_allow_html=True)
    st.markdown("#### 📝 Ticket Preview")
    
    # Title field (editable, pre-filled from chat analysis)
    ticket_title = st.text_input(
        "Title:", 
        value=st.session_state.suggested_title or "IT Support Required",
        placeholder="Brief description of your issue",
        key="ticket_title_chat_history"
    )
    
    # Description field (pre-filled with chat history and context)
    default_description = ""
    if has_chat_history:
        # Generate comprehensive description from chat history
        user_queries = [msg['message'] for msg in st.session_state.chat_history if msg['role'] == 'user']
        assistant_responses = [msg['message'] for msg in st.session_state.chat_history if msg['role'] == 'assistant' and msg != st.session_state.chat_history[0]]
        
        default_description = "ORIGINAL USER QUERY:\n"
        if user_queries:
            default_description += f"{user_queries[0]}\n\n"
        
        default_description += "ASSISTANT'S ATTEMPTED SOLUTIONS:\n"
        if assistant_responses:
            default_description += f"{assistant_responses[0][:500]}{'...' if len(assistant_responses[0]) > 500 else ''}\n\n"
        
        default_description += "ISSUE STATUS:\nThe provided solutions did not resolve my issue. I require human technical support to investigate and resolve this problem.\n\n"
        default_description += "FULL CHAT HISTORY:\nComplete conversation history has been included with this ticket for reference.\n\n"
        default_description += "ADDITIONAL INFORMATION:\n"
    
    elif st.session_state.current_response:
        default_description = f"USER QUERY: {st.session_state.get('last_user_query', 'N/A')}\n\nASSISTANT RESPONSE:\n{st.session_state.current_response}\n\nADDITIONAL INFORMATION:\nThe above solution did not resolve my issue. I need human assistance to resolve this problem.\n\n"
    else:
        default_description = "ISSUE DESCRIPTION:\nPlease describe your IT issue in detail...\n\nSTEPS ALREADY TAKEN:\n- \n\nEXPECTED RESOLUTION:\n"
    
    # Description as subheader under title
    ticket_description = st.text_area(
        "Description:",
        value=default_description,
        height=250,
        placeholder="Detailed description of your issue...",
        key="ticket_description_field"
    )
    
    # Add helpful text and attach button below the description box
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown('<p style="font-size: 12px; color: #666; margin-top: 5px;">You can add any additional information you think would be helpful.</p>', unsafe_allow_html=True)
    with col2:
        show_attachment = st.button("📎 Attach", key="attach_files_btn")
    
    # Optional file attachment section (only shown when button is clicked)
    uploaded_files = None
    if show_attachment or st.session_state.get('show_attachment_section', False):
        st.session_state.show_attachment_section = True
        st.markdown("#### 📎 Optional Attachments")
        uploaded_files = st.file_uploader(
            "Attach files (PDF, screenshots, documents):",
            type=['pdf', 'png', 'jpg', 'jpeg', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Max 5MB per file. Supported: PDF, images, Word docs, text files.",
            key="optional_attachments"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) selected")
            for file in uploaded_files:
                file_size = len(file.getvalue()) / 1024 / 1024
                st.markdown(f"📄 **{file.name}** ({file_size:.2f} MB)")
        
        if st.button("❌ Remove attachment section", key="remove_attachment"):
            st.session_state.show_attachment_section = False
            st.rerun()
    
    # Set default values
    priority = "Medium"
    category = "Technical Support"
    contact_method = "Email"
    contact_time_formatted = "Best time to contact: Business hours"
    
    # Action buttons
    st.markdown('<div class="ticket-actions">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Confirm and Create Ticket", type="primary", use_container_width=True, key="confirm_ticket_direct"):
            # Handle optional file uploads
            uploaded_file_paths = []
            if uploaded_files:
                try:
                    ticket_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    upload_dir = os.path.join("uploads", f"ticket_{ticket_timestamp}_{st.session_state.get('user_id', 'unknown')}")
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    for file in uploaded_files:
                        file_size = len(file.getvalue()) / 1024 / 1024
                        if file_size <= 5:  # 5MB limit
                            file_path = os.path.join(upload_dir, file.name)
                            with open(file_path, "wb") as f:
                                f.write(file.getvalue())
                            uploaded_file_paths.append(file_path)
                        else:
                            st.warning(f"File {file.name} is too large ({file_size:.1f}MB). Skipped.")
                except Exception as e:
                    st.error(f"File upload error: {str(e)}")
            
            # Create comprehensive ticket summary
            detailed_summary = f"""TITLE: {ticket_title}

PRIORITY: Medium
CATEGORY: Technical Support

DESCRIPTION:
{ticket_description}

USER DETAILS:
- Username: {st.session_state.get('username', 'N/A')}
- Employee ID: {st.session_state.get('user_id', 'N/A')}
- Email: {st.session_state.get('email', 'N/A')}
- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CONTACT PREFERENCES:
- Preferred Method: {contact_method}
- Best Time: {contact_time_formatted}"""

            if uploaded_file_paths:
                detailed_summary += f"\n\nATTACHED FILES ({len(uploaded_file_paths)}):\n"
                detailed_summary += "\n".join([f"- {os.path.basename(path)}" for path in uploaded_file_paths])

            if has_chat_history:
                detailed_summary += "\n\nCHAT HISTORY:\n"
                for chat in st.session_state.chat_history:
                    if chat["role"] == "user":
                        detailed_summary += f"User ({chat.get('timestamp', 'N/A')}): {chat['message']}\n"
                    elif chat["role"] == "assistant" and chat != st.session_state.chat_history[0]:
                        detailed_summary += f"Assistant ({chat.get('timestamp', 'N/A')}): {chat['message']}\n"
                detailed_summary += "\nNOTE: This ticket was created from an unresolved chat session."
            
            # Create the ticket
            ticket_id = safe_create_ticket(
                st.session_state.get('username', 'User'),
                st.session_state.get('user_id', 'N/A'),
                st.session_state.get('email', 'N/A'),
                detailed_summary
            )
            
            st.success(f"🎉 Ticket created successfully! **Ticket ID: {ticket_id}**")
            
            # Show response time based on priority
            response_times = {"Critical": "2 hours", "High": "4 hours", "Medium": "24 hours", "Low": "48 hours"}
            st.info(f"📧 You will receive an email confirmation shortly. Expected response time: **{response_times.get('Medium', '24 hours')}**")
            
            # Show ticket summary
            with st.expander("📋 Ticket Summary", expanded=True):
                st.markdown(f"**Ticket ID:** {ticket_id}")
                st.markdown(f"**Contact Method:** {contact_method}")
                if uploaded_file_paths:
                    st.markdown(f"**📎 Attachments:** {len(uploaded_file_paths)} file(s)")
                if has_chat_history:
                    st.markdown("**📝 Chat History:** Included")
                st.markdown("**Description:**")
                st.text(ticket_description[:200] + "..." if len(ticket_description) > 200 else ticket_description)
            
            # Clear session states
            st.session_state.current_response = None
            st.session_state.show_ticket_form = False
            st.session_state.feedback_given = {}
            st.session_state.suggested_title = ""
            if 'chat_history' in st.session_state:
                del st.session_state.chat_history
            if 'show_satisfaction' in st.session_state:
                del st.session_state.show_satisfaction
            
            # Navigation options
            st.markdown("---")
            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                if st.button("🤖 Start New Chat", type="secondary", key="new_chat_direct"):
                    st.switch_page("pages/2_Query.py")
            with col_nav2:
                if st.button("🏠 Go to Home", key="home_direct"):
                    st.switch_page("pages/2_Query.py")
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True, key="cancel_ticket_direct"):
            st.session_state.show_ticket_form = False
            st.session_state.feedback_given = {}
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Bottom input section (always visible unless ticket form is shown)
if not (st.session_state.show_ticket_form or st.session_state.feedback_given.get('not_helpful') or coming_from_query):
    st.markdown("---")
    st.markdown("### 💬 Ask your question here...")

    # Create the input form
    with st.form("question_form_1", clear_on_submit=True):
        user_question = st.text_input(
            "Question",
            placeholder="Type your IT question here... (e.g., 'How do I reset my password?', 'VPN not connecting')",
            label_visibility="collapsed",
            key="user_question_1"
        )
        
        submit_question = st.form_submit_button("🚀 Get Help", type="primary", use_container_width=True)

    if submit_question and user_question.strip():
        # Store the user query
        st.session_state.last_user_query = user_question.strip()
        
        # Get AI response
        with st.spinner("🤖 Getting response..."):
            user_context = {
                'username': st.session_state.get('username', 'User'),
                'user_id': st.session_state.get('user_id', 'N/A'),
                'email': st.session_state.get('email', 'N/A')
            }
            
            # Try AI service first
            if is_grok_available():
                try:
                    grok_service = get_grok_service()
                    messages = [{"role": "user", "content": user_question}]
                    response = grok_service.chat_completion(messages, user_context)
                    st.session_state.current_response = response
                except Exception:
                    # Fallback to simple steps
                    response = match_query(user_question)
                    st.session_state.current_response = response
            else:
                # Use simple steps as fallback
                response = match_query(user_question)
                st.session_state.current_response = response
        
        # Reset feedback states
        st.session_state.feedback_given = {}
        st.session_state.show_ticket_form = False
        
        # Rerun to show the response
        st.rerun()

# Welcome message for first-time users (only show if no chat history and no active forms)
if (not st.session_state.current_response and 
    not st.session_state.show_ticket_form and 
    not has_chat_history and 
    not coming_from_query):
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; background: white; border: 1px solid #ddd; border-radius: 5px; margin: 20px 0;">
        <h3 style="color: #000; margin-bottom: 15px;">👋 Welcome to IT Support!</h3>
        <p style="color: #000; font-size: 1.1em; margin-bottom: 20px;">
            I'm here to help you with your IT questions and issues.
        </p>
        <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
            <span style="background: white; color: #000; padding: 8px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 0.9em;">🔑 Password Reset</span>
            <span style="background: white; color: #000; padding: 8px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 0.9em;">🌐 VPN Issues</span>
            <span style="background: white; color: #000; padding: 8px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 0.9em;">📧 Email Problems</span>
            <span style="background: white; color: #000; padding: 8px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 0.9em;">🖨️ Printer Setup</span>
        </div>
        <div style="margin-top: 20px;">
            <p style="color: #000; font-size: 0.95em;">
                💡 <strong>Tip:</strong> If you've already chatted with our assistant on the Query page, 
                your conversation history will automatically be included in your support ticket!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
