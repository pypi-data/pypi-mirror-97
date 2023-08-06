import typing

import System
import System.Runtime
import System.Runtime.ConstrainedExecution


class AssemblyTargetedPatchBandAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def TargetedPatchBand(self) -> str:
        ...

    def __init__(self, targetedPatchBand: str) -> None:
        ...


class TargetedPatchingOptOutAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Reason(self) -> str:
        ...

    def __init__(self, reason: str) -> None:
        ...


class AmbiguousImplementationException(System.Exception):
    """This class has no documentation."""

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...


class MemoryFailPoint(System.Runtime.ConstrainedExecution.CriticalFinalizerObject, System.IDisposable):
    """This class has no documentation."""

    MemoryFailPointReservedMemory: int

    def __init__(self, sizeInMegabytes: int) -> None:
        ...

    def Dispose(self) -> None:
        ...


class ProfileOptimization(System.Object):
    """This class has no documentation."""

    @staticmethod
    def SetProfileRoot(directoryPath: str) -> None:
        ...

    @staticmethod
    def StartProfile(profile: str) -> None:
        ...


class GCLargeObjectHeapCompactionMode(System.Enum):
    """This class has no documentation."""

    Default = 1

    CompactOnce = 2


class GCLatencyMode(System.Enum):
    """This class has no documentation."""

    Batch = 0

    Interactive = 1

    LowLatency = 2

    SustainedLowLatency = 3

    NoGCRegion = 4


class GCSettings(System.Object):
    """This class has no documentation."""

    LatencyMode: int
    """This property contains the int value of a member of the System.Runtime.GCLatencyMode enum."""

    LargeObjectHeapCompactionMode: int
    """This property contains the int value of a member of the System.Runtime.GCLargeObjectHeapCompactionMode enum."""

    IsServerGC: bool


