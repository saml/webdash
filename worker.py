#!/usr/bin/env python

import datetime
import argparse
import logging

from webdash import get_db, config, exec_parallel, Worker, configure_logging
def main(args):
    logger = logging.getLogger(__name__)
    configure_logging(logger)
    mongo = get_db()
    worker_fn = Worker(mongo.webdash)
    t = datetime.datetime.now()
    exec_parallel(worker_fn, config.urls, args.concurrent)
    logger.info('Fetched {} urls. Took: {}'.format(len(config.urls), datetime.datetime.now() - t))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--concurrent', type=int, default=4)
    args = parser.parse_args()
    main(args)

