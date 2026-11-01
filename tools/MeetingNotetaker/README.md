# the assistant — Meeting Notetaker

Records both sides of a Google Meet call (your mic + the client's voice) locally on your Mac, transcribes it for free via Groq (same pipeline as VoiceType), and hands the transcript to the assistant in your Claude chat to turn into a recap email draft. Nothing joins the call. Nothing is visible to the client. 100% free (Groq free tier: 2,000 transcription requests/day).

## Part 1 — One-time audio routing setup (do this once, ever)

### Step 1: Install BlackHole

1. Go to https://existential.audio/blackhole/ and download **BlackHole 2ch** (free).
2. Run the installer. You may need to restart your Mac afterward.

### Step 2: Create your Multi-Output + Aggregate Device pairs

Open **Audio MIDI Setup** (Spotlight search → "Audio MIDI Setup"). You'll create one pair for each audio setup you actually use — built-in, wired, and/or Bluetooth. Takes about a minute per pair.

**For each setup (repeat for Built-in / Wired / Bluetooth):**

1. Click the **+** button (bottom-left) → **Create Multi-Output Device**.
   - Check the box for your actual output (e.g. "MacBook Air Speakers", "Sumit's AirPods", or your wired headset).
   - Check the box for **BlackHole 2ch**.
   - Rename it (double-click the name) to something clear, e.g. `Meet Output - Built-in`, `Meet Output - Wired`, `Meet Output - Bluetooth`.
2. Click **+** again → **Create Aggregate Device**.
   - Check the box for your actual microphone (e.g. "MacBook Air Microphone" or your headset's mic).
   - Check the box for **BlackHole 2ch**.
   - Rename it to e.g. `Meet Input - Built-in`, `Meet Input - Wired`, `Meet Input - Bluetooth`.
   - **Important:** click the little clock-icon column next to your real microphone and set it as the **Primary/Clock Source** if asked (avoids sync drift over long calls).

You now have a matched pair per setup. You don't need to touch Audio MIDI Setup again after this.

### Bluetooth note

Bluetooth devices can sometimes drop into a lower-quality "phone call" mode once the mic is active, which can make sync a bit less reliable. Built-in and wired are rock-solid; if you're on AirPods/Bluetooth for an important call, do a 30-second test recording first (see Part 3) to confirm both channels are coming through clearly.

## Part 2 — Script setup (do this once)

```
cd "~/MeetingNotetaker"
bash setup.sh
```

This installs Python dependencies and reuses your existing Groq API key from VoiceType automatically — no new signup needed. macOS will prompt for Microphone permission for Terminal on first run — grant it, then quit and reopen Terminal.

## Part 3 — Using it in a real meeting

1. **Before or right as the call starts**, in Google Meet click the **gear icon → Audio**, and set:
   - **Microphone** → the `Meet Input - [Built-in/Wired/Bluetooth]` device matching what you're wearing today.
   - **Speaker** → the matching `Meet Output - [...]` device.
   - (You'll still hear the client completely normally — this doesn't change what you hear, only adds a second, silent destination for the recording.)
2. **Double-click `the assistant.command`** (or run `bash run.sh` in Terminal). It'll ask for the client/meeting name (optional), then start recording.
3. Talk normally through the whole call.
4. **When the call ends**, go back to that Terminal window and press **ENTER**. It'll transcribe both channels (takes roughly 30-90 seconds for a typical call) and save a transcript to the `Transcripts/` folder.
5. In your Claude chat, say **"process last meeting"** and the assistant will read the transcript, write the recap + action plan + roadmap, and hand you a Gmail draft to review and send.

## Troubleshooting

- **"No 'Aggregate' input device found"**: you either skipped Part 1, or Meet's mic isn't set to the Aggregate Device — check Step 1 of Part 3.
- **Transcript only shows SUMIT, no OTHER PARTICIPANT lines**: Meet's Speaker isn't set to the Multi-Output Device, so the client's voice never reached BlackHole. Recheck Step 1 of Part 3.
- **"No Groq API key found"**: re-run `bash setup.sh`, or confirm `../VoiceType/config.json` still exists.
- **429 error**: free-tier rate limit (very unlikely at your call volume) — wait a minute and it'll recover on the next chunk.
- Audio quality sounding off on Bluetooth: switch that call's Meet audio devices to the Built-in or Wired pair instead.

## Privacy note

Recording a call without mentioning it to the other party is regulated in various ways depending on jurisdiction — worth a quick heads-up to clients at the start of calls ("I'll keep notes for my own reference") as standard practice.
