# *-* encoding:utf-8 *-*

import os
import imp 
import re

from django.conf import settings

"""Levanta todos los Forms (source: http://wiki.python.org/moin/ModulesAsPlugins)"""

_rForm = re.compile(r'^[\S]+Form$')

path = getattr(settings, 'DYNAFORM_FORMS_PATH', False)
if not path:
    path = os.path.dirname(__file__)

def _find_modules(path=path):
    """Return names of modules in a directory.
    Returns module names in a list. Filenames that end in ".py" or
    ".pyc" are considered to be modules. The extension is not included
    in the returned list.
    """
    modules = set()
    for filename in os.listdir(path):
        module = None
        if filename.endswith(".py"):
            module = filename[:-3]
        #elif filename.endswith(".pyc"):
        #    module = filename[:-4]
        if module is not None and module not in ['__init__', 'base']:
            modules.add(module)
    return list(modules)

def _load_module(name, path=[path]):
    """Return a named module found in a given path."""
    (file, pathname, description) = imp.find_module(name, path)
    return imp.load_module(name, file, pathname, description)

def _load_forms(module):
    forms = []
    for obj in module.__dict__.values():
        try:
            if _rForm.match(obj.__name__):
                forms.append(obj)
        except:
            pass
    return forms

all_forms = {}

for module in [_load_module(name) for name in _find_modules()]:
    for inst in _load_forms(module):
        all_forms[inst.__name__] = inst

del re, os, imp
del inst, module, name
del _find_modules, _rForm, _load_forms, _load_module
