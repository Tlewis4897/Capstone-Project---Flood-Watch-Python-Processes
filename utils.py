import json
import os
import arcpy
from pathlib import Path
import glob
import zipfile
import pyodbc


def read_json(json_data):
    """reads a json file and returns the text as a dictionary"""
    try:
        with open(json_data, 'r') as json_file:
            get_json = json.load(json_file)
        return get_json
    except Exception as err:
        return err


def sql_connection(config):
    cnxn = pyodbc.connect(
			driver='{}'.format('SQL Server'),
			server=config["sql"]["server"],
			database=config["sql"]["database"],
			UID=config["sql"]["user"],
			PWD=config["sql"]["password"],autocommit=True)
    return cnxn


def zip_hosted_layer(path: str, name: str) -> str:
    zipobj = zipfile.ZipFile(name, "w")
    for infile in glob.glob(path + "/*"):
        zipobj.write(infile, os.path.basename(path) +
                     "/" + os.path.basename(infile), zipfile.ZIP_DEFLATED)
    zipobj.close()
    return name


def createSdeFile(sde_path, config):
    # Check if sde connection exists for ArcPy creation of tables
    if os.path.exists(os.path.join(sde_path, config['sde']['sde_name'] + '.sde')):
        print('sde exists')
    else:
    # if connection does not exist, create connection and store to config file
        arcpy.CreateDatabaseConnection_management(sde_path,
                                                config['sde']['sde_name'],
                                                "SQL_SERVER",
                                                config["sql"]["server"],
                                                "DATABASE_AUTH",
                                                config["sql"]["user"],
                                                config["sql"]["password"],
                                                "SAVE_USERNAME",
                                                config["sql"]["database"])