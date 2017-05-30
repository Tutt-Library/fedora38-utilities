__author__ = "Jeremy Nelson"
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from legacy_fedora.app import app

app.config['DEBUG'] = True

application = DispatcherMiddleware(
    app,
    {"/fedora_utilities": app}
)


if __name__ == '__main__':
    run_simple('0.0.0.0', 9455, application, use_reloader=True, use_debugger=True)
