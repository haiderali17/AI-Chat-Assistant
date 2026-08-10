# 🤖 AI Chat Assistant

An AI-powered conversational assistant built with **Python, Streamlit, and Groq API**.

The application supports multiple AI personalities, streaming responses, adjustable temperature, configurable models, session-based conversation memory, and conversation export in TXT, JSON, and PDF formats.

---

## ✨ Features

### 💬 AI Chat

- AI-powered conversational chat
- Real-time streaming responses
- Session-based conversation history
- Context-aware conversations

### 🧠 AI Personalities

Choose how the assistant should behave:

- General Assistant
- Coding Assistant
- Study Assistant
- Career Assistant
- General Knowledge Expert
- Creative Writing Assistant
- Language Learning Assistant
- Gym and Fitness Coach
- Mental Health Support Assistant
- Travel and Adventure Guide
- Financial Advisor
- Health and Wellness Coach
- Art and Design Mentor

Each personality uses a dedicated **system prompt** to control the assistant's behavior and response style.

### ⚙️ Model Configuration

- Configurable Groq model
- Adjustable temperature
- Runtime configuration without changing the core chatbot logic

### 📤 Conversation Export

Export the current conversation as:

- 📄 TXT
- 📦 JSON
- 📑 PDF

PDF files are generated using **ReportLab**.

### 🛠️ Additional Features

- 🗑️ Clear conversation
- 🔐 Environment-based API key management
- 📝 Application logging
- 🎨 Custom Streamlit UI
- ♻️ Reusable service and utility classes

---

## 🏗️ Architecture

The application follows a modular architecture with clear separation of responsibilities.

```text
User
  ↓
Streamlit UI
  ↓
AI Personality + Model + Temperature
  ↓
GroqService
  ↓
Groq API
  ↓
Streaming Response
  ↓
Session State
  ↓
Conversation Export
  ├── TXT
  ├── JSON
  └── PDF
```

---

## 📁 Project Structure

```text
AI-Chat-Assistant/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── services/
│   └── groq_service.py
│
├── utils/
│   ├── logger.py
│   └── pdf_generator.py
│
└── styles/
    └── style.css
```

### Responsibilities

| Component | Responsibility |
|---|---|
| `app.py` | Streamlit UI and application flow |
| `config.py` | Environment configuration, models, and AI personalities |
| `GroqService` | Groq API communication |
| `PDFGenerator` | Conversation PDF generation |
| `logger.py` | Application logging |
| `style.css` | Custom UI styling |

---

## 🧩 Software Engineering Concepts

This project was structured around practical software engineering principles.

### Single Responsibility Principle

Each component has a focused responsibility.

```text
app.py
→ UI and application flow

GroqService
→ Groq API communication

PDFGenerator
→ PDF generation

logger
→ Application logging

config.py
→ Configuration
```

### Reusability

Services and utilities are initialized once and reused throughout the application.

```python
groq_service = GroqService()
pdf_generator = PDFGenerator()
```

### Separation of Concerns

The application separates:

- UI logic
- API communication
- Configuration
- PDF generation
- Logging
- Styling

### Configuration-Driven Design

AI personalities are stored centrally in `config.py`.

Adding a new personality does not require modifying the sidebar UI.

```python

AI_PERSONALITIES = {
    "General Assistant": "...",
    "Coding Assistant": "...",
    "Study Assistant": "...",
    "Career Assistant": "...",
    "General Knowledge Expert": "...",
    "Creative Writing Assistant": "...",
    "Language Learning Assistant": "...",
    "Gym and Fitness Coach": "...",
    "Mental Health Support Assistant": "...",
    "Travel and Adventure Guide": "...",
    "Financial Advisor": "...",
    "Health and Wellness Coach": "...",
    "Art and Design Mentor": "..."
}

The UI automatically gets the available personalities from the configuration.

---

## 🧠 How AI Personalities Work

The selected personality is converted into a system prompt.

```text
User selects personality
        ↓
AI_PERSONALITIES
        ↓
System Prompt
        ↓
GroqService
        ↓
Groq API
```

For example:

```python
"Coding Assistant": (
    "You are an expert programming assistant. "
    "Explain programming concepts clearly. "
    "Provide practical examples and clean code when useful."
)
```

This allows the same underlying LLM to behave differently depending on the selected personality.

---

## 🌡️ Temperature

Temperature controls the variability of generated responses.

```text
Lower temperature
        ↓
More consistent responses

Higher temperature
        ↓
More varied responses
```

Temperature is not an intelligence setting. It controls response variability.

---

## ⚡ Streaming

Instead of waiting for the entire response, the application displays the response progressively.

```text
Groq API
    ↓
Response chunks
    ↓
Streamlit
    ↓
User sees response progressively
```

This improves the perceived responsiveness of the application.

---

## 💾 Conversation Export

The current conversation can be exported in three formats.

### 📄 TXT

Creates a simple, readable text version of the conversation.

Example:

```text
USER:
Explain inheritance in C++

ASSISTANT:
Inheritance is an object-oriented programming concept...
```

### 📦 JSON

Stores the conversation as structured data.

Example:

```json
[
    {
        "role": "user",
        "content": "Explain inheritance in C++"
    },
    {
        "role": "assistant",
        "content": "Inheritance is an object-oriented programming concept..."
    }
]
```

### 📑 PDF

The conversation is converted into a formatted PDF using ReportLab.

```text
Conversation
     ↓
PDFGenerator
     ↓
ReportLab
     ↓
PDF bytes
     ↓
Streamlit download
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application UI |
| Groq API | LLM inference |
| ReportLab | PDF generation |
| python-dotenv | Environment variable management |
| JSON | Conversation serialization |
| Python Logging | Application logging |
| CSS | Custom UI styling |

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/haiderali17/AI-Chat-Assistant.git
```

### 2. Navigate to the project

```bash
cd AI-Chat-Assistant
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key_here
```

The application loads the API key using `python-dotenv`.

### Important

Never commit your `.env` file to GitHub.

The repository includes `.env.example` instead:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will start locally and open in your browser.

---

## 📦 Requirements

The project uses:

```text
streamlit
groq
python-dotenv
reportlab
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🔮 Future Improvements

Possible future improvements include:

- Persistent conversation history
- Multiple chat sessions
- Database integration
- User authentication
- Voice input
- Voice output
- File and document chat
- Additional LLM providers
- Production deployment
- Advanced conversation management

---

## 📌 Project Status

**Version 2 — Completed**

This project was built as a practical AI engineering project to explore:

- LLM API integration
- Prompt engineering
- Streaming responses
- Session state
- Configurable AI behavior
- JSON serialization
- PDF generation
- Modular architecture
- Software engineering principles

---

## 👨‍💻 Author

### Haider Ali

BS IT Student interested in:

- Artificial Intelligence
- Machine Learning
- AI Engineering
- LLM Applications
- AI-powered Automation