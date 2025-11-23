# app.py
import json
from pathlib import Path

import streamlit as st

from backend.email_processor import (
    load_emails,
    load_prompts,
    save_prompts,
    ingest_and_process,
    load_processed_emails,
)
from backend.draft_agent import generate_reply_draft, load_drafts
from backend.email_agent_logic import run_email_agent_query, run_inbox_query

DATA_DIR = Path(__file__).resolve().parent / "data"

st.set_page_config(page_title="Email Productivity Agent", layout="wide")

st.title("📧 Prompt-Driven Email Productivity Agent")

tabs = st.tabs(["🧠 Prompt Brain", "📥 Inbox", "🤖 Email Agent & Drafts"])


# ---------- TAB 1: Prompt Brain ----------
with tabs[0]:
    st.subheader("Agent Brain: Configure Prompts")

    prompts = load_prompts()

    cat = st.text_area("Categorization Prompt", prompts.get("categorization_prompt", ""), height=150)
    act = st.text_area("Action Item Prompt", prompts.get("action_item_prompt", ""), height=150)
    auto = st.text_area("Auto-Reply Draft Prompt", prompts.get("auto_reply_prompt", ""), height=150)

    if st.button("Save Prompts"):
        prompts["categorization_prompt"] = cat
        prompts["action_item_prompt"] = act
        prompts["auto_reply_prompt"] = auto
        save_prompts(prompts)
        st.success("Prompts saved successfully!")


# ---------- TAB 2: Inbox ----------
with tabs[1]:
    st.subheader("Inbox")

    if st.button("Load & Process Inbox"):
        processed = ingest_and_process()
        st.success("Inbox processed using current prompts.")
        with st.expander("Raw processed JSON"):
            st.json(processed)

    emails = load_emails()
    processed_list = load_processed_emails()
    processed_map = {p["id"]: p for p in processed_list}

    st.write("### Emails")

    for e in emails:
        p = processed_map.get(e["id"], {})
        header = f"{e['subject']} — {e['sender']}"
        with st.expander(header):
            st.write(f"**From:** {e['sender']}")
            st.write(f"**Subject:** {e['subject']}")
            st.write(f"**Timestamp:** {e.get('timestamp', 'N/A')}")
            st.write("**Body:**")
            st.write(e["body"])

            st.write("---")
            st.write(f"**Category:** {p.get('category', 'Not processed')}")
            st.write("**Actions:**")
            st.json(p.get("actions", []))
            st.write("**Summary:**")
            st.write(p.get("summary", ""))

    st.write("---")
    st.write("### Ask the Agent About the Whole Inbox")
    inbox_query = st.text_input("Ask something like: 'Show me all urgent emails' or 'List To-Do items'")
    if st.button("Ask Inbox Agent"):
        if inbox_query.strip():
            answer = run_inbox_query(inbox_query.strip())
            st.write("**Agent Response:**")
            st.write(answer)
        else:
            st.warning("Please enter a question.")


# ---------- TAB 3: Email Agent & Drafts ----------
with tabs[2]:
    st.subheader("Email Agent & Drafts")

    emails = load_emails()
    if not emails:
        st.warning("No emails found. Please add some to mock_inbox.json.")
    else:
        email_options = {f"{e['subject']} ({e['sender']})": e["id"] for e in emails}
        selected_label = st.selectbox("Select an email", list(email_options.keys()))
        selected_id = email_options[selected_label]
        selected_email = next(e for e in emails if e["id"] == selected_id)

        st.write("### Selected Email")
        st.write(f"**From:** {selected_email['sender']}")
        st.write(f"**Subject:** {selected_email['subject']}")
        st.write("**Body:**")
        st.write(selected_email["body"])

        st.write("---")
        st.write("### Ask the Email Agent About This Email")
        user_query = st.text_input("e.g. 'Summarize this', 'What tasks do I need to do?', 'Draft a reply based on my tone'")
        if st.button("Ask Email Agent"):
            if user_query.strip():
                answer = run_email_agent_query(selected_email, user_query.strip())
                st.write("**Agent Response:**")
                st.write(answer)
            else:
                st.warning("Please enter a question for the agent.")

        st.write("---")
        st.write("### Generate Reply Draft")
        tone = st.text_input("Desired tone (optional)", "friendly and professional")
        if st.button("Generate Draft"):
            draft = generate_reply_draft(selected_id, user_tone=tone)
            if draft:
                st.success("Draft generated and saved (not sent).")
                st.write(f"**Draft ID:** {draft['draft_id']}")
                st.write(f"**Subject:** {draft['subject']}")
                st.text_area("Body", draft["body"], height=200)
            else:
                st.error("Could not generate draft.")

    st.write("---")
    st.write("### Saved Drafts")
    drafts = load_drafts()
    if not drafts:
        st.info("No drafts saved yet.")
    else:
        for d in drafts:
            with st.expander(f"{d['subject']} (for email {d['email_id']})"):
                st.text_area("Body", d["body"], height=200, key=f"draft_body_{d['draft_id']}")
                st.write("Metadata:")
                st.json(d.get("metadata", {}))
