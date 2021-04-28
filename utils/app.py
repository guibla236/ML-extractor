

def get_options_and_applied_filters(url):
    import requests
    from bs4 import BeautifulSoup
    import re

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    total_data = int(''.join(
        re.findall(r'\d+', soup.select(
            '.ui-search-search-result__quantity-results')[0].text)))

    options_element = soup.select(
        '.ui-search-filter-groups .ui-search-filter-dl .ui-search-filter-dt-title')[1:]
    options = []
    search_options = {}
    for option in options_element:
        options.append(option.text)

        filters_elements = option.parent.select(".ui-search-filter-container")

        filters = {}

        for elements in filters_elements:
            filters[elements.select(".ui-search-filter-name")
                    [0].text] = elements.select("a")[0].get("href")

        search_options[option.text] = filters

    applied_filters_element = soup.select(".ui-search-applied-filters")
    applied_filters = {}

    if len(applied_filters_element) != 0:
        applied_filters_element = applied_filters_element[0]

        for element in applied_filters_element.select(".andes-tag"):
            applied_filters[element.text] = element.parent.get("href")
    
    result = {'search_options': search_options,
              'applied_filters': applied_filters,
              'total_data': total_data}

    return result


def get_search_link(query):
    return "https://listado.mercadolibre.com.uy/"+query+"#D[A:"+query+"]"


def get_cotizacion():
    import requests
    from bs4 import BeautifulSoup
    import cchardet

    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    url = "http://www.ine.gub.uy/cotizacion-de-monedas"
    r = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(r.content, 'lxml')
    columna = soup.find_all(text="Dolar USA")[1]

    print("Cotización tomada del INE con fecha: " +
          columna.parent.parent.select("td")[1].text)
    compra = float(columna.parent.parent.select("td")[2].text)
    venta = float(columna.parent.parent.select("td")[3].text)

    return (compra, venta)


def moneda(texto, valor, cotizacion):
    dolar_compra = cotizacion[0]
    dolar_venta = cotizacion[1]

    if (texto == "$"):
        return (valor, valor/dolar_compra)

    elif (texto == "U$S"):
        return (dolar_venta*valor, valor)

    else:
        print("Hay un error en un artículo que vale " + texto + valor)


def get_seller_and_amount_solded(soup_element):
    """
    Soup element is the element with the complete page transformed with the instruction
    soup_element = BeautifulSoup(r.content,'lxml')
    Where r.content is requests.get(article_url)
    """
    import re
    try:
        vendedor = soup_element.select('.ui-pdp-seller__link-trigger')[0].text
    except:
        vendedor = "[no divulgado]"
    try:
        vendidos = re.findall(
            r'\d+', soup_element.select('.ui-pdp-subtitle')[0].text)
        vendidos = int(
            ''.join(re.findall(r'\d+', soup_element.select('.ui-pdp-subtitle')[0].text)))

    except:
        vendidos = 0

    return [vendedor, vendidos]


def get_basic_features(soup_element):
    """
    Soup element is the element with the complete page transformed with the instruction
    soup_element = BeautifulSoup(r.content,'lxml')
    Where r.content is requests.get(article_url)
    """
    basic_features_elements = soup_element.select(
        ".ui-vpp-highlighted-specs__key-value")
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
        try:
            feature_name = element.select("thead")[0].text
            feature_row = {}
            for row in element.select("tbody tr"):
                feature_row[row.select("th")[0].text] = row.select("td")[0].text
        except:
            continue

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
    result["seller_and_amount_solded"] = get_seller_and_amount_solded(
        soup_element)
    result["basic_features"] = get_basic_features(soup_element)
    result["detailed_features"] = get_detailed_features(soup_element)

    return result
