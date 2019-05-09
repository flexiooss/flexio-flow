import json
from json import JSONEncoder

from PoomCiDependency.FullRepository import FullRepository
from PoomCiDependency.Module import Module


class PoomCiDependencyJSONEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, FullRepository) or isinstance(object, Module):

            return object.__dict__

        else:

            return json.JSONEncoder.default(self, object)
