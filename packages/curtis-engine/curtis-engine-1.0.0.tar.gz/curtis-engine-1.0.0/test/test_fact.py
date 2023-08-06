from curtis.facts import CurtisFacts
from curtis.exceptions import CurtisParameterError
from curtis.utils.validation import validation_bounds


def test_creates_facts_instance():
    """ Should correctly create a `CurtisFacts` instance. """
    facts = CurtisFacts(
        sex=1,
        age=89,
        height=140,
        weight=30,
        HR=56,
        Pd=122,
        PQ=164,
        QRS=118,
        QT=460,
        QTcFra=451
    )

    assert isinstance(facts, CurtisFacts)

    assert facts.sex == 1
    assert facts.age == 89
    assert facts.height == 140
    assert facts.weight == 30
    assert facts.HR == 56
    assert facts.Pd == 122
    assert facts.PQ == 164
    assert facts.QRS == 118
    assert facts.QT == 460
    assert facts.QTcFra == 451


def test_excepts_invalid_facts():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts()
    except:
        assert True


def test_excepts_invalid_sex():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts(
            sex=2,  # <- Cause
            age=89,
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['sex']['reason']


def test_excepts_invalid_age():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts(
            sex=1,
            age=0,  # <- Cause
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['age']['reason']


def test_excepts_invalid_height():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts(
            sex=1,
            age=0,
            height=450,  # <- Cause
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['height']['reason']


def test_excepts_invalid_weight():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts(
            sex=1,
            age=0,
            height=140,
            weight=501,  # <- Cause
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['weight']['reason']


def test_excepts_invalid_HR():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=120,  # <- Cause
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['HR']['reason']


def test_excepts_invalid_Pd():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=56,
            Pd=69,  # <- Cause
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['Pd']['reason']


def test_excepts_invalid_PQ():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=220,  # <- Cause
            QRS=118,
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['PQ']['reason']


def test_excepts_invalid_QRS():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=180,  # <- Cause
            QT=460,
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['QRS']['reason']


def test_excepts_invalid_QT():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=320,  # <- Cause
            QTcFra=451
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['QT']['reason']


def test_excepts_invalid_QTcFra():
    """ Should not create a `CurtisFacts` instance and raise an exception. """
    try:
        CurtisFacts(
            sex=1,
            age=0,
            height=140,
            weight=30,
            HR=56,
            Pd=122,
            PQ=164,
            QRS=118,
            QT=460,
            QTcFra=520  # <- Cause
        )
    except CurtisParameterError as e:
        assert str(e) == validation_bounds['QTcFra']['reason']
