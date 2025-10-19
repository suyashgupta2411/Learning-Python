import os
import json
import time
import wave
import threading
import pyaudio
import websocket
from datetime import datetime
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
AAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

# --- Audio Config ---
FRAMES_PER_BUFFER = 800   # 50ms @ 16kHz
SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16

# --- Globals ---
audio = None
stream = None
ws_app = None
audio_thread = None
stop_event = threading.Event()
recorded_frames = []
recording_lock = threading.Lock()

# --- WebSocket Handlers (AssemblyAI) ---
def on_open(ws):
    print("WebSocket connection opened. 🎙️ Start speaking...")

    def stream_audio():
        global stream
        while not stop_event.is_set():
            try:
                data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                with recording_lock:
                    recorded_frames.append(data)
                ws.send(data, websocket.ABNF.OPCODE_BINARY)
            except Exception as e:
                print(f"Audio stream error: {e}")
                break
        print("Audio streaming stopped.")

    global audio_thread
    audio_thread = threading.Thread(target=stream_audio, daemon=True)
    audio_thread.start()

def on_message(ws, message):
    try:
        data = json.loads(message)
        if "text" in data:
            transcript = data["text"]
            if transcript.strip():
                print(f"\n📝 You said: {transcript}")
                # Call Gemini for response
                ai_response = query_gemini(transcript)
                print(f"🤖 Jarvis: {ai_response}")
                # Speak with Murf
                speak_murf(ai_response)
    except Exception as e:
        print(f"Message error: {e}")

def on_error(ws, error):
    print(f"WebSocket Error: {error}")
    stop_event.set()

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket Disconnected: {close_status_code}, {close_msg}")
    save_wav_file()
    cleanup_audio()

# --- Save WAV ---
def save_wav_file():
    if not recorded_frames:
        return
    filename = f"recorded_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    try:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            with recording_lock:
                wf.writeframes(b''.join(recorded_frames))
        print(f"💾 Audio saved: {filename}")
    except Exception as e:
        print(f"Error saving wav: {e}")

def cleanup_audio():
    global stream, audio
    stop_event.set()
    if stream:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        stream = None
    if audio:
        audio.terminate()
        audio = None
    if audio_thread and audio_thread.is_alive():
        audio_thread.join(timeout=1.0)
    print("🎤 Audio cleanup complete.")

# --- Gemini Query ---
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

def query_gemini(text):
    try:
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(
            text + " (Respond briefly in simple English)"
        )
        return response.text.strip()
    except Exception as e:
        return f"[Gemini error: {e}]"

# --- Murf TTS ---
from murf import Murf
murf_client = Murf(api_key=MURF_API_KEY)

def speak_murf(text):
    try:
        res = murf_client.text_to_speech.generate(
            text=text,
            voice_id="en-US-terrell",
        )
        print("🔊 (Murf generated audio)")
        # Optional: save audio
        with open("response.mp3", "wb") as f:
            f.write(res.audio_file.read())
    except Exception as e:
        print(f"Murf error: {e}")

# --- Main ---
def run():
    global audio, stream, ws_app
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            channels=CHANNELS,
            format=FORMAT,
            rate=SAMPLE_RATE,
        )
        print("Microphone ready. Speak to Jarvis (Ctrl+C to exit).")
    except Exception as e:
        print(f"Mic error: {e}")
        return

    url =f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}&model=universal-streaming"

    ws_app = websocket.WebSocketApp(
        url,
        header={"Authorization": AAI_API_KEY},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws_thread = threading.Thread(target=ws_app.run_forever, daemon=True)
    ws_thread.start()

    try:
        while ws_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping...")
        stop_event.set()
        if ws_app and ws_app.sock and ws_app.sock.connected:
            ws_app.send(json.dumps({"terminate_session": True}))
            time.sleep(1)
        ws_app.close()
        ws_thread.join()

if __name__ == "__main__":
    run()
