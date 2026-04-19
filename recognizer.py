import sounddevice as sd
import vosk
import queue
import json
import config

class Recognizer:
    def __init__(self, callback):
        """
        callback: a function that receives transcribed text
        e.g. def on_text(text): print(text)
        """
        self.model = vosk.Model(config.VOSK_MODEL_PATH)
        self.recognizer = vosk.KaldiRecognizer(self.model, config.SAMPLE_RATE)
        self.audio_queue = queue.Queue()
        self.callback = callback
        self.running = False

    def _audio_callback(self, indata, frames, time, status):
        """Called by sounddevice for each audio chunk from the mic."""
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(bytes(indata))

    def start(self):
        """Start listening to the mic and transcribing."""
        self.running = True
        print("Listening...")

        with sd.RawInputStream(
            samplerate=config.SAMPLE_RATE,
            blocksize=8000,
            device=config.MIC_DEVICE_INDEX,
            dtype="int16",
            channels=config.CHANNELS,
            callback=self._audio_callback
        ):
            while self.running:
                data = self.audio_queue.get()

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print(f"Recognized: {text}")
                        self.callback(text)
                else:
                    # partial result — useful for faster matching
                    partial = json.loads(self.recognizer.PartialResult())
                    text = partial.get("partial", "").strip()
                    if text:
                        print(f"Partial: {text}")
                        self.callback(text)

    def stop(self):
        """Stop listening."""
        self.running = False
