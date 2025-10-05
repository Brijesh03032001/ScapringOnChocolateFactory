from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose


class ChocolateProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    price_in = MapCompose(lambda x: x.replace("£", "").strip(), float)
    link_in = MapCompose(lambda x: "https://www.chocolate.co.uk" + x)
