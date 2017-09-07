from scrapy import Field, Item
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


class Estacion(Item):
    linea = Field(output_processor=TakeFirst())
    url_page = Field(output_processor=TakeFirst())
    nombre = Field(output_processor=TakeFirst())
    latitud_dms = Field(output_processor=TakeFirst())
    longitud_dms = Field(output_processor=TakeFirst())
    latitud_dec = Field(output_processor=TakeFirst())
    longitud_dec = Field(output_processor=TakeFirst())
