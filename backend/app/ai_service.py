import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

def _client_context(client, notes) -> str:
    note_text = "\n".join(f"- {note.content}" for note in notes) or "No notes yet."
    return (
        f"Client: {client.name}\n"
        f"Company: {client.company}\n"
        f"Email: {client.email}\n"
        f"Status: {client.status}\n"
        f"Priority: {client.priority}\n"
        f"Last contact: {client.last_contact_date}\n"
        f"Notes:\n{note_text}"
    )

def generate_summary(client, notes) -> str:
    context = _client_context(client, notes)
    prompt = f"Summarize this CRM client history in 3 concise bullets and suggest one next action:\n\n{context}"
    return _call_ai(prompt, fallback=f"Summary for {client.name}: status is {client.status}, priority is {client.priority}. Review recent notes and plan the next follow-up based on the client's latest needs.")

def generate_follow_up(client, notes) -> str:
    context = _client_context(client, notes)
    prompt = f"Write a friendly professional follow-up email for this CRM client:\n\n{context}"
    fallback = (
        f"Hi {client.name},\n\n"
        "I hope you are doing well. I wanted to follow up on our previous conversation and check whether there are any updates or questions from your side. "
        "I would be happy to help with the next steps.\n\n"
        "Best regards"
    )
    return _call_ai(prompt, fallback=fallback)

def _call_ai(prompt: str, fallback: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return fallback + "\n\n[Local fallback used: add OPENAI_API_KEY to enable live AI responses.]"

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful CRM assistant. Keep responses practical and concise."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content or fallback
