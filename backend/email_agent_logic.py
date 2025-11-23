# backend/email_agent_logic.py
from typing import Dict, Any, List

from .llm_client import call_llm
from .email_processor import load_prompts, load_processed_emails, load_emails

def run_email_agent_query(email: Dict[str, Any], user_query: str) -> str:
    """
    Handles user queries about a single email:
    - Summaries
    - Tasks
    - Tone-based replies
    """
    prompts = load_prompts()

    system_prompt = (
        "You are an Email Productivity Agent. You help the user with email summaries, "
        "action items, and reply suggestions. Be concise but clear."
    )

    user_message = (
        f"User query: {user_query}\n\n"
        f"Selected email:\n"
        f"From: {email.get('sender')}\n"
        f"Subject: {email.get('subject')}\n"
        f"Body:\n{email.get('body')}\n\n"
        "Here are the agent prompts you must respect:\n\n"
        f"Categorization prompt:\n{prompts['categorization_prompt']}\n\n"
        f"Action item prompt:\n{prompts['action_item_prompt']}\n\n"
        f"Auto-reply prompt:\n{prompts['auto_reply_prompt']}\n\n"
        "Use these prompts to guide how you interpret the email and respond to the query."
    )

    return call_llm(system_prompt, user_message)


def run_inbox_query(user_query: str) -> str:
    """
    For queries across the inbox, e.g.:
    - 'Show me all urgent emails'
    - 'List To-Do emails'
    """
    emails = load_emails()
    processed = load_processed_emails()

    # Merge basic info
    id_to_processed = {p["id"]: p for p in processed}
    inbox_view = []
    for e in emails:
        pid = id_to_processed.get(e["id"], {})
        inbox_view.append({
            "id": e["id"],
            "sender": e.get("sender"),
            "subject": e.get("subject"),
            "body": e.get("body"),
            "category": pid.get("category", "Unknown"),
            "actions": pid.get("actions", []),
            "summary": pid.get("summary", "")
        })

    system_prompt = (
        "You are an Email Productivity Agent answering questions about the entire inbox. "
        "When listing emails, return a human-readable explanation including subject and category."
    )

    user_message = (
        f"User query: {user_query}\n\n"
        f"Inbox data (JSON array):\n{inbox_view}\n\n"
        "Use categories and summaries to decide what is urgent or important."
    )

    return call_llm(system_prompt, user_message)
