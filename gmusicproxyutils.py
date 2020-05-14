import logging
import json
import urllib.parse as uparse
from datetime import datetime, timezone
from xml.sax.saxutils import escape

# Constants
REQ_TYPE = 'REQUEST_TYPE'
REQ_PATH = 'REQUEST_PATH'
REQ_URIINFO = 'REQUEST_URI'

XSPF_MIME = "application/xspf+xml"
M3U_MIME = "audio/mpegurl"
JSON_MIME = "application/json"
TXT_MIME = "text/plain"


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


class PlaylistMeta:
    BASE_URL = "http://%s/get_%s"

    def __init__(self, host_and_port, api_call, params):
        self.base_url = self.BASE_URL % (host_and_port, api_call)
        self.api_call = api_call
        self.params = params
        self.host_and_port = host_and_port
        self.format = params.get('format', ['m3u'])[0].lower().strip()
        if self.format == 'text':
            self.format = 'txt'
        self.base_params = {} if api_call == 'song' else {"format":self.format}

    def get_file_name(self):
        print(self.params[REQ_URIINFO])
        return self.params[REQ_URIINFO].path.replace('/', '') + "." + self.format

    def get_gmp_url(self, g_id, record):
        qs_params = record.get("qstring", {})
        qs_params["id"] = g_id
        qs_params.update(self.base_params)
        q_string = uparse.urlencode(qs_params)
        return f'{self.base_url}?{q_string}'


class TextWriter:

    def __init__(self, p_meta):
        self.p_meta = p_meta
        self.separator = p_meta.params.get('separator', ['|'])[0]
        self.only_url = p_meta.params.get('only_url', ['no'])[0].lower().strip() == 'yes'
        self.key_format_lookup = {
            'album':   TextWriter._album_formatter,
            'default': TextWriter._default_formatter
        }

    def generate(self, results):
        playlist = []
        kf_pair = self.key_format_lookup.get(self.p_meta.api_call, self.key_format_lookup['default'])
        formatter = kf_pair if not self.only_url else TextWriter._empty_formatter
        for r_id, result in results:
            playlist.append('%s%s' % (formatter(self, result), self.p_meta.get_gmp_url(r_id, result)))
        rendered = '\n'.join(playlist)
        return TXT_MIME, self.p_meta.get_file_name(), rendered

    def _album_formatter(self, album):
        album_format = '%s%s%s%s' % (album['name'], self.separator, album['year'], self.separator) if (
                'name' in album and 'year' in album and not self.only_url) else ''
        return album_format

    def _empty_formatter(self, record):
        return ''

    def _default_formatter(self, result):
        record_format = '%s%s' % (result['name'], self.separator) if ('name' in result) else ''
        return record_format


class M3UWriter:

    def __init__(self, p_meta):
        self.p_meta = p_meta
        self.is_extended_m3u = p_meta.params.get('extended_m3u', False)
        self.key_format_lookup = {
            'album':   M3UWriter._album_formatter,
            'song':    M3UWriter._song_formatter,
            'default': M3UWriter._default_formatter
        }

    def generate(self, results):
        formatter = self.key_format_lookup.get(self.p_meta.api_call, self.key_format_lookup.get('default'))
        playlist = ['#EXTM3U']
        for r_id, result in results:
            playlist.append(formatter(self, result))
            playlist.append(self.p_meta.get_gmp_url(r_id, result))
        rendered = '\n'.join(playlist)
        return M3U_MIME, self.p_meta.get_file_name(), rendered

    def _default_formatter(self, result):
        return '#EXTINF:-1,%s' % (result.get("title", result.get('name', '')))

    def _album_formatter(self, album):
        return '#EXTINF:-1,%s [%s]' % (album.get('name', ''), album.get('year', ''))

    def _song_formatter(self, track):
        return '#EXTINF:%s,%s%s%s' % (
        (int(track.get('durationMillis', '-1000')) / 1000), '%s - ' % track['artist'] if 'artist' in track else '',
        track.get('title', ''), ' - %s' % track['album'] if self.is_extended_m3u and 'album' in track else '')


class SPFWriter:

    def __init__(self, p_meta):
        self.p_meta = p_meta
        if p_meta.format == 'json':
            self.mime_type = JSON_MIME
            self.writer = spf_to_json
        else:
            self.mime_type = XSPF_MIME
            self.writer = spf_to_xml

    def generate(self, results):
        tracks = []
        for r_id, result in results:
            track = {
                'location':   self.p_meta.get_gmp_url(r_id, result),
                'title':      result.get("title", result.get("name", "")),
                'creator':    result.get("artist", ""),
                'album':      result.get("album", ""),
                'trackNum':   result.get("trackNumber", 0),
                'duration':   result.get("durationMillis", -1),
                'annotation': "year: %s" % result.get("year", "unknown"),
                'image':      result.get('albumArtRef', [{}])[0].get('url', None)
            }
            tracks.append(track)
        uri_info = self.p_meta.params[REQ_URIINFO]
        playlist = SPFList(title="GMP Playlist",
                           creator="GMusicProxy",
                           location='http://%s%s?%s' % (self.p_meta.host_and_port, uri_info.path, uri_info.query),
                           tracks=tracks)
        return self.mime_type, self.p_meta.get_file_name(), self.writer(playlist)


def make_xml_tag(tag_name, tag_value):
    tval = str(tag_value)
    if tag_value is None or len(tval) is 0:
        return ''
    return '<%s>%s</%s>' % (tag_name, escape(tval), tag_name)


"""
 See: http://www.xspf.org/ for detailed spec info
"""
class SPFList:

    def __init__(self, title, creator="GMusicProxy", location=None, tracks=[]):
        self.title = title
        self.creator = creator
        self.location = location # GMP URL
        self.date = datetime.now(timezone.utc).astimezone().isoformat()
        self.track = tracks


def spf_to_json(spf_list):
    return json.dumps({"playlist": {
        'title': spf_list.title,
        'creator': spf_list.creator,
        'location': spf_list.location,
        'date': spf_list.date,
        'track': spf_list.track
    }})

def spf_to_xml(spf_list):
    xml_tracks = []
    for d in spf_list.track:
        xml_track = ''.join(map(lambda x: make_xml_tag(x[0], x[1]), d.items()))
        if len(xml_track) > 0:
            xml_tracks.append('<track>%s</track>' % xml_track)
    xml_tracks = '<trackList>%s</trackList>' % ''.join(xml_tracks) if len(xml_tracks) > 0 else '<trackList />'
    return '<?xml version="1.0" encoding="UTF-8"?><playlist version="1" xmlns="http://xspf.org/ns/0/">' \
           + '%s%s%s%s%s</playlist>' % (make_xml_tag("title", spf_list.title), make_xml_tag("creator", spf_list.creator),
                                        make_xml_tag("location", spf_list.location), make_xml_tag("date", spf_list.date), xml_tracks)


def build_writer(host_and_port, api_call, params):
    p_meta = PlaylistMeta(host_and_port, api_call, params)
    requested_fmt = p_meta.format
    if requested_fmt == 'txt':
        writer = TextWriter(p_meta)
    elif requested_fmt == 'xml' or requested_fmt == 'json':
        writer = SPFWriter(p_meta)
    else:
        writer = M3UWriter(p_meta)
    return writer
