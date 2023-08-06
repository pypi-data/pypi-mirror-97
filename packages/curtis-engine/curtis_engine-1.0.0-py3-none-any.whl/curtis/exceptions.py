class CurtisIntegrityError(Exception):
    """
    Integrity error exception

    Gets raised when the Curtis' model file (`model/curtis.sav`) is either
    inaccessible or corrupted, prevents anything else from running and the 
    engine halts.
    """
    pass


class CurtisParameterError(ValueError):
    """
    Parameter error exception

    Gets raised when an invalid value gets passed to a `CurtisFact`, creating
    data impurity and leading the system to an incorrect decision/diagnosis.
    """
    pass
