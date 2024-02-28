import uuid
from tinydb import TinyDB 
import os 
from . import fingerprint as fp
from . import recogniser as rc
class Schnipsel: 
    def __init__(self, file):
        self.db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'))
        self.file = file
        self.schnipselhash = self.fingerprint_audio()

    def fingerprint_audio(self):
        """Generate hashes for a series of audio frames.

        Used when recording audio.

        :param frames: A mono audio stream. Data type is any that ``scipy.signal.spectrogram`` accepts.
        :returns: same as hash_points(): A list of tuples of the form (hash, time offset, song_id)
        """
        f, t, Sxx = fp.file_to_spectrogram(self.file)
        peaks = fp.find_peaks(Sxx)
        peaks = fp.idxs_to_tf_pairs(peaks, t, f)
        return fp.hash_points(peaks, self.file, 1200)
    """
    def check_hashes(self): # code here only for demonstration purposes, will not work like this
        db_hashes = self.db_connnector.getall()
        for i in db_hashes:
            if self.schnipselhash == i:
                print(i)
    """
    def print_hash(self):
        print(self.schnipselhash)

    def recognise_song(self):
        """Recognises a pre-recorded sample.

        Recognises the sample stored at the path ``filename``. The sample can be in any of the
        formats in :data:`recognise.KNOWN_FORMATS`.

        :param filename: Path of file to be recognised.
        :returns: :func:`~abracadabra.recognise.get_song_info` result for matched song or None.
        :rtype: tuple(str, str, str)
        """
        hashes = self.schnipselhash
        amthashes = len(hashes)
        print(f"Amount of matching hashes found: {amthashes}")
        matches = rc.get_matches(hashes)
        amtmatches = len(matches)
        print(f"Amount of matches found: {amtmatches}")
        matched_song = rc.best_match(matches)
        print(matched_song)
        #if info is not None:
        #    return info
        return matched_song
