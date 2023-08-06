import abc
import typing

import System
import System.Collections
import System.Collections.Generic
import System.Collections.ObjectModel
import System.Runtime.Serialization
import System.Threading

System_Converter = typing.Any
System_Predicate = typing.Any
System_Comparison = typing.Any
ValueTask = typing.Any

System_Collections_Generic_IEnumerable_T = typing.TypeVar("System_Collections_Generic_IEnumerable_T")
System_Collections_Generic_IList_T = typing.TypeVar("System_Collections_Generic_IList_T")
System_Collections_Generic_IAsyncEnumerable_T = typing.TypeVar("System_Collections_Generic_IAsyncEnumerable_T")
System_Collections_Generic_ICollection_T = typing.TypeVar("System_Collections_Generic_ICollection_T")
System_Collections_Generic_IReadOnlySet_T = typing.TypeVar("System_Collections_Generic_IReadOnlySet_T")
System_Collections_Generic_IComparer_T = typing.TypeVar("System_Collections_Generic_IComparer_T")
System_Collections_Generic_IDictionary_TValue = typing.TypeVar("System_Collections_Generic_IDictionary_TValue")
System_Collections_Generic_IDictionary_TKey = typing.TypeVar("System_Collections_Generic_IDictionary_TKey")
System_Collections_Generic_List_T = typing.TypeVar("System_Collections_Generic_List_T")
System_Collections_Generic_List_ConvertAll_TOutput = typing.TypeVar("System_Collections_Generic_List_ConvertAll_TOutput")
System_Collections_Generic_EqualityComparer_T = typing.TypeVar("System_Collections_Generic_EqualityComparer_T")
System_Collections_Generic_GenericEqualityComparer_T = typing.TypeVar("System_Collections_Generic_GenericEqualityComparer_T")
System_Collections_Generic_NullableEqualityComparer_T = typing.TypeVar("System_Collections_Generic_NullableEqualityComparer_T")
System_Collections_Generic_ObjectEqualityComparer_T = typing.TypeVar("System_Collections_Generic_ObjectEqualityComparer_T")
System_Collections_Generic_EnumEqualityComparer_T = typing.TypeVar("System_Collections_Generic_EnumEqualityComparer_T")
System_Collections_Generic_Dictionary_TValue = typing.TypeVar("System_Collections_Generic_Dictionary_TValue")
System_Collections_Generic_Dictionary_TKey = typing.TypeVar("System_Collections_Generic_Dictionary_TKey")
System_Collections_Generic_IReadOnlyCollection_T = typing.TypeVar("System_Collections_Generic_IReadOnlyCollection_T")
System_Collections_Generic_IAsyncEnumerator_T = typing.TypeVar("System_Collections_Generic_IAsyncEnumerator_T")
System_Collections_Generic_KeyValuePair_TKey = typing.TypeVar("System_Collections_Generic_KeyValuePair_TKey")
System_Collections_Generic_KeyValuePair_TValue = typing.TypeVar("System_Collections_Generic_KeyValuePair_TValue")
System_Collections_Generic_KeyValuePair_Create_TKey = typing.TypeVar("System_Collections_Generic_KeyValuePair_Create_TKey")
System_Collections_Generic_KeyValuePair_Create_TValue = typing.TypeVar("System_Collections_Generic_KeyValuePair_Create_TValue")
System_Collections_Generic_Comparer_T = typing.TypeVar("System_Collections_Generic_Comparer_T")
System_Collections_Generic_GenericComparer_T = typing.TypeVar("System_Collections_Generic_GenericComparer_T")
System_Collections_Generic_NullableComparer_T = typing.TypeVar("System_Collections_Generic_NullableComparer_T")
System_Collections_Generic_ObjectComparer_T = typing.TypeVar("System_Collections_Generic_ObjectComparer_T")
System_Collections_Generic_ISet_T = typing.TypeVar("System_Collections_Generic_ISet_T")
System_Collections_Generic_IReadOnlyList_T = typing.TypeVar("System_Collections_Generic_IReadOnlyList_T")
System_Collections_Generic_IReadOnlyDictionary_TKey = typing.TypeVar("System_Collections_Generic_IReadOnlyDictionary_TKey")
System_Collections_Generic_IReadOnlyDictionary_TValue = typing.TypeVar("System_Collections_Generic_IReadOnlyDictionary_TValue")
System_Collections_Generic_HashSet_T = typing.TypeVar("System_Collections_Generic_HashSet_T")
System_Collections_Generic_IEnumerator_T = typing.TypeVar("System_Collections_Generic_IEnumerator_T")
System_Collections_Generic_IEqualityComparer_T = typing.TypeVar("System_Collections_Generic_IEqualityComparer_T")


class IEnumerator(typing.Generic[System_Collections_Generic_IEnumerator_T], System.IDisposable, System.Collections.IEnumerator, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Current(self) -> System_Collections_Generic_IEnumerator_T:
        ...


class IEnumerable(typing.Generic[System_Collections_Generic_IEnumerable_T], System.Collections.IEnumerable, typing.Iterable[System_Collections_Generic_IEnumerable_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_Generic_IEnumerable_T]:
        ...


class ICollection(typing.Generic[System_Collections_Generic_ICollection_T], System.Collections.Generic.IEnumerable[System_Collections_Generic_ICollection_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Count(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def IsReadOnly(self) -> bool:
        ...

    def Add(self, item: System_Collections_Generic_ICollection_T) -> None:
        ...

    def Clear(self) -> None:
        ...

    def Contains(self, item: System_Collections_Generic_ICollection_T) -> bool:
        ...

    def __contains__(self, item: System_Collections_Generic_ICollection_T) -> bool:
        ...

    def __len__(self) -> int:
        ...

    def CopyTo(self, array: typing.List[System_Collections_Generic_ICollection_T], arrayIndex: int) -> None:
        ...

    def Remove(self, item: System_Collections_Generic_ICollection_T) -> bool:
        ...


class IList(typing.Generic[System_Collections_Generic_IList_T], System.Collections.Generic.ICollection[System_Collections_Generic_IList_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __getitem__(self, index: int) -> System_Collections_Generic_IList_T:
        ...

    def __setitem__(self, index: int, value: System_Collections_Generic_IList_T) -> None:
        ...

    def IndexOf(self, item: System_Collections_Generic_IList_T) -> int:
        ...

    def Insert(self, index: int, item: System_Collections_Generic_IList_T) -> None:
        ...

    def RemoveAt(self, index: int) -> None:
        ...


class IAsyncEnumerator(typing.Generic[System_Collections_Generic_IAsyncEnumerator_T], System.IAsyncDisposable, metaclass=abc.ABCMeta):
    """Supports a simple asynchronous iteration over a generic collection."""

    @property
    @abc.abstractmethod
    def Current(self) -> System_Collections_Generic_IAsyncEnumerator_T:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def MoveNextAsync(self) -> ValueTask:
        """
        Advances the enumerator asynchronously to the next element of the collection.
        
        :returns: A ValueTask{Boolean} that will complete with a result of true if the enumerator was successfully advanced to the next element, or false if the enumerator has passed the end of the collection.
        """
        ...


class IAsyncEnumerable(typing.Generic[System_Collections_Generic_IAsyncEnumerable_T], metaclass=abc.ABCMeta):
    """Exposes an enumerator that provides asynchronous iteration over values of a specified type."""

    def GetAsyncEnumerator(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Collections.Generic.IAsyncEnumerator[System_Collections_Generic_IAsyncEnumerable_T]:
        """
        Returns an enumerator that iterates asynchronously through the collection.
        
        :param cancellationToken: A CancellationToken that may be used to cancel the asynchronous iteration.
        :returns: An enumerator that can be used to iterate asynchronously through the collection.
        """
        ...


class IReadOnlyCollection(typing.Generic[System_Collections_Generic_IReadOnlyCollection_T], System.Collections.Generic.IEnumerable[System_Collections_Generic_IReadOnlyCollection_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Count(self) -> int:
        ...


class IReadOnlySet(typing.Generic[System_Collections_Generic_IReadOnlySet_T], System.Collections.Generic.IReadOnlyCollection[System_Collections_Generic_IReadOnlySet_T], metaclass=abc.ABCMeta):
    """Provides a readonly abstraction of a set."""

    def Contains(self, item: System_Collections_Generic_IReadOnlySet_T) -> bool:
        """
        Determines if the set contains a specific item
        
        :param item: The item to check if the set contains.
        :returns: true if found; otherwise false.
        """
        ...

    def __contains__(self, item: System_Collections_Generic_IReadOnlySet_T) -> bool:
        """
        Determines if the set contains a specific item
        
        :param item: The item to check if the set contains.
        :returns: true if found; otherwise false.
        """
        ...

    def __len__(self) -> int:
        ...

    def IsProperSubsetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_IReadOnlySet_T]) -> bool:
        """
        Determines whether the current set is a proper (strict) subset of a specified collection.
        
        :param other: The collection to compare to the current set.
        :returns: true if the current set is a proper subset of other; otherwise false.
        """
        ...

    def IsProperSupersetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_IReadOnlySet_T]) -> bool:
        """
        Determines whether the current set is a proper (strict) superset of a specified collection.
        
        :param other: The collection to compare to the current set.
        :returns: true if the collection is a proper superset of other; otherwise false.
        """
        ...

    def IsSubsetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_IReadOnlySet_T]) -> bool:
        """
        Determine whether the current set is a subset of a specified collection.
        
        :param other: The collection to compare to the current set.
        :returns: true if the current set is a subset of other; otherwise false.
        """
        ...

    def IsSupersetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_IReadOnlySet_T]) -> bool:
        """
        Determine whether the current set is a super set of a specified collection.
        
        :param other: The collection to compare to the current set
        :returns: true if the current set is a subset of other; otherwise false.
        """
        ...

    def Overlaps(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_IReadOnlySet_T]) -> bool:
        """
        Determines whether the current set overlaps with the specified collection.
        
        :param other: The collection to compare to the current set.
        :returns: trueif the current set and other share at least one common element; otherwise, false.
        """
        ...

    def SetEquals(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_IReadOnlySet_T]) -> bool:
        """
        Determines whether the current set and the specified collection contain the same elements.
        
        :param other: The collection to compare to the current set.
        :returns: true if the current set is equal to other; otherwise, false.
        """
        ...


class IComparer(typing.Generic[System_Collections_Generic_IComparer_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Compare(self, x: System_Collections_Generic_IComparer_T, y: System_Collections_Generic_IComparer_T) -> int:
        ...


class IEqualityComparer(typing.Generic[System_Collections_Generic_IEqualityComparer_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Equals(self, x: System_Collections_Generic_IEqualityComparer_T, y: System_Collections_Generic_IEqualityComparer_T) -> bool:
        ...

    def GetHashCode(self, obj: System_Collections_Generic_IEqualityComparer_T) -> int:
        ...


class NonRandomizedStringEqualityComparer(System.Object, System.Collections.Generic.IEqualityComparer[str], System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    WrappedAroundDefaultComparer: System.Collections.Generic.NonRandomizedStringEqualityComparer = ...

    WrappedAroundStringComparerOrdinal: System.Collections.Generic.NonRandomizedStringEqualityComparer = ...

    WrappedAroundStringComparerOrdinalIgnoreCase: System.Collections.Generic.NonRandomizedStringEqualityComparer = ...

    def __init__(self, information: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...

    def Equals(self, x: str, y: str) -> bool:
        ...

    def GetHashCode(self, obj: str) -> int:
        ...

    def GetUnderlyingEqualityComparer(self) -> System.Collections.Generic.IEqualityComparer[str]:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...


class KeyValuePair(typing.Generic[System_Collections_Generic_KeyValuePair_TKey, System_Collections_Generic_KeyValuePair_TValue]):
    """This class has no documentation."""

    @property
    def Key(self) -> System_Collections_Generic_KeyValuePair_TKey:
        ...

    @property
    def Value(self) -> System_Collections_Generic_KeyValuePair_TValue:
        ...

    @staticmethod
    def Create(key: System_Collections_Generic_KeyValuePair_Create_TKey, value: System_Collections_Generic_KeyValuePair_Create_TValue) -> System.Collections.Generic.KeyValuePair[System_Collections_Generic_KeyValuePair_Create_TKey, System_Collections_Generic_KeyValuePair_Create_TValue]:
        ...

    def __init__(self, key: System_Collections_Generic_KeyValuePair_TKey, value: System_Collections_Generic_KeyValuePair_TValue) -> None:
        ...

    def ToString(self) -> str:
        ...

    def Deconstruct(self, key: System_Collections_Generic_KeyValuePair_TKey, value: System_Collections_Generic_KeyValuePair_TValue) -> None:
        ...


class IDictionary(typing.Generic[System_Collections_Generic_IDictionary_TKey, System_Collections_Generic_IDictionary_TValue], System.Collections.Generic.ICollection[System.Collections.Generic.KeyValuePair[System_Collections_Generic_IDictionary_TKey, System_Collections_Generic_IDictionary_TValue]], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Keys(self) -> System.Collections.Generic.ICollection[System_Collections_Generic_IDictionary_TKey]:
        ...

    @property
    @abc.abstractmethod
    def Values(self) -> System.Collections.Generic.ICollection[System_Collections_Generic_IDictionary_TValue]:
        ...

    def __getitem__(self, key: System_Collections_Generic_IDictionary_TKey) -> System_Collections_Generic_IDictionary_TValue:
        ...

    def __setitem__(self, key: System_Collections_Generic_IDictionary_TKey, value: System_Collections_Generic_IDictionary_TValue) -> None:
        ...

    def ContainsKey(self, key: System_Collections_Generic_IDictionary_TKey) -> bool:
        ...

    def __contains__(self, key: System_Collections_Generic_IDictionary_TKey) -> bool:
        ...

    def __len__(self) -> int:
        ...

    def Add(self, key: System_Collections_Generic_IDictionary_TKey, value: System_Collections_Generic_IDictionary_TValue) -> None:
        ...

    def Remove(self, key: System_Collections_Generic_IDictionary_TKey) -> bool:
        ...

    def TryGetValue(self, key: System_Collections_Generic_IDictionary_TKey, value: System_Collections_Generic_IDictionary_TValue) -> bool:
        ...


class List(typing.Generic[System_Collections_Generic_List_T], System.Object, System.Collections.Generic.IList[System_Collections_Generic_List_T], System.Collections.IList, typing.Iterable[System_Collections_Generic_List_T]):
    """This class has no documentation."""

    class Enumerator(System.Collections.Generic.IEnumerator[System_Collections_Generic_List_T], System.Collections.IEnumerator):
        """This class has no documentation."""

        @property
        def Current(self) -> System_Collections_Generic_List_T:
            ...

        def Dispose(self) -> None:
            ...

        def MoveNext(self) -> bool:
            ...

        def Reset(self) -> None:
            ...

    @property
    def _items(self) -> typing.List[System_Collections_Generic_List_T]:
        ...

    @_items.setter
    def _items(self, value: typing.List[System_Collections_Generic_List_T]):
        ...

    @property
    def _size(self) -> int:
        ...

    @_size.setter
    def _size(self, value: int):
        ...

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
    def __init__(self, collection: System.Collections.Generic.IEnumerable[System_Collections_Generic_List_T]) -> None:
        ...

    @typing.overload
    def __getitem__(self, index: int) -> System_Collections_Generic_List_T:
        ...

    @typing.overload
    def __setitem__(self, index: int, value: System_Collections_Generic_List_T) -> None:
        ...

    @typing.overload
    def __getitem__(self, index: int) -> System.Object:
        ...

    @typing.overload
    def __setitem__(self, index: int, value: System.Object) -> None:
        ...

    @typing.overload
    def Add(self, item: System_Collections_Generic_List_T) -> None:
        ...

    @typing.overload
    def Add(self, item: typing.Any) -> int:
        ...

    def AddRange(self, collection: System.Collections.Generic.IEnumerable[System_Collections_Generic_List_T]) -> None:
        ...

    def AsReadOnly(self) -> System.Collections.ObjectModel.ReadOnlyCollection[System_Collections_Generic_List_T]:
        ...

    @typing.overload
    def BinarySearch(self, index: int, count: int, item: System_Collections_Generic_List_T, comparer: System.Collections.Generic.IComparer[System_Collections_Generic_List_T]) -> int:
        ...

    @typing.overload
    def BinarySearch(self, item: System_Collections_Generic_List_T) -> int:
        ...

    @typing.overload
    def BinarySearch(self, item: System_Collections_Generic_List_T, comparer: System.Collections.Generic.IComparer[System_Collections_Generic_List_T]) -> int:
        ...

    def Clear(self) -> None:
        ...

    @typing.overload
    def Contains(self, item: System_Collections_Generic_List_T) -> bool:
        ...

    @typing.overload
    def __contains__(self, item: System_Collections_Generic_List_T) -> bool:
        ...

    def __len__(self) -> int:
        ...

    @typing.overload
    def Contains(self, item: typing.Any) -> bool:
        ...

    @typing.overload
    def __contains__(self, item: typing.Any) -> bool:
        ...

    def ConvertAll(self, converter: System_Converter) -> System.Collections.Generic.List[System_Collections_Generic_List_ConvertAll_TOutput]:
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[System_Collections_Generic_List_T]) -> None:
        ...

    @typing.overload
    def CopyTo(self, array: System.Array, arrayIndex: int) -> None:
        ...

    @typing.overload
    def CopyTo(self, index: int, array: typing.List[System_Collections_Generic_List_T], arrayIndex: int, count: int) -> None:
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[System_Collections_Generic_List_T], arrayIndex: int) -> None:
        ...

    def EnsureCapacity(self, capacity: int) -> int:
        """
        Ensures that the capacity of this list is at least the specified .
        If the current capacity of the list is less than specified ,
        the capacity is increased by continuously twice current capacity until it is at least the specified .
        
        :param capacity: The minimum capacity to ensure.
        """
        ...

    def Exists(self, match: System_Predicate) -> bool:
        ...

    def Find(self, match: System_Predicate) -> System_Collections_Generic_List_T:
        ...

    def FindAll(self, match: System_Predicate) -> System.Collections.Generic.List[System_Collections_Generic_List_T]:
        ...

    @typing.overload
    def FindIndex(self, match: System_Predicate) -> int:
        ...

    @typing.overload
    def FindIndex(self, startIndex: int, match: System_Predicate) -> int:
        ...

    @typing.overload
    def FindIndex(self, startIndex: int, count: int, match: System_Predicate) -> int:
        ...

    def FindLast(self, match: System_Predicate) -> System_Collections_Generic_List_T:
        ...

    @typing.overload
    def FindLastIndex(self, match: System_Predicate) -> int:
        ...

    @typing.overload
    def FindLastIndex(self, startIndex: int, match: System_Predicate) -> int:
        ...

    @typing.overload
    def FindLastIndex(self, startIndex: int, count: int, match: System_Predicate) -> int:
        ...

    def ForEach(self, action: typing.Callable[[System_Collections_Generic_List_T], None]) -> None:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.List.Enumerator:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_Generic_List_T]:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    def GetRange(self, index: int, count: int) -> System.Collections.Generic.List[System_Collections_Generic_List_T]:
        ...

    @typing.overload
    def IndexOf(self, item: System_Collections_Generic_List_T) -> int:
        ...

    @typing.overload
    def IndexOf(self, item: typing.Any) -> int:
        ...

    @typing.overload
    def IndexOf(self, item: System_Collections_Generic_List_T, index: int) -> int:
        ...

    @typing.overload
    def IndexOf(self, item: System_Collections_Generic_List_T, index: int, count: int) -> int:
        ...

    @typing.overload
    def Insert(self, index: int, item: System_Collections_Generic_List_T) -> None:
        ...

    @typing.overload
    def Insert(self, index: int, item: typing.Any) -> None:
        ...

    def InsertRange(self, index: int, collection: System.Collections.Generic.IEnumerable[System_Collections_Generic_List_T]) -> None:
        ...

    @typing.overload
    def LastIndexOf(self, item: System_Collections_Generic_List_T) -> int:
        ...

    @typing.overload
    def LastIndexOf(self, item: System_Collections_Generic_List_T, index: int) -> int:
        ...

    @typing.overload
    def LastIndexOf(self, item: System_Collections_Generic_List_T, index: int, count: int) -> int:
        ...

    @typing.overload
    def Remove(self, item: System_Collections_Generic_List_T) -> bool:
        ...

    @typing.overload
    def Remove(self, item: typing.Any) -> None:
        ...

    def RemoveAll(self, match: System_Predicate) -> int:
        ...

    def RemoveAt(self, index: int) -> None:
        ...

    def RemoveRange(self, index: int, count: int) -> None:
        ...

    @typing.overload
    def Reverse(self) -> None:
        ...

    @typing.overload
    def Reverse(self, index: int, count: int) -> None:
        ...

    @typing.overload
    def Sort(self) -> None:
        ...

    @typing.overload
    def Sort(self, comparer: System.Collections.Generic.IComparer[System_Collections_Generic_List_T]) -> None:
        ...

    @typing.overload
    def Sort(self, index: int, count: int, comparer: System.Collections.Generic.IComparer[System_Collections_Generic_List_T]) -> None:
        ...

    @typing.overload
    def Sort(self, comparison: System_Comparison) -> None:
        ...

    def ToArray(self) -> typing.List[System_Collections_Generic_List_T]:
        ...

    def TrimExcess(self) -> None:
        ...

    def TrueForAll(self, match: System_Predicate) -> bool:
        ...


class EqualityComparer(typing.Generic[System_Collections_Generic_EqualityComparer_T], System.Object, System.Collections.Generic.IEqualityComparer[System_Collections_Generic_EqualityComparer_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    Default: System.Collections.Generic.EqualityComparer[System_Collections_Generic_EqualityComparer_T]

    @typing.overload
    def Equals(self, x: System_Collections_Generic_EqualityComparer_T, y: System_Collections_Generic_EqualityComparer_T) -> bool:
        ...

    @typing.overload
    def GetHashCode(self, obj: System_Collections_Generic_EqualityComparer_T) -> int:
        ...

    @typing.overload
    def GetHashCode(self, obj: typing.Any) -> int:
        ...

    @typing.overload
    def Equals(self, x: typing.Any, y: typing.Any) -> bool:
        ...


class GenericEqualityComparer(typing.Generic[System_Collections_Generic_GenericEqualityComparer_T], System.Collections.Generic.EqualityComparer[System_Collections_Generic_GenericEqualityComparer_T]):
    """This class has no documentation."""

    @typing.overload
    def Equals(self, x: System_Collections_Generic_GenericEqualityComparer_T, y: System_Collections_Generic_GenericEqualityComparer_T) -> bool:
        ...

    @typing.overload
    def GetHashCode(self, obj: System_Collections_Generic_GenericEqualityComparer_T) -> int:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def GetHashCode(self) -> int:
        ...


class NullableEqualityComparer(typing.Generic[System_Collections_Generic_NullableEqualityComparer_T], System.Collections.Generic.EqualityComparer[typing.Optional[System_Collections_Generic_NullableEqualityComparer_T]]):
    """This class has no documentation."""

    @typing.overload
    def Equals(self, x: typing.Optional[System_Collections_Generic_NullableEqualityComparer_T], y: typing.Optional[System_Collections_Generic_NullableEqualityComparer_T]) -> bool:
        ...

    @typing.overload
    def GetHashCode(self, obj: typing.Optional[System_Collections_Generic_NullableEqualityComparer_T]) -> int:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def GetHashCode(self) -> int:
        ...


class ObjectEqualityComparer(typing.Generic[System_Collections_Generic_ObjectEqualityComparer_T], System.Collections.Generic.EqualityComparer[System_Collections_Generic_ObjectEqualityComparer_T]):
    """This class has no documentation."""

    @typing.overload
    def Equals(self, x: System_Collections_Generic_ObjectEqualityComparer_T, y: System_Collections_Generic_ObjectEqualityComparer_T) -> bool:
        ...

    @typing.overload
    def GetHashCode(self, obj: System_Collections_Generic_ObjectEqualityComparer_T) -> int:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def GetHashCode(self) -> int:
        ...


class ByteEqualityComparer(System.Collections.Generic.EqualityComparer[int]):
    """This class has no documentation."""

    @typing.overload
    def Equals(self, x: int, y: int) -> bool:
        ...

    @typing.overload
    def GetHashCode(self, b: int) -> int:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def GetHashCode(self) -> int:
        ...


class EnumEqualityComparer(typing.Generic[System_Collections_Generic_EnumEqualityComparer_T], System.Collections.Generic.EqualityComparer[System_Collections_Generic_EnumEqualityComparer_T], System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    @typing.overload
    def GetHashCode(self, obj: System_Collections_Generic_EnumEqualityComparer_T) -> int:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def GetHashCode(self) -> int:
        ...

    @typing.overload
    def Equals(self, x: System_Collections_Generic_EnumEqualityComparer_T, y: System_Collections_Generic_EnumEqualityComparer_T) -> bool:
        ...


class Dictionary(typing.Generic[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue], System.Object, System.Collections.Generic.IDictionary[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue], System.Collections.IDictionary, System.Runtime.Serialization.ISerializable, System.Runtime.Serialization.IDeserializationCallback, typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]]):
    """This class has no documentation."""

    class Enumerator(System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]], System.Collections.IDictionaryEnumerator):
        """This class has no documentation."""

        DictEntry: int = 1

        KeyValuePair: int = 2

        @property
        def Current(self) -> System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]:
            ...

        @property
        def Entry(self) -> System.Collections.DictionaryEntry:
            ...

        @property
        def Key(self) -> System.Object:
            ...

        @property
        def Value(self) -> System.Object:
            ...

        def MoveNext(self) -> bool:
            ...

        def Dispose(self) -> None:
            ...

        def Reset(self) -> None:
            ...

    class KeyCollection(System.Object, System.Collections.Generic.ICollection[System_Collections_Generic_Dictionary_TKey], System.Collections.ICollection, typing.Iterable[System_Collections_Generic_Dictionary_TKey]):
        """This class has no documentation."""

        class Enumerator(System.Collections.Generic.IEnumerator[System_Collections_Generic_Dictionary_TKey], System.Collections.IEnumerator):
            """This class has no documentation."""

            @property
            def Current(self) -> System_Collections_Generic_Dictionary_TKey:
                ...

            def Dispose(self) -> None:
                ...

            def MoveNext(self) -> bool:
                ...

            def Reset(self) -> None:
                ...

        @property
        def Count(self) -> int:
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

        def __init__(self, dictionary: System.Collections.Generic.Dictionary[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]) -> None:
            ...

        @typing.overload
        def GetEnumerator(self) -> System.Collections.Generic.Dictionary.KeyCollection.Enumerator:
            ...

        @typing.overload
        def CopyTo(self, array: typing.List[System_Collections_Generic_Dictionary_TKey], index: int) -> None:
            ...

        def Add(self, item: System_Collections_Generic_Dictionary_TKey) -> None:
            ...

        def Clear(self) -> None:
            ...

        def Contains(self, item: System_Collections_Generic_Dictionary_TKey) -> bool:
            ...

        def __contains__(self, item: System_Collections_Generic_Dictionary_TKey) -> bool:
            ...

        def __len__(self) -> int:
            ...

        def Remove(self, item: System_Collections_Generic_Dictionary_TKey) -> bool:
            ...

        @typing.overload
        def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_Generic_Dictionary_TKey]:
            ...

        @typing.overload
        def GetEnumerator(self) -> System.Collections.IEnumerator:
            ...

        @typing.overload
        def CopyTo(self, array: System.Array, index: int) -> None:
            ...

    class ValueCollection(System.Object, System.Collections.Generic.ICollection[System_Collections_Generic_Dictionary_TValue], System.Collections.ICollection, typing.Iterable[System_Collections_Generic_Dictionary_TValue]):
        """This class has no documentation."""

        class Enumerator(System.Collections.Generic.IEnumerator[System_Collections_Generic_Dictionary_TValue], System.Collections.IEnumerator):
            """This class has no documentation."""

            @property
            def Current(self) -> System_Collections_Generic_Dictionary_TValue:
                ...

            def Dispose(self) -> None:
                ...

            def MoveNext(self) -> bool:
                ...

            def Reset(self) -> None:
                ...

        @property
        def Count(self) -> int:
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

        def __init__(self, dictionary: System.Collections.Generic.Dictionary[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]) -> None:
            ...

        @typing.overload
        def GetEnumerator(self) -> System.Collections.Generic.Dictionary.ValueCollection.Enumerator:
            ...

        @typing.overload
        def CopyTo(self, array: typing.List[System_Collections_Generic_Dictionary_TValue], index: int) -> None:
            ...

        def Add(self, item: System_Collections_Generic_Dictionary_TValue) -> None:
            ...

        def Remove(self, item: System_Collections_Generic_Dictionary_TValue) -> bool:
            ...

        def Clear(self) -> None:
            ...

        def Contains(self, item: System_Collections_Generic_Dictionary_TValue) -> bool:
            ...

        def __contains__(self, item: System_Collections_Generic_Dictionary_TValue) -> bool:
            ...

        def __len__(self) -> int:
            ...

        @typing.overload
        def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_Generic_Dictionary_TValue]:
            ...

        @typing.overload
        def GetEnumerator(self) -> System.Collections.IEnumerator:
            ...

        @typing.overload
        def CopyTo(self, array: System.Array, index: int) -> None:
            ...

    @property
    def Comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Generic_Dictionary_TKey]:
        ...

    @property
    def Count(self) -> int:
        ...

    @property
    def Keys(self) -> System.Collections.Generic.Dictionary.KeyCollection:
        ...

    @property
    def Values(self) -> System.Collections.Generic.Dictionary.ValueCollection:
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

    @property
    def IsFixedSize(self) -> bool:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int) -> None:
        ...

    @typing.overload
    def __init__(self, comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Generic_Dictionary_TKey]) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int, comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Generic_Dictionary_TKey]) -> None:
        ...

    @typing.overload
    def __init__(self, dictionary: System.Collections.Generic.IDictionary[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]) -> None:
        ...

    @typing.overload
    def __init__(self, dictionary: System.Collections.Generic.IDictionary[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Generic_Dictionary_TKey]) -> None:
        ...

    @typing.overload
    def __init__(self, collection: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]]) -> None:
        ...

    @typing.overload
    def __init__(self, collection: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Generic_Dictionary_TKey]) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __getitem__(self, key: System_Collections_Generic_Dictionary_TKey) -> System_Collections_Generic_Dictionary_TValue:
        ...

    @typing.overload
    def __setitem__(self, key: System_Collections_Generic_Dictionary_TKey, value: System_Collections_Generic_Dictionary_TValue) -> None:
        ...

    @typing.overload
    def Add(self, key: System_Collections_Generic_Dictionary_TKey, value: System_Collections_Generic_Dictionary_TValue) -> None:
        ...

    @typing.overload
    def Add(self, keyValuePair: System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]) -> None:
        ...

    @typing.overload
    def Contains(self, keyValuePair: System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]) -> bool:
        ...

    @typing.overload
    def __contains__(self, keyValuePair: System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]) -> bool:
        ...

    def __len__(self) -> int:
        ...

    @typing.overload
    def Remove(self, keyValuePair: System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]) -> bool:
        ...

    def Clear(self) -> None:
        ...

    def ContainsKey(self, key: System_Collections_Generic_Dictionary_TKey) -> bool:
        ...

    @typing.overload
    def __contains__(self, key: System_Collections_Generic_Dictionary_TKey) -> bool:
        ...

    def ContainsValue(self, value: System_Collections_Generic_Dictionary_TValue) -> bool:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.Dictionary.Enumerator:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]]:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def OnDeserialization(self, sender: typing.Any) -> None:
        ...

    @typing.overload
    def Remove(self, key: System_Collections_Generic_Dictionary_TKey) -> bool:
        ...

    @typing.overload
    def Remove(self, key: System_Collections_Generic_Dictionary_TKey, value: System_Collections_Generic_Dictionary_TValue) -> bool:
        ...

    def TryGetValue(self, key: System_Collections_Generic_Dictionary_TKey, value: System_Collections_Generic_Dictionary_TValue) -> bool:
        ...

    def TryAdd(self, key: System_Collections_Generic_Dictionary_TKey, value: System_Collections_Generic_Dictionary_TValue) -> bool:
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[System.Collections.Generic.KeyValuePair[System_Collections_Generic_Dictionary_TKey, System_Collections_Generic_Dictionary_TValue]], index: int) -> None:
        ...

    @typing.overload
    def CopyTo(self, array: System.Array, index: int) -> None:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    def EnsureCapacity(self, capacity: int) -> int:
        """Ensures that the dictionary can hold up to 'capacity' entries without any further expansion of its backing storage"""
        ...

    @typing.overload
    def TrimExcess(self) -> None:
        """Sets the capacity of this dictionary to what it would be if it had been originally initialized with all its entries"""
        ...

    @typing.overload
    def TrimExcess(self, capacity: int) -> None:
        """Sets the capacity of this dictionary to hold up 'capacity' entries without any further expansion of its backing storage"""
        ...

    @typing.overload
    def __getitem__(self, key: typing.Any) -> System.Object:
        ...

    @typing.overload
    def __setitem__(self, key: typing.Any, value: System.Object) -> None:
        ...

    @typing.overload
    def Add(self, key: typing.Any, value: typing.Any) -> None:
        ...

    @typing.overload
    def Contains(self, key: typing.Any) -> bool:
        ...

    @typing.overload
    def __contains__(self, key: typing.Any) -> bool:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...

    @typing.overload
    def Remove(self, key: typing.Any) -> None:
        ...


class Comparer(typing.Generic[System_Collections_Generic_Comparer_T], System.Object, System.Collections.Generic.IComparer[System_Collections_Generic_Comparer_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    Default: System.Collections.Generic.Comparer[System_Collections_Generic_Comparer_T]

    @staticmethod
    def Create(comparison: System_Comparison) -> System.Collections.Generic.Comparer[System_Collections_Generic_Comparer_T]:
        ...

    @typing.overload
    def Compare(self, x: System_Collections_Generic_Comparer_T, y: System_Collections_Generic_Comparer_T) -> int:
        ...

    @typing.overload
    def Compare(self, x: typing.Any, y: typing.Any) -> int:
        ...


class GenericComparer(typing.Generic[System_Collections_Generic_GenericComparer_T], System.Collections.Generic.Comparer[System_Collections_Generic_GenericComparer_T]):
    """This class has no documentation."""

    def Compare(self, x: System_Collections_Generic_GenericComparer_T, y: System_Collections_Generic_GenericComparer_T) -> int:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class NullableComparer(typing.Generic[System_Collections_Generic_NullableComparer_T], System.Collections.Generic.Comparer[typing.Optional[System_Collections_Generic_NullableComparer_T]]):
    """This class has no documentation."""

    def Compare(self, x: typing.Optional[System_Collections_Generic_NullableComparer_T], y: typing.Optional[System_Collections_Generic_NullableComparer_T]) -> int:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class ObjectComparer(typing.Generic[System_Collections_Generic_ObjectComparer_T], System.Collections.Generic.Comparer[System_Collections_Generic_ObjectComparer_T]):
    """This class has no documentation."""

    def Compare(self, x: System_Collections_Generic_ObjectComparer_T, y: System_Collections_Generic_ObjectComparer_T) -> int:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class ISet(typing.Generic[System_Collections_Generic_ISet_T], System.Collections.Generic.ICollection[System_Collections_Generic_ISet_T], metaclass=abc.ABCMeta):
    """
    Generic collection that guarantees the uniqueness of its elements, as defined
    by some comparer. It also supports basic set operations such as Union, Intersection,
    Complement and Exclusive Complement.
    """

    def Add(self, item: System_Collections_Generic_ISet_T) -> bool:
        ...

    def UnionWith(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_ISet_T]) -> None:
        ...

    def IntersectWith(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_ISet_T]) -> None:
        ...

    def ExceptWith(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_ISet_T]) -> None:
        ...

    def SymmetricExceptWith(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_ISet_T]) -> None:
        ...

    def IsSubsetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_ISet_T]) -> bool:
        ...

    def IsSupersetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_ISet_T]) -> bool:
        ...

    def IsProperSupersetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_ISet_T]) -> bool:
        ...

    def IsProperSubsetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_ISet_T]) -> bool:
        ...

    def Overlaps(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_ISet_T]) -> bool:
        ...

    def SetEquals(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_ISet_T]) -> bool:
        ...


class IReadOnlyList(typing.Generic[System_Collections_Generic_IReadOnlyList_T], System.Collections.Generic.IReadOnlyCollection[System_Collections_Generic_IReadOnlyList_T], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __getitem__(self, index: int) -> System_Collections_Generic_IReadOnlyList_T:
        ...


class IReadOnlyDictionary(typing.Generic[System_Collections_Generic_IReadOnlyDictionary_TKey, System_Collections_Generic_IReadOnlyDictionary_TValue], System.Collections.Generic.IReadOnlyCollection[System.Collections.Generic.KeyValuePair[System_Collections_Generic_IReadOnlyDictionary_TKey, System_Collections_Generic_IReadOnlyDictionary_TValue]], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Keys(self) -> System.Collections.Generic.IEnumerable[System_Collections_Generic_IReadOnlyDictionary_TKey]:
        ...

    @property
    @abc.abstractmethod
    def Values(self) -> System.Collections.Generic.IEnumerable[System_Collections_Generic_IReadOnlyDictionary_TValue]:
        ...

    def ContainsKey(self, key: System_Collections_Generic_IReadOnlyDictionary_TKey) -> bool:
        ...

    def __contains__(self, key: System_Collections_Generic_IReadOnlyDictionary_TKey) -> bool:
        ...

    def __len__(self) -> int:
        ...

    def TryGetValue(self, key: System_Collections_Generic_IReadOnlyDictionary_TKey, value: System_Collections_Generic_IReadOnlyDictionary_TValue) -> bool:
        ...

    def __getitem__(self, key: System_Collections_Generic_IReadOnlyDictionary_TKey) -> System_Collections_Generic_IReadOnlyDictionary_TValue:
        ...


class HashSet(typing.Generic[System_Collections_Generic_HashSet_T], System.Object, System.Collections.Generic.ICollection[System_Collections_Generic_HashSet_T], System.Runtime.Serialization.ISerializable, System.Runtime.Serialization.IDeserializationCallback, typing.Iterable[System_Collections_Generic_HashSet_T]):
    """This class has no documentation."""

    class Enumerator(System.Collections.Generic.IEnumerator[System_Collections_Generic_HashSet_T]):
        """This class has no documentation."""

        @property
        def Current(self) -> System_Collections_Generic_HashSet_T:
            ...

        def MoveNext(self) -> bool:
            ...

        def Dispose(self) -> None:
            ...

        def Reset(self) -> None:
            ...

    @property
    def Count(self) -> int:
        """Gets the number of elements that are contained in the set."""
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def Comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Generic_HashSet_T]:
        """Gets the IEqualityComparer object that is used to determine equality for the values in the set."""
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Generic_HashSet_T]) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int) -> None:
        ...

    @typing.overload
    def __init__(self, collection: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> None:
        ...

    @typing.overload
    def __init__(self, collection: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Generic_HashSet_T]) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int, comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Generic_HashSet_T]) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def Add(self, item: System_Collections_Generic_HashSet_T) -> None:
        ...

    def Clear(self) -> None:
        """Removes all elements from the HashSet{T} object."""
        ...

    def Contains(self, item: System_Collections_Generic_HashSet_T) -> bool:
        """
        Determines whether the HashSet{T} contains the specified element.
        
        :param item: The element to locate in the HashSet{T} object.
        :returns: true if the HashSet{T} object contains the specified element; otherwise, false.
        """
        ...

    def __contains__(self, item: System_Collections_Generic_HashSet_T) -> bool:
        """
        Determines whether the HashSet{T} contains the specified element.
        
        :param item: The element to locate in the HashSet{T} object.
        :returns: true if the HashSet{T} object contains the specified element; otherwise, false.
        """
        ...

    def __len__(self) -> int:
        ...

    def Remove(self, item: System_Collections_Generic_HashSet_T) -> bool:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.HashSet.Enumerator:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_Generic_HashSet_T]:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def OnDeserialization(self, sender: typing.Any) -> None:
        ...

    @typing.overload
    def Add(self, item: System_Collections_Generic_HashSet_T) -> bool:
        ...

    def TryGetValue(self, equalValue: System_Collections_Generic_HashSet_T, actualValue: System_Collections_Generic_HashSet_T) -> bool:
        """
        Searches the set for a given value and returns the equal value it finds, if any.
        
        :param equalValue: The value to search for.
        :param actualValue: The value from the set that the search found, or the default value of T when the search yielded no match.
        :returns: A value indicating whether the search was successful.
        """
        ...

    def UnionWith(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> None:
        """
        Modifies the current HashSet{T} object to contain all elements that are present in itself, the specified collection, or both.
        
        :param other: The collection to compare to the current HashSet{T} object.
        """
        ...

    def IntersectWith(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> None:
        """
        Modifies the current HashSet{T} object to contain only elements that are present in that object and in the specified collection.
        
        :param other: The collection to compare to the current HashSet{T} object.
        """
        ...

    def ExceptWith(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> None:
        """
        Removes all elements in the specified collection from the current HashSet{T} object.
        
        :param other: The collection to compare to the current HashSet{T} object.
        """
        ...

    def SymmetricExceptWith(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> None:
        """
        Modifies the current HashSet{T} object to contain only elements that are present either in that object or in the specified collection, but not both.
        
        :param other: The collection to compare to the current HashSet{T} object.
        """
        ...

    def IsSubsetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> bool:
        """
        Determines whether a HashSet{T} object is a subset of the specified collection.
        
        :param other: The collection to compare to the current HashSet{T} object.
        :returns: true if the HashSet{T} object is a subset of ; otherwise, false.
        """
        ...

    def IsProperSubsetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> bool:
        """
        Determines whether a HashSet{T} object is a proper subset of the specified collection.
        
        :param other: The collection to compare to the current HashSet{T} object.
        :returns: true if the HashSet{T} object is a proper subset of ; otherwise, false.
        """
        ...

    def IsSupersetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> bool:
        """
        Determines whether a HashSet{T} object is a proper superset of the specified collection.
        
        :param other: The collection to compare to the current HashSet{T} object.
        :returns: true if the HashSet{T} object is a superset of ; otherwise, false.
        """
        ...

    def IsProperSupersetOf(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> bool:
        """
        Determines whether a HashSet{T} object is a proper superset of the specified collection.
        
        :param other: The collection to compare to the current HashSet{T} object.
        :returns: true if the HashSet{T} object is a proper superset of ; otherwise, false.
        """
        ...

    def Overlaps(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> bool:
        """
        Determines whether the current HashSet{T} object and a specified collection share common elements.
        
        :param other: The collection to compare to the current HashSet{T} object.
        :returns: true if the HashSet{T} object and  share at least one common element; otherwise, false.
        """
        ...

    def SetEquals(self, other: System.Collections.Generic.IEnumerable[System_Collections_Generic_HashSet_T]) -> bool:
        """
        Determines whether a HashSet{T} object and the specified collection contain the same elements.
        
        :param other: The collection to compare to the current HashSet{T} object.
        :returns: true if the HashSet{T} object is equal to ; otherwise, false.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[System_Collections_Generic_HashSet_T]) -> None:
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[System_Collections_Generic_HashSet_T], arrayIndex: int) -> None:
        """
        Copies the elements of a HashSet{T} object to an array, starting at the specified array index.
        
        :param array: The destination array.
        :param arrayIndex: The zero-based index in array at which copying begins.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[System_Collections_Generic_HashSet_T], arrayIndex: int, count: int) -> None:
        ...

    def RemoveWhere(self, match: System_Predicate) -> int:
        """Removes all elements that match the conditions defined by the specified predicate from a HashSet{T} collection."""
        ...

    def EnsureCapacity(self, capacity: int) -> int:
        """Ensures that this hash set can hold the specified number of elements without growing."""
        ...

    def TrimExcess(self) -> None:
        """
        Sets the capacity of a HashSet{T} object to the actual number of elements it contains,
        rounded up to a nearby, implementation-specific value.
        """
        ...

    @staticmethod
    def CreateSetComparer() -> System.Collections.Generic.IEqualityComparer[System.Collections.Generic.HashSet[System_Collections_Generic_HashSet_T]]:
        ...


class KeyNotFoundException(System.SystemException):
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


