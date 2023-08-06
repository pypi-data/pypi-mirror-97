from curtis.utils.encoding import diagnosis_indexes


def test_correctly_decodes_diagnosis_indexes():
    """ Test for the diagnosis indexes dictionary's length. """
    assert len(diagnosis_indexes) == 61
