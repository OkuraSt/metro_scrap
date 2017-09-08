# -*- coding: utf-8 -*-
from urllib.parse import urlparse

from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from metro_scrap.items.Estacion import Estacion
from metro_scrap.items.Linea import Linea


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
        for i in range(len(l_elements)):
            url_linea = l_elements[i].xpath('@href').extract_first()
            next_page = response.urljoin(url_linea)
            request = Request(next_page, callback=self.parse_linea)
            yield request

    def parse_linea(self, response):
        linea_item_loader = ItemLoader(item=Linea(), response=response)

        # Informacion de linea
        # ---------------------------
        # clave
        # url_page
        # nombre
        # imagen
        # no_estaciones
        clave_linea = response.css('#firstHeading::text').extract_first().split(' ')[1]
        url_page = urlparse(response.url).path

        linea_item_loader.add_value('clave', clave_linea)
        linea_item_loader.add_value('url_page', url_page)
        linea_item_loader.add_xpath('imagen', '//*[@id="mw-content-text"]/div/table[1]/tr[2]//img/@src')
        linea_item_loader.add_xpath('imagen', '//*[@id="mw-content-text"]/div/table[2]/tr[2]//img/@src')
        linea_item_loader.add_xpath('no_estaciones',
                                    '//th[contains(text(),"Estaciones")]/following-sibling::td/text()')

        yield linea_item_loader.load_item()

        # Tabla de estaciones
        tabla_estaciones = response.css('.wikitable')[0]

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
        estacion_item_loader = ItemLoader(item=Estacion(), response=response)

        # Informacion de estacion
        # ---------------------------
        # linea
        # url_page
        # nombre
        # latitud_dms
        # longitud_dms
        # latitud_dec
        # longitud_dec

        # Informacion general
        info_general = estacion_item_loader.nested_xpath('//*[@id="mw-content-text"]/div/table[1]')

        linea = response.meta['clave_linea']
        url_page = urlparse(response.url).path
        nombre = response.xpath('//*[@id="mw-content-text"]/div/table[1]/tr[1]/th/text()').extract()

        estacion_item_loader.add_value('linea', linea)
        estacion_item_loader.add_value('nombre', nombre)
        estacion_item_loader.add_value('url_page', url_page)

        estacion_item_loader.add_css('latitud_dms', '.geo-dms .latitude::text')
        estacion_item_loader.add_css('longitud_dms', '.geo-dms .longitude::text')

        estacion_item_loader.add_css('latitud_dec', '.geo-dec .latitude::text')
        estacion_item_loader.add_css('longitud_dec', '.geo-dec .longitude::text')

        # informacion de conexiones
        conexiones = response.css('.infobox table')
        conexion = conexiones[0]

        image = conexion.css('tr')[0].css('td')[3].css('a.image').extract_first()

        # direccion down
        direccion_down = conexion.css('tr')[0].css('td')[1].css('b a')
        if direccion_down:
            direccion_down.extract()

        # direccion_up
        direccion_up = conexion.css('tr')[0].css('td')[5].css('b a')
        if direccion_up:
            direccion_up.extract()

        yield estacion_item_loader.load_item()
        # print(image)
        # print(direccion_down)
        # print(direccion_up)
        # print(page)
