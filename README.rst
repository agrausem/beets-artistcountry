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

The plugin stores the field `artist_country` on each item when you import it.
To turn this off, add this to your configuration file ::

    artistcountry:
        auto: no

To fill in items you have already imported, run ::

    $> beet artistcountry [QUERY]

Items that already have a country are skipped. Use `-f` to fetch them again.

You can use the field `artist_country` to build your path in your audio
library. Here is an example to do this in your configuration file ::

    paths:
        defaults:
            $albumartist ($artist_country)/[$year] $album%aunique{}/$track $title

Now the path for a track looks like ::

    Metallica (us)/[1984] Ride The Lightning/04 Fade To Black.mp3
