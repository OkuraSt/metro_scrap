from scrapy import Field, Item
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class Linea(Item):
    clave = Field(output_processor=TakeFirst())
    url_page = Field(output_processor=TakeFirst())
    imagen = Field(output_processor=TakeFirst())
    no_estaciones = Field(output_processor=TakeFirst())
