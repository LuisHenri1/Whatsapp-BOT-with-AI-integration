# WhatsApp Dental Clinic Assistant

A Flask-based WhatsApp webhook bot designed to run as a 24/7 PythonAnywhere Web App. It uses Google Gemini to answer patient questions for a dental clinic and is restricted to clinic-related topics such as appointments, business hours, location, dental services, visit preparation, service channels, and administrative questions.

## Features

- WhatsApp Cloud API webhook verification and message handling
- Gemini-powered responses for dental clinic support
- Scope filtering before calling the AI model
- Short WhatsApp-friendly replies in Brazilian Portuguese
- Basic menu options for common requests
- Safe fallback responses for unsupported message types and AI errors
- PythonAnywhere-first deployment as a continuously available web app

## Project Structure

```text
.
|-- app.py              # Flask app, WhatsApp webhook routes, and response flow
|-- escopo_clinica.py   # Allowed clinic topics and out-of-scope response
|-- gemini_client.py    # Gemini client setup and dental assistant instructions
|-- .env                # Local environment variables, not meant for GitHub
`-- README.md
```

## Requirements

- Python 3.10+
- A Meta WhatsApp Cloud API app
- A Google Gemini API key
- A PythonAnywhere account with a configured Web App

Python packages:

```bash
pip install flask requests python-dotenv google-genai
```

## Environment Variables

Create a `.env` file in the project root:

```env
WHATSAPP_TOKEN=your_meta_whatsapp_access_token
PHONE_NUMBER_ID=your_whatsapp_phone_number_id
VERIFY_TOKEN=your_custom_webhook_verify_token
GRAPH_API_VERSION=v25.0
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash-lite
```

Do not commit `.env` to GitHub.

## PythonAnywhere-Only Implementation

This project is intended to run exclusively on PythonAnywhere as a Flask Web App. PythonAnywhere serves the WSGI application continuously, so there is no need to keep a terminal open or run the Flask development server manually.

### 1. Upload the Project

Upload the project files to a folder such as:

```text
/home/your_user/whatsapp-bot
```

The folder should contain:

```text
app.py
escopo_clinica.py
gemini_client.py
.env
README.md
```

### 2. Create the Virtual Environment

Open a PythonAnywhere Bash console:

```bash
cd /home/your_user/whatsapp-bot
python3.10 -m venv venv
source venv/bin/activate
pip install flask requests python-dotenv google-genai
```

### 3. Configure the Web App

In the PythonAnywhere **Web** tab:

- Create a new manual configuration Web App.
- Select the same Python version used by the virtual environment.
- Set the virtualenv path:

```text
/home/your_user/whatsapp-bot/venv
```

Edit the WSGI configuration file and point it to the Flask app:

```python
import sys

project_home = "/home/your_user/whatsapp-bot"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
```

Save the WSGI file and click **Reload**.

### 4. Configure the Meta Webhook

In the Meta Developer dashboard, use the PythonAnywhere public URL as the WhatsApp webhook callback:

```text
https://your_user.pythonanywhere.com/webhook
```

Use the same verification token configured in `.env`:

```env
VERIFY_TOKEN=your_custom_webhook_verify_token
```

After verification, subscribe the webhook to WhatsApp message events.

### 5. 24/7 Operation

Once the Web App is reloaded, PythonAnywhere keeps the Flask application available online. Incoming WhatsApp messages are delivered by Meta to `/webhook`, processed by the bot, optionally answered by Gemini, and returned through the Meta Graph API.

After changing code or environment variables, reload the app in the PythonAnywhere **Web** tab. Use the PythonAnywhere error and server logs to debug import errors, missing API keys, webhook payload issues, or API failures.

## Webhook Endpoints

### `GET /webhook`

Used by Meta to verify the webhook. It checks:

- `hub.mode`
- `hub.verify_token`
- `hub.challenge`

### `POST /webhook`

Receives WhatsApp events, processes text messages, generates a response, and sends it back through the WhatsApp Cloud API.

### `GET /`

Basic health response for confirming that the app is running.

## AI Scope Control

The assistant only answers questions related to:

- Dental appointments
- Scheduling
- Business hours
- Clinic address and location
- Dental services
- Preparation for appointments
- Service channels
- Clinic administrative questions

Out-of-scope messages are blocked before Gemini is called and receive a fixed response from `escopo_clinica.py`.

Gemini also receives a system instruction in `gemini_client.py` that reinforces the same boundaries and avoids unsafe behavior such as definitive diagnoses or medication prescriptions.

## Security Notes

- Never commit `.env`, API keys, tokens, or patient data.
- This project does not persist messages to a database by default.
- The bot should not provide definitive medical diagnoses or prescribe medication.
- Sensitive cases and urgent situations should be escalated to a qualified professional.

## Customization

- Update allowed keywords in `escopo_clinica.py`.
- Update the Gemini system instruction in `gemini_client.py`.
- Adjust fixed menu responses in `gerar_resposta()` inside `app.py`.
- Change `GEMINI_MODEL` in `.env` to use another supported Gemini model.

## License

Add your preferred license before publishing the repository.
