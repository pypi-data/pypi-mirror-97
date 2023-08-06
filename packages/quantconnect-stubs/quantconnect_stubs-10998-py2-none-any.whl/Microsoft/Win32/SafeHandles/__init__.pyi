import abc
import typing

import Microsoft.Win32.SafeHandles
import System
import System.Runtime.InteropServices
import System.Threading

Interop_ErrorInfo = typing.Any


class SafeHandleZeroOrMinusOneIsInvalid(System.Runtime.InteropServices.SafeHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def IsInvalid(self) -> bool:
        ...

    def __init__(self, ownsHandle: bool) -> None:
        """This method is protected."""
        ...


class SafeWaitHandle(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid):
    """This class has no documentation."""

    @typing.overload
    def ReleaseHandle(self) -> bool:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, existingHandle: System.IntPtr, ownsHandle: bool) -> None:
        ...

    @typing.overload
    def ReleaseHandle(self) -> bool:
        """This method is protected."""
        ...

    @typing.overload
    def ReleaseHandle(self) -> bool:
        """This method is protected."""
        ...


class SafeHandleMinusOneIsInvalid(System.Runtime.InteropServices.SafeHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def IsInvalid(self) -> bool:
        ...

    def __init__(self, ownsHandle: bool) -> None:
        """This method is protected."""
        ...


class SafeFileHandle(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid):
    """This class has no documentation."""

    @property
    def IsAsync(self) -> typing.Optional[bool]:
        ...

    @IsAsync.setter
    def IsAsync(self, value: typing.Optional[bool]):
        ...

    t_lastCloseErrorInfo: typing.Optional[Interop_ErrorInfo]

    @property
    def IsInvalid(self) -> bool:
        ...

    @property
    def ThreadPoolBinding(self) -> System.Threading.ThreadPoolBoundHandle:
        ...

    @ThreadPoolBinding.setter
    def ThreadPoolBinding(self, value: System.Threading.ThreadPoolBoundHandle):
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, preexistingHandle: System.IntPtr, ownsHandle: bool) -> None:
        ...

    @typing.overload
    def ReleaseHandle(self) -> bool:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, preexistingHandle: System.IntPtr, ownsHandle: bool) -> None:
        ...

    @typing.overload
    def ReleaseHandle(self) -> bool:
        """This method is protected."""
        ...


class CriticalHandleMinusOneIsInvalid(System.Runtime.InteropServices.CriticalHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def IsInvalid(self) -> bool:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...


class CriticalHandleZeroOrMinusOneIsInvalid(System.Runtime.InteropServices.CriticalHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def IsInvalid(self) -> bool:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...


