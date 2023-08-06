""" 
The Cardiovascular Unified Real-Time Intelligent System.

Curtis is a system whose purpose is to analyze cardiovascular health 
of a given person, this is done through ECG analysis (an existent ECG
measuring system is needed to obtain the required values).

To accomplish this, Curtis acts as an expert system, a rule-based program
that emulates a real-life expert way of thinking about a certain topic, those
rules were obtained for Curtis using the "decision tree approach", in which
some existent data was given to a decision tree classifier, and it categorized
the data into branches of rules and decisions.
"""
__version__ = '1.0.0'

try:
    from .facts import CurtisFacts
    from .engine import CurtisEngine
    from .exceptions import exceptions
    from .utils import utils
except ImportError:
    pass
