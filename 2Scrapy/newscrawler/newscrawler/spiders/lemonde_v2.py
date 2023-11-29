import scrapy
from scrapy import Request


class LemondeSpider(scrapy.Spider):
    name = "lemondev2"
    allowed_domains = ["www.lemonde.fr"]
    start_urls = ['https://www.lemonde.fr']

    def parse(self, response):
        title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css("#nav-markup .Nav__item")[3].css("a::text").extract(),
            response.css("#nav-markup .Nav__item")[3].css("a::attr(href)").extract())
        }
        yield {
            "title":title,
            "all_links":all_links
        }

    def parse_category(self, response):
        for article in response.css(".river")[0].css(".teaser"):
            title = self.clean_spaces(article.css("h3::text").extract_first())
            image = article.css("img::attr(data-src)").extract_first()
            description = article.css("p::text").extract_first()
            yield {
                "title": title,
                "image": image,
                "description": description
            }
    def clean_spaces(string_):
        if string_ is not None:
            return " ".join(string_.split())