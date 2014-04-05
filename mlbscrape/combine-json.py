import json

def main():
    with open('mlb-walk-up-tracks.json', 'r') as fp:
        tracks = json.load(fp)

    with open('mlb-track-rdio-map.json', 'r') as fp:
        track_map = json.load(fp)

    for track in tracks:
        track_id = track['track_id']
        if track_id in track_map:
            track['rdio_keys'] = track_map[track_id]
        else:
            track['rdio_keys'] = []

    with open('mlb-tracks-combined.json', 'w') as fp:
        json.dump(tracks, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    main()
