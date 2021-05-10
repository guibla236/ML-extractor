from flask import Flask, render_template, jsonify, request
from .utils.app import get_options_and_applied_filters, get_search_link
from .utils.DataCollectorThread import DataCollector

app = Flask(__name__)

search_link = None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
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

@app.route('/collect-data', methods=["POST"])
def collect_data():
    global thread_data
    
    link = request.json.get("link")
    
    #print("link pedido = "+link)

    total_data = request.json.get("total_data")
    
    #print("total_data = "+total_data)

    thread_data = DataCollector(link, total_data)
    thread_data.start()
    return jsonify({"total_data": thread_data.total_data})
    

@app.route('/ask-progress', methods=["POST"])
def ask_progress():
    global thread_data
    return jsonify({"elapsed": thread_data.processed_data,
                    "total": thread_data.total_data,
                    "finished": thread_data.finished })

@app.route('/get-data', methods=["POST"])
def get_data():
    global thread_data
    return jsonify(thread_data.collected_data)

@app.route('/apply-filter',methods=['POST'])
def apply_filter():    
    if request.method == "POST":
        link = request.json.get("link")
        print("link="+link)
        options = get_options(link)
        return render_template('seleccion-de-filtros.html', options=options)
