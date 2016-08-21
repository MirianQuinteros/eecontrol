#!/usr/bin/python

import sys
import json
from model import Experience

class ExpEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Experience):
            return super(ExpEncoder, self).default(obj)
        return obj.__dict__