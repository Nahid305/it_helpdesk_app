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
    
    # Debug: Check what language was detected
    user_language = user_context.get('language', 'en') if user_context else 'en'
    print(f"DEBUG: Query='{query}', Language='{user_language}', Context={user_context}")
    
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
                print(f"DEBUG: Got AI response for language {user_language}")
                return response
        except Exception as e:
            # Fall back to basic NLP if AI fails
            print(f"AI service error: {e}")
    
    # Fallback to basic NLP matching
    print(f"DEBUG: Using basic NLP fallback for language {user_language}")
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
    if any(word in query_lower for word in ['password', 'login', 'forgot', 'reset', 'locked', 'contraseña', 'mot de passe', 'passwort', 'accesso', 'dimenticato', 'blocca', 'reimpostare', 'restablecer', 'olvidé', 'olvidado', 'bloqueado', 'iniciar sesión']):
        if language_support:
            if user_language == 'es':
                return f"""¡Hola {user_name}! ¡Definitivamente puedo ayudarte a restablecer tu contraseña. ¡Este es uno de los problemas más comunes que manejamos! 😊

**Paso 1:** Ve al portal de inicio de sesión de tu empresa en portal.company.com
**Paso 2:** Haz clic en el enlace 'Olvidé mi contraseña' debajo del formulario de inicio de sesión
**Paso 3:** Ingresa tu dirección de correo electrónico registrada o ID de empleado
**Paso 4:** Revisa tu correo electrónico para el enlace de restablecimiento (llega en 2-3 minutos)
**Paso 5:** Haz clic en el enlace de restablecimiento y crea una nueva contraseña segura
**Paso 6:** Inicia sesión con tu nueva contraseña y actualiza las contraseñas guardadas

¡Eso debería devolverle el acceso a tu cuenta! 🎉 Si no recibes el correo de restablecimiento en 5 minutos, revisa tu carpeta de spam primero."""
            elif user_language == 'it':
                return f"""Ciao {user_name}! Posso sicuramente aiutarti a reimpostare la tua password. Questo è uno dei problemi più comuni che gestiamo! 😊

**Passo 1:** Vai al portale di accesso della tua azienda su portal.company.com
**Passo 2:** Clicca sul link 'Password dimenticata' sotto il modulo di accesso
**Passo 3:** Inserisci il tuo indirizzo email registrato o ID dipendente
**Passo 4:** Controlla la tua email per il link di reimpostazione (arriva in 2-3 minuti)
**Passo 5:** Clicca sul link di reimpostazione e crea una nuova password sicura
**Passo 6:** Accedi con la tua nuova password e aggiorna le password salvate

Questo dovrebbe ripristinare l'accesso al tuo account! 🎉 Se non ricevi l'email di reimpostazione entro 5 minuti, controlla prima la cartella spam."""
            elif user_language == 'fr':
                return f"""Bonjour {user_name}! Je peux certainement vous aider à réinitialiser votre mot de passe. C'est l'un des problèmes les plus courants que nous traitons! 😊

**Étape 1:** Allez au portail de connexion de votre entreprise sur portal.company.com
**Étape 2:** Cliquez sur le lien 'Mot de passe oublié' sous le formulaire de connexion
**Étape 3:** Entrez votre adresse email enregistrée ou ID employé
**Étape 4:** Vérifiez votre email pour le lien de réinitialisation (arrive en 2-3 minutes)
**Étape 5:** Cliquez sur le lien de réinitialisation et créez un nouveau mot de passe sécurisé
**Étape 6:** Connectez-vous avec votre nouveau mot de passe et mettez à jour les mots de passe enregistrés

Cela devrait vous reconnecter à votre compte! 🎉 Si vous ne recevez pas l'email de réinitialisation dans les 5 minutes, vérifiez d'abord votre dossier spam."""
            else:
                return f"""Hi {user_name}! I can definitely help you reset your password. This is one of the most common issues we handle! 😊

**Step 1:** Go to your company login portal at portal.company.com
**Step 2:** Click the 'Forgot Password' link below the login form  
**Step 3:** Enter your registered email address or employee ID
**Step 4:** Check your email for the reset link (arrives in 2-3 minutes)
**Step 5:** Click the reset link and create a new secure password
**Step 6:** Log in with your new password and update saved passwords

That should get you back into your account! 🎉 If you don't receive the reset email within 5 minutes, check your spam folder first."""
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
    elif any(word in query_lower for word in ['vpn', 'remote', 'connection', 'work from home', 'installare', 'installa', 'connessione', 'accesso remoto', 'instalar', 'quiero', 'conexión', 'acceso remoto']):
        if language_support:
            if user_language == 'es':
                return f"""¡Hola {user_name}! ¡Te ayudaré a hacer funcionar el cliente VPN sin problemas! 🔒

**Paso 1:** Abre el centro de software de tu empresa o portal de descargas
**Paso 2:** Busca 'Cliente VPN Corporativo' o 'Cisco AnyConnect'
**Paso 3:** Haz clic en 'Instalar' y espera a que se complete la descarga
**Paso 4:** Ejecuta el instalador con privilegios de administrador (clic derecho > 'Ejecutar como administrador')
**Paso 5:** Inicia la aplicación VPN desde tu escritorio o menú de inicio
**Paso 6:** Ingresa la dirección del servidor: vpn.company.com
**Paso 7:** Inicia sesión con las credenciales de tu empresa
**Paso 8:** Haz clic en 'Conectar' y verifica el estado de conexión verde

¡Ahora deberías estar conectado de forma segura! 🌐 El icono de conexión aparecerá en tu bandeja del sistema."""
            elif user_language == 'it':
                return f"""Ciao {user_name}! Ti aiuterò a far funzionare il client VPN senza problemi! 🔒

**Passo 1:** Apri il centro software della tua azienda o portale download
**Passo 2:** Cerca 'Client VPN Aziendale' o 'Cisco AnyConnect'
**Passo 3:** Clicca su 'Installa' e aspetta il completamento del download
**Passo 4:** Esegui l'installer con privilegi di amministratore (tasto destro > 'Esegui come amministratore')
**Passo 5:** Avvia l'app VPN dal desktop o dal menu start
**Passo 6:** Inserisci l'indirizzo del server: vpn.company.com
**Passo 7:** Accedi con le credenziali della tua azienda
**Passo 8:** Clicca su 'Connetti' e verifica lo stato di connessione verde

Ora dovresti essere connesso in modo sicuro! 🌐 L'icona di connessione apparirà nella barra delle applicazioni."""
            elif user_language == 'fr':
                return f"""Bonjour {user_name}! Je vais vous aider à faire fonctionner le client VPN en douceur! 🔒

**Étape 1:** Ouvrez le centre logiciel de votre entreprise ou le portail de téléchargement
**Étape 2:** Recherchez 'Client VPN d'entreprise' ou 'Cisco AnyConnect'
**Étape 3:** Cliquez sur 'Installer' et attendez la fin du téléchargement
**Étape 4:** Exécutez l'installateur avec des privilèges d'administrateur (clic droit > 'Exécuter en tant qu'administrateur')
**Étape 5:** Lancez l'application VPN depuis votre bureau ou menu démarrer
**Étape 6:** Entrez l'adresse du serveur: vpn.company.com
**Étape 7:** Connectez-vous avec vos identifiants d'entreprise
**Étape 8:** Cliquez sur 'Connecter' et vérifiez l'état de connexion vert

Vous devriez maintenant être connecté en toute sécurité! 🌐 L'icône de connexion apparaîtra dans votre barre système."""
            else:
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
        else:
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
        
        # General help for unrecognized queries with language support
        if language_support and user_language == 'es':
            return f"""¡Hola {user_name}! ¡Estoy aquí para ayudarte con tu problema de TI! 🤔

Me gustaría saber más sobre lo que está pasando para poder ayudarte mejor:

• ¿Qué estabas tratando de hacer cuando comenzó el problema?
• ¿Estás viendo algún mensaje de error específico?
• ¿Cuándo notaste este problema por primera vez?
• ¿Ha cambiado algo recientemente en tu computadora?

**Soluciones universales rápidas que a menudo funcionan:**
• Reiniciar tu dispositivo
• Verificar todas las conexiones de cables
• Actualizar tu software/controladores
• Limpiar caché del navegador (para problemas web)

¡No te preocupes - resolveremos esto juntos! Si necesitas ayuda inmediata, también puedo ayudarte a crear un ticket de soporte para nuestro equipo técnico. 🎫"""
        elif language_support and user_language == 'it':
            return f"""Ciao {user_name}! Sono qui per aiutarti con il tuo problema IT! 🤔

Mi piacerebbe saperne di più su quello che sta succedendo per poterti aiutare meglio:

• Cosa stavi cercando di fare quando è iniziato il problema?
• Stai vedendo messaggi di errore specifici?
• Quando hai notato questo problema per la prima volta?
• È cambiato qualcosa di recente sul tuo computer?

**Soluzioni universali rapide che spesso funzionano:**
• Riavviare il dispositivo
• Controllare tutte le connessioni dei cavi
• Aggiornare software/driver
• Pulire cache del browser (per problemi web)

Non preoccuparti - risolveremo questo insieme! Se hai bisogno di aiuto immediato, posso anche aiutarti a creare un ticket di supporto per il nostro team tecnico. 🎫"""
        elif language_support and user_language == 'fr':
            return f"""Bonjour {user_name}! Je suis là pour vous aider avec votre problème informatique! 🤔

J'aimerais en savoir plus sur ce qui se passe pour mieux vous aider:

• Que faisiez-vous quand le problème a commencé?
• Voyez-vous des messages d'erreur spécifiques?
• Quand avez-vous remarqué ce problème pour la première fois?
• Quelque chose a-t-il changé récemment sur votre ordinateur?

**Solutions universelles rapides qui fonctionnent souvent:**
• Redémarrer votre appareil
• Vérifier toutes les connexions de câbles
• Mettre à jour logiciels/pilotes
• Vider le cache du navigateur (pour problèmes web)

Ne vous inquiétez pas - nous allons résoudre cela ensemble! Si vous avez besoin d'aide immédiate, je peux aussi vous aider à créer un ticket de support pour notre équipe technique. 🎫"""
        else:
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
