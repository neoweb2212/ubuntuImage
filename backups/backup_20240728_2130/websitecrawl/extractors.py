from abc import ABC, abstractmethod
import re

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, response):
        pass

class ExtractorManager:
    def __init__(self):
        self.extractors = {}

    def register_extractor(self, name, extractor_class):
        if not issubclass(extractor_class, BaseExtractor):
            raise ValueError(f"{extractor_class.__name__} is not a subclass of BaseExtractor")
        self.extractors[name] = extractor_class()

    def get_extractor(self, name):
        extractor = self.extractors.get(name)
        if not extractor:
            raise ValueError(f"No extractor registered for '{name}'")
        return extractor

extractor_manager = ExtractorManager()

class EmailExtractor(BaseExtractor):
    def extract(self, response):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, response.text)

class PriceExtractor(BaseExtractor):
    def extract(self, response):
        prices = response.css('span.price::text').getall()
        return [price.strip() for price in prices if price.strip()]

# Enregistrement des extracteurs
extractor_manager.register_extractor('email', EmailExtractor)
extractor_manager.register_extractor('price', PriceExtractor)
