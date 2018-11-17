# GMusicProxy – Google Play Music Proxy 

*"Let's stream Google Play Music using any media-player"*

https://gmusicproxy.github.io

contributors:
- [Mario Di Raimondo](mailto:mario.diraimondo@gmail.com)
- [Nick Depinet](mailto:depinetnick@gmail.com)
- [Adam Prato](mailto:adam.prato@gmail.com)
- [Pierre Karashchuk](mailto:krchtchk@gmail.com)
- [Alex Busenius](mailto:)
- [Mark Gillespie](mailto:mark.gillespie@gmail.com)

License: **GPL v3**

## About
This program permits the use of Google Play Music with All Access subscription with any music player that is able to stream MP3 files and to manage M3U playlists (e.g., [MPD server][1], [VLC][2], ...). It can work also with a free account without All Access extras.

Google has released a nice music service with the possibility to stream all the available music using the All Access subscription. The Google-way to listen your collection and the stations is by means of Android devices or any web browser. If you want to use your TVs or HiFi audio systems, the main tool is the Chromecast key (or its audio variant). These devices are closed and limited in someway. I already got a music-system at home based on a small Raspberry-PI connected to my HiFi audio system (using a professional DAC): it makes use of [MPD][1] and I wanted to keep it.

My project is based on the great [Unofficial Google Play Music API][3] of Simon Weber: it already permits to create URLs to stream the tracks as regular MP3 but they expire in 1 minute! Keeping this proxy running, it can generate persistent local URLs that never expire and that can be used in any media-player.

This project is not supported nor endorsed by Google. Its aim is not the abuse of the service but the one to improve the access to it. I'm not responsible of its misuse.

### Features
- create persistent URLs to all the tracks, albums and stations available on the Google Play Music + All Access platform
- get access to all the songs in your collection, playlists and registered stations
- search by name any artist, album or song
- request a transient (it will be not registered in your account) station based on any search (a.k.a. "Instant Mix")
- stream any songs as standard MP3 complete of IDv3 tag with all the information and album image

### Changelog
- 1.0.9-beta (unreleased):
  - experimental Python 3 support: soon the support for 2.7 version will be removed (thanks to Pierre Karashchuk)
  - fix issues with missing recording year and with `__get_matches` function
  - less strict version requirement for gmusicapi (easy life for packaging managers)
- 1.0.8 (2017-02-07):
  - daemon-mode is not supported under Windows (but it could be under cygwin...): this allows to run gmusicproxy without the `daemon` module
  - support for on-the-fly shuffling of playlists and collections
  - support for public/shared playlists
  - support filtering collection returned from get_collection by minimum rating (thanks to Mark Gillespie)
  - cache the end of song in RAM in order to prevent some connection timeout errors (thanks to Alex Busenius)
  - possible fix for the long standing bug on the truncated download of some songs
  - support for recording year in IDv3 tag (thanks to redlulz)
  - fix for deadlock in cache management and in ids handling
- 1.0.7 (2017-01-09):
  - possibility to bind to a specific network interface (thanks to fgtham)
  - bug fixes (shoutcast metadata)
  - early release to fix the lack of requirement for gmusicapi 10.1.0 in the setup
- 1.0.6 (2016-12-03):
  - support for concurrent requests (thanks to Pierre Karashchuk)
  - support for HEAD requests
  - better shoutcast headers handling
  - documentation improvements
  - a more robust re-authentication system (thanks to Alex Busenius)
  - new keyring support for desktop computers (thanks to Alex Busenius)
  - supported recent gmusicapi v.10.1.0 (fixed bugs and packaging problems)
  - bug fixes (shoutcast metadata support, content-disposition header, ...)
- 1.0.5 (2016-05-04):
  - send to the client the effective song size: this should allow the player (VLC) to properly show the progress of the playback
  - make HTTP connection for version control more robust: not fatal on error (my HTTP server is down: sorry!)
  - new support to the Shoutcast metadata protocol: at the moment alternative to the IDv3 tag supporto, so disabled by default (thanks to Adam Prato)
- 1.0.4 (2016-02-27):
  - implemented a RAM-based cache for songs list: it speeds-up streaming of songs in collection or if AA is disabled
  - implemented the automatic increment of the playcounts of the fetched songs; the previous behavior can be restored with option `disable-playcount-increment`
- 1.0.3 (2015-12-07):
  - added `Access-Control-Allow-Origin: *` header to allow web-pages to interact with GMusicProxy API
  - bump `gmusicapi` requirement to 7.0.0 to fix validation errors
  - fix in documentation
  - fix/workaround to use python-daemon>=2.1
- 1.0.2 (2015-07-16):
  - added possibility to get the full discography of a specified artist using `get_discography_artist` (thanks to e-matterson for the idea and an attempted implementation)
- 1.0.1 (2015-06-21):
  - switched on gmusicapi 6.0.0
  - the use of a registered device ID is no longer stricly necessary but it is still suggested
- 1.0.0 (2015-06-12):
  - finally fixed the support of uploaded tracks: now GMusicProxy can really work without a paid subscription!
  - code cleanup
  - some bugs squashing
  - now it is possible to support the project with a small [donation][8]
- 0.9.9.2 (2015-06-04):
  - fixed breakage on login due to gmusicapi change (thanks for the pull request to @Mlmlte)
  - reverted on gmusicapi 5.0.0: it was released!
  - restored `--list-devices` functionality moving on new mobileclient `get_registered_devices` function of gmusicapi
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

- Simon's Unofficial-Google-Music-API (the great backend used by gmusicproxy): https://github.com/simon-weber/gmusicapi
- web2py-mpd-gmproxy (a web interface that uses gmusicproxy as backend): https://github.com/matclab/web2py-mpd-gmproxy
- GMusic-MPD (an helper script for GMusicProxy together with MPD): https://github.com/Illyism/GMusic-MPD
- gmproxy-scripts (helper scripts for working with GMusicProxy): https://github.com/kmac/gmproxy-scripts
- gpmplay (a bash script to easily search with GMusicproxy): https://github.com/onespaceman/gmpplay
- g-music (Emacs client for gmusicproxy and mpd): https://github.com/bodicsek/g-music
- GMusicProxyGui (a C# GUI for the GMusicProxy): https://github.com/Poket-Jony/GMusicProxyGui

## Support
### Donations
At the moment I'm looking for another Maintainer for the project. I'll continue to accept [donations][8] as long as I can't find who succeed me just to be able to keep up the Google server subscription.  Many thanks for the donations received in these years. 

### Issues
Feel free to open [bug reports][4] (complete of verbose output produced with options `--debug` and `--log`) on GitHub, to fork the project and to make [pull requests][5] for your contributions.

## Setup
### Requirements
- a Google Play Music account with All Access subscription (some functionalities continue to work even with a free account)
- a **Python** 2.7 interpreter (experimental support for **Python** 3 is included)
- some python libs: *gmusicapi*, *netifaces*, *pyxdg*, *eyed3*, *python-daemon*

### Installation
The following instructions have a Debian/Ubuntu GNU/Linux system as reference: nevertheless they work on any other GNU/Linux system using the right substitute of `apt-get`. It is known to work also on Mac OS X and Windows systems.

In order to build some dependencies, you need for sure a working building system with `sudo apt-get install build-essential python2.7-dev`. It could be useful to add some necessary packages: `sudo apt-get install libffi-dev  libssl-dev`.

- The easiest way, but not suggested, is to use the `pip` command to install the proxy with all the dependencies from PyPI and GitHub repositories:

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

To launch the proxy you need the credentials of your Google account: *email* and *password*. If you are using the 2-factor authentication, you have to create an application-specific password to be used with this program. Another usefull information would be the device ID of an Android/iOS device registered in your account: you can discover it using the option `--list-devices` on the command-line. As default a fake-id, based on the mac address of the main network card of the server running the service, is used.

You can provide such necessary information, as well as other options, on the command-line of the program or using a configuration file.

### Command-line
Here a list of the supported options on the command-line:

- `--email`: email address of the Google account [required]
- `--password`: password of the Google account [required]
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
- `--keyring-backend`: name of the keyring backend to use instead of the default one
- `--list-keyring-backends`: list the available keyring backends
- `--keyring-service`: keyring service to use, takes precedence over `--password` if set
- `--keyring-entry`: keyring entry to use, required if `--keyring-service` is used

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

### URL-based interface
The only way to use the service is to query the proxy by means of properly formatted HTTP requests over the configured TCP port. Such URLs can be used directly in music programs or in scripts or in any browser. A URL looks like this: `http://host:port/command?param_1=value&param_2=value`. I don't apply any validation to the submitted values: please, be nice with the proxy and don't exploit it! :)

Consider that any song, album, artist, playlist or station got a unique ID in Google Music API but there are many methods to discover them.

Here a list of the supported requests (with some restricted by the availability of a All Access subscription):

- `/get_collection`: reports an M3U playlist with all the songs in your personal collection; the resulting list can be shuffled and/or filtered using the rating; note that not all the rated (liked) songs belong to your collection.
  Allowed parameters:
     - `shuffle`: if the collection has to be shuffled [default: no]
	 - `rating`: an integer value (typically between 1-5) to filter out low rated or unrated songs form your collection
- `/search_id`: reports the unique ID as result of a search for an artist, a song or an album.
  Allowed parameters:
     - `type`: search for `artist`, `album` or `song` [required]
     - `title`: a string to search in the title of the album or of the song
     - `artist`: a string to search in the name of the artist in any kind of search
     - `exact`: a `yes` implies an exact match between the query parameters `artist` and `title` and the real data of the artist/album/song [default: `yes`]
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
- `/get_new_station_by_search`: reports as M3U playlist the content of a new (transient or permanent) station created on the result of a search for artist/album/song (a.k.a. "Instant Mix") [requires A.A.].
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
- `/get_playlist`: reports the content of a registered playlist in the M3U format; the list can be also shuffled.
  Allowed parameters:
     - `id`: the unique identifier of the playlist [required]
     - `shuffle`: if the list has to be shuffled [default: no]
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
- `/get_discography_artist`: reports the list of available albums of a specified artist as M3U playlist (with URLs to other M3U playlist) or as plain-text list (with one album per line)  [requires A.A.].
  Allowed parameters:
     - `id`: the unique identifier of the artist [required]
     - `format`: `m3u` for an M3U list or `text` for a plain-text list with lines like `Name of Album|Year|URL to an M3U playlist` [default: `m3u`]
     - `separator`: a separator for the plain-text lists [default: `|`]
     - `only_url`: a `yes` creates a list of just URLs in the plain-text lists (the name of the album is totally omitted) [default: `no`]
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


[0]: http://gmusicproxy.net/
[1]: http://www.musicpd.org/
[2]: http://www.videolan.org/vlc/
[3]: https://github.com/simon-weber/gmusicapi
[4]: https://github.com/diraimondo/gmusicproxy/issues
[5]: https://github.com/diraimondo/gmusicproxy/pulls
[6]: https://github.com/leoedin/gmusicproxy/archive/master.tar.gz
[7]: https://github.com/leoedin/gmusicproxy/archive/master.zip
[8]: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=mario%2ediraimondo%40gmail%2ecom&lc=US&item_name=GMusicProxy%20support&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_SM%2egif%3aNonHosted

![ga tracker](https://www.google-analytics.com/collect?v=1&a=257770996&t=pageview&dl=https%3A%2F%2Fgithub.com%2Fdiraimondo%2Fgmusicproxy&ul=en-us&de=UTF-8&cid=978224512.1377738459&tid=UA-3018229-6&z=887657232 "ga tracker")
