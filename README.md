# FaceMood — Django Emotion Classifier

A Django web app that classifies a face photo as **angry / happy / neutral / sad** using a pretrained facial-emotion model (DeepFace). Users sign up, upload a photo, and instantly see the predicted emotion with confidence scores and a per-class breakdown. All past predictions are saved to a per-user history.

> Final-year college project — Computer Science.

## Features

- User authentication (signup, login, logout)
- Image upload with on-the-spot emotion prediction
- 4-class output (angry / happy / neutral / sad) with confidence bars
- Per-user prediction history with thumbnails
- Django admin panel for viewing/managing all predictions
- Graceful fallback predictor when DeepFace can't run (so the UI is never broken)

## Tech stack

| Layer    | Tool                                        |
|----------|---------------------------------------------|
| Backend  | Django 4.2+                                 |
| Database | SQLite (zero-config)                        |
| ML       | DeepFace (wraps TensorFlow/Keras)           |
| Frontend | Bootstrap 5                                 |
| Language | Python 3.10+                                |

## Quick start (anyone can run this in 3 steps)

### Prerequisites
Install **Python 3.10 or newer** from https://www.python.org/downloads/
(On Windows, tick **"Add Python to PATH"** during install.)

### 1. Clone the repo
```bash
git clone https://github.com/<YOUR-USERNAME>/<REPO-NAME>.git
cd <REPO-NAME>
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
1. Create a virtual environment in `.venv/`
2. Install all dependencies from `requirements.txt`
3. Run database migrations
4. Start the dev server at **http://127.0.0.1:8000/**

### 3. Use the app
1. Open http://127.0.0.1:8000/ in your browser
2. Click **Signup** → create an account
3. Click **Predict** → upload a face photo
4. See the emotion prediction with confidence breakdown

That's it. 🎉

## Manual setup (if scripts don't work)

```bash
python -m venv .venv
# Windows:   .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional — for admin access
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
├── mp/                     # main app
│   ├── models.py           # Prediction model
│   ├── views.py            # upload, result, history
│   └── emotion.py          # DeepFace wrapper → 4-class output
├── templates/              # HTML (Bootstrap 5)
├── static/css/             # styles
├── media/uploads/          # user uploads (gitignored)
└── dataset/                # optional reference images for the 4 classes
```

## How the prediction works

`mp/emotion.py` calls `DeepFace.analyze(actions=["emotion"])`, which returns scores across DeepFace's 7 emotions. We collapse them into our 4 target classes:

| DeepFace class    | Mapped to   |
|-------------------|-------------|
| angry, disgust    | **angry**   |
| fear, sad         | **sad**     |
| happy, surprise   | **happy**   |
| neutral           | **neutral** |

If DeepFace is unavailable or face detection fails, a deterministic stub predictor is used so the UI keeps working.

## Notes

- The first DeepFace prediction downloads model weights (~5 MB) — cached at `~/.deepface/` afterwards, so subsequent runs are fast.
- Uploaded photos are stored under `media/uploads/` and gitignored — they stay on your machine.
- `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` are environment-variable configurable for deployment.
- Admin panel: http://127.0.0.1:8000/admin/ (login with the superuser you created).

## Troubleshooting

| Issue                                       | Fix                                                                  |
|---------------------------------------------|----------------------------------------------------------------------|
| `python` is not recognized                  | Reinstall Python with **"Add to PATH"** ticked                       |
| DeepFace install fails on Windows           | Run `pip install --upgrade pip` first, then `pip install -r requirements.txt` |
| "No face detected"                          | The stub predictor will still return a result; use a clearer photo for real predictions |
| Port 8000 already in use                    | Run `python manage.py runserver 8080`                                |

## License

MIT
