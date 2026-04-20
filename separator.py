import subprocess
import sys
import os

def separate_vocals(input_file: str) -> str:
    """
    Takes an audio file, runs Demucs vocal separation on it,
    and returns the path to the isolated vocals file.
    """

    if not os.path.exists(input_file):
        print(f"Error: file '{input_file}' not found.")
        sys.exit(1)

    print(f"Separating vocals from: {input_file}")
    print("This may take a few minutes depending on song length...")

    # run demucs with two stems (vocals + no_vocals)
    result = subprocess.run([
        "demucs",
        "--two-stems=vocals",
        input_file
    ], capture_output=False)

    if result.returncode != 0:
        print("Demucs failed. Check the output above for details.")
        sys.exit(1)

    # build the output path demucs creates automatically
    song_name = os.path.splitext(os.path.basename(input_file))[0]
    vocals_path = os.path.join("separated", "htdemucs", song_name, "vocals.wav")

    if not os.path.exists(vocals_path):
        print(f"Error: expected vocals file not found at {vocals_path}")
        sys.exit(1)

    print(f"Vocals isolated successfully: {vocals_path}")
    return vocals_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python separator.py <audio_file>")
        print("Example: python separator.py songs/my_song.mp3")
        sys.exit(1)

    input_file = sys.argv[1]
    vocals_path = separate_vocals(input_file)
    print(f"\nDone! Vocals saved to: {vocals_path}")
    print(f"You can now use this file for testing with the lyrics display.")
