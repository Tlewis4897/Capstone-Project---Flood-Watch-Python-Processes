import requests
import os
import json
import urllib
import pyodbc
import sys
import arcpy

from utils import read_json, sql_connection, createSdeFile
from update_status import update_gauge_status
from upsert_fc import create_temp_fc


def get_gauge_status(config):
    gauges = tuple(config['gauges'])
    params = urllib.parse.urlencode({'where': f'gaugelid in {gauges}', 
                                     'outFields': '*','client': 'requestip', 'f': 'json'})
    results = requests.get(config['noaa_url'],params).json()
    cursor = sql_connection(config).cursor()
    for data in results['features']:
        for k in config['key_val_gauge']:
            if k == data['attributes']['gaugelid']:
                update_gauge_status(config['key_val_gauge'][k],
                                    data['attributes']['status'],cursor)


def main():
    try:
        #Define paths
        config_vals = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                    'config'))
        sde_location = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                 'config'))
        CURRENT_DIR = os.path.realpath(os.path.dirname(__file__))
        #Read config file
        config = read_json(os.path.join(config_vals, 'config.json'))
        # #Create SDE connection file
        createSdeFile(sde_location, config)
        # Create connection for sde path
        sde_path = os.path.join(sde_location, config['sde']['sde_name'])
        get_gauge_status(config)
        create_temp_fc(config)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main() 