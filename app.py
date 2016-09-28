"""
 mod:`urls` Fedora Batch App URL rourting
"""
__author__ = "Jeremy Nelson"

from flask import Flask, render_template, request
from forms import AddFedoraObjectFromTemplate
from helpers import create_mods, create_stubs

app = Flask(__name__, instance_relative_config=True)

@app.route("/")
def default():
    return render_template('fedora_utilities/app.html')

@app.route("/add_stub", methods=["GET", "POST"])
def add_stub():
    ingest_form = AddFedoraObjectFromTemplate(csrf_enabled=False)
    if ingest_form.validate_on_submit():
        mods_xml = create_mods(request.form)
        pids = create_stubs(mods_xml,
            request.form.get('title'),
            request.form.get('parent_collection'),
            request.form.get('number_objects'),
            request.form.get('content_models'))
        return "Ingest form {}".format(mods_xml)
    return render_template('fedora_utilities/batch-ingest.html',
        ingest_form=ingest_form)


@app.route("/index")
def index_repository():
    return render_template('fedora_utilities/index-repository.html')

#@app.route("/ingest$")
#return views.batch_ingest()

if __name__ == '__main__':
    app.run(debug=True)
