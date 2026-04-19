from rapidfuzz import fuzz
import config

class LyricsMatcher:
    def __init__(self, lyrics: list[str]):
        """
        lyrics: a list of strings, one per line
        e.g. ["Amazing grace how sweet the sound",
               "That saved a wretch like me"]
        """
        self.lyrics = lyrics
        self.current_index = 0  # where we are in the song

    def match(self, transcribed_text: str) -> str | None:
        """
        Takes transcribed speech, fuzzy matches it against the
        next WINDOW_SIZE lines, returns the best matching line
        or None if no match is confident enough.
        """
        if self.current_index >= len(self.lyrics):
            return None  # end of song

        # only look ahead within the window, never backwards
        window_end = min(self.current_index + config.WINDOW_SIZE, len(self.lyrics))
        window = self.lyrics[self.current_index:window_end]

        best_score = 0
        best_index = None

        for i, line in enumerate(window):
            score = fuzz.partial_ratio(
                transcribed_text.lower(),
                line.lower()
            )
            if score > best_score:
                best_score = score
                best_index = i

        # only advance if we're confident enough
        if best_score >= config.MATCH_THRESHOLD and best_index is not None:
            self.current_index += best_index + 1
            return self.lyrics[self.current_index - 1]

        return None  # not confident enough, hold current slide

    def current_line(self) -> str | None:
        """Returns the currently displayed lyric line."""
        if self.current_index == 0:
            return None
        return self.lyrics[self.current_index - 1]

    def reset(self):
        """Reset to the beginning of the song."""
        self.current_index = 0
