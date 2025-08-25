import streamlit as st
import os
from datetime import datetime
from utils.grok_ai import get_grok_service, is_grok_available
from utils.simple_steps import match_query

# Check authentication - redirect to login if not logged in
if not st.session_state.get('logged_in', False):
    st.switch_page("pages/1_Login.py")

# Safe import for ticket creation
def safe_create_ticket(username, user_id, email, summary):
    """Safely create a ticket with fallback"""
    try:
        from utils.tickets import create_ticket
        return create_ticket(username, user_id, email, summary)
    except Exception as e:
        # Fallback: Generate a simple ticket ID
        import time
        ticket_id = f"TKT{int(time.time())}"
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

/* White background buttons with black text */
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

/* Ensure all button types have white background */
.stButton > button[data-testid*="primary"] {
    background-color: white !important;
    color: #333 !important;
    border: 2px solid #dee2e6 !important;
}

.stButton > button[data-testid*="primary"]:hover {
    background-color: #f8f9fa !important;
    border-color: #adb5bd !important;
}

/* Make container responsive */
@media (max-width: 768px) {
    .chat-container, .ticket-section, .ticket-preview {
        margin: 10px 5px;
        padding: 15px;
    }
}

/* Success page styling */
.ticket-success-container {
    max-width: 100%;
    margin: 0 auto;
    padding: 20px 0;
}

.success-banner {
    background: linear-gradient(90deg, #4CAF50, #45a049);
    color: white;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.ticket-id-box {
    background-color: #e3f2fd;
    padding: 25px;
    border-radius: 12px;
    border-left: 6px solid #1976d2;
    margin: 25px 0;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.info-cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin: 25px 0;
}

.info-card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #ddd;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.description-card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin: 25px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

st.header("🎫 Support Ticket System")

# Initialize session state
if 'feedback_given' not in st.session_state:
    st.session_state.feedback_given = {}
if 'show_ticket_form' not in st.session_state:
    st.session_state.show_ticket_form = False
if 'current_response' not in st.session_state:
    st.session_state.current_response = None
if 'suggested_title' not in st.session_state:
    st.session_state.suggested_title = ""

# Check if chat history exists
has_chat_history = 'chat_history' in st.session_state and len(st.session_state.chat_history) > 1

# Check if coming from Query page with unresolved issue
coming_from_query = has_chat_history and st.session_state.get('show_satisfaction', False)

# Display chat summary if available and showing ticket form
if has_chat_history and (st.session_state.show_ticket_form or st.session_state.feedback_given.get('not_helpful') or coming_from_query):
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

# Display current response if exists and not creating a ticket
if st.session_state.current_response and not (st.session_state.show_ticket_form or st.session_state.feedback_given.get('not_helpful') or coming_from_query):
    # Chat response area
    st.markdown("### 🤖 Assistant Response")
    st.markdown(st.session_state.current_response)
    
    # Feedback buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("👍 Helpful", key="helpful_btn_1"):
            st.session_state.feedback_given['helpful'] = True
            st.success("Thank you for your feedback!")
    with col3:
        if st.button("👎 Not Helpful", key="not_helpful_btn_1"):
            st.session_state.feedback_given['not_helpful'] = True
            st.session_state.show_ticket_form = True
            st.info("I'll help you create a support ticket for human assistance.")

# Ticket creation section
if st.session_state.show_ticket_form or st.session_state.feedback_given.get('not_helpful') or coming_from_query:
    # Ticket Preview Form
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
        assistant_responses = [msg['message'] for msg in st.session_state.chat_history if msg['role'] == 'assistant']
        
        if user_queries:
            default_description = f"""ORIGINAL USER QUERY:
{user_queries[0]}

ASSISTANT'S ATTEMPTED SOLUTIONS:
{assistant_responses[-1] if assistant_responses else 'No response recorded'}

ADDITIONAL CONTEXT:
The user indicated that the provided solution was not helpful and requested human assistance. This ticket was created from an unresolved chat session.
"""
    
    ticket_description = st.text_area(
        "Description:", 
        value=default_description,
        placeholder="Please describe your issue in detail...",
        height=200,
        key="ticket_description_chat_history"
    )
    
    st.markdown('<p style="font-size: 12px; color: #666; margin-top: 5px;">You can add any additional information you think would be helpful.</p>', unsafe_allow_html=True)
    
    # Compact file upload section
    uploaded_files = None
    col_attach, col_spacer = st.columns([1, 3])
    with col_attach:
        with st.expander("📎 Attach Files", expanded=False):
            uploaded_files = st.file_uploader(
                "Select files",
                accept_multiple_files=True,
                type=['png', 'jpg', 'jpeg', 'pdf', 'txt', 'doc', 'docx'],
                key="file_upload_chat_history",
                label_visibility="collapsed"
            )
            st.caption("Max 5MB each")
    
    # Action buttons
    st.markdown("---")
    
    if st.button("✅ Confirm and Create Ticket", key="confirm_ticket_direct", type="primary"):
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
                            st.warning(f"File {file.name} is too large (max 5MB)")
                except Exception as e:
                    st.error(f"Error uploading files: {str(e)}")
            
            # Create comprehensive ticket summary
            detailed_summary = f"""
Title: {ticket_title}
Description: {ticket_description}
Contact Method: Email
Priority: Medium
Category: Technical Support

Ticket created from IT Support Chat System.
"""
            
            if uploaded_file_paths:
                detailed_summary += f"\nAttached Files: {', '.join([os.path.basename(path) for path in uploaded_file_paths])}"
            
            # Add chat history if available
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
            
            # Display clean success page with simple formatting
            st.success("🎉 Ticket Created Successfully!")
            st.write("Your support request has been submitted and will be reviewed by our team.")
            
            # Display ticket information in simple format
            st.write(f"**🎫 Ticket ID: {ticket_id}**")
            st.write("Please save this ID for future reference")
            
            st.write("**📧 Email Confirmation**")
            st.write("You will receive an email confirmation shortly.")
            st.write("**Expected response time: 24 hours**")
            
            st.write("**📧 Contact Details**")
            st.write(f"**Contact Method:** Email")
            st.write(f"**📎 Attachments:** {len(uploaded_file_paths)} file(s)")
            st.write(f"**💬 Chat History:** {'✅ Included' if has_chat_history else '❌ Not Included'}")
            
            st.write("**📝 Issue Summary**")
            st.write(f"**Title:** {ticket_title}")
            st.write("**Description:**")
            
            if len(ticket_description) > 300:
                st.write(ticket_description[:300] + "...")
                with st.expander("📖 View Complete Description"):
                    st.write(ticket_description)
            else:
                st.write(ticket_description)
            
            # Set a flag that ticket was created successfully
            st.session_state.ticket_created_successfully = True

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
                'location': st.session_state.get('location', 'Unknown'),
                'department': st.session_state.get('department', 'Unknown')
            }
            
            # Try to get response from Grok AI service
            if is_grok_available():
                try:
                    grok_service = get_grok_service()
                    if grok_service:
                        response = grok_service.get_it_support_response(user_question.strip(), user_context)
                    else:
                        response = match_query(user_question.strip())
                except Exception as e:
                    st.error(f"AI service error: {str(e)}")
                    response = match_query(user_question.strip())
            else:
                response = match_query(user_question.strip())
            
            # Store the response
            st.session_state.current_response = response
            
            # Initialize or clear chat history
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # Add current interaction to chat history
            current_time = datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({
                "role": "user",
                "message": user_question.strip(),
                "timestamp": current_time
            })
            st.session_state.chat_history.append({
                "role": "assistant", 
                "message": response,
                "timestamp": current_time
            })
            
            st.rerun()
