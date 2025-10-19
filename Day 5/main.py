# pip install websocket-client pyaudio

import pyaudio
import websocket
import json
import threading
import time
from urllib.parse import urlencode

# Configuration
API_KEY = "239f4246625b46b4bb840010f2aaafeb"
CONNECTION_PARAMS = {"sample_rate": 16000, "format_turns": True}
API_ENDPOINT = f"wss://streaming.assemblyai.com/v3/ws?{urlencode(CONNECTION_PARAMS)}"

# Audio settings
FRAMES_PER_BUFFER = 800
SAMPLE_RATE = 16000
FORMAT = pyaudio.paInt16

# Global variables
audio = None
stream = None
ws_app = None
stop_event = threading.Event()

# Global transcript storage
TRANSCRIPT = {'text': ''}
transcript_lock = threading.Lock()

def on_open(ws):
    def stream_audio():
        while not stop_event.is_set():
            try:
                audio_data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                ws.send(audio_data, websocket.ABNF.OPCODE_BINARY)
            except:
                break
    
    threading.Thread(target=stream_audio, daemon=True).start()

def on_message(ws, message):
    try:
        data = json.loads(message)
        if data.get('type') == "Turn" and data.get('turn_is_formatted'):
            transcript = data.get('transcript', '').strip()
            if transcript:
                with transcript_lock:
                    if TRANSCRIPT['text']:
                        TRANSCRIPT['text'] += ' ' + transcript
                    else:
                        TRANSCRIPT['text'] = transcript
    except:
        pass

def on_error(ws, error):
    stop_event.set()

def on_close(ws, close_status_code, close_msg):
    stop_event.set()
    try:
        if stream:
            stream.stop_stream()
            stream.close()
        if audio:
            audio.terminate()
    except:
        pass

def run():
    global audio, stream, ws_app

    audio = pyaudio.PyAudio()
    
    try:
        stream = audio.open(
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            channels=1,
            format=FORMAT,
            rate=SAMPLE_RATE,
        )
    except Exception as e:
        print(f"Microphone error: {e}")
        return

    ws_app = websocket.WebSocketApp(
        API_ENDPOINT,
        header={"Authorization": API_KEY},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws_thread = threading.Thread(target=ws_app.run_forever, daemon=True)
    ws_thread.start()

    try:
        print("Recording... Press Ctrl+C to stop.")
        while ws_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping...")
        stop_event.set()
        
        try:
            ws_app.send(json.dumps({"type": "Terminate"}))
            time.sleep(0.5)
            ws_app.close()
        except:
            pass
        
        ws_thread.join(timeout=1.0)
       # print(f"Transcript: {TRANSCRIPT['text']}")

if __name__ == "__main__":
    run()

