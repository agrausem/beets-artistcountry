beets-artistcountry
===================

Beets plugin to retrieve the country of an artist from Musicbrainz

Install
-------

To install, use `pip` ::

    $> pip install beets-artistcountry

To activate it, add `artistcountry` to the list of you plugins in your
configuration file (config.yaml) ::

    plugins: [...] artistcountry [...]


How to use it
-------------

You can now use the template field `artist_country` to build your path in your
audio library. Here is an example to do this in your configuration file ::

    paths:
        defaults:
            $albumartist ($artist_country)/[$year] $album%aunique{}/$track $title

Now the path for a track looks like ::

    Metallica (us)/[1984] Ride The Lightning/04 Fade To Black.mp3
