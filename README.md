#GMusicProxy – Google Play Music Proxy

*"Let's stream Google Play Music using any media-player"*

© [Mario Di Raimondo](mailto:info@gmusicproxy.net)
site: http://gmusicproxy.net

contributors:
- [Nick Depinet](mailto:depinetnick@gmail.com)

License: **GPL v3**

## About
This program permits the use of Google Play Music with All Access subscription with any music player that is able to stream MP3 files and M3U playlists (e.g., [MPD server][1], [VLC][2], ...). It can work also with a free account without All Access extras.

Google has released a nice music service and now it is even more interesting with the All Access option. The Google-way to listen your collection and the stations is by means of Android devices or any web browser. If you want to use your TVs or HiFi audio systems, the main tool is the Chromecast key. I can't buy one (at the moment it is not available in my country) and it looks a bit closed. Even more I already got a music-system based on a PC connected to my HiFi audio system: it makes use of [MPD][1] and I would like keep it.

My project is based on the great [Unofficial Google Play Music API][3] of Simon Weber: it already permits to create URLs to stream the tracks as regular MP3 but they expire in 1 minute! Keeping this proxy running, it can generate persistent local URLs that never expire and that can be used in any media-player.

This project is not supported nor endorsed by Google. Its aim is not the abuse of the service but the one to improve the access to it. I'm not responsible of its misuse.

### Features
- create persistent URLs to all the tracks, albums and stations available on the Google Play Music + All Access platform
- get access to all the songs in your collection, playlists and registered stations
- search by name any artist, album or song
- request a transient (it will be not registered in your account) station based on any search
- stream any songs as standard MP3 complete of IDv3 tag with all the information and album image

### Changelog
- 0.9.9.1 (unreleased):
  - fixed breakage on login due to gmusicapi change on the development branch (thanks for the pull request to @Mlmlte)
- 0.9.9 (2015-05-27):
  - fixed login problem using the devel branch (5.0.0-dev0) of gmusicapi (today not yet released)
  - changed the installation instructions using pip `requirements.txt` file: this permits the automatic deploy of gmusicapi from github
  - the functionality `--list-devices` is actually broken: keep a copy of you device ids!
- 0.9.8 (2014-09-14):
  - new option `extended-m3u`: it optionally extends `#EXTINF:` lines of the produced M3U lists to a non-standard format like `artist - song title - album title`
- 0.9.7 (2014-08-25):
  - merged a contribution by Nick Depinet to report all the possible matches of a search (support required by project CSH DJ)
- 0.9.6 (2014-08-08):
  - added support for returning multiple songs in the search results using type `songs` for `get_by_search`
- 0.9.5 (2014-03-23):
  - added support for the dynamic 'I'm feeling lucky' station: `get_ifl_station`
- 0.9.4 (2014-02-02):
  - added support for 'album artist' tag (requires a development version >= 0.7.5-beta of eyed3 lib)
  - added control on startup for new versions
- 0.9.2 (2013-10-30):
  - added the possibility to rate songs (like/dislike)
- 0.9.1 (2013-10-05):
  - a new and more robust message/log system
  - possibility to daemonize the proxy
- 0.8 (2013-09-22):
  - rewrote command-line/config system
  - possibility to disable AA features for a free GM account
  - improved documentation
- 0.6 (2013-09-15): first public version

### Related projects

- Simon's Unofficial-Google-Music-API (the great backend used by gmusicproxy): https://github.com/simon-weber/Unofficial-Google-Music-API
- web2py-mpd-gmproxy (a web interface that uses gmusicproxy as backend): https://github.com/matclab/web2py-mpd-gmproxy
- GMusic-MPD (an helper script for GMusicProxy together with MPD): https://github.com/Illyism/GMusic-MPD

## Setup
### Requirements
- a Google Play Music account with All Access subscription (some functionalities continue to work even with a free account)
- a **Python** 2.7 interpreter
- some python libs: *gmusicapi*, *netifaces*, *pyxdg*, *eyed3*, *python-daemon*

### Installation
The following instructions have a Debian/Ubuntu GNU/Linux system as reference: nevertheless they work on any other GNU/Linux system using the right substitute of `apt-get`. It should work on a Mac OS X system and it *could* even work on a Windows one.

In order to build some dependencies, you need for sure a working building system: `sudo apt-get install build-essential python2.7-dev` .

- The easiest way is to use the `pip` command to install the proxy with all the dependencies from PyPI and GitHub repositories:

    - `sudo apt-get install python-pip`
    - get a copy of the sources using one of these methods:
      - `git clone https://github.com/diraimondo/gmusicproxy.git`
      - download and extract a [tar][6] or [zip][7] archive of the last version
    - install it and all the dependencies using `sudo pip install -r requirements.txt` from the inside of the folder
    - use it from everywhere: `GMusicProxy`

  The `pip install ...` command could require the options `--allow-external eyed3 --allow-unverified eyed3` on some systems in order to validate the installation of `eyed3`.

  Importante note: the usage of `sudo pip ...` commands could mess up your main packaging system; consider the next method.

- The right way to use an under-development python project makes use of `virtualenv` and `virtualenvwrapper` utilities:
  - install the proxy once:

    ```bash
    sudo apt-get install python-pip python-virtualenv virtualenvwrapper
    mkvirtualenv -p /usr/bin/python2 gmusicproxy
    git clone https://github.com/diraimondo/gmusicproxy.git
    cd gmusicproxy
    pip install -r requirements.txt
    ```
    note: it could be necessary to close/reopen the shell in order to use virtualenvwrapper aliases
  - launch the proxy when you need it:

    ```bash
    workon gmusicproxy
    GMusicProxy
    ```
  - if you need to upgrade the proxy and its dependencies:
    - use the option `--upgrade` on the `pip` installation command (e.g., `pip install --upgrade -r requirements`), or
    - clean-up the virtualenv using `deactivate ; rmvirtualenv gmusicproxy` and reinstall everything as before.

## Usage 
With the service running on a computer on the LAN, it can be used by any others of the same network.

To launch the proxy you need the credentials of your Google account: *email* and *password*. If you are using the 2-factor authentication, you have to create an application-specific password to be used with this program. Another required information is the device ID of an Android device registered in your account: you can discover it using the option `--list-devices` on the command-line.

You can provide such necessary information, as well as other options, on the command-line of the program or using a configuration file.

### Command-line
Here a list of the supported options on the command-line:

- `--email`: email address of the Google account [required]
- `--password`: password of the Google account [required]
- `--device-id`: the ID of a registered Android device [required]
- `--host`: host in the generated URLs [default: autodetected local ip address]
- `--port`: default TCP port to use [default: 9999]
- `--config`: specific configuration file to use
- `--disable-all-access`: disable All Access functionalities
- `--list-devices`: list the registered devices
- `--debug`: enable debug messages
- `--log`: log file
- `--daemon`: daemonize the program
- `--disable-version-check`: disable check for latest available version
- `--extended-m3u`: enable non-standard extended m3u headers

### Config file
All the command-line options can be specified in a configuration file. An example of configuration with the strictly required options could look like this:

  ```
  email = my.email@gmail.com
  password = my-secret-password
  device-id = 54bbd32a309a34ef
  ```

When the proxy is launched, it searches for a file named `gmusicproxy.cfg` in the XDG-compliant folders like `/home/USER/.config/` or `/etc/xdg/`. It is possible to specify an arbitrary config file on the command-line using the option `--config`.

### URL-based interface
The only way to use the service is to query the proxy by means of properly formatted HTTP requests over the configured TCP port. Such URLs can be used directly in music programs or in scripts or in any browser. A URL looks like this: `http://host:port/command?param_1=value&param_2=value`. I don't apply any validation to the submitted values: please, be nice with the proxy and don't exploit it! :)

Consider that any song, album, artist, playlist or station got a unique ID in Google Music API but there are many methods to discover them. 

Here a list of the supported requests (with some restricted by the availability of a All Access subscription):

- `/get_collection`: reports an M3U playlist with all the songs in your personal collection.
- `/search_id`: reports the unique ID as result of a search for an artist, a song or an album.
  Allowed parameters:
     - `type`: search for `artist`, `album` or `song` [required]
     - `title`: a string to search in the title of the album or of the song
     - `artist`: a string to search in the name of the artist in any kind of search
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song [default: `no`]
- `/get_by_search`: makes a search for artist/album/song as `/search_id` and returns the related content (an M3U list for the album or for the top songs of an artist and the MP3 file for a song); it is also possible to get the full list of matches reported by Google Music using search with `type=matches` [requires A.A.].
  Allowed parameters:
     - `type`: search for `artist`, `album`, `song` or `matches` [required]
     - `title`: a string to search in the title of the album or of the song
     - `artist`: a string to search in the name of the artist in any kind of search
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song; it doesn't make sense with a search for `matches` [default: `no`]
     - `num_tracks`: the number of top songs to return in a search for artist [default: 20]
- `/get_all_stations`: reports a list of registered stations as M3U playlist (with URLs to other M3U playlist) or as plain-text list (with one station per line)  [requires A.A.].
  Allowed parameters:
     - `format`: `m3u` for an M3U list or `text` for a plain-text list with lines like `Name of the Station|URL to an M3U playlist` [default: `m3u`]
     - `separator`: a separator for the plain-text lists [default: `|`]
     - `only_url`: a `yes` creates a list of just URLs in the plain-text lists (the name of the station is totally omitted) [default: `no`]
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song [default: `no`]
- `/get_all_playlists`: reports the playlists registered in the account as M3U playlist (with URLs to other M3U playlist) or as plain-text list (with one playlist per line).
  The allowed parameters are the same as `/get_all_stations`.
- `/get_new_station_by_search`: reports as M3U playlist the content of a new (transient or permanent) station created on the result of a search for artist/album/song [requires A.A.].
  Allowed parameters:
     - `type`: search for `artist`, `album` or `song` [required]
     - `title`: a string to search in the title of the album or of the song
     - `artist`: a string to search in the name of the artist in any kind of search
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song [default: `no`]
     - `num_tracks`: the number of songs to extract from the new station [default: 20]
     - `transient`: a `no` creates a persistent station that will be registered into the account [default: `yes`]
     - `name`: the name of the persistent station to create [required if `transient` is `no`]
- `/get_new_station_by_id`: reports as M3U playlist the content of a new (transient or permanent) station created on a specified id of an artist/album/song [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the artist/album/song [required]
     - `type`: the type of id specified among `artist`, `album` and `song` [required]
     - `num_tracks`: the number of songs to extract from the new station [default: 20]
     - `transient`: a `no` creates a persistent station that will be registered into the account [default: `yes`]
     - `name`: the name of the persistent station to create [required if `transient` is `no`]
- `/get_station`: reports an M3U playlist of tracks associated to the given station  [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the station [required]
     - `num_tracks`: the number of tracks to extract [default: 20]
- `/get_ifl_station`: reports an M3U playlist of tracks associated to the automatic "I'm feeling lucky" station  [requires A.A.].
  Allowed parameters:
     - `num_tracks`: the number of tracks to extract [default: 20]
- `/get_playlist`: reports the content of a registered playlist in the M3U format.
  Allowed parameters:
     - `id`: the unique identifier of the playlist [required]
- `/get_album`: reports the content of an album as an M3U playlist.
  Allowed parameters:
     - `id`: the unique identifier of the album [required]
- `/get_song`: streams the content of the specified song as a standard MP3 file with IDv3 tag.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]
- `/get_top_tracks_artist`: reports an M3U playlist with the top songs of a specified artist [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the artist [required]
     - `type`: the type of id specified among `artist`, `album` and `song` [required]
     - `num_tracks`: the number of top songs to return [default: 20]
- `/like_song`: reports a positive rating on the song with specified id.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]
- `/dislike_song`: reports a negative rating on the song with specified id.
  Allowed parameters:
     - `id`: the unique identifier of the song [required]

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

## Support
Get this project as it is: I will work on it as long as I have fun in developing and using it. I share it as Open-Source code because I believe in OSS and to open it to external contributions.

Feel free to open [bug reports][4] (complete of verbose output produced with options `--debug` and `--log`) on GitHub, to fork the project and to make [pull requests][5] for your contributions.

### Known problems / Ideas
- It looks that some uploaded MP3 files not present in the GM catalog can't be streamed: to investigate.
- Waiting for recent packaging of Simon's gmusicapi 3.0.0, I could release packages for Debian/Ubuntu systems.

### Limitations
The proxy can manage only one request at time. The internal structure of the proxy can be extended to manage concurrent requests but first I have to investigate about the Google API and gmusicapi limitations on concurrent accesses.

As stated above, you need the device ID of a registered Android device in order to stream the music. This is a requirement of the Google API. An alternative could be to register a virtual-device using the emulator of the Android SDK.

The program was designed under Linux systems but it *could* work also under Windows or Mac OS X. Reports by audacious testers are welcome!


[0]: http://gmusicproxy.net/
[1]: http://www.musicpd.org/
[2]: http://www.videolan.org/vlc/
[3]: https://github.com/simon-weber/Unofficial-Google-Music-API
[4]: https://github.com/diraimondo/gmusicproxy/issues
[5]: https://github.com/diraimondo/gmusicproxy/pulls
[6]: https://github.com/leoedin/gmusicproxy/archive/master.tar.gz
[7]: https://github.com/leoedin/gmusicproxy/archive/master.zip

[![githalytics.com alpha](https://cruel-carlota.pagodabox.com/0642422a568805bba9569fa9c7d83bac "githalytics.com")](http://githalytics.com/diraimondo/gmusicproxy)
