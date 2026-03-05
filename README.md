# Wake Word Activated Voice Assistant

A prototype conversational voice assistant that listens for a wake word, converts speech to text, sends the query to a Large Language Model (LLM), and responds using text-to-speech.
This project demonstrates a complete **voice AI pipeline** including wake-word detection, speech recognition, LLM integration, response generation, and latency measurement.

---

## Project Objective

The goal of this prototype is to implement a **real-time voice assistant system** capable of:

1. Detecting a wake word.
2. Capturing and converting speech to text.
3. Sending the query to an LLM API.
4. Generating a conversational response.
5. Converting the response into speech.
6. Measuring the total system latency.

---

## System Architecture

```
Microphone
   │
   ▼
Wake Word Detection (Porcupine)
   │
   ▼
Speech-to-Text (SpeechRecognition)
   │
   ▼
User Query
   │
   ▼
LLM API (Groq - Llama 3.1)
   │
   ▼
Generated Response
   │
   ▼
Text-to-Speech (pyttsx3)
   │
   ▼
Speaker Output
```

---

## Technologies Used

| Component            | Technology                      |
| -------------------- | ------------------------------- |
| Wake Word Detection  | Picovoice Porcupine             |
| Speech Recognition   | SpeechRecognition (Google STT)  |
| Language Model       | Groq API (Llama-3.1-8B-Instant) |
| Text-to-Speech       | pyttsx3                         |
| Programming Language | Python                          |
| Latency Measurement  | Python `time` module            |

---

## Features

* Wake-word activated interaction
* Real-time speech recognition
* LLM-powered conversational responses
* Text-to-speech output
* Automatic return to wake-word listening mode
* Latency benchmarking
* Error handling for speech timeouts

---

## Project Structure

```
voice-assistant/
│
├── assistant.py
├── config.py
├── wake_word.ppn
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/TechnoSiva/OkDriver-assistant.git
cd OkDriver-assistant
```

### 2. Install Dependencies

```bash
pip install pvporcupine pyaudio speechrecognition pyttsx3 requests python-dotenv
```

If PyAudio fails on Windows:

```bash
pip install pipwin
pipwin install pyaudio
```

---

### 3. Get Required API Keys

#### Picovoice Access Key

Create an account at:

https://console.picovoice.ai

Generate a **Porcupine Access Key** and download a **Windows wake-word `.ppn` file**.

Example wake word:

```
OK Driver
```

---

#### Groq API Key

Create an account at:

https://console.groq.com

Generate an API key and add it to `.env`.

---

### 4. Configure Keys

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key
PICOVOICE_ACCESS_KEY=your_picovoice_access_key
WAKE_WORD_PATH=wake_word.ppn
```

---

### 5. Run the Assistant

```bash
python assistant.py
```

Example output:

```
Waiting for wake word...

Wake word detected!

Listening...

User: kya haal chaal

Assistant: Main theek hoon.

Total latency: 2.5 seconds
```

---

## Latency Measurement

The system measures the total latency for the full pipeline:

```
Wake Word → STT → LLM → TTS
```

Typical performance:

| Stage               | Latency      |
| ------------------- | ------------ |
| Wake Word Detection | ~0.1s        |
| Speech Recognition  | ~1.5s        |
| LLM Response        | ~0.15s       |
| Text-to-Speech      | ~0.8s        |
| Total               | ~2–3 seconds |

---

## Example Interaction

User:

```
OK Driver
kya haal chaal
```

Assistant:

```
Main theek hoon. Aap kaise ho?
```

---


## Conclusion

This prototype demonstrates a complete **end-to-end conversational AI pipeline** integrating wake-word detection, speech recognition, LLM reasoning, and voice synthesis. The system is designed to simulate how modern voice assistants operate in real-time environments such as driver assistance platforms.

---

## Author

K Sivaram Achary
B.Tech Computer Science & Engineering
