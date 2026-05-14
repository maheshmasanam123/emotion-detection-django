# FaceMood Music — Live Mood Detection & Music Journey

A Django web app that **detects your emotion live from the webcam** and plays a **mood-journey playlist** — songs that meet you where you are emotionally and gradually lift you to where you want to be. Music can be uploaded files **or** YouTube / Spotify / SoundCloud links.

> Final-year college project — Computer Science.

## ✨ Highlights

- 📷 **Live webcam detection** — opens your camera, captures a frame, predicts your mood with DeepFace. No file upload needed.
- 🎵 **Mood-journey playlists** — instead of just matching your mood, the app *guides* it:
  - **Sad** → Motivation → Uplift → Happy
  - **Angry** → Calm → Chill → Happy
  - **Happy** → Chill → Party
  - **Neutral** → Uplift → Happy
- 🔗 **Bring any music** — local MP3 uploads **or** YouTube / Spotify / SoundCloud links, embedded inline with auto-advance.
- 🔐 User auth + per-user prediction history.
- 🛠 Django admin to manage songs and view all predictions.
- 🪂 Graceful fallback if DeepFace isn't installed (stub predictor keeps the UI working).

## 🎬 How a user experiences it

1. **Click "📷 Live"** in the navbar.
2. Browser asks for camera permission → live video appears.
3. Click **Auto-detect (3s countdown)** or **Detect now**.
4. The app captures a frame, classifies emotion (angry / happy / neutral / sad), and redirects to the player.
5. The player loads a **mood-journey playlist** with phase badges (e.g. `Sad → Motivation → Uplift → Happy`) and starts playing the first track — local audio or embedded YouTube/Spotify iframe.
6. Auto-advance, Shuffle, Prev/Next controls — all built-in.

## Tech stack

| Layer    | Tool                                                                   |
|----------|------------------------------------------------------------------------|
| Backend  | Django 4.2+                                                            |
| Database | SQLite (zero-config)                                                   |
| ML       | DeepFace (pretrained — wraps TensorFlow/Keras)                         |
| Camera   | Browser `getUserMedia` API → POST base64 frame to Django               |
| Audio    | HTML5 `<audio>` (local files) + YouTube / Spotify / SoundCloud iframes |
| Frontend | Bootstrap 5, vanilla JS                                                |
| Language | Python 3.10+                                                           |

## 🚀 Quick start

### Prerequisites
Install **Python 3.10+** from https://www.python.org/downloads/
(Windows: tick **"Add Python to PATH"** during install.)

### 1. Clone
```bash
git clone https://github.com/<YOUR-USERNAME>/emotion-detection-django.git
cd emotion-detection-django
```

### 2. Run setup
**Windows:** `setup.bat`
**macOS / Linux:** `chmod +x setup.sh && ./setup.sh`

The script: creates a virtualenv → installs deps → migrates DB → starts the server at http://127.0.0.1:8000/

### 3. Add songs & try it

In a second terminal (venv active):
```bash
python manage.py createsuperuser
```

1. Visit http://127.0.0.1:8000/admin/ → log in → **Songs** → **Add song**
2. For each song:
   - **Title**, **Artist** (optional), **Mood** (pick one of *angry / calm / chill / sad / motivation / uplift / happy / neutral / party*)
   - Either upload an **audio file** OR paste an **external URL** (YouTube, Spotify, or SoundCloud)
3. Add a few songs across the moods listed in [Mood journeys](#-mood-journeys) so playlists are non-empty.
4. Visit http://127.0.0.1:8000/, sign up as a regular user, click **📷 Live**, allow camera access — the app detects your mood and starts the journey. 🎉

> 💡 **Camera tip:** Modern browsers require HTTPS or `localhost` for camera access. `127.0.0.1` and `localhost` both work locally. For deployment, you'll need HTTPS.

## 🗺️ Mood journeys

Defined in [`mp/journey.py`](mp/journey.py):

| Detected emotion | Journey                                |
|------------------|----------------------------------------|
| **Sad**          | sad → motivation → uplift → happy      |
| **Angry**        | angry → calm → chill → happy           |
| **Happy**        | happy → chill → party                  |
| **Neutral**      | neutral → uplift → happy               |

The view picks ~4 songs per phase, in order, so the playlist transitions naturally.

## 📁 Project structure

```
.
├── manage.py
├── setup.bat / setup.sh    # one-click setup
├── requirements.txt
├── config/                 # Django project (settings, urls, wsgi)
├── accounts/               # signup, login, logout
├── mp/                     # main app
│   ├── models.py           # Song (with external URL) + Prediction
│   ├── views.py            # live, upload, result, library, history, predict-frame API
│   ├── emotion.py          # DeepFace wrapper → 4-class output
│   ├── journey.py          # mood-journey definitions + YouTube/Spotify embed helpers
│   └── admin.py
├── templates/
│   ├── base.html
│   ├── accounts/           # login, signup
│   └── mp/                 # home, live (webcam), upload, result (player), library, history
├── static/css/
└── media/                  # uploaded audio, covers, face images (gitignored)
```

## 🔬 How prediction works

1. **Capture** — `templates/mp/live.html` uses `navigator.mediaDevices.getUserMedia` to access the webcam, draws a frame to a `<canvas>`, and serialises it as a base64 JPEG data URL.
2. **POST** — sends the data URL to `POST /api/predict-frame/` (CSRF-protected).
3. **Predict** — `mp/emotion.py` calls `DeepFace.analyze(actions=["emotion"])`. DeepFace returns 7 emotion scores; we collapse them to 4 target classes:

   | DeepFace          | Mapped to   |
   |-------------------|-------------|
   | angry, disgust    | **angry**   |
   | fear, sad         | **sad**     |
   | happy, surprise   | **happy**   |
   | neutral           | **neutral** |

4. **Journey** — `mp/journey.py` maps the detected mood to its phase sequence, and the result view queries `Song.objects.filter(mood=phase)` for each phase.
5. **Play** — `result.html` renders an HTML5 `<audio>` for local files or a YouTube/Spotify/SoundCloud `<iframe>` for external URLs. Auto-advances to the next track on `ended`.

## 🧰 Adding songs

Songs are managed in the Django admin. Each Song needs:

- **Title** (required), **Artist** (optional)
- **Mood** — pick from the 9 mood tags
- **Either** an uploaded audio file **or** an external URL (YouTube / Spotify / SoundCloud — auto-detected on save)
- **Cover image** (optional)

You can mix sources freely — a single playlist phase can contain MP3s, YouTube videos, and Spotify tracks side-by-side.

## ⚠️ Notes

- First DeepFace prediction downloads model weights (~5 MB), cached at `~/.deepface/`.
- Browser autoplay policies may require one user click before audio plays.
- All uploaded media is gitignored — content stays local.
- Camera access requires HTTPS in production (works on `localhost` for dev).

## 🛠️ Troubleshooting

| Issue                              | Fix                                                                  |
|------------------------------------|----------------------------------------------------------------------|
| Camera permission denied           | Allow camera in your browser's site settings, then reload            |
| `python` not recognized            | Reinstall Python with **"Add to PATH"** ticked                       |
| DeepFace install fails             | `pip install --upgrade pip` then re-run                              |
| "No songs for this mood"           | Add songs in admin tagged with the missing mood                      |
| YouTube embed shows "Video unavailable" | The video has embedding disabled; try another link              |
| Port 8000 in use                   | `python manage.py runserver 8080`                                    |

## License

MIT
