import pandas as pd

from curtis.facts import CurtisFacts
from curtis.engine import CurtisEngine
from curtis.utils.encoding import diagnosis_indexes


def test_creates_engine_instance():
    """ Should correctly create a `CurtisEngine` instance. """
    curtis = CurtisEngine()

    assert isinstance(curtis, CurtisEngine)


def test_declares_facts():
    """ Should correctly declare a fact. """
    curtis = CurtisEngine()
    test_facts = CurtisFacts(
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

    curtis.declare_facts(test_facts)

    assert curtis.facts == test_facts


def test_predicts_correctly():
    """ Should correctly predict a given diagnosis based on validation data. """
    curtis = CurtisEngine()

    test_df = pd.read_csv('curtis/data/validation_sample.csv')
    test_df = test_df.drop(['diagnosis'], axis='columns')

    for patient in test_df.iloc:
        test_facts = CurtisFacts(
            sex=patient['sex'],
            age=patient['age'],
            height=patient['height'],
            weight=patient['weight'],
            HR=patient['HR'],
            Pd=patient['Pd'],
            PQ=patient['PQ'],
            QRS=patient['QRS'],
            QT=patient['QT'],
            QTcFra=patient['QTcFra']
        )

        curtis.declare_facts(test_facts)

        diagnosis_predicted = curtis.diagnose()
        diagnosis_expected = patient['diagnosis_index']

        assert diagnosis_predicted == diagnosis_expected
        assert diagnosis_indexes[diagnosis_predicted] is not None
