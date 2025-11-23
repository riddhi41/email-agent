# backend/draft_agent.py
import json
from typing import Any, Dict, List, Optional

from .storage import load_json, save_json
from .llm_client import call_llm
from .email_processor import load_emails, load_prompts

def load_drafts() -> List[Dict[str, Any]]:
    return load_json("drafts.json", default=[])

def save_drafts(drafts: List[Dict[str, Any]]):
    save_json("drafts.json", drafts)

def get_email_by_id(email_id: str) -> Optional[Dict[str, Any]]:
    emails = load_emails()
    for e in emails:
        if e.get("id") == email_id:
            return e
    return None

def generate_reply_draft(email_id: str, user_tone: str = "friendly and professional") -> Optional[Dict[str, Any]]:
    email = get_email_by_id(email_id)
    if not email:
        return None

    prompts = load_prompts()
    auto_reply_prompt = prompts["auto_reply_prompt"]

    system_prompt = (
        "You are an assistant that writes email drafts. "
        "Never send emails; only draft them. Always return valid JSON."
    )
    user_message = (
        f"{auto_reply_prompt}\n\n"
        f"Use this tone: {user_tone}\n\n"
        f"Original email:\n"
        f"From: {email['sender']}\n"
        f"Subject: {email['subject']}\n"
        f"Body:\n{email['body']}\n\n"
        "Return JSON with keys: subject (string), body (string), "
        "suggested_follow_ups (array of strings)."
    )

    raw = call_llm(system_prompt, user_message)

    try:
        draft_data = json.loads(raw)
    except Exception:
        draft_data = {
            "subject": f"Re: {email['subject']}",
            "body": raw,
            "suggested_follow_ups": []
        }

    drafts = load_drafts()
    draft_id = f"draft_{len(drafts) + 1}"

    draft = {
        "draft_id": draft_id,
        "email_id": email_id,
        "subject": draft_data.get("subject", f"Re: {email['subject']}"),
        "body": draft_data.get("body", raw),
        "metadata": {
            "suggested_follow_ups": draft_data.get("suggested_follow_ups", [])
        }
    }

    drafts.append(draft)
    save_drafts(drafts)
    return draft
