from datetime import datetime
import logging


class GMSongsCache:

    def __init__(self, logger=None):
        self.logger = logging.getLogger('GMSongsCache') if logger is None else logger
        self.cache = []
        self.index = {}
        self.last_update = datetime(1970, 1, 1)

    def add_song(self, song):
        the_key = self.index_if_needed(song.get('id'), song)
        the_key = self.index_if_needed(song.get('nid'), song, the_key)
        self.index_if_needed(song.get('storeId'), song, the_key)

    def index_if_needed(self, idx_key, song, known_key=None):
        if not idx_key:
            return None
        song_idx = self.index.get(idx_key)
        if not song_idx:
            if known_key is not None:
                song_idx = known_key
            else:
                # new item
                song_idx = len(self.cache)
                self.cache[song_idx:] = [song]
            self.logger.debug("self.cache length %s idx: %s", len(self.cache), song_idx)
            self.index[idx_key] = song_idx
        else:
            self.cache[song_idx] = song
        return song_idx

    def add_all_songs(self, all_songs):
        for song in all_songs:
            self.add_song(song)
        self.last_update = datetime.now()

    def lookup_song(self, id):
        cache_idx = self.index.get(id, -1)
        if cache_idx != -1:
            song = self.cache[cache_idx]
            return song.copy()

    def get_last_update(self):
        return self.last_update
