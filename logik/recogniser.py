from . import fingerprint as fp
import numpy as np
from tinydb import TinyDB, Query
from collections import defaultdict
from . import songclass as sc
import os

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
  hist, _ = np.histogram(tks, bins=np.arange(int(min(tks)), int(max(tks)) + binwidth + 1, binwidth))
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
      score = score_match(offsets)
      if score > best_score:
          best_score = score
          matched_song = song_id
  return matched_song

def get_matches(hashes, threshhold=5):
    # Adaptation of get_matches() from abracadabra/storage.py
    # hashes = [(hash, offset, id),(hash2, offset 2, id)]
    
    connector = sc.Song.db_connector
    songs = connector.all()
    
    result_dict = defaultdict(list)
    # iterate over songs
    for song in songs:
        #iterate over hash-tuples
        for song_hash, song_offset, songid in song["song_hash"]: # song["song_hash"] = (hash, offset, id)
            #iterate over schnipsel_hash
            for schnipsel_hash, schnipsel_offset, o_o in hashes:
                if schnipsel_hash == song_hash:
                    result_dict[songid].append((song_offset, song_hash))

    return result_dict
