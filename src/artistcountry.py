from beets.plugins import BeetsPlugin
from beets import mediafile
from musicbrainzngs.musicbrainz import get_artist_by_id

class CountryPlugin(BeetsPlugin):
    pass
      
def memoize_artist(f):
    cache = {}
    def memf(item):
        artist_id = item.record['mb_artistid']
        if artist_id not in cache:
            cache[artist_id] = f(item)
        return cache[artist_id]
    return memf

@CountryPlugin.template_field('artist_country')
@memoize_artist
def _tmpl_country(item):
    artist_item = get_artist_by_id(item.record['mb_artistid'])
    artist_country = artist_item['artist'].get('country', '')
    if not artist_country:
        print "No country for %s" % artist_item['artist']['name']
        return ''
    return artist_country.lower()
