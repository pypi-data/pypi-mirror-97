#!/usr/bin/env python3

import base64
import json
import logging
import os
import pathlib
import pickle

import dcyd
from . import constants

def get_project_id() -> str:
    '''Returns project_id from either env var or config file'''

    project_id = get_project_credentials()['project_id']

    if not project_id:
        report_client_error("Please set either DCYD_PROJECT_ID or DCYD_CONFIG_FILE env var")
        return ''

    return project_id

CONFIG_FROM_FILE = {}
if os.getenv('DCYD_CONFIG_FILE'):
    CONFIG_FROM_FILE = json.loads(pathlib.Path(os.getenv('DCYD_CONFIG_FILE')).read_text())

def get_project_credentials() -> dict:
    '''
    Returns project_access_token from either env var or config file

    >>> 'project_id' in get_project_credentials()
    True
    >>> 'project_access_token' in get_project_credentials()
    True
    '''

    project_id = os.getenv('DCYD_PROJECT_ID') or CONFIG_FROM_FILE.get('project_id')
    project_access_token = os.getenv('DCYD_PROJECT_ACCESS_TOKEN') or CONFIG_FROM_FILE.get('project_access_token')

    return {
        'project_id': project_id,
        'project_access_token': project_access_token,
    }

CLIENT_ERROR_MODE = os.getenv('DCYD_CLIENT_ERROR_MODE', 'log')

def report_client_error(message: str):
    if CLIENT_ERROR_MODE == 'raise_error':
        raise RuntimeError(message)
    elif CLIENT_ERROR_MODE == 'silent':
        return
    else:
        logging.error(message)

def serialize_objects(obj_dict: dict):
    errors = []
    serialized_data = {}
    for k,v in obj_dict.items():
        serialized_data[k], success = make_json_serializable(v)
        if not success:
            errors.append(k)
    return serialized_data, errors

def make_json_serializable(obj):
    '''To ensure obj is JSON-serializable, pickle and base64-encode it.

    arg obj: object to be tested for JSON-serializability
    type obj: any Python object

    returns: a transformation of obj that is JSON-serializable.
    '''
    try:
        encoded_obj = base64.b64encode( # encode byte string into bytes
                        pickle.dumps(obj) # convert object into a byte string
                      ).decode('ascii')
        success = True
    except Exception as e:
        encoded_obj = base64.b64encode(
                        pickle.dumps(e)
                      ).decode('ascii')
        success = False
    return encoded_obj, success

def api_url(path='') -> str:
    return os.getenv('DCYD_API_BASE', 'https://api.dcyd.io') + '/' + path
