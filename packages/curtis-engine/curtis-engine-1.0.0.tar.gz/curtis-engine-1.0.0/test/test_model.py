import os
import pickle
from sklearn.tree._classes import DecisionTreeClassifier


def test_model_file_exists():
    """ Should correctly ensure that the model's file exists. """
    assert os.path.isfile('curtis/model/curtis.sav')


def test_model_loads_correctly():
    """ Should correctly load the model. """
    with open('curtis/model/curtis.sav', 'rb') as f:
        model = pickle.load(f)

        assert isinstance(model, DecisionTreeClassifier)
