from flask import Flask, redirect, render_template, request, url_for
import sys
sys.path.insert(1, 'models')
from query_graph import graph_query
from unittest import result
from rdflib import *
from rdflib import Namespace
from rdflib.term import URIRef
from rdflib.plugins import sparql
from rdflib.namespace import RDF, RDFS, OWL

g = Graph().parse('models/plan-ontology-rdf-instances-planner-info.owl')

app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def mainPage():
    if request.method == "POST":
        sql_query = request.form["sql_editor"]
        namespace = request.form.get("namespace")
        headers, rows = graph_query(sql_query,g,namespace)
        return render_template('index.html', sql_input=sql_query, headers=headers, rows=list(rows), namespace=namespace)
    else:
        namespace = request.form.get("namespace")
        return render_template('index.html', sql_input=None, headers=None, rows=None, namespace=namespace)

if __name__ == '__main__':
    app.run(debug=True)