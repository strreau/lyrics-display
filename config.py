# ── Audio Input ──────────────────────────────────────────────
MIC_DEVICE_INDEX = None   # None = system default, change to int if needed
SAMPLE_RATE = 16000       # Vosk works best at 16kHz
CHANNELS = 1              # Mono input

# ── Speech Recognition ───────────────────────────────────────
VOSK_MODEL_PATH = "models/vosk-model-spanish"  # Path to downloaded Vosk model

# ── Fuzzy Matching ───────────────────────────────────────────
MATCH_THRESHOLD = 65      # Minimum match score (0-100) to advance a slide
WINDOW_SIZE = 5           # How many lines ahead to search for a match

# ── Display ──────────────────────────────────────────────────
FONT_SIZE = 72
FONT_COLOR = (255, 255, 255)       # White
BACKGROUND_COLOR = (0, 0, 0)      # Black
SCREEN_INDEX = 0                   # 0 = primary, 1 = second monitor
FULLSCREEN = True

# ── Songs ────────────────────────────────────────────────────
SONGS_DIR = "songs"
