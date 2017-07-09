from scrapy import Field, Item
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


class Estacion(Item):
    linea = Field()
    nombre = Field()
    descripcion = Field()
    latitud = Field()
    longitud = Field()
