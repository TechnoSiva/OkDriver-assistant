import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import pyttsx3
import requests
import time
from config import GROQ_API_KEY, WAKE_WORD_PATH
from config import PICOVOICE_ACCESS_KEY


# Initialize TTS
engine = pyttsx3.init()
engine.setProperty("rate", 210)

# Speech recognizer
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.5
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.non_speaking_duration = 0.2


# LLM API endpoint
LLM_URL = "https://api.groq.com/openai/v1/chat/completions"
SYSTEM_PROMPT = (
    "You are a fast voice assistant for drivers. "
    "Remember recent conversation context and reply in one short sentence."
)
MEMORY_TURNS = 6

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
REQUEST_TIMEOUT = (1.5, 8)
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def calibrate_microphone():
    # Running ambient calibration once at startup to avoid per-query latency.
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=0.25)


def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=3,
                phrase_time_limit=4
            )
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None

    try:
        text = recognizer.recognize_google(audio)
        print("User:", text)
        return text

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None

    except sr.RequestError:
        print("Speech recognition service failed.")
        return None


def trim_conversation(conversation_history):
    # Keep system prompt + last N user/assistant turns to bound latency.
    max_messages = MEMORY_TURNS * 2
    non_system_count = len(conversation_history) - 1
    if non_system_count > max_messages:
        del conversation_history[1:1 + (non_system_count - max_messages)]


def ask_llm(conversation_history):

    payload = {
    "model": "llama-3.1-8b-instant",
    "messages": conversation_history,
    "max_tokens": 24
}

    try:
        response = SESSION.post(
            LLM_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException:
        return None

    data = response.json()

    #print("LLM RAW RESPONSE:", data)   # debug output

    if "choices" in data:
        return data["choices"][0]["message"]["content"].strip()
    else:
        return None


def run_assistant():

    porcupine = pvporcupine.create(
    access_key=PICOVOICE_ACCESS_KEY,
    keyword_paths=[WAKE_WORD_PATH]
)

    calibrate_microphone()

    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Waiting for wake word...")
    conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    try:
        while True:

            pcm = stream.read(
                porcupine.frame_length,
                exception_on_overflow=False,
            )
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm)

            if result >= 0:

                print("Wake word detected!")

                total_start = time.perf_counter()

                stt_start = time.perf_counter()
                query = speech_to_text()
                stt_end = time.perf_counter()

                if query is not None:
                    normalized_query = query.strip().lower()
                    if normalized_query in {"clear memory", "reset memory", "forget conversation"}:
                        conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
                        llm_end = stt_end
                        speak("Memory cleared.")
                        tts_end = time.perf_counter()
                    else:
                        conversation_history.append({"role": "user", "content": query})
                        trim_conversation(conversation_history)

                        response = ask_llm(conversation_history)
                        llm_end = time.perf_counter()

                        if response is None:
                            response = "Sorry, I couldn't process that request."
                        else:
                            conversation_history.append({"role": "assistant", "content": response})
                            trim_conversation(conversation_history)

                        speak(response)
                        tts_end = time.perf_counter()
                else:
                    print("Returning to wake word mode...")
                    llm_end = stt_end
                    tts_end = stt_end

                total_end = time.perf_counter()

                print(
                    "Latency breakdown (s): "
                    f"STT={stt_end - stt_start:.2f}, "
                    f"LLM={llm_end - stt_end:.2f}, "
                    f"TTS={tts_end - llm_end:.2f}, "
                    f"TOTAL={total_end - total_start:.2f}"
                )
                print("\nWaiting for wake word...")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    run_assistant()
