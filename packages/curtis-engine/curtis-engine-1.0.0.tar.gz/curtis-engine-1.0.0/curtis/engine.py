import os
import pickle
from .facts import CurtisFacts
from .exceptions import CurtisIntegrityError


class CurtisEngine:
    """
    The Curtis engine

    This class will act as the inference engine of an expert system, in which an initial
    facts lists must be declared in order for curtis to run and perform a diagnosis. This facts
    must be passed as a `CurtisFacts` object, that contains automatic validation for each
    expected field.
    """

    def __init__(self):
        """
        Engine constructor

        When instantiating a `CurtisEngine` object, the engine's model gets
        loaded and placed into the `engine` variable, it is necessary since 
        all classification tasks are performed by the engine.
        """
        here = os.path.dirname(os.path.abspath(__file__))

        try:
            with open(os.path.join(here, "model", "curtis.sav"), "rb") as f:
                self.engine = pickle.load(f)
        except:
            raise CurtisIntegrityError(
                "The curtis model file appears to be missing/corrupted")

    def declare_facts(self, facts: CurtisFacts):
        """
        Facts declaration

        To declare a set of facts, a `CurtisFacts` object must be passed in order for the engine
        to store it, the `CurtisFacts` object automatically performs validation to each 
        field, making sure no value is going to affect the decision/diagnosis.

        Parameters
        ----------
        :param facts: The general facts that contain a patient's ECG values

        Returns
        -------
        :return: None
        """
        self.facts = facts

    def diagnose(self):
        """
        Perform a diagnostic.

        After facts are declared, the engine now performs a diagnostic over the
        provided values, which get passed to the inner's decision-making module
        and returns a diagnostic index. The returned diagnostic index must be
        passed to the `utils.encoding.diagnosis_indexes` dictionary as a key
        in order to obtain the diagnostis' title.

        Returns
        -------
        :return: A diagnosis index
        """
        diagnosis = self.engine.predict([
            [
                self.facts.sex,
                self.facts.age,
                self.facts.height,
                self.facts.weight,
                self.facts.HR,
                self.facts.Pd,
                self.facts.PQ,
                self.facts.QRS,
                self.facts.QT,
                self.facts.QTcFra
            ]
        ])

        return diagnosis[0]
