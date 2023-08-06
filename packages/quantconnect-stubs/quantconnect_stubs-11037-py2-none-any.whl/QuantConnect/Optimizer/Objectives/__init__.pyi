import abc
import typing

import QuantConnect.Optimizer.Objectives
import QuantConnect.Util
import System

System_EventHandler = typing.Any


class Extremum(System.Object):
    """
    Define the way to compare current real-values and the new one (candidates).
    It's encapsulated in different abstraction to allow configure the direction of optimization, i.e. max or min.
    """

    def __init__(self, comparer: typing.Callable[[float, float], bool]) -> None:
        """
        Create an instance of Extremum to compare values.
        
        :param comparer: The way old and new values should be compared
        """
        ...

    def Better(self, current: float, candidate: float) -> bool:
        """
        Compares two values; identifies whether condition is met or not.
        
        :param current: Left operand
        :param candidate: Right operand
        :returns: Returns the result of comparer with this arguments.
        """
        ...


class ExtremumJsonConverter(QuantConnect.Util.TypeChangeJsonConverter[QuantConnect.Optimizer.Objectives.Extremum, str]):
    """This class has no documentation."""

    @property
    def PopulateProperties(self) -> bool:
        """
        Don't populate any property
        
        This property is protected.
        """
        ...

    @typing.overload
    def Convert(self, value: QuantConnect.Optimizer.Objectives.Extremum) -> str:
        """This method is protected."""
        ...

    @typing.overload
    def Convert(self, value: str) -> QuantConnect.Optimizer.Objectives.Extremum:
        """This method is protected."""
        ...


class Objective(System.Object, metaclass=abc.ABCMeta):
    """Base class for optimization Objectives.Target and Constraint"""

    @property
    def Target(self) -> str:
        """Target; property of json file we want to track"""
        ...

    @property
    def TargetValue(self) -> typing.Optional[float]:
        """Target value"""
        ...

    def __init__(self, target: str, targetValue: typing.Optional[float]) -> None:
        """
        Creates a new instance
        
        This method is protected.
        """
        ...


class Constraint(QuantConnect.Optimizer.Objectives.Objective):
    """
    A backtest optimization constraint.
    Allows specifying statistical constraints for the optimization, eg. a backtest can't have a DrawDown less than 10%
    """

    @property
    def Operator(self) -> int:
        """
        The target comparison operation, eg. 'Greater'
        
        This property contains the int value of a member of the QuantConnect.Util.ComparisonOperatorTypes enum.
        """
        ...

    def __init__(self, target: str, operator: QuantConnect.Util.ComparisonOperatorTypes, targetValue: typing.Optional[float]) -> None:
        """Creates a new instance"""
        ...

    def IsMet(self, jsonBacktestResult: str) -> bool:
        """Asserts the constraint is met"""
        ...

    def ToString(self) -> str:
        """Pretty representation of a constraint"""
        ...


class Minimization(QuantConnect.Optimizer.Objectives.Extremum):
    """Defines standard minimization strategy, i.e. right operand is less than left"""

    def __init__(self) -> None:
        """Creates an instance of Minimization"""
        ...


class Target(QuantConnect.Optimizer.Objectives.Objective):
    """The optimization statistical target"""

    @property
    def Extremum(self) -> QuantConnect.Optimizer.Objectives.Extremum:
        """Defines the direction of optimization, i.e. maximization or minimization"""
        ...

    @property
    def Current(self) -> typing.Optional[float]:
        """Current value"""
        ...

    @Current.setter
    def Current(self, value: typing.Optional[float]):
        """Current value"""
        ...

    @property
    def Reached(self) -> typing.List[System_EventHandler]:
        """Fires when target complies specified value"""
        ...

    @Reached.setter
    def Reached(self, value: typing.List[System_EventHandler]):
        """Fires when target complies specified value"""
        ...

    def __init__(self, target: str, extremum: QuantConnect.Optimizer.Objectives.Extremum, targetValue: typing.Optional[float]) -> None:
        """Creates a new instance"""
        ...

    def ToString(self) -> str:
        """Pretty representation of this optimization target"""
        ...

    def MoveAhead(self, jsonBacktestResult: str) -> bool:
        """
        Check backtest result
        
        :param jsonBacktestResult: Backtest result json
        :returns: true if found a better solution; otherwise false.
        """
        ...

    def CheckCompliance(self) -> None:
        """Try comply target value"""
        ...


class Maximization(QuantConnect.Optimizer.Objectives.Extremum):
    """Defines standard maximization strategy, i.e. right operand is great than left"""

    def __init__(self) -> None:
        """Creates an instance of Maximization"""
        ...


