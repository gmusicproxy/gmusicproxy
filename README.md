# [GMusicProxy][0] - Google Play Music Proxy 

*"Let's stream Google Play Music using any media-player"*

![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gmusicproxy/gmusicproxy) ![Python Versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)

contributors:
- [Mario Di Raimondo](mailto:mario.diraimondo@gmail.com)
- [Nick Depinet](mailto:depinetnick@gmail.com)
- [Adam Prato](mailto:adam.prato@gmail.com)
- [Pierre Karashchuk](mailto:krchtchk@gmail.com)
- [Alex Busenius](mailto:)
- [Mark Gillespie](mailto:mark.gillespie@gmail.com)
- [Justin Woody](mailto:gmusicproxy@gmail.com)

License: **GPL v3**

## About
This program permits the use of Google Play Music with All Access subscription with any music player that is able to stream MP3 files and to manage playlists (e.g., [MPD server][1], [VLC][2], ...). It can work also with a free account without All Access extras.

Google has a music service with the possibility to stream all the available music using an All Access subscription. The Google-way to listen your collection and the stations is by means of Android devices, web browser, or Chromecast devices to integrate with TVs or HiFi audio systems. These devices are typically closed or limited in someway. Many people use music-systems based on Raspberry-PIs, [MPD][1], or other software and GMP provide an integration point.

The project is based on the great [Unofficial Google Play Music API][3] by Simon Weber: it already permits to create URLs to stream the tracks as regular MP3 but they expire in 1 minute! Keeping this proxy running, it can generate persistent local URLs that never expire and that can be used in any media-player.

This project is not supported nor endorsed by Google. Its aim is not the abuse of the service but the one to improve the access to it. The maintainers are not responsible for misuse.

### Features
- create persistent URLs to all the tracks, albums and stations available on the Google Play Music + All Access platform
- get access to all the songs in your collection, playlists and registered stations
- search by name any artist, album or song
- request a transient (it will be not registered in your account) station based on any search (a.k.a. "Instant Mix")
- stream any songs as standard MP3 complete of IDv3 tag with all the information and album image

### URL-based interface
The only way to use the service is to query the proxy by means of properly formatted HTTP requests over the configured TCP port. Such URLs can be used directly in music programs or in scripts or in any browser. A URL looks like this: `http://host:port/command?param_1=value&param_2=value`. Validation on submitted values is minimal, please be aware.

Consider that any song, album, artist, playlist or station got a unique ID in Google Music API but there are many methods to discover them.

Here a list of the supported requests (with some restricted by the availability of a All Access subscription):

- `/get_collection`: reports a playlist with all the songs in your personal collection; the resulting list can be shuffled and/or filtered using the rating; note that not all the rated (liked) songs belong to your collection.
  Allowed parameters:
     - [See common request options](#reqoptions)
     - `rating`: an integer value (typically between 1-5) to filter out low rated or unrated songs form your collection
- `/search_id`: reports the unique ID as result of a search for an artist, a song or an album.
  Allowed parameters:
     - `type`: search for `artist`, `album` or `song` [required]
     - `title`: a string to search in the title of the album or of the song
     - `artist`: a string to search in the name of the artist in any kind of search
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song [default: `yes`]
     - [See common request options](#reqoptions)
- `/get_by_search`: makes a search for artist/album/song as `/search_id` and returns the related content (a list for the album or for the top songs of an artist and the MP3 file for a song); it is also possible to get the full list of matches reported by Google Music using search with `type=matches` [requires A.A.].
  Allowed parameters:
     - `type`: search for `artist`, `album`, `song` or `matches` [required]
     - `title`: a string to search in the title of the album or of the song
     - `artist`: a string to search in the name of the artist in any kind of search
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song; it doesn't make sense with a search for `matches` [default: `no`]
     - [See common request options](#reqoptions)
- `/get_all_stations`: reports a list of registered stations as a playlist (with URLs to each station playlist)  [requires A.A.].
  Allowed parameters:
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song [default: `no`]
     - [See common request options](#reqoptions)
- `/get_all_playlists`: reports the playlists registered in the account as playlist (with URLs to other playlist) 
  The allowed parameters are the same as `/get_all_stations`.
- `/get_new_station_by_search`: returns a playlist containing songs from a new (transient or permanent) station created on the result of a search for artist/album/song (a.k.a. "Instant Mix") [requires A.A.].
  Allowed parameters:
     - `type`: search for `artist`, `album` or `song` [required]
     - `title`: a string to search in the title of the album or of the song
     - `artist`: a string to search in the name of the artist in any kind of search
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song [default: `no`]
     - `transient`: a `no` creates a persistent station that will be registered into the account [default: `yes`]
     - `name`: the name of the persistent station to create [required if `transient` is `no`]
     - [See common request options](#reqoptions)
- `/get_new_station_by_id`: returns a playlist containing tracks from a new (transient or permanent) station created on a specified id of an artist/album/song [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the artist/album/song [required]
     - `type`: the type of id specified among `artist`, `album` and `song` [required]
     - `transient`: a `no` creates a persistent station that will be registered into the account [default: `yes`]
     - `name`: the name of the persistent station to create [required if `transient` is `no`]
     - [See common request options](#reqoptions)
- `/get_station`: reports a playlist of tracks associated to the given station  [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the station [required]
     - [See common request options](#reqoptions)
- `/get_ifl_station`: reports a playlist of tracks associated to the automatic "I'm feeling lucky" station  [requires A.A.].
  Allowed parameters:
     - [See common request options](#reqoptions)
- `/get_playlist`: reports the content of a registered playlist
  Allowed parameters:
     - `id`: the unique identifier of the playlist [required]
     - [See common request options](#reqoptions)
- `/get_album`: reports the content of an album as a playlist.
  Allowed parameters:
     - `id`: the unique identifier of the album [required]
     - [See common request options](#reqoptions)
- `/get_song`: streams the content of the specified song as a standard MP3 file with IDv3 tag.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]
- `/get_song_info`: returns JSON Metadata for the specified song.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]
- `/get_top_tracks_artist`: reports a playlist with the top songs of a specified artist [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the artist [required]
     - `type`: the type of id specified among `artist`, `album` and `song` [required]
     - [See common request options](#reqoptions)
- `/get_discography_artist`: reports the list of available albums of a specified artist as a playlist (with URLs to other playlists) or as plain-text list (with one album per line)  [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the artist [required]
     - [See common request options](#reqoptions)
- `/get_top_songs`: Returns a playlist of top songs
- `/get_situations`: Returns a collection of situations, e.g. Today's biggest hits
- `/get_listen_now`: Provides 'Listen Now' playlists by either album or artist. Allowed Parameters:
     - `type`: `album` or `artist`. [Defaults to `artist`]
     - [See common request options](#reqoptions)
- `/get_listen_now_list`: Call for specific Listen Now playlist
- `/like_song`: reports a positive rating on the song with specified id.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]
- `/dislike_song`: reports a negative rating on the song with specified id.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]
- `/get_version`: displays current version in JSON format

### <a name="reqoptions"></a>Common request options

The proxy supports common options for responses:

- `format` or HTTP Accept header: [See Output Format](#format)
- `shuffle`: Set to `yes` to shuffle the list [default: `no`]
- `num_tracks`: Maximum number of items to return. If `shuffle` is set to `yes`, shuffle is applied prior to limiting the results.

**Note:** these parameters are not valid for `get_song`.

Examples:

```bash
# request XSPF/XML format
curl http://[gmp host|ip]:9999/get_all_playlists?format=xsfp
# request shuffled output
curl http://[gmp host|ip]:9999/get_all_playlists?shuffle=yes
# Return playlist with 10 items
curl http://[gmp host|ip]:9999/get_all_playlists?num_tracks=10
```

#### <a name="format"></a>Output Format
Beginning with version 2.2.0, Accept headers should be the preferred way to request a specific output format. e.g. for JSON:

```bash
curl -H 'Accept: application/json' http://[gmp host|ip]:9999/get_all_playlists
```

The `format` parameter can be used to generate output in the following formats:
   - `m3u`: Generates an M3U formatted list. 
   - `xm3u`: lines of the produced M3U lists to a non-standard format like `artist - song title - album title`
   - `text`|`txt`: for a plain-text list with lines like `Name of the Station|URL to a song or playlist`
       - `separator`: when requesting text formatted output, the separator to delineate fields [default: `|`]
       - `only_url`: a `yes` creates a list of just URLs in the plain-text lists (the name of the album is totally omitted) [default: `no`]
   - `xspf`|`xml`: Returns an [XSPF][7] formatted playlist
   - `json`: Returns a json formatted playlist following the XSPF json format

### Changelog
- See RELEASES.md for release information.

### Related projects

- Simon's Unofficial-Google-Music-API (the great backend used by gmusicproxy): https://github.com/simon-weber/gmusicapi
- web2py-mpd-gmproxy (a web interface that uses gmusicproxy as backend): https://github.com/matclab/web2py-mpd-gmproxy
- GMusic-MPD (an helper script for GMusicProxy together with MPD): https://github.com/Illyism/GMusic-MPD
- gmproxy-scripts (helper scripts for working with GMusicProxy): https://github.com/kmac/gmproxy-scripts
- gpmplay (a bash script to easily search with GMusicproxy): https://github.com/onespaceman/gmpplay
- g-music (Emacs client for gmusicproxy and mpd): https://github.com/bodicsek/g-music
- GMusicProxyGui (a C# GUI for the GMusicProxy): https://github.com/Poket-Jony/GMusicProxyGui

## Support

### Issues
Feel free to open [bug reports][4] (complete of verbose output produced with options `--debug` and `--log`) on GitHub, to fork the project and to make [pull requests][5] for your contributions.

## Setup
### Requirements
- a Google Play Music account with All Access subscription (some functionalities continue to work even with a free account)
- a **Python** 3.8 interpreter.
- some python libs, see `setup.py`

### Installation
The following instructions have a Debian/Ubuntu GNU/Linux system as reference: nevertheless they work on any other GNU/Linux system using the right substitute of `apt-get`. It is known to work also on Mac OS X and Windows systems.

In order to build/install GMusicProxy, the following should work on Ubuntu/Debian based systems:

```bash
sudo apt install python3 python3-dev git
git clone https://github.com/gmusicproxy:/gmusicproxy.git
cd gmusicproxy
virtualenv -p python3.8 venv
. venv/bin/activate
pip install -r requirements.txt
python GMusicProxy
```

- The `pip install` command could require the options `--allow-external eyed3 --allow-unverified eyed3` on some systems in order to validate the installation of `eyed3`.

## Usage
With the service running on a computer on the LAN, it can be used by any others of the same network.

To use the proxy, you first need to login via OAuth2. If you haven't authorized gmusicapi yet (or the credentials were revoked or deleted), when you first launch GMusicProxy, your browser will open letting you login and authorize gmusicapi. If no browser is available, the URL printed out can be used to login. After this, OAuth2 credentials (not your *email* and *password*) are cached to disk so future uses don't require you to login again.

Another useful information would be the device ID of an Android/iOS device registered in your account: you can discover it using the option `--list-devices` on the command-line. As default a fake-id, based on the mac address of the main network card of the server running the service, is used.

You can provide such necessary information, as well as other options, on the command-line of the program or using a configuration file.

### Command-line
Here a list of the supported options on the command-line:

- `--email`: [DEPRECATED] email address of the Google account
- `--password`: [DEPRECATED] password of the Google account
- `--device-id`: the ID of a registered Android/iOS device [default: fake-id based on mac address of network card]
- `--host`: host in the generated URLs [default: autodetected local ip address]
- `--host-port`: port in the generated URLs [default: -P or 9999]
- `--bind-address`: ip address to bind to [default: 0.0.0.0=all]
- `--port`: default TCP port to use [default: 9999]
- `--config`: specific configuration file to use
- `-F DEFAULT_FORMAT, --default-format DEFAULT_FORMAT`: Sets the defualut output format
- `--disable-all-access`: disable All Access functionalities
- `--list-devices`: list the registered devices
- `--debug`: enable debug messages
- `--log`: log file
- `--daemon`: daemonize the program
- `--disable-version-check`: disable check for latest available version
- `--shoutcast-metadata`: enable Shoutcast metadata protocol support (disabling IDv3 tags)
- `--disable-playcount-increment`: disable the automatic increment of playcounts upon song fetch
- `--keyring-backend`: [DEPRECATED] name of the keyring backend to use instead of the default one
- `--list-keyring-backends`: [DEPRECATED] list the available keyring backends
- `--keyring-service`: [DEPRECATED] keyring service to use, takes precedence over `--password` if set
- `--keyring-entry`: [DEPRECATED] keyring entry to use, required if `--keyring-service` is used

### Config file
All the command-line options can be specified in a configuration file. An example of configuration with the strictly required options could look like this:

```
email = my.email@gmail.com
password = my-secret-password
device-id = 54bbd32a309a34ef
```

When the proxy is launched, it searches for a file named `gmusicproxy.cfg` in the XDG-compliant folders like `/home/USER/.config/` or `/etc/xdg/`. It is possible to specify an arbitrary config file on the command-line using the option `--config`.


### Examples of integration
#### [MPD][1]
You can copy any M3U list generated by the proxy in the playlists registered inside MPD. MPD usually keeps the playlists inside the folder specified by `playlist_directory` in its configuration file `mpd.conf`.

```bash
curl -s 'http://localhost:9999/get_by_search?type=album&artist=Queen&title=Greatest%20Hits' > /var/lib/mpd/playlists/queen.m3u
mpc load queen
mpc play
```

You can also request a fresh list of songs from a station and add them to the current playlist.

```bash
mpc clear
curl -s 'http://localhost:9999/get_new_station_by_search?type=artist&artist=Queen&num_tracks=100' | grep -v "^#" | while read url; do mpc add "$url"; done
mpc play
```

You can add an XSPF playlist to mpd, which provides better metadata:

```bash
mpc load "http://localhost:9999/get_top_songs?format=xspf"
```

#### [VLC][2]
You can listen any generated playlist using VLC from command-line.

```bash
vlc 'http://localhost:9999/get_by_search?type=album&artist=Rolling%20Stones&title=tattoo&exact=no'
```
With the addition of XSPF playlists, better metadata is provided:
```bash
vlc 'http://localhost:9999/get_top_songs?format=xspf'
```

You can automatically choose at random one registered station.

```bash
curl -s 'http://localhost:9999/get_all_stations?format=text&only_url=yes' | sort -R | head -n1 | vlc -
```

### [Docker][6]

Official Docker builds are available on [Docker Hub][8]. To build and run the Docker container, follow these steps:

```bash
docker build -t gmusicproxy:latest .
# Note that OAuth is the preferred login method 
# You may need to run interactively (-it) in order to
# establish your credentials.
# Replace /path/for/oauthcreds with a directory for oauth token storage
docker run -it -p 9999:9999 -v /path/for/oauthcreds:/root/.local/share/gmusicapi gmusicproxy:latest
# Once OAuth is established, run normally:
docker run -v /path/for/oauthcreds:/root/.local/share/gmusicapi -p 9999:9999 gmusicproxy:latest
```

#### Other Docker Examples
Running as daemon
```bash
docker run -d -p 9999:9999 -v /path/for/oauthcreds:/root/.local/share/gmusicapi gmusicproxy/gmusicproxy:VERSION
```
Running on port 80 with a different Host/IP in the URLs. Note the required `-T` argument
```bash
docker run -p 80:9999 -v /path/for/oauthcreds:/root/.local/share/gmusicapi gmusicproxy/gmusicproxy:VERSION -T 80
```

[0]: https://gmusicproxy.github.io
[1]: http://www.musicpd.org/
[2]: http://www.videolan.org/vlc/
[3]: https://github.com/simon-weber/gmusicapi
[4]: https://github.com/gmusicproxy/gmusicproxy/issues
[5]: https://github.com/gmusicproxy/gmusicproxy/pulls
[6]: https://docker.com/
[7]: http://www.xspf.org/
[8]: https://hub.docker.com/r/gmusicproxy/gmusicproxy
