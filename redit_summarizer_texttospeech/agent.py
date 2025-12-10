
import os
from typing import List, Dict

import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai import types


load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")  # must be a valid ElevenLabs voice_id


def get_top_posts(subreddits: List[str], limit: int = 5) -> Dict[str, List[Dict[str, str]]]:
    """
    For each subreddit in `subreddits`, return up to `limit` top posts of the day.
    Returns a dict: {subreddit_name: [{title, link}, ...], ...}
    """
    results: Dict[str, List[Dict[str, str]]] = {}
    headers = {"User-Agent": "my-simple-script/0.1 by your_name"}

    for subreddit in subreddits:
        url = f"https://www.reddit.com/r/{subreddit}/top.json"
        params = {"t": "day", "limit": limit}
        resp = requests.get(url, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        posts: List[Dict[str, str]] = []
        for child in data.get("data", {}).get("children", []):
            post_data = child.get("data", {})
            title = post_data.get("title", "")
            link = "https://www.reddit.com" + post_data.get("permalink", "")
            posts.append({"title": title, "link": link})
        results[subreddit] = posts

    return results


get_top_posts_tool = FunctionTool(get_top_posts)


reddit_fetcher_agent = Agent(
    name="reddit_fetcher_agent",
    description="Fetches top Reddit posts from specified subreddits.",
    model="gemini-2.0-flash",
    instruction=(
        "You are a Reddit data fetcher. "
        "When asked to fetch Reddit posts, use the get_top_posts tool to retrieve the top posts "
        "from the specified subreddits. Return the results in a clear, organized format."
    ),
    tools=[get_top_posts_tool],
)


summarizer_agent = Agent(
    name="newscaster_summarizer_agent",
    description="Summarizes a list of Reddit post titles in a newscaster style.",
    model="gemini-2.0-flash",
    instruction=(
        "You are a news anchor summarizing Reddit headlines. "
        "Given a list of post titles, provide a concise, engaging summary in a professional newscaster style. "
        "Highlight key themes or interesting points found only in the titles. "
        "Start with an anchor intro like 'Here are today's top stories from the subreddit...' or similar. "
        "Refer to subreddits by name, no need to mention 'r/'."
    ),
    tools=[],
)


def text_to_speech_will(text: str) -> str:
    """
    Convert text to speech using ElevenLabs.
    Returns the local file path of the generated audio.
    """

    ELEVENLABS_VOICE_ID = "weA4Q36twV5kwSaTEL0Q"
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY is not set")
    if not ELEVENLABS_VOICE_ID:
        raise RuntimeError("ELEVENLABS_VOICE_ID is not set (use a valid ElevenLabs voice_id)")

    voice_id = ELEVENLABS_VOICE_ID  # must be a valid ElevenLabs voice_id, not the display name
    model_id = "eleven_multilingual_v2"
    output_path = "output_will_tts.mp3"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": model_id,
    }

    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(resp.content)

    return output_path


tts_tool = FunctionTool(text_to_speech_will)


tts_agent = Agent(
    name="tts_speaker_agent",
    description="Converts provided text into speech using ElevenLabs TTS.",
    instruction=(
        "You are a Text-to-Speech agent. Convert user text to speech audio files.\n\n"
        "IMPORTANT FORMATTING RULES:\n"
        "1. Always use the text_to_speech_will tool (voice 'Will').\n"
        "2. When the tool returns a file path, format your response like this example:\n"
        "   \"I've converted your text to speech. The audio file is saved at `/path/to/file.mp3`\"\n"
        "3. Put ONLY the file path inside backticks (`), not any additional text.\n"
        "4. Never modify or abbreviate the path.\n\n"
        "This exact format is critical for proper processing."
    ),
    model="gemini-2.0-flash",
    tools=[tts_tool],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=250,
    ),
)


root_agent = Agent(
    name="redit_summarizer_texttospeech",
    model="gemini-2.0-flash",
    description="Fetches Reddit posts, summarizes them, and can convert summaries to speech.",
    instruction=(
        "You are a helpful assistant that can fetch Reddit posts and summarize them. "
        "Use the reddit_fetcher_agent to get posts, then use the summarizer_agent to create summaries. "
        "When audio is requested, delegate to tts_speaker_agent."
    ),
    tools=[],
    sub_agents=[reddit_fetcher_agent, summarizer_agent, tts_agent],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=2050,
    ),
)