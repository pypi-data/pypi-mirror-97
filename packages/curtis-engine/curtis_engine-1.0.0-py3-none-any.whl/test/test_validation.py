from curtis.utils.validation import validation_bounds


def test_validation_rules_are_defined():
    """ Should ensure that every validation rule is defined. """
    for parameter in validation_bounds:
        assert validation_bounds[parameter] is not None
        assert validation_bounds[parameter]['min'] is not None
        assert validation_bounds[parameter]['max'] is not None
        assert validation_bounds[parameter]['reason'] is not None
