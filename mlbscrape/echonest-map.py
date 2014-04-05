import httplib
import logging
import time
import json

from pyechonest import config as echo_nest_config, catalog as echo_nest_catalog


echo_nest_config.ECHO_NEST_API_KEY = 'G0AGBL9AYFHPWBNPB'

RDIO_API_TOKEN = 'REPLACE_ME'
ECHO_NEST_SLEEP = 10
ECHO_NEST_BUCKET = 'id:rdio-US'
RDIO_API_URL = 'https://www.rdio.com/api/1/'


def get_tracks():
    with open('mlb-walk-up-tracks.json', 'r') as f:
        return json.load(f)


def update_catalog(catalog_name, tracks):
    """Adds the ``tracks`` to the Echo Nest catalog named ``catalog_name``."""

    logger = logging.getLogger('catalog-updater')

    catalog = echo_nest_catalog.Catalog(catalog_name, type='song')

    items = []
    for track in tracks:
        items.append({
            'action': 'update',
            'item': {
                'item_id': str(track['track_id']),
                'song_name': track['track_name'],
                'artist_name': track['artist_name'],
            }
        })

    catalog_ticket = catalog.update(items)
    logger.info('Updated catalog named "%s" and got ticket "%s"', catalog_name,
                catalog_ticket)

    return catalog_ticket


def check_catalog_status(catalog_name, catalog_ticket):
    """Polls catalog ticket and blocks until it's finished."""
    logger = logging.getLogger('catalog-check')

    catalog = echo_nest_catalog.Catalog(catalog_name, type='song')

    completed = False
    while not completed:
        time.sleep(ECHO_NEST_SLEEP)
        catalog_status = catalog.status(catalog_ticket)
        completed = catalog_status['ticket_status'] == 'complete'
        logger.info('Catalog %s, ticket %s, status %s', catalog_name,
                    catalog_ticket, catalog_status['ticket_status'])


def dump_catalog(catalog_name):
    """Songs can be: Unknown, Identified, Found"""

    catalog = echo_nest_catalog.Catalog(catalog_name, type='song')

    found_rdio_tracks = {}
    items = catalog.get_item_dicts(results=700, buckets=[ECHO_NEST_BUCKET, 'tracks'])
    print 'start', items.start, 'count', len(items), 'total', items.total
    for item in items:
        if 'artist_name' in item:
            print item['artist_name'], '-', item['song_name']

            rdio_track_keys = [track['foreign_id'].split(':')[2] for track in item['tracks']]
            if len(item['tracks']):
                print '\t', 'Found'
                print '\t', ', '.join(rdio_track_keys)
                track_id = item['request']['item_id']
                found_rdio_tracks[track_id] = rdio_track_keys
            else:
                print '\t', 'Identified'
        else:
            print item['request']['artist_name'], '-', item['request']['song_name']
            print '\t', 'Unkonwn'
        print

    return found_rdio_tracks


def main():
    catalog_name = 'mlb-v2'
    tracks = get_tracks()
    catalog_ticket = update_catalog(catalog_name, tracks)
    check_catalog_status(catalog_name, catalog_ticket)
    found_rdio_tracks = dump_catalog(catalog_name)

    with open('mlb-track-rdio-map.json', 'w') as f:
        json.dump(found_rdio_tracks, f, sort_keys=True, indent=2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Python requests logging (requests->urllib3->httplib)
    httplib.HTTPConnection.debuglevel = 0
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARN)
    requests_log.propagate = True

    main()