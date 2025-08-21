# IT Helpdesk Application

A Streamlit-based IT helpdesk application with AI-powered query assistance and ticket management.

## Features

- 🔐 **Authentication System**: Secure user login with session management
- 🤖 **AI-Powered Chat**: Interactive IT support with intelligent responses
- 🎫 **Ticket Management**: Create and manage support tickets
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd it_helpdesk_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Fork this repository
2. Connect your GitHub account to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and select this repository
4. Set up your secrets in the Streamlit Cloud dashboard:
   - Add your environment variables from `.env.example`
5. Deploy!

## Configuration

Create a `.env` file based on `.env.example` and configure:

- `GROK_API_KEY`: Your Grok AI API key (optional)
- Other environment-specific settings

## Project Structure

```
├── app.py              # Main application entry point
├── pages/              # Streamlit pages
│   ├── 1_Login.py     # Authentication page
│   ├── 2_Query.py     # AI chat interface
│   └── 3_Ticket.py    # Ticket management
├── utils/              # Core utilities
│   ├── auth.py        # Authentication logic
│   ├── grok_ai.py     # AI integration
│   ├── simple_steps.py # Query matching
│   └── tickets.py     # Ticket functions
├── data/               # Application data
├── assets/             # Static assets
└── .streamlit/         # Streamlit configuration
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.