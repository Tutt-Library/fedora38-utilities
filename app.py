"""
 mod:`urls` Fedora Batch App URL rourting
"""
__author__ = "Jeremy Nelson"

from flask import Flask, render_template, request, redirect, Response
from flask import jsonify
from forms import AddFedoraObjectFromTemplate, IndexRepositoryForm
from forms import MODSReplacementForm
from helpers import create_mods, generate_stubs
from indexer import Indexer

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

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
        return jsonify(generate_stubs(mods_xml=mods_xml,
            title=request.form.get('title'),
            parent_pid=request.form.get('collection_pid'),
            num_objects=request.form.get('number_objects'),
            content_model=request.form.get('content_models')))
    return render_template('fedora_utilities/batch-ingest.html',
        ingest_form=ingest_form)


@app.route("/index", methods=["POST", "GET"])
def index_repository():
    index_form = IndexRepositoryForm(csrf_enabled=False)
    if index_form.validate_on_submit():
        indexer = Indexer(app=app)
        if index_form.index_choice.data.startswith("0"):
            return "In Incremental Index"
        elif index_form.index_choice.data.startswith("1"):
            indexer.index_collection("coccc:root")
            return "Should now run full index"
        else:
            return "Unknown Indexing option"
 
    return render_template('fedora_utilities/index-repository.html',
        index_form=index_form)


@app.route("/mods-replacement")
def mods_replacement():
    replace_form = MODSReplacementForm(csrf_enabled=False)
    if replace_form.validate_on_submit():
        return "Submitted {}".format(replace_form.select_xpath.value)
    return render_template('fedora_utilities/mods-replacement.html',
        replace_form=replace_form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=9455)
