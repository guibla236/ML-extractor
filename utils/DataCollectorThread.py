import threading
import time
import threading
from . import app as utils

class DataCollector(threading.Thread):
    def __init__(self, url, total_data):
        self.url = url
        self.total_data = total_data
        self.collected_data = None
        self.processed_data = None
        self.finished = False
        self.link = None
        super().__init__()

    def run(self):
        import requests
        from bs4 import BeautifulSoup
        """
        Acá se transforman todos los parámetros en un link
        y se extrae toda la información de todas las páginas
        y artículos disponibles.
        """
        
        self.processed_data = 0
        next_link = ""
        cotizacion = utils.get_cotizacion()
        
        elements = []

        while(next_link is not None):
            if self.processed_data != 0:
                self.url = next_link
            
            r = requests.get(self.url)         

            soup = BeautifulSoup(r.content, 'lxml')

            lista_productos = soup.select('.ui-search-layout__item')
            
            num_in_list = 0
            for producto in lista_productos:
                num_in_list += 1

                currencies = utils.currency(producto.select('.price-tag-symbol')[0].text,
                                       float(producto.select(
                                           '.price-tag-fraction')[0].text.replace('.', '')),
                                       cotizacion)
                self.link = producto.select(
                            ".ui-search-result__image a")[0].get("href")
                detailed_data = utils.get_detailed_data(BeautifulSoup(requests.get(self.link).content,
                                                                      "lxml"))

                elem = {'titulo': producto.select("h2")[0].text,
                        'currency': producto.select('.price-tag-symbol')[0].text,
                        'pesos': currencies[0],
                        'dolares': currencies[1],
                        'vendedor': detailed_data.get("seller_and_amount_solded")[0],
                        'ventas': detailed_data.get("seller_and_amount_solded")[1],
                        'caract_bas': detailed_data.get("basic_features"),
                        'caract_det': detailed_data.get("detailed_features"),
                        'link': self.link}
                
                elements.append(elem)
                self.processed_data += 1
            try:
                next_link = soup.select('.andes-pagination__button--next a')[0].get("href")
            except IndexError:
                next_link = None
            
            
            
        self.collected_data = elements
        self.finished = True