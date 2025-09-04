import os
import json
import requests
from typing import List, Dict, Any

# Try to import streamlit for secrets support
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

# Load environment variables from .env file if it exists
def load_env_vars():
    """Load environment variables from .env file"""
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def get_config_value(key: str, default: str = None):
    """Get configuration value from environment variables or Streamlit secrets"""
    # First try environment variables
    value = os.getenv(key, default)
    
    # If not found and Streamlit is available, try secrets
    if not value and STREAMLIT_AVAILABLE:
        try:
            value = st.secrets.get(key, default)
        except:
            pass
    
    return value

# Load environment variables
load_env_vars()

class GrokAIService:
    def __init__(self):
        self.api_key = get_config_value('GROK_API_KEY')
        self.api_url = get_config_value('GROK_API_URL', 'https://api.x.ai/v1')
        self.model = get_config_value('GROK_MODEL', 'grok-beta')
        self.org_id = get_config_value('GROK_ORG_ID')
        
        if not self.api_key:
            raise ValueError("GROK_API_KEY not found in environment variables or Streamlit secrets")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        if self.org_id:
            headers['OpenAI-Organization'] = self.org_id
        return headers
    
    def _get_helpdesk_system_prompt(self) -> str:
        """Get the system prompt for helpdesk-specific responses."""
        return """You are an expert IT Helpdesk Assistant for a global corporation. Your role is to:

1. **Provide immediate technical support** for common IT issues including:
   - Network connectivity problems
   - Software installation and troubleshooting
   - Hardware issues (printers, monitors, keyboards, etc.)
   - Password resets and account access
   - Email and communication tools
   - VPN and security-related queries
   - Operating system issues (Windows, macOS, Linux)
   - Microsoft Office and productivity software
   - Mobile device support

2. **Respond professionally** with:
   - Clear, step-by-step instructions
   - Technical accuracy appropriate for business users
   - Friendly but professional tone
   - Empathy for user frustration
   - Confidence in your solutions

3. **Structure your responses** with:
   - Brief acknowledgment of the issue
   - Numbered step-by-step solutions
   - Additional tips or warnings if relevant
   - Offer to escalate if the solution doesn't work

4. **For complex issues**:
   - Provide initial troubleshooting steps
   - Suggest when to escalate to human support
   - Recommend creating a support ticket for tracking

5. **Security awareness**:
   - Never ask for passwords or sensitive information
   - Provide secure best practices
   - Warn about potential security risks

Always maintain a helpful, solution-oriented approach while ensuring users feel supported and confident in implementing your suggestions."""

    def chat_completion(self, messages: List[Dict[str, str]], user_context: Dict[str, Any] = None) -> str:
        """
        Get a chat completion from Grok AI with helpdesk-specific context.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            user_context: Additional context about the user (username, department, etc.)
        
        Returns:
            AI response as string
        """
        try:
            # Prepare the system message with helpdesk context
            system_message = {
                "role": "system",
                "content": self._get_helpdesk_system_prompt()
            }
            
            # Add user context if provided
            if user_context:
                context_info = f"\nUser Context: Username: {user_context.get('username', 'N/A')}, ID: {user_context.get('user_id', 'N/A')}, Email: {user_context.get('email', 'N/A')}"
                system_message["content"] += context_info
                
                # Add language-specific instructions if available
                if 'language_prompt' in user_context and user_context['language_prompt']:
                    system_message["content"] = user_context['language_prompt'] + "\n\n" + system_message["content"]
            
            # Prepare the full message list
            full_messages = [system_message] + messages
            
            # Prepare the request payload
            payload = {
                "model": self.model,
                "messages": full_messages,
                "temperature": 0.7,
                "max_tokens": 1000,
                "stream": False
            }
            
            # Make the API request
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                # Fallback to dummy response if API fails
                return self._get_fallback_response(messages[-1]['content'] if messages else "")
                
        except Exception as e:
            # Fallback to dummy response on any error
            return self._get_fallback_response(messages[-1]['content'] if messages else "")
    
    def _get_fallback_response(self, user_query: str) -> str:
        """Provide a fallback response when AI service is unavailable."""
        fallback_responses = {
            "password": "I can help you reset your password. Please go to the company login portal, click 'Forgot Password', enter your registered email, and follow the reset link sent to your email to set a new secure password.",
            "vpn": "**Steps to install VPN:**\n1. Open company software center\n2. Search for 'Corporate VPN Client'\n3. Click 'Install' and wait for completion\n4. Launch VPN app and log in with your credentials\n5. Click 'Connect'",
            "email": "For email issues, try restarting your email client first. If that doesn't work, check your internet connection and verify your email settings. You may also try logging out and back into your email account.",
            "printer": "For printer issues: Check if the printer is powered on and connected to the network, ensure you have the latest printer drivers installed, clear any paper jams, and try printing a test page. If issues persist, restart both your computer and the printer.",
            "network": "For network connectivity issues: Check if your ethernet cable is properly connected, restart your router/modem, try connecting to a different network, and run the network troubleshooter from your system settings."
        }
        
        query_lower = user_query.lower()
        for keyword, response in fallback_responses.items():
            if keyword in query_lower:
                return f"🔧 **Quick Solution for {keyword.title()} Issue:**\n\n{response}\n\n<p style='font-size: 0.8rem; color: #003d82; margin: 0;'>Note: This is AI-generated content kindly evaluate the message</p>"
        
        return "I understand you need help with an IT issue. While I'm currently operating in limited mode, I recommend creating a support ticket so our technical team can provide you with detailed assistance. In the meantime, try restarting your device or application, which resolves many common issues."

    def generate_ticket_summary(self, chat_history: List[Dict[str, str]], user_context: Dict[str, Any] = None) -> str:
        """Generate a comprehensive ticket summary from chat history."""
        try:
            # Prepare messages for summarization
            chat_content = "\n".join([
                f"{msg['role'].title()}: {msg['message']}" 
                for msg in chat_history 
                if msg['role'] in ['user', 'assistant']
            ])
            
            summary_prompt = f"""Based on the following IT helpdesk chat conversation, create a comprehensive support ticket summary:

{chat_content}

Please provide:
1. **Issue Summary**: Brief description of the problem
2. **Steps Attempted**: What solutions were tried during the chat
3. **Current Status**: Whether the issue was resolved or needs escalation
4. **Recommended Next Steps**: What should be done next
5. **Priority Level**: Suggested priority (Low/Medium/High/Critical)
6. **Category**: IT category (Network, Software, Hardware, Security, etc.)

Format as a professional support ticket summary."""

            response = self.chat_completion([{"role": "user", "content": summary_prompt}], user_context)
            return response
            
        except Exception as e:
            # Fallback summary
            return f"**Support Ticket Summary**\n\nUser {user_context.get('username', 'N/A')} ({user_context.get('user_id', 'N/A')}) engaged in a chat session seeking IT assistance. The conversation included multiple exchanges between the user and the AI assistant. This ticket requires human review to determine the appropriate resolution steps.\n\n**Priority**: Medium\n**Category**: General IT Support"

# Global instance
grok_service = None

def get_grok_service():
    """Get or create the Grok AI service instance."""
    global grok_service
    if grok_service is None:
        try:
            grok_service = GrokAIService()
        except ValueError:
            # Return None if API key is not configured
            grok_service = None
    return grok_service

def is_grok_available() -> bool:
    """Check if Grok AI service is available and configured."""
    service = get_grok_service()
    return service is not None


