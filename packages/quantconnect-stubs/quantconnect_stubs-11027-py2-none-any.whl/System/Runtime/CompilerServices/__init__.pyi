import abc
import typing

import System
import System.Collections
import System.Collections.Generic
import System.Diagnostics.Contracts
import System.Runtime.CompilerServices
import System.Runtime.Serialization
import System.Threading
import System.Threading.Tasks

System_Runtime_CompilerServices_ConditionalWeakTable_CreateValueCallback = typing.Any
System_EventHandler = typing.Any
IStateMachineBoxAwareAwaiter = typing.Any
ValueTaskAwaiter = typing.Any
typing_Any = typing.Any
ValueTaskAwaiter_TResult = typing.Any
System_Runtime_CompilerServices_RuntimeHelpers_TryCode = typing.Any
System_Runtime_CompilerServices_RuntimeHelpers_CleanupCode = typing.Any

System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_ConditionalWeakTable_TKey = typing.TypeVar("System_Runtime_CompilerServices_ConditionalWeakTable_TKey")
System_Runtime_CompilerServices_ConditionalWeakTable_TValue = typing.TypeVar("System_Runtime_CompilerServices_ConditionalWeakTable_TValue")
System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T = typing.TypeVar("System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult")
System_Runtime_CompilerServices_TaskAwaiter_TResult = typing.TypeVar("System_Runtime_CompilerServices_TaskAwaiter_TResult")
System_Runtime_CompilerServices_ConfiguredTaskAwaitable_TResult = typing.TypeVar("System_Runtime_CompilerServices_ConfiguredTaskAwaitable_TResult")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T = typing.TypeVar("System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T")
System_Runtime_CompilerServices_StrongBox_T = typing.TypeVar("System_Runtime_CompilerServices_StrongBox_T")
System_Runtime_CompilerServices_ConfiguredValueTaskAwaitable_TResult = typing.TypeVar("System_Runtime_CompilerServices_ConfiguredValueTaskAwaitable_TResult")


class LoadHint(System.Enum):
    """This class has no documentation."""

    Default = ...

    Always = ...

    Sometimes = ...


class DefaultDependencyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def LoadHint(self) -> int:
        """This property contains the int value of a member of the System.Runtime.CompilerServices.LoadHint enum."""
        ...

    def __init__(self, loadHintArgument: System.Runtime.CompilerServices.LoadHint) -> None:
        ...


class IAsyncStateMachine(metaclass=abc.ABCMeta):
    """
    Represents state machines generated for asynchronous methods.
    This type is intended for compiler use only.
    """

    def MoveNext(self) -> None:
        """Moves the state machine to its next state."""
        ...

    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Configures the state machine with a heap-allocated replica.
        
        :param stateMachine: The heap-allocated replica.
        """
        ...


class AsyncVoidMethodBuilder:
    """
    Provides a builder for asynchronous methods that return void.
    This type is intended for compiler use only.
    """

    @property
    def ObjectIdForDebugger(self) -> System.Object:
        """Gets an object that may be used to uniquely identify this builder to the debugger."""
        ...

    @staticmethod
    def Create() -> System.Runtime.CompilerServices.AsyncVoidMethodBuilder:
        """
        Initializes a new AsyncVoidMethodBuilder.
        
        :returns: The initialized AsyncVoidMethodBuilder.
        """
        ...

    def Start(self, stateMachine: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine) -> None:
        """
        Initiates the builder's execution with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...

    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the state machine it represents.
        
        :param stateMachine: The heap-allocated state machine object.
        """
        ...

    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    def SetResult(self) -> None:
        """Completes the method builder successfully."""
        ...

    def SetException(self, exception: System.Exception) -> None:
        """
        Faults the method builder with an exception.
        
        :param exception: The exception that is the cause of this fault.
        """
        ...


class RuntimeWrappedException(System.Exception):
    """Exception used to wrap all non-CLS compliant exceptions."""

    @property
    def WrappedException(self) -> System.Object:
        ...

    def __init__(self, thrownObject: typing.Any) -> None:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...


class ConditionalWeakTable(typing.Generic[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_TValue], System.Object, System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_TValue]], typing.Iterable[System.Collections.Generic.KeyValuePair[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_TValue]]):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...

    def TryGetValue(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: System_Runtime_CompilerServices_ConditionalWeakTable_TValue) -> bool:
        """
        Gets the value of the specified key.
        
        :param key: key of the value to find. Cannot be null.
        :param value: If the key is found, contains the value associated with the key upon method return. If the key is not found, contains default(TValue).
        :returns: Returns "true" if key was found, "false" otherwise.
        """
        ...

    def Add(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: System_Runtime_CompilerServices_ConditionalWeakTable_TValue) -> None:
        """
        Adds a key to the table.
        
        :param key: key to add. May not be null.
        :param value: value to associate with key.
        """
        ...

    def AddOrUpdate(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: System_Runtime_CompilerServices_ConditionalWeakTable_TValue) -> None:
        """
        Adds the key and value if the key doesn't exist, or updates the existing key's value if it does exist.
        
        :param key: key to add or update. May not be null.
        :param value: value to associate with key.
        """
        ...

    def Remove(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey) -> bool:
        """
        Removes a key and its value from the table.
        
        :param key: key to remove. May not be null.
        :returns: true if the key is found and removed. Returns false if the key was not in the dictionary.
        """
        ...

    def Clear(self) -> None:
        """Clear all the key/value pairs"""
        ...

    def GetValue(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, createValueCallback: System_Runtime_CompilerServices_ConditionalWeakTable_CreateValueCallback) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        """
        Atomically searches for a specified key in the table and returns the corresponding value.
        If the key does not exist in the table, the method invokes a callback method to create a
        value that is bound to the specified key.
        
        :param key: key of the value to find. Cannot be null.
        :param createValueCallback: callback that creates value for key. Cannot be null.
        """
        ...

    def GetOrCreateValue(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        """
        Helper method to call GetValue without passing a creation delegate.  Uses Activator.CreateInstance
        to create new instances as needed.  If TValue does not have a default constructor, this will throw.
        
        :param key: key of the value to find. Cannot be null.
        """
        ...

    def CreateValueCallback(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_TValue]]:
        """Gets an enumerator for the table."""
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...


class IsReadOnlyAttribute(System.Attribute):
    """
    Reserved to be used by the compiler for tracking metadata.
    This attribute should not be used by developers in source code.
    """

    def __init__(self) -> None:
        ...


class DiscardableAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class ContractHelper(System.Object):
    """This class has no documentation."""

    InternalContractFailed: typing.List[System_EventHandler]
    """
    Allows a managed application environment such as an interactive interpreter (IronPython) or a
    web browser host (Jolt hosting Silverlight in IE) to be notified of contract failures and
    potentially "handle" them, either by throwing a particular exception type, etc.  If any of the
    event handlers sets the Cancel flag in the ContractFailedEventArgs, then the Contract class will
    not pop up an assert dialog box or trigger escalation policy.
    """

    @staticmethod
    def RaiseContractFailedEvent(failureKind: System.Diagnostics.Contracts.ContractFailureKind, userMessage: str, conditionText: str, innerException: System.Exception) -> str:
        """
        Rewriter will call this method on a contract failure to allow listeners to be notified.
        The method should not perform any failure (assert/throw) itself.
        This method has 3 functions:
        1. Call any contract hooks (such as listeners to Contract failed events)
        2. Determine if the listeners deem the failure as handled (then resultFailureMessage should be set to null)
        3. Produce a localized resultFailureMessage used in advertising the failure subsequently.
        On exit: null if the event was handled and should not trigger a failure.
                 Otherwise, returns the localized failure message.
        """
        ...

    @staticmethod
    def TriggerFailure(kind: System.Diagnostics.Contracts.ContractFailureKind, displayMessage: str, userMessage: str, conditionText: str, innerException: System.Exception) -> None:
        """Rewriter calls this method to get the default failure behavior."""
        ...


class DisablePrivateReflectionAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class INotifyCompletion(metaclass=abc.ABCMeta):
    """Represents an operation that will schedule continuations when the operation completes."""

    def OnCompleted(self, continuation: System.Action) -> None:
        """
        Schedules the continuation action to be invoked when the instance completes.
        
        :param continuation: The action to invoke when the operation completes.
        """
        ...


class ICriticalNotifyCompletion(System.Runtime.CompilerServices.INotifyCompletion, metaclass=abc.ABCMeta):
    """Represents an awaiter used to schedule continuations when an await operation completes."""

    def UnsafeOnCompleted(self, continuation: System.Action) -> None:
        """
        Schedules the continuation action to be invoked when the instance completes.
        
        :param continuation: The action to invoke when the operation completes.
        """
        ...


class ValueTaskAwaiter(System.Runtime.CompilerServices.ICriticalNotifyCompletion, IStateMachineBoxAwareAwaiter):
    """Provides an awaiter for a ValueTask."""

    s_invokeActionDelegate: typing.Callable[[System.Object], None] = ...
    """Shim used to invoke an Action passed as the state argument to a Action{Object}."""

    @property
    def action(self) -> System.Action:
        ...

    @action.setter
    def action(self, value: System.Action):
        ...


class Any(typing_Any):
    """Provides an awaiter for a ValueTask{TResult}."""

    @property
    def IsCompleted(self) -> bool:
        """Gets whether the ValueTask{TResult} has completed."""
        ...

    def GetResult(self) -> ValueTaskAwaiter_TResult:
        """Gets the result of the ValueTask."""
        ...

    def OnCompleted(self, continuation: typing.Any) -> None:
        """Schedules the continuation action for this ValueTask."""
        ...

    def UnsafeOnCompleted(self, continuation: typing.Any) -> None:
        """Schedules the continuation action for this ValueTask."""
        ...

    def AwaitUnsafeOnCompleted(self, box: typing.Any) -> None:
        ...


class CallerArgumentExpressionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def ParameterName(self) -> str:
        ...

    def __init__(self, parameterName: str) -> None:
        ...


class StateMachineAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def StateMachineType(self) -> typing.Type:
        ...

    def __init__(self, stateMachineType: typing.Type) -> None:
        ...


class AsyncStateMachineAttribute(System.Runtime.CompilerServices.StateMachineAttribute):
    """This class has no documentation."""

    def __init__(self, stateMachineType: typing.Type) -> None:
        ...


class ExtensionAttribute(System.Attribute):
    """Indicates that a method is an extension method, or that a class or assembly contains extension methods."""


class IsByRefLikeAttribute(System.Attribute):
    """
    Reserved to be used by the compiler for tracking metadata.
    This attribute should not be used by developers in source code.
    """

    def __init__(self) -> None:
        ...


class ConfiguredValueTaskAwaitable(typing.Generic[System_Runtime_CompilerServices_ConfiguredValueTaskAwaitable_TResult]):
    """Provides an awaitable type that enables configured awaits on a ValueTask{TResult}."""

    @typing.overload
    def GetAwaiter(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable.ConfiguredValueTaskAwaiter:
        """Returns an awaiter for this ConfiguredValueTaskAwaitable instance."""
        ...

    @typing.overload
    def GetAwaiter(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable.ConfiguredValueTaskAwaiter:
        """Returns an awaiter for this ConfiguredValueTaskAwaitable{TResult} instance."""
        ...


class ConfiguredCancelableAsyncEnumerable(typing.Generic[System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T]):
    """Provides an awaitable async enumerable that enables cancelable iteration and configured awaits."""

    class Enumerator:
        """Provides an awaitable async enumerator that enables cancelable iteration and configured awaits."""

        @property
        def Current(self) -> System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T:
            """Gets the element in the collection at the current position of the enumerator."""
            ...

        def MoveNextAsync(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable[bool]:
            """
            Advances the enumerator asynchronously to the next element of the collection.
            
            :returns: A ConfiguredValueTaskAwaitable{Boolean} that will complete with a result of true if the enumerator was successfully advanced to the next element, or false if the enumerator has passed the end of the collection.
            """
            ...

        def DisposeAsync(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable:
            """
            Performs application-defined tasks associated with freeing, releasing, or
            resetting unmanaged resources asynchronously.
            """
            ...

    def ConfigureAwait(self, continueOnCapturedContext: bool) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable[System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T]:
        """
        Configures how awaits on the tasks returned from an async iteration will be performed.
        
        :param continueOnCapturedContext: Whether to capture and marshal back to the current context.
        :returns: The configured enumerable.
        """
        ...

    def WithCancellation(self, cancellationToken: System.Threading.CancellationToken) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable[System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T]:
        """
        Sets the CancellationToken to be passed to IAsyncEnumerable{T}.GetAsyncEnumerator(CancellationToken) when iterating.
        
        :param cancellationToken: The CancellationToken to use.
        :returns: The configured enumerable.
        """
        ...

    def GetAsyncEnumerator(self) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable.Enumerator:
        ...


class CompilationRelaxations(System.Enum):
    """This class has no documentation."""

    NoStringInterning = ...


class CustomConstantAttribute(System.Attribute, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Value(self) -> System.Object:
        ...


class DateTimeConstantAttribute(System.Runtime.CompilerServices.CustomConstantAttribute):
    """This class has no documentation."""

    @property
    def Value(self) -> System.Object:
        ...

    def __init__(self, ticks: int) -> None:
        ...


class AsyncTaskMethodBuilder(typing.Generic[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult]):
    """
    Provides a builder for asynchronous methods that return System.Threading.Tasks.Task{TResult}.
    This type is intended for compiler use only.
    """

    @property
    def Task(self) -> System.Threading.Tasks.Task:
        """Gets the System.Threading.Tasks.Task for this builder."""
        ...

    @property
    def ObjectIdForDebugger(self) -> System.Object:
        """Gets an object that may be used to uniquely identify this builder to the debugger."""
        ...

    @staticmethod
    @typing.overload
    def Create() -> System.Runtime.CompilerServices.AsyncTaskMethodBuilder:
        """
        Initializes a new AsyncTaskMethodBuilder.
        
        :returns: The initialized AsyncTaskMethodBuilder.
        """
        ...

    @typing.overload
    def Start(self, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine) -> None:
        """
        Initiates the builder's execution with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...

    @typing.overload
    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the state machine it represents.
        
        :param stateMachine: The heap-allocated state machine object.
        """
        ...

    @typing.overload
    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @typing.overload
    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @typing.overload
    def SetResult(self) -> None:
        """
        Completes the System.Threading.Tasks.Task in the
        System.Threading.Tasks.TaskStatus state.
        """
        ...

    @typing.overload
    def SetException(self, exception: System.Exception) -> None:
        """
        Completes the System.Threading.Tasks.Task in the
        System.Threading.Tasks.TaskStatus state with the specified exception.
        
        :param exception: The System.Exception to use to fault the task.
        """
        ...

    @staticmethod
    @typing.overload
    def Create() -> System.Runtime.CompilerServices.AsyncTaskMethodBuilder[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult]:
        """
        Initializes a new AsyncTaskMethodBuilder.
        
        :returns: The initialized AsyncTaskMethodBuilder.
        """
        ...

    @typing.overload
    def Start(self, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine) -> None:
        """
        Initiates the builder's execution with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...

    @typing.overload
    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the state machine it represents.
        
        :param stateMachine: The heap-allocated state machine object.
        """
        ...

    @typing.overload
    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @typing.overload
    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @typing.overload
    def SetResult(self, result: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult) -> None:
        """
        Completes the System.Threading.Tasks.Task{TResult} in the
        System.Threading.Tasks.TaskStatus state with the specified result.
        
        :param result: The result to use to complete the task.
        """
        ...

    @typing.overload
    def SetException(self, exception: System.Exception) -> None:
        """
        Completes the System.Threading.Tasks.Task{TResult} in the
        System.Threading.Tasks.TaskStatus state with the specified exception.
        
        :param exception: The System.Exception to use to fault the task.
        """
        ...


class ReferenceAssemblyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Description(self) -> str:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, description: str) -> None:
        ...


class RuntimeFeature(System.Object):
    """This class has no documentation."""

    PortablePdb: str = ...
    """Name of the Portable PDB feature."""

    DefaultImplementationsOfInterfaces: str = ...
    """Indicates that this version of runtime supports default interface method implementations."""

    UnmanagedSignatureCallingConvention: str = ...
    """Indicates that this version of runtime supports the Unmanaged calling convention value."""

    CovariantReturnsOfClasses: str = ...
    """Indicates that this version of runtime supports covariant returns in overrides of methods declared in classes."""

    IsDynamicCodeSupported: bool

    IsDynamicCodeCompiled: bool

    @staticmethod
    def IsSupported(feature: str) -> bool:
        """Checks whether a certain feature is supported by the Runtime."""
        ...


class EnumeratorCancellationAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class TaskAwaiter(typing.Generic[System_Runtime_CompilerServices_TaskAwaiter_TResult], System.Runtime.CompilerServices.ICriticalNotifyCompletion, System.Runtime.CompilerServices.ITaskAwaiter):
    """Provides an awaiter for awaiting a System.Threading.Tasks.Task{TResult}."""

    @property
    def m_task(self) -> System.Threading.Tasks.Task:
        ...

    @property
    def IsCompleted(self) -> bool:
        """Gets whether the task being awaited is completed."""
        ...

    @typing.overload
    def OnCompleted(self, continuation: System.Action) -> None:
        """
        Schedules the continuation onto the System.Threading.Tasks.Task associated with this TaskAwaiter.
        
        :param continuation: The action to invoke when the await operation completes.
        """
        ...

    @typing.overload
    def UnsafeOnCompleted(self, continuation: System.Action) -> None:
        """
        Schedules the continuation onto the System.Threading.Tasks.Task associated with this TaskAwaiter.
        
        :param continuation: The action to invoke when the await operation completes.
        """
        ...

    @typing.overload
    def GetResult(self) -> None:
        """Ends the await on the completed System.Threading.Tasks.Task."""
        ...

    @typing.overload
    def OnCompleted(self, continuation: System.Action) -> None:
        """
        Schedules the continuation onto the System.Threading.Tasks.Task associated with this TaskAwaiter.
        
        :param continuation: The action to invoke when the await operation completes.
        """
        ...

    @typing.overload
    def UnsafeOnCompleted(self, continuation: System.Action) -> None:
        """
        Schedules the continuation onto the System.Threading.Tasks.Task associated with this TaskAwaiter.
        
        :param continuation: The action to invoke when the await operation completes.
        """
        ...

    @typing.overload
    def GetResult(self) -> System_Runtime_CompilerServices_TaskAwaiter_TResult:
        """
        Ends the await on the completed System.Threading.Tasks.Task{TResult}.
        
        :returns: The result of the completed System.Threading.Tasks.Task{TResult}.
        """
        ...


class ConfiguredTaskAwaitable(typing.Generic[System_Runtime_CompilerServices_ConfiguredTaskAwaitable_TResult]):
    """Provides an awaitable object that allows for configured awaits on System.Threading.Tasks.Task{TResult}."""

    @typing.overload
    def GetAwaiter(self) -> System.Runtime.CompilerServices.ConfiguredTaskAwaitable.ConfiguredTaskAwaiter:
        """
        Gets an awaiter for this awaitable.
        
        :returns: The awaiter.
        """
        ...

    @typing.overload
    def GetAwaiter(self) -> System.Runtime.CompilerServices.ConfiguredTaskAwaitable.ConfiguredTaskAwaiter:
        """
        Gets an awaiter for this awaitable.
        
        :returns: The awaiter.
        """
        ...


class CompilerGeneratedAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class TupleElementNamesAttribute(System.Attribute):
    """Indicates that the use of System.ValueTuple on a member is meant to be treated as a tuple with element names."""

    @property
    def TransformNames(self) -> System.Collections.Generic.IList[str]:
        """
        Specifies, in a pre-order depth-first traversal of a type's
        construction, which System.ValueTuple elements are
        meant to carry element names.
        """
        ...

    def __init__(self, transformNames: typing.List[str]) -> None:
        """
        Initializes a new instance of the TupleElementNamesAttribute class.
        
        :param transformNames: Specifies, in a pre-order depth-first traversal of a type's construction, which System.ValueType occurrences are meant to carry element names.
        """
        ...


class TypeForwardedFromAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def AssemblyFullName(self) -> str:
        ...

    def __init__(self, assemblyFullName: str) -> None:
        ...


class IteratorStateMachineAttribute(System.Runtime.CompilerServices.StateMachineAttribute):
    """This class has no documentation."""

    def __init__(self, stateMachineType: typing.Type) -> None:
        ...


class ConfiguredAsyncDisposable:
    """Provides a type that can be used to configure how awaits on an IAsyncDisposable are performed."""

    def DisposeAsync(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable:
        ...


class CallConvCdecl(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvFastcall(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvStdcall(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvSuppressGCTransition(System.Object):
    """Indicates that a method should suppress the GC transition as part of the calling convention."""

    def __init__(self) -> None:
        """Initializes a new instance of the CallConvSuppressGCTransition class."""
        ...


class CallConvThiscall(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class ITuple(metaclass=abc.ABCMeta):
    """This interface is required for types that want to be indexed into by dynamic patterns."""

    @property
    @abc.abstractmethod
    def Length(self) -> int:
        """The number of positions in this data structure."""
        ...

    def __getitem__(self, index: int) -> System.Object:
        """Get the element at position ."""
        ...


class MethodCodeType(System.Enum):
    """This class has no documentation."""

    IL = ...

    Native = ...

    OPTIL = ...

    Runtime = ...


class PreserveBaseOverridesAttribute(System.Attribute):
    """This class has no documentation."""


class DecimalConstantAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Value(self) -> float:
        ...

    @typing.overload
    def __init__(self, scale: int, sign: int, hi: int, mid: int, low: int) -> None:
        ...

    @typing.overload
    def __init__(self, scale: int, sign: int, hi: int, mid: int, low: int) -> None:
        ...


class SpecialNameAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallerMemberNameAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class YieldAwaitable:
    """This class has no documentation."""

    class YieldAwaiter(System.Runtime.CompilerServices.ICriticalNotifyCompletion, IStateMachineBoxAwareAwaiter):
        """Provides an awaiter that switches into a target environment."""

        @property
        def IsCompleted(self) -> bool:
            """Gets whether a yield is not required."""
            ...

        def OnCompleted(self, continuation: System.Action) -> None:
            """
            Posts the  back to the current context.
            
            :param continuation: The action to invoke asynchronously.
            """
            ...

        def UnsafeOnCompleted(self, continuation: System.Action) -> None:
            """
            Posts the  back to the current context.
            
            :param continuation: The action to invoke asynchronously.
            """
            ...

        def AwaitUnsafeOnCompleted(self, box: System.Runtime.CompilerServices.IAsyncStateMachineBox) -> None:
            ...

        def GetResult(self) -> None:
            """Ends the await operation."""
            ...

    def GetAwaiter(self) -> System.Runtime.CompilerServices.YieldAwaitable.YieldAwaiter:
        """
        Gets an awaiter for this YieldAwaitable.
        
        :returns: An awaiter for this awaitable.
        """
        ...


class IsVolatile(System.Object):
    """This class has no documentation."""


class AsyncValueTaskMethodBuilder(typing.Generic[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult]):
    """Represents a builder for asynchronous methods that returns a ValueTask{TResult}."""

    s_valueTaskPoolingEnabled: bool = ...
    """true if we should use reusable boxes for async completions of ValueTask methods; false if we should use tasks."""

    s_valueTaskPoolingCacheSize: int = ...
    """Maximum number of boxes that are allowed to be cached per state machine type."""

    @property
    def Task(self) -> System.Threading.Tasks.ValueTask:
        """Gets the task for this builder."""
        ...

    @property
    def ObjectIdForDebugger(self) -> System.Object:
        """Gets an object that may be used to uniquely identify this builder to the debugger."""
        ...

    s_syncSuccessSentinel: System.Object = ...
    """Sentinel object used to indicate that the builder completed synchronously and successfully."""

    @staticmethod
    @typing.overload
    def Create() -> System.Runtime.CompilerServices.AsyncValueTaskMethodBuilder:
        """
        Creates an instance of the AsyncValueTaskMethodBuilder struct.
        
        :returns: The initialized instance.
        """
        ...

    @typing.overload
    def Start(self, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine) -> None:
        """
        Begins running the builder with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...

    @typing.overload
    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the specified state machine.
        
        :param stateMachine: The state machine instance to associate with the builder.
        """
        ...

    @typing.overload
    def SetResult(self) -> None:
        """Marks the task as successfully completed."""
        ...

    @typing.overload
    def SetException(self, exception: System.Exception) -> None:
        """
        Marks the task as failed and binds the specified exception to the task.
        
        :param exception: The exception to bind to the task.
        """
        ...

    @typing.overload
    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @typing.overload
    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @staticmethod
    @typing.overload
    def Create() -> System.Runtime.CompilerServices.AsyncValueTaskMethodBuilder[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult]:
        """
        Creates an instance of the AsyncValueTaskMethodBuilder{TResult} struct.
        
        :returns: The initialized instance.
        """
        ...

    @typing.overload
    def Start(self, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine) -> None:
        """
        Begins running the builder with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...

    @typing.overload
    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the specified state machine.
        
        :param stateMachine: The state machine instance to associate with the builder.
        """
        ...

    @typing.overload
    def SetResult(self, result: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult) -> None:
        """
        Marks the value task as successfully completed.
        
        :param result: The result to use to complete the value task.
        """
        ...

    @typing.overload
    def SetException(self, exception: System.Exception) -> None:
        """
        Marks the value task as failed and binds the specified exception to the value task.
        
        :param exception: The exception to bind to the value task.
        """
        ...

    @typing.overload
    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: the awaiter
        :param stateMachine: The state machine.
        """
        ...

    @typing.overload
    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: the awaiter
        :param stateMachine: The state machine.
        """
        ...


class CompilerGlobalScopeAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class AccessedThroughPropertyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def PropertyName(self) -> str:
        ...

    def __init__(self, propertyName: str) -> None:
        ...


class CallerFilePathAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class TypeForwardedToAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Destination(self) -> typing.Type:
        ...

    def __init__(self, destination: typing.Type) -> None:
        ...


class ModuleInitializerAttribute(System.Attribute):
    """
    Used to indicate to the compiler that a method should be called
    in its containing module's initializer.
    """

    def __init__(self) -> None:
        ...


class UnsafeValueTypeAttribute(System.Attribute):
    """This class has no documentation."""


class CallerLineNumberAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class IsExternalInit(System.Object):
    """
    Reserved to be used by the compiler for tracking metadata.
    This class should not be used by developers in source code.
    """


class MethodImplOptions(System.Enum):
    """This class has no documentation."""

    Unmanaged = ...

    NoInlining = ...

    ForwardRef = ...

    Synchronized = ...

    NoOptimization = ...

    PreserveSig = ...

    AggressiveInlining = ...

    AggressiveOptimization = ...

    InternalCall = ...


class MethodImplAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def MethodCodeType(self) -> System.Runtime.CompilerServices.MethodCodeType:
        ...

    @MethodCodeType.setter
    def MethodCodeType(self, value: System.Runtime.CompilerServices.MethodCodeType):
        ...

    @property
    def Value(self) -> int:
        """This property contains the int value of a member of the System.Runtime.CompilerServices.MethodImplOptions enum."""
        ...

    @typing.overload
    def __init__(self, methodImplOptions: System.Runtime.CompilerServices.MethodImplOptions) -> None:
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...


class AsyncIteratorStateMachineAttribute(System.Runtime.CompilerServices.StateMachineAttribute):
    """Indicates whether a method is an asynchronous iterator."""

    def __init__(self, stateMachineType: typing.Type) -> None:
        """
        Initializes a new instance of the AsyncIteratorStateMachineAttribute class.
        
        :param stateMachineType: The type object for the underlying state machine type that's used to implement a state machine method.
        """
        ...


class FixedBufferAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def ElementType(self) -> typing.Type:
        ...

    @property
    def Length(self) -> int:
        ...

    def __init__(self, elementType: typing.Type, length: int) -> None:
        ...


class IsConst(System.Object):
    """This class has no documentation."""


class InternalsVisibleToAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def AssemblyName(self) -> str:
        ...

    @property
    def AllInternalsVisible(self) -> bool:
        ...

    @AllInternalsVisible.setter
    def AllInternalsVisible(self, value: bool):
        ...

    def __init__(self, assemblyName: str) -> None:
        ...


class IndexerNameAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self, indexerName: str) -> None:
        ...


class CompilationRelaxationsAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def CompilationRelaxations(self) -> int:
        ...

    @typing.overload
    def __init__(self, relaxations: int) -> None:
        ...

    @typing.overload
    def __init__(self, relaxations: System.Runtime.CompilerServices.CompilationRelaxations) -> None:
        ...


class AsyncIteratorMethodBuilder:
    """Represents a builder for asynchronous iterators."""

    @property
    def ObjectIdForDebugger(self) -> System.Object:
        """Gets an object that may be used to uniquely identify this builder to the debugger."""
        ...

    @staticmethod
    def Create() -> System.Runtime.CompilerServices.AsyncIteratorMethodBuilder:
        """
        Creates an instance of the AsyncIteratorMethodBuilder struct.
        
        :returns: The initialized instance.
        """
        ...

    def MoveNext(self, stateMachine: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine) -> None:
        """
        Invokes IAsyncStateMachine.MoveNext on the state machine while guarding the ExecutionContext.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...

    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    def Complete(self) -> None:
        """Marks iteration as being completed, whether successfully or otherwise."""
        ...


class AsyncMethodBuilderAttribute(System.Attribute):
    """
    Indicates the type of the async method builder that should be used by a language compiler to
    build the attributed type when used as the return type of an async method.
    """

    @property
    def BuilderType(self) -> typing.Type:
        """Gets the Type of the associated builder."""
        ...

    def __init__(self, builderType: typing.Type) -> None:
        """
        Initializes the AsyncMethodBuilderAttribute.
        
        :param builderType: The Type of the associated builder.
        """
        ...


class FormattableStringFactory(System.Object):
    """A factory type used by compilers to create instances of the type FormattableString."""

    @staticmethod
    def Create(format: str, *arguments: typing.Any) -> System.FormattableString:
        """
        Create a FormattableString from a composite format string and object
        array containing zero or more objects to format.
        """
        ...


class RuntimeHelpers(System.Object):
    """This class has no documentation."""

    QCall: str = "QCall"

    OffsetToStringData: int

    def TryCode(self, userData: typing.Any) -> None:
        ...

    def CleanupCode(self, userData: typing.Any, exceptionThrown: bool) -> None:
        ...

    @staticmethod
    def GetSubArray(array: typing.List[System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T], range: System.Range) -> typing.List[System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T]:
        """Slices the specified array using the specified range."""
        ...

    @staticmethod
    def ExecuteCodeWithGuaranteedCleanup(code: System_Runtime_CompilerServices_RuntimeHelpers_TryCode, backoutCode: System_Runtime_CompilerServices_RuntimeHelpers_CleanupCode, userData: typing.Any) -> None:
        ...

    @staticmethod
    def PrepareContractedDelegate(d: System.Delegate) -> None:
        ...

    @staticmethod
    def ProbeForSufficientStack() -> None:
        ...

    @staticmethod
    def PrepareConstrainedRegions() -> None:
        ...

    @staticmethod
    def PrepareConstrainedRegionsNoOP() -> None:
        ...

    @staticmethod
    def InitializeArray(array: System.Array, fldHandle: System.RuntimeFieldHandle) -> None:
        ...

    @staticmethod
    def GetHashCode(o: typing.Any) -> int:
        ...

    @staticmethod
    def Equals(o1: typing.Any, o2: typing.Any) -> bool:
        ...

    @staticmethod
    def GetObjectValue(obj: typing.Any) -> System.Object:
        ...

    @staticmethod
    def RunClassConstructor(type: System.RuntimeTypeHandle) -> None:
        ...

    @staticmethod
    def EnsureSufficientExecutionStack() -> None:
        ...

    @staticmethod
    def TryEnsureSufficientExecutionStack() -> bool:
        ...

    @staticmethod
    def PrepareDelegate(d: System.Delegate) -> None:
        ...

    @staticmethod
    @typing.overload
    def PrepareMethod(method: System.RuntimeMethodHandle) -> None:
        ...

    @staticmethod
    @typing.overload
    def PrepareMethod(method: System.RuntimeMethodHandle, instantiation: typing.List[System.RuntimeTypeHandle]) -> None:
        ...

    @staticmethod
    def RunModuleConstructor(module: System.ModuleHandle) -> None:
        ...

    @staticmethod
    def AllocateTypeAssociatedMemory(type: typing.Type, size: int) -> System.IntPtr:
        ...

    @staticmethod
    def IsReferenceOrContainsReferences() -> bool:
        ...

    @staticmethod
    def GetUninitializedObject(type: typing.Type) -> System.Object:
        ...


class DependencyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def DependentAssembly(self) -> str:
        ...

    @property
    def LoadHint(self) -> int:
        """This property contains the int value of a member of the System.Runtime.CompilerServices.LoadHint enum."""
        ...

    def __init__(self, dependentAssemblyArgument: str, loadHintArgument: System.Runtime.CompilerServices.LoadHint) -> None:
        ...


class SkipLocalsInitAttribute(System.Attribute):
    """
    Used to indicate to the compiler that the .locals init
    flag should not be set in method headers.
    """

    def __init__(self) -> None:
        ...


class SuppressIldasmAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class IStrongBox(metaclass=abc.ABCMeta):
    """Defines a property for accessing the value that an object references."""

    @property
    @abc.abstractmethod
    def Value(self) -> System.Object:
        """Gets or sets the value the object references."""
        ...

    @Value.setter
    @abc.abstractmethod
    def Value(self, value: System.Object):
        """Gets or sets the value the object references."""
        ...


class StrongBox(typing.Generic[System_Runtime_CompilerServices_StrongBox_T], System.Object, System.Runtime.CompilerServices.IStrongBox):
    """Holds a reference to a value."""

    @property
    def Value(self) -> System_Runtime_CompilerServices_StrongBox_T:
        """Gets the strongly typed value associated with the StrongBox{T}This is explicitly exposed as a field instead of a property to enable loading the address of the field."""
        ...

    @Value.setter
    def Value(self, value: System_Runtime_CompilerServices_StrongBox_T):
        """Gets the strongly typed value associated with the StrongBox{T}This is explicitly exposed as a field instead of a property to enable loading the address of the field."""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Initializes a new StrongBox which can receive a value when used in a reference call."""
        ...

    @typing.overload
    def __init__(self, value: System_Runtime_CompilerServices_StrongBox_T) -> None:
        """
        Initializes a new StrongBox{T} with the specified value.
        
        :param value: A value that the StrongBox{T} will reference.
        """
        ...


class SwitchExpressionException(System.InvalidOperationException):
    """
    Indicates that a switch expression that was non-exhaustive failed to match its input
    at runtime, e.g. in the C# 8 expression 3 switch { 4 => 5 }.
    The exception optionally contains an object representing the unmatched value.
    """

    @property
    def UnmatchedValue(self) -> System.Object:
        ...

    @property
    def Message(self) -> str:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, innerException: System.Exception) -> None:
        ...

    @typing.overload
    def __init__(self, unmatchedValue: typing.Any) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...


class ICastable(metaclass=abc.ABCMeta):
    """
    Support for dynamic interface casting. Specifically implementing this interface on a type will allow the
    type to support interfaces (for the purposes of casting and interface dispatch) that do not appear in its
    interface map.
    """

    def IsInstanceOfInterface(self, interfaceType: System.RuntimeTypeHandle, castError: System.Exception) -> bool:
        ...

    def GetImplType(self, interfaceType: System.RuntimeTypeHandle) -> System.RuntimeTypeHandle:
        ...


class FixedAddressValueTypeAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class StringFreezingAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class RuntimeCompatibilityAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def WrapNonExceptionThrows(self) -> bool:
        ...

    @WrapNonExceptionThrows.setter
    def WrapNonExceptionThrows(self, value: bool):
        ...

    def __init__(self) -> None:
        ...


