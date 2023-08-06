import abc
import typing

import System
import System.Collections
import System.Collections.Concurrent
import System.Collections.Generic

System_Collections_Concurrent_IProducerConsumerCollection_T = typing.TypeVar("System_Collections_Concurrent_IProducerConsumerCollection_T")
System_Collections_Concurrent_ConcurrentQueue_T = typing.TypeVar("System_Collections_Concurrent_ConcurrentQueue_T")


class IProducerConsumerCollection(typing.Generic[System_Collections_Concurrent_IProducerConsumerCollection_T], System.Collections.Generic.IEnumerable[System_Collections_Concurrent_IProducerConsumerCollection_T], System.Collections.ICollection, metaclass=abc.ABCMeta):
    """
    A common interface for all concurrent collections.
    Defines methods to manipulate thread-safe collections intended for producer/consumer usage.
    """

    def CopyTo(self, array: typing.List[System_Collections_Concurrent_IProducerConsumerCollection_T], index: int) -> None:
        """
        Copies the elements of the IProducerConsumerCollection{T} to
        an
        System.Array, starting at a specified index.
        
        :param array: The one-dimensional System.Array that is the destination of the elements copied from the IProducerConsumerCollection{T}. The array must have zero-based indexing.
        :param index: The zero-based index in  at which copying begins.
        """
        ...

    def TryAdd(self, item: System_Collections_Concurrent_IProducerConsumerCollection_T) -> bool:
        """
        Attempts to add an object to the IProducerConsumerCollection{T}.
        
        :param item: The object to add to the IProducerConsumerCollection{T}.
        :returns: true if the object was added successfully; otherwise, false.
        """
        ...

    def TryTake(self, item: System_Collections_Concurrent_IProducerConsumerCollection_T) -> bool:
        """
        Attempts to remove and return an object from the IProducerConsumerCollection{T}.
        
        :param item: When this method returns, if the object was removed and returned successfully,  contains the removed object. If no object was available to be removed, the value is unspecified.
        :returns: true if an object was removed and returned successfully; otherwise, false.
        """
        ...

    def ToArray(self) -> typing.List[System_Collections_Concurrent_IProducerConsumerCollection_T]:
        """
        Copies the elements contained in the IProducerConsumerCollection{T} to a new array.
        
        :returns: A new array containing the elements copied from the IProducerConsumerCollection{T}.
        """
        ...


class ConcurrentQueue(typing.Generic[System_Collections_Concurrent_ConcurrentQueue_T], System.Object, System.Collections.Concurrent.IProducerConsumerCollection[System_Collections_Concurrent_ConcurrentQueue_T], System.Collections.Generic.IReadOnlyCollection[System_Collections_Concurrent_ConcurrentQueue_T], typing.Iterable[System_Collections_Concurrent_ConcurrentQueue_T]):
    """Represents a thread-safe first-in, first-out collection of objects."""

    @property
    def IsSynchronized(self) -> bool:
        """
        Gets a value indicating whether access to the ICollection is
        synchronized with the SyncRoot.
        """
        ...

    @property
    def SyncRoot(self) -> System.Object:
        """Gets an object that can be used to synchronize access to the ICollection. This property is not supported."""
        ...

    @property
    def IsEmpty(self) -> bool:
        """Gets a value that indicates whether the ConcurrentQueue{T} is empty."""
        ...

    @property
    def Count(self) -> int:
        """Gets the number of elements contained in the ConcurrentQueue{T}."""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Initializes a new instance of the ConcurrentQueue{T} class."""
        ...

    @typing.overload
    def __init__(self, collection: System.Collections.Generic.IEnumerable[System_Collections_Concurrent_ConcurrentQueue_T]) -> None:
        """
        Initializes a new instance of the ConcurrentQueue{T} class that contains elements copied
        from the specified collection.
        
        :param collection: The collection whose elements are copied to the new ConcurrentQueue{T}.
        """
        ...

    @typing.overload
    def CopyTo(self, array: System.Array, index: int) -> None:
        """
        Copies the elements of the ICollection to an Array, starting at a particular Array index.
        
        :param array: The one-dimensional Array that is the destination of the elements copied from the ConcurrentQueue{T}.  must have zero-based indexing.
        :param index: The zero-based index in  at which copying begins.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Returns an enumerator that iterates through a collection.
        
        :returns: An IEnumerator that can be used to iterate through the collection.
        """
        ...

    def TryAdd(self, item: System_Collections_Concurrent_ConcurrentQueue_T) -> bool:
        """
        Attempts to add an object to the Concurrent.IProducerConsumerCollection{T}.
        
        :param item: The object to add to the Concurrent.IProducerConsumerCollection{T}. The value can be a null reference (Nothing in Visual Basic) for reference types.
        :returns: true if the object was added successfully; otherwise, false.
        """
        ...

    def TryTake(self, item: System_Collections_Concurrent_ConcurrentQueue_T) -> bool:
        """
        Attempts to remove and return an object from the Concurrent.IProducerConsumerCollection{T}.
        
        :param item: When this method returns, if the operation was successful,  contains the object removed. If no object was available to be removed, the value is unspecified.
        :returns: true if an element was removed and returned successfully; otherwise, false.
        """
        ...

    def ToArray(self) -> typing.List[System_Collections_Concurrent_ConcurrentQueue_T]:
        """
        Copies the elements stored in the ConcurrentQueue{T} to a new array.
        
        :returns: A new array containing a snapshot of elements copied from the ConcurrentQueue{T}.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[System_Collections_Concurrent_ConcurrentQueue_T], index: int) -> None:
        """
        Copies the ConcurrentQueue{T} elements to an existing one-dimensional Array, starting at the specified array index.
        
        :param array: The one-dimensional Array that is the destination of the elements copied from the ConcurrentQueue{T}. The Array must have zero-based indexing.
        :param index: The zero-based index in  at which copying begins.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_Concurrent_ConcurrentQueue_T]:
        """
        Returns an enumerator that iterates through the ConcurrentQueue{T}.
        
        :returns: An enumerator for the contents of the ConcurrentQueue{T}.
        """
        ...

    def Enqueue(self, item: System_Collections_Concurrent_ConcurrentQueue_T) -> None:
        """
        Adds an object to the end of the ConcurrentQueue{T}.
        
        :param item: The object to add to the end of the ConcurrentQueue{T}. The value can be a null reference (Nothing in Visual Basic) for reference types.
        """
        ...

    def TryDequeue(self, result: System_Collections_Concurrent_ConcurrentQueue_T) -> bool:
        """
        Attempts to remove and return the object at the beginning of the ConcurrentQueue{T}.
        
        :param result: When this method returns, if the operation was successful,  contains the object removed. If no object was available to be removed, the value is unspecified.
        :returns: true if an element was removed and returned from the beginning of the ConcurrentQueue{T} successfully; otherwise, false.
        """
        ...

    def TryPeek(self, result: System_Collections_Concurrent_ConcurrentQueue_T) -> bool:
        """
        Attempts to return an object from the beginning of the ConcurrentQueue{T}
        without removing it.
        
        :param result: When this method returns,  contains an object from the beginning of the Concurrent.ConcurrentQueue{T} or default(T) if the operation failed.
        :returns: true if and object was returned successfully; otherwise, false.
        """
        ...

    def Clear(self) -> None:
        """Removes all objects from the ConcurrentQueue{T}."""
        ...


