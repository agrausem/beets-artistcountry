from beets.plugins import BeetsPlugin
from musicbrainzngs.musicbrainz import get_artist_by_id, get_area_by_id


class CountryPlugin(BeetsPlugin):
    pass


def memoize_artist(f):
    cache = {}

    def memf(item):
        artist_id = item['mb_artistid']
        if artist_id not in cache:
            cache[artist_id] = f(item)
        return cache[artist_id]

    return memf


@CountryPlugin.template_field('artist_country')
@memoize_artist
def _tmpl_country(item):
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
            except:
                print("No country for %s" % artist['name'])
                return ''
        return country.lower()
    except Exception as e:
        print(f"Error fetching country for artist {mb_artistid}: {e}")
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
