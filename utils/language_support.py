"""
Multi-Language Support for IT Helpdesk
Provides language detection, translation, and localized responses
"""

import streamlit as st
import json
import os
from typing import Dict, Any, Optional

class LanguageSupport:
    """Handles multi-language support for the IT Helpdesk"""
    
    def __init__(self):
        self.supported_languages = {
            'en': {'name': 'English', 'flag': '🇺🇸'},
            'es': {'name': 'Español', 'flag': '🇪🇸'},
            'fr': {'name': 'Français', 'flag': '🇫🇷'},
            'de': {'name': 'Deutsch', 'flag': '🇩🇪'},
            'it': {'name': 'Italiano', 'flag': '🇮🇹'},
            'pt': {'name': 'Português', 'flag': '🇵🇹'},
            'nl': {'name': 'Nederlands', 'flag': '🇳🇱'},
            'ru': {'name': 'Русский', 'flag': '🇷🇺'},
            'zh': {'name': '中文', 'flag': '🇨🇳'},
            'ja': {'name': '日本語', 'flag': '🇯🇵'},
            'ko': {'name': '한국어', 'flag': '🇰🇷'},
            'ar': {'name': 'العربية', 'flag': '🇸🇦'},
            'hi': {'name': 'हिन्दी', 'flag': '🇮🇳'}
        }
        self.load_translations()
    
    def load_translations(self):
        """Load translation dictionary for common IT terms and responses"""
        self.translations = {
            'en': {
                'welcome': "Hello! I'm your AI-powered IT Helpdesk assistant. How can I help you today?",
                'ask_question': "Ask your IT question:",
                'send': "Send",
                'helpful': "Helpful",
                'not_helpful': "Not Helpful", 
                'create_ticket': "Create Ticket",
                'new_chat': "Start New Chat",
                'end_chat': "End Chat",
                'clear_chat': "Clear Chat",
                'thank_you': "Thank you for using our IT Support! 😊",
                'new_session': "Starting a new chat session for you...",
                'ticket_question': "Would you like to create a ticket for a human to assist you?",
                'no_thanks': "No, thanks",
                'start_new_chat': "Start New Chat",
                'login_required': "You must be logged in to use the chat assistant.",
                'basic_mode': "⚡ **Basic Mode**: AI service unavailable, using rule-based responses. Check your API configuration in .env file.",
                'enter_message': "Please enter a message before sending.",
                'starting_new_chat': "Starting a new chat session for you...",
                'language_select': "Select Language:",
                'password_reset': "Password Reset",
                'vpn_issues': "VPN Issues",
                'email_problems': "Email Problems",
                'printer_setup': "Printer Setup",
                'network_issues': "Network Issues",
                'software_help': "Software Help"
            },
            'es': {
                'welcome': "¡Hola! Soy tu asistente de mesa de ayuda IT con IA. ¿Cómo puedo ayudarte hoy?",
                'ask_question': "Haz tu pregunta de IT:",
                'send': "Enviar",
                'helpful': "Útil",
                'not_helpful': "No Útil",
                'create_ticket': "Crear Ticket",
                'new_chat': "Nuevo Chat",
                'end_chat': "Terminar Chat",
                'clear_chat': "Limpiar Chat",
                'thank_you': "¡Gracias por usar nuestro soporte IT! 😊",
                'new_session': "Iniciando una nueva sesión de chat para ti...",
                'ticket_question': "¿Te gustaría crear un ticket para que un humano te asista?",
                'no_thanks': "No, gracias",
                'start_new_chat': "Iniciar Nuevo Chat",
                'login_required': "Debes iniciar sesión para usar el asistente de chat.",
                'basic_mode': "⚡ **Modo Básico**: Servicio de IA no disponible, usando respuestas basadas en reglas. Verifica tu configuración de API en el archivo .env.",
                'enter_message': "Por favor ingresa un mensaje antes de enviar.",
                'starting_new_chat': "Iniciando una nueva sesión de chat para ti...",
                'language_select': "Seleccionar Idioma:",
                'password_reset': "Restablecer Contraseña",
                'vpn_issues': "Problemas de VPN",
                'email_problems': "Problemas de Email",
                'printer_setup': "Configurar Impresora",
                'network_issues': "Problemas de Red",
                'software_help': "Ayuda de Software"
            },
            'fr': {
                'welcome': "Bonjour! Je suis votre assistant de support IT alimenté par IA. Comment puis-je vous aider aujourd'hui?",
                'ask_question': "Posez votre question IT:",
                'send': "Envoyer",
                'helpful': "Utile",
                'not_helpful': "Pas Utile",
                'create_ticket': "Créer Ticket",
                'new_chat': "Nouveau Chat",
                'end_chat': "Terminer Chat",
                'clear_chat': "Effacer Chat",
                'thank_you': "Merci d'utiliser notre support IT! 😊",
                'new_session': "Démarrage d'une nouvelle session de chat pour vous...",
                'ticket_question': "Souhaitez-vous créer un ticket pour qu'un humain vous assiste?",
                'no_thanks': "Non, merci",
                'start_new_chat': "Démarrer Nouveau Chat",
                'login_required': "Vous devez être connecté pour utiliser l'assistant de chat.",
                'basic_mode': "⚡ **Mode Basique**: Service IA indisponible, utilisant des réponses basées sur des règles. Vérifiez votre configuration API dans le fichier .env.",
                'enter_message': "Veuillez saisir un message avant d'envoyer.",
                'starting_new_chat': "Démarrage d'une nouvelle session de chat pour vous...",
                'language_select': "Sélectionner la Langue:",
                'password_reset': "Réinitialiser Mot de Passe",
                'vpn_issues': "Problèmes VPN",
                'email_problems': "Problèmes Email",
                'printer_setup': "Configuration Imprimante",
                'network_issues': "Problèmes Réseau",
                'software_help': "Aide Logiciel"
            },
            'de': {
                'welcome': "Hallo! Ich bin Ihr KI-gestützter IT-Helpdesk-Assistent. Wie kann ich Ihnen heute helfen?",
                'ask_question': "Stellen Sie Ihre IT-Frage:",
                'send': "Senden",
                'helpful': "Hilfreich",
                'not_helpful': "Nicht Hilfreich",
                'create_ticket': "Ticket Erstellen",
                'new_chat': "Neuer Chat",
                'end_chat': "Chat Beenden",
                'clear_chat': "Chat Löschen",
                'thank_you': "Vielen Dank für die Nutzung unseres IT-Supports!",
                'starting_new_chat': "Starte eine neue Chat-Sitzung für Sie...",
                'language_select': "Sprache Auswählen:",
                'password_reset': "Passwort Zurücksetzen",
                'vpn_issues': "VPN-Probleme",
                'email_problems': "E-Mail-Probleme",
                'printer_setup': "Drucker Einrichten",
                'network_issues': "Netzwerkprobleme",
                'software_help': "Software-Hilfe"
            },
            'zh': {
                'welcome': "您好！我是您的AI驱动的IT帮助台助手。今天我可以为您做些什么？",
                'ask_question': "请提出您的IT问题：",
                'send': "发送",
                'helpful': "有帮助",
                'not_helpful': "没帮助",
                'create_ticket': "创建工单",
                'new_chat': "新对话",
                'end_chat': "结束对话",
                'clear_chat': "清除对话",
                'thank_you': "感谢您使用我们的IT支持！",
                'starting_new_chat': "正在为您开始新的聊天会话...",
                'language_select': "选择语言：",
                'password_reset': "密码重置",
                'vpn_issues': "VPN问题",
                'email_problems': "邮箱问题",
                'printer_setup': "打印机设置",
                'network_issues': "网络问题",
                'software_help': "软件帮助"
            }
        }
    
    def get_supported_languages(self) -> Dict[str, Dict[str, str]]:
        """Get list of supported languages"""
        return self.supported_languages
    
    def get_text(self, key: str, language: str = 'en') -> str:
        """Get translated text for a given key and language"""
        if language not in self.translations:
            language = 'en'  # Fallback to English
        
        return self.translations[language].get(key, self.translations['en'].get(key, key))
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on common words and patterns"""
        text_lower = text.lower()
        
        # Simple keyword-based detection with scoring
        language_indicators = {
            'it': ['ciao', 'grazie', 'per favore', 'aiuto', 'problema', 'password', 'italiano', 'ho', 'bisogno', 'può', 'salve', 'buongiorno'],
            'es': ['hola', 'gracias', 'por favor', 'ayuda', 'problema', 'contraseña', 'español', 'tengo', 'necesito', 'puede', 'buenos días', 'quiero', 'instalar', 'como', 'donde', 'que', 'soy', 'estoy', 'mi', 'tu', 'su', 'este', 'esta'],
            'fr': ['bonjour', 'merci', 's\'il vous plaît', 'aide', 'problème', 'mot de passe', 'français', 'j\'ai', 'besoin', 'pouvez', 'salut'],
            'de': ['hallo', 'danke', 'bitte', 'hilfe', 'problem', 'passwort', 'deutsch', 'ich habe', 'brauche', 'können', 'guten tag'],
            'pt': ['olá', 'obrigado', 'por favor', 'ajuda', 'problema', 'senha', 'português', 'tenho', 'preciso', 'pode', 'bom dia'],
            'nl': ['hallo', 'dank je', 'alsjeblieft', 'hulp', 'probleem', 'wachtwoord', 'nederlands', 'ik heb', 'nodig', 'kunt', 'goedemorgen'],
            'zh': ['你好', '谢谢', '请', '帮助', '问题', '密码', '中文', '我有', '需要', '可以'],
            'ja': ['こんにちは', 'ありがとう', 'お願い', 'ヘルプ', '問題', 'パスワード', '日本語', '私は', '必要', 'できます'],
            'ko': ['안녕하세요', '감사합니다', '제발', '도움', '문제', '비밀번호', '한국어', '저는', '필요', '할 수'],
            'ar': ['مرحبا', 'شكرا', 'من فضلك', 'مساعدة', 'مشكلة', 'كلمة المرور', 'عربي', 'لدي', 'أحتاج', 'يمكن'],
            'ru': ['привет', 'спасибо', 'пожалуйста', 'помощь', 'проблема', 'пароль', 'русский', 'у меня', 'нужно', 'можете'],
            'hi': ['नमस्ते', 'धन्यवाद', 'कृपया', 'मदद', 'समस्या', 'पासवर्ड', 'हिंदी', 'मेरे पास', 'चाहिए', 'कर सकते']
        }
        
        # Score each language based on keyword matches
        language_scores = {}
        for lang, keywords in language_indicators.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                language_scores[lang] = score
        
        # Return the language with the highest score
        if language_scores:
            return max(language_scores.items(), key=lambda x: x[1])[0]
        
        return 'en'  # Default to English
    
    def format_multilingual_response(self, response: str, user_language: str) -> str:
        """Format response with language-appropriate styling"""
        if user_language == 'ar':
            # Right-to-left for Arabic
            return f'<div dir="rtl" style="text-align: right;">{response}</div>'
        elif user_language in ['zh', 'ja', 'ko']:
            # Special formatting for CJK languages
            return f'<div style="line-height: 1.6;">{response}</div>'
        else:
            return response
    
    def get_language_prompt(self, user_language: str) -> str:
        """Get language-specific prompt for AI responses"""
        prompts = {
            'es': "IMPORTANTE: Responde SIEMPRE en español. Eres un asistente de soporte técnico IT. Traduce toda tu respuesta al español, incluyendo títulos, pasos y notas. Usa términos técnicos en español cuando sea posible.",
            'fr': "IMPORTANT: Répondez TOUJOURS en français. Vous êtes un assistant de support technique IT. Traduisez toute votre réponse en français.",
            'de': "WICHTIG: Antworte IMMER auf Deutsch. Du bist ein IT-Support-Assistent. Übersetze deine gesamte Antwort ins Deutsche.",
            'zh': "重要：始终用中文回答。你是一个IT技术支持助手。将你的整个回答翻译成中文。",
            'ja': "重要：必ず日本語で答えてください。あなたはITサポートアシスタントです。回答全体を日本語に翻訳してください。",
            'ar': "مهم: أجب دائماً باللغة العربية. أنت مساعد دعم تقني IT. ترجم إجابتك كاملة إلى العربية.",
            'ru': "ВАЖНО: Всегда отвечай на русском языке. Ты помощник IT-поддержки. Переводи весь свой ответ на русский язык.",
            'hi': "महत्वपूर्ण: हमेशा हिंदी में जवाब दें। आप एक IT सपोर्ट असिस्टेंट हैं। अपना पूरा उत्तर हिंदी में अनुवाद करें।",
            'pt': "IMPORTANTE: Responda SEMPRE em português. Você é um assistente de suporte técnico IT. Traduza toda sua resposta para o português.",
            'it': "IMPORTANTE: Rispondi SEMPRE in italiano. Sei un assistente di supporto tecnico IT. Traduci tutta la tua risposta in italiano.",
            'nl': "BELANGRIJK: Antwoord ALTIJD in het Nederlands. Je bent een IT-ondersteuningsassistent. Vertaal je hele antwoord naar het Nederlands.",
            'ko': "중요: 항상 한국어로 답하세요. 당신은 IT 지원 도우미입니다. 전체 답변을 한국어로 번역하세요."
        }
        
        return prompts.get(user_language, "Respond in English. You are an IT support assistant.")
    
    def format_response(self, response: str, user_language: str) -> str:
        """Format a basic response in the user's language using simple translation patterns"""
        if user_language == 'en':
            return response
            
        # Simple keyword translation for basic responses
        translations = {
            'es': {
                'Hi': 'Hola', 'Hello': 'Hola', 'Step': 'Paso', 'Click': 'Haz clic',
                'Go to': 'Ve a', 'Enter': 'Ingresa', 'Check': 'Verifica',
                'That should get you back': 'Eso debería devolverle el acceso',
                'If you don\'t receive': 'Si no recibes', 'minutes': 'minutos',
                'check your spam folder': 'revisa tu carpeta de spam'
            },
            'fr': {
                'Hi': 'Salut', 'Hello': 'Bonjour', 'Step': 'Étape', 'Click': 'Cliquez',
                'Go to': 'Allez à', 'Enter': 'Entrez', 'Check': 'Vérifiez',
                'That should get you back': 'Cela devrait vous reconnecter',
                'If you don\'t receive': 'Si vous ne recevez pas', 'minutes': 'minutes',
                'check your spam folder': 'vérifiez votre dossier spam'
            }
            # Add more languages as needed
        }
        
        if user_language in translations:
            translated_response = response
            for english, translation in translations[user_language].items():
                translated_response = translated_response.replace(english, translation)
            return translated_response
        
        return response  # Return original if no translation available
    
    def get_welcome_message(self, username: str, is_grok_available: bool, language: str = None) -> str:
        """Generate a welcome message in the specified language"""
        if language is None:
            language = 'en'  # Default to English
        
        # Get base welcome text
        welcome_text = self.get_text('welcome', language)
        
        # Replace placeholder with username
        if language == 'en':
            welcome_text = welcome_text.replace("Hello!", f"Hello {username}!")
        else:
            # For other languages, just add username at appropriate place
            welcome_text = welcome_text.replace("Hello!", f"{username}!")
        
        # Add capability message based on Grok availability
        if is_grok_available:
            if language == 'en':
                welcome_text += " I can help you with a wide range of IT issues. What can I help you with today?"
            elif language == 'es':
                welcome_text += " Puedo ayudarte con una amplia gama de problemas de IT. ¿En qué puedo ayudarte hoy?"
            elif language == 'fr':
                welcome_text += " Je peux vous aider avec une large gamme de problèmes IT. Comment puis-je vous aider aujourd'hui?"
            else:
                welcome_text += " I can help you with a wide range of IT issues. What can I help you with today?"
        else:
            if language == 'en':
                welcome_text += " I'm in basic mode but can still help with common issues. How can I assist you?"
            elif language == 'es':
                welcome_text += " Estoy en modo básico pero aún puedo ayudar con problemas comunes. ¿Cómo puedo asistirte?"
            elif language == 'fr':
                welcome_text += " Je suis en mode de base mais je peux encore aider avec des problèmes courants. Comment puis-je vous aider?"
            else:
                welcome_text += " I'm in basic mode but can still help with common issues. How can I assist you?"
        
        return welcome_text

# Global language support instance
language_support = LanguageSupport()
