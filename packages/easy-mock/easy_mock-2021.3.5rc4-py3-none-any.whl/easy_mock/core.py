# -*- coding: utf-8 -*-
# Created by mcwT <machongwei_vendor@sensetime.com> on 2021/02/24.
import os

from flask import Flask, request, make_response
from werkzeug.routing import BaseConverter

from easy_mock.common import check_schema
from easy_mock.loader import locate_processor_py, load_processor_func, get_api_yaml, get_request_body
from easy_mock.process import resolve_all_refs

SUPPORT_METHOD_LIST = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]


class WildcardConverter(BaseConverter):
    regex = r'.*?'
    weight = 200


def mock_server(path):
    conf = get_api_yaml(path, request.method)
    if not conf:
        return make_response({"error": "This easy_mock interface is not defined."}, 405)

    req = get_request_body(request)

    setup, teardown = conf.get("setup"), conf.get("teardown")

    # setup processor
    req = load_processor_func().get(setup)(req) if setup and locate_processor_py(os.getcwd()) else req

    # match easy_mock data
    for md in conf.get("defined_data_list"):
        if req == md.get("body"):
            resp = md.get("response")
            break
    else:
        # random data for schema TODO 通过response schema 生成随机数据
        response_schema = conf.get("response_schema")

        if not response_schema:
            return make_response({"error": "Must define response_schema or have matching defined_data_list"}, 404)

        resp = resolve_all_refs(response_schema)

    # teardown processor
    resp = load_processor_func().get(teardown)(req, resp) if teardown and locate_processor_py(os.getcwd()) else resp

    if conf.get("request_schema", None):
        check_schema(conf.get("request_schema"), req)

    return resp


def main(port):
    app = Flask(__name__)

    app.url_map.converters['wildcard'] = WildcardConverter

    app.add_url_rule(rule='/<wildcard:path>', view_func=mock_server, methods=SUPPORT_METHOD_LIST)

    app.run(host='0.0.0.0', port=port)
