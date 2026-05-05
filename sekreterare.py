import os
import queue
import sounddevice as sd
import numpy as np
import whisper
import wave
import threading
import time
from datetime import datetime
from god_brain_core import GodBrainEngine, logger

class AISecretary:
    """
    AI Secretary: Handles local audio capture and multi-device transcription.
    Syncs with GodBrain core for persistent memory.
    """
    def __init__(self, model_size="base"):
        self.engine = GodBrainEngine()
        logger.info(f"[+] Loading Whisper Model ({model_size})...")
        self.model = whisper.load_model(model_size)
        self.audio_queue = queue.Queue()
        self.recording = False
        self.sample_rate = 16000 # Whisper standard
        
    def start_recording(self):
        self.recording = True
        self.recording_thread = threading.Thread(target=self._record_loop)
        self.recording_thread.start()
        logger.info("[!] AI Secretary is now listening...")

    def stop_recording(self, filename="meeting_audio.wav"):
        self.recording = False
        self.recording_thread.join()
        logger.info("[+] Recording stopped. Processing...")
        return self.transcribe(filename)

    def _record_loop(self):
        with sd.InputStream(samplerate=self.sample_rate, channels=1, callback=self._audio_callback):
            while self.recording:
                sd.sleep(100)

    def _audio_callback(self, indata, frames, time, status):
        if status:
            logger.warning(f"Audio status: {status}")
        self.audio_queue.put(indata.copy())

    def save_wav(self, filename, audio_data):
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2) # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())

    def transcribe(self, audio_path):
        """Transcribes audio and saves to GodBrain."""
        start_time = time.time()
        result = self.model.transcribe(audio_path, language="sv")
        text = result["text"].strip()
        duration = time.time() - start_time
        
        logger.info(f"[+] Transcription Complete ({duration:.2f}s): {text[:50]}...")
        
        # Create a new event loop for the async save call if one isn't running
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        if loop.is_running():
            # If we're inside FastAPI (already running), use create_task
            loop.create_task(self.engine.save_thought(
                content=f"[Meeting Note] {text}",
                source="AI_Secretary",
                tags=["meeting", "transcription"]
            ))
        else:
            # For standalone CLI testing
            loop.run_until_complete(self.engine.save_thought(
                content=f"[Meeting Note] {text}",
                source="AI_Secretary",
                tags=["meeting", "transcription"]
            ))
        return text

    async def ingest_remote_audio(self, audio_bytes, device_name="iPhone"):
        """Endpoint-ready method for iPhone audio ingestion."""
        filename = f"remote_{device_name}_{int(time.time())}.wav"
        with open(filename, "wb") as f:
            f.write(audio_bytes)
        logger.info(f"[+] Received audio from {device_name}")
        return self.transcribe(filename)

if __name__ == "__main__":
    import asyncio
    sec = AISecretary()
    # Simple CLI Trigger test
    print("Press Enter to start recording (Swedish)...")
    input()
    sec.start_recording()
    print("Recording... Press Enter to stop.")
    input()
    # We save a temporary buffer for testing
    audio_data = []
    while not sec.audio_queue.empty():
        audio_data.append(sec.audio_queue.get())
    
    if audio_data:
        full_audio = np.concatenate(audio_data, axis=0)
        test_file = "test_meeting.wav"
        sec.save_wav(test_file, full_audio)
        sec.stop_recording(test_file)
    else:
        sec.recording = False
        print("No audio captured.")
