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
      score = fp.score_match(offsets)
      if score > best_score:
          best_score = score
          matched_song = song_id
  return matched_song

def get_matches(hashes, threshhold=5):
    # Adaptation of get_matches() from abracadabra/storage.py

    connector = sc.Song.db_connector
    songs = connector.all()
    result_dict = {}
    # iterate over songs
    for song in songs:
        #iterate over hash-tuples
        for song_hash, song_offset, _ in song["song_hash"]:
            #iterate over schnipsel_hash
            for schnipsel_hash, schnipsel_offset, _ in hashes:
                pass


#    for h, t, _ in hashes:
#        # Query the database for matching hashes
#        matching_hashes = connector.search(Song.song_hash == h)
#        for match in matching_hashes:
#            # Add the match to the result dictionary
#            result_dict[match['name']].append((match['offset'], t))
#    
#    # Filter the results based on the threshold
#    result_dict = {k: v for k, v in result_dict.items() if len(v) > threshold}
#    
    return result_dict

