import abc
import typing

import QuantConnect.Lean.Engine.DataFeeds.WorkScheduling
import System
import System.Collections.Concurrent
import System.Threading


class WeightedWorkScheduler(System.Object):
    """
    This singleton class will create a thread pool to processes work
    that will be prioritized based on it's weight
    """

    WorkBatchSize: int = 50
    """This is the size of each work sprint"""

    MaxWorkWeight: int
    """
    This is the maximum size a work item can weigh,
    if reached, it will be ignored and not executed until its less
    """

    Instance: QuantConnect.Lean.Engine.DataFeeds.WorkScheduling.WeightedWorkScheduler = ...
    """Singleton instance"""

    def QueueWork(self, workFunc: typing.Callable[[int], bool], weightFunc: typing.Callable[[], int]) -> None:
        """
        Add a new work item to the queue
        
        :param workFunc: The work function to run
        :param weightFunc: The weight function. Work will be sorted in ascending order based on this weight
        """
        ...


class WorkItem(System.Object):
    """This class has no documentation."""

    @property
    def Weight(self) -> int:
        """The current weight"""
        ...

    @Weight.setter
    def Weight(self, value: int):
        """The current weight"""
        ...

    @property
    def Work(self) -> typing.Callable[[int], bool]:
        """The work function to execute"""
        ...

    def __init__(self, work: typing.Callable[[int], bool], weightFunc: typing.Callable[[], int]) -> None:
        """
        Creates a new instance
        
        :param work: The work function, takes an int, the amount of work to do and returns a bool, false if this work item is finished
        :param weightFunc: The function used to determine the current weight
        """
        ...

    def UpdateWeight(self) -> int:
        """Updates the weight of this work item"""
        ...

    @staticmethod
    def Compare(obj: QuantConnect.Lean.Engine.DataFeeds.WorkScheduling.WorkItem, other: QuantConnect.Lean.Engine.DataFeeds.WorkScheduling.WorkItem) -> int:
        """Compares two work items based on their weights"""
        ...


class IWorkQueue(metaclass=abc.ABCMeta):
    """Work queue abstraction"""

    @property
    @abc.abstractmethod
    def ThreadPriority(self) -> int:
        """
        Returns the thread priority to use for this work queue
        
        This property contains the int value of a member of the System.Threading.ThreadPriority enum.
        """
        ...

    def WorkerThread(self, newWork: System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Lean.Engine.DataFeeds.WorkScheduling.WorkItem], newWorkEvent: System.Threading.AutoResetEvent) -> None:
        """
        This is the worker thread loop.
        It will first try to take a work item from the new work queue else will check his own queue.
        """
        ...

    def Sort(self) -> None:
        """Sorts the work queue"""
        ...


