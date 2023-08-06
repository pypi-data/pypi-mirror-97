import abc
import datetime
import typing

import Microsoft.Win32.SafeHandles
import System
import System.Collections.Generic
import System.Globalization
import System.Runtime.CompilerServices
import System.Runtime.ConstrainedExecution
import System.Runtime.InteropServices
import System.Runtime.Serialization
import System.Security.Principal
import System.Threading
import System.Threading.Tasks

Timer = typing.Any
typing_Any = typing.Any
System_Threading_SendOrPostCallback = typing.Any
System_Threading_ThreadStart = typing.Any
System_Threading_ParameterizedThreadStart = typing.Any
System_Threading_CancellationTokenRegistration = typing.Any
System_Threading_ContextCallback = typing.Any
System_Threading_AsyncFlowControl = typing.Any
System_Threading_IOCompletionCallback = typing.Any

System_Threading_Volatile_Read_T = typing.TypeVar("System_Threading_Volatile_Read_T")
System_Threading_Volatile_Write_T = typing.TypeVar("System_Threading_Volatile_Write_T")
System_Threading_Interlocked_CompareExchange_T = typing.TypeVar("System_Threading_Interlocked_CompareExchange_T")
System_Threading_Interlocked_Exchange_T = typing.TypeVar("System_Threading_Interlocked_Exchange_T")
System_Threading_LazyInitializer_EnsureInitialized_T = typing.TypeVar("System_Threading_LazyInitializer_EnsureInitialized_T")
System_Threading_ThreadLocal_T = typing.TypeVar("System_Threading_ThreadLocal_T")
System_Threading_AsyncLocal_T = typing.TypeVar("System_Threading_AsyncLocal_T")
System_Threading_AsyncLocalValueChangedArgs_T = typing.TypeVar("System_Threading_AsyncLocalValueChangedArgs_T")


class WaitHandleCannotBeOpenedException(System.ApplicationException):
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

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class WaitHandle(System.MarshalByRefObject, System.IDisposable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    MaxWaitHandles: int = 64

    InvalidHandle: System.IntPtr = ...
    """This field is protected."""

    WaitSuccess: int = 0

    WaitAbandoned: int = ...

    WaitTimeout: int = ...

    @property
    def Handle(self) -> System.IntPtr:
        ...

    @Handle.setter
    def Handle(self, value: System.IntPtr):
        ...

    @property
    def SafeWaitHandle(self) -> Microsoft.Win32.SafeHandles.SafeWaitHandle:
        ...

    @SafeWaitHandle.setter
    def SafeWaitHandle(self, value: Microsoft.Win32.SafeHandles.SafeWaitHandle):
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def Close(self) -> None:
        ...

    @typing.overload
    def Dispose(self, explicitDisposing: bool) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    @typing.overload
    def WaitOne(self, millisecondsTimeout: int) -> bool:
        ...

    @typing.overload
    def WaitOne(self, timeout: datetime.timedelta) -> bool:
        ...

    @typing.overload
    def WaitOne(self) -> bool:
        ...

    @typing.overload
    def WaitOne(self, millisecondsTimeout: int, exitContext: bool) -> bool:
        ...

    @typing.overload
    def WaitOne(self, timeout: datetime.timedelta, exitContext: bool) -> bool:
        ...

    @staticmethod
    @typing.overload
    def WaitAll(waitHandles: typing.List[System.Threading.WaitHandle], millisecondsTimeout: int) -> bool:
        ...

    @staticmethod
    @typing.overload
    def WaitAll(waitHandles: typing.List[System.Threading.WaitHandle], timeout: datetime.timedelta) -> bool:
        ...

    @staticmethod
    @typing.overload
    def WaitAll(waitHandles: typing.List[System.Threading.WaitHandle]) -> bool:
        ...

    @staticmethod
    @typing.overload
    def WaitAll(waitHandles: typing.List[System.Threading.WaitHandle], millisecondsTimeout: int, exitContext: bool) -> bool:
        ...

    @staticmethod
    @typing.overload
    def WaitAll(waitHandles: typing.List[System.Threading.WaitHandle], timeout: datetime.timedelta, exitContext: bool) -> bool:
        ...

    @staticmethod
    @typing.overload
    def WaitAny(waitHandles: typing.List[System.Threading.WaitHandle], millisecondsTimeout: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def WaitAny(waitHandles: typing.List[System.Threading.WaitHandle], timeout: datetime.timedelta) -> int:
        ...

    @staticmethod
    @typing.overload
    def WaitAny(waitHandles: typing.List[System.Threading.WaitHandle]) -> int:
        ...

    @staticmethod
    @typing.overload
    def WaitAny(waitHandles: typing.List[System.Threading.WaitHandle], millisecondsTimeout: int, exitContext: bool) -> int:
        ...

    @staticmethod
    @typing.overload
    def WaitAny(waitHandles: typing.List[System.Threading.WaitHandle], timeout: datetime.timedelta, exitContext: bool) -> int:
        ...

    @staticmethod
    @typing.overload
    def SignalAndWait(toSignal: System.Threading.WaitHandle, toWaitOn: System.Threading.WaitHandle) -> bool:
        ...

    @staticmethod
    @typing.overload
    def SignalAndWait(toSignal: System.Threading.WaitHandle, toWaitOn: System.Threading.WaitHandle, timeout: datetime.timedelta, exitContext: bool) -> bool:
        ...

    @staticmethod
    @typing.overload
    def SignalAndWait(toSignal: System.Threading.WaitHandle, toWaitOn: System.Threading.WaitHandle, millisecondsTimeout: int, exitContext: bool) -> bool:
        ...


class ThreadStateException(System.SystemException):
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

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class Volatile(System.Object):
    """Methods for accessing memory with volatile semantics."""

    @staticmethod
    @typing.overload
    def Read(location: bool) -> bool:
        ...

    @staticmethod
    @typing.overload
    def Write(location: bool, value: bool) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Write(location: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: float) -> float:
        ...

    @staticmethod
    @typing.overload
    def Write(location: float, value: float) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Write(location: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Write(location: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Write(location: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: System.IntPtr) -> System.IntPtr:
        ...

    @staticmethod
    @typing.overload
    def Write(location: System.IntPtr, value: System.IntPtr) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Write(location: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: float) -> float:
        ...

    @staticmethod
    @typing.overload
    def Write(location: float, value: float) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Write(location: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Write(location: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Write(location: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: System.UIntPtr) -> System.UIntPtr:
        ...

    @staticmethod
    @typing.overload
    def Write(location: System.UIntPtr, value: System.UIntPtr) -> None:
        ...

    @staticmethod
    @typing.overload
    def Read(location: System_Threading_Volatile_Read_T) -> System_Threading_Volatile_Read_T:
        ...

    @staticmethod
    @typing.overload
    def Write(location: System_Threading_Volatile_Write_T, value: System_Threading_Volatile_Write_T) -> None:
        ...


class Any(typing_Any):
    """This class has no documentation."""

    MaxSupportedTimeout: int = ...

    ActiveCount: int
    """
    Gets the number of timers that are currently active. An active timer is registered to tick at some point in the
    future, and has not yet been canceled.
    """

    @typing.overload
    def __init__(self, callback: typing.Any, state: typing.Any, dueTime: int, period: int) -> None:
        ...

    @typing.overload
    def __init__(self, callback: typing.Any, state: typing.Any, dueTime: typing.Any, period: typing.Any) -> None:
        ...

    @typing.overload
    def __init__(self, callback: typing.Any, state: typing.Any, dueTime: int, period: int) -> None:
        ...

    @typing.overload
    def __init__(self, callback: typing.Any, state: typing.Any, dueTime: int, period: int) -> None:
        ...

    @typing.overload
    def __init__(self, callback: typing.Any) -> None:
        ...

    @typing.overload
    def Change(self, dueTime: int, period: int) -> bool:
        ...

    @typing.overload
    def Change(self, dueTime: typing.Any, period: typing.Any) -> bool:
        ...

    @typing.overload
    def Change(self, dueTime: int, period: int) -> bool:
        ...

    @typing.overload
    def Change(self, dueTime: int, period: int) -> bool:
        ...

    @typing.overload
    def Dispose(self, notifyObject: typing.Any) -> bool:
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    def DisposeAsync(self) -> System.Threading.Tasks.ValueTask:
        ...


class Timeout(System.Object):
    """This class has no documentation."""

    InfiniteTimeSpan: datetime.timedelta = ...

    Infinite: int = -1

    UnsignedInfinite: int = ...


class Interlocked(System.Object):
    """Provides atomic operations for variables that are shared by multiple threads."""

    @staticmethod
    @typing.overload
    def Increment(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Increment(location: int) -> int:
        """
        Increments a specified variable and stores the result, as an atomic operation.
        
        :param location: The variable whose value is to be incremented.
        :returns: The incremented value.
        """
        ...

    @staticmethod
    @typing.overload
    def Decrement(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Decrement(location: int) -> int:
        """
        Decrements a specified variable and stores the result, as an atomic operation.
        
        :param location: The variable whose value is to be decremented.
        :returns: The decremented value.
        """
        ...

    @staticmethod
    @typing.overload
    def Exchange(location1: int, value: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Exchange(location1: int, value: int) -> int:
        """
        Sets a 64-bit unsigned integer to a specified value and returns the original value, as an atomic operation.
        
        :param location1: The variable to set to the specified value.
        :param value: The value to which the  parameter is set.
        :returns: The original value of .
        """
        ...

    @staticmethod
    @typing.overload
    def Exchange(location1: System.IntPtr, value: System.IntPtr) -> System.IntPtr:
        """
        Sets a platform-specific handle or pointer to a specified value and returns the original value, as an atomic operation.
        
        :param location1: The variable to set to the specified value.
        :param value: The value to which the  parameter is set.
        :returns: The original value of .
        """
        ...

    @staticmethod
    @typing.overload
    def CompareExchange(location1: int, value: int, comparand: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def CompareExchange(location1: int, value: int, comparand: int) -> int:
        """
        Compares two 64-bit unsigned integers for equality and, if they are equal, replaces the first value.
        
        :param location1: The destination, whose value is compared with  and possibly replaced.
        :param value: The value that replaces the destination value if the comparison results in equality.
        :param comparand: The value that is compared to the value at .
        :returns: The original value in .
        """
        ...

    @staticmethod
    @typing.overload
    def CompareExchange(location1: System.IntPtr, value: System.IntPtr, comparand: System.IntPtr) -> System.IntPtr:
        """
        Compares two platform-specific handles or pointers for equality and, if they are equal, replaces the first one.
        
        :param location1: The destination IntPtr, whose value is compared with the value of  and possibly replaced by .
        :param value: The IntPtr that replaces the destination value if the comparison results in equality.
        :param comparand: The IntPtr that is compared to the value at .
        :returns: The original value in .
        """
        ...

    @staticmethod
    @typing.overload
    def Add(location1: int, value: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Add(location1: int, value: int) -> int:
        """
        Adds two 64-bit unsigned integers and replaces the first integer with the sum, as an atomic operation.
        
        :param location1: A variable containing the first value to be added. The sum of the two values is stored in .
        :param value: The value to be added to the integer at .
        :returns: The new value stored at .
        """
        ...

    @staticmethod
    @typing.overload
    def Read(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def And(location1: int, value: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def And(location1: int, value: int) -> int:
        """
        Bitwise "ands" two 32-bit unsigned integers and replaces the first integer with the result, as an atomic operation.
        
        :param location1: A variable containing the first value to be combined. The result is stored in .
        :param value: The value to be combined with the integer at .
        :returns: The original value in .
        """
        ...

    @staticmethod
    @typing.overload
    def And(location1: int, value: int) -> int:
        """
        Bitwise "ands" two 64-bit signed integers and replaces the first integer with the result, as an atomic operation.
        
        :param location1: A variable containing the first value to be combined. The result is stored in .
        :param value: The value to be combined with the integer at .
        :returns: The original value in .
        """
        ...

    @staticmethod
    @typing.overload
    def And(location1: int, value: int) -> int:
        """
        Bitwise "ands" two 64-bit unsigned integers and replaces the first integer with the result, as an atomic operation.
        
        :param location1: A variable containing the first value to be combined. The result is stored in .
        :param value: The value to be combined with the integer at .
        :returns: The original value in .
        """
        ...

    @staticmethod
    @typing.overload
    def Or(location1: int, value: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Or(location1: int, value: int) -> int:
        """
        Bitwise "ors" two 32-bit unsigned integers and replaces the first integer with the result, as an atomic operation.
        
        :param location1: A variable containing the first value to be combined. The result is stored in .
        :param value: The value to be combined with the integer at .
        :returns: The original value in .
        """
        ...

    @staticmethod
    @typing.overload
    def Or(location1: int, value: int) -> int:
        """
        Bitwise "ors" two 64-bit signed integers and replaces the first integer with the result, as an atomic operation.
        
        :param location1: A variable containing the first value to be combined. The result is stored in .
        :param value: The value to be combined with the integer at .
        :returns: The original value in .
        """
        ...

    @staticmethod
    @typing.overload
    def Or(location1: int, value: int) -> int:
        """
        Bitwise "ors" two 64-bit unsigned integers and replaces the first integer with the result, as an atomic operation.
        
        :param location1: A variable containing the first value to be combined. The result is stored in .
        :param value: The value to be combined with the integer at .
        :returns: The original value in .
        """
        ...

    @staticmethod
    @typing.overload
    def CompareExchange(location1: int, value: int, comparand: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def CompareExchange(location1: typing.Any, value: typing.Any, comparand: typing.Any) -> System.Object:
        ...

    @staticmethod
    @typing.overload
    def CompareExchange(location1: float, value: float, comparand: float) -> float:
        ...

    @staticmethod
    @typing.overload
    def Decrement(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Decrement(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Increment(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Increment(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Exchange(location1: int, value: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Exchange(location1: typing.Any, value: typing.Any) -> System.Object:
        ...

    @staticmethod
    @typing.overload
    def Exchange(location1: float, value: float) -> float:
        ...

    @staticmethod
    @typing.overload
    def CompareExchange(location1: int, value: int, comparand: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def CompareExchange(location1: float, value: float, comparand: float) -> float:
        ...

    @staticmethod
    @typing.overload
    def CompareExchange(location1: System_Threading_Interlocked_CompareExchange_T, value: System_Threading_Interlocked_CompareExchange_T, comparand: System_Threading_Interlocked_CompareExchange_T) -> System_Threading_Interlocked_CompareExchange_T:
        ...

    @staticmethod
    @typing.overload
    def Exchange(location1: int, value: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Exchange(location1: float, value: float) -> float:
        ...

    @staticmethod
    @typing.overload
    def Exchange(location1: System_Threading_Interlocked_Exchange_T, value: System_Threading_Interlocked_Exchange_T) -> System_Threading_Interlocked_Exchange_T:
        ...

    @staticmethod
    @typing.overload
    def Read(location: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Add(location1: int, value: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def Add(location1: int, value: int) -> int:
        ...

    @staticmethod
    def MemoryBarrier() -> None:
        ...

    @staticmethod
    def MemoryBarrierProcessWide() -> None:
        ...


class LazyInitializer(System.Object):
    """Provides lazy initialization routines."""

    @staticmethod
    @typing.overload
    def EnsureInitialized(target: System_Threading_LazyInitializer_EnsureInitialized_T) -> System_Threading_LazyInitializer_EnsureInitialized_T:
        """
        Initializes a target reference type with the type's default constructor if the target has not
        already been initialized.
        
        :param target: A reference of type T to initialize if it has not already been initialized.
        :returns: The initialized reference of type T.
        """
        ...

    @staticmethod
    @typing.overload
    def EnsureInitialized(target: System_Threading_LazyInitializer_EnsureInitialized_T, valueFactory: typing.Callable[[], System_Threading_LazyInitializer_EnsureInitialized_T]) -> System_Threading_LazyInitializer_EnsureInitialized_T:
        """
        Initializes a target reference type using the specified function if it has not already been
        initialized.
        
        :param target: The reference of type T to initialize if it has not already been initialized.
        :param valueFactory: The System.Func{T} invoked to initialize the reference.
        :returns: The initialized reference of type T.
        """
        ...

    @staticmethod
    @typing.overload
    def EnsureInitialized(target: System_Threading_LazyInitializer_EnsureInitialized_T, initialized: bool, syncLock: typing.Any) -> System_Threading_LazyInitializer_EnsureInitialized_T:
        """
        Initializes a target reference or value type with its default constructor if it has not already
        been initialized.
        
        :param target: A reference or value of type T to initialize if it has not already been initialized.
        :param initialized: A reference to a boolean that determines whether the target has already been initialized.
        :param syncLock: A reference to an object used as the mutually exclusive lock for initializing . If  is null, and if the target hasn't already been initialized, a new object will be instantiated.
        :returns: The initialized value of type T.
        """
        ...

    @staticmethod
    @typing.overload
    def EnsureInitialized(target: System_Threading_LazyInitializer_EnsureInitialized_T, initialized: bool, syncLock: typing.Any, valueFactory: typing.Callable[[], System_Threading_LazyInitializer_EnsureInitialized_T]) -> System_Threading_LazyInitializer_EnsureInitialized_T:
        """
        Initializes a target reference or value type with a specified function if it has not already been
        initialized.
        
        :param target: A reference or value of type T to initialize if it has not already been initialized.
        :param initialized: A reference to a boolean that determines whether the target has already been initialized.
        :param syncLock: A reference to an object used as the mutually exclusive lock for initializing . If  is null, and if the target hasn't already been initialized, a new object will be instantiated.
        :param valueFactory: The System.Func{T} invoked to initialize the reference or value.
        :returns: The initialized value of type T.
        """
        ...

    @staticmethod
    @typing.overload
    def EnsureInitialized(target: System_Threading_LazyInitializer_EnsureInitialized_T, syncLock: typing.Any, valueFactory: typing.Callable[[], System_Threading_LazyInitializer_EnsureInitialized_T]) -> System_Threading_LazyInitializer_EnsureInitialized_T:
        """
        Initializes a target reference type with a specified function if it has not already been initialized.
        
        :param target: A reference of type T to initialize if it has not already been initialized.
        :param syncLock: A reference to an object used as the mutually exclusive lock for initializing . If  is null, and if the target hasn't already been initialized, a new object will be instantiated.
        :param valueFactory: The System.Func{T} invoked to initialize the reference.
        :returns: The initialized value of type T.
        """
        ...


class Mutex(System.Threading.WaitHandle):
    """Synchronization primitive that can also be used for interprocess synchronization"""

    @typing.overload
    def ReleaseMutex(self) -> None:
        ...

    @typing.overload
    def __init__(self, initiallyOwned: bool, name: str, createdNew: bool) -> None:
        ...

    @typing.overload
    def __init__(self, initiallyOwned: bool, name: str) -> None:
        ...

    @typing.overload
    def __init__(self, initiallyOwned: bool) -> None:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @staticmethod
    def OpenExisting(name: str) -> System.Threading.Mutex:
        ...

    @staticmethod
    def TryOpenExisting(name: str, result: System.Threading.Mutex) -> bool:
        ...

    @typing.overload
    def ReleaseMutex(self) -> None:
        ...

    @typing.overload
    def ReleaseMutex(self) -> None:
        ...


class Semaphore(System.Threading.WaitHandle):
    """This class has no documentation."""

    @typing.overload
    def __init__(self, initialCount: int, maximumCount: int) -> None:
        ...

    @typing.overload
    def __init__(self, initialCount: int, maximumCount: int, name: str) -> None:
        ...

    @typing.overload
    def __init__(self, initialCount: int, maximumCount: int, name: str, createdNew: bool) -> None:
        ...

    @staticmethod
    def OpenExisting(name: str) -> System.Threading.Semaphore:
        ...

    @staticmethod
    def TryOpenExisting(name: str, result: System.Threading.Semaphore) -> bool:
        ...

    @typing.overload
    def Release(self) -> int:
        ...

    @typing.overload
    def Release(self, releaseCount: int) -> int:
        ...


class CancellationToken:
    """Propagates notification that operations should be canceled."""

    # Cannot convert to Python: None: System.Threading.CancellationToken

    @property
    def IsCancellationRequested(self) -> bool:
        """Gets whether cancellation has been requested for this token."""
        ...

    @property
    def CanBeCanceled(self) -> bool:
        """Gets whether this token is capable of being in the canceled state."""
        ...

    @property
    def WaitHandle(self) -> System.Threading.WaitHandle:
        """Gets a System.Threading.WaitHandle that is signaled when the token is canceled."""
        ...

    def __init__(self, canceled: bool) -> None:
        """
        Initializes the System.Threading.CancellationToken.
        
        :param canceled: The canceled state for the token.
        """
        ...

    @typing.overload
    def Register(self, callback: System.Action) -> System.Threading.CancellationTokenRegistration:
        """
        Registers a delegate that will be called when this System.Threading.CancellationToken is canceled.
        
        :param callback: The delegate to be executed when the System.Threading.CancellationToken is canceled.
        :returns: The System.Threading.CancellationTokenRegistration instance that can be used to unregister the callback.
        """
        ...

    @typing.overload
    def Register(self, callback: System.Action, useSynchronizationContext: bool) -> System.Threading.CancellationTokenRegistration:
        """
        Registers a delegate that will be called when this
        System.Threading.CancellationToken is canceled.
        
        :param callback: The delegate to be executed when the System.Threading.CancellationToken is canceled.
        :param useSynchronizationContext: A Boolean value that indicates whether to capture the current System.Threading.SynchronizationContext and use it when invoking the .
        :returns: The System.Threading.CancellationTokenRegistration instance that can be used to unregister the callback.
        """
        ...

    @typing.overload
    def Register(self, callback: typing.Callable[[System.Object], None], state: typing.Any) -> System.Threading.CancellationTokenRegistration:
        """
        Registers a delegate that will be called when this
        System.Threading.CancellationToken is canceled.
        
        :param callback: The delegate to be executed when the System.Threading.CancellationToken is canceled.
        :param state: The state to pass to the  when the delegate is invoked.  This may be null.
        :returns: The System.Threading.CancellationTokenRegistration instance that can be used to unregister the callback.
        """
        ...

    @typing.overload
    def Register(self, callback: typing.Callable[[System.Object, System.Threading.CancellationToken], None], state: typing.Any) -> System.Threading.CancellationTokenRegistration:
        """
        Registers a delegate that will be called when this CancellationToken is canceled.
        
        :param callback: The delegate to be executed when the System.Threading.CancellationToken is canceled.
        :param state: The state to pass to the  when the delegate is invoked.  This may be null.
        :returns: The CancellationTokenRegistration instance that can be used to unregister the callback.
        """
        ...

    @typing.overload
    def Register(self, callback: typing.Callable[[System.Object], None], state: typing.Any, useSynchronizationContext: bool) -> System.Threading.CancellationTokenRegistration:
        """
        Registers a delegate that will be called when this
        System.Threading.CancellationToken is canceled.
        
        :param callback: The delegate to be executed when the System.Threading.CancellationToken is canceled.
        :param state: The state to pass to the  when the delegate is invoked.  This may be null.
        :param useSynchronizationContext: A Boolean value that indicates whether to capture the current System.Threading.SynchronizationContext and use it when invoking the .
        :returns: The System.Threading.CancellationTokenRegistration instance that can be used to unregister the callback.
        """
        ...

    @typing.overload
    def UnsafeRegister(self, callback: typing.Callable[[System.Object], None], state: typing.Any) -> System.Threading.CancellationTokenRegistration:
        """
        Registers a delegate that will be called when this
        System.Threading.CancellationToken is canceled.
        
        :param callback: The delegate to be executed when the System.Threading.CancellationToken is canceled.
        :param state: The state to pass to the  when the delegate is invoked.  This may be null.
        :returns: The System.Threading.CancellationTokenRegistration instance that can be used to unregister the callback.
        """
        ...

    @typing.overload
    def UnsafeRegister(self, callback: typing.Callable[[System.Object, System.Threading.CancellationToken], None], state: typing.Any) -> System.Threading.CancellationTokenRegistration:
        """
        Registers a delegate that will be called when this CancellationToken is canceled.
        
        :param callback: The delegate to be executed when the System.Threading.CancellationToken is canceled.
        :param state: The state to pass to the  when the delegate is invoked.  This may be null.
        :returns: The CancellationTokenRegistration instance that can be used to unregister the callback.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Threading.CancellationToken) -> bool:
        """
        Determines whether the current System.Threading.CancellationToken instance is equal to the
        specified token.
        
        :param other: The other System.Threading.CancellationToken to which to compare this instance.
        :returns: True if the instances are equal; otherwise, false. Two tokens are equal if they are associated with the same System.Threading.CancellationTokenSource or if they were both constructed from public CancellationToken constructors and their IsCancellationRequested values are equal.
        """
        ...

    @typing.overload
    def Equals(self, other: typing.Any) -> bool:
        """
        Determines whether the current System.Threading.CancellationToken instance is equal to the
        specified object.
        
        :param other: The other object to which to compare this instance.
        :returns: True if  is a System.Threading.CancellationToken and if the two instances are equal; otherwise, false. Two tokens are equal if they are associated with the same System.Threading.CancellationTokenSource or if they were both constructed from public CancellationToken constructors and their IsCancellationRequested values are equal.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Serves as a hash function for a System.Threading.CancellationToken.
        
        :returns: A hash code for the current System.Threading.CancellationToken instance.
        """
        ...

    def ThrowIfCancellationRequested(self) -> None:
        """
        Throws a System.OperationCanceledException if
        this token has had cancellation requested.
        """
        ...


class ManualResetEventSlim(System.Object, System.IDisposable):
    """This class has no documentation."""

    @property
    def WaitHandle(self) -> System.Threading.WaitHandle:
        ...

    @property
    def IsSet(self) -> bool:
        """Gets whether the event is set."""
        ...

    @IsSet.setter
    def IsSet(self, value: bool):
        """Gets whether the event is set."""
        ...

    @property
    def SpinCount(self) -> int:
        """Gets the number of spin waits that will be occur before falling back to a true wait."""
        ...

    @SpinCount.setter
    def SpinCount(self, value: int):
        """Gets the number of spin waits that will be occur before falling back to a true wait."""
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, initialState: bool) -> None:
        """
        Initializes a new instance of the ManualResetEventSlim
        class with a boolean value indicating whether to set the initial state to signaled.
        
        :param initialState: true to set the initial state signaled; false to set the initial state to nonsignaled.
        """
        ...

    @typing.overload
    def __init__(self, initialState: bool, spinCount: int) -> None:
        """
        Initializes a new instance of the ManualResetEventSlim
        class with a Boolean value indicating whether to set the initial state to signaled and a specified
        spin count.
        
        :param initialState: true to set the initial state to signaled; false to set the initial state to nonsignaled.
        :param spinCount: The number of spin waits that will occur before falling back to a true wait.
        """
        ...

    def Set(self) -> None:
        """
        Sets the state of the event to signaled, which allows one or more threads waiting on the event to
        proceed.
        """
        ...

    def Reset(self) -> None:
        """Sets the state of the event to nonsignaled, which causes threads to block."""
        ...

    @typing.overload
    def Wait(self) -> None:
        """Blocks the current thread until the current ManualResetEventSlim is set."""
        ...

    @typing.overload
    def Wait(self, cancellationToken: System.Threading.CancellationToken) -> None:
        """
        Blocks the current thread until the current ManualResetEventSlim receives a signal,
        while observing a System.Threading.CancellationToken.
        
        :param cancellationToken: The System.Threading.CancellationToken to observe.
        """
        ...

    @typing.overload
    def Wait(self, timeout: datetime.timedelta) -> bool:
        """
        Blocks the current thread until the current ManualResetEventSlim is set, using a
        System.TimeSpan to measure the time interval.
        
        :param timeout: A System.TimeSpan that represents the number of milliseconds to wait, or a System.TimeSpan that represents -1 milliseconds to wait indefinitely.
        :returns: true if the System.Threading.ManualResetEventSlim was set; otherwise, false.
        """
        ...

    @typing.overload
    def Wait(self, timeout: datetime.timedelta, cancellationToken: System.Threading.CancellationToken) -> bool:
        """
        Blocks the current thread until the current ManualResetEventSlim is set, using a
        System.TimeSpan to measure the time interval, while observing a System.Threading.CancellationToken.
        
        :param timeout: A System.TimeSpan that represents the number of milliseconds to wait, or a System.TimeSpan that represents -1 milliseconds to wait indefinitely.
        :param cancellationToken: The System.Threading.CancellationToken to observe.
        :returns: true if the System.Threading.ManualResetEventSlim was set; otherwise, false.
        """
        ...

    @typing.overload
    def Wait(self, millisecondsTimeout: int) -> bool:
        """
        Blocks the current thread until the current ManualResetEventSlim is set, using a
        32-bit signed integer to measure the time interval.
        
        :param millisecondsTimeout: The number of milliseconds to wait, or Timeout.Infinite(-1) to wait indefinitely.
        :returns: true if the System.Threading.ManualResetEventSlim was set; otherwise, false.
        """
        ...

    @typing.overload
    def Wait(self, millisecondsTimeout: int, cancellationToken: System.Threading.CancellationToken) -> bool:
        """
        Blocks the current thread until the current ManualResetEventSlim is set, using a
        32-bit signed integer to measure the time interval, while observing a System.Threading.CancellationToken.
        
        :param millisecondsTimeout: The number of milliseconds to wait, or Timeout.Infinite(-1) to wait indefinitely.
        :param cancellationToken: The System.Threading.CancellationToken to observe.
        :returns: true if the System.Threading.ManualResetEventSlim was set; otherwise, false.
        """
        ...

    @typing.overload
    def Dispose(self) -> None:
        """Releases all resources used by the current instance of ManualResetEventSlim."""
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """
        When overridden in a derived class, releases the unmanaged resources used by the
        ManualResetEventSlim, and optionally releases the managed resources.
        
        This method is protected.
        
        :param disposing: true to release both managed and unmanaged resources; false to release only unmanaged resources.
        """
        ...


class LockRecursionException(System.Exception):
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

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class ThreadExceptionEventArgs(System.EventArgs):
    """This class has no documentation."""

    @property
    def Exception(self) -> System.Exception:
        ...

    def __init__(self, t: System.Exception) -> None:
        ...


class SynchronizationContext(System.Object):
    """This class has no documentation."""

    Current: System.Threading.SynchronizationContext

    def __init__(self) -> None:
        ...

    def SetWaitNotificationRequired(self) -> None:
        """This method is protected."""
        ...

    def IsWaitNotificationRequired(self) -> bool:
        ...

    def Send(self, d: System_Threading_SendOrPostCallback, state: typing.Any) -> None:
        ...

    def Post(self, d: System_Threading_SendOrPostCallback, state: typing.Any) -> None:
        ...

    def OperationStarted(self) -> None:
        """Optional override for subclasses, for responding to notification that operation is starting."""
        ...

    def OperationCompleted(self) -> None:
        """Optional override for subclasses, for responding to notification that operation has completed."""
        ...

    def Wait(self, waitHandles: typing.List[System.IntPtr], waitAll: bool, millisecondsTimeout: int) -> int:
        ...

    @staticmethod
    def WaitHelper(waitHandles: typing.List[System.IntPtr], waitAll: bool, millisecondsTimeout: int) -> int:
        """This method is protected."""
        ...

    @staticmethod
    def SetSynchronizationContext(syncContext: System.Threading.SynchronizationContext) -> None:
        ...

    def CreateCopy(self) -> System.Threading.SynchronizationContext:
        ...


class SemaphoreFullException(System.SystemException):
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

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class EventResetMode(System.Enum):
    """This class has no documentation."""

    AutoReset = 0

    ManualReset = 1


class EventWaitHandle(System.Threading.WaitHandle):
    """This class has no documentation."""

    @typing.overload
    def Reset(self) -> bool:
        ...

    @typing.overload
    def Set(self) -> bool:
        ...

    @typing.overload
    def Reset(self) -> bool:
        ...

    @typing.overload
    def Set(self) -> bool:
        ...

    @typing.overload
    def __init__(self, initialState: bool, mode: System.Threading.EventResetMode) -> None:
        ...

    @typing.overload
    def __init__(self, initialState: bool, mode: System.Threading.EventResetMode, name: str) -> None:
        ...

    @typing.overload
    def __init__(self, initialState: bool, mode: System.Threading.EventResetMode, name: str, createdNew: bool) -> None:
        ...

    @staticmethod
    def OpenExisting(name: str) -> System.Threading.EventWaitHandle:
        ...

    @staticmethod
    def TryOpenExisting(name: str, result: System.Threading.EventWaitHandle) -> bool:
        ...

    @typing.overload
    def Set(self) -> bool:
        ...

    @typing.overload
    def Reset(self) -> bool:
        ...


class ThreadInterruptedException(System.SystemException):
    """An exception class to indicate that the thread was interrupted from a waiting state."""

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class LockRecursionPolicy(System.Enum):
    """This class has no documentation."""

    NoRecursion = 0

    SupportsRecursion = 1


class ReaderWriterLockSlim(System.Object, System.IDisposable):
    """
    A reader-writer lock implementation that is intended to be simple, yet very
    efficient.  In particular only 1 interlocked operation is taken for any lock
    operation (we use spin locks to achieve this).  The spin lock is never held
    for more than a few instructions (in particular, we never call event APIs
    or in fact any non-trivial API while holding the spin lock).
    """

    @property
    def IsReadLockHeld(self) -> bool:
        ...

    @property
    def IsUpgradeableReadLockHeld(self) -> bool:
        ...

    @property
    def IsWriteLockHeld(self) -> bool:
        ...

    @property
    def RecursionPolicy(self) -> int:
        """This property contains the int value of a member of the System.Threading.LockRecursionPolicy enum."""
        ...

    @property
    def CurrentReadCount(self) -> int:
        ...

    @property
    def RecursiveReadCount(self) -> int:
        ...

    @property
    def RecursiveUpgradeCount(self) -> int:
        ...

    @property
    def RecursiveWriteCount(self) -> int:
        ...

    @property
    def WaitingReadCount(self) -> int:
        ...

    @property
    def WaitingUpgradeCount(self) -> int:
        ...

    @property
    def WaitingWriteCount(self) -> int:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, recursionPolicy: System.Threading.LockRecursionPolicy) -> None:
        ...

    def EnterReadLock(self) -> None:
        ...

    @typing.overload
    def TryEnterReadLock(self, timeout: datetime.timedelta) -> bool:
        ...

    @typing.overload
    def TryEnterReadLock(self, millisecondsTimeout: int) -> bool:
        ...

    def EnterWriteLock(self) -> None:
        ...

    @typing.overload
    def TryEnterWriteLock(self, timeout: datetime.timedelta) -> bool:
        ...

    @typing.overload
    def TryEnterWriteLock(self, millisecondsTimeout: int) -> bool:
        ...

    def EnterUpgradeableReadLock(self) -> None:
        ...

    @typing.overload
    def TryEnterUpgradeableReadLock(self, timeout: datetime.timedelta) -> bool:
        ...

    @typing.overload
    def TryEnterUpgradeableReadLock(self, millisecondsTimeout: int) -> bool:
        ...

    def ExitReadLock(self) -> None:
        ...

    def ExitWriteLock(self) -> None:
        ...

    def ExitUpgradeableReadLock(self) -> None:
        ...

    def Dispose(self) -> None:
        ...


class AsyncFlowControl(System.IEquatable[System_Threading_AsyncFlowControl], System.IDisposable):
    """This class has no documentation."""

    def Undo(self) -> None:
        ...

    def Dispose(self) -> None:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def Equals(self, obj: System.Threading.AsyncFlowControl) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class ExecutionContext(System.Object, System.IDisposable, System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    Default: System.Threading.ExecutionContext = ...

    @property
    def HasChangeNotifications(self) -> bool:
        ...

    @property
    def IsDefault(self) -> bool:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    @staticmethod
    def Capture() -> System.Threading.ExecutionContext:
        ...

    @staticmethod
    def SuppressFlow() -> System.Threading.AsyncFlowControl:
        ...

    @staticmethod
    def RestoreFlow() -> None:
        ...

    @staticmethod
    def IsFlowSuppressed() -> bool:
        ...

    @staticmethod
    def Run(executionContext: System.Threading.ExecutionContext, callback: System_Threading_ContextCallback, state: typing.Any) -> None:
        ...

    @staticmethod
    def Restore(executionContext: System.Threading.ExecutionContext) -> None:
        """
        Restores a captured execution context to on the current thread.
        
        :param executionContext: The ExecutionContext to set.
        """
        ...

    def CreateCopy(self) -> System.Threading.ExecutionContext:
        ...

    def Dispose(self) -> None:
        ...


class ApartmentState(System.Enum):
    """This class has no documentation."""

    STA = 0

    MTA = 1

    Unknown = 2


class CompressedStack(System.Object, System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    @staticmethod
    def Capture() -> System.Threading.CompressedStack:
        ...

    def CreateCopy(self) -> System.Threading.CompressedStack:
        ...

    @staticmethod
    def GetCompressedStack() -> System.Threading.CompressedStack:
        ...

    @staticmethod
    def Run(compressedStack: System.Threading.CompressedStack, callback: System_Threading_ContextCallback, state: typing.Any) -> None:
        ...


class Thread(System.Runtime.ConstrainedExecution.CriticalFinalizerObject):
    """This class has no documentation."""

    IsThreadStartSupported: bool = True

    @property
    def CurrentCulture(self) -> System.Globalization.CultureInfo:
        ...

    @CurrentCulture.setter
    def CurrentCulture(self, value: System.Globalization.CultureInfo):
        ...

    @property
    def CurrentUICulture(self) -> System.Globalization.CultureInfo:
        ...

    @CurrentUICulture.setter
    def CurrentUICulture(self, value: System.Globalization.CultureInfo):
        ...

    CurrentPrincipal: System.Security.Principal.IPrincipal

    CurrentThread: System.Threading.Thread

    @property
    def ExecutionContext(self) -> System.Threading.ExecutionContext:
        ...

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def ApartmentState(self) -> int:
        """This property contains the int value of a member of the System.Threading.ApartmentState enum."""
        ...

    @ApartmentState.setter
    def ApartmentState(self, value: int):
        """This property contains the int value of a member of the System.Threading.ApartmentState enum."""
        ...

    @property
    def thread_id(self) -> int:
        ...

    @thread_id.setter
    def thread_id(self, value: int):
        ...

    @property
    def threadpool_thread(self) -> bool:
        ...

    @threadpool_thread.setter
    def threadpool_thread(self, value: bool):
        ...

    @property
    def stack_size(self) -> int:
        ...

    @stack_size.setter
    def stack_size(self, value: int):
        ...

    @property
    def apartment_state(self) -> int:
        ...

    @apartment_state.setter
    def apartment_state(self, value: int):
        ...

    @property
    def managed_id(self) -> int:
        ...

    @managed_id.setter
    def managed_id(self, value: int):
        ...

    @property
    def _executionContext(self) -> System.Threading.ExecutionContext:
        ...

    @_executionContext.setter
    def _executionContext(self, value: System.Threading.ExecutionContext):
        ...

    @property
    def _synchronizationContext(self) -> System.Threading.SynchronizationContext:
        ...

    @_synchronizationContext.setter
    def _synchronizationContext(self, value: System.Threading.SynchronizationContext):
        ...

    CurrentOSThreadId: int

    @property
    def IsAlive(self) -> bool:
        ...

    @property
    def IsBackground(self) -> bool:
        ...

    @IsBackground.setter
    def IsBackground(self, value: bool):
        ...

    @property
    def IsThreadPoolThread(self) -> bool:
        ...

    @IsThreadPoolThread.setter
    def IsThreadPoolThread(self, value: bool):
        ...

    @property
    def ManagedThreadId(self) -> int:
        ...

    OptimalMaxSpinWaitsPerSpinIteration: int

    @property
    def Priority(self) -> int:
        """This property contains the int value of a member of the System.Threading.ThreadPriority enum."""
        ...

    @Priority.setter
    def Priority(self, value: int):
        """This property contains the int value of a member of the System.Threading.ThreadPriority enum."""
        ...

    @property
    def ThreadState(self) -> int:
        """This property contains the int value of a member of the System.Threading.ThreadState enum."""
        ...

    IsThreadStartSupported: bool = False

    @typing.overload
    def __init__(self, start: System_Threading_ThreadStart) -> None:
        ...

    @typing.overload
    def __init__(self, start: System_Threading_ThreadStart, maxStackSize: int) -> None:
        ...

    @typing.overload
    def __init__(self, start: System_Threading_ParameterizedThreadStart) -> None:
        ...

    @typing.overload
    def __init__(self, start: System_Threading_ParameterizedThreadStart, maxStackSize: int) -> None:
        ...

    @typing.overload
    def Start(self, parameter: typing.Any) -> None:
        """
        Causes the operating system to change the state of the current instance to ThreadState.Running, and optionally supplies an object containing data to be used by the method the thread executes.
        
        :param parameter: An object that contains data to be used by the method the thread executes.
        """
        ...

    @typing.overload
    def UnsafeStart(self, parameter: typing.Any) -> None:
        """
        Causes the operating system to change the state of the current instance to ThreadState.Running, and optionally supplies an object containing data to be used by the method the thread executes.
        
        :param parameter: An object that contains data to be used by the method the thread executes.
        """
        ...

    @typing.overload
    def Start(self) -> None:
        """Causes the operating system to change the state of the current instance to ThreadState.Running."""
        ...

    @typing.overload
    def UnsafeStart(self) -> None:
        """Causes the operating system to change the state of the current instance to ThreadState.Running."""
        ...

    @typing.overload
    def ThreadNameChanged(self, value: str) -> None:
        ...

    @typing.overload
    def Abort(self) -> None:
        ...

    @typing.overload
    def Abort(self, stateInfo: typing.Any) -> None:
        ...

    @staticmethod
    def ResetAbort() -> None:
        ...

    def Suspend(self) -> None:
        ...

    def Resume(self) -> None:
        ...

    @staticmethod
    def BeginCriticalRegion() -> None:
        ...

    @staticmethod
    def EndCriticalRegion() -> None:
        ...

    @staticmethod
    def BeginThreadAffinity() -> None:
        ...

    @staticmethod
    def EndThreadAffinity() -> None:
        ...

    @staticmethod
    def AllocateDataSlot() -> System.LocalDataStoreSlot:
        ...

    @staticmethod
    def AllocateNamedDataSlot(name: str) -> System.LocalDataStoreSlot:
        ...

    @staticmethod
    def GetNamedDataSlot(name: str) -> System.LocalDataStoreSlot:
        ...

    @staticmethod
    def FreeNamedDataSlot(name: str) -> None:
        ...

    @staticmethod
    def GetData(slot: System.LocalDataStoreSlot) -> System.Object:
        ...

    @staticmethod
    def SetData(slot: System.LocalDataStoreSlot, data: typing.Any) -> None:
        ...

    def SetApartmentState(self, state: System.Threading.ApartmentState) -> None:
        ...

    def TrySetApartmentState(self, state: System.Threading.ApartmentState) -> bool:
        ...

    def GetCompressedStack(self) -> System.Threading.CompressedStack:
        ...

    def SetCompressedStack(self, stack: System.Threading.CompressedStack) -> None:
        ...

    @staticmethod
    def GetDomain() -> System.AppDomain:
        ...

    @staticmethod
    def GetDomainID() -> int:
        ...

    def GetHashCode(self) -> int:
        ...

    @typing.overload
    def Join(self) -> None:
        ...

    @typing.overload
    def Join(self, timeout: datetime.timedelta) -> bool:
        ...

    @staticmethod
    def MemoryBarrier() -> None:
        ...

    @staticmethod
    @typing.overload
    def Sleep(timeout: datetime.timedelta) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: float) -> float:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: System.IntPtr) -> System.IntPtr:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: typing.Any) -> System.Object:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: float) -> float:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def VolatileRead(address: System.UIntPtr) -> System.UIntPtr:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: float, value: float) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: System.IntPtr, value: System.IntPtr) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: typing.Any, value: typing.Any) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: float, value: float) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: int, value: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def VolatileWrite(address: System.UIntPtr, value: System.UIntPtr) -> None:
        ...

    def GetApartmentState(self) -> int:
        """:returns: This method returns the int value of a member of the System.Threading.ApartmentState enum."""
        ...

    def DisableComObjectEagerCleanup(self) -> None:
        ...

    @staticmethod
    def GetCurrentProcessorId() -> int:
        ...

    def Interrupt(self) -> None:
        ...

    @typing.overload
    def Join(self, millisecondsTimeout: int) -> bool:
        ...

    @staticmethod
    def SpinWait(iterations: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def Sleep(millisecondsTimeout: int) -> None:
        ...

    @typing.overload
    def ThreadNameChanged(self, value: str) -> None:
        ...

    @staticmethod
    def Yield() -> bool:
        ...

    @typing.overload
    def Start(self) -> None:
        ...

    @typing.overload
    def Start(self, parameter: typing.Any) -> None:
        ...

    @typing.overload
    def UnsafeStart(self) -> None:
        ...

    @typing.overload
    def UnsafeStart(self, parameter: typing.Any) -> None:
        ...


class CancellationTokenSource(System.Object, System.IDisposable):
    """Signals to a CancellationToken that it should be canceled."""

    s_canceledSource: System.Threading.CancellationTokenSource = ...
    """A CancellationTokenSource that's already canceled."""

    s_neverCanceledSource: System.Threading.CancellationTokenSource = ...
    """A CancellationTokenSource that's never canceled.  This isn't enforced programmatically, only by usage.  Do not cancel!"""

    @property
    def IsCancellationRequested(self) -> bool:
        """Gets whether cancellation has been requested for this CancellationTokenSource."""
        ...

    @property
    def IsCancellationCompleted(self) -> bool:
        """A simple helper to determine whether cancellation has finished."""
        ...

    @property
    def Token(self) -> System.Threading.CancellationToken:
        """Gets the CancellationToken associated with this CancellationTokenSource."""
        ...

    @property
    def WaitHandle(self) -> System.Threading.WaitHandle:
        ...

    @typing.overload
    def __init__(self) -> None:
        """Initializes the CancellationTokenSource."""
        ...

    @typing.overload
    def __init__(self, delay: datetime.timedelta) -> None:
        """
        Constructs a CancellationTokenSource that will be canceled after a specified time span.
        
        :param delay: The time span to wait before canceling this CancellationTokenSource
        """
        ...

    @typing.overload
    def __init__(self, millisecondsDelay: int) -> None:
        """
        Constructs a CancellationTokenSource that will be canceled after a specified time span.
        
        :param millisecondsDelay: The time span to wait before canceling this CancellationTokenSource
        """
        ...

    @typing.overload
    def Cancel(self) -> None:
        """Communicates a request for cancellation."""
        ...

    @typing.overload
    def Cancel(self, throwOnFirstException: bool) -> None:
        """
        Communicates a request for cancellation.
        
        :param throwOnFirstException: Specifies whether exceptions should immediately propagate.
        """
        ...

    @typing.overload
    def CancelAfter(self, delay: datetime.timedelta) -> None:
        """
        Schedules a Cancel operation on this CancellationTokenSource.
        
        :param delay: The time span to wait before canceling this CancellationTokenSource.
        """
        ...

    @typing.overload
    def CancelAfter(self, millisecondsDelay: int) -> None:
        """
        Schedules a Cancel operation on this CancellationTokenSource.
        
        :param millisecondsDelay: The time span to wait before canceling this CancellationTokenSource.
        """
        ...

    @typing.overload
    def Dispose(self) -> None:
        """Releases the resources used by this CancellationTokenSource."""
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """
        Releases the unmanaged resources used by the CancellationTokenSource class and optionally releases the managed resources.
        
        This method is protected.
        
        :param disposing: true to release both managed and unmanaged resources; false to release only unmanaged resources.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateLinkedTokenSource(token1: System.Threading.CancellationToken, token2: System.Threading.CancellationToken) -> System.Threading.CancellationTokenSource:
        """
        Creates a CancellationTokenSource that will be in the canceled state
        when any of the source tokens are in the canceled state.
        
        :param token1: The first CancellationToken to observe.
        :param token2: The second CancellationToken to observe.
        :returns: A CancellationTokenSource that is linked to the source tokens.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateLinkedTokenSource(token: System.Threading.CancellationToken) -> System.Threading.CancellationTokenSource:
        """
        Creates a CancellationTokenSource that will be in the canceled state
        when the supplied token is in the canceled state.
        
        :param token: The CancellationToken to observe.
        :returns: A CancellationTokenSource that is linked to the source token.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateLinkedTokenSource(*tokens: System.Threading.CancellationToken) -> System.Threading.CancellationTokenSource:
        """
        Creates a CancellationTokenSource that will be in the canceled state
        when any of the source tokens are in the canceled state.
        
        :param tokens: The CancellationToken instances to observe.
        :returns: A CancellationTokenSource that is linked to the source tokens.
        """
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...


class CancellationTokenRegistration(System.IEquatable[System_Threading_CancellationTokenRegistration], System.IDisposable, System.IAsyncDisposable):
    """Represents a callback delegate that has been registered with a System.Threading.CancellationToken."""

    @property
    def Token(self) -> System.Threading.CancellationToken:
        """Gets the CancellationToken with which this registration is associated."""
        ...

    def Dispose(self) -> None:
        """
        Disposes of the registration and unregisters the target callback from the associated
        System.Threading.CancellationToken.
        If the target callback is currently executing, this method will wait until it completes, except
        in the degenerate cases where a callback method unregisters itself.
        """
        ...

    def DisposeAsync(self) -> System.Threading.Tasks.ValueTask:
        """
        Disposes of the registration and unregisters the target callback from the associated
        System.Threading.CancellationToken.
        The returned ValueTask will complete once the associated callback
        is unregistered without having executed or once it's finished executing, except
        in the degenerate case where the callback itself is unregistering itself.
        """
        ...

    def Unregister(self) -> bool:
        """
        Disposes of the registration and unregisters the target callback from the associated
        System.Threading.CancellationToken.
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Determines whether the current System.Threading.CancellationTokenRegistration instance is equal to the
        specified object.
        
        :param obj: The other object to which to compare this instance.
        :returns: True, if both this and  are equal. False, otherwise. Two System.Threading.CancellationTokenRegistration instances are equal if they both refer to the output of a single call to the same Register method of a System.Threading.CancellationToken.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Threading.CancellationTokenRegistration) -> bool:
        """
        Determines whether the current System.Threading.CancellationToken instance is equal to the
        specified object.
        
        :param other: The other System.Threading.CancellationTokenRegistration to which to compare this instance.
        :returns: True, if both this and  are equal. False, otherwise. Two System.Threading.CancellationTokenRegistration instances are equal if they both refer to the output of a single call to the same Register method of a System.Threading.CancellationToken.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Serves as a hash function for a System.Threading.CancellationTokenRegistration.
        
        :returns: A hash code for the current System.Threading.CancellationTokenRegistration instance.
        """
        ...


class RegisteredWaitHandle(System.MarshalByRefObject):
    """An object representing the registration of a WaitHandle via ThreadPool.RegisterWaitForSingleObject."""

    @property
    def Callback(self) -> System.Threading._ThreadPoolWaitOrTimerCallback:
        """The callback to execute when the wait on Handle either times out or completes."""
        ...

    @property
    def Handle(self) -> Microsoft.Win32.SafeHandles.SafeWaitHandle:
        """The SafeWaitHandle that was registered."""
        ...

    @property
    def TimeoutTimeMs(self) -> int:
        """The time this handle times out at in ms."""
        ...

    @TimeoutTimeMs.setter
    def TimeoutTimeMs(self, value: int):
        """The time this handle times out at in ms."""
        ...

    @property
    def TimeoutDurationMs(self) -> int:
        ...

    @property
    def IsInfiniteTimeout(self) -> bool:
        ...

    @property
    def Repeating(self) -> bool:
        """Whether or not the wait is a repeating wait."""
        ...

    @property
    def IsBlocking(self) -> bool:
        ...

    @property
    def WaitThread(self) -> System.Threading.PortableThreadPool.WaitThread:
        """The PortableThreadPool.WaitThread this RegisteredWaitHandle was registered on."""
        ...

    @WaitThread.setter
    def WaitThread(self, value: System.Threading.PortableThreadPool.WaitThread):
        """The PortableThreadPool.WaitThread this RegisteredWaitHandle was registered on."""
        ...

    @typing.overload
    def Unregister(self, waitObject: System.Threading.WaitHandle) -> bool:
        ...

    @typing.overload
    def Unregister(self, waitObject: System.Threading.WaitHandle) -> bool:
        ...


class ThreadPool(System.Object):
    """This class has no documentation."""

    EnableDispatchAutoreleasePool: bool

    WorkerThreadName: str = ".NET ThreadPool Worker"

    s_workQueue: System.Threading.ThreadPoolWorkQueue = ...

    s_invokeAsyncStateMachineBox: typing.Callable[[System.Object], None] = ...
    """Shim used to invoke IAsyncStateMachineBox.MoveNext of the supplied IAsyncStateMachineBox."""

    box: System.Runtime.CompilerServices.IAsyncStateMachineBox

    SupportsTimeSensitiveWorkItems: bool = True

    EnableWorkerTracking: bool = ...

    ThreadCount: int
    """Gets the number of thread pool threads that currently exist."""

    CompletedWorkItemCount: int
    """Gets the number of work items that have been processed by the thread pool so far."""

    SupportsTimeSensitiveWorkItems: bool = False

    EnableWorkerTracking: bool = False

    @staticmethod
    @typing.overload
    def SetMaxThreads(workerThreads: int, completionPortThreads: int) -> bool:
        ...

    @staticmethod
    @typing.overload
    def GetMaxThreads(workerThreads: int, completionPortThreads: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def SetMinThreads(workerThreads: int, completionPortThreads: int) -> bool:
        ...

    @staticmethod
    @typing.overload
    def GetMinThreads(workerThreads: int, completionPortThreads: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def GetAvailableThreads(workerThreads: int, completionPortThreads: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def SetMaxThreads(workerThreads: int, completionPortThreads: int) -> bool:
        ...

    @staticmethod
    @typing.overload
    def GetMaxThreads(workerThreads: int, completionPortThreads: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def SetMinThreads(workerThreads: int, completionPortThreads: int) -> bool:
        ...

    @staticmethod
    @typing.overload
    def GetMinThreads(workerThreads: int, completionPortThreads: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def GetAvailableThreads(workerThreads: int, completionPortThreads: int) -> None:
        ...

    @staticmethod
    def UnsafeQueueNativeOverlapped(overlapped: typing.Any) -> bool:
        ...

    @staticmethod
    @typing.overload
    def BindHandle(osHandle: System.IntPtr) -> bool:
        ...

    @staticmethod
    @typing.overload
    def BindHandle(osHandle: System.Runtime.InteropServices.SafeHandle) -> bool:
        ...


class SemaphoreSlim(System.Object, System.IDisposable):
    """Limits the number of threads that can access a resource or pool of resources concurrently."""

    @property
    def CurrentCount(self) -> int:
        ...

    @property
    def AvailableWaitHandle(self) -> System.Threading.WaitHandle:
        """Returns a System.Threading.WaitHandle that can be used to wait on the semaphore."""
        ...

    @typing.overload
    def __init__(self, initialCount: int) -> None:
        ...

    @typing.overload
    def __init__(self, initialCount: int, maxCount: int) -> None:
        """
        Initializes a new instance of the SemaphoreSlim class, specifying
        the initial and maximum number of requests that can be granted concurrently.
        
        :param initialCount: The initial number of requests for the semaphore that can be granted concurrently.
        :param maxCount: The maximum number of requests for the semaphore that can be granted concurrently.
        """
        ...

    @typing.overload
    def Wait(self) -> None:
        ...

    @typing.overload
    def Wait(self, cancellationToken: System.Threading.CancellationToken) -> None:
        """
        Blocks the current thread until it can enter the SemaphoreSlim, while observing a
        System.Threading.CancellationToken.
        
        :param cancellationToken: The System.Threading.CancellationToken token to observe.
        """
        ...

    @typing.overload
    def Wait(self, timeout: datetime.timedelta) -> bool:
        """
        Blocks the current thread until it can enter the SemaphoreSlim, using a System.TimeSpan to measure the time interval.
        
        :param timeout: A System.TimeSpan that represents the number of milliseconds to wait, or a System.TimeSpan that represents -1 milliseconds to wait indefinitely.
        :returns: true if the current thread successfully entered the SemaphoreSlim; otherwise, false.
        """
        ...

    @typing.overload
    def Wait(self, timeout: datetime.timedelta, cancellationToken: System.Threading.CancellationToken) -> bool:
        """
        Blocks the current thread until it can enter the SemaphoreSlim, using a System.TimeSpan to measure the time interval, while observing a System.Threading.CancellationToken.
        
        :param timeout: A System.TimeSpan that represents the number of milliseconds to wait, or a System.TimeSpan that represents -1 milliseconds to wait indefinitely.
        :param cancellationToken: The System.Threading.CancellationToken to observe.
        :returns: true if the current thread successfully entered the SemaphoreSlim; otherwise, false.
        """
        ...

    @typing.overload
    def Wait(self, millisecondsTimeout: int) -> bool:
        """
        Blocks the current thread until it can enter the SemaphoreSlim, using a 32-bit
        signed integer to measure the time interval.
        
        :param millisecondsTimeout: The number of milliseconds to wait, or Timeout.Infinite(-1) to wait indefinitely.
        :returns: true if the current thread successfully entered the SemaphoreSlim; otherwise, false.
        """
        ...

    @typing.overload
    def Wait(self, millisecondsTimeout: int, cancellationToken: System.Threading.CancellationToken) -> bool:
        """
        Blocks the current thread until it can enter the SemaphoreSlim,
        using a 32-bit signed integer to measure the time interval,
        while observing a System.Threading.CancellationToken.
        
        :param millisecondsTimeout: The number of milliseconds to wait, or Timeout.Infinite(-1) to wait indefinitely.
        :param cancellationToken: The System.Threading.CancellationToken to observe.
        :returns: true if the current thread successfully entered the SemaphoreSlim; otherwise, false.
        """
        ...

    @typing.overload
    def WaitAsync(self) -> System.Threading.Tasks.Task:
        """
        Asynchronously waits to enter the SemaphoreSlim.
        
        :returns: A task that will complete when the semaphore has been entered.
        """
        ...

    @typing.overload
    def WaitAsync(self, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        """
        Asynchronously waits to enter the SemaphoreSlim, while observing a
        System.Threading.CancellationToken.
        
        :param cancellationToken: The System.Threading.CancellationToken token to observe.
        :returns: A task that will complete when the semaphore has been entered.
        """
        ...

    @typing.overload
    def WaitAsync(self, millisecondsTimeout: int) -> System.Threading.Tasks.Task[bool]:
        """
        Asynchronously waits to enter the SemaphoreSlim,
        using a 32-bit signed integer to measure the time interval.
        
        :param millisecondsTimeout: The number of milliseconds to wait, or Timeout.Infinite(-1) to wait indefinitely.
        :returns: A task that will complete with a result of true if the current thread successfully entered the SemaphoreSlim, otherwise with a result of false.
        """
        ...

    @typing.overload
    def WaitAsync(self, timeout: datetime.timedelta) -> System.Threading.Tasks.Task[bool]:
        """
        Asynchronously waits to enter the SemaphoreSlim, using a System.TimeSpan to measure the time interval, while observing a
        System.Threading.CancellationToken.
        
        :param timeout: A System.TimeSpan that represents the number of milliseconds to wait, or a System.TimeSpan that represents -1 milliseconds to wait indefinitely.
        :returns: A task that will complete with a result of true if the current thread successfully entered the SemaphoreSlim, otherwise with a result of false.
        """
        ...

    @typing.overload
    def WaitAsync(self, timeout: datetime.timedelta, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[bool]:
        """
        Asynchronously waits to enter the SemaphoreSlim, using a System.TimeSpan to measure the time interval.
        
        :param timeout: A System.TimeSpan that represents the number of milliseconds to wait, or a System.TimeSpan that represents -1 milliseconds to wait indefinitely.
        :param cancellationToken: The System.Threading.CancellationToken token to observe.
        :returns: A task that will complete with a result of true if the current thread successfully entered the SemaphoreSlim, otherwise with a result of false.
        """
        ...

    @typing.overload
    def WaitAsync(self, millisecondsTimeout: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[bool]:
        """
        Asynchronously waits to enter the SemaphoreSlim,
        using a 32-bit signed integer to measure the time interval,
        while observing a System.Threading.CancellationToken.
        
        :param millisecondsTimeout: The number of milliseconds to wait, or Timeout.Infinite(-1) to wait indefinitely.
        :param cancellationToken: The System.Threading.CancellationToken to observe.
        :returns: A task that will complete with a result of true if the current thread successfully entered the SemaphoreSlim, otherwise with a result of false.
        """
        ...

    @typing.overload
    def Release(self) -> int:
        """
        Exits the SemaphoreSlim once.
        
        :returns: The previous count of the SemaphoreSlim.
        """
        ...

    @typing.overload
    def Release(self, releaseCount: int) -> int:
        """
        Exits the SemaphoreSlim a specified number of times.
        
        :param releaseCount: The number of times to exit the semaphore.
        :returns: The previous count of the SemaphoreSlim.
        """
        ...

    @typing.overload
    def Dispose(self) -> None:
        """Releases all resources used by the current instance of SemaphoreSlim."""
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """
        When overridden in a derived class, releases the unmanaged resources used by the
        System.Threading.ManualResetEventSlim, and optionally releases the managed resources.
        
        This method is protected.
        
        :param disposing: true to release both managed and unmanaged resources; false to release only unmanaged resources.
        """
        ...


class ManualResetEvent(System.Threading.EventWaitHandle):
    """This class has no documentation."""

    def __init__(self, initialState: bool) -> None:
        ...


class IThreadPoolWorkItem(metaclass=abc.ABCMeta):
    """Represents a work item that can be executed by the ThreadPool."""

    def Execute(self) -> None:
        ...


class AbandonedMutexException(System.SystemException):
    """This class has no documentation."""

    @property
    def Mutex(self) -> System.Threading.Mutex:
        ...

    @property
    def MutexIndex(self) -> int:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...

    @typing.overload
    def __init__(self, location: int, handle: System.Threading.WaitHandle) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, location: int, handle: System.Threading.WaitHandle) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, inner: System.Exception, location: int, handle: System.Threading.WaitHandle) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class SynchronizationLockException(System.SystemException):
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

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class SpinLock:
    """
    Provides a mutual exclusion lock primitive where a thread trying to acquire the lock waits in a loop
    repeatedly checking until the lock becomes available.
    """

    @property
    def IsHeld(self) -> bool:
        """Gets whether the lock is currently held by any thread."""
        ...

    @property
    def IsHeldByCurrentThread(self) -> bool:
        """Gets whether the lock is currently held by any thread."""
        ...

    @property
    def IsThreadOwnerTrackingEnabled(self) -> bool:
        """Gets whether thread ownership tracking is enabled for this instance."""
        ...

    def __init__(self, enableThreadOwnerTracking: bool) -> None:
        """
        Initializes a new instance of the System.Threading.SpinLock
        structure with the option to track thread IDs to improve debugging.
        
        :param enableThreadOwnerTracking: Whether to capture and use thread IDs for debugging purposes.
        """
        ...

    def Enter(self, lockTaken: bool) -> None:
        """
        Initializes a new instance of the System.Threading.SpinLock
        structure with the option to track thread IDs to improve debugging.
        
        :param lockTaken: True if the lock is acquired; otherwise, false.  must be initialized to false prior to calling this method.
        """
        ...

    @typing.overload
    def TryEnter(self, lockTaken: bool) -> None:
        """
        Attempts to acquire the lock in a reliable manner, such that even if an exception occurs within
        the method call,  can be examined reliably to determine whether the
        lock was acquired.
        
        :param lockTaken: True if the lock is acquired; otherwise, false.  must be initialized to false prior to calling this method.
        """
        ...

    @typing.overload
    def TryEnter(self, timeout: datetime.timedelta, lockTaken: bool) -> None:
        """
        Attempts to acquire the lock in a reliable manner, such that even if an exception occurs within
        the method call,  can be examined reliably to determine whether the
        lock was acquired.
        
        :param timeout: A System.TimeSpan that represents the number of milliseconds to wait, or a System.TimeSpan that represents -1 milliseconds to wait indefinitely.
        :param lockTaken: True if the lock is acquired; otherwise, false.  must be initialized to false prior to calling this method.
        """
        ...

    @typing.overload
    def TryEnter(self, millisecondsTimeout: int, lockTaken: bool) -> None:
        """
        Attempts to acquire the lock in a reliable manner, such that even if an exception occurs within
        the method call,  can be examined reliably to determine whether the
        lock was acquired.
        
        :param millisecondsTimeout: The number of milliseconds to wait, or System.Threading.Timeout.Infinite (-1) to wait indefinitely.
        :param lockTaken: True if the lock is acquired; otherwise, false.  must be initialized to false prior to calling this method.
        """
        ...

    @typing.overload
    def Exit(self) -> None:
        """Releases the lock."""
        ...

    @typing.overload
    def Exit(self, useMemoryBarrier: bool) -> None:
        """
        Releases the lock.
        
        :param useMemoryBarrier: A Boolean value that indicates whether a memory fence should be issued in order to immediately publish the exit operation to other threads.
        """
        ...


class LazyThreadSafetyMode(System.Enum):
    """Specifies how a System.Lazy{T} instance should synchronize access among multiple threads."""

    # Cannot convert to Python: None = 0
    """
    This mode makes no guarantees around the thread-safety of the System.Lazy{T} instance.  If used from multiple threads, the behavior of the System.Lazy{T} is undefined.
    This mode should be used when a System.Lazy{T} is guaranteed to never be initialized from more than one thread simultaneously and high performance is crucial.
    If valueFactory throws an exception when the System.Lazy{T} is initialized, the exception will be cached and returned on subsequent accesses to Value. Also, if valueFactory recursively
    accesses Value on this System.Lazy{T} instance, a System.InvalidOperationException will be thrown.
    """

    PublicationOnly = 1
    """
    When multiple threads attempt to simultaneously initialize a System.Lazy{T} instance, this mode allows each thread to execute the
    valueFactory but only the first thread to complete initialization will be allowed to set the final value of the  System.Lazy{T}.
    Once initialized successfully, any future calls to Value will return the cached result.  If valueFactory throws an exception on any thread, that exception will be
    propagated out of Value. If any thread executes valueFactory without throwing an exception and, therefore, successfully sets the value, that value will be returned on
    subsequent accesses to Value from any thread.  If no thread succeeds in setting the value, IsValueCreated will remain false and subsequent accesses to Value will result in
    the valueFactory delegate re-executing.  Also, if valueFactory recursively accesses Value on this  System.Lazy{T} instance, an exception will NOT be thrown.
    """

    ExecutionAndPublication = 2
    """
    This mode uses locks to ensure that only a single thread can initialize a System.Lazy{T} instance in a thread-safe manner.  In general,
    taken if this mode is used in conjunction with a System.Lazy{T} valueFactory delegate that uses locks internally, a deadlock can occur if not
    handled carefully.  If valueFactory throws an exception when theSystem.Lazy{T} is initialized, the exception will be cached and returned on
    subsequent accesses to Value. Also, if valueFactory recursively accesses Value on this System.Lazy{T} instance, a  System.InvalidOperationException will be thrown.
    """


class ThreadLocal(typing.Generic[System_Threading_ThreadLocal_T], System.Object, System.IDisposable):
    """Provides thread-local storage of data."""

    @property
    def Value(self) -> System_Threading_ThreadLocal_T:
        """Gets or sets the value of this instance for the current thread."""
        ...

    @Value.setter
    def Value(self, value: System_Threading_ThreadLocal_T):
        """Gets or sets the value of this instance for the current thread."""
        ...

    @property
    def Values(self) -> System.Collections.Generic.IList[System_Threading_ThreadLocal_T]:
        """Gets a list for all of the values currently stored by all of the threads that have accessed this instance."""
        ...

    @property
    def ValuesAsEnumerable(self) -> System.Collections.Generic.IEnumerable[System_Threading_ThreadLocal_T]:
        ...

    @property
    def IsValueCreated(self) -> bool:
        """Gets whether Value is initialized on the current thread."""
        ...

    @property
    def ValueForDebugDisplay(self) -> System_Threading_ThreadLocal_T:
        """
        Gets the value of the ThreadLocal<T> for debugging display purposes. It takes care of getting
        the value for the current thread in the ThreadLocal mode.
        """
        ...

    @property
    def ValuesForDebugDisplay(self) -> System.Collections.Generic.List[System_Threading_ThreadLocal_T]:
        """Gets the values of all threads that accessed the ThreadLocal<T>."""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Initializes the System.Threading.ThreadLocal{T} instance."""
        ...

    @typing.overload
    def __init__(self, trackAllValues: bool) -> None:
        """
        Initializes the System.Threading.ThreadLocal{T} instance.
        
        :param trackAllValues: Whether to track all values set on the instance and expose them through the Values property.
        """
        ...

    @typing.overload
    def __init__(self, valueFactory: typing.Callable[[], System_Threading_ThreadLocal_T]) -> None:
        """
        Initializes the System.Threading.ThreadLocal{T} instance with the
        specified  function.
        
        :param valueFactory: The System.Func{T} invoked to produce a lazily-initialized value when an attempt is made to retrieve Value without it having been previously initialized.
        """
        ...

    @typing.overload
    def __init__(self, valueFactory: typing.Callable[[], System_Threading_ThreadLocal_T], trackAllValues: bool) -> None:
        """
        Initializes the System.Threading.ThreadLocal{T} instance with the
        specified  function.
        
        :param valueFactory: The System.Func{T} invoked to produce a lazily-initialized value when an attempt is made to retrieve Value without it having been previously initialized.
        :param trackAllValues: Whether to track all values set on the instance and expose them via the Values property.
        """
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """
        Releases the resources used by this System.Threading.ThreadLocal{T} instance.
        
        This method is protected.
        
        :param disposing: A Boolean value that indicates whether this method is being called due to a call to Dispose().
        """
        ...

    def ToString(self) -> str:
        ...


class ThreadPoolBoundHandle(System.Object, System.IDisposable):
    """This class has no documentation."""

    @property
    def Handle(self) -> System.Runtime.InteropServices.SafeHandle:
        ...

    @staticmethod
    def BindHandle(handle: System.Runtime.InteropServices.SafeHandle) -> System.Threading.ThreadPoolBoundHandle:
        ...

    @typing.overload
    def AllocateNativeOverlapped(self, callback: System_Threading_IOCompletionCallback, state: typing.Any, pinData: typing.Any) -> typing.Any:
        ...

    @typing.overload
    def AllocateNativeOverlapped(self, preAllocated: System.Threading.PreAllocatedOverlapped) -> typing.Any:
        ...

    def FreeNativeOverlapped(self, overlapped: typing.Any) -> None:
        ...

    @staticmethod
    def GetNativeOverlappedState(overlapped: typing.Any) -> System.Object:
        ...

    def Dispose(self) -> None:
        ...


class ThreadPriority(System.Enum):
    """This class has no documentation."""

    Lowest = 0

    BelowNormal = 1

    Normal = 2

    AboveNormal = 3

    Highest = 4


class ThreadState(System.Enum):
    """This class has no documentation."""

    Running = 0

    StopRequested = 1

    SuspendRequested = 2

    Background = 4

    Unstarted = 8

    Stopped = 16

    WaitSleepJoin = 32

    Suspended = 64

    AbortRequested = 128

    Aborted = 256


class Monitor(System.Object):
    """This class has no documentation."""

    LockContentionCount: int

    @staticmethod
    @typing.overload
    def TryEnter(obj: typing.Any, timeout: datetime.timedelta) -> bool:
        ...

    @staticmethod
    @typing.overload
    def TryEnter(obj: typing.Any, timeout: datetime.timedelta, lockTaken: bool) -> None:
        ...

    @staticmethod
    @typing.overload
    def Wait(obj: typing.Any, timeout: datetime.timedelta) -> bool:
        ...

    @staticmethod
    @typing.overload
    def Wait(obj: typing.Any) -> bool:
        ...

    @staticmethod
    @typing.overload
    def Wait(obj: typing.Any, millisecondsTimeout: int, exitContext: bool) -> bool:
        ...

    @staticmethod
    @typing.overload
    def Wait(obj: typing.Any, timeout: datetime.timedelta, exitContext: bool) -> bool:
        ...

    @staticmethod
    @typing.overload
    def Enter(obj: typing.Any) -> None:
        ...

    @staticmethod
    @typing.overload
    def Enter(obj: typing.Any, lockTaken: bool) -> None:
        ...

    @staticmethod
    def Exit(obj: typing.Any) -> None:
        ...

    @staticmethod
    @typing.overload
    def TryEnter(obj: typing.Any) -> bool:
        ...

    @staticmethod
    @typing.overload
    def TryEnter(obj: typing.Any, lockTaken: bool) -> None:
        ...

    @staticmethod
    @typing.overload
    def TryEnter(obj: typing.Any, millisecondsTimeout: int) -> bool:
        ...

    @staticmethod
    @typing.overload
    def TryEnter(obj: typing.Any, millisecondsTimeout: int, lockTaken: bool) -> None:
        ...

    @staticmethod
    def IsEntered(obj: typing.Any) -> bool:
        ...

    @staticmethod
    @typing.overload
    def Wait(obj: typing.Any, millisecondsTimeout: int) -> bool:
        ...

    @staticmethod
    def Pulse(obj: typing.Any) -> None:
        ...

    @staticmethod
    def PulseAll(obj: typing.Any) -> None:
        ...


class ThreadAbortException(System.SystemException):
    """This class has no documentation."""

    @property
    def ExceptionState(self) -> System.Object:
        ...


class NativeOverlapped:
    """This class has no documentation."""

    @property
    def InternalLow(self) -> System.IntPtr:
        ...

    @InternalLow.setter
    def InternalLow(self, value: System.IntPtr):
        ...

    @property
    def InternalHigh(self) -> System.IntPtr:
        ...

    @InternalHigh.setter
    def InternalHigh(self, value: System.IntPtr):
        ...

    @property
    def OffsetLow(self) -> int:
        ...

    @OffsetLow.setter
    def OffsetLow(self, value: int):
        ...

    @property
    def OffsetHigh(self) -> int:
        ...

    @OffsetHigh.setter
    def OffsetHigh(self, value: int):
        ...

    @property
    def EventHandle(self) -> System.IntPtr:
        ...

    @EventHandle.setter
    def EventHandle(self, value: System.IntPtr):
        ...


class ThreadStartException(System.SystemException):
    """This class has no documentation."""


class AutoResetEvent(System.Threading.EventWaitHandle):
    """This class has no documentation."""

    def __init__(self, initialState: bool) -> None:
        ...


class WaitHandleExtensions(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetSafeWaitHandle(waitHandle: System.Threading.WaitHandle) -> Microsoft.Win32.SafeHandles.SafeWaitHandle:
        """
        Gets the native operating system handle.
        
        :param waitHandle: The System.Threading.WaitHandle to operate on.
        :returns: A System.Runtime.InteropServices.SafeHandle representing the native operating system handle.
        """
        ...

    @staticmethod
    def SetSafeWaitHandle(waitHandle: System.Threading.WaitHandle, value: Microsoft.Win32.SafeHandles.SafeWaitHandle) -> None:
        """
        Sets the native operating system handle
        
        :param waitHandle: The System.Threading.WaitHandle to operate on.
        :param value: A System.Runtime.InteropServices.SafeHandle representing the native operating system handle.
        """
        ...


class SpinWait:
    """This class has no documentation."""

    YieldThreshold: int = 10

    DefaultSleep1Threshold: int = 20

    SpinCountforSpinBeforeWait: int = ...
    """
    A suggested number of spin iterations before doing a proper wait, such as waiting on an event that becomes signaled
    when the resource becomes available.
    """

    @property
    def Count(self) -> int:
        """Gets the number of times SpinOnce() has been called on this instance."""
        ...

    @Count.setter
    def Count(self, value: int):
        """Gets the number of times SpinOnce() has been called on this instance."""
        ...

    @property
    def NextSpinWillYield(self) -> bool:
        """
        Gets whether the next call to SpinOnce() will yield the processor, triggering a
        forced context switch.
        """
        ...

    @typing.overload
    def SpinOnce(self) -> None:
        """Performs a single spin."""
        ...

    @typing.overload
    def SpinOnce(self, sleep1Threshold: int) -> None:
        """
        Performs a single spin.
        
        :param sleep1Threshold: A minimum spin count after which Thread.Sleep(1) may be used. A value of -1 may be used to disable the use of Thread.Sleep(1).
        """
        ...

    def Reset(self) -> None:
        """Resets the spin counter."""
        ...

    @staticmethod
    @typing.overload
    def SpinUntil(condition: typing.Callable[[], bool]) -> None:
        ...

    @staticmethod
    @typing.overload
    def SpinUntil(condition: typing.Callable[[], bool], timeout: datetime.timedelta) -> bool:
        """
        Spins until the specified condition is satisfied or until the specified timeout is expired.
        
        :param condition: A delegate to be executed over and over until it returns true.
        :param timeout: A TimeSpan that represents the number of milliseconds to wait, or a TimeSpan that represents -1 milliseconds to wait indefinitely.
        :returns: True if the condition is satisfied within the timeout; otherwise, false.
        """
        ...

    @staticmethod
    @typing.overload
    def SpinUntil(condition: typing.Callable[[], bool], millisecondsTimeout: int) -> bool:
        """
        Spins until the specified condition is satisfied or until the specified timeout is expired.
        
        :param condition: A delegate to be executed over and over until it returns true.
        :param millisecondsTimeout: The number of milliseconds to wait, or System.Threading.Timeout.Infinite (-1) to wait indefinitely.
        :returns: True if the condition is satisfied within the timeout; otherwise, false.
        """
        ...


class AsyncLocalValueChangedArgs(typing.Generic[System_Threading_AsyncLocalValueChangedArgs_T]):
    """This class has no documentation."""

    @property
    def PreviousValue(self) -> System_Threading_AsyncLocalValueChangedArgs_T:
        ...

    @property
    def CurrentValue(self) -> System_Threading_AsyncLocalValueChangedArgs_T:
        ...

    @property
    def ThreadContextChanged(self) -> bool:
        ...


class AsyncLocal(typing.Generic[System_Threading_AsyncLocal_T], System.Object, System.Threading.IAsyncLocal):
    """This class has no documentation."""

    @property
    def Value(self) -> System_Threading_AsyncLocal_T:
        ...

    @Value.setter
    def Value(self, value: System_Threading_AsyncLocal_T):
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, valueChangedHandler: typing.Callable[[System.Threading.AsyncLocalValueChangedArgs[System_Threading_AsyncLocal_T]], None]) -> None:
        ...

    def OnValueChanged(self, previousValueObj: typing.Any, currentValueObj: typing.Any, contextChanged: bool) -> None:
        ...


