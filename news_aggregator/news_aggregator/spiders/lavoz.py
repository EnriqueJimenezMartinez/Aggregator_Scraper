"""
Spider para La Voz de Galicia usando solo selectores CSS
Extrae: título, fecha, autor y descripción
"""
import scrapy
from datetime import datetime


class LaVozSpider(scrapy.Spider):
    name = "lavoz"
    allowed_domains = ["lavozdegalicia.es"]
    start_urls = [
        "https://www.lavozdegalicia.es/",
    ]

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    def parse(self, response):
        """
        Parsea la portada de La Voz de Galicia
        Usa SOLO selectores CSS
        """
        articles = response.css("article")

        links = []
        for article in articles:
            link = article.css("a::attr(href)").get()
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
        title = response.css("title::text").get()
        date = response.css("time::attr(datetime), time::text").get()
        body_parts = response.css("article p::text").getall()

        if title:
            title = " ".join(title.split()).strip()
        if date:
            date = date.strip()

        body = " ".join([p.strip() for p in body_parts if p.strip()])

        yield {
            "source": "La Voz de Galicia",
            "title": title or "N/A",
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "url": response.url,
            "body": body or "N/A",
        }