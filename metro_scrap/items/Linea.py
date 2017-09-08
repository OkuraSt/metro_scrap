from scrapy import Field, Item
from scrapy.loader.processors import Join, MapCompose, TakeFirst


def try_parse_int(value):
    try:
        return int(value)
    except ValueError:
        return None


class Linea(Item):
    clave = Field(output_processor=TakeFirst())
    url_page = Field(output_processor=TakeFirst())
    imagen = Field(output_processor=TakeFirst())
    no_estaciones = Field(output_processor=TakeFirst(), input_processor=MapCompose(try_parse_int))
