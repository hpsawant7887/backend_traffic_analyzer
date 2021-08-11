#!/usr/bin/env python3

import argparse
import threading as th
import json
import logging
import os
import sys

from threading import Lock
from logging import handlers
from src.call_endpoint import get_endpoint_status
from src.aggregator import aggregate_success_rate


BATCH_SIZE = 25
LOG_DIR = '/var/log/backend_traffic_analyzer'

AGGREGATED_SUCCESS_RATE = {}     # This is a shared resource across threads

LOCK = Lock()


def process_endpoint(endpoint):
    """The function queries the endpoint and generates aggeregated success rate
       :endpoint: hostname or fqdn
       :type endpoint: A String
    """
    status_response_json = get_endpoint_status(endpoint, logger)
    
    if not status_response_json:
        return
    
    status_response = json.loads(status_response_json)
        
    LOCK.acquire()
    
    global AGGREGATED_SUCCESS_RATE
    
    AGGREGATED_SUCCESS_RATE = aggregate_success_rate(AGGREGATED_SUCCESS_RATE, status_response, logger)
    
    LOCK.release()
    

def process_batch(batch):
    """The function starts threads for a batch of hosts
       :batch: list of hosts
       :type batch: List
       :return: None
    """
    threads = []
    
    for endpoint in batch:
        thread = th.Thread(target=process_endpoint, args=(endpoint,))
        threads.append(thread)
        thread.start()
    
    # wait for all threads to finish
    for thread in threads:
        thread.join()   

def write_to_log():
    """This method writes to logger
    """
    message = 'Success_rate by App and Version\n'
    
    app_log = '\t'
    for app in AGGREGATED_SUCCESS_RATE:
        app_log += app + '\n'
        for version in AGGREGATED_SUCCESS_RATE[app]:
            line = '\t  version={},success_rate_%={}\n'.format(version, AGGREGATED_SUCCESS_RATE[app][version]['success_rate_%'])
            app_log += line
        message += app_log
        app_log = '\t'

    logger.info(message)
    

def setupLogging():
    """this method sets up logging to log to a file and to stdout
    """
    #check if app log dir exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    current_file = os.path.realpath(__file__)
    base_file = os.path.basename(current_file)
    log_file = os.path.splitext(base_file)[0] + '.' + 'log'
    log_file_path = '{}/{}'.format(LOG_DIR, log_file)
    
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    format_ = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(format_)
    logger.addHandler(ch)
    
    
    fh = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=20000, backupCount=10)
    fh.setFormatter(format_)
    logger.addHandler(fh)
    
    return logger


def main():
    """This is the main entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="File containing list of endpoints (example: servers.txt)", required=True)
    args = parser.parse_args()
    
    global logger
    logger = setupLogging()
    
    with open(args.file) as fd:
        batch = []      # max 10 endpoints per batch
        for line in fd:
            endpoint = line.rstrip()
            batch.append(endpoint)
            if len(batch) >= BATCH_SIZE:
                process_batch(batch)
                batch = []
        if len(batch) > 0:
            process_batch(batch)
    
    write_to_log()
            

if __name__ == '__main__':
    main()


