#!/usr/bin/env python3
import datetime as dt
import functools
import inspect
import json
import logging
import os
import pprint as pp
import sys
import threading
import uuid

import dcyd
from . import gcp
from dcyd.utils.utils import (
    serialize_objects,
    get_project_id,
)

instance_id = str(uuid.uuid4())
project_id = get_project_id()
client_profile = {
    'client_name': 'dcyd',
    'client_version': dcyd.__version__,
    'client_language': 'python'
}

def bind_arguments(signature, func_args, func_kwargs):
    ba = signature.bind(*func_args, **func_kwargs)
    ba.apply_defaults()
    return ba.arguments

def log_entry(payload: dict):
    '''
    Write a dictionary with the underlying logging infrastructure.
    '''
    if type(payload) is not dict:
        logging.getLogger(__name__).error(f"payload should be a dict but is a {type(payload)}; payload={pp.pprint(payload)}")
        return #TODO: find out if there is any other action we can do
    return gcp.log_struct(record=payload)

def attach_runtime_data(*, payload: dict):
    '''
    Adding runtime data to a payload
    '''
    return {
        **payload, #NOTE: This must be at the top so the data inside won't override the below data
        **client_profile,
        'protocol_version': '1.0',
        'project_id': project_id,
        'instance_id' : instance_id,
        'process_id' : os.getpid(),
        'thread_id' : threading.get_ident(),
    }

def attach_function_runtime_data(*, function: callable, payload: dict):
    '''
    Attach function information and runtime data to a payload
    '''
    signature = inspect.signature(function)
    return attach_runtime_data(payload={
        **payload,
        'function' : {
            'function_name': function.__name__,
            'function_qualname': function.__qualname__,
            'function_module': function.__module__,
            'function_sourcefile': inspect.getsourcefile(function),
            'function_parameters': {
                k: str(v.kind) for k, v in signature.parameters.items()
            }
        },
    })

def log_customer_record(record: dict):
    serialized_customer_record, errors = serialize_objects(record)
    serialized_customer_record = serialized_customer_record
    payload = attach_runtime_data(payload={
        'event_type': 'customer_record',
        'record_timestamp' : dt.datetime.utcnow().isoformat()
    })
    payload['customer_data'] = serialized_customer_record
    if errors:
        payload['serialization_errors']={}
        payload['serialization_errors']['customer_data']
    return log_entry(payload=payload)

def construct_request_payload(function: callable, request_id, request_timestamp, args, kwargs, customer_data: dict={}):
    error_dict = {}
    signature = inspect.signature(function)
    bound_args = bind_arguments(signature, args, kwargs)
    serialized_request_data, arg_errors = serialize_objects(bound_args)
    if arg_errors:
        error_dict['request_data'] = arg_errors

    serialized_customer_data, cust_errors = serialize_objects(customer_data)
    if cust_errors:
        error_dict['customer_data'] = cust_errors

    initial_payload = {
            'event_type' : 'request',
            'request' : {
            'request_id' : request_id,
            'request_timestamp': request_timestamp or dt.datetime.utcnow().isoformat(),
            'request_data': serialized_request_data
        },
        'customer_data' : serialized_customer_data
    }
    if error_dict:
        initial_payload['serialization_errors'] = error_dict

    payload = attach_function_runtime_data(function=function, payload=initial_payload)
    return payload

def construct_response_payload(payload, response, response_timestamp):
    response_payload = {}
    for key in payload:
        response_payload[key] = payload[key]
    response_payload['event_type'] = 'response'
    serialized_response, response_errors = serialize_objects({'response_value': response})
    serialized_response = serialized_response['response_value']
    response_payload['response'] = {
        'response_timestamp': response_timestamp or dt.datetime.utcnow().isoformat(),
        'response_data': serialized_response
    }
    if response_errors:
        if not response_payload.get('serialization_errors'):
            response_payload['serialization_errors'] = {}
        response_payload['serialization_errors']['response_data'] = response_errors
    return response_payload

def monitor(function=None, **customer_data):
    """Decorate a client's function."""
    def decorate(function: callable):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            # Log call of client's function
            request_id = str(uuid.uuid4())
            request_timestamp = dt.datetime.utcnow().isoformat()
            request_payload = construct_request_payload(function, request_id, request_timestamp, args, kwargs, customer_data)
            log_entry(request_payload)

            # Call client's function
            response = function(*args, **kwargs)

            # Log response of client's function
            response_timestamp = dt.datetime.utcnow().isoformat()
            response_payload = construct_response_payload(request_payload, response, response_timestamp)
            log_entry(response_payload)

            # Pass along the function clientall response
            return response
        return wrapper
    if function:
        return decorate(function)
    return decorate

