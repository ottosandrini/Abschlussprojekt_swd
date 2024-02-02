import tinydb
import os
from . import fingerprint as fp


class Song:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'))
    """
    Song Klasse
    kann einen Hash aus einem Song generieren und die Hashes + Songinfo speichern
    """
    def __init__(self, name, file, album, artist, album_art):
        self.name = name
        self.file = file
        self.album = album
        self.artist = artist
        self.album_art = album_art
        self.song_hash = self.fingerprint_file()

    def fingerprint_file(self.file):
        """Generate hashes for a file.

        Given a file, runs it through the fingerprint process to produce a list of hashes from it.

        :param filename: The path to the file.
        :returns: The output of :func:`hash_points`.
        """
        f, t, Sxx = fp.file_to_spectrogram(filename)
        peaks = fp.find_peaks(Sxx)
        peaks = fp.idxs_to_tf_pairs(peaks, t, f)
        return fp.hash_points(peaks, filename)

    def store_data(self):
        print("... storing data")
        self.db_connector.insert(self.__dict__)
        print("... data stored!")
