import abc
import typing

import System
import System.Collections
import System.Globalization
import System.Runtime.Serialization


class IEnumerator(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Current(self) -> System.Object:
        ...

    def MoveNext(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class IEnumerable(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...


class ICollection(System.Collections.IEnumerable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Count(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def SyncRoot(self) -> System.Object:
        ...

    @property
    @abc.abstractmethod
    def IsSynchronized(self) -> bool:
        ...

    def CopyTo(self, array: System.Array, index: int) -> None:
        ...


class DictionaryEntry:
    """This class has no documentation."""

    @property
    def Key(self) -> System.Object:
        ...

    @Key.setter
    def Key(self, value: System.Object):
        ...

    @property
    def Value(self) -> System.Object:
        ...

    @Value.setter
    def Value(self, value: System.Object):
        ...

    def __init__(self, key: typing.Any, value: typing.Any) -> None:
        ...

    def Deconstruct(self, key: typing.Any, value: typing.Any) -> None:
        ...


class IDictionaryEnumerator(System.Collections.IEnumerator, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Key(self) -> System.Object:
        ...

    @property
    @abc.abstractmethod
    def Value(self) -> System.Object:
        ...

    @property
    @abc.abstractmethod
    def Entry(self) -> System.Collections.DictionaryEntry:
        ...


class IDictionary(System.Collections.ICollection, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Keys(self) -> System.Collections.ICollection:
        ...

    @property
    @abc.abstractmethod
    def Values(self) -> System.Collections.ICollection:
        ...

    @property
    @abc.abstractmethod
    def IsReadOnly(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def IsFixedSize(self) -> bool:
        ...

    def __getitem__(self, key: typing.Any) -> System.Object:
        ...

    def __setitem__(self, key: typing.Any, value: System.Object) -> None:
        ...

    def Contains(self, key: typing.Any) -> bool:
        ...

    def Add(self, key: typing.Any, value: typing.Any) -> None:
        ...

    def Clear(self) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...

    def Remove(self, key: typing.Any) -> None:
        ...


class IHashCodeProvider(metaclass=abc.ABCMeta):
    """
    Provides a mechanism for a Hashtable user to override the default
    GetHashCode() function on Objects, providing their own hash function.
    """

    def GetHashCode(self, obj: typing.Any) -> int:
        """Returns a hash code for the given object."""
        ...


class IComparer(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Compare(self, x: typing.Any, y: typing.Any) -> int:
        ...


class IEqualityComparer(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Equals(self, x: typing.Any, y: typing.Any) -> bool:
        ...

    def GetHashCode(self, obj: typing.Any) -> int:
        ...


class Hashtable(System.Object, System.Collections.IDictionary, System.Runtime.Serialization.ISerializable, System.Runtime.Serialization.IDeserializationCallback, System.ICloneable):
    """This class has no documentation."""

    @property
    def hcp(self) -> System.Collections.IHashCodeProvider:
        """This property is protected."""
        ...

    @hcp.setter
    def hcp(self, value: System.Collections.IHashCodeProvider):
        """This property is protected."""
        ...

    @property
    def comparer(self) -> System.Collections.IComparer:
        """This property is protected."""
        ...

    @comparer.setter
    def comparer(self, value: System.Collections.IComparer):
        """This property is protected."""
        ...

    @property
    def EqualityComparer(self) -> System.Collections.IEqualityComparer:
        """This property is protected."""
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def IsFixedSize(self) -> bool:
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def Keys(self) -> System.Collections.ICollection:
        ...

    @property
    def Values(self) -> System.Collections.ICollection:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    @property
    def Count(self) -> int:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int, loadFactor: float) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int, loadFactor: float, equalityComparer: System.Collections.IEqualityComparer) -> None:
        ...

    @typing.overload
    def __init__(self, hcp: System.Collections.IHashCodeProvider, comparer: System.Collections.IComparer) -> None:
        ...

    @typing.overload
    def __init__(self, equalityComparer: System.Collections.IEqualityComparer) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int, hcp: System.Collections.IHashCodeProvider, comparer: System.Collections.IComparer) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int, equalityComparer: System.Collections.IEqualityComparer) -> None:
        ...

    @typing.overload
    def __init__(self, d: System.Collections.IDictionary) -> None:
        ...

    @typing.overload
    def __init__(self, d: System.Collections.IDictionary, loadFactor: float) -> None:
        ...

    @typing.overload
    def __init__(self, d: System.Collections.IDictionary, hcp: System.Collections.IHashCodeProvider, comparer: System.Collections.IComparer) -> None:
        ...

    @typing.overload
    def __init__(self, d: System.Collections.IDictionary, equalityComparer: System.Collections.IEqualityComparer) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int, loadFactor: float, hcp: System.Collections.IHashCodeProvider, comparer: System.Collections.IComparer) -> None:
        ...

    @typing.overload
    def __init__(self, d: System.Collections.IDictionary, loadFactor: float, hcp: System.Collections.IHashCodeProvider, comparer: System.Collections.IComparer) -> None:
        ...

    @typing.overload
    def __init__(self, d: System.Collections.IDictionary, loadFactor: float, equalityComparer: System.Collections.IEqualityComparer) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...

    def Add(self, key: typing.Any, value: typing.Any) -> None:
        ...

    def Clear(self) -> None:
        ...

    def Clone(self) -> System.Object:
        ...

    def Contains(self, key: typing.Any) -> bool:
        ...

    def ContainsKey(self, key: typing.Any) -> bool:
        ...

    def ContainsValue(self, value: typing.Any) -> bool:
        ...

    def CopyTo(self, array: System.Array, arrayIndex: int) -> None:
        ...

    def __getitem__(self, key: typing.Any) -> System.Object:
        ...

    def __setitem__(self, key: typing.Any, value: System.Object) -> None:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...

    def GetHash(self, key: typing.Any) -> int:
        """This method is protected."""
        ...

    def KeyEquals(self, item: typing.Any, key: typing.Any) -> bool:
        """This method is protected."""
        ...

    def Remove(self, key: typing.Any) -> None:
        ...

    @staticmethod
    def Synchronized(table: System.Collections.Hashtable) -> System.Collections.Hashtable:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def OnDeserialization(self, sender: typing.Any) -> None:
        ...


class IList(System.Collections.ICollection, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def IsReadOnly(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def IsFixedSize(self) -> bool:
        ...

    def __getitem__(self, index: int) -> System.Object:
        ...

    def __setitem__(self, index: int, value: System.Object) -> None:
        ...

    def Add(self, value: typing.Any) -> int:
        ...

    def Contains(self, value: typing.Any) -> bool:
        ...

    def Clear(self) -> None:
        ...

    def IndexOf(self, value: typing.Any) -> int:
        ...

    def Insert(self, index: int, value: typing.Any) -> None:
        ...

    def Remove(self, value: typing.Any) -> None:
        ...

    def RemoveAt(self, index: int) -> None:
        ...


class ListDictionaryInternal(System.Object, System.Collections.IDictionary):
    """This class has no documentation."""

    @property
    def Count(self) -> int:
        ...

    @property
    def Keys(self) -> System.Collections.ICollection:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def IsFixedSize(self) -> bool:
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    @property
    def Values(self) -> System.Collections.ICollection:
        ...

    def __init__(self) -> None:
        ...

    def __getitem__(self, key: typing.Any) -> System.Object:
        ...

    def __setitem__(self, key: typing.Any, value: System.Object) -> None:
        ...

    def Add(self, key: typing.Any, value: typing.Any) -> None:
        ...

    def Clear(self) -> None:
        ...

    def Contains(self, key: typing.Any) -> bool:
        ...

    def CopyTo(self, array: System.Array, index: int) -> None:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    def Remove(self, key: typing.Any) -> None:
        ...


class ArrayList(System.Object, System.Collections.IList, System.ICloneable):
    """This class has no documentation."""

    @property
    def Capacity(self) -> int:
        ...

    @Capacity.setter
    def Capacity(self, value: int):
        ...

    @property
    def Count(self) -> int:
        ...

    @property
    def IsFixedSize(self) -> bool:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int) -> None:
        ...

    @typing.overload
    def __init__(self, c: System.Collections.ICollection) -> None:
        ...

    def __getitem__(self, index: int) -> System.Object:
        ...

    def __setitem__(self, index: int, value: System.Object) -> None:
        ...

    @staticmethod
    def Adapter(list: System.Collections.IList) -> System.Collections.ArrayList:
        ...

    def Add(self, value: typing.Any) -> int:
        ...

    def AddRange(self, c: System.Collections.ICollection) -> None:
        ...

    @typing.overload
    def BinarySearch(self, index: int, count: int, value: typing.Any, comparer: System.Collections.IComparer) -> int:
        ...

    @typing.overload
    def BinarySearch(self, value: typing.Any) -> int:
        ...

    @typing.overload
    def BinarySearch(self, value: typing.Any, comparer: System.Collections.IComparer) -> int:
        ...

    def Clear(self) -> None:
        ...

    def Clone(self) -> System.Object:
        ...

    def Contains(self, item: typing.Any) -> bool:
        ...

    @typing.overload
    def CopyTo(self, array: System.Array) -> None:
        ...

    @typing.overload
    def CopyTo(self, array: System.Array, arrayIndex: int) -> None:
        ...

    @typing.overload
    def CopyTo(self, index: int, array: System.Array, arrayIndex: int, count: int) -> None:
        ...

    @staticmethod
    @typing.overload
    def FixedSize(list: System.Collections.IList) -> System.Collections.IList:
        ...

    @staticmethod
    @typing.overload
    def FixedSize(list: System.Collections.ArrayList) -> System.Collections.ArrayList:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    @typing.overload
    def GetEnumerator(self, index: int, count: int) -> System.Collections.IEnumerator:
        ...

    @typing.overload
    def IndexOf(self, value: typing.Any) -> int:
        ...

    @typing.overload
    def IndexOf(self, value: typing.Any, startIndex: int) -> int:
        ...

    @typing.overload
    def IndexOf(self, value: typing.Any, startIndex: int, count: int) -> int:
        ...

    def Insert(self, index: int, value: typing.Any) -> None:
        ...

    def InsertRange(self, index: int, c: System.Collections.ICollection) -> None:
        ...

    @typing.overload
    def LastIndexOf(self, value: typing.Any) -> int:
        ...

    @typing.overload
    def LastIndexOf(self, value: typing.Any, startIndex: int) -> int:
        ...

    @typing.overload
    def LastIndexOf(self, value: typing.Any, startIndex: int, count: int) -> int:
        ...

    @staticmethod
    @typing.overload
    def ReadOnly(list: System.Collections.IList) -> System.Collections.IList:
        ...

    @staticmethod
    @typing.overload
    def ReadOnly(list: System.Collections.ArrayList) -> System.Collections.ArrayList:
        ...

    def Remove(self, obj: typing.Any) -> None:
        ...

    def RemoveAt(self, index: int) -> None:
        ...

    def RemoveRange(self, index: int, count: int) -> None:
        ...

    @staticmethod
    def Repeat(value: typing.Any, count: int) -> System.Collections.ArrayList:
        ...

    @typing.overload
    def Reverse(self) -> None:
        ...

    @typing.overload
    def Reverse(self, index: int, count: int) -> None:
        ...

    def SetRange(self, index: int, c: System.Collections.ICollection) -> None:
        ...

    def GetRange(self, index: int, count: int) -> System.Collections.ArrayList:
        ...

    @typing.overload
    def Sort(self) -> None:
        ...

    @typing.overload
    def Sort(self, comparer: System.Collections.IComparer) -> None:
        ...

    @typing.overload
    def Sort(self, index: int, count: int, comparer: System.Collections.IComparer) -> None:
        ...

    @staticmethod
    @typing.overload
    def Synchronized(list: System.Collections.IList) -> System.Collections.IList:
        ...

    @staticmethod
    @typing.overload
    def Synchronized(list: System.Collections.ArrayList) -> System.Collections.ArrayList:
        ...

    @typing.overload
    def ToArray(self) -> typing.List[System.Object]:
        ...

    @typing.overload
    def ToArray(self, type: typing.Type) -> System.Array:
        ...

    def TrimToSize(self) -> None:
        ...


class IStructuralComparable(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def CompareTo(self, other: typing.Any, comparer: System.Collections.IComparer) -> int:
        ...


class IStructuralEquatable(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Equals(self, other: typing.Any, comparer: System.Collections.IEqualityComparer) -> bool:
        ...

    def GetHashCode(self, comparer: System.Collections.IEqualityComparer) -> int:
        ...


class Comparer(System.Object, System.Collections.IComparer, System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    Default: System.Collections.Comparer = ...

    DefaultInvariant: System.Collections.Comparer = ...

    def __init__(self, culture: System.Globalization.CultureInfo) -> None:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def Compare(self, a: typing.Any, b: typing.Any) -> int:
        ...


