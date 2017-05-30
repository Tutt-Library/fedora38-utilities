"""
 mod:`urls` Fedora Batch App URL rourting
"""
__author__ = "Jeremy Nelson"

import json
import time
import threading

from concurrent.futures import ThreadPoolExecutor
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, redirect, Response
from flask import jsonify, flash, url_for, abort
from flask_socketio import SocketIO, emit
from .forms import AddFedoraObjectFromTemplate, IndexRepositoryForm
from .forms import MODSReplacementForm, MODSSearchForm
from .forms import EditFedoraObjectFromTemplate, LoadMODSForm 
from .helpers import create_mods, generate_stubs, load_edit_form, build_mods
from .helpers import save_mods_xml
from .indexer import Indexer
from .repairer import update_multiple, update_mods

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
socketio = SocketIO(app)

executor = ThreadPoolExecutor(2)

ACTIVE_MSGS = []
BACKEND_THREAD = None
MODS_NS = {'mods': 'http://www.loc.gov/mods/v3'}

class IndexerThread(threading.Thread):

    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.indexer = Indexer(app=app, 
            elasticsearch=kwargs.get('elasticsearch'))
        self.job = kwargs.get("job")
        self.pid = kwargs.get("pid")
        
    def run(self):
        if self.job.lower().startswith("full"):
            self.indexer.reset()
            self.indexer.index_collection(self.pid)
        return 

class RepairerThread(threading.Thread):

    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.pid_listing = kwargs.get('pid_listing')
        self.xpath = kwargs.get('xpath')
        self.old_value = kwargs.get('old_value')
        self.new_value = kwargs.get('new_value')
        
    def run(self):
        update_multiple(pid_list=self.pid_listing, 
            xpath=self.xpath,
            old_value=self.old_value,
            new_value=self.new_value)
        return

@app.route("/")
def default():
    return render_template('fedora_utilities/app.html')

@app.route("/about")
def about():
    return render_template("fedora_utilities/about.html")

@app.route("/add_stub", methods=["GET", "POST"])
def add_stub():
    ingest_form = AddFedoraObjectFromTemplate(csrf_enabled=False)
    if ingest_form.validate_on_submit():
        mods_xml = create_mods(request.form)
        return jsonify(generate_stubs(
            config=app.config,
            mods_xml=mods_xml,
            title=request.form.get('title'),
            parent_pid=request.form.get('collection_pid'),
            num_objects=request.form.get('number_objects'),
            content_model=request.form.get('content_models')))
    return render_template('fedora_utilities/batch-ingest.html',
        ingest_form=ingest_form)

@app.route("/edit/", methods=["GET", "POST"])
@app.route("/edit/<path:pid>", methods=["GET", "POST"])
def edit_mods(pid=None):
    load_form, mods_xml = None, None
    if pid is None:
        load_form = LoadMODSForm()
        if load_form.validate_on_submit():
            return redirect(url_for("edit_mods", pid=load_form.pid.data))
    else:
        mods_xml = load_edit_form(app.config, pid)
        if mods_xml is None:
            return abort(404)
        if request.method.startswith("POST"):
            mods_xml = build_mods(edit_form)
            return mods_xml
    return render_template('fedora_utilities/mods-edit.html',
        load_form=load_form,
        pid=pid,
        mods_xml=mods_xml)

@app.route("/edit/<pid>/save", methods=["POST"])
def save_mods(pid):
    mods_xml = request.form.get("xml")
    mods_xml = mods_xml.replace('xml:space="preserve"', "")
    save_mods_xml(app.config, pid, mods_xml)
    return jsonify({"message": "MODS XML saved",
                    "pid": pid})

@app.route("/index/status")
def indexing_status():
    if BACKEND_THREAD is None:
        # Check in 15 seconds
        time.sleep(15)
        if BACKEND_THREAD is None:
            msg = "Finished, Indexer no longer active"
    elif len(BACKEND_THREAD.indexer.messages) > 0:
        msg = BACKEND_THREAD.indexer.messages.pop(0)
    else:
        msg = "Finished"
    return jsonify({"message": msg})
    #socketio.emit('status event', {"message": msg})

@socketio.on('index status')
def handle_index_status(data):
    print(data)
    emit('indexer status', 1)

def __index_pid__(search_idx, pid):
    indexer = Indexer(app=app, 
        elasticsearch=search_index)
    ancestors = indexer.__get_ancestry__(pid)
    ancestors.reverse()
    indexer.index_pid(pid, ancestors[-1], ancestors)


@app.route("/index/pid", methods=["POST"])
def index_pid():
    pid = request.form.get("pid")
    search_index = request.form.get("indices")
    __index_pid__(search_index, pid)
    flash("Indexed PID {} in index {}".format(pid, search_index))
    return redirect(url_for('index_repository'))

@app.route("/index", methods=["POST", "GET"])
def index_repository():
    global BACKEND_THREAD
    index_form = IndexRepositoryForm(csrf_enabled=False)
    if index_form.validate_on_submit():
        if index_form.index_choice.data.startswith("0"):
            return jsonify({"message": "Started Incremental Indexing"})
        elif index_form.index_choice.data.startswith("1"):
            elastic_host = index_form.indices.data
            BACKEND_THREAD = IndexerThread(
                elasticsearch=elastic_host,
                job="full", 
                pid="coccc:root")
            BACKEND_THREAD.start()
            return jsonify({"message": "Started Full Indexing"})
        else:
            return jsonify({"message": "Unknown Indexing option"})
 
    return render_template('fedora_utilities/index-repository.html',
        index_form=index_form)


@app.route("/mods-replacement", methods=["POST", "GET"])
def mods_replacement():
    replace_form = MODSReplacementForm(csrf_enabled=False)
    search_form = MODSSearchForm(csrf_enabled=False)
    if replace_form.validate_on_submit():
        collection_pid = replace_form.collection_pid.data
        pid_listing = replace_form.pid_listing.data.split(",")
        xpath = replace_form.select_xpath.data
        old_value = replace_form.old_value.data
        new_value = replace_form.new_value.data
        if collection_pid is not None and len(collection_pid) > 0:
            pid_listing = get_collection_pids(app.config, collection_pid)
        for pid in pid_listing:
            future = executor.submit(update_mods,
                app=app,
                pid=pid,
                xpath=xpath,
                old=old_value,
                new=new_value)
            flash("Replaces {} old {} with {} for pid {}".format(
                xpath,
                old_value,
                new_value,
                pid))
            
        #return jsonify({"total": len(pid_listing)})
        return redirect(url_for('mods_replacement'))
    return render_template('fedora_utilities/mods-replacement.html',
        replace_form=replace_form,
        search_form=search_form)

@app.route("/search", methods=["POST", "GET"])
def search_pids():
    search_form = MODSSearchForm(csrf_enabled=False)
    if search_form.validate_on_submit():
        es_host = search_form.indices.data
        es = Elasticsearch(hosts=[es_host])
        found_pids = []
        query = search_form.query.data
        facet = search_form.facet.data
        dsl = {"_source": ["pid"]}
        if facet.startswith("none"):
            dsl["query"] = {
                "match": {
                    "_all": query
                }    
            }
        else:
            dsl = {
                "query": {
                    "term": { facet: query }
                }
            }
        search_results = es.search(body=dsl, 
                index='repository',
                size=50)
        for hit in search_results.get('hits', {})\
            .get('hits', []):
            pid = hit.get('_source', {}).get('pid')
            found_pids.append(pid)
        return jsonify({
            "pids": found_pids, 
            "total": search_results.get('hits', {}).get('total', 0)})
    return jsonify({"pids": []})
    

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=9455)
    #app.run(host='0.0.0.0', debug=True, port=9455)
