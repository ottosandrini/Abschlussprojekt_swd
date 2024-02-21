import uuid
import TinyDB
import os 
from . import fingerprint as fp

class Schnipsel: 
    def __init__(self, frames):
        self.db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'))
        self.frames = frames
        self.schnipselhash = self.fingerprint_audio(self.frames)

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
