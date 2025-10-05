import scrapy
import re
from chocolatescraper.items import ChocolatesProduct
from chocolatescraper.itemLoaders import ChocolateProductLoader


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["www.chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css("product-item")

        for product in products:
            chocolate = ChocolateProductLoader(
                item=ChocolatesProduct(), selector=product
            )
            price_texts = product.css("span.price ::text").getall()
            visible = " ".join(
                t.strip() for t in price_texts if t.strip() and "Sale price" not in t
            )
            # extract currency+amount like "£12.34" (fallback to joined visible text)
            m = re.search(r"£\s*[\d,]+(?:\.\d+)?", visible)
            price = m.group(0) if m else visible.strip() or None

            chocolate.add_css("name", "a.product-item-meta__title::text")
            chocolate.add_css(
                "price",
                "span.price",
                re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>',
            )
            chocolate.add_css("link", "div.product-item-meta a::attr(href)")

            yield chocolate.load_item()
        next_page = response.css('[rel="next"]').attrib.get("href")
        if next_page:
            yield response.follow(next_page, self.parse)
