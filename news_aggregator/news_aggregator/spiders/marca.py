"""
Spider para Marca usando selectores mixtos (CSS y XPath)
Extrae: título, fecha, URL y body
"""
import scrapy
from datetime import datetime


class MarcaSpider(scrapy.Spider):
    name = "marca"
    allowed_domains = ["marca.com"]
    start_urls = [
        "https://www.marca.com/",
    ]

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "DOWNLOAD_DELAY": 2,
    }

    def parse(self, response):
        """
        Parsea la portada de Marca
        Usa selectores mixtos (CSS y XPath)
        """
        articles = response.css("article")

        links = []
        for article in articles:
            link = article.xpath(".//a/@href").get()
            if link:
                if not link.startswith("http"):
                    link = response.urljoin(link)
                if link not in links:
                    links.append(link)
            if len(links) >= 10:
                break

        for link in links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title = response.css("h1::text").get() or response.css("title::text").get()
        date = response.css("time::attr(datetime), time::text").get()
        body_parts = response.css("article p::text").getall()

        if title:
            title = " ".join(title.split()).strip()
        if date:
            date = date.strip()

        body = " ".join([p.strip() for p in body_parts if p.strip()])

        yield {
            "source": "Marca",
            "title": title or "N/A",
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "url": response.url,
            "body": body or "N/A",
        }