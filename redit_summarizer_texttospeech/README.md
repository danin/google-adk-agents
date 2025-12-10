# Reddit Summarizer Text-to-Speech

This project fetches top Reddit posts, summarizes them in a news-anchor style, and can convert the summary to speech using ElevenLabs.

## Agents
- `reddit_fetcher_agent` — fetches top posts for requested subreddits via `get_top_posts`.
- `newscaster_summarizer_agent` — summarizes Reddit headlines.
- `tts_speaker_agent` — converts text to speech via ElevenLabs (voice id required).
- `root_agent` — orchestrates: fetch → summarize → (optional) text-to-speech.

## Requirements
- Python 3.10+
- Dependencies from `requirements.txt`
- API keys:
  - `GOOGLE_API_KEY`
  - `ELEVENLABS_API_KEY`
  - `ELEVENLABS_VOICE_ID` (the actual ElevenLabs voice ID, not the display name)

## Setup
1) Install dependencies:
```bash
pip install -r requirements.txt
```
2) Copy the sample env and fill in keys:
```bash
cp redit_summarizer_texttospeech/sample_env .env
```
Edit `.env` to set:
```
GOOGLE_API_KEY=your_key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=your_voice_id   # e.g., 21m00Tcm4TlvDq8ikWAM
```

## How to run
The file defines `root_agent`. You can run a prompt via Python:
```bash
python - <<'PY'
from redit_summarizer_texttospeech.agent import root_agent
resp = root_agent.run("Fetch top 5 posts from r/news and summarize them.")
print(resp.text)
PY
```

## Notes
- The ElevenLabs call requires a valid `ELEVENLABS_VOICE_ID`; using a display name (e.g., "Will") will fail.
- `output_will_tts.mp3` is written locally when TTS runs.
- `GOOGLE_GENAI_USE_VERTEXAI=FALSE` ensures the Gemini Developer API endpoints are used.
Reditt MCP: https://github.com/adhikasp/mcp-reddit