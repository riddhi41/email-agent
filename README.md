# Prompt-Driven Email Productivity Agent

Powered by Groq (LLaMA 3.1 8B Instant) + Streamlit

This project is a fully functional AI Email Productivity Agent that:

1. Loads a mock inbox
2. Processes emails
3. Extracts action items
4. Categorizes emails
5. Summarizes emails
6. Generates reply drafts
7. Allows natural-language queries over the inbox
8. Provides custom prompts to shape agent behavior

It is built using Python, Streamlit, and Groq API.

**Features**
1. Prompt Brain (Fully Customizable Prompts)

-Categorization prompt
-Action item extraction prompt
-Auto-reply generation prompt
-All editable in the UI
-Saved in prompts.json

2. Email Ingestion + Processing

For each email, the agent automatically:

-Categorizes
-Extracts tasks
-Summarizes
-Stored in processed_emails.json.

3. Email Agent Chat

Ask things like:

“Summarize this email”
“What tasks do I need to do?”
“Draft a reply in a friendly tone”
“Does this email need urgent action?”

4. Inbox-Level Agent Chat

Ask across all emails:
“Show me all urgent emails”
“List all To-Do items”
“Summaries of important emails”

5. Auto-Reply Draft Generator

Generates subject + body
Suggests follow-up actions
Saves drafts in drafts.json

**Folder Structure**
email-agent/
│── app.py
│── README.md
│── .gitignore
│── .env.example
│── requirements.txt
│
├── backend/
│   ├── email_agent_logic.py
│   ├── email_processor.py
│   ├── draft_agent.py
│   ├── llm_client.py
│   ├── storage.py
│
├── data/
│   ├── mock_inbox.json
│   ├── prompts.json
│   ├── drafts.json
│   ├── processed_emails.json


**Installation & Setup**
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/email-agent.git
cd email-agent

2. Create Virtual Environment
python -m venv .venv


Activate it:

Windows:
.\.venv\Scripts\activate

Mac/Linux:
source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

**Setup API Key (Groq)**

1. Create a Groq account: https://console.groq.com

2. Go to API Keys → Create API Key

3. Copy your key

4. Create .env file (NOT committed to GitHub)

Inside .env:

GROQ_API_KEY=your_actual_key_here


**Mock Inbox**

You can edit the mock inbox here:
data/mock_inbox.json


Contains ~15 realistic sample emails covering:

-HR
-Manager requests
-Tasks
-Meetings
-Reminders
-Newsletters
-Promo/Spam

**Running the App**

Start the Streamlit app:

streamlit run app.py


The app will open at:

http://localhost:8501

**How to Use the UI**
TAB 1: Prompt Brain
-Edit Categorization Prompt
-Edit Action Item Prompt
-Edit Auto-Reply Prompt
-Click Save Prompts

TAB 2: Inbox
1.Click Load & Process Inbox
2.View:
  Category
  Tasks
  Summary
3.Ask the inbox agent:
  “Show me urgent emails”
  “List To-Do items”

TAB 3: Email Agent & Drafts
1.Select an email
2.Ask:
  “Summarize this email”
  “What tasks do I need to do?”
3.Generate reply draft (tone optional)
4.View saved drafts


