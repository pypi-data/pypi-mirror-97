# -*- coding: utf-8 -*-
"""
This package contains a series of python specific modes (calltips,
autoindent, code linting,...).

"""
from .autocomplete import PyAutoCompleteMode
from .autoindent import PyAutoIndentMode
from .calltips import CalltipsMode
# Has been moved to pyqode.core
from pyqode.core.modes.comments import CommentsMode
from .frosted_checker import PyFlakesChecker
# for backward compatibility, will be removed in a future release
from .frosted_checker import PyFlakesChecker as FrostedCheckerMode
from .goto_assignements import Assignment
from .goto_assignements import GoToAssignmentsMode
from .sh import PythonSH
from .pep8_checker import PEP8CheckerMode
from .auto_pep8 import AutoPEP8
from pyqode.core.modes import IndenterMode as PyIndenterMode  # deprecated


try:
    # load pyqode.python resources (code completion icons)
    from pyqode.python._forms import pyqode_python_icons_rc  # DO NOT REMOVE!!!
except ImportError:
    # PyQt/PySide might not be available for the interpreter that run the
    # backend
    pass


__all__ = [
    'Assignment',
    'CalltipsMode',
    'CommentsMode',
    'PyFlakesChecker',
    'FrostedCheckerMode',
    'GoToAssignmentsMode',
    'PEP8CheckerMode',
    'PyAutoCompleteMode',
    'PyAutoIndentMode',
    'PyIndenterMode',
    'PythonSH',
    'AutoPEP8'
]
