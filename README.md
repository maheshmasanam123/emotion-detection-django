# FaceMood Music — Mood-Based Music Player

A Django web app that **detects emotion from a face photo** and **plays matching music**. Upload a selfie, the app classifies your mood as *angry / happy / neutral / sad* using a pretrained facial-emotion model (DeepFace), then instantly streams a playlist tagged with that mood.

> Final-year college project — Computer Science.

## Features

- 📸 **Face → emotion detection** using DeepFace (pretrained, no training needed)
- 🎵 **Mood-tagged music library** — songs in admin tagged with `angry / happy / neutral / sad`
- ▶️ **Auto-playing music player** with Prev / Next / Shuffle controls and clickable playlist
- 🔐 User auth (signup, login, logout)
- 📚 **Library page** browsing songs by mood
- 🕓 Per-user prediction history
- 🛠 Django admin panel for uploading songs and viewing predictions
- 🪂 Graceful fallback predictor when DeepFace isn't installed (UI keeps working)

## Tech stack

| Layer    | Tool                                |
|----------|-------------------------------------|
| Backend  | Django 4.2+                         |
| Database | SQLite (zero-config)                |
| ML       | DeepFace (wraps TensorFlow / Keras) |
| Audio    | HTML5 `<audio>` (MP3 streaming)     |
| Frontend | Bootstrap 5                         |
| Language | Python 3.10+                        |

## Quick start (anyone can run this in 3 steps)

### Prerequisites
Install **Python 3.10 or newer** from https://www.python.org/downloads/
(On Windows, tick **"Add Python to PATH"** during install.)

### 1. Clone the repo
```bash
git clone https://github.com/<YOUR-USERNAME>/emotion-detection-django.git
cd emotion-detection-django
```

### 2. Run the setup script
**Windows:**
```bat
setup.bat
```
**macOS / Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

The script will:
1. Create a virtualenv in `.venv/`
2. Install all dependencies
3. Run database migrations
4. Start the dev server at **http://127.0.0.1:8000/**

### 3. Add some songs and try it

1. Create an admin user (in a second terminal, with the venv activated):
   ```bash
   python manage.py createsuperuser
   ```
2. Open http://127.0.0.1:8000/admin/ → log in → **Songs** → **Add song**
3. Upload an MP3, give it a title/artist, and pick a mood (`angry / happy / neutral / sad`)
4. Add at least one song per mood for the best experience.
5. Go back to http://127.0.0.1:8000/, sign up as a regular user, click **Detect & Play**, and upload a face photo.

🎉 The app will detect your mood and start playing the matching playlist instantly.

## Manual setup (if scripts don't work)

```bash
python -m venv .venv
# Windows:    .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # for admin / uploading songs
python manage.py runserver
```

## Project structure

```
.
├── manage.py
├── setup.bat / setup.sh    # one-click setup
├── requirements.txt
├── config/                 # Django project (settings, urls, wsgi)
├── accounts/               # signup, login, logout
├── mp/                     # main app (music player)
│   ├── models.py           # Song + Prediction models
│   ├── views.py            # upload, result (player), library, history
│   ├── emotion.py          # DeepFace wrapper → 4-class output
│   └── admin.py            # song management
├── templates/              # HTML (Bootstrap 5)
├── static/css/             # styles
├── media/
│   ├── songs/              # uploaded audio (gitignored)
│   ├── covers/             # song cover art (gitignored)
│   └── uploads/            # user-uploaded face photos (gitignored)
└── dataset/                # optional reference images for the 4 mood classes
```

## How it works

1. **Upload** — user uploads a face photo on `/upload/`.
2. **Predict** — `mp/emotion.py` calls `DeepFace.analyze(actions=["emotion"])`. DeepFace returns scores for 7 emotions; we collapse them into 4 target moods:

   | DeepFace class    | Mapped to   |
   |-------------------|-------------|
   | angry, disgust    | **angry**   |
   | fear, sad         | **sad**     |
   | happy, surprise   | **happy**   |
   | neutral           | **neutral** |

3. **Match** — the view queries `Song.objects.filter(mood=predicted_mood)` and shuffles up to 20 results.
4. **Play** — the result page renders an HTML5 audio player that auto-plays the first track and queues the rest, with Prev / Next / Shuffle controls.

If DeepFace is missing or face detection fails, a deterministic stub predictor returns a plausible mood so the UI never breaks.

## Adding music

Songs are managed through the Django admin (`/admin/mp/song/add/`). Each song has:

- **Title** (required)
- **Artist** (optional)
- **Mood** — one of `angry / happy / neutral / sad`
- **Audio file** — MP3 / OGG / WAV
- **Cover image** (optional)

Tip: bulk-add by uploading MP3s to `media/songs/` first, then creating Song records pointing at them.

## Notes

- First DeepFace call downloads model weights (~5 MB), cached at `~/.deepface/`.
- All uploaded media is stored under `media/` and gitignored — content stays on your machine.
- `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` are environment-variable configurable for deployment.
- Browser auto-play policies may require the user to interact with the page once before audio starts.

## Troubleshooting

| Issue                                  | Fix                                                                  |
|----------------------------------------|----------------------------------------------------------------------|
| `python` is not recognized             | Reinstall Python with **"Add to PATH"** ticked                       |
| DeepFace install fails on Windows      | `pip install --upgrade pip` first, then `pip install -r requirements.txt` |
| "No songs for this mood"               | Add songs in admin and tag them with the mood                        |
| Audio doesn't auto-play                | Browser policy — click anywhere on the page once, then it'll play    |
| Port 8000 already in use               | `python manage.py runserver 8080`                                    |

## License

MIT
