import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, request

from clinic_scope import OUT_OF_SCOPE_RESPONSE, is_within_scope
from gemini_client import ask_gemini

load_dotenv(Path(__file__).with_name(".env"))
app = Flask(__name__)

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v25.0")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def send_message(phone_number: str, text: str) -> None:
    response = requests.post(
        f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PHONE_NUMBER_ID}/messages",
        headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"},
        json={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {"body": text[:4096]},
        },
        timeout=30,
    )
    print("Sent:", response.status_code, response.text)
    response.raise_for_status()


def generate_response(text: str) -> str:
    message = text.strip()
    normalized_text = message.lower()

    if normalized_text in {"hi", "hello", "good morning", "good afternoon", "good evening", "menu"}:
        return (
            "Hello! I am the virtual assistant.\n\n"
            "Choose an option:\n"
            "1 - Business hours\n"
            "2 - Services\n"
            "3 - Speak with a staff member\n\n"
            "You can also write your question."
        )
    if normalized_text == "1":
        return "Our business hours are Monday to Friday, from 8 AM to 5 PM."
    if normalized_text == "2":
        return "Please tell me which service you are looking for so I can help."
    if normalized_text == "3":
        return "Sure. Your request will be forwarded to a staff member."
    if not is_within_scope(message):
        return OUT_OF_SCOPE_RESPONSE
    return ask_gemini(message)


@app.get("/webhook")
def verify_webhook():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        print("Webhook verified by Meta.")
        return request.args.get("hub.challenge"), 200
    return "Verification failed", 403


@app.post("/webhook")
def receive_webhook():
    payload = request.get_json(silent=True) or {}
    print("Event received:", payload)

    try:
        value = payload["entry"][0]["changes"][0]["value"]
        for status in value.get("statuses", []):
            print("Status:", status.get("status"), status.get("id"), status.get("errors", ""))

        for message in value.get("messages", []):
            phone_number, message_type = message.get("from"), message.get("type")
            response = generate_response(message["text"]["body"]) if message_type == "text" else (
                "For now, I can only reply to text messages."
            )
            send_message(phone_number, response)
    except (KeyError, IndexError, TypeError) as error:
        print("Event without a processable message:", error)
    except requests.RequestException as error:
        print("Error replying through the WhatsApp API:", error)

    return "OK", 200


@app.get("/")
def home():
    return "WhatsApp bot with Gemini is running.", 200


if __name__ == "__main__":
    if not all([WHATSAPP_TOKEN, PHONE_NUMBER_ID, VERIFY_TOKEN, GEMINI_API_KEY]):
        raise RuntimeError("Check the .env variables, including GEMINI_API_KEY.")
    app.run(host="0.0.0.0", port=5000, debug=True)
