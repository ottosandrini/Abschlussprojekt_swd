import tinydb
from . import fingerprint as fp


class Song:
    def __init__(self, name, ):
        self.name = name

    def fingerprint_file(filename):
        """Generate hashes for a file.

        Given a file, runs it through the fingerprint process to produce a list of hashes from it.

        :param filename: The path to the file.
        :returns: The output of :func:`hash_points`.
        """
        f, t, Sxx = fp.file_to_spectrogram(filename)
        peaks = fp.find_peaks(Sxx)
        peaks = fp.idxs_to_tf_pairs(peaks, t, f)
        return fp.hash_points(peaks, filename)


    def fingerprint_audio(frames):
        """Generate hashes for a series of audio frames.

        Used when recording audio.

        :param frames: A mono audio stream. Data type is any that ``scipy.signal.spectrogram`` accepts.
        :returns: The output of :func:`hash_points`.
        """
        f, t, Sxx = fp.my_spectrogram(frames)
        peaks = fp.find_peaks(Sxx)
        peaks = fp.idxs_to_tf_pairs(peaks, t, f)
        return fp.hash_points(peaks, "recorded")

