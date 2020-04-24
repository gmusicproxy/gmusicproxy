import logging
import json
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

class GMPWriter:
    BASE_URL = "http://%s/get_%s?id="


class TextWriter(GMPWriter):

    def __init__(self, host_and_port, api_call, params):
        self.base_url = self.BASE_URL % (host_and_port, api_call)
        self.separator = params.get('separator', ['|'])[0]
        self.only_url = params.get('only_url', ['no'])[0].lower().strip() == 'yes'
        self.api_call = api_call
        self.key_format_lookup = {
            'album':   TextWriter._album_formatter,
            'default': TextWriter._default_formatter
        }

    def generate(self, results):
        playlist = []
        kf_pair = self.key_format_lookup.get(self.api_call, self.key_format_lookup['default'])
        formatter = kf_pair if not self.only_url else TextWriter._empty_formatter
        q_string = '&format=txt' if self.api_call != 'song' else ''
        for r_id, result in results:
            playlist.append('%s%s%s%s' % (formatter(self, result), self.base_url, r_id, q_string))
        rendered = '\n'.join(playlist)
        return TXT_MIME, 'txt', rendered

    def _album_formatter(self, album):
        album_format = '%s%s%s%s' % (album['name'], self.separator, album['year'], self.separator) if (
                'name' in album and 'year' in album and not self.only_url) else ''
        return album_format

    def _empty_formatter(self, record):
        return ''

    def _default_formatter(self, result):
        record_format = '%s%s' % (result['name'], self.separator) if ('name' in result) else ''
        return record_format


class M3UWriter(GMPWriter):

    def __init__(self, host_and_port, api_call, params):
        self.host_and_port = host_and_port
        self.api_call = api_call
        self.base_url = self.BASE_URL % (host_and_port, api_call)
        self.is_extended_m3u = params.get('extended_m3u', False)
        self.key_format_lookup = {
            'album':   M3UWriter._album_formatter,
            'song':    M3UWriter._song_formatter,
            'default': M3UWriter._default_formatter
        }

    def generate(self, results):
        formatter = self.key_format_lookup.get(self.api_call, self.key_format_lookup.get('default'))
        playlist = ['#EXTM3U']
        for r_id, result in results:
            playlist.append(formatter(self, result))
            playlist.append('%s%s' % (self.base_url, r_id))
        rendered = '\n'.join(playlist)
        return M3U_MIME, 'm3u', rendered

    def _default_formatter(self, result):
        return '#EXTINF:-1,%s' % (result.get('name', ''))

    def _album_formatter(self, album):
        return '#EXTINF:-1,%s [%s]' % (album.get('name', ''), album.get('year', ''))

    def _song_formatter(self, track):
        return '#EXTINF:%s,%s%s%s' % (
        (int(track.get('durationMillis', '-1000')) / 1000), '%s - ' % track['artist'] if 'artist' in track else '',
        track.get('title', ''), ' - %s' % track['album'] if self.is_extended_m3u and 'album' in track else '')


class SPFWriter(GMPWriter):

    def __init__(self, host_and_port, api_call, params):
        self.base_url = self.BASE_URL % (host_and_port, api_call)
        self.host_and_port = host_and_port
        self.api_call = api_call
        self.params = params
        self.is_json = params.get('format', ['json'])[0] == 'json'
        self.f_ext = 'json' if self.is_json else 'xml'

    def generate(self, results):
        tracks = []
        q_string = '&format=' + self.f_ext if self.api_call != 'song' else ''
        for r_id, result in results:
            track = {
                'location':   '%s%s%s' % (self.base_url, r_id, q_string),
                'title':      result.get("title", result.get("name", "")),
                'creator':    result.get("artist", ""),
                'album':      result.get("album", ""),
                'trackNum':   result.get("trackNumber", 0),
                'duration':   result.get("durationMillis", -1),
                'annotation': "year: %s" % result.get("year", "unknown"),
                'image':      result.get('albumArtRef', [{}])[0].get('url', None)
            }
            tracks.append(track)
        uri_info = self.params[REQ_URIINFO]
        playlist = SPFList(title="GMP Playlist",
                           creator="GMusicProxy",
                           location='%s%s?%s' % (self.host_and_port, uri_info.path, uri_info.query),
                           tracks=tracks)
        if self.is_json:
            return JSON_MIME, 'json', playlist.to_json()
        else:
            return XSPF_MIME, 'xspf', playlist.to_xml()


def make_xml_tag(tag_name, tag_value):
    tval = str(tag_value)
    if tag_value is None or len(tval) is 0:
        return ''
    return '<%s>%s</%s>' % (tag_name, escape(tval), tag_name)


"""
Comprehensive example of JSPF
{
   "playlist" : {
     "title"         : "JSPF example",
     "creator"       : "Name of playlist author",
     "annotation"    : "Super playlist",
     "info"          : "http://example.com/",
     "location"      : "http://example.com/",
     "identifier"    : "http://example.com/",
     "image"         : "http://example.com/",
     "date"          : "2005-01-08T17:10:47-05:00",
     "license"       : "http://example.com/",
     "attribution"   : [
       {"identifier"   : "http://example.com/"},
       {"location"     : "http://example.com/"}
     ],
     "link"          : [
       {"http://example.com/rel/1/" : "http://example.com/body/1/"},
       {"http://example.com/rel/2/" : "http://example.com/body/2/"}
     ],
     "meta"          : [
       {"http://example.com/rel/1/" : "my meta 14"},
       {"http://example.com/rel/2/" : "345"}
     ],
     "extension"     : {
       "http://example.com/app/1/" : [ARBITRARY_EXTENSION_BODY, ARBITRARY_EXTENSION_BODY],
       "http://example.com/app/2/" : [ARBITRARY_EXTENSION_BODY]
     },
     "track"         : [
       {
         "location"      : ["http://example.com/1.ogg", "http://example.com/2.mp3"],
         "identifier"    : ["http://example.com/1/", "http://example.com/2/"],
         "title"         : "Track title",
         "creator"       : "Artist name",
         "annotation"    : "Some text",
         "info"          : "http://example.com/",
         "image"         : "http://example.com/",
         "album"         : "Album name",
         "trackNum"      : 1,
         "duration"      : 0,
         "link"          : [
           {"http://example.com/rel/1/" : "http://example.com/body/1/"},
           {"http://example.com/rel/2/" : "http://example.com/body/2/"}
         ],
         "meta"          : [
           {"http://example.com/rel/1/" : "my meta 14"},
           {"http://example.com/rel/2/" : "345"}
         ],
         "extension"     : {
           "http://example.com/app/1/" : [ARBITRARY_EXTENSION_BODY, ARBITRARY_EXTENSION_BODY],
           "http://example.com/app/2/" : [ARBITRARY_EXTENSION_BODY]
         }
       }
     ]
   }
 }
"""
class SPFList:

    def __init__(self, title, creator="GMusicProxy", location=None, tracks=[]):
        self.title = title
        self.creator = creator
        self.location = location # GMP URL
        self.date = datetime.now(timezone.utc).astimezone().isoformat()
        self.track = tracks

    def to_json(self):
        return json.dumps({"playlist" : {
            'title': self.title,
            'creator': self.creator,
            'location':self.location,
            'date': self.date,
            'track': self.track
        }})

    def to_xml(self):
        xml_tracks = []
        for d in self.track:
            xml_track = ''.join(map(lambda x: make_xml_tag(x[0], x[1]), d.items()))
            if len(xml_track) > 0:
                xml_tracks.append('<track>%s</track>' % xml_track)
        xml_tracks = '<trackList>%s</trackList>' % ''.join(xml_tracks) if len(xml_tracks) > 0 else '<trackList />'
        return '<?xml version="1.0" encoding="UTF-8"?><playlist version="1" xmlns="http://xspf.org/ns/0/">' \
               + '%s%s%s%s%s</playlist>' % (make_xml_tag("title", self.title), make_xml_tag("creator", self.creator),
                                            make_xml_tag("location", self.location), make_xml_tag("date", self.date), xml_tracks)


def build_writer(host_and_port, api_call, params):
    requested_fmt = params.get('format', ['m3u'])[0].lower().strip()
    if requested_fmt == 'txt' or requested_fmt == 'text':
        writer = TextWriter(host_and_port, api_call, params)
    elif requested_fmt == 'xml' or requested_fmt == 'json':
        writer = SPFWriter(host_and_port, api_call, params)
    else:
        writer = M3UWriter(host_and_port, api_call, params)

    return writer
