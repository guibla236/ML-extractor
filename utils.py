#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 14:56:37 2021

@author: guillermo
"""


def get_cotizacion():
    import requests
    from bs4 import BeautifulSoup
    import cchardet

    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    url = "http://www.ine.gub.uy/cotizacion-de-monedas"
    r = requests.get(url,headers=headers,verify=False)
    soup = BeautifulSoup(r.content, 'lxml')
    columna = soup.find_all(text="Dolar USA")[1]
    
    print("Cotización tomada del INE con fecha: "+columna.parent.parent.select("td")[1].text)
    compra = float(columna.parent.parent.select("td")[2].text)
    venta = float(columna.parent.parent.select("td")[3].text)
    
    return (compra, venta)

def moneda (texto, valor, cotizacion):
    dolar_compra = cotizacion[0]
    dolar_venta = cotizacion[1]
    
    if (texto=="$"): return (valor, valor/dolar_compra)
    
    elif (texto =="U$S"): return (dolar_venta*valor, valor)

    else: 
        print ("Hay un error en un artículo que vale "+ texto + valor)
        return None


def print_options(elementos):
    text = '\nOpción 0: Cancelar'

    for i in elementos.keys():
        text += "\nOpción " + str(i+1) + ": " + elementos.get(i)[0]
    return text

def apply_filters(url):
    import requests
    from bs4 import BeautifulSoup
    import cchardet

    keep_filtering = True
    primer_iteracion = True

    while(keep_filtering):
        if primer_iteracion == True:
            print("Ahora filtraremos los resultados para que sean más precisos y demore menos en generarlos.")
            primer_iteracion = False
        else:
            print("\n\n\nSe aplicó el filtro de "+options.get(int(option_selected)-1)[0]+": "+filters.get(int(filter_selected)-1)[0])
            print("\nCuántos más filtros, mejor:\n")
        
        
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'lxml')

        options_element = soup.select('.ui-search-filter-groups .ui-search-filter-dl .ui-search-filter-dt-title')[1:]
        
        options = [(i.text, i) for i in options_element]

        options = {v:k for v, k in enumerate(options)}

        option_selected = input("Ingrese el número de categoría de búsqueda entre las siguientes: "+print_options(options)+"\n[*]: ")
        
        while int(option_selected)-1 not in options.keys() and int(option_selected) != 0:
            print("\n\nOpción inválida. Intente nuevamente.")
            option_selected = input(print_options(options)+"\n[*]: ")

        if int(option_selected) == 0:
            keep_filtering = False
            break
            
        filter_element = options.get(int(option_selected)-1)[1].parent

        filters = [(i.text, i) for i in filter_element.select(".ui-search-filter-name")]
        filters = {v:k for v,k in enumerate(filters)}

        filter_selected = input("Ahora seleccione el número de filtro de interés dentro de la categoría indicada: "+print_options(filters)+"\n[*]: ")
        
        while int(filter_selected)-1 not in filters.keys() and int(filter_selected) != 0:
            print("\n\nOpción inválida. Intente nuevamente.")
            filter_selected = input(print_options(filters)+"\n[*]: ")
        
        if int(filter_selected) == 0:
            keep_filtering = False
            break

        url = filters.get(int(filter_selected)-1)[1].parent.get("href")

    return url

def get_seller_and_amount_solded(soup_element):
    """
    Soup element is the element with the complete page transformed with the instruction
    soup_element = BeautifulSoup(r.content,'lxml')
    Where r.content is requests.get(article_url)
    """
    import re
    
    vendedor = soup_element.select('.ui-pdp-seller__link-trigger')[0].text

    vendidos = re.findall(r'\d+', soup_element.select('.ui-pdp-subtitle')[0].text)
    if len(vendidos) == 0:
        vendidos = 0
    else:
        vendidos = int(''.join(re.findall(r'\d+', soup_element.select('.ui-pdp-subtitle')[0].text)))
    
    return [vendedor, vendidos]


def get_basic_features(soup_element):
    """
    Soup element is the element with the complete page transformed with the instruction
    soup_element = BeautifulSoup(r.content,'lxml')
    Where r.content is requests.get(article_url)
    """
    basic_features_elements = soup_element.select(".ui-vpp-highlighted-specs__key-value")
    basic_features = {}

    for element in basic_features_elements:
        feature = element.select("p span")
        basic_features[feature[0].text[:-1].lower()] = feature[1].text.lower()
    
    return basic_features

def get_detailed_features(soup_element):
    """
    Soup element is the element with the complete page transformed with the instruction
    soup_element = BeautifulSoup(r.content,'lxml')
    Where r.content is requests.get(article_url)
    """
    detailed_features_elements = soup_element.select(".andes-table")
    detailed_features = {}

    for element in detailed_features_elements:
        feature_name = element.select("thead")[0].text 
        feature_row = {}
        for row in element.select("tbody tr"):
            feature_row[row.select("th")[0].text] = row.select("td")[0].text
        
        detailed_features[feature_name] = feature_row 
    
    return detailed_features

def get_detailed_data(soup_element):
    """
    This function gives all the data that is inside the article page
    Soup element is the element with the complete page transformed with the instruction
    soup_element = BeautifulSoup(r.content,'lxml')
    Where r.content is requests.get(article_url)
    """
    result = {}
    result["seller_and_amount_solded"] = get_seller_and_amount_solded(soup_element)
    result["basic_features"] = get_basic_features(soup_element)
    result["detailed_features"] = get_detailed_features(soup_element)

    return result
