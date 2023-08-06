import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Auxiliary
import QuantConnect.Data.Consolidators
import QuantConnect.Data.UniverseSelection
import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.DataFeeds
import QuantConnect.Lean.Engine.DataFeeds.Enumerators
import QuantConnect.Lean.Engine.Results
import QuantConnect.Securities
import QuantConnect.Util
import System
import System.Collections.Generic

System_EventHandler = typing.Any

QuantConnect_Lean_Engine_DataFeeds_Enumerators_BaseDataCollectionAggregatorEnumerator_T = typing.TypeVar("QuantConnect_Lean_Engine_DataFeeds_Enumerators_BaseDataCollectionAggregatorEnumerator_T")
QuantConnect_Lean_Engine_DataFeeds_Enumerators_EnqueueableEnumerator_T = typing.TypeVar("QuantConnect_Lean_Engine_DataFeeds_Enumerators_EnqueueableEnumerator_T")
QuantConnect_Lean_Engine_DataFeeds_Enumerators_RefreshEnumerator_T = typing.TypeVar("QuantConnect_Lean_Engine_DataFeeds_Enumerators_RefreshEnumerator_T")
QuantConnect_Lean_Engine_DataFeeds_Enumerators_RateLimitEnumerator_T = typing.TypeVar("QuantConnect_Lean_Engine_DataFeeds_Enumerators_RateLimitEnumerator_T")
QuantConnect_Lean_Engine_DataFeeds_Enumerators_ScannableEnumerator_T = typing.TypeVar("QuantConnect_Lean_Engine_DataFeeds_Enumerators_ScannableEnumerator_T")


class FastForwardEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """Provides the ability to fast forward an enumerator based on the age of the data"""

    @property
    def Current(self) -> QuantConnect.Data.BaseData:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def __init__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], timeProvider: QuantConnect.ITimeProvider, timeZone: typing.Any, maximumDataAge: datetime.timedelta) -> None:
        """
        Initializes a new instance of the FastForwardEnumerator class
        
        :param enumerator: The source enumerator
        :param timeProvider: A time provider used to determine age of data
        :param timeZone: The data's time zone
        :param maximumDataAge: The maximum age of data allowed
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


class FillForwardEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """
    The FillForwardEnumerator wraps an existing base data enumerator and inserts extra 'base data' instances
    on a specified fill forward resolution
    """

    @property
    def Exchange(self) -> QuantConnect.Securities.SecurityExchange:
        """
        The exchange used to determine when to insert fill forward data
        
        This field is protected.
        """
        ...

    @property
    def Current(self) -> QuantConnect.Data.BaseData:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    @Current.setter
    def Current(self, value: QuantConnect.Data.BaseData):
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def __init__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], exchange: QuantConnect.Securities.SecurityExchange, fillForwardResolution: QuantConnect.Util.IReadOnlyRef[datetime.timedelta], isExtendedMarketHours: bool, subscriptionEndTime: datetime.datetime, dataResolution: datetime.timedelta, dataTimeZone: typing.Any) -> None:
        """
        Initializes a new instance of the FillForwardEnumerator class that accepts
        a reference to the fill forward resolution, useful if the fill forward resolution is dynamic
        and changing as the enumeration progresses
        
        :param enumerator: The source enumerator to be filled forward
        :param exchange: The exchange used to determine when to insert fill forward data
        :param fillForwardResolution: The resolution we'd like to receive data on
        :param isExtendedMarketHours: True to use the exchange's extended market hours, false to use the regular market hours
        :param subscriptionEndTime: The end time of the subscrition, once passing this date the enumerator will stop
        :param dataResolution: The source enumerator's data resolution
        :param dataTimeZone: The time zone of the underlying source data. This is used for rounding calculations and is NOT the time zone on the BaseData instances (unless of course data time zone equals the exchange time zone)
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def RequiresFillForwardData(self, fillForwardResolution: datetime.timedelta, previous: QuantConnect.Data.BaseData, next: QuantConnect.Data.BaseData, fillForward: QuantConnect.Data.BaseData) -> bool:
        """
        Determines whether or not fill forward is required, and if true, will produce the new fill forward data
        
        This method is protected.
        
        :param previous: The last piece of data emitted by this enumerator
        :param next: The next piece of data on the source enumerator
        :param fillForward: When this function returns true, this will have a non-null value, null when the function returns false
        :returns: True when a new fill forward piece of data was produced and should be emitted by this enumerator.
        """
        ...


class LiveFillForwardEnumerator(QuantConnect.Lean.Engine.DataFeeds.Enumerators.FillForwardEnumerator):
    """
    An implementation of the FillForwardEnumerator that uses an ITimeProvider
    to determine if a fill forward bar needs to be emitted
    """

    def __init__(self, timeProvider: QuantConnect.ITimeProvider, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], exchange: QuantConnect.Securities.SecurityExchange, fillForwardResolution: QuantConnect.Util.IReadOnlyRef[datetime.timedelta], isExtendedMarketHours: bool, subscriptionEndTime: datetime.datetime, dataResolution: datetime.timedelta, dataTimeZone: typing.Any) -> None:
        """
        Initializes a new instance of the LiveFillForwardEnumerator class that accepts
        a reference to the fill forward resolution, useful if the fill forward resolution is dynamic
        and changing as the enumeration progresses
        
        :param timeProvider: The source of time used to gauage when this enumerator should emit extra bars when null data is returned from the source enumerator
        :param enumerator: The source enumerator to be filled forward
        :param exchange: The exchange used to determine when to insert fill forward data
        :param fillForwardResolution: The resolution we'd like to receive data on
        :param isExtendedMarketHours: True to use the exchange's extended market hours, false to use the regular market hours
        :param subscriptionEndTime: The end time of the subscription, once passing this date the enumerator will stop
        :param dataResolution: The source enumerator's data resolution
        :param dataTimeZone: Time zone of the underlying source data
        """
        ...

    def RequiresFillForwardData(self, fillForwardResolution: datetime.timedelta, previous: QuantConnect.Data.BaseData, next: QuantConnect.Data.BaseData, fillForward: QuantConnect.Data.BaseData) -> bool:
        """
        Determines whether or not fill forward is required, and if true, will produce the new fill forward data
        
        This method is protected.
        
        :param previous: The last piece of data emitted by this enumerator
        :param next: The next piece of data on the source enumerator, this may be null
        :param fillForward: When this function returns true, this will have a non-null value, null when the function returns false
        :returns: True when a new fill forward piece of data was produced and should be emitted by this enumerator.
        """
        ...


class BaseDataCollectionAggregatorEnumerator(typing.Generic[QuantConnect_Lean_Engine_DataFeeds_Enumerators_BaseDataCollectionAggregatorEnumerator_T], System.Object, System.Collections.Generic.IEnumerator[QuantConnect_Lean_Engine_DataFeeds_Enumerators_BaseDataCollectionAggregatorEnumerator_T]):
    """
    Provides an implementation of IEnumerator{BaseDataCollection}
    that aggregates an underlying IEnumerator{BaseData} into a single
    data packet
    """

    @property
    def Current(self) -> QuantConnect_Lean_Engine_DataFeeds_Enumerators_BaseDataCollectionAggregatorEnumerator_T:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    @Current.setter
    def Current(self, value: QuantConnect_Lean_Engine_DataFeeds_Enumerators_BaseDataCollectionAggregatorEnumerator_T):
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    @typing.overload
    def __init__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], symbol: typing.Union[QuantConnect.Symbol, str], liveMode: bool = False) -> None:
        """
        Initializes a new instance of the BaseDataCollectionAggregatorEnumerator class
        This will aggregate instances emitted from the underlying enumerator and tag them with the
        specified symbol
        
        :param enumerator: The underlying enumerator to aggregate
        :param symbol: The symbol to place on the aggregated collection
        :param liveMode: True if running in live mode
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def CreateCollection(self, symbol: typing.Union[QuantConnect.Symbol, str], time: datetime.datetime, endTime: datetime.datetime) -> QuantConnect_Lean_Engine_DataFeeds_Enumerators_BaseDataCollectionAggregatorEnumerator_T:
        """
        Creates a new, empty BaseDataCollection.
        
        This method is protected.
        
        :param symbol: The base data collection symbol
        :param time: The start time of the collection
        :param endTime: The end time of the collection
        :returns: A new, empty BaseDataCollection.
        """
        ...

    def Add(self, collection: QuantConnect_Lean_Engine_DataFeeds_Enumerators_BaseDataCollectionAggregatorEnumerator_T, current: QuantConnect.Data.BaseData) -> None:
        """
        Adds the specified instance of BaseData to the current collection
        
        This method is protected.
        
        :param collection: The collection to be added to
        :param current: The data to be added
        """
        ...

    def SetData(self, collection: QuantConnect_Lean_Engine_DataFeeds_Enumerators_BaseDataCollectionAggregatorEnumerator_T, current: System.Collections.Generic.List[QuantConnect.Data.BaseData]) -> None:
        """
        Adds all specified instances of BaseData to the current collection
        
        This method is protected.
        
        :param collection: The collection to be added to
        :param current: The data collection to be added
        """
        ...

    def IsValid(self, collection: QuantConnect_Lean_Engine_DataFeeds_Enumerators_BaseDataCollectionAggregatorEnumerator_T) -> bool:
        """
        Determines if a given data point is valid and can be emitted
        
        This method is protected.
        
        :param collection: The collection to be emitted
        :returns: True if its a valid data point.
        """
        ...

    @typing.overload
    def __init__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], symbol: typing.Union[QuantConnect.Symbol, str], liveMode: bool = False) -> None:
        """
        Initializes a new instance of the BaseDataCollectionAggregatorEnumerator class
        
        :param enumerator: The enumerator to aggregate
        :param symbol: The output data's symbol
        :param liveMode: True if running in live mode
        """
        ...


class SubscriptionFilterEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """Implements a wrapper around a base data enumerator to provide a final filtering step"""

    @property
    def DataFilterError(self) -> typing.List[System_EventHandler]:
        """Fired when there's an error executing a user's data filter"""
        ...

    @DataFilterError.setter
    def DataFilterError(self, value: typing.List[System_EventHandler]):
        """Fired when there's an error executing a user's data filter"""
        ...

    @property
    def Current(self) -> QuantConnect.Data.BaseData:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    @Current.setter
    def Current(self, value: QuantConnect.Data.BaseData):
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    @staticmethod
    def WrapForDataFeed(resultHandler: QuantConnect.Lean.Engine.Results.IResultHandler, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], security: QuantConnect.Securities.Security, endTime: datetime.datetime, extendedMarketHours: bool, liveMode: bool, securityExchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> QuantConnect.Lean.Engine.DataFeeds.Enumerators.SubscriptionFilterEnumerator:
        """
        Convenience method to wrap the enumerator and attach the data filter event to log and alery users of errors
        
        :param resultHandler: Result handler reference used to send errors
        :param enumerator: The source enumerator to be wrapped
        :param security: The security who's data is being enumerated
        :param endTime: The end time of the subscription
        :param extendedMarketHours: True if extended market hours are enabled
        :param liveMode: True if live mode
        :param securityExchangeHours: The security exchange hours instance to use
        :returns: A new instance of the SubscriptionFilterEnumerator class that has had it's DataFilterError event subscribed to to send errors to the result handler.
        """
        ...

    def __init__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], security: QuantConnect.Securities.Security, endTime: datetime.datetime, extendedMarketHours: bool, liveMode: bool, securityExchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> None:
        """
        Initializes a new instance of the SubscriptionFilterEnumerator class
        
        :param enumerator: The source enumerator to be wrapped
        :param security: The security containing an exchange and data filter
        :param endTime: The end time of the subscription
        :param extendedMarketHours: True if extended market hours are enabled
        :param liveMode: True if live mode
        :param securityExchangeHours: The security exchange hours instance to use
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...


class EnqueueableEnumerator(typing.Generic[QuantConnect_Lean_Engine_DataFeeds_Enumerators_EnqueueableEnumerator_T], System.Object, System.Collections.Generic.IEnumerator[QuantConnect_Lean_Engine_DataFeeds_Enumerators_EnqueueableEnumerator_T]):
    """
    An implementation of IEnumerator{T} that relies on the
    Enqueue method being called and only ends when Stop
    is called
    """

    @property
    def Count(self) -> int:
        """Gets the current number of items held in the internal queue"""
        ...

    @property
    def LastEnqueued(self) -> QuantConnect_Lean_Engine_DataFeeds_Enumerators_EnqueueableEnumerator_T:
        """Gets the last item that was enqueued"""
        ...

    @property
    def HasFinished(self) -> bool:
        """Returns true if the enumerator has finished and will not accept any more data"""
        ...

    @property
    def Current(self) -> QuantConnect_Lean_Engine_DataFeeds_Enumerators_EnqueueableEnumerator_T:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def __init__(self, blocking: bool = False) -> None:
        """
        Initializes a new instance of the EnqueueableEnumerator{T} class
        
        :param blocking: Specifies whether or not to use the blocking behavior
        """
        ...

    def Enqueue(self, data: QuantConnect_Lean_Engine_DataFeeds_Enumerators_EnqueueableEnumerator_T) -> None:
        """
        Enqueues the new data into this enumerator
        
        :param data: The data to be enqueued
        """
        ...

    def Stop(self) -> None:
        """
        Signals the enumerator to stop enumerating when the items currently
        held inside are gone. No more items will be added to this enumerator.
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


class ITradableDatesNotifier(metaclass=abc.ABCMeta):
    """
    Interface which will provide an event handler
    who will be fired with each new tradable day
    """

    @property
    @abc.abstractmethod
    def NewTradableDate(self) -> typing.List[System_EventHandler]:
        """Event fired when there is a new tradable date"""
        ...

    @NewTradableDate.setter
    @abc.abstractmethod
    def NewTradableDate(self, value: typing.List[System_EventHandler]):
        """Event fired when there is a new tradable date"""
        ...


class RefreshEnumerator(typing.Generic[QuantConnect_Lean_Engine_DataFeeds_Enumerators_RefreshEnumerator_T], System.Object, System.Collections.Generic.IEnumerator[QuantConnect_Lean_Engine_DataFeeds_Enumerators_RefreshEnumerator_T]):
    """
    Provides an implementation of IEnumerator{T} that will
    always return true via MoveNext.
    """

    @property
    def Current(self) -> QuantConnect_Lean_Engine_DataFeeds_Enumerators_RefreshEnumerator_T:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def __init__(self, enumeratorFactory: typing.Callable[[], System.Collections.Generic.IEnumerator[QuantConnect_Lean_Engine_DataFeeds_Enumerators_RefreshEnumerator_T]]) -> None:
        """
        Initializes a new instance of the RefreshEnumerator{T} class
        
        :param enumeratorFactory: Enumerator factory used to regenerate the underlying enumerator when it ends
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


class RateLimitEnumerator(typing.Generic[QuantConnect_Lean_Engine_DataFeeds_Enumerators_RateLimitEnumerator_T], System.Object, System.Collections.Generic.IEnumerator[QuantConnect_Lean_Engine_DataFeeds_Enumerators_RateLimitEnumerator_T]):
    """
    Provides augmentation of how often an enumerator can be called. Time is measured using
    an ITimeProvider instance and calls to the underlying enumerator are limited
    to a minimum time between each call.
    """

    @property
    def Current(self) -> QuantConnect_Lean_Engine_DataFeeds_Enumerators_RateLimitEnumerator_T:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def __init__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect_Lean_Engine_DataFeeds_Enumerators_RateLimitEnumerator_T], timeProvider: QuantConnect.ITimeProvider, minimumTimeBetweenCalls: datetime.timedelta) -> None:
        """
        Initializes a new instance of the RateLimitEnumerator{T} class
        
        :param enumerator: The underlying enumerator to place rate limits on
        :param timeProvider: Time provider used for determing the time between calls
        :param minimumTimeBetweenCalls: The minimum time allowed between calls to the underlying enumerator
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


class ITradableDateEventProvider(metaclass=abc.ABCMeta):
    """Interface for event providers for new tradable dates"""

    def GetEvents(self, eventArgs: QuantConnect.NewTradableDateEventArgs) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Called each time there is a new tradable day
        
        :param eventArgs: The new tradable day event arguments
        :returns: New corporate event if any.
        """
        ...

    def Initialize(self, config: QuantConnect.Data.SubscriptionDataConfig, factorFile: QuantConnect.Data.Auxiliary.FactorFile, mapFile: QuantConnect.Data.Auxiliary.MapFile, startTime: datetime.datetime) -> None:
        """
        Initializes the event provider instance
        
        :param config: The SubscriptionDataConfig
        :param factorFile: The factor file to use
        :param mapFile: The MapFile to use
        :param startTime: Start date for the data request
        """
        ...


class MappingEventProvider(System.Object, QuantConnect.Lean.Engine.DataFeeds.Enumerators.ITradableDateEventProvider):
    """Event provider who will emit SymbolChangedEvent events"""

    def Initialize(self, config: QuantConnect.Data.SubscriptionDataConfig, factorFile: QuantConnect.Data.Auxiliary.FactorFile, mapFile: QuantConnect.Data.Auxiliary.MapFile, startTime: datetime.datetime) -> None:
        """
        Initializes this instance
        
        :param config: The SubscriptionDataConfig
        :param factorFile: The factor file to use
        :param mapFile: The MapFile to use
        :param startTime: Start date for the data request
        """
        ...

    def GetEvents(self, eventArgs: QuantConnect.NewTradableDateEventArgs) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Check for new mappings
        
        :param eventArgs: The new tradable day event arguments
        :returns: New mapping event if any.
        """
        ...


class DataQueueFuturesChainUniverseDataCollectionEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.UniverseSelection.FuturesChainUniverseDataCollection]):
    """Enumerates live futures symbol universe data into FuturesChainUniverseDataCollection instances"""

    @property
    def Current(self) -> QuantConnect.Data.UniverseSelection.FuturesChainUniverseDataCollection:
        """Returns current futures chain enumerator position"""
        ...

    @Current.setter
    def Current(self, value: QuantConnect.Data.UniverseSelection.FuturesChainUniverseDataCollection):
        """Returns current futures chain enumerator position"""
        ...

    def __init__(self, subscriptionRequest: QuantConnect.Data.UniverseSelection.SubscriptionRequest, universeProvider: QuantConnect.Interfaces.IDataQueueUniverseProvider, timeProvider: QuantConnect.ITimeProvider) -> None:
        """
        Initializes a new instance of the DataQueueFuturesChainUniverseDataCollectionEnumerator class.
        
        :param subscriptionRequest: The subscription request to be used
        :param universeProvider: Symbol universe provider of the data queue
        :param timeProvider: The time provider to be used
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...


class QuoteBarFillForwardEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """
    The QuoteBarFillForwardEnumerator wraps an existing base data enumerator
    If the current QuoteBar has null Bid and/or Ask bars, it copies them from the previous QuoteBar
    """

    @property
    def Current(self) -> QuantConnect.Data.BaseData:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    @Current.setter
    def Current(self, value: QuantConnect.Data.BaseData):
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def __init__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]) -> None:
        """Initializes a new instance of the FillForwardEnumerator class"""
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...


class FuturesChainUniverseDataCollectionAggregatorEnumerator(QuantConnect.Lean.Engine.DataFeeds.Enumerators.BaseDataCollectionAggregatorEnumerator[QuantConnect.Data.UniverseSelection.FuturesChainUniverseDataCollection]):
    """Aggregates an enumerator into FuturesChainUniverseDataCollection instances"""

    def __init__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], symbol: typing.Union[QuantConnect.Symbol, str]) -> None:
        """
        Initializes a new instance of the FuturesChainUniverseDataCollectionAggregatorEnumerator class
        
        :param enumerator: The enumerator to aggregate
        :param symbol: The output data's symbol
        """
        ...

    def Add(self, collection: QuantConnect.Data.UniverseSelection.FuturesChainUniverseDataCollection, current: QuantConnect.Data.BaseData) -> None:
        """
        Adds the specified instance of BaseData to the current collection
        
        This method is protected.
        
        :param collection: The collection to be added to
        :param current: The data to be added
        """
        ...


class SynchronizingEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """
    Represents an enumerator capable of synchronizing other base data enumerators in time.
    This assumes that all enumerators have data time stamped in the same time zone
    """

    @property
    def Current(self) -> QuantConnect.Data.BaseData:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    @Current.setter
    def Current(self, value: QuantConnect.Data.BaseData):
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    @typing.overload
    def __init__(self, *enumerators: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]) -> None:
        """
        Initializes a new instance of the SynchronizingEnumerator class
        
        :param enumerators: The enumerators to be synchronized. NOTE: Assumes the same time zone for all data
        """
        ...

    @typing.overload
    def __init__(self, enumerators: System.Collections.Generic.IEnumerable[System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]]) -> None:
        """
        Initializes a new instance of the SynchronizingEnumerator class
        
        :param enumerators: The enumerators to be synchronized. NOTE: Assumes the same time zone for all data
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


class DataQueueOptionChainUniverseDataCollectionEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.UniverseSelection.OptionChainUniverseDataCollection]):
    """Enumerates live options symbol universe data into OptionChainUniverseDataCollection instances"""

    @property
    def Underlying(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """Gets the enumerator for the underlying asset"""
        ...

    @property
    def Current(self) -> QuantConnect.Data.UniverseSelection.OptionChainUniverseDataCollection:
        """Returns current option chain enumerator position"""
        ...

    @Current.setter
    def Current(self, value: QuantConnect.Data.UniverseSelection.OptionChainUniverseDataCollection):
        """Returns current option chain enumerator position"""
        ...

    def __init__(self, subscriptionRequest: QuantConnect.Data.UniverseSelection.SubscriptionRequest, underlying: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], universeProvider: QuantConnect.Interfaces.IDataQueueUniverseProvider, timeProvider: QuantConnect.ITimeProvider) -> None:
        """
        Initializes a new instance of the DataQueueOptionChainUniverseDataCollectionEnumerator class.
        
        :param subscriptionRequest: The subscription request to be used
        :param underlying: Underlying enumerator
        :param universeProvider: Symbol universe provider of the data queue
        :param timeProvider: The time provider to be used
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...


class DividendEventProvider(System.Object, QuantConnect.Lean.Engine.DataFeeds.Enumerators.ITradableDateEventProvider):
    """Event provider who will emit Dividend events"""

    def Initialize(self, config: QuantConnect.Data.SubscriptionDataConfig, factorFile: QuantConnect.Data.Auxiliary.FactorFile, mapFile: QuantConnect.Data.Auxiliary.MapFile, startTime: datetime.datetime) -> None:
        """
        Initializes this instance
        
        :param config: The SubscriptionDataConfig
        :param factorFile: The factor file to use
        :param mapFile: The MapFile to use
        :param startTime: Start date for the data request
        """
        ...

    def GetEvents(self, eventArgs: QuantConnect.NewTradableDateEventArgs) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Check for dividends and returns them
        
        :param eventArgs: The new tradable day event arguments
        :returns: New Dividend event if any.
        """
        ...


class SplitEventProvider(System.Object, QuantConnect.Lean.Engine.DataFeeds.Enumerators.ITradableDateEventProvider):
    """Event provider who will emit Split events"""

    def Initialize(self, config: QuantConnect.Data.SubscriptionDataConfig, factorFile: QuantConnect.Data.Auxiliary.FactorFile, mapFile: QuantConnect.Data.Auxiliary.MapFile, startTime: datetime.datetime) -> None:
        """
        Initializes this instance
        
        :param config: The SubscriptionDataConfig
        :param factorFile: The factor file to use
        :param mapFile: The MapFile to use
        :param startTime: Start date for the data request
        """
        ...

    def GetEvents(self, eventArgs: QuantConnect.NewTradableDateEventArgs) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Check for new splits
        
        :param eventArgs: The new tradable day event arguments
        :returns: New split event if any.
        """
        ...


class DelistingEventProvider(System.Object, QuantConnect.Lean.Engine.DataFeeds.Enumerators.ITradableDateEventProvider):
    """Event provider who will emit Delisting events"""

    @property
    def DelistingDate(self) -> QuantConnect.Util.ReferenceWrapper[datetime.datetime]:
        """
        The delisting date
        
        This property is protected.
        """
        ...

    @DelistingDate.setter
    def DelistingDate(self, value: QuantConnect.Util.ReferenceWrapper[datetime.datetime]):
        """
        The delisting date
        
        This property is protected.
        """
        ...

    def Initialize(self, config: QuantConnect.Data.SubscriptionDataConfig, factorFile: QuantConnect.Data.Auxiliary.FactorFile, mapFile: QuantConnect.Data.Auxiliary.MapFile, startTime: datetime.datetime) -> None:
        """
        Initializes this instance
        
        :param config: The SubscriptionDataConfig
        :param factorFile: The factor file to use
        :param mapFile: The MapFile to use
        :param startTime: Start date for the data request
        """
        ...

    def GetEvents(self, eventArgs: QuantConnect.NewTradableDateEventArgs) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Check for delistings
        
        :param eventArgs: The new tradable day event arguments
        :returns: New delisting event if any.
        """
        ...


class LiveDataBasedDelistingEventProvider(QuantConnect.Lean.Engine.DataFeeds.Enumerators.DelistingEventProvider, System.IDisposable):
    """Delisting event provider implementation which will source the delisting date based on the incoming data point"""

    def __init__(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig, dataQueueHandler: QuantConnect.Interfaces.IDataQueueHandler) -> None:
        """Creates a new instance"""
        ...

    def Dispose(self) -> None:
        """Clean up"""
        ...


class ScannableEnumerator(typing.Generic[QuantConnect_Lean_Engine_DataFeeds_Enumerators_ScannableEnumerator_T], System.Object, System.Collections.Generic.IEnumerator[QuantConnect_Lean_Engine_DataFeeds_Enumerators_ScannableEnumerator_T]):
    """An implementation of IEnumerator{T} that relies on "consolidated" data"""

    @property
    def Current(self) -> QuantConnect_Lean_Engine_DataFeeds_Enumerators_ScannableEnumerator_T:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def __init__(self, consolidator: QuantConnect.Data.Consolidators.IDataConsolidator, timeZone: typing.Any, timeProvider: QuantConnect.ITimeProvider, newDataAvailableHandler: System_EventHandler, isPeriodBased: bool = True) -> None:
        """
        Initializes a new instance of the ScannableEnumerator{T} class
        
        :param consolidator: Consolidator taking BaseData updates and firing events containing new 'consolidated' data
        :param timeZone: The time zone the raw data is time stamped in
        :param timeProvider: The time provider instance used to determine when bars are completed and can be emitted
        :param newDataAvailableHandler: The event handler for a new available data point
        :param isPeriodBased: The consolidator is period based, this will enable scanning on MoveNext
        """
        ...

    def Update(self, data: QuantConnect_Lean_Engine_DataFeeds_Enumerators_ScannableEnumerator_T) -> None:
        """
        Updates the consolidator
        
        :param data: The data to consolidate
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


class ConcatEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """Enumerator that will concatenate enumerators together sequentially enumerating them in the provided order"""

    @property
    def Current(self) -> QuantConnect.Data.BaseData:
        """The current BaseData object"""
        ...

    @Current.setter
    def Current(self, value: QuantConnect.Data.BaseData):
        """The current BaseData object"""
        ...

    def __init__(self, skipDuplicateEndTimes: bool, *enumerators: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]) -> None:
        """
        Creates a new instance
        
        :param skipDuplicateEndTimes: True will skip data points from enumerators if before or at the last end time
        :param enumerators: The sequence of enumerators to concatenate
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: True if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


class FrontierAwareEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """
    Provides an implementation of IEnumerator{BaseData} that will not emit
    data ahead of the frontier as specified by an instance of ITimeProvider.
    An instance of TimeZoneOffsetProvider is used to convert between UTC
    and the data's native time zone
    """

    @property
    def Current(self) -> QuantConnect.Data.BaseData:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def __init__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], timeProvider: QuantConnect.ITimeProvider, offsetProvider: QuantConnect.TimeZoneOffsetProvider) -> None:
        """
        Initializes a new instance of the FrontierAwareEnumerator class
        
        :param enumerator: The underlying enumerator to make frontier aware
        :param timeProvider: The time provider used for resolving the current frontier time
        :param offsetProvider: An offset provider used for converting the frontier UTC time into the data's native time zone
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


class LiveAuxiliaryDataSynchronizingEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """
    Represents an enumerator capable of synchronizing live equity data enumerators in time.
    This assumes that all enumerators have data time stamped in the same time zone.
    """

    @property
    def Current(self) -> QuantConnect.Data.BaseData:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    @Current.setter
    def Current(self, value: QuantConnect.Data.BaseData):
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def __init__(self, timeProvider: QuantConnect.ITimeProvider, exchangeTimeZone: typing.Any, tradeBarAggregator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], *auxDataEnumerators: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]) -> None:
        """
        Initializes a new instance of the LiveAuxiliaryDataSynchronizingEnumerator class
        
        :param timeProvider: The source of time used to gauge when this enumerator should emit extra bars when null data is returned from the source enumerator
        :param exchangeTimeZone: The time zone the raw data is time stamped in
        :param tradeBarAggregator: The trade bar aggregator enumerator
        :param auxDataEnumerators: The auxiliary data enumerators
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


class AuxiliaryDataEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """
    Auxiliary data enumerator that will, initialize and call the ITradableDateEventProvider.GetEvents
    implementation each time there is a new tradable day for every ITradableDateEventProvider
    provided.
    """

    @property
    def Current(self) -> System.Object:
        ...

    def __init__(self, config: QuantConnect.Data.SubscriptionDataConfig, factorFile: System.Lazy[QuantConnect.Data.Auxiliary.FactorFile], mapFile: System.Lazy[QuantConnect.Data.Auxiliary.MapFile], tradableDateEventProviders: typing.List[QuantConnect.Lean.Engine.DataFeeds.Enumerators.ITradableDateEventProvider], tradableDayNotifier: QuantConnect.Lean.Engine.DataFeeds.Enumerators.ITradableDatesNotifier, includeAuxiliaryData: bool, startTime: datetime.datetime) -> None:
        """
        Creates a new instance
        
        :param config: The SubscriptionDataConfig
        :param factorFile: The factor file to use
        :param mapFile: The MapFile to use
        :param tradableDateEventProviders: The tradable dates event providers
        :param tradableDayNotifier: Tradable dates provider
        :param includeAuxiliaryData: True to emit auxiliary data
        :param startTime: Start date for the data request
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element.
        
        :returns: Always true.
        """
        ...

    def Dispose(self) -> None:
        """Dispose of the Stream Reader and close out the source stream and file connections."""
        ...

    def Reset(self) -> None:
        """Reset the IEnumeration"""
        ...


class SubscriptionDataEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Lean.Engine.DataFeeds.SubscriptionData]):
    """An IEnumerator{SubscriptionData} which wraps an existing IEnumerator{BaseData}."""

    @property
    def Current(self) -> System.Object:
        ...

    def __init__(self, configuration: QuantConnect.Data.SubscriptionDataConfig, exchangeHours: QuantConnect.Securities.SecurityExchangeHours, offsetProvider: QuantConnect.TimeZoneOffsetProvider, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]) -> None:
        """
        Creates a new instance
        
        :param configuration: The subscription's configuration
        :param exchangeHours: The security's exchange hours
        :param offsetProvider: The subscription's time zone offset provider
        :param enumerator: The underlying data enumerator
        :returns: A subscription data enumerator.
        """
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: True if the enumerator was successfully advanced to the next element; False if the enumerator has passed the end of the collection.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...


class OptionChainUniverseDataCollectionEnumerator(QuantConnect.Lean.Engine.DataFeeds.Enumerators.BaseDataCollectionAggregatorEnumerator[QuantConnect.Data.UniverseSelection.OptionChainUniverseDataCollection]):
    """Enumerates data into OptionChainUniverseDataCollection instances"""

    def __init__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], symbol: typing.Union[QuantConnect.Symbol, str]) -> None:
        """
        Initializes a new instance of the OptionChainUniverseDataCollectionEnumerator class
        
        :param enumerator: The enumerator to aggregate
        :param symbol: The output data's symbol
        """
        ...

    def Add(self, collection: QuantConnect.Data.UniverseSelection.OptionChainUniverseDataCollection, current: QuantConnect.Data.BaseData) -> None:
        """
        Adds the specified instance of BaseData to the current collection
        
        This method is protected.
        
        :param collection: The collection to be added to
        :param current: The data to be added
        """
        ...

    def IsValid(self, collection: QuantConnect.Data.UniverseSelection.OptionChainUniverseDataCollection) -> bool:
        """
        Determines if a given data point is valid and can be emitted
        
        This method is protected.
        
        :param collection: The collection to be emitted
        :returns: True if its a valid data point.
        """
        ...


class LiveDelistingEventProviderEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """
    A live trading delisting event provider which uses a DelistingEventProvider internally to emit events
    based on the current frontier time
    """

    @property
    def Current(self) -> QuantConnect.Data.BaseData:
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    @Current.setter
    def Current(self, value: QuantConnect.Data.BaseData):
        """Gets the element in the collection at the current position of the enumerator."""
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Sets the enumerator to its initial position, which is before the first element in the collection."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    @staticmethod
    def TryCreate(dataConfig: QuantConnect.Data.SubscriptionDataConfig, timeProvider: QuantConnect.ITimeProvider, dataQueueHandler: QuantConnect.Interfaces.IDataQueueHandler, securityCache: QuantConnect.Securities.SecurityCache, mapFileProvider: QuantConnect.Interfaces.IMapFileProvider, enumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]) -> bool:
        """
        Helper method to create a new instance.
        Knows which security types should create one and determines the appropriate delisting event provider to use
        """
        ...


class PriceScaleFactorEnumerator(System.Object, System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]):
    """
    This enumerator will update the SubscriptionDataConfig.PriceScaleFactor when required
    and adjust the raw BaseData prices based on the provided SubscriptionDataConfig.
    Assumes the prices of the provided IEnumerator are in raw mode.
    """

    @property
    def Current(self) -> System.Object:
        """Explicit interface implementation for Current"""
        ...

    def __init__(self, rawDataEnumerator: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], config: QuantConnect.Data.SubscriptionDataConfig, factorFile: System.Lazy[QuantConnect.Data.Auxiliary.FactorFile]) -> None:
        """
        Creates a new instance of the PriceScaleFactorEnumerator.
        
        :param rawDataEnumerator: The underlying raw data enumerator
        :param config: The SubscriptionDataConfig to enumerate for. Will determine the DataNormalizationMode to use.
        :param factorFile: The FactorFile instance to use
        """
        ...

    def Dispose(self) -> None:
        """Dispose of the underlying enumerator."""
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next element of the collection.
        
        :returns: True if the enumerator was successfully advanced to the next element; False if the enumerator has passed the end of the collection.
        """
        ...

    def Reset(self) -> None:
        """Reset the IEnumeration"""
        ...


