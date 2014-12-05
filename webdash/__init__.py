import time
import datetime
import multiprocessing

import pymongo
import requests

from . import config

class Worker(object):
    def __init__(self, db):
        self.db = db

    def __call__(self, url):
        data = download(url)
        self.db.data.insert(data.to_dict())
        return data

def exec_procs(procs):
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()

def exec_parallel(fn, things, concurrent):
    procs = []
    for i,thing in enumerate(things, 1):
        procs.append(multiprocessing.Process(target=fn, args=(thing,)))
        if i % concurrent == 0:
            exec_procs(procs)
            procs = []
    if procs:
        exec_procs(procs)



class Data(object):
    def __init__(self, url, secs, size, fetch_date):
        self.url = url
        self.secs = secs
        self.msecs = secs*1000
        self.size = size
        self.rate = size/self.msecs
        self.fetch_date = fetch_date

    def to_dict(self):
        return {'url': self.url, 
                'secs': self.secs,
                'bytes': self.size,
                'fetch_date': self.fetch_date}

    @classmethod
    def from_dict(cls, doc):
        return cls(doc['url'], doc['secs'], doc['bytes'], doc['fetch_date'])

def download(url):
    fetch_date = datetime.datetime.utcnow()
    t = time.time()
    resp = requests.get(url)
    delta = time.time() - t
    size = len(resp.content)
    return Data(url,delta,size, fetch_date)


def get_db(mongouri=config.mongouri):
    return pymongo.MongoClient(mongouri)

