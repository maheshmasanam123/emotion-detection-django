"""Mood journeys: ordered playlists that gently transition the user's mood.

Idea: don't just match the detected mood — guide it. A sad user gets a playlist
that opens with empathetic songs, then motivational, then upbeat. An angry user
is brought down through calm and chill to happy.
"""
from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

# detected_emotion -> sequence of mood phases the playlist will pass through.
MOOD_JOURNEYS: dict[str, list[str]] = {
    "sad":     ["sad", "motivation", "uplift", "happy"],
    "angry":   ["angry", "calm", "chill", "happy"],
    "neutral": ["neutral", "uplift", "happy"],
    "happy":   ["happy", "chill", "party"],
}

# Friendly captions shown alongside each phase in the UI.
PHASE_CAPTIONS: dict[str, str] = {
    "angry":      "Let it out",
    "calm":       "Cooling down",
    "chill":      "Chilling",
    "sad":        "Sitting with it",
    "motivation": "Picking it up",
    "uplift":     "Rising",
    "happy":      "Feeling good",
    "neutral":    "Steady",
    "party":      "Celebrate",
}

DEFAULT_PHASE_SONG_COUNT = 4


def get_journey(detected_emotion: str) -> list[str]:
    """Return the mood-phase sequence for a detected emotion."""
    return MOOD_JOURNEYS.get(detected_emotion, [detected_emotion])


def caption_for(phase: str) -> str:
    return PHASE_CAPTIONS.get(phase, phase.title())


# ---------------------------------------------------------------------------
# External-URL helpers (YouTube / Spotify / SoundCloud embeds)
# ---------------------------------------------------------------------------

_YT_ID_RE = re.compile(r"(?:v=|youtu\.be/|/embed/|/shorts/)([\w-]{11})")


def youtube_embed_url(url: str) -> str | None:
    """Convert any YouTube URL to an embed URL with autoplay."""
    match = _YT_ID_RE.search(url)
    if match:
        return f"https://www.youtube.com/embed/{match.group(1)}?autoplay=1&rel=0"
    parsed = urlparse(url)
    if "youtube.com" in parsed.netloc:
        qs = parse_qs(parsed.query)
        vid = qs.get("v", [None])[0]
        if vid:
            return f"https://www.youtube.com/embed/{vid}?autoplay=1&rel=0"
    return None


def spotify_embed_url(url: str) -> str | None:
    """Convert a Spotify track/playlist URL to its embed form."""
    parsed = urlparse(url)
    if "spotify.com" not in parsed.netloc:
        return None
    path = parsed.path
    if path.startswith("/embed/"):
        return url
    return f"https://open.spotify.com/embed{path}"


def soundcloud_embed_url(url: str) -> str:
    return (
        "https://w.soundcloud.com/player/?url="
        + url
        + "&auto_play=true&hide_related=true&visual=false"
    )


def embed_for(song) -> str | None:
    """Return an iframe-ready embed URL for a song's external link, or None."""
    if not getattr(song, "external_url", None):
        return None
    if song.source == "youtube":
        return youtube_embed_url(song.external_url)
    if song.source == "spotify":
        return spotify_embed_url(song.external_url)
    if song.source == "soundcloud":
        return soundcloud_embed_url(song.external_url)
    return None
