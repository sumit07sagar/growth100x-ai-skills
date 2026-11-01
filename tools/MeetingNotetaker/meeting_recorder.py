#!/usr/bin/env python3
"""
the assistant's recorder — records a Google Meet call via a macOS Aggregate Device
(your mic = channel 1, BlackHole = channel 2 = the other participant),
transcribes both channels with Groq Whisper (same free pipeline as VoiceType),
and merges them into one timestamped, speaker-labeled transcript.

Nothing joins the call. Nothing leaves your Mac until you press ENTER to stop
— at that point audio chunks are sent to Groq for transcription, and never
before.

Usage:
    python3 meeting_recorder.py "Client Name"
    (or just: python3 meeting_recorder.py  -- uses "Meeting" as the label)

Press ENTER to stop recording and finalize the transcript.

One-time setup required (see README.md):
  1. Install BlackHole 2ch (https://existential.audio/blackhole/)
  2. Create Multi-Output + Aggregate Device pairs in Audio MIDI Setup — one
     pair per audio setup you use (built-in / wired / Bluetooth).
  3. In Google Meet's in-call audio settings, select the Aggregate Device as
     your Microphone and the matching Multi-Output Device as your Speaker.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import time
import wave
from datetime import datetime
from pathlib import Path

try:
    import numpy as np
    import requests
    import sounddevice as sd
except ImportError as e:
    print(f"Missing dependency: {e.name}. Run ./setup.sh first.")
    sys.exit(1)

# ----------------------------- CONFIG ---------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SCRIPT_DIR / "config.json"
VOICETYPE_CONFIG = SCRIPT_DIR.parent / "VoiceType" / "config.json"  # reuse existing key if present
TRANSCRIPTS_DIR = SCRIPT_DIR / "Transcripts"

SAMPLE_RATE = 16000
CHUNK_SECONDS = 240           # ~4 min per Groq call, keeps files well under the 25MB limit
INPUT_DEVICE_NAME = "auto"    # "auto" = first device with "aggregate" in its name; or set an exact name/index

WHISPER_MODEL = "whisper-large-v3-turbo"
VOCAB_PROMPT = (
    "Growth100X, GEO, AEO, SEO, LLM, Upwork, WordPress, Elementor, "
    "ChatGPT, Claude, Google Meet, roadmap, action items, proposal, the assistant."
)
GROQ_BASE = "https://api.groq.com/openai/v1"

SPEAKER_LABELS = {0: "SUMIT", 1: "OTHER PARTICIPANT"}  # channel 0 = mic, channel 1 = BlackHole

# ----------------------------- HELPERS --------------------------------------

def load_api_key() -> str:
    key = os.environ.get("GROQ_API_KEY", "").strip()
    for f in (CONFIG_FILE, VOICETYPE_CONFIG):
        if key:
            break
        if f.exists():
            try:
                key = json.loads(f.read_text()).get("groq_api_key", "").strip()
            except json.JSONDecodeError:
                pass
    if not key:
        print("No Groq API key found. Run ./setup.sh, or copy VoiceType/config.json here.")
        sys.exit(1)
    return key


def find_input_device():
    """Returns a device index for the Aggregate Device, or None to fall back
    to the system default input (mic-only, no other-participant channel)."""
    if INPUT_DEVICE_NAME != "auto":
        return INPUT_DEVICE_NAME
    try:
        devices = sd.query_devices()
    except Exception as e:
        print(f"! Could not query audio devices ({e}); using system default.")
        return None
    for i, d in enumerate(devices):
        if d["max_input_channels"] >= 2 and "aggregate" in d["name"].lower():
            print(f"Using input device: {d['name']} (#{i})")
            return i
    print("! No 'Aggregate' input device found — falling back to system default input.")
    print("  You'll only capture your own mic, not the other participant. See README.md.")
    return None


def wav_bytes_mono(frames: np.ndarray) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(np.ascontiguousarray(frames, dtype=np.int16).tobytes())
    return buf.getvalue()

# ----------------------------- GROQ -----------------------------------------

class Groq:
    def __init__(self, api_key: str):
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def transcribe_segments(self, audio: bytes) -> list:
        """Returns Whisper verbose_json segments: [{start, end, text}, ...]"""
        r = requests.post(
            f"{GROQ_BASE}/audio/transcriptions",
            headers=self.headers,
            files={"file": ("audio.wav", audio, "audio/wav")},
            data={
                "model": WHISPER_MODEL,
                "response_format": "verbose_json",
                "language": "en",
                "prompt": VOCAB_PROMPT,
                "temperature": 0,
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("segments", []) or []

# ----------------------------- RECORDER -------------------------------------

class Recorder:
    def __init__(self, device):
        self.device = device
        self.channels = 2 if device is not None else 1
        self.chunks = []
        self.stream = None
        self.started_at = 0.0

    def start(self):
        self.started_at = time.time()
        try:
            self.stream = sd.InputStream(
                samplerate=SAMPLE_RATE, channels=self.channels, dtype="int16",
                device=self.device,
                callback=lambda indata, *_: self.chunks.append(indata.copy()),
            )
            self.stream.start()
        except Exception as e:
            print(f"! Could not open {self.channels}-channel stream on that device ({e}).")
            print("  Falling back to single-channel (mic only).")
            self.channels = 1
            self.device = None
            self.stream = sd.InputStream(
                samplerate=SAMPLE_RATE, channels=1, dtype="int16",
                callback=lambda indata, *_: self.chunks.append(indata.copy()),
            )
            self.stream.start()
        print(f"● Recording started at {datetime.now().strftime('%H:%M:%S')} — press ENTER to stop.")

    def stop(self) -> np.ndarray:
        self.stream.stop()
        self.stream.close()
        if not self.chunks:
            return np.zeros((0, self.channels), dtype=np.int16)
        return np.concatenate(self.chunks)

# ----------------------------- MAIN -----------------------------------------

def build_chunks(frames_1ch: np.ndarray):
    step = CHUNK_SECONDS * SAMPLE_RATE
    return [frames_1ch[i:i + step] for i in range(0, len(frames_1ch), step)
            if len(frames_1ch[i:i + step]) > SAMPLE_RATE]  # drop trailing <1s scraps


def transcribe_channel(groq: Groq, frames_1ch: np.ndarray, speaker: str) -> list:
    segments = []
    chunks = build_chunks(frames_1ch)
    for idx, chunk in enumerate(chunks):
        offset = idx * CHUNK_SECONDS
        print(f"  Transcribing {speaker} chunk {idx + 1}/{len(chunks)}...")
        try:
            for seg in groq.transcribe_segments(wav_bytes_mono(chunk)):
                text = (seg.get("text") or "").strip()
                if text:
                    segments.append({"start": seg["start"] + offset, "speaker": speaker, "text": text})
        except requests.HTTPError as e:
            body = e.response.text[:200] if e.response is not None else ""
            print(f"  ! Groq error on {speaker} chunk {idx}: {e} {body}")
        except requests.RequestException as e:
            print(f"  ! Network error on {speaker} chunk {idx}: {e}")
    return segments


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "Meeting"
    groq = Groq(load_api_key())
    device = find_input_device()
    rec = Recorder(device)
    rec.start()

    try:
        input()
    except KeyboardInterrupt:
        pass
    frames = rec.stop()
    duration = len(frames) / SAMPLE_RATE
    print(f"■ Stopped. {duration:.0f}s recorded. Transcribing (this can take a minute or two)...")

    if duration < 1:
        print("Nothing recorded — check your audio device setup (see README.md). No transcript saved.")
        return

    if frames.ndim == 1 or frames.shape[1] < 2:
        print("Only one channel captured — everything labeled SUMIT (no other-participant channel found).")
        all_segments = transcribe_channel(groq, frames if frames.ndim == 1 else frames[:, 0], "SUMIT")
    else:
        mic_segments = transcribe_channel(groq, frames[:, 0], SPEAKER_LABELS[0])
        other_segments = transcribe_channel(groq, frames[:, 1], SPEAKER_LABELS[1])
        all_segments = mic_segments + other_segments

    all_segments.sort(key=lambda s: s["start"])

    TRANSCRIPTS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M")
    safe_label = re.sub(r"[^A-Za-z0-9_-]+", "_", label).strip("_") or "Meeting"
    out_path = TRANSCRIPTS_DIR / f"{ts}_{safe_label}.txt"

    lines = [f"# Meeting transcript — {label} — {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    for seg in all_segments:
        mm, ss = divmod(int(seg["start"]), 60)
        lines.append(f"[{mm:02d}:{ss:02d}] {seg['speaker']}: {seg['text']}")
    out_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"✓ Transcript saved: {out_path}")
    print('  Tell the assistant in your Growth 100x chat: "process last meeting" to get the recap drafted.')


if __name__ == "__main__":
    main()
