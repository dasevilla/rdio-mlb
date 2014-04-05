from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider

from mlbscrape.items import MLBTrack

MLB_TEAMS = [
    ("Los Angeles Angels of Anaheim", "LAA"),
    ("Los Angeles Dodgers", "LAD"),
    ("Arizona Diamondbacks", "ARI"),
    ("Atlanta Braves", "ATL"),
    ("Baltimore Orioles", "BAL"),
    ("Boston Red Sox", "BOS"),
    ("Chicago Cubs", "CHC"),
    ("Chicago White Sox", "CWS"),
    ("Cincinnati Reds", "CIN"),
    ("Cleveland Indians", "CLE"),
    ("Colorado Rockies", "COL"),
    ("Detroit Tigers", "DET"),
    ("Florida Marlins", "MIA"),
    ("Houston Astros", "HOU"),
    ("Kansas City Royals", "KC"),
    ("Milwaukee Brewers", "MIL"),
    ("Minnesota Twins", "MIN"),
    ("New York Mets", "NYM"),
    ("New York Yankees", "NYY"),
    ("Oakland Athletics", "OAK"),
    ("Philadelphia Phillies", "PHI"),
    ("Pittsburgh Pirates", "PIT"),
    ("San Diego Padres", "SD"),
    ("San Francisco Giants", "SF"),
    ("Seattle Mariners", "SEA"),
    ("St. Louis Cardinals", "STL"),
    ("Tampa Bay Rays", "TB"),
    ("Texas Rangers", "TEX"),
    ("Toronto Blue Jays", "TOR"),
    ("Washington Nationals", "WAS"),
]

class MLBSpider(Spider):
    name = "mlb"
    allowed_domains = ["m.mlb.com"]

    def __init__(self, category=None):
        self.failed_urls = []
        self.max_id = 100

    def get_id(self):
        self.max_id += 1
        return "mlb-track-%s" % self.max_id

    def start_requests(self):
        req_list = []
        for name, abbr in MLB_TEAMS:
            req = Request(
                'http://m.mlb.com/%s/fans/music/' % abbr.lower(),
                meta={
                    'mlb_team': (name, abbr),
                }
            )
            req_list.append(req)
        return req_list

    def parse(self, response):
        if response.status == 404:
            print '404', response.url

        sel = Selector(response)
        tracks = sel.xpath("//section[@class='music_Player Music']//div[@class='info']")
        # tracks = sel.xpath("//section[@class='music_Stadium Music']//div[@class='info']")

        team_name, team_abbr = response.meta['mlb_team']

        mlb_tracks = []
        for track in tracks:
            player = track.xpath("h3/text()").extract()[0]
            track_name = track.xpath("h4/text()").extract()[0]
            artist_name = track.xpath("h5/text()").extract()[0]

            mlb_track = MLBTrack(
                track_id=self.get_id(),
                player=player,
                track_name=track_name,
                artist_name=artist_name,
                team_abbr=team_abbr
            )
            mlb_tracks.append(mlb_track)

        return mlb_tracks
