import beets
import musicbrainzngs
from beets import logging, ui
from beets.dbcore import types
from beets.plugins import BeetsPlugin
from musicbrainzngs.musicbrainz import get_artist_by_id, get_area_by_id

log = logging.getLogger('beets.artistcountry')


class CountryPlugin(BeetsPlugin):
    item_types = {'artist_country': types.STRING}

    def __init__(self):
        super(CountryPlugin, self).__init__()
        self.config.add({'auto': True})
        # beets 2.x no longer sets a user agent for musicbrainzngs, which
        # refuses to send requests without one.
        musicbrainzngs.set_useragent('beets', beets.__version__,
                                     'https://beets.io/')
        if self.config['auto']:
            self.import_stages = [self.imported]

    def commands(self):
        cmd = ui.Subcommand('artistcountry',
                            help=u'fetch the country of artists from MusicBrainz')
        cmd.parser.add_option(
            '-f', '--force', action='store_true', default=False,
            help=u'fetch the country again when it is already set')

        def func(lib, opts, args):
            for item in lib.items(args):
                if opts.force or not item.get('artist_country'):
                    fetch_country(item)

        cmd.func = func
        return [cmd]

    def imported(self, session, task):
        for item in task.imported_items():
            fetch_country(item)


def fetch_country(item):
    country = _artist_country(item)
    if country:
        item['artist_country'] = country
        item.store()


def memoize_artist(f):
    cache = {}

    def memf(item):
        artist_id = item['mb_artistid']
        if artist_id not in cache:
            cache[artist_id] = f(item)
        return cache[artist_id]

    return memf


@memoize_artist
def _artist_country(item):
    mb_artistid = item['mb_artistid']

    # Check if we have a valid MusicBrainz UUID (not Spotify ID)
    if not mb_artistid or len(mb_artistid) != 36 or mb_artistid.count('-') != 4:
        return ''

    try:
        artist_item = get_artist_by_id(mb_artistid)
        artist = artist_item['artist']
        country = artist.get('country', '')
        if not country:
            try:
                country = _country_from_area(artist['area'])
            except (KeyError, IndexError):
                log.info(u'No country for {0}', artist['name'])
                return ''
        log.info(u'{0}: {1}', artist['name'], country.lower())
        return country.lower()
    except musicbrainzngs.WebServiceError as e:
        log.warning(u'Error fetching country for artist {0}: {1}',
                    mb_artistid, e)
        return ''


def _country_from_area(area):
    countries = _find_top_area(area)
    return countries[0]


def _find_top_area(area):
    new_area = get_area_by_id(area['id'], includes=['area-rels'])
    new_area = [
        a['area'] for a in new_area['area']['area-relation-list']
        if a.get('direction', '') == 'backward'
    ]

    if not new_area:
        return area['iso-3166-1-code-list']

    area = new_area[0]
    if _has_country_iso_code(area):
        return area['iso-3166-1-code-list']

    return _find_top_area(area)


def _has_country_iso_code(area):
    return area['type'] == "Country" and "iso-3166-1-code-list" in area
