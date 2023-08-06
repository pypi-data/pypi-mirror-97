from curtis.exceptions import CurtisIntegrityError, CurtisParameterError


def test_raises_integrity_error():
    """ Should correctly raise a `CurtisIntegrityError` exception. """
    test_message = 'Integrity error test'

    try:
        raise CurtisIntegrityError(test_message)
    except CurtisIntegrityError as e:
        assert str(e) == test_message


def test_raises_parameter_error():
    """ Should correctly raise a `CurtisParameterError` exception. """
    test_message = 'Parameter error test'

    try:
        raise CurtisParameterError(test_message)
    except CurtisParameterError as e:
        assert str(e) == test_message
