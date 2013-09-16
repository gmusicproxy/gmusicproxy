#gmusicproxy: Google Play Music Proxy

*"Let's stream Google Play Music using any music program"*

© [Mario Di Raimondo](mario.diraimondo@gmail.com)

License: **GPL v3**


## About
This program permits the use of Google Play Music with All Access subscription with any music player that is able to stream MP3 files and M3U playlists (e.g., [MPD server][1], [VLC][2], ...). 

Google has released a nice music service and now it is even more interesting with the All Access option. The Google-way to listen your collection and the stations is by means of Android devices or any web browser. If you want to use your TVs or HiFi audio systems, the main tool is the Chromecast key. I can't buy one (at the moment it is not available in my country) and it looks a bit closed. Even more I already got a music-system based on a PC connected to my HiFi audio system: it is based on [MPD][1] and I would like to continue to use it.

My project is based on the great [Unofficial Google Play Music API][3] of Simon Weber: it already permits to create URLs to stream the tracks as regular MP3 but they expire in 1 minute! This proxy generates persistent URLs that never expire and that you can add to any playlist.

This is not supported nor endorsed by Google. It's aim is the abuse of the service but the one to open the ways to access this great service.

### Features
- create persistent URLs to all the tracks, albums and stations available on the Google Play Music + All Access platform
- get access to all the songs in your collection, playlists as well as to the already registered stations
- search by name any artist, album or song
- request a transient (it will be not registered in your account) station based on any search

## Install
**[TODO]**
### Requirements
- a Google Play Music account with All Access subscription (some functionalities could work even with a free account)
- a **Python** 2.x interpreter
- **gmusicapi** with support to MobileClient and All Access (at the moment you have to use the `develop` branch)
- many other libraries to report here **[TODO]**

## Usage 
With the service running on any computer on the LAN, it can be used by any other of the same LAN. 

To launch the proxy you need the credentials of your Google account: *email* and *password*. If you are are using the 2-factor authentication, you have to create a password-specific password to use with this program. Another required information is the device ID of an Android device: you can discover the one of your devices using the option `--list_devices` on the command-line.

You can provide such necessary information, as well as other options, on the command-line of the program or using a configuration file

### Command-line
Here a list of the supported option on the command-line:
- `--email`: email address of the Google account [required]
- `--password`: password of the Google account [required]
- `--device_id`: the ID of a registered Android device [required]
- `--host`: host in the generated URLs [default: autodetected local ip address]
- `--port`: default TCP port to use [default: 9999]
- `--config`: specific configuration file to use
- `--list_devices`: list the registered devices
- `--debug`: enable debug messages

### Config file
All the command-line options can be specified in a configuration file. A configuration with the strictly required options could look like this:
`email = my.email@google.com
password = my-secret-password
device_id = 54bbd32a309a34ef`
When the proxy is launched it searchs for a file named `gmusicproxy.cfg` on the XDG-compliant folders like `/home/USER/.config/` or `/etc/xdg/`. It is possible to specify an arbitrary config file on the command-line using option `--config`.

### URL-based interface
The only to way to use the service is to query the proxy using properly formatted HTTP requests on the configured port. Such URLs can be used directly in music programs or in scripts or in a browser. A URL looks like this: `http://host:port/command?param_1=value&param_2=value`. Consider that any song, album, artist, playlist or station got an unique ID in GPM API but there are many methods to discover them.

Here a list of the supported requests:
- `/get_collection`: reports an M3U playlist with all the songs in your personal collection.
- `/search_id`: reports the unique ID as result of a search for an artist, a song or an album.
  allowed parameters:

*[TO DO]*

- `/get_all_stations`
- `/get_all_playlists`
- `/get_station`
- `/get_playlist`
- `/get_album`
- `/get_top_tracks_artist`

- `/get_by_search`
- `/get_new_station_by_id`
- `/get_new_station_by_search`
- `/get_song`


### Known problems
- It looks that some uploaded MP3 files not present in the GM catalog can't be streamed: to investigate.

### Limitations
The proxy can manage only one request at time. The internal structure of the proxy can be obviuosly extended to manage concurrent requests but I have to investigate about the Google API and gmusicapi limitations on concurrent accesses.

As stated above, you need the device ID of a registered Android device in order to stream the music. This is a requirement of the Google API. An alternative could be to register a virtual-device using the emulator of the Android SDK.

[1]: http://www.musicpd.org/
[2]: http://www.videolan.org/vlc/
[3]: https://github.com/simon-weber/Unofficial-Google-Music-API



