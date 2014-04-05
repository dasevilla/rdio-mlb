# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MLBTrack(Item):
    track_id = Field()
    player = Field()
    track_name = Field()
    artist_name = Field()
    team_abbr = Field()
