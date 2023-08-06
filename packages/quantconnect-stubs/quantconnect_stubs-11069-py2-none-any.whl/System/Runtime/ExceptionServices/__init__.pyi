import typing

import System
import System.Runtime.ExceptionServices


class HandleProcessCorruptedStateExceptionsAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class FirstChanceExceptionEventArgs(System.EventArgs):
    """This class has no documentation."""

    @property
    def Exception(self) -> System.Exception:
        ...

    def __init__(self, exception: System.Exception) -> None:
        ...


class ExceptionDispatchInfo(System.Object):
    """This class has no documentation."""

    @property
    def SourceException(self) -> System.Exception:
        ...

    @staticmethod
    def Capture(source: System.Exception) -> System.Runtime.ExceptionServices.ExceptionDispatchInfo:
        ...

    @typing.overload
    def Throw(self) -> None:
        ...

    @staticmethod
    @typing.overload
    def Throw(source: System.Exception) -> None:
        ...

    @staticmethod
    def SetCurrentStackTrace(source: System.Exception) -> System.Exception:
        """
        Stores the current stack trace into the specified Exception instance.
        
        :param source: The unthrown Exception instance.
        :returns: The  exception instance.
        """
        ...


