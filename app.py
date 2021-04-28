from flask import Flask, render_template, jsonify, request
from .utils.app import get_options_and_applied_filters, get_search_link
from .utils.DataCollectorThread import DataCollector
app = Flask(__name__)

search_link = None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buscar')
def primer_busqueda():
    if request.args.get("query"):
        query = request.args.get("query")
        search_link = get_search_link(query)

    elif request.args.get("link"):
        search_link = request.args.get("link")

    parameters = get_options_and_applied_filters(search_link)
    
    options = parameters.get("search_options")
    applied_filters = parameters.get("applied_filters")
    total_data = parameters.get("total_data")
    
    return render_template('seleccion-de-filtros.html', 
                            options = options,
                            applied_filters = applied_filters,
                            total_data = total_data,
                            actual_link = search_link)

thread_data = None

@app.route('/recolectar-datos', methods=["POST"])
def recoleccion_de_datos():
    global thread_data
    # Declaración e inicio.
    link = request.json.get("link")
    print("link pedido = "+link)
    total_data = request.json.get("total_data")
    print("total_data = "+total_data)
    thread_data = DataCollector(link, total_data)
    thread_data.start()
    return jsonify({"total_data": thread_data.total_data})
    # Lógica normal

@app.route('/preguntar-progreso', methods=["POST"])
def preguntar_progreso():
    global thread_data
    return jsonify({"elapsed": thread_data.processed_data,
                    "total": thread_data.total_data,
                    "finished": thread_data.finished })

@app.route('/pedir-datos', methods=["POST"])
def pedir_datos():
    global thread_data
    return jsonify(thread_data.collected_data)

@app.route('/aplicar-filtro',methods=['POST'])
def aplicar_filtro():    
    if request.method == "POST":
        link = request.json.get("link")
        print("link="+link)
        options = get_options(link)
        return render_template('seleccion-de-filtros.html', options=options)
