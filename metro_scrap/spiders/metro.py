# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from metro_scrap.items.Estacion import Estacion



class MetroSpider(Spider):
    name = 'metro'

    def start_requests(self):
        urls = [
            'https://es.wikipedia.org/wiki/Metro_de_la_Ciudad_de_M%C3%A9xico',
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        l_cont = response.css('.infobox tr:nth-child(16) td')
        l_elements = l_cont.css('a')
        for i in xrange(len(l_elements)):
            url_linea = l_elements[i].xpath('@href').extract_first()
            next_page = response.urljoin(url_linea)
            yield Request(next_page, callback=self.parse_linea)

    def parse_linea(self, response):
        # page = response.url.split('/')
        # print(page)

        # Obtener informacion de linea
        # Clave
        clave_linea = response.css('#firstHeading::text').extract_first().split(' ')[1]
        print(clave_linea)

        # Tabla de estaciones
        tabla_estaciones = response.css('.wikitable')

        # Para cada estacion
        for estacion in tabla_estaciones.css('tr'):
            datos = estacion.css('td')
            if len(datos):
                url_estation = datos[0].css('a::attr(href)').extract_first()

                next_page = response.urljoin(url_estation)

                # Request para pprocesar pagina de estacion
                request = Request(next_page, callback=self.parse_estation)
                # Extrae informacion de estacion
                nombre = datos[0].css('a::text').extract_first()
                inauguracion = datos[1].css('a::text').extract_first()
                delegacion = datos[2].css('a::text').extract_first()

                # incluir informacion para el procesado de la estacion
                request.meta['clave_linea'] = clave_linea
                request.meta['nombre'] = nombre
                request.meta['inauguracion'] = inauguracion
                request.meta['delegacion'] = delegacion
                yield request

        # e_elements = response.css('.wikitable td:nth-child(1)')
        # for estation in e_elements:
        #     url_estation = estation.css('a').xpath('@href').extract_first()
        #     next_page = response.urljoin(url_estation)
        #     yield Request(next_page, callback=self.parse_estation)

    def parse_estation(self, response):
        page = response.url.split('/')
        loader = ItemLoader(item=Estacion(), response=response)

        # informacion de conexiones
        conexiones = response.css('.infobox table')
        conexion = conexiones[0]

        # linea
        image = conexion.css('tr')[0].css('td')[3].css('a.image').extract()

        # direccion down
        direccion_down = conexion.css('tr')[0].css('td')[1].css('b a')
        if direccion_down:
            direccion_down.extract()

        # direccion_up
        direccion_up = conexion.css('tr')[0].css('td')[5].css('b a')
        if direccion_up:
            direccion_up.extract()

        print(image)
        print(direccion_down)
        print(direccion_up)
        print(page)
