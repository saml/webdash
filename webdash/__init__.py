import time
import datetime
import multiprocessing
import logging
import logging.handlers
import os
import json

import pymongo
import requests
from bson.objectid import ObjectId
from bson import json_util

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

def configure_logging(logger):
    log_level = getattr(logging, config.log_level.upper())
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s (%(pathname)s:%(lineno)d)')

    log_path = config.log_path
    log_dir = os.path.dirname(log_path)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    handler = logging.handlers.TimedRotatingFileHandler(log_path, when='midnight', interval=1, backupCount=365)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(stream_handler)

def to_jsonable(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, ObjectId):
        return json_util.default(obj)
    props = dir(obj)
    if 'to_dict' in props:
        return obj.as_dict()
    if '__iter__' in props:
        return list(obj)
    raise TypeError('Cannot serialize {} of type {}'.format(obj, type(obj)))

def jsondumps(obj):
    return json.dumps(obj, default=to_jsonable, indent=2)

def jsonloads(s):
    return json.loads(s)
