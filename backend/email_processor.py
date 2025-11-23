# backend/email_processor.py
import json
from typing import List, Dict, Any

from .storage import load_json, save_json
from .llm_client import call_llm

def load_emails() -> List[Dict[str, Any]]:
    return load_json("mock_inbox.json", default=[])

def load_prompts() -> Dict[str, str]:
    return load_json("prompts.json", default={
        "categorization_prompt": "",
        "action_item_prompt": "",
        "auto_reply_prompt": ""
    })

def save_prompts(prompts: Dict[str, str]):
    save_json("prompts.json", prompts)

def load_processed_emails() -> List[Dict[str, Any]]:
    return load_json("processed_emails.json", default=[])

def save_processed_emails(processed: List[Dict[str, Any]]):
    save_json("processed_emails.json", processed)


def categorize_email(email: Dict[str, Any], categorization_prompt: str) -> str:
    system_prompt = "You are an email classification assistant. Reply with only the label name."
    user_message = (
        f"{categorization_prompt}\n\n"
        f"Email:\n"
        f"From: {email.get('sender')}\n"
        f"Subject: {email.get('subject')}\n"
        f"Body:\n{email.get('body')}"
    )
    result = call_llm(system_prompt, user_message)
    return result.strip()


def extract_actions(email: Dict[str, Any], action_prompt: str):
    system_prompt = "You are an assistant that extracts tasks from emails and returns valid JSON."
    user_message = (
        f"{action_prompt}\n\n"
        f"Email:\n"
        f"Subject: {email.get('subject')}\n"
        f"Body:\n{email.get('body')}"
    )
    raw = call_llm(system_prompt, user_message)
    try:
        actions = json.loads(raw)
        if isinstance(actions, dict):
            actions = [actions]
    except Exception:
        actions = []
    return actions


def summarize_email(email: Dict[str, Any]) -> str:
    system_prompt = "You are an assistant that summarizes emails in 1–2 concise sentences."
    user_message = (
        f"Summarize this email:\n\n"
        f"From: {email.get('sender')}\n"
        f"Subject: {email.get('subject')}\n"
        f"Body:\n{email.get('body')}"
    )
    return call_llm(system_prompt, user_message).strip()


def ingest_and_process():
    """
    Main ingestion pipeline:
    1. Load emails
    2. Load prompts
    3. Run categorization + action extraction + summary
    4. Save processed results
    """
    emails = load_emails()
    prompts = load_prompts()
    processed = []

    for e in emails:
        category = categorize_email(e, prompts["categorization_prompt"])
        actions = extract_actions(e, prompts["action_item_prompt"])
        summary = summarize_email(e)

        processed.append({
            "id": e["id"],
            "category": category,
            "actions": actions,
            "summary": summary
        })

    save_processed_emails(processed)
    return processed
