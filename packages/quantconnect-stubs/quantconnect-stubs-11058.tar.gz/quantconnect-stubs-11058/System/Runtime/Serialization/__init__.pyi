import abc
import datetime
import typing

import System
import System.Collections
import System.Runtime.Serialization
import System.Threading


class OnDeserializedAttribute(System.Attribute):
    """This class has no documentation."""


class IFormatterConverter(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @typing.overload
    def Convert(self, value: typing.Any, type: typing.Type) -> System.Object:
        ...

    @typing.overload
    def Convert(self, value: typing.Any, typeCode: System.TypeCode) -> System.Object:
        ...

    def ToBoolean(self, value: typing.Any) -> bool:
        ...

    def ToChar(self, value: typing.Any) -> str:
        ...

    def ToSByte(self, value: typing.Any) -> int:
        ...

    def ToByte(self, value: typing.Any) -> int:
        ...

    def ToInt16(self, value: typing.Any) -> int:
        ...

    def ToUInt16(self, value: typing.Any) -> int:
        ...

    def ToInt32(self, value: typing.Any) -> int:
        ...

    def ToUInt32(self, value: typing.Any) -> int:
        ...

    def ToInt64(self, value: typing.Any) -> int:
        ...

    def ToUInt64(self, value: typing.Any) -> int:
        ...

    def ToSingle(self, value: typing.Any) -> float:
        ...

    def ToDouble(self, value: typing.Any) -> float:
        ...

    def ToDecimal(self, value: typing.Any) -> float:
        ...

    def ToDateTime(self, value: typing.Any) -> datetime.datetime:
        ...

    def ToString(self, value: typing.Any) -> str:
        ...


class DeserializationToken(System.IDisposable):
    """This class has no documentation."""

    def Dispose(self) -> None:
        ...


class StreamingContextStates(System.Enum):
    """This class has no documentation."""

    CrossProcess = ...

    CrossMachine = ...

    File = ...

    Persistence = ...

    Remoting = ...

    Other = ...

    Clone = ...

    CrossAppDomain = ...

    All = ...


class StreamingContext:
    """This class has no documentation."""

    @property
    def State(self) -> int:
        """This property contains the int value of a member of the System.Runtime.Serialization.StreamingContextStates enum."""
        ...

    @property
    def Context(self) -> System.Object:
        ...

    @typing.overload
    def __init__(self, state: System.Runtime.Serialization.StreamingContextStates) -> None:
        ...

    @typing.overload
    def __init__(self, state: System.Runtime.Serialization.StreamingContextStates, additional: typing.Any) -> None:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class ISafeSerializationData(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def CompleteDeserialization(self, deserialized: typing.Any) -> None:
        ...


class SerializationInfoEnumerator(System.Object, System.Collections.IEnumerator):
    """This class has no documentation."""

    @property
    def Current(self) -> System.Object:
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def Value(self) -> System.Object:
        ...

    @property
    def ObjectType(self) -> typing.Type:
        ...

    def MoveNext(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class SerializationInfo(System.Object):
    """The structure for holding all of the data needed for object serialization and deserialization."""

    AsyncDeserializationInProgress: System.Threading.AsyncLocal[bool]

    DeserializationInProgress: bool

    @property
    def FullTypeName(self) -> str:
        ...

    @FullTypeName.setter
    def FullTypeName(self, value: str):
        ...

    @property
    def AssemblyName(self) -> str:
        ...

    @AssemblyName.setter
    def AssemblyName(self, value: str):
        ...

    @property
    def IsFullTypeNameSetExplicit(self) -> bool:
        ...

    @IsFullTypeNameSetExplicit.setter
    def IsFullTypeNameSetExplicit(self, value: bool):
        ...

    @property
    def IsAssemblyNameSetExplicit(self) -> bool:
        ...

    @IsAssemblyNameSetExplicit.setter
    def IsAssemblyNameSetExplicit(self, value: bool):
        ...

    @property
    def MemberCount(self) -> int:
        ...

    @property
    def ObjectType(self) -> typing.Type:
        ...

    @staticmethod
    @typing.overload
    def ThrowIfDeserializationInProgress() -> None:
        ...

    @staticmethod
    @typing.overload
    def ThrowIfDeserializationInProgress(switchSuffix: str, cachedValue: int) -> None:
        ...

    @staticmethod
    def StartDeserialization() -> System.Runtime.Serialization.DeserializationToken:
        ...

    @typing.overload
    def __init__(self, type: typing.Type, converter: System.Runtime.Serialization.IFormatterConverter) -> None:
        ...

    @typing.overload
    def __init__(self, type: typing.Type, converter: System.Runtime.Serialization.IFormatterConverter, requireSameTokenInPartialTrust: bool) -> None:
        ...

    def SetType(self, type: typing.Type) -> None:
        ...

    def GetEnumerator(self) -> System.Runtime.Serialization.SerializationInfoEnumerator:
        ...

    @typing.overload
    def AddValue(self, name: str, value: typing.Any, type: typing.Type) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: typing.Any) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: bool) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: str) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: float) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: float) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: float) -> None:
        ...

    @typing.overload
    def AddValue(self, name: str, value: datetime.datetime) -> None:
        ...

    def UpdateValue(self, name: str, value: typing.Any, type: typing.Type) -> None:
        """
        Finds the value if it exists in the current data. If it does, we replace
        the values, if not, we append it to the end. This is useful to the
        ObjectManager when it's performing fixups.
        
        All error checking is done with asserts. Although public in coreclr,
        it's not exposed in a contract and is only meant to be used by other runtime libraries.
        
        This isn't a public API, but it gets invoked dynamically by
        BinaryFormatter
        
        This should not be used by clients: exposing out this functionality would allow children
        to overwrite their parent's values. It is public in order to give other runtime libraries access to it for
        its ObjectManager implementation, but it should not be exposed out of a contract.
        
        :param name: The name of the data to be updated.
        :param value: The new value.
        :param type: The type of the data being added.
        """
        ...

    def GetValue(self, name: str, type: typing.Type) -> System.Object:
        ...

    def GetBoolean(self, name: str) -> bool:
        ...

    def GetChar(self, name: str) -> str:
        ...

    def GetSByte(self, name: str) -> int:
        ...

    def GetByte(self, name: str) -> int:
        ...

    def GetInt16(self, name: str) -> int:
        ...

    def GetUInt16(self, name: str) -> int:
        ...

    def GetInt32(self, name: str) -> int:
        ...

    def GetUInt32(self, name: str) -> int:
        ...

    def GetInt64(self, name: str) -> int:
        ...

    def GetUInt64(self, name: str) -> int:
        ...

    def GetSingle(self, name: str) -> float:
        ...

    def GetDouble(self, name: str) -> float:
        ...

    def GetDecimal(self, name: str) -> float:
        ...

    def GetDateTime(self, name: str) -> datetime.datetime:
        ...

    def GetString(self, name: str) -> str:
        ...


class SerializationException(System.SystemException):
    """This class has no documentation."""

    @typing.overload
    def __init__(self) -> None:
        """
        Creates a new SerializationException with its message
        string set to a default message.
        """
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


class SerializationEntry:
    """This class has no documentation."""

    @property
    def Value(self) -> System.Object:
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def ObjectType(self) -> typing.Type:
        ...


class SafeSerializationEventArgs(System.EventArgs):
    """This class has no documentation."""

    @property
    def StreamingContext(self) -> System.Runtime.Serialization.StreamingContext:
        ...

    def AddSerializedState(self, serializedState: System.Runtime.Serialization.ISafeSerializationData) -> None:
        ...


class IDeserializationCallback(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def OnDeserialization(self, sender: typing.Any) -> None:
        ...


class OnDeserializingAttribute(System.Attribute):
    """This class has no documentation."""


class ISerializable(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...


class OnSerializingAttribute(System.Attribute):
    """This class has no documentation."""


class OptionalFieldAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def VersionAdded(self) -> int:
        ...

    @VersionAdded.setter
    def VersionAdded(self, value: int):
        ...


class OnSerializedAttribute(System.Attribute):
    """This class has no documentation."""


class IObjectReference(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetRealObject(self, context: System.Runtime.Serialization.StreamingContext) -> System.Object:
        ...


