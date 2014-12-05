#!/usr/bin/env python

import datetime
import argparse

from webdash import get_db, config, exec_parallel, Worker
def main(args):
    mongo = get_db()
    worker_fn = Worker(mongo.webdash)
    t = datetime.datetime.now()
    exec_parallel(worker_fn, config.urls, args.concurrent)
    print('Fetched {} urls. Took: {}'.format(len(config.urls), datetime.datetime.now() - t))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--concurrent', type=int, default=4)
    args = parser.parse_args()
    main(args)





