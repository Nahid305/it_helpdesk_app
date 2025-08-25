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
            'it': {
                'welcome': "Ciao! Sono il tuo assistente IT helpdesk alimentato dall'IA. Come posso aiutarti oggi?",
                'ask_question': "Fai la tua domanda IT:",
                'send': "Invia",
                'helpful': "Utile",
                'not_helpful': "Non Utile",
                'create_ticket': "Crea Ticket",
                'new_chat': "Nuova Chat",
                'end_chat': "Termina Chat",
                'clear_chat': "Cancella Chat",
                'thank_you': "Grazie per aver utilizzato il nostro supporto IT! 😊",
                'new_session': "Avvio di una nuova sessione di chat per te...",
                'ticket_question': "Vorresti creare un ticket perché un umano ti assista?",
                'no_thanks': "No, grazie",
                'start_new_chat': "Inizia Nuova Chat",
                'login_required': "Devi effettuare il login per utilizzare l'assistente chat.",
                'basic_mode': "⚡ **Modalità Base**: Servizio IA non disponibile, utilizzo risposte basate su regole. Controlla la configurazione API nel file .env.",
                'enter_message': "Per favore inserisci un messaggio prima di inviare.",
                'starting_new_chat': "Avvio di una nuova sessione di chat per te...",
                'language_select': "Seleziona Lingua:",
                'password_reset': "Reset Password",
                'vpn_issues': "Problemi VPN",
                'email_problems': "Problemi Email",
                'printer_setup': "Configurazione Stampante",
                'network_issues': "Problemi di Rete",
                'software_help': "Aiuto Software"
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
            'en': ['how', 'to', 'reset', 'password', 'help', 'need', 'can', 'please', 'my', 'the', 'is', 'have', 'get', 'make', 'want', 'install', 'setup', 'problem', 'issue', 'error', 'cannot', 'unable', 'trying', 'work', 'don\'t', 'doesn\'t', 'won\'t', 'can\'t', 'shouldn\'t', 'wouldn\'t', 'understand', 'these', 'steps', 'more', 'some', 'any', 'all', 'every', 'each', 'this', 'that', 'those', 'what', 'when', 'where', 'why', 'who', 'which', 'how', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'might', 'must', 'shall', 'may', 'am', 'are', 'was', 'were', 'been', 'being', 'has', 'had', 'having', 'go', 'goes', 'went', 'going', 'come', 'comes', 'came', 'coming', 'see', 'sees', 'saw', 'seeing', 'know', 'knows', 'knew', 'knowing', 'think', 'thinks', 'thought', 'thinking', 'say', 'says', 'said', 'saying', 'tell', 'tells', 'told', 'telling', 'ask', 'asks', 'asked', 'asking', 'give', 'gives', 'gave', 'giving', 'take', 'takes', 'took', 'taking', 'find', 'finds', 'found', 'finding', 'use', 'uses', 'used', 'using', 'try', 'tries', 'tried', 'trying', 'work', 'works', 'worked', 'working'],
            'it': ['ciao', 'grazie', 'per favore', 'aiuto', 'problema', 'password', 'italiano', 'ho', 'bisogno', 'può', 'salve', 'buongiorno', 'voglio', 'installare', 'come', 'fare', 'dove', 'che', 'cosa', 'una', 'sono', 'questo', 'non', 'riesco', 'capire', 'questi', 'passaggi', 'devo', 'posso', 'mi', 'la', 'le', 'di', 'da', 'con', 'per', 'su', 'in', 'il', 'lo', 'gli', 'del', 'della', 'delle', 'dei', 'mio', 'mia', 'suoi', 'sua', 'loro', 'funziona', 'funzionare', 'errore', 'sbagliato', 'sbagliata', 'quando', 'ora', 'adesso', 'sempre', 'mai', 'oggi', 'ieri', 'domani', 'primo', 'prima', 'dopo', 'durante', 'mentre', 'perché', 'quindi', 'allora', 'però', 'però', 'anche', 'ancora', 'già', 'qui', 'qua', 'lì', 'là'],
            'es': ['hola', 'gracias', 'por favor', 'ayuda', 'problema', 'contraseña', 'español', 'tengo', 'necesito', 'puede', 'buenos días', 'quiero', 'instalar', 'vpn', 'un', 'como', 'hacer', 'donde', 'soy', 'esto', 'restablecer', 'olvidé', 'olvidado', 'password', 'iniciar', 'no', 'puedo', 'entender', 'estos', 'pasos', 'debo', 'mi', 'mis', 'tu', 'sus', 'el', 'la', 'los', 'las', 'del', 'de', 'con', 'por', 'para', 'en', 'es', 'está', 'son', 'han', 'he', 'has', 'hemos', 'cuando', 'que', 'qué', 'por qué', 'porque', 'entonces', 'pero', 'también', 'siempre', 'nunca', 'ahora', 'hoy', 'ayer', 'mañana', 'aquí', 'allí', 'muy', 'más', 'menos', 'bien', 'mal', 'funciona', 'error', 'problema', 'tiempo', 'vez', 'veces', 'buenas', 'tardes', 'noches', 'sí', 'claro', 'correo', 'email', 'conectar', 'conexión', 'servidor', 'configurar', 'instalación', 'usuario', 'cuenta', 'acceso', 'seguridad', 'red', 'internet', 'wifi', 'impresora', 'imprimir', 'software', 'programa', 'aplicación', 'ventana', 'pantalla', 'teclado', 'ratón', 'mouse', 'ordenador', 'computadora', 'equipo', 'dispositivo', 'móvil', 'celular', 'teléfono', 'tablet'],
            'fr': ['bonjour', 'merci', 's\'il vous plaît', 'aide', 'problème', 'mot de passe', 'français', 'j\'ai', 'besoin', 'pouvez', 'salut', 'je', 'ne', 'pas', 'ces', 'étapes', 'comprends', 'comprendre', 'vous', 'nous', 'ils', 'elles', 'le', 'la', 'les', 'du', 'des', 'un', 'une', 'avec', 'dans', 'sur', 'pour', 'par', 'et', 'ou', 'mais', 'donc', 'si', 'quand', 'comment', 'où', 'pourquoi', 'que', 'qui', 'dont', 'très', 'plus', 'moins', 'bien', 'mal', 'toujours', 'jamais', 'maintenant', 'aujourd\'hui', 'hier', 'demain', 'ici', 'là'],
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
        
        # Score each language based on keyword matches (using word boundaries)
        import re
        text_words = text_lower.split()
        language_scores = {}
        for lang, keywords in language_indicators.items():
            score = 0
            for keyword in keywords:
                # Use word boundary matching to avoid partial matches
                if ' ' in keyword:  # Multi-word phrases
                    if keyword in text_lower:
                        score += 1
                else:  # Single words - check if they appear as complete words
                    if keyword in text_words:
                        score += 1
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
            'es': "IMPORTANTE: Responde SIEMPRE en español. Eres un asistente de soporte técnico IT que debe proporcionar respuestas completas en español con pasos numerados y un tono profesional pero amigable.",
            'fr': "IMPORTANT: Répondez TOUJOURS en français. Vous êtes un assistant de support technique IT qui doit fournir des réponses complètes en français avec des étapes numérotées et un ton professionnel mais amical.",
            'de': "WICHTIG: Antworte IMMER auf Deutsch. Du bist ein IT-Support-Assistent, der vollständige Antworten auf Deutsch mit nummerierten Schritten und einem professionellen aber freundlichen Ton geben muss.",
            'zh': "重要提示：始终用中文回答。你是一个IT技术支持助手，必须用中文提供完整的回答，包含编号步骤和专业而友好的语调。",
            'ja': "重要：必ず日本語で答えてください。あなたはITサポートアシスタントで、番号付きの手順と専門的で親しみやすい口調で日本語で完全な回答を提供する必要があります。",
            'ar': "مهم: أجب دائماً باللغة العربية. أنت مساعد دعم تقني IT يجب أن يقدم إجابات كاملة باللغة العربية مع خطوات مرقمة ونبرة مهنية ولكن ودودة.",
            'ru': "ВАЖНО: Всегда отвечай на русском языке. Ты помощник IT-поддержки, который должен предоставлять полные ответы на русском языке с пронумерованными шагами и профессиональным, но дружелюбным тоном.",
            'hi': "महत्वपूर्ण: हमेशा हिंदी में जवाब दें। आप एक IT सपोर्ट असिस्टेंट हैं जिन्हें संख्या दिए गए चरणों और पेशेवर लेकिन मित्रवत स्वर के साथ हिंदी में पूरे उत्तर देने चाहिए।",
            'pt': "IMPORTANTE: Responda SEMPRE em português. Você é um assistente de suporte técnico IT que deve fornecer respostas completas em português com etapas numeradas e tom profissional mas amigável.",
            'it': "IMPORTANTE: Rispondi SEMPRE in italiano. Sei un assistente di supporto tecnico IT che deve fornire risposte complete in italiano con passaggi numerati e tono professionale ma amichevole.",
            'nl': "BELANGRIJK: Antwoord ALTIJD in het Nederlands. Je bent een IT-ondersteuningsassistent die volledige antwoorden in het Nederlands moet geven met genummerde stappen en een professionele maar vriendelijke toon.",
            'ko': "중요: 항상 한국어로 답하세요. 당신은 번호가 매겨진 단계와 전문적이지만 친근한 어조로 한국어로 완전한 답변을 제공해야 하는 IT 지원 도우미입니다."
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
                'check your spam folder': 'revisa tu carpeta de spam',
                'I\'ll help you get the VPN client working smoothly': 'Te ayudaré a hacer funcionar el cliente VPN sin problemas',
                'Open your company software center': 'Abre el centro de software de tu empresa',
                'or download portal': 'o portal de descargas',
                'Search for': 'Busca', 'Install': 'Instalar', 'and wait for download completion': 'y espera a que se complete la descarga',
                'Run installer with administrator privileges': 'Ejecuta el instalador con privilegios de administrador',
                'right-click': 'clic derecho', 'Run as administrator': 'Ejecutar como administrador',
                'Launch the VPN app': 'Inicia la aplicación VPN', 'from your desktop or start menu': 'desde tu escritorio o menú de inicio',
                'Enter server address': 'Ingresa la dirección del servidor', 'Log in with your company credentials': 'Inicia sesión con las credenciales de tu empresa',
                'Connect': 'Conectar', 'and check for green connection status': 'y verifica el estado de conexión verde',
                'You should now be securely connected': 'Ahora deberías estar conectado de forma segura',
                'The connection icon will appear in your system tray': 'El icono de conexión aparecerá en tu bandeja del sistema'
            },
            'fr': {
                'Hi': 'Salut', 'Hello': 'Bonjour', 'Step': 'Étape', 'Click': 'Cliquez',
                'Go to': 'Allez à', 'Enter': 'Entrez', 'Check': 'Vérifiez',
                'That should get you back': 'Cela devrait vous reconnecter',
                'If you don\'t receive': 'Si vous ne recevez pas', 'minutes': 'minutes',
                'check your spam folder': 'vérifiez votre dossier spam'
            },
            'it': {
                'Hi': 'Ciao', 'Hello': 'Ciao', 'Step': 'Passo', 'Click': 'Clicca',
                'Go to': 'Vai a', 'Enter': 'Inserisci', 'Check': 'Controlla',
                'That should get you back': 'Questo dovrebbe ripristinare il tuo accesso',
                'If you don\'t receive': 'Se non ricevi', 'minutes': 'minuti',
                'check your spam folder': 'controlla la cartella spam',
                'I\'ll help you get the VPN client working smoothly': 'Ti aiuterò a far funzionare il client VPN senza problemi',
                'Open your company software center': 'Apri il centro software della tua azienda',
                'Search for': 'Cerca', 'Install': 'Installa', 'wait for download completion': 'aspetta il completamento del download',
                'Run installer with administrator privileges': 'Esegui l\'installer con privilegi di amministratore',
                'Launch the VPN app': 'Avvia l\'app VPN', 'from your desktop or start menu': 'dal desktop o dal menu start',
                'Enter server address': 'Inserisci l\'indirizzo del server', 'Log in with your company credentials': 'Accedi con le credenziali della tua azienda',
                'Connect': 'Connetti', 'check for green connection status': 'verifica lo stato di connessione verde',
                'You should now be securely connected': 'Ora dovresti essere connesso in modo sicuro',
                'The connection icon will appear in your system tray': 'L\'icona di connessione apparirà nella barra delle applicazioni'
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
