import os

import openapi3
import requests
import yaml
from dict_tools.data import NamespaceDict


def new(hub, name: str, **kwargs):
    spec = hub.pop_create.exec.openapi3.init.read(path=hub.OPT.pop_create.openapi_spec)
    spec.openapi = spec.get("openapi", "3")
    api = openapi3.OpenAPI(spec, use_session=True)
    from pprint import pprint

    pprint(spec.keys())
    pprint(api.paths)
    return
    print(api.components)
    print(api.info)
    for p in api.paths.values():
        openapi3.paths.Path
        print(p.__class__)


def read(hub, path: str):
    """
    If the path is a file, then parse the json contents of the file,
    If the path is a url, then return a json response from the url.
    """
    if os.path.exists(path):
        with open(path, "w") as fh_:
            ret = yaml.safe_load(fh_)
    else:
        request = requests.get(path)
        ret = request.json()
    return NamespaceDict(ret)
