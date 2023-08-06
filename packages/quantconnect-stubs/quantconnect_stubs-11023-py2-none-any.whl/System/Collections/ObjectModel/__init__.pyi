import typing

import System
import System.Collections
import System.Collections.Generic
import System.Collections.ObjectModel

System_Collections_ObjectModel_ReadOnlyCollection_T = typing.TypeVar("System_Collections_ObjectModel_ReadOnlyCollection_T")
System_Collections_ObjectModel_Collection_T = typing.TypeVar("System_Collections_ObjectModel_Collection_T")


class ReadOnlyCollection(typing.Generic[System_Collections_ObjectModel_ReadOnlyCollection_T], System.Object, System.Collections.Generic.IList[System_Collections_ObjectModel_ReadOnlyCollection_T], System.Collections.IList, typing.Iterable[System_Collections_ObjectModel_ReadOnlyCollection_T]):
    """This class has no documentation."""

    @property
    def Count(self) -> int:
        ...

    @property
    def Items(self) -> System.Collections.Generic.IList[System_Collections_ObjectModel_ReadOnlyCollection_T]:
        """This property is protected."""
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

    def __init__(self, list: System.Collections.Generic.IList[System_Collections_ObjectModel_ReadOnlyCollection_T]) -> None:
        ...

    @typing.overload
    def __getitem__(self, index: int) -> System_Collections_ObjectModel_ReadOnlyCollection_T:
        ...

    @typing.overload
    def Contains(self, value: System_Collections_ObjectModel_ReadOnlyCollection_T) -> bool:
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[System_Collections_ObjectModel_ReadOnlyCollection_T], index: int) -> None:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_ObjectModel_ReadOnlyCollection_T]:
        ...

    @typing.overload
    def IndexOf(self, value: System_Collections_ObjectModel_ReadOnlyCollection_T) -> int:
        ...

    @typing.overload
    def __getitem__(self, index: int) -> System_Collections_ObjectModel_ReadOnlyCollection_T:
        ...

    @typing.overload
    def __setitem__(self, index: int, value: System_Collections_ObjectModel_ReadOnlyCollection_T) -> None:
        ...

    @typing.overload
    def Add(self, value: System_Collections_ObjectModel_ReadOnlyCollection_T) -> None:
        ...

    @typing.overload
    def Clear(self) -> None:
        ...

    @typing.overload
    def Insert(self, index: int, value: System_Collections_ObjectModel_ReadOnlyCollection_T) -> None:
        ...

    @typing.overload
    def Remove(self, value: System_Collections_ObjectModel_ReadOnlyCollection_T) -> bool:
        ...

    @typing.overload
    def RemoveAt(self, index: int) -> None:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    @typing.overload
    def CopyTo(self, array: System.Array, index: int) -> None:
        ...

    @typing.overload
    def __getitem__(self, index: int) -> System.Object:
        ...

    @typing.overload
    def __setitem__(self, index: int, value: System.Object) -> None:
        ...

    @typing.overload
    def Add(self, value: typing.Any) -> int:
        ...

    @typing.overload
    def Clear(self) -> None:
        ...

    @typing.overload
    def Contains(self, value: typing.Any) -> bool:
        ...

    @typing.overload
    def IndexOf(self, value: typing.Any) -> int:
        ...

    @typing.overload
    def Insert(self, index: int, value: typing.Any) -> None:
        ...

    @typing.overload
    def Remove(self, value: typing.Any) -> None:
        ...

    @typing.overload
    def RemoveAt(self, index: int) -> None:
        ...


class Collection(typing.Generic[System_Collections_ObjectModel_Collection_T], System.Object, System.Collections.Generic.IList[System_Collections_ObjectModel_Collection_T], System.Collections.IList, typing.Iterable[System_Collections_ObjectModel_Collection_T]):
    """This class has no documentation."""

    @property
    def Count(self) -> int:
        ...

    @property
    def Items(self) -> System.Collections.Generic.IList[System_Collections_ObjectModel_Collection_T]:
        """This property is protected."""
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
    def __init__(self, list: System.Collections.Generic.IList[System_Collections_ObjectModel_Collection_T]) -> None:
        ...

    @typing.overload
    def __getitem__(self, index: int) -> System_Collections_ObjectModel_Collection_T:
        ...

    @typing.overload
    def __setitem__(self, index: int, value: System_Collections_ObjectModel_Collection_T) -> None:
        ...

    @typing.overload
    def Add(self, item: System_Collections_ObjectModel_Collection_T) -> None:
        ...

    def Clear(self) -> None:
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[System_Collections_ObjectModel_Collection_T], index: int) -> None:
        ...

    @typing.overload
    def Contains(self, item: System_Collections_ObjectModel_Collection_T) -> bool:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_ObjectModel_Collection_T]:
        ...

    @typing.overload
    def IndexOf(self, item: System_Collections_ObjectModel_Collection_T) -> int:
        ...

    @typing.overload
    def Insert(self, index: int, item: System_Collections_ObjectModel_Collection_T) -> None:
        ...

    @typing.overload
    def Remove(self, item: System_Collections_ObjectModel_Collection_T) -> bool:
        ...

    def RemoveAt(self, index: int) -> None:
        ...

    def ClearItems(self) -> None:
        """This method is protected."""
        ...

    def InsertItem(self, index: int, item: System_Collections_ObjectModel_Collection_T) -> None:
        """This method is protected."""
        ...

    def RemoveItem(self, index: int) -> None:
        """This method is protected."""
        ...

    def SetItem(self, index: int, item: System_Collections_ObjectModel_Collection_T) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    @typing.overload
    def CopyTo(self, array: System.Array, index: int) -> None:
        ...

    @typing.overload
    def __getitem__(self, index: int) -> System.Object:
        ...

    @typing.overload
    def __setitem__(self, index: int, value: System.Object) -> None:
        ...

    @typing.overload
    def Add(self, value: typing.Any) -> int:
        ...

    @typing.overload
    def Contains(self, value: typing.Any) -> bool:
        ...

    @typing.overload
    def IndexOf(self, value: typing.Any) -> int:
        ...

    @typing.overload
    def Insert(self, index: int, value: typing.Any) -> None:
        ...

    @typing.overload
    def Remove(self, value: typing.Any) -> None:
        ...


