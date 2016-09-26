"""
 mod:`urls` Fedora Batch App URL rourting
"""
__author__ = "Jeremy Nelson"

from flask import Flask, render_template, request

from forms import AddFedoraObjectFromTemplate

app = Flask(__name__, instance_relative_config=True)

@app.route("/")
def default():
    return render_template('fedora_utilities/app.html')

@app.route("/add_stub", methods=["GET", "POST"])
def add_stub():
    ingest_form = AddFedoraObjectFromTemplate(csrf_enabled=False)
    if request.method.startswith("POST"):
        if ingest_form.validate_on_submit():
            return "Ingest form {}".format(ingest_form.validate())
    return render_template('fedora_utilities/batch-ingest.html',
        ingest_form=ingest_form)


@app.route("/index")
def index_repository():
    return render_template('fedora_utilities/index-repository.html')

#@app.route("/ingest$")
#return views.batch_ingest()

if __name__ == '__main__':
    app.run(debug=True)
