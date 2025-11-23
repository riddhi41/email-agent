# Prompt-Driven Email Productivity Agent
 
_AI-powered email organizer, task extractor, summarizer, and draft generator, built using Streamlit + Groq LLaMA 3.1._

---

## Overview

This project is an **AI-driven Email Productivity Agent** that processes a mock inbox and performs:

- **Email categorization**
- **Action-item extraction**
- **Automatic summarization**
- **Reply draft generation**
- **Inbox-wide analysis**
- **Prompt-driven behavior** (via customizable “Agent Brain” prompts)

Built using:

- Python  
- Streamlit  
- Groq API (LLaMA 3.1 8B Instant)  
- Local JSON storage  

---

## Key Features

### 1. Prompt Brain (Fully Customizable)
Edit and save prompts controlling:
- Email categorization  
- Task detection  
- Auto-reply generation  

Prompts persist in `prompts.json`.

---

### 2. Inbox Processing
Click **Load & Process Inbox** to automatically:

- Categorize each email  
- Extract tasks  
- Generate concise summaries  

Stored in `processed_emails.json`.

---

### 3. Email Agent
Ask natural-language questions:

- “Summarize this email”  
- “What tasks do I need to do?”  
- “Draft a reply in a friendly tone”  
- “Is this email urgent?”  

---

### 4. Inbox-Level Agent
Query across the whole inbox:

- “Show all urgent emails”  
- “List pending tasks”  

---

### 5. Reply Draft Generator
Generates:
- Subject  
- Body  
- Follow-up suggestions  

Drafts saved in: data/drafts.json


---

## 📁 Project Structure

```text
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
```


## Installation & Setup
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

## Setup API Key (Groq)

1. Create a Groq account: https://console.groq.com

2. Go to API Keys → Create API Key

3. Copy your key

4. Create .env file (NOT committed to GitHub)

Inside .env:

GROQ_API_KEY=your_actual_key_here


## Mock Inbox

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

## Running the App

Start the Streamlit app:

streamlit run app.py


The app will open at:

http://localhost:8501

## 🧭 How to Use the UI

### **TAB 1: Prompt Brain**
- Edit **Categorization Prompt**
- Edit **Action Item Prompt**
- Edit **Auto-Reply Prompt**
- Click **Save Prompts** to store your changes

---

### **TAB 2: Inbox**
1. Click **Load & Process Inbox**
2. View generated data for each email:
   - **Category**
   - **Tasks / Action Items**
   - **Summary**
3. Ask the inbox agent questions such as:
   - “Show me urgent emails”
   - “List To-Do items”

---

### **TAB 3: Email Agent & Drafts**
1. **Select an email** from the dropdown
2. Ask questions like:
   - “Summarize this email”
   - “What tasks do I need to do?”
3. Generate a **reply draft** (you can specify tone)
4. View all saved drafts at the bottom of the page



