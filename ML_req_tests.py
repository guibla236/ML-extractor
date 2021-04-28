#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:40:59 2021

@author: guillermo
"""
import requests
from bs4 import BeautifulSoup
import re

url = "https://articulo.mercadolibre.com.uy/MLU-454017162-cafetera-6-tazas-filtro-permanente-cafe-molido-xion-cm6-dimm-_JM?searchVariation=70162183105#searchVariation=70162183105&position=1&type=item&tracking_id=47ed14fd-9fc4-4a9c-88ea-657071fe1a9e"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

def get_solded(soup_element):
    """
    Soup element is the element with the complete page transformed with the instruction
    soup_element = BeautifulSoup(r.content,'html5lib')
    Where r.content is requests.get(article_url)
    """

    vendidos = re.findall(r'\d+', soup.select('.ui-pdp-subtitle')[0].text)
    if len(vendidos) == 0:
        vendidos = 0
    else:
        vendidos = int(''.join(re.findall(r'\d+', soup.select('.ui-pdp-subtitle')[0].text)))
    return vendidos


def get_basic_features(soup_element):
    """
    Soup element is the element with the complete page transformed with the instruction
    soup_element = BeautifulSoup(r.content,'html5lib')
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
    soup_element = BeautifulSoup(r.content,'html5lib')
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


        



