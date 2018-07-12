#!/home/libraryadmin/py3-env/bin/python
"""Command-line tool for indexing Fedora 3.8 repository into Elasticsearch"""
__author__ = "Jeremy Nelson"

import datetime
import os
import sys
from instance import config
from legacy_fedora.indexer import Indexer

class StubApp(object):

    def __init__(self, config):
        self.config = dict()
        for var in dir(config):
            self.config[var] = getattr(config, var)


if __name__ == "__main__":
    start = datetime.datetime.utcnow()
    print("Started indexing at {}".format(start,
        start))
    app = StubApp(config)
    indexer = Indexer(app=app)
    indexer.reset()
    indexer.index_collection(
        app.config.get("INITIAL_PID"))
    finished = datetime.datetime.utcnow()
    print("Finished indexing at {}, total time: {:,} minutes".format(
        finished,
        (finished-start).second / 60.0))
    
