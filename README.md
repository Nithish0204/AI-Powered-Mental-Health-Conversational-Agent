<div align="center">

<img src="https://img.shields.io/badge/Lumina-AI%20Mental%20Health%20Companion-blueviolet?style=for-the-badge&logo=heart&logoColor=white" alt="Lumina Banner"/>

# 🌟 Lumina – AI-Powered Mental Health Companion

> *"You're never alone when Lumina is here."*

Lumina is an emotionally intelligent AI chatbot that provides personalized mental health support through relationship-based conversations, voice cloning, and expressive speech synthesis — designed to feel like talking to someone who truly knows you.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![ElevenLabs](https://img.shields.io/badge/ElevenLabs-Voice%20AI-orange?style=flat-square)](https://elevenlabs.io)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/whisper)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 📖 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup Instructions](#-setup-instructions)
- [Use Cases](#-use-cases)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 💬 About

Lumina bridges the gap between technology and emotional well-being. Rather than a generic chatbot, Lumina lets users choose a **relationship persona** — a Mom, Dad, or Friend — and even **clone a real voice** using an uploaded audio sample. The result is a deeply personal companion that speaks to you the way the people you love do.

Built for students, individuals managing stress, and anyone who needs a safe, judgment-free space to be heard.

---

## ✨ Features

### 🧠 Relationship-Based AI
| Persona | Personalities Available |
|---|---|
| Mom | Calm, Fun, Strict, Emotional |
| Dad | Supportive, Motivational, Wise |
| Friend | Cheerful, Chill, Empathetic |

- Custom **nickname support** — Lumina addresses you the way you want
- Context-aware responses tailored to the chosen relationship

### 🎙️ Voice & Speech
- **Voice Cloning** using uploaded audio samples via ElevenLabs
- **Text-to-Speech** with emotional tone using SSML
- **Static Indian voice fallback** for users without voice samples
- **Speech-to-Text** powered by OpenAI Whisper

### 🌐 Language Support
- English & Hindi (regional language expansion planned)

### 🧘 Therapy & Mood Booster Section
- 😄 Jokes & Fun Therapy
- 🎵 Music Therapy
- 💬 Positive Affirmations
- 🌬️ Breathing & Guided Exercises
- 📖 Motivational Quotes & Stories

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python (Flask) |
| **LLM** | Gemma 3 |
| **Speech-to-Text** | OpenAI Whisper |
| **Text-to-Speech & Voice Cloning** | ElevenLabs |
| **Emotion Detection** | Custom Emotion Detection Model |

---

## 📁 Project Structure

```
mental_health_chatbot/
│
├── app.py                  # Main Flask application entry point
├── main.py                 # Core logic and routing
│
├── chatbot/                # Chatbot logic, persona handling, response generation
├── models/                 # Emotion detection and ML models
│
├── static/                 # Frontend assets (CSS, JS, images)
├── templates/              # HTML templates (Jinja2)
├── uploads/                # User-uploaded voice samples
│
├── voice_generator.py      # Text-to-Speech with emotional SSML
├── voice_cloning.py        # ElevenLabs voice cloning integration
│
└── .env                    # Environment variables (API keys)
```

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.10+
- pip
- An [ElevenLabs](https://elevenlabs.io) account (for TTS & voice cloning)
- An [OpenAI](https://platform.openai.com) account (for Whisper STT)

---

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/lumina.git
cd lumina
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
ELEVEN_API_KEY=your_elevenlabs_api_key
OPENAI_API_KEY=your_openai_api_key
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### 5. Run the Application

```bash
python app.py
```

Open your browser and navigate to:

```
http://localhost:5000
```

---

## 💡 Use Cases

- 🎓 **Students** dealing with academic pressure and loneliness
- 🧑‍💼 **Professionals** experiencing workplace stress
- 💔 **Individuals** going through difficult emotional phases
- 🏥 **Healthcare + AI Hackathon** use case demonstrations
- 🌙 **Anyone** who needs a calm, non-judgmental presence at any hour

---

## 🔮 Future Improvements

- [ ] User authentication & secure profiles
- [ ] Conversation history & session storage
- [ ] Emotional progress tracking over time
- [ ] Expanded regional language support (Tamil, Telugu, Bengali, etc.)
- [ ] Mobile application (Android & iOS)
- [ ] Integration with wearable devices for real-time mood sensing

---

## 👨‍💻 Author

**Nithish**
B.Tech – Information Technology | Expected Graduation: 2027

> *Built with empathy, powered by AI.*

---

<div align="center">

⭐ If Lumina helped or inspired you, consider giving this repo a star!

</div>
