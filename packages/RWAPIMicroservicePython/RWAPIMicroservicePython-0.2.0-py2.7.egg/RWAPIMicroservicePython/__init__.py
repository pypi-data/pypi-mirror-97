import json
import os
import threading

import requests
from flask import jsonify, request, Response
from requests import post, Session, Request
from werkzeug.datastructures import ImmutableMultiDict

from RWAPIMicroservicePython.errors import NotFound

AUTOREGISTER_MODE = 'AUTOREGISTER_MODE'
NORMAL_MODE = 'NORMAL_MODE'

CT_URL = None
CT_TOKEN = None
API_VERSION = None


def __ct_register(name, ct_url, url):
    """Autoregister method"""
    payload = {'name': name, 'url': url, 'active': True}

    try:
        r = post(ct_url + '/api/v1/microservice', json=payload, timeout=10)
    except Exception as error:
        os._exit(1)

    if r.status_code >= 400:
        os._exit(1)


def register(app, name, info, swagger, mode, ct_url, url, token, api_version, delay=5.0):
    """Register method"""
    if mode == AUTOREGISTER_MODE:
        if delay is not None:
            t = threading.Timer(delay, __ct_register, [name, ct_url, url])
            t.start()
        else:
            __ct_register(name, ct_url, url)

    global CT_TOKEN, CT_URL, API_VERSION
    CT_TOKEN = token
    CT_URL = ct_url
    API_VERSION = api_version

    @app.before_request
    def get_logger_user():
        authorization_token_header = request.headers.get('authorization')
        if authorization_token_header is None:
            return

        logged_user_response = requests.get(
            CT_URL + '/auth/user/me',
            headers={
                'content-type': 'application/json',
                'Authorization': authorization_token_header
            }
        )

        if logged_user_response.status_code >= 400:
            return Response(logged_user_response.text, status=logged_user_response.status_code, mimetype='application/json')

        http_args = request.args.to_dict()
        http_args['loggedUser'] = logged_user_response.text
        request.args = ImmutableMultiDict(http_args)

    @app.after_request
    def add_cache_headers(response):
        response.headers.set('cache-control', 'private')
        return response

    @app.route('/info')
    def get_info():
        info['swagger'] = swagger
        return jsonify(info)

    @app.route('/ping')
    def get_ping():
        return 'pong'


def request_to_microservice(config):
    """Request to microservice method"""
    try:
        session = Session()
        request_config = Request(
            method=config.get('method'),
            url=CT_URL + config.get('uri') if config.get(
                'ignore_version') or not API_VERSION else CT_URL + '/' + API_VERSION + config.get('uri'),
            headers={
                'content-type': 'application/json',
                'Authorization': 'Bearer ' + CT_TOKEN,
                'APP_KEY': config.get('application', 'rw')
            },
            data=json.dumps(config.get('body'))
        )
        prepped = session.prepare_request(request_config)

        response = session.send(prepped)
    except Exception as error:
        raise error

    try:
        return response.json()
    except Exception:
        raise NotFound(response.text)
