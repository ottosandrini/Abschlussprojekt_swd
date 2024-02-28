from tinydb import TinyDB, Query
import os
from . import fingerprint as fp


class Song:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'))
    query = Query()
    """
    Song Klasse
    kann einen Hash aus einem Song generieren und die Hashes + Songinfo speichern
    """
    def __init__(self, name, file, album, artist, album_art, song_id):
        self.name = name
        self.file = file
        self.album = album
        self.artist = artist
        self.album_art = album_art
        self.song_id = song_id
        self.song_hash = self.fingerprint_file()

    def fingerprint_file(self):
        """Generate hashes for a file.

        Given a file, runs it through the fingerprint process to produce a list of hashes from it.

        :param filename: The path to the file.
        :returns: The output of :func:`hash_points`.
        """
        f, t, Sxx = fp.file_to_spectrogram(self.file)
        peaks = fp.find_peaks(Sxx)
        peaks = fp.idxs_to_tf_pairs(peaks, t, f)
        return fp.hash_points(peaks, self.file, self.song_id)

    def store_data(self):
        print("... storing data")
        self.db_connector.insert(self.__dict__)
        print("... data stored!")

    @classmethod
    def cleardb(cls):
        # removes all songs from database
        Song.db_connector.truncate()

    @classmethod
    def get_song_name_by_id(cls, sid):
        # Retrieve song name from the database based on the provided song_id

        song_data = cls.db_connector.search(cls.query.song_id == sid)
        if song_data:
            return song_data[0]['name']
        else:
            return None
