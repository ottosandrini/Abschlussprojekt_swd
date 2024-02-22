import uuid
from tinydb import TinyDB 
import os 
from . import fingerprint as fp
import numpy as np 
class Schnipsel: 
    def __init__(self, frames):
        self.db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'))
        self.frames = frames
        self.schnipselhash = self.fingerprint_audio()

    def fingerprint_audio(self):
        
        """Generate hashes for a series of audio frames.

        Used when recording audio.

        :param frames: A mono audio stream. Data type is any that ``scipy.signal.spectrogram`` accepts.
        :returns: The output of :func:`hash_points`.
        """
        f, t, Sxx = fp.my_spectrogram(self.frames)
        peaks = fp.find_peaks(Sxx)
        peaks = fp.idxs_to_tf_pairs(peaks, t, f)
        return fp.hash_points(peaks, "recorded")
    
    def check_hashes(self): # code here only for demonstration purposes, will not work like this
        db_hashes = self.db_connnector.getall()
        for i in db_hashes:
            if self.schnipselhash == i:
                print(i)

    def score_match(offsets):
        """Score a matched song.

        Calculates a histogram of the deltas between the time offsets of the hashes from the
        recorded sample and the time offsets of the hashes matched in the database for a song.
        The function then returns the size of the largest bin in this histogram as a score.

        :param offsets: List of offset pairs for matching hashes
        :returns: The highest peak in a histogram of time deltas
        :rtype: int
        """
        # Use bins spaced 0.5 seconds apart
        binwidth = 0.5
        tks = list(map(lambda x: x[0] - x[1], offsets))
        hist, _ = np.histogram(tks,
                            bins=np.arange(int(min(tks)),
                                            int(max(tks)) + binwidth + 1,
                                            binwidth))
        return np.max(hist)


    def best_match(matches):
        """For a dictionary of song_id: offsets, returns the best song_id.

        Scores each song in the matches dictionary and then returns the song_id with the best score.

        :param matches: Dictionary of song_id to list of offset pairs (db_offset, sample_offset)
        as returned by :func:`~abracadabra.Storage.storage.get_matches`.
        :returns: song_id with the best score.
        :rtype: str
        """
        matched_song = None
        best_score = 0
        for song_id, offsets in matches.items():
            if len(offsets) < best_score:
                # can't be best score, avoid expensive histogram
                continue
            score = fp.score_match(offsets)
            if score > best_score:
                best_score = score
                matched_song = song_id
        return matched_song


    def recognise_song(filename):
        """Recognises a pre-recorded sample.

        Recognises the sample stored at the path ``filename``. The sample can be in any of the
        formats in :data:`recognise.KNOWN_FORMATS`.

        :param filename: Path of file to be recognised.
        :returns: :func:`~abracadabra.recognise.get_song_info` result for matched song or None.
        :rtype: tuple(str, str, str)
        """
        hashes = fp.fingerprint_file(filename)
        matches = fp.get_matches(hashes)
        matched_song = fp.best_match(matches)
        info = fp.get_info_for_song_id(matched_song)
        if info is not None:
            return info
        return matched_song