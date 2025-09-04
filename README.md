# IT Helpdesk Application

A modern, AI-powered IT helpdesk application built with Streamlit. Features WhatsApp-style chat interface, multilingual support, and intelligent ticket management.

## 🚀 Live Demo

[View Live Application](https://your-app-name.streamlit.app) *(Update with your actual URL after deployment)*

## ✨ Features

- 🔐 **Secure Authentication**: Session-based login system
- 🤖 **AI-Powered Support**: Intelligent responses using Grok AI
- 💬 **WhatsApp-Style Chat**: Modern, intuitive chat interface
- 🌍 **Multilingual Support**: 13+ languages with auto-detection
- 🎫 **Smart Ticketing**: Create and manage support tickets
- 📱 **Responsive Design**: Works seamlessly on all devices
- 📎 **File Attachments**: Support for various file formats
- 🎨 **Professional UI**: Clean, modern KIITOS branding

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python 3.8+
- **AI Integration**: Grok AI API
- **Authentication**: JWT-based sessions
- **Storage**: JSON-based data persistence
- **Deployment**: Streamlit Cloud ready

## 📦 Quick Start

### Local Development

1. **Clone the repository**:
```bash
git clone https://github.com/YOUR_USERNAME/it-helpdesk-app.git
cd it-helpdesk-app
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration (optional)
```

4. **Run the application**:
```bash
streamlit run app.py
```

5. **Access the app**: Open [http://localhost:8501](http://localhost:8501)

### 🌐 Deploy to Streamlit Cloud

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud)

1. **Fork this repository** to your GitHub account
2. **Connect to Streamlit Cloud**: Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. **Create new app** and select your forked repository
4. **Configure secrets** (optional for AI features):
   ```toml
   GROK_API_KEY = "your_api_key_here"
   GROK_API_URL = "https://api.x.ai/v1"
   GROK_MODEL = "grok-beta"
   ```
5. **Deploy**: Your app will be live at `https://your-app-name.streamlit.app`

For detailed deployment instructions, see [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md).

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROK_API_KEY` | Grok AI API key for AI responses | No | None |
| `GROK_API_URL` | Grok AI API endpoint | No | `https://api.x.ai/v1` |
| `GROK_MODEL` | AI model to use | No | `grok-beta` |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | No | Auto-generated |

### Features Without API Key

The application works fully without an API key:
- ✅ Authentication and login
- ✅ Basic IT support responses
- ✅ Ticket creation and management
- ✅ File uploads and attachments
- ✅ Multilingual interface
- ❌ AI-powered responses (falls back to predefined responses)

## 📁 Project Structure

```
it_helpdesk_app/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── DEPLOYMENT_CHECKLIST.md # Deployment guide
├── LICENSE              # MIT License
│
├── .streamlit/          # Streamlit configuration
│   ├── config.toml     # App configuration
│   └── secrets_template.toml # Secrets template
│
├── pages/               # Streamlit pages
│   ├── 1_Login.py      # Authentication page
│   ├── 2_Query.py      # AI chat interface
│   └── 3_Ticket.py     # Ticket management
│
├── utils/               # Core utilities
│   ├── __init__.py     # Package initialization
│   ├── auth.py         # Authentication logic
│   ├── grok_ai.py      # AI integration
│   ├── language_support.py # Multilingual support
│   ├── simple_steps.py # Query matching
│   └── tickets.py      # Ticket management
│
├── data/                # Application data
│   ├── dummy_steps.json # Sample troubleshooting steps
│   ├── tickets.json    # Ticket storage
│   └── users.json      # User data
│
└── assets/              # Static assets
    └── style.css       # Additional styling
```

## 🎯 Usage

### For End Users

1. **Login**: Use any username to access the system
2. **Get Help**: Ask questions in natural language
3. **Create Tickets**: Escalate issues that need human attention
4. **Attach Files**: Upload screenshots or documents
5. **Track Progress**: View ticket status and responses

### For Administrators

- **User Management**: Configure users in `data/users.json`
- **Knowledge Base**: Update responses in `data/dummy_steps.json`
- **Monitor Tickets**: Review tickets in `data/tickets.json`
- **Customize Branding**: Modify UI elements and colors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a Pull Request

## 🐛 Troubleshooting

### Common Issues

**App won't start locally:**
- Check Python version (3.8+ required)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Ensure no port conflicts on 8501

**AI responses not working:**
- Verify `GROK_API_KEY` is set correctly
- Check API quota and billing status
- App will fall back to predefined responses

**Streamlit Cloud deployment fails:**
- Check `requirements.txt` for typos
- Verify main file path is `app.py`
- Review deployment logs for specific errors

**Login issues:**
- Clear browser cache and cookies
- Check if JavaScript is enabled
- Try different browser or incognito mode

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) framework
- AI powered by [Grok AI](https://x.ai/)
- Icons and design inspired by modern chat applications
- Community feedback and contributions

## 📞 Support

- 📧 **Email**: Create an issue on GitHub
- 💬 **Chat**: Use the app's built-in support system
- 📖 **Documentation**: Check deployment and troubleshooting guides
- 🐛 **Bug Reports**: Open an issue with detailed description

---

**Made with ❤️ for better IT support experiences**