# Import all functions from each module
from .clean_images import *
from .clean_tables import *
from .convert_encoding import *
from .run_pandoc import *
from .table_styler import *

# Explicitly list all functions for top-level import
__all__ = []

# Helper to automatically add all functions from each module to __all__
import sys
import types

for module_name in ['clean_images', 'clean_tables', 'convert_encoding', 'run_pandoc', 'table_styler']:
    module = sys.modules[__name__].__dict__.get(module_name)
    if module is None:
        # import module
        module = __import__(f".{module_name}", globals(), locals(), level=1)
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, types.FunctionType):
            setattr(sys.modules[__name__], attr_name, attr)
            __all__.append(attr_name)
