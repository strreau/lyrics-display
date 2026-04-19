import threading
import sys
import os
import config
from matcher import LyricsMatcher
from recognizer import Recognizer
from display import LyricsDisplay

def load_lyrics(song_filename: str) -> list[str]:
    """Load a lyrics file from the songs directory, one line per line."""
    path = os.path.join(config.SONGS_DIR, song_filename)
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        # filter out empty lines
        return [line for line in lines if line]

def main():
    # ── 1. Load song ─────────────────────────────────────────
    if len(sys.argv) < 2:
        print("Usage: python main.py <song_filename>")
        print("Example: python main.py example_song.txt")
        sys.exit(1)

    song_file = sys.argv[1]
    lyrics = load_lyrics(song_file)
    print(f"Loaded {len(lyrics)} lines from {song_file}")

    # ── 2. Set up components ─────────────────────────────────
    matcher = LyricsMatcher(lyrics)
    display = LyricsDisplay()

    # ── 3. Define what happens when speech is recognized ─────
    def on_transcribed(text: str):
        matched_line = matcher.match(text)
        if matched_line:
            display.update(matched_line)

    # ── 4. Run recognizer in background thread ───────────────
    recognizer = Recognizer(callback=on_transcribed)
    mic_thread = threading.Thread(target=recognizer.start, daemon=True)
    mic_thread.start()

    # ── 5. Run display on main thread ────────────────────────
    print("Display running — press ESC to quit")
    while display.running:
        display.render()

    # ── 6. Clean up ──────────────────────────────────────────
    recognizer.stop()
    display.close()
    print("Stopped.")

if __name__ == "__main__":
    main()
