import scrapy

class LapolloSpider(scrapy.Spider):
    name = "lapollo"
    allowed_domains = ["lapollo.fr"]
    start_urls = ["https://www.lapollo.fr"]

    def parse(self, response):
        # Extrait le titre principal
        title = response.css('h1::text').get()
        
        # Extrait les liens du menu principal
        menu_items = response.css('nav.main-navigation a::text').getall()
        
        # Extrait les titres des articles ou sections principales
        article_titles = response.css('h2::text').getall()
        
        # Extrait les liens vers les pages internes
        internal_links = response.css('a[href^="/"]::attr(href)').getall()

        yield {
            'title': title,
            'menu_items': menu_items,
            'article_titles': article_titles,
            'internal_links': internal_links
        }

        # Suivre les liens internes pour un crawl plus approfondi
        for link in internal_links:
            yield response.follow(link, self.parse)
