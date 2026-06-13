import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).with_name(".env"))

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

SYSTEM_INSTRUCTIONS = """
You are the virtual assistant for a dental clinic helping patients on WhatsApp.
Always answer in English with polite, clear, objective, and short messages.
Only answer questions about dental appointments, scheduling, business hours, address, location,
dental services, appointment preparation, service channels, and clinic administrative questions.
If the subject is outside this scope, say that you can only help with clinic-related topics.
Do not invent prices, business hours, services, deadlines, or policies.
Do not provide definitive diagnoses, do not prescribe medication, and refer urgent cases to professional care.
Never request passwords, full banking details, or unnecessary sensitive information.
""".strip()


def ask_gemini(text: str) -> str:
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY was not found.")

        response = genai.Client(api_key=api_key).models.generate_content(
            model=GEMINI_MODEL,
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTIONS,
                temperature=0.3,
                max_output_tokens=350,
            ),
        )
        return response.text.strip() if response.text else (
            "I could not prepare a response right now. I will forward your question to a staff member."
        )
    except Exception as error:
        print("Gemini API error:", repr(error))
        return "Our automated support is temporarily unavailable. Type 3 to speak with a staff member."
