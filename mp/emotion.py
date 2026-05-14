"""Emotion classifier.

Wraps DeepFace (which itself wraps several pretrained models) and maps its
seven-class output down to the four classes we care about: angry, happy,
neutral, sad.

If DeepFace is unavailable the predictor falls back to a deterministic stub so
the web app still runs end-to-end during development.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, Tuple

TARGET_CLASSES = ("angry", "happy", "neutral", "sad")

# DeepFace's seven classes -> our four. Disgust and fear collapse to angry/sad,
# surprise collapses to happy (positive arousal).
DEEPFACE_TO_TARGET = {
    "angry": "angry",
    "disgust": "angry",
    "fear": "sad",
    "happy": "happy",
    "sad": "sad",
    "surprise": "happy",
    "neutral": "neutral",
}


def _collapse_scores(scores: Dict[str, float]) -> Dict[str, float]:
    out = {cls: 0.0 for cls in TARGET_CLASSES}
    for label, value in scores.items():
        target = DEEPFACE_TO_TARGET.get(label.lower())
        if target:
            out[target] += float(value)
    total = sum(out.values()) or 1.0
    return {k: round(v / total, 4) for k, v in out.items()}


def _stub_predict(image_path: str) -> Tuple[str, float, Dict[str, float]]:
    """Deterministic fallback so the UI still works without DeepFace installed."""
    digest = hashlib.md5(Path(image_path).read_bytes()).digest()
    weights = [digest[i] + 1 for i in range(4)]
    total = sum(weights)
    scores = {cls: round(w / total, 4) for cls, w in zip(TARGET_CLASSES, weights)}
    top = max(scores, key=scores.get)
    return top, scores[top], scores


def predict_emotion(image_path: str) -> Tuple[str, float, Dict[str, float]]:
    """Return (label, confidence in [0,1], full score dict).

    Falls back to a stub predictor if DeepFace isn't installed or face
    detection fails.
    """
    try:
        from deepface import DeepFace  # type: ignore
    except ImportError:
        return _stub_predict(image_path)

    try:
        result = DeepFace.analyze(
            img_path=image_path,
            actions=["emotion"],
            enforce_detection=False,
            silent=True,
        )
    except Exception:
        return _stub_predict(image_path)

    if isinstance(result, list):
        if not result:
            return _stub_predict(image_path)
        result = result[0]

    raw_scores = result.get("emotion") or {}
    collapsed = _collapse_scores(raw_scores)
    if not any(collapsed.values()):
        return _stub_predict(image_path)
    top = max(collapsed, key=collapsed.get)
    return top, collapsed[top], collapsed
