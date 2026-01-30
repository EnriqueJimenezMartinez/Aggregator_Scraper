"""
Spider para El País usando solo selectores XPath
Extrae: título, fecha, URL y body
"""
import scrapy
from datetime import datetime


class ElPaisSpider(scrapy.Spider):
    name = "elpais"
    allowed_domains = ["elpais.com"]
    start_urls = [
        "https://elpais.com/",
    ]
    
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    def parse(self, response):
        """
        Parsea la página principal de El País
        Usa SOLO selectores XPath
        """
        # Selector XPath para los artículos
        articles = response.xpath('//article[contains(@class, "c")]')

        links = []
        for article in articles:
            link = article.xpath('.//h2/a/@href | .//a[contains(@class, "c_t")]/@href').get()
            if link:
                if not link.startswith('http'):
                    link = response.urljoin(link)
                if link not in links:
                    links.append(link)
            if len(links) >= 10:
                break

        for link in links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get() or response.css('title::text').get()
        date = response.css('time::attr(datetime), time::text').get()
        body_parts = response.css('article p::text').getall()

        if title:
            title = ' '.join(title.split()).strip()
        if date:
            date = date.strip()

        body = ' '.join([p.strip() for p in body_parts if p.strip()])

        yield {
            'source': 'El País',
            'title': title or 'N/A',
            'date': date or datetime.now().strftime('%Y-%m-%d'),
            'url': response.url,
            'body': body or 'N/A',
        }
