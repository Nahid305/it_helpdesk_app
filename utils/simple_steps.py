import json
import os

# Import Grok AI service
try:
    from .grok_ai import get_grok_service, is_grok_available
except ImportError:
    def get_grok_service():
        return None
    def is_grok_available():
        return False

# Import language support
try:
    from .language_support import LanguageSupport
    language_support = LanguageSupport()
except ImportError:
    language_support = None

def load_steps():
    path = os.path.join(os.path.dirname(__file__), '../data/dummy_steps.json')
    with open(path, 'r') as f:
        return json.load(f)

def match_query(query, user_context=None, chat_history=None):
    """Enhanced query matching with AI and NLP fallback."""
    
    # Try Grok AI first if available
    if is_grok_available():
        try:
            from .grok_ai import get_grok_service
            
            service = get_grok_service()
            if service:
                # Convert chat history to the format expected by AI
                formatted_history = []
                if chat_history:
                    for chat in chat_history[-10:]:  # Last 10 messages for context
                        if chat['role'] == 'user':
                            formatted_history.append({"role": "user", "content": chat['message']})
                        elif chat['role'] == 'assistant' and chat['message'] != chat_history[0]['message']:  # Skip welcome message
                            formatted_history.append({"role": "assistant", "content": chat['message']})
                
                # Add current query
                formatted_history.append({"role": "user", "content": query})
                
                # Get AI response
                response = service.chat_completion(formatted_history, user_context)
                return response
        except Exception as e:
            # Fall back to basic NLP if AI fails
            print(f"AI service error: {e}")
    
    # Fallback to basic NLP matching
    return _basic_nlp_match(query, user_context)

def _basic_nlp_match(query, user_context=None):
    """Basic NLP matching for when AI is not available."""
    
    user_name = user_context.get('username', 'there') if user_context else 'there'
    user_language = user_context.get('language', 'en') if user_context else 'en'
    query_lower = query.lower()
    
    # Use language support to format responses if available
    if language_support:
        # Get language-appropriate response format
        response_formatter = language_support.format_response
        get_text = language_support.get_text
    else:
        # Fallback to English
        response_formatter = lambda text, lang: text
        get_text = lambda key, lang='en': key.replace('_', ' ').title()
    
    # Password reset queries
    if any(word in query_lower for word in ['password', 'login', 'forgot', 'reset', 'locked', 'contraseña', 'mot de passe', 'passwort']):
        if language_support:
            return language_support.format_response(f"""Hi {user_name}! I can definitely help you reset your password. This is one of the most common issues we handle! 😊

**Step 1:** Go to your company login portal at portal.company.com
**Step 2:** Click the 'Forgot Password' link below the login form  
**Step 3:** Enter your registered email address or employee ID
**Step 4:** Check your email for the reset link (arrives in 2-3 minutes)
**Step 5:** Click the reset link and create a new secure password
**Step 6:** Log in with your new password and update saved passwords

That should get you back into your account! 🎉 If you don't receive the reset email within 5 minutes, check your spam folder first.""", user_language)
        else:
            return f"""Hi {user_name}! I can definitely help you reset your password. This is one of the most common issues we handle! 😊

**Step 1:** Go to your company login portal at portal.company.com
**Step 2:** Click the 'Forgot Password' link below the login form  
**Step 3:** Enter your registered email address or employee ID
**Step 4:** Check your email for the reset link (arrives in 2-3 minutes)
**Step 5:** Click the reset link and create a new secure password
**Step 6:** Log in with your new password and update saved passwords

That should get you back into your account! 🎉 If you don't receive the reset email within 5 minutes, check your spam folder first."""
    
    # VPN issues
    elif any(word in query_lower for word in ['vpn', 'remote', 'connection', 'work from home']):
        return f"""Hello {user_name}! I'll help you get the VPN client working smoothly! 🔒

**Step 1:** Open your company software center or download portal
**Step 2:** Search for 'Corporate VPN Client' or 'Cisco AnyConnect'
**Step 3:** Click 'Install' and wait for download completion
**Step 4:** Run installer with administrator privileges (right-click > 'Run as administrator')
**Step 5:** Launch the VPN app from your desktop or start menu
**Step 6:** Enter server address: vpn.company.com
**Step 7:** Log in with your company credentials
**Step 8:** Click 'Connect' and check for green connection status

You should now be securely connected! 🌐 The connection icon will appear in your system tray."""

    # Email problems
    elif any(word in query_lower for word in ['email', 'outlook', 'mail', 'send', 'receive']):
        return f"""Hi {user_name}! Email problems can be frustrating. Let's get this fixed! 📧

**Step 1:** Check internet connection (try opening a website)
**Step 2:** Restart your email client completely (Outlook, etc.)
**Step 3:** Verify email settings (incoming/outgoing servers, ports)
**Step 4:** Check if mailbox is full - delete old emails if needed
**Step 5:** Temporarily disable antivirus email scanning
**Step 6:** Try webmail at webmail.company.com as a test
**Step 7:** Note any error messages for further troubleshooting

Email issues are often simple connectivity problems! 📬"""

    # Printer issues  
    elif any(word in query_lower for word in ['printer', 'print', 'printing']):
        return f"""Hey {user_name}! Printer troubles are classic IT challenges, but we can fix this! 🖨️

**Step 1:** Check printer is powered on and shows 'Ready' status
**Step 2:** Verify connection (ethernet cable or WiFi)
**Step 3:** Ensure computer and printer are on same network
**Step 4:** Update/reinstall printer drivers from manufacturer website
**Step 5:** Clear print queue: Control Panel > Devices > right-click printer > clear documents
**Step 6:** Run Windows printer troubleshooter
**Step 7:** Print test page from printer properties

Most printer issues are network or driver related! 🎯 These steps resolve the majority of problems."""

    # Slow computer
    elif any(word in query_lower for word in ['slow', 'performance', 'running slow', 'sluggish']):
        return f"""Hi {user_name}! Let's speed up your computer and get it running smoothly! ⚡

**Step 1:** Restart your computer (clears memory and processes)
**Step 2:** Check storage space (need at least 15% free)
**Step 3:** Run disk cleanup (type 'disk cleanup' in start menu)
**Step 4:** Install Windows updates (Settings > Update & Security)
**Step 5:** Run malware scan with Windows Defender
**Step 6:** Disable unnecessary startup programs (Task Manager > Startup)
**Step 7:** Consider RAM upgrade if computer is 4+ years old

These steps should give your computer a nice performance boost! 🚀"""

    # WiFi/Network issues
    elif any(word in query_lower for word in ['wifi', 'wi-fi', 'wireless', 'internet', 'network']):
        return f"""Hello {user_name}! WiFi problems can be really frustrating. Let's fix your connection! 📶

**Step 1:** Restart WiFi adapter (Network settings > disable/enable WiFi)
**Step 2:** Forget and reconnect to network (WiFi settings > manage networks)
**Step 3:** Test if other devices connect to same WiFi
**Step 4:** Restart router (unplug 30 seconds, plug back in)
**Step 5:** Update WiFi drivers (Device Manager > Network adapters)
**Step 6:** Reset network settings if needed (Settings > Network > Network reset)
**Step 7:** Contact network admin for corporate WiFi issues

WiFi problems usually respond well to these steps! 📡"""

    # Fallback to original logic for backward compatibility
    else:
        steps_db = load_steps()
        for keyword, steps in steps_db.items():
            if keyword in query_lower:
                instructions = '\n'.join([f"**Step {i+1}:** {step}" for i, step in enumerate(steps)])
                return f"Hi {user_name}! I understand you're having trouble with '{keyword}'. Please follow these steps carefully:\n\n{instructions}"
        
        # General help for unrecognized queries
        return f"""Hi {user_name}! I'm here to help with your IT issue! 🤔

I'd love to learn more about what's happening so I can assist you better:

• What were you trying to do when the problem started?
• Are you seeing any specific error messages?
• When did you first notice this issue?
• Has anything changed recently on your computer?

**Quick universal fixes that often work:**
• Restart your device
• Check all cable connections  
• Update your software/drivers
• Clear browser cache (for web issues)

Don't worry - we'll figure this out together! If you need immediate help, I can also help you create a support ticket for our technical team. 🎫"""
