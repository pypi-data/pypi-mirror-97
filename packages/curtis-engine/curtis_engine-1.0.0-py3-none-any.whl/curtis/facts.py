from .exceptions import CurtisParameterError
from .utils.validation import validation_bounds


class CurtisFacts:
    """
    Curtis facts

    Represents the shape & data models of the Curtis engine. Instances of this class
    get declared on the engine's `declare_facts` method in order to pass a patient's
    information to the system and perform a diagnosis.
    """

    def __init__(self, sex: int, age: int, height: float, weight: float, HR: float, Pd: float, PQ: float, QRS: float, QT: float, QTcFra: float):
        """
        Create a list of facts and assign all values to their corresponding properties

        This values must be carefully declared and must met a certain set of validations in
        order for the fact to be valid. Each property has a setter and an accessor in order
        to guarantee the diagnosis' integrity.
        """

        self.sex = sex
        self.age = age
        self.height = height
        self.weight = weight
        self.HR = HR
        self.Pd = Pd
        self.PQ = PQ
        self.QRS = QRS
        self.QT = QT
        self.QTcFra = QTcFra

    @property
    def sex(self):
        """
        Sex property

        Defines a person's gender.
        """
        return self._sex

    @property
    def age(self):
        """
        Age property

        Defines a person's age.
        """
        return self._age

    @property
    def height(self):
        """
        Height property

        Defines a person's height.
        """
        return self._height

    @property
    def weight(self):
        """
        Age property

        Defines a person's age.
        """
        return self._weight

    @property
    def HR(self):
        """
        HR property

        Defines a person's HR wave value.
        """
        return self._HR

    @property
    def Pd(self):
        """
        Pd property

        Defines a person's Pd wave value.
        """
        return self._Pd

    @property
    def PQ(self):
        """
        PQ property

        Defines a person's PQ segment value.
        """
        return self._PQ

    @property
    def QRS(self):
        """
        QRS property

        Defines a person's QRS segment value.
        """
        return self._QRS

    @property
    def QT(self):
        """
        QRS property

        Defines a person's QRS segment value.
        """
        return self._QT

    @property
    def QTcFra(self):
        """
        QTcFra property

        Defines a person's QTcFra wave value.
        """
        return self._QTcFra

    @sex.setter
    def sex(self, value: int):
        """
        Sex property setter

        Assigns and validates the fact's sex property.
        """
        if value != validation_bounds['sex']['min'] and value != validation_bounds['sex']['max']:
            raise CurtisParameterError(validation_bounds['sex']['reason'])

        self._sex = value

    @age.setter
    def age(self, value: int):
        """
        Age property setter

        Assigns and validates the fact's age property.
        """
        if value < validation_bounds['age']['min'] or value > validation_bounds['age']['max']:
            raise CurtisParameterError(validation_bounds['age']['reason'])

        self._age = value

    @height.setter
    def height(self, value: int):
        """
        Height property setter

        Assigns and validates the fact's height property.
        """
        if value < validation_bounds['height']['min'] or value > validation_bounds['height']['max']:
            raise CurtisParameterError(validation_bounds['height']['reason'])

        self._height = value

    @weight.setter
    def weight(self, value: int):
        """
        Weight property setter

        Assigns and validates the fact's weight property.
        """
        if value < validation_bounds['weight']['min'] or value > validation_bounds['weight']['max']:
            raise CurtisParameterError(validation_bounds['weight']['reason'])

        self._weight = value

    @HR.setter
    def HR(self, value: int):
        """
        HR property setter

        Assigns and validates the fact's HR property.
        """
        if value < validation_bounds['HR']['min'] or value > validation_bounds['HR']['max']:
            raise CurtisParameterError(validation_bounds['HR']['reason'])

        self._HR = value

    @Pd.setter
    def Pd(self, value: int):
        """
        Pd property setter

        Assigns and validates the fact's Pd property.
        """
        if value < validation_bounds['Pd']['min'] or value > validation_bounds['Pd']['max']:
            raise CurtisParameterError(validation_bounds['Pd']['reason'])

        self._Pd = value

    @PQ.setter
    def PQ(self, value: int):
        """
        PQ property setter

        Assigns and validates the fact's PQ property.
        """
        if value < validation_bounds['PQ']['min'] or value > validation_bounds['PQ']['max']:
            raise CurtisParameterError(validation_bounds['PQ']['reason'])

        self._PQ = value

    @QRS.setter
    def QRS(self, value: int):
        """
        QRS property setter

        Assigns and validates the fact's QRS property.
        """
        if value < validation_bounds['QRS']['min'] or value > validation_bounds['QRS']['max']:
            raise CurtisParameterError(validation_bounds['QRS']['reason'])

        self._QRS = value

    @QT.setter
    def QT(self, value: int):
        """
        QT property setter

        Assigns and validates the fact's QT property.
        """
        if value < validation_bounds['QT']['min'] or value > validation_bounds['QT']['max']:
            raise CurtisParameterError(validation_bounds['QT']['reason'])

        self._QT = value

    @QTcFra.setter
    def QTcFra(self, value: int):
        """
        QTcFra property setter

        Assigns and validates the fact's QTcFra property.
        """
        if value < validation_bounds['QTcFra']['min'] or value > validation_bounds['QTcFra']['max']:
            raise CurtisParameterError(validation_bounds['QTcFra']['reason'])

        self._QTcFra = value
