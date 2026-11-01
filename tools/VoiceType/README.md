# VoiceType — speak instead of type

Tap **Right Option (⌥)** once to start recording, tap it again to stop. Cleaned-up text appears wherever your cursor is — Cowork, browser, Gmail, WordPress, anywhere. 100% free (Groq free tier: 2,000 dictations/day).

## Pipeline

Mic → **Groq Whisper large-v3-turbo** (transcription, handles Indian-accented English + Hinglish) → **Llama 3.3 70B** (removes "um/uh/like", fixes punctuation, applies "new line"/"new paragraph" commands) → pastes at cursor.

## Setup (5 minutes, one time)

1. Get a free API key: https://console.groq.com/keys — sign in with Google, click "Create API Key". No card needed.
2. Open Terminal, then:
   ```
   cd "~/VoiceType"
   bash setup.sh
   ```
   Paste your key when asked.
3. Start it:
   ```
   bash run.sh
   ```
4. First run: macOS will prompt for permissions. Grant **Microphone**, **Input Monitoring**, and **Accessibility** to Terminal (System Settings → Privacy & Security). Then quit Terminal fully (Cmd+Q), reopen, and `bash run.sh` again.

## Daily use

- Keep the Terminal window running (minimize it).
- Click into any text box, **tap Right Option once** to start, speak for as long as you need, **tap Right Option again** to stop and paste. No need to hold it down.
- **Esc** while recording = cancel. The transcript also stays in your clipboard (Cmd+V to paste again).
- Sounds: *pop* = recording, *glass* = pasted, *basso* = error/cancelled.
- A recording auto-stops and transcribes after 10 minutes as a safety net, in case a "stop" tap gets missed.
- Long dictations (a few minutes) now transcribe fine — the old hold-to-talk mode could silently drop most of a long recording if the key state glitched during a long physical hold. Toggle mode (tap-start / tap-stop) doesn't have that failure mode, since nothing needs to stay held.

## Tweaks (top of `voicetype.py`)

- `HOTKEY` — change the trigger key.
- `TOGGLE_MODE = False` — go back to classic hold-to-talk (hold the key, release to stop) instead of tap-to-start/tap-to-stop.
- `MAX_RECORDING_SECONDS` — safety auto-stop for a forgotten toggle (default 10 min).
- `CLEANUP_ENABLED = False` — raw Whisper output, no LLM pass.
- `VOCAB_PROMPT` — add words Whisper should spell correctly (client names, jargon).
- `CLEANUP_SYSTEM_PROMPT` — change the writing style of the output.

## Troubleshooting

- **Nothing pastes**: Accessibility permission missing, or you clicked out of the text box.
- **Hotkey does nothing**: Input Monitoring permission missing → grant, restart Terminal.
- **"No Groq API key found"**: re-run `bash setup.sh` or check `config.json`.
- **429 error**: free-tier rate limit (rare at personal volume) — wait a minute.

## Productization path (later)

This local script can't ship as a web subscription directly. The SaaS version = browser extension or web app (mic via browser) + your server calling the same Groq APIs (paid tier: ~$0.04/hour of audio — margin is huge at $10/mo pricing). The pipeline logic here transfers 1:1.
