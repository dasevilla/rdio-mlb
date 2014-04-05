# MLB Walk-Up Songs

Listen to the walk-up songs from your favorite MLB team.

Built at [Bitcamp 2014](https://bitca.mp/) using the [Rdio API](http://www.rdio.com/developers/).


## Usage

    cd mlbscrape

Crawl m.mlb.com for walk-up tracks:

    scrapy crawl mlb -o mlb-walk-up-tracks.json -t json

Use The Echo Nest to convert track text to Rdio keys:

    python echonest-map.py

Add Rdio track keys to the JSON file:

    python combine-json.py

Copy it to the web app:

    cp mlb-tracks-combined.json ../webapp/js/

Update GitHub page

    git checkout gh-pages
    git archive master | tar x --strip=1 webapp
