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
This program permits the use of Google Play Music with All Access subscription with any music player that is able to stream MP3 files and to manage M3U playlists (e.g., [MPD server][1], [VLC][2], ...). It can work also with a free account without All Access extras.

Google has released a nice music service with the possibility to stream all the available music using the All Access subscription. The Google-way to listen your collection and the stations is by means of Android devices or any web browser. If you want to use your TVs or HiFi audio systems, the main tool is the Chromecast key (or its audio variant). These devices are closed and limited in someway. I already got a music-system at home based on a small Raspberry-PI connected to my HiFi audio system (using a professional DAC): it makes use of [MPD][1] and I wanted to keep it.

My project is based on the great [Unofficial Google Play Music API][3] of Simon Weber: it already permits to create URLs to stream the tracks as regular MP3 but they expire in 1 minute! Keeping this proxy running, it can generate persistent local URLs that never expire and that can be used in any media-player.

This project is not supported nor endorsed by Google. Its aim is not the abuse of the service but the one to improve the access to it. The maintainers are not responsible for misuse.

### Features
- create persistent URLs to all the tracks, albums and stations available on the Google Play Music + All Access platform
- get access to all the songs in your collection, playlists and registered stations
- search by name any artist, album or song
- request a transient (it will be not registered in your account) station based on any search (a.k.a. "Instant Mix")
- stream any songs as standard MP3 complete of IDv3 tag with all the information and album image

### URL-based interface
The only way to use the service is to query the proxy by means of properly formatted HTTP requests over the configured TCP port. Such URLs can be used directly in music programs or in scripts or in any browser. A URL looks like this: `http://host:port/command?param_1=value&param_2=value`. I don't apply any validation to the submitted values: please, be nice with the proxy and don't exploit it! :)

Consider that any song, album, artist, playlist or station got a unique ID in Google Music API but there are many methods to discover them.

Here a list of the supported requests (with some restricted by the availability of a All Access subscription):

- `/get_collection`: reports an M3U playlist with all the songs in your personal collection; the resulting list can be shuffled and/or filtered using the rating; note that not all the rated (liked) songs belong to your collection.
  Allowed parameters:
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
     - `shuffle`: if the collection has to be shuffled [default: no]
	 - `rating`: an integer value (typically between 1-5) to filter out low rated or unrated songs form your collection
- `/search_id`: reports the unique ID as result of a search for an artist, a song or an album.
  Allowed parameters:
     - `type`: search for `artist`, `album` or `song` [required]
     - `title`: a string to search in the title of the album or of the song
     - `artist`: a string to search in the name of the artist in any kind of search
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song [default: `yes`]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/get_by_search`: makes a search for artist/album/song as `/search_id` and returns the related content (an M3U list for the album or for the top songs of an artist and the MP3 file for a song); it is also possible to get the full list of matches reported by Google Music using search with `type=matches` [requires A.A.].
  Allowed parameters:
     - `type`: search for `artist`, `album`, `song` or `matches` [required]
     - `title`: a string to search in the title of the album or of the song
     - `artist`: a string to search in the name of the artist in any kind of search
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song; it doesn't make sense with a search for `matches` [default: `no`]
     - `num_tracks`: the number of top songs to return in a search for artist [default: 20]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/get_all_stations`: reports a list of registered stations as M3U playlist (with URLs to other M3U playlist) or as plain-text list (with one station per line)  [requires A.A.].
  Allowed parameters:
     - `only_url`: a `yes` creates a list of just URLs in the plain-text lists (the name of the station is totally omitted) [default: `no`]
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song [default: `no`]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/get_all_playlists`: reports the playlists registered in the account as M3U playlist (with URLs to other M3U playlist) or as plain-text list (with one playlist per line).
  The allowed parameters are the same as `/get_all_stations`.
- `/get_new_station_by_search`: reports as M3U playlist the content of a new (transient or permanent) station created on the result of a search for artist/album/song (a.k.a. "Instant Mix") [requires A.A.].
  Allowed parameters:
     - `type`: search for `artist`, `album` or `song` [required]
     - `title`: a string to search in the title of the album or of the song
     - `artist`: a string to search in the name of the artist in any kind of search
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song [default: `no`]
     - `num_tracks`: the number of songs to extract from the new station [default: 20]
     - `transient`: a `no` creates a persistent station that will be registered into the account [default: `yes`]
     - `name`: the name of the persistent station to create [required if `transient` is `no`]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/get_new_station_by_id`: reports as M3U playlist the content of a new (transient or permanent) station created on a specified id of an artist/album/song [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the artist/album/song [required]
     - `type`: the type of id specified among `artist`, `album` and `song` [required]
     - `num_tracks`: the number of songs to extract from the new station [default: 20]
     - `transient`: a `no` creates a persistent station that will be registered into the account [default: `yes`]
     - `name`: the name of the persistent station to create [required if `transient` is `no`]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/get_station`: reports an M3U playlist of tracks associated to the given station  [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the station [required]
     - `num_tracks`: the number of tracks to extract [default: 20]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/get_ifl_station`: reports an M3U playlist of tracks associated to the automatic "I'm feeling lucky" station  [requires A.A.].
  Allowed parameters:
     - `num_tracks`: the number of tracks to extract [default: 20]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/get_playlist`: reports the content of a registered playlist in the M3U format; the list can be also shuffled.
  Allowed parameters:
     - `id`: the unique identifier of the playlist [required]
     - `shuffle`: if the list has to be shuffled [default: no]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/get_album`: reports the content of an album as an M3U playlist.
  Allowed parameters:
     - `id`: the unique identifier of the album [required]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/get_song`: streams the content of the specified song as a standard MP3 file with IDv3 tag.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]
- `/get_song_info`: returns JSON Metadata for the specified song.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]
- `/get_top_tracks_artist`: reports an M3U playlist with the top songs of a specified artist [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the artist [required]
     - `type`: the type of id specified among `artist`, `album` and `song` [required]
     - `num_tracks`: the number of top songs to return [default: 20]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/get_discography_artist`: reports the list of available albums of a specified artist as a playlist (with URLs to other M3U playlist) or as plain-text list (with one album per line)  [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the artist [required]
     - `only_url`: a `yes` creates a list of just URLs in the plain-text lists (the name of the album is totally omitted) [default: `no`]
     - `format`: if omitted, returns `m3u` but can be one of `m3u`, `text`, `xml`, or `json`. See below for format 
     information [default: `m3u`]
- `/like_song`: reports a positive rating on the song with specified id.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]
- `/dislike_song`: reports a negative rating on the song with specified id.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]
- `/get_version`: displays current version in JSON format

The `format` parameter can be used to generate output in the following formats:
   - `m3u`: Generates an M3U formatted list. 
   - `text`: for a plain-text list with lines like `Name of the Station|URL to a song or playlist`
       - `separator`: when requesting text formatted output, the separator to delineate fields [default: `|`]
   - `xml`: Returns an [XSPF][7] formatted playlist
   - `json`: Returns a json formatted playlist folling the XSPF json format

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
- `--bind-address`: ip address to bind to [default: 0.0.0.0=all]
- `--port`: default TCP port to use [default: 9999]
- `--config`: specific configuration file to use
- `--disable-all-access`: disable All Access functionalities
- `--list-devices`: list the registered devices
- `--debug`: enable debug messages
- `--log`: log file
- `--daemon`: daemonize the program
- `--disable-version-check`: disable check for latest available version
- `--extended-m3u`: enable non-standard extended m3u headers
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

### Using keyring to store the password
Password can be retrieved from one of the available keyrings (e.g. KWallet, Freedesktop Secret Service, Windows Credential Vault, Mac OS X Keychain). Use command-line option `--list-keyring-backends` to find out, which keyring backends are supported on your platform.
If the default keyring backend is not what you want, you can override it using option `--keyring-backend`.

To read the password from the keyring, specify the options `--keyring-service` and `--keyring-entry`. Use the corresponding keyring manager to store the password or find entry name for one of your existing passwords.

E.g. for KWallet, you can list available service names and entries as follows:

  ```bash
  # list service names
  kwallet-query -l kdewallet -f ""
  # list entries of service "Passwords"
  kwallet-query -l kdewallet -f "Passwords"
  ```

### Examples of integration
#### [MPD][1]
- You can copy any M3U list generated by the proxy in the playlists registered inside MPD. MPD usually keeps the playlists inside the folder specified by `playlist_directory` in its configuration file `mpd.conf`.

  ```bash
  curl -s 'http://localhost:9999/get_by_search?type=album&artist=Queen&title=Greatest%20Hits' >
    /var/lib/mpd/playlists/queen.m3u
  mpc load queen
  mpc play
  ```

- You can also request a fresh list of songs from a station and add them to the current playlist.

  ```bash
  mpc clear
  curl -s 'http://localhost:9999/get_new_station_by_search?type=artist&artist=Queen&num_tracks=100' |
    grep -v ^# | while read url; do mpc add "$url"; done
  mpc play
  ```

#### [VLC][2]
- You can listen any generated playlist using VLC from command-line.

  ```bash
  vlc 'http://localhost:9999/get_by_search?type=album&artist=Rolling%20Stones&title=tattoo&exact=no'
  ```

- You can automatically choose at random one registered station.

  ```bash
  curl -s 'http://localhost:9999/get_all_stations?format=text&only_url=yes' | sort -R | head -n1 | vlc -
  ```

### [Docker][6]

- Official Docker builds are available on [Docker Hub][8]

- To build and run the Docker container, follow these steps

  ```bash
  sudo docker build -t gmusicproxy:latest .
  # Note that you may need to adjust the volume argument to point to your gmusicproxy.cfg file
  sudo docker run -v /home/ubuntu/gmusicproxy.cfg:/root/.config/gmusicproxy.cfg -p 9999:9999 gmusicproxy:latest
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
