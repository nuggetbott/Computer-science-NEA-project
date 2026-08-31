"""
FASTER, more responsive voice control.

Key change from the previous version:
- Volume (for jump) is checked on tiny, continuous chunks of audio in real
  time using a callback - no waiting, no blocking, no speech-to-text needed.
- Speech-to-text (for "pause") is only run when needed, in the background,
  on a short recent buffer - it does not block the volume checking at all.

This matches the flowchart logic (Is Volume > threshold? -> Trigger jump,
Voice == "pause"? -> Open pause menu) but restructures WHEN each check
happens so the game stays responsive.

Install:
    pip install sounddevice numpy SpeechRecognition
"""

import sounddevice as sd
import numpy as np
import speech_recognition as sr
import threading
import queue
import time

THRESHOLD = 6000     # tune this to your mic - see note below
SAMPLE_RATE = 16000
CHUNK_MS = 100            # check volume every 100ms - much faster than 3s frames
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_MS / 1000)

recognizer = sr.Recognizer()
audio_queue = queue.Queue()
running = True

# rolling buffer used only for speech-to-text (pause command)
speech_buffer = np.zeros(0, dtype="int16")
SPEECH_BUFFER_SECONDS = 2


def audio_callback(indata, frames, time_info, status):
    """Called automatically by sounddevice for every small chunk of audio - non-blocking."""
    audio_queue.put(indata.copy())


def volume_of(chunk):
    return float(np.abs(chunk).mean())


def check_for_pause(buffer):
    """
    Runs speech-to-text on a short buffer, in a separate thread, so it
    never blocks the fast jump-detection loop above.
    """
    try:
        audio_bytes = buffer.tobytes()
        audio_source = sr.AudioData(audio_bytes, SAMPLE_RATE, 2)
        command = recognizer.recognize_google(audio_source).lower()
        if command == "pause":
            print(">>> Open pause menu")
    except (sr.UnknownValueError, sr.RequestError):
        pass  # ignore - most chunks won't contain clear speech


def main():
    global speech_buffer
    print("Listening in real time. Speak loudly to jump, say 'pause' to pause. Ctrl+C to quit.\n")

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16",
                         blocksize=CHUNK_SIZE, callback=audio_callback):
        last_jump_time = 0
        jump_cooldown = 0.5  # prevents one shout triggering multiple jumps

        while True:
            chunk = audio_queue.get().flatten()
            volume = volume_of(chunk)

            # --- fast path: jump (checked on every tiny chunk, no delay) ---
            now = time.time()
            if volume > THRESHOLD and (now - last_jump_time) > jump_cooldown:
                print(f"Volume {volume:.0f} > {THRESHOLD} -> Trigger jump")
                last_jump_time = now

            # --- slow path: pause (only runs speech-to-text every ~2s, in background) ---
            speech_buffer = np.concatenate([speech_buffer, chunk])
            max_len = SAMPLE_RATE * SPEECH_BUFFER_SECONDS
            if len(speech_buffer) >= max_len:
                buffer_copy = speech_buffer.copy()
                speech_buffer = np.zeros(0, dtype="int16")
                threading.Thread(target=check_for_pause, args=(buffer_copy,), daemon=True).start()


if __name__ == "__main__":
    main()