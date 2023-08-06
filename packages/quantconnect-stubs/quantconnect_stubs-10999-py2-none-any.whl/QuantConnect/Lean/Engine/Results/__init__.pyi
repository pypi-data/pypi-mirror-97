import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Data.UniverseSelection
import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.Results
import QuantConnect.Lean.Engine.TransactionHandlers
import QuantConnect.Logging
import QuantConnect.Orders
import QuantConnect.Orders.Serialization
import QuantConnect.Packets
import QuantConnect.Statistics
import System
import System.Collections.Concurrent
import System.Collections.Generic
import System.Threading


class BaseResultsHandler(System.Object, metaclass=abc.ABCMeta):
    """Provides base functionality to the implementations of IResultHandler"""

    @property
    def MainUpdateInterval(self) -> datetime.timedelta:
        """
        The main loop update interval
        
        This property is protected.
        """
        ...

    @property
    def ChartUpdateInterval(self) -> datetime.timedelta:
        """
        The chart update interval
        
        This field is protected.
        """
        ...

    @ChartUpdateInterval.setter
    def ChartUpdateInterval(self, value: datetime.timedelta):
        """
        The chart update interval
        
        This field is protected.
        """
        ...

    @property
    def LastDeltaOrderPosition(self) -> int:
        """
        The last position consumed from the ITransactionHandler.OrderEvents by GetDeltaOrders
        
        This field is protected.
        """
        ...

    @LastDeltaOrderPosition.setter
    def LastDeltaOrderPosition(self, value: int):
        """
        The last position consumed from the ITransactionHandler.OrderEvents by GetDeltaOrders
        
        This field is protected.
        """
        ...

    @property
    def LastDeltaOrderEventsPosition(self) -> int:
        """
        The last position consumed from the ITransactionHandler.OrderEvents while determining delta order events
        
        This field is protected.
        """
        ...

    @LastDeltaOrderEventsPosition.setter
    def LastDeltaOrderEventsPosition(self, value: int):
        """
        The last position consumed from the ITransactionHandler.OrderEvents while determining delta order events
        
        This field is protected.
        """
        ...

    @property
    def IsActive(self) -> bool:
        """Boolean flag indicating the thread is still active."""
        ...

    @property
    def Messages(self) -> System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Packets.Packet]:
        """Live packet messaging queue. Queue the messages here and send when the result queue is ready."""
        ...

    @Messages.setter
    def Messages(self, value: System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Packets.Packet]):
        """Live packet messaging queue. Queue the messages here and send when the result queue is ready."""
        ...

    @property
    def Charts(self) -> System.Collections.Concurrent.ConcurrentDictionary[str, QuantConnect.Chart]:
        """Storage for the price and equity charts of the live results."""
        ...

    @Charts.setter
    def Charts(self, value: System.Collections.Concurrent.ConcurrentDictionary[str, QuantConnect.Chart]):
        """Storage for the price and equity charts of the live results."""
        ...

    @property
    def ExitTriggered(self) -> bool:
        """
        True if the exit has been triggered
        
        This field is protected.
        """
        ...

    @ExitTriggered.setter
    def ExitTriggered(self, value: bool):
        """
        True if the exit has been triggered
        
        This field is protected.
        """
        ...

    @property
    def ExitEvent(self) -> System.Threading.ManualResetEvent:
        """
        Event set when exit is triggered
        
        This property is protected.
        """
        ...

    @property
    def LogStore(self) -> System.Collections.Generic.List[QuantConnect.Logging.LogEntry]:
        """
        The log store instance
        
        This property is protected.
        """
        ...

    @property
    def AlgorithmPerformanceCharts(self) -> System.Collections.Generic.List[str]:
        """
        Algorithms performance related chart names
        
        This property is protected.
        """
        ...

    @property
    def ChartLock(self) -> System.Object:
        """
        Lock to be used when accessing the chart collection
        
        This property is protected.
        """
        ...

    @property
    def ProjectId(self) -> int:
        """
        The algorithm project id
        
        This property is protected.
        """
        ...

    @ProjectId.setter
    def ProjectId(self, value: int):
        """
        The algorithm project id
        
        This property is protected.
        """
        ...

    @property
    def RamAllocation(self) -> str:
        """
        The maximum amount of RAM (in MB) this algorithm is allowed to utilize
        
        This property is protected.
        """
        ...

    @RamAllocation.setter
    def RamAllocation(self, value: str):
        """
        The maximum amount of RAM (in MB) this algorithm is allowed to utilize
        
        This property is protected.
        """
        ...

    @property
    def CompileId(self) -> str:
        """
        The algorithm unique compilation id
        
        This property is protected.
        """
        ...

    @CompileId.setter
    def CompileId(self, value: str):
        """
        The algorithm unique compilation id
        
        This property is protected.
        """
        ...

    @property
    def AlgorithmId(self) -> str:
        """
        The algorithm job id.
        This is the deploy id for live, backtesting id for backtesting
        
        This property is protected.
        """
        ...

    @AlgorithmId.setter
    def AlgorithmId(self, value: str):
        """
        The algorithm job id.
        This is the deploy id for live, backtesting id for backtesting
        
        This property is protected.
        """
        ...

    @property
    def StartTime(self) -> datetime.datetime:
        """
        The result handler start time
        
        This property is protected.
        """
        ...

    @property
    def RuntimeStatistics(self) -> System.Collections.Generic.Dictionary[str, str]:
        """
        Customizable dynamic statistics IAlgorithm.RuntimeStatistics
        
        This property is protected.
        """
        ...

    @property
    def MessagingHandler(self) -> QuantConnect.Interfaces.IMessagingHandler:
        """
        The handler responsible for communicating messages to listeners
        
        This field is protected.
        """
        ...

    @MessagingHandler.setter
    def MessagingHandler(self, value: QuantConnect.Interfaces.IMessagingHandler):
        """
        The handler responsible for communicating messages to listeners
        
        This field is protected.
        """
        ...

    @property
    def TransactionHandler(self) -> QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler:
        """
        The transaction handler used to get the algorithms Orders information
        
        This field is protected.
        """
        ...

    @TransactionHandler.setter
    def TransactionHandler(self, value: QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler):
        """
        The transaction handler used to get the algorithms Orders information
        
        This field is protected.
        """
        ...

    @property
    def StartingPortfolioValue(self) -> float:
        """
        The algorithms starting portfolio value.
        Used to calculate the portfolio return
        
        This property is protected.
        """
        ...

    @StartingPortfolioValue.setter
    def StartingPortfolioValue(self, value: float):
        """
        The algorithms starting portfolio value.
        Used to calculate the portfolio return
        
        This property is protected.
        """
        ...

    @property
    def Algorithm(self) -> QuantConnect.Interfaces.IAlgorithm:
        """
        The algorithm instance
        
        This property is protected.
        """
        ...

    @Algorithm.setter
    def Algorithm(self, value: QuantConnect.Interfaces.IAlgorithm):
        """
        The algorithm instance
        
        This property is protected.
        """
        ...

    @property
    def AlphaRuntimeStatistics(self) -> QuantConnect.AlphaRuntimeStatistics:
        """
        Gets or sets the current alpha runtime statistics
        
        This property is protected.
        """
        ...

    @AlphaRuntimeStatistics.setter
    def AlphaRuntimeStatistics(self, value: QuantConnect.AlphaRuntimeStatistics):
        """
        Gets or sets the current alpha runtime statistics
        
        This property is protected.
        """
        ...

    @property
    def DailyPortfolioValue(self) -> float:
        """
        Closing portfolio value. Used to calculate daily performance.
        
        This field is protected.
        """
        ...

    @DailyPortfolioValue.setter
    def DailyPortfolioValue(self, value: float):
        """
        Closing portfolio value. Used to calculate daily performance.
        
        This field is protected.
        """
        ...

    @property
    def PreviousUtcSampleTime(self) -> datetime.datetime:
        """
        Last time the IResultHandler.Sample(DateTime, bool) method was called in UTC
        
        This field is protected.
        """
        ...

    @PreviousUtcSampleTime.setter
    def PreviousUtcSampleTime(self, value: datetime.datetime):
        """
        Last time the IResultHandler.Sample(DateTime, bool) method was called in UTC
        
        This field is protected.
        """
        ...

    @property
    def ResamplePeriod(self) -> datetime.timedelta:
        """
        Sampling period for timespans between resamples of the charting equity.
        
        This property is protected.
        """
        ...

    @ResamplePeriod.setter
    def ResamplePeriod(self, value: datetime.timedelta):
        """
        Sampling period for timespans between resamples of the charting equity.
        
        This property is protected.
        """
        ...

    @property
    def NotificationPeriod(self) -> datetime.timedelta:
        """
        How frequently the backtests push messages to the browser.
        
        This property is protected.
        """
        ...

    @NotificationPeriod.setter
    def NotificationPeriod(self, value: datetime.timedelta):
        """
        How frequently the backtests push messages to the browser.
        
        This property is protected.
        """
        ...

    @property
    def ResultsDestinationFolder(self) -> str:
        """
        Directory location to store results
        
        This field is protected.
        """
        ...

    @ResultsDestinationFolder.setter
    def ResultsDestinationFolder(self, value: str):
        """
        Directory location to store results
        
        This field is protected.
        """
        ...

    @property
    def OrderEventJsonConverter(self) -> QuantConnect.Orders.Serialization.OrderEventJsonConverter:
        """
        The order event json converter instance to use
        
        This property is protected.
        """
        ...

    @OrderEventJsonConverter.setter
    def OrderEventJsonConverter(self, value: QuantConnect.Orders.Serialization.OrderEventJsonConverter):
        """
        The order event json converter instance to use
        
        This property is protected.
        """
        ...

    def __init__(self) -> None:
        """
        Creates a new instance
        
        This method is protected.
        """
        ...

    def OrderEvent(self, newEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        New order event for the algorithm
        
        :param newEvent: New event details
        """
        ...

    def Exit(self) -> None:
        """Terminate the result thread and apply any required exit procedures like sending final results"""
        ...

    def GetServerStatistics(self, utcNow: datetime.datetime) -> System.Collections.Generic.Dictionary[str, str]:
        """
        Gets the current Server statistics
        
        This method is protected.
        """
        ...

    def StoreOrderEvents(self, utcTime: datetime.datetime, orderEvents: System.Collections.Generic.List[QuantConnect.Orders.OrderEvent]) -> None:
        """
        Stores the order events
        
        This method is protected.
        
        :param utcTime: The utc date associated with these order events
        :param orderEvents: The order events to store
        """
        ...

    def GetDeltaOrders(self, orderEventsStartPosition: int, shouldStop: typing.Callable[[int], bool]) -> System.Collections.Generic.Dictionary[int, QuantConnect.Orders.Order]:
        """
        Gets the orders generated starting from the provided ITransactionHandler.OrderEvents position
        
        This method is protected.
        
        :returns: The delta orders.
        """
        ...

    def Initialize(self, job: QuantConnect.Packets.AlgorithmNodePacket, messagingHandler: QuantConnect.Interfaces.IMessagingHandler, api: QuantConnect.Interfaces.IApi, transactionHandler: QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler) -> None:
        """
        Initialize the result handler with this result packet.
        
        :param job: Algorithm job packet for this result handler
        :param messagingHandler: The handler responsible for communicating messages to listeners
        :param api: The api instance used for handling logs
        :param transactionHandler: The transaction handler used to get the algorithms Order information
        """
        ...

    def Run(self) -> None:
        """
        Result handler update method
        
        This method is protected.
        """
        ...

    def GetResultsPath(self, filename: str) -> str:
        """
        Gets the full path for a results file
        
        This method is protected.
        
        :param filename: The filename to add to the path
        :returns: The full path, including the filename.
        """
        ...

    def OnSecuritiesChanged(self, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """Event fired each time that we add/remove securities from the data feed"""
        ...

    def SaveLogs(self, id: str, logs: System.Collections.Generic.List[QuantConnect.Logging.LogEntry]) -> str:
        """
        Returns the location of the logs
        
        :param id: Id that will be incorporated into the algorithm log name
        :param logs: The logs to save
        :returns: The path to the logs.
        """
        ...

    def SaveResults(self, name: str, result: QuantConnect.Result) -> None:
        """
        Save the results to disk
        
        :param name: The name of the results
        :param result: The results to save
        """
        ...

    def SetAlphaRuntimeStatistics(self, statistics: QuantConnect.AlphaRuntimeStatistics) -> None:
        """
        Sets the current alpha runtime statistics
        
        :param statistics: The current alpha runtime statistics
        """
        ...

    def PurgeQueue(self) -> None:
        """
        Purge/clear any outstanding messages in message queue.
        
        This method is protected.
        """
        ...

    def StopUpdateRunner(self) -> None:
        """
        Stops the update runner task
        
        This method is protected.
        """
        ...

    def GetNetReturn(self) -> float:
        """
        Gets the algorithm net return
        
        This method is protected.
        """
        ...

    def StoreResult(self, packet: QuantConnect.Packets.Packet) -> None:
        """
        Save the snapshot of the total results to storage.
        
        This method is protected.
        
        :param packet: Packet to store.
        """
        ...

    def GetPortfolioValue(self) -> float:
        """
        Gets the current portfolio value
        
        This method is protected.
        """
        ...

    def GetBenchmarkValue(self) -> float:
        """
        Gets the current benchmark value
        
        This method is protected.
        """
        ...

    @typing.overload
    def Sample(self, time: datetime.datetime, force: bool = False) -> None:
        """
        Samples portfolio equity, benchmark, and daily performance
        
        :param time: Current UTC time in the AlgorithmManager loop
        :param force: Force sampling of equity, benchmark, and performance to be
        """
        ...

    def SampleEquity(self, time: datetime.datetime, value: float) -> None:
        """
        Sample the current equity of the strategy directly with time-value pair.
        
        This method is protected.
        
        :param time: Time of the sample.
        :param value: Current equity value.
        """
        ...

    def SamplePerformance(self, time: datetime.datetime, value: float) -> None:
        """
        Sample the current daily performance directly with a time-value pair.
        
        This method is protected.
        
        :param time: Time of the sample.
        :param value: Current daily performance value.
        """
        ...

    def SampleBenchmark(self, time: datetime.datetime, value: float) -> None:
        """
        Sample the current benchmark performance directly with a time-value pair.
        
        This method is protected.
        
        :param time: Time of the sample.
        :param value: Current benchmark value.
        """
        ...

    @typing.overload
    def Sample(self, chartName: str, seriesName: str, seriesIndex: int, seriesType: QuantConnect.SeriesType, time: datetime.datetime, value: float, unit: str = "$") -> None:
        """
        Add a sample to the chart specified by the chartName, and seriesName.
        
        This method is protected.
        
        :param chartName: String chart name to place the sample.
        :param seriesName: Series name for the chart.
        :param seriesIndex: Series chart index - which chart should this series belong
        :param seriesType: Series type for the chart.
        :param time: Time for the sample
        :param value: Value for the chart sample.
        :param unit: Unit for the chart axis
        """
        ...

    def GetAlgorithmRuntimeStatistics(self, summary: System.Collections.Generic.Dictionary[str, str], runtimeStatistics: System.Collections.Generic.Dictionary[str, str] = None, capacityEstimate: typing.Optional[float] = None) -> System.Collections.Generic.Dictionary[str, str]:
        """
        Gets the algorithm runtime statistics
        
        This method is protected.
        """
        ...

    def GenerateStatisticsResults(self, charts: System.Collections.Generic.Dictionary[str, QuantConnect.Chart], profitLoss: System.Collections.Generic.SortedDictionary[datetime.datetime, float] = None, estimatedStrategyCapacity: float = 0) -> QuantConnect.Statistics.StatisticsResults:
        """
        Will generate the statistics results and update the provided runtime statistics
        
        This method is protected.
        """
        ...

    def AddToLogStore(self, message: str) -> None:
        """
        Save an algorithm message to the log store. Uses a different timestamped method of adding messaging to interweve debug and logging messages.
        
        This method is protected.
        
        :param message: String message to store
        """
        ...

    def ProcessAlgorithmLogs(self, messageQueueLimit: typing.Optional[int] = None) -> None:
        """
        Processes algorithm logs.
        Logs of the same type are batched together one per line and are sent out
        
        This method is protected.
        """
        ...


class IResultHandler(metaclass=abc.ABCMeta):
    """
    Handle the results of the backtest: where should we send the profit, portfolio updates:
    Backtester or the Live trading platform:
    """

    @property
    @abc.abstractmethod
    def Messages(self) -> System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Packets.Packet]:
        """Put messages to process into the queue so they are processed by this thread."""
        ...

    @Messages.setter
    @abc.abstractmethod
    def Messages(self, value: System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Packets.Packet]):
        """Put messages to process into the queue so they are processed by this thread."""
        ...

    @property
    @abc.abstractmethod
    def IsActive(self) -> bool:
        """
        Boolean flag indicating the result hander thread is busy.
        False means it has completely finished and ready to dispose.
        """
        ...

    def OnSecuritiesChanged(self, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """Event fired each time that we add/remove securities from the data feed"""
        ...

    def Initialize(self, job: QuantConnect.Packets.AlgorithmNodePacket, messagingHandler: QuantConnect.Interfaces.IMessagingHandler, api: QuantConnect.Interfaces.IApi, transactionHandler: QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler) -> None:
        """
        Initialize the result handler with this result packet.
        
        :param job: Algorithm job packet for this result handler
        :param messagingHandler: The messaging handler provider to use
        :param api: The api implementation to use
        """
        ...

    def DebugMessage(self, message: str) -> None:
        """
        Process debug messages with the preconfigured settings.
        
        :param message: String debug message
        """
        ...

    def SystemDebugMessage(self, message: str) -> None:
        """
        Process system debug messages with the preconfigured settings.
        
        :param message: String debug message
        """
        ...

    def SecurityType(self, types: System.Collections.Generic.List[QuantConnect.SecurityType]) -> None:
        """
        Send a list of security types to the browser
        
        :param types: Security types list inside algorithm
        """
        ...

    def LogMessage(self, message: str) -> None:
        """
        Send a logging message to the log list for storage.
        
        :param message: Message we'd in the log.
        """
        ...

    def ErrorMessage(self, error: str, stacktrace: str = ...) -> None:
        """
        Send an error message back to the browser highlighted in red with a stacktrace.
        
        :param error: Error message we'd like shown in console.
        :param stacktrace: Stacktrace information string
        """
        ...

    def RuntimeError(self, message: str, stacktrace: str = ...) -> None:
        """
        Send a runtime error message back to the browser highlighted with in red
        
        :param message: Error message.
        :param stacktrace: Stacktrace information string
        """
        ...

    def Sample(self, time: datetime.datetime, force: bool = False) -> None:
        """
        Method to attempt to update the IResultHandler with various performance metrics.
        
        :param time: Current time
        :param force: Forces a sampling event if true
        """
        ...

    def SetAlgorithm(self, algorithm: QuantConnect.Interfaces.IAlgorithm, startingPortfolioValue: float) -> None:
        """
        Set the algorithm of the result handler after its been initialized.
        
        :param algorithm: Algorithm object matching IAlgorithm interface
        :param startingPortfolioValue: Algorithm starting capital for statistics calculations
        """
        ...

    def SetAlphaRuntimeStatistics(self, statistics: QuantConnect.AlphaRuntimeStatistics) -> None:
        """
        Sets the current alpha runtime statistics
        
        :param statistics: The current alpha runtime statistics
        """
        ...

    def SendStatusUpdate(self, status: QuantConnect.AlgorithmStatus, message: str = ...) -> None:
        """
        Send a algorithm status update to the user of the algorithms running state.
        
        :param status: Status enum of the algorithm.
        :param message: Optional string message describing reason for status change.
        """
        ...

    def RuntimeStatistic(self, key: str, value: str) -> None:
        """
        Set a dynamic runtime statistic to show in the (live) algorithm header
        
        :param key: Runtime headline statistic name
        :param value: Runtime headline statistic value
        """
        ...

    def OrderEvent(self, newEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Send a new order event.
        
        :param newEvent: Update, processing or cancellation of an order, update the IDE in live mode or ignore in backtesting.
        """
        ...

    def Exit(self) -> None:
        """Terminate the result thread and apply any required exit procedures like sending final results."""
        ...

    def ProcessSynchronousEvents(self, forceProcess: bool = False) -> None:
        """Process any synchronous events in here that are primarily triggered from the algorithm loop"""
        ...

    def SaveResults(self, name: str, result: QuantConnect.Result) -> None:
        """
        Save the results
        
        :param name: The name of the results
        :param result: The results to save
        """
        ...


class BacktestingResultHandler(QuantConnect.Lean.Engine.Results.BaseResultsHandler, QuantConnect.Lean.Engine.Results.IResultHandler):
    """Backtesting result handler passes messages back from the Lean to the User."""

    @property
    def FinalStatistics(self) -> System.Collections.Generic.Dictionary[str, str]:
        """A dictionary containing summary statistics"""
        ...

    @FinalStatistics.setter
    def FinalStatistics(self, value: System.Collections.Generic.Dictionary[str, str]):
        """A dictionary containing summary statistics"""
        ...

    def __init__(self) -> None:
        """Creates a new instance"""
        ...

    def Initialize(self, job: QuantConnect.Packets.AlgorithmNodePacket, messagingHandler: QuantConnect.Interfaces.IMessagingHandler, api: QuantConnect.Interfaces.IApi, transactionHandler: QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler) -> None:
        """
        Initialize the result handler with this result packet.
        
        :param job: Algorithm job packet for this result handler
        :param messagingHandler: The handler responsible for communicating messages to listeners
        :param api: The api instance used for handling logs
        :param transactionHandler: The transaction handler used to get the algorithms Order information
        """
        ...

    def Run(self) -> None:
        """
        The main processing method steps through the messaging queue and processes the messages one by one.
        
        This method is protected.
        """
        ...

    def SplitPackets(self, deltaCharts: System.Collections.Generic.Dictionary[str, QuantConnect.Chart], deltaOrders: System.Collections.Generic.Dictionary[int, QuantConnect.Orders.Order], runtimeStatistics: System.Collections.Generic.Dictionary[str, str], progress: float, serverStatistics: System.Collections.Generic.Dictionary[str, str]) -> System.Collections.Generic.IEnumerable[QuantConnect.Packets.BacktestResultPacket]:
        """Run over all the data and break it into smaller packets to ensure they all arrive at the terminal"""
        ...

    def StoreResult(self, packet: QuantConnect.Packets.Packet) -> None:
        """
        Save the snapshot of the total results to storage.
        
        This method is protected.
        
        :param packet: Packet to store.
        """
        ...

    def SendFinalResult(self) -> None:
        """
        Send a final analysis result back to the IDE.
        
        This method is protected.
        """
        ...

    def SetAlgorithm(self, algorithm: QuantConnect.Interfaces.IAlgorithm, startingPortfolioValue: float) -> None:
        """
        Set the Algorithm instance for ths result.
        
        :param algorithm: Algorithm we're working on.
        :param startingPortfolioValue: Algorithm starting capital for statistics calculations
        """
        ...

    def DebugMessage(self, message: str) -> None:
        """
        Send a debug message back to the browser console.
        
        :param message: Message we'd like shown in console.
        """
        ...

    def SystemDebugMessage(self, message: str) -> None:
        """
        Send a system debug message back to the browser console.
        
        :param message: Message we'd like shown in console.
        """
        ...

    def LogMessage(self, message: str) -> None:
        """
        Send a logging message to the log list for storage.
        
        :param message: Message we'd in the log.
        """
        ...

    def AddToLogStore(self, message: str) -> None:
        """This method is protected."""
        ...

    def SecurityType(self, types: System.Collections.Generic.List[QuantConnect.SecurityType]) -> None:
        """Send list of security asset types the algortihm uses to browser."""
        ...

    def ErrorMessage(self, message: str, stacktrace: str = ...) -> None:
        """
        Send an error message back to the browser highlighted in red with a stacktrace.
        
        :param message: Error message we'd like shown in console.
        :param stacktrace: Stacktrace information string
        """
        ...

    def RuntimeError(self, message: str, stacktrace: str = ...) -> None:
        """
        Send a runtime error message back to the browser highlighted with in red
        
        :param message: Error message.
        :param stacktrace: Stacktrace information string
        """
        ...

    def Sample(self, chartName: str, seriesName: str, seriesIndex: int, seriesType: QuantConnect.SeriesType, time: datetime.datetime, value: float, unit: str = "$") -> None:
        """
        Add a sample to the chart specified by the chartName, and seriesName.
        
        This method is protected.
        
        :param chartName: String chart name to place the sample.
        :param seriesName: Series name for the chart.
        :param seriesIndex: Type of chart we should create if it doesn't already exist.
        :param seriesType: Series type for the chart.
        :param time: Time for the sample
        :param value: Value for the chart sample.
        :param unit: Unit of the sample
        """
        ...

    def SampleEquity(self, time: datetime.datetime, value: float) -> None:
        """
        Sample the current equity of the strategy directly with time-value pair.
        
        This method is protected.
        
        :param time: Current backtest time.
        :param value: Current equity value.
        """
        ...

    def SampleRange(self, updates: System.Collections.Generic.List[QuantConnect.Chart]) -> None:
        """
        Add a range of samples from the users algorithms to the end of our current list.
        
        This method is protected.
        
        :param updates: Chart updates since the last request.
        """
        ...

    def Exit(self) -> None:
        """Terminate the result thread and apply any required exit procedures like sending final results."""
        ...

    def SendStatusUpdate(self, status: QuantConnect.AlgorithmStatus, message: str = ...) -> None:
        """
        Send an algorithm status update to the browser.
        
        :param status: Status enum value.
        :param message: Additional optional status message.
        """
        ...

    def RuntimeStatistic(self, key: str, value: str) -> None:
        """
        Set the current runtime statistics of the algorithm.
        These are banner/title statistics which show at the top of the live trading results.
        
        :param key: Runtime headline statistic name
        :param value: Runtime headline statistic value
        """
        ...

    def OrderEvent(self, newEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def ProcessSynchronousEvents(self, forceProcess: bool = False) -> None:
        """
        Process the synchronous result events, sampling and message reading.
        This method is triggered from the algorithm manager thread.
        """
        ...

    def ConfigureConsoleTextWriter(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        Configures the Console.Out and Console.ErrorTextWriter
        instances. By default, we forward Console.WriteLine(string) to IAlgorithm.Debug.
        This is perfect for running in the cloud, but since they're processed asynchronously, the ordering of these
        messages with respect to Log messages is broken. This can lead to differences in regression
        test logs based solely on the ordering of messages. To disable this forwarding, set "forward-console-messages"
        to false in the configuration.
        
        This method is protected.
        """
        ...


class RegressionResultHandler(QuantConnect.Lean.Engine.Results.BacktestingResultHandler):
    """
    Provides a wrapper over the BacktestingResultHandler that logs all order events
    to a separate file
    """

    @property
    def LogFilePath(self) -> str:
        """Gets the path used for logging all portfolio changing events, such as orders, TPV, daily holdings values"""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the RegressionResultHandler class"""
        ...

    def SetAlgorithm(self, algorithm: QuantConnect.Interfaces.IAlgorithm, startingPortfolioValue: float) -> None:
        """Initializes the stream writer using the algorithm's id (name) in the file path"""
        ...

    def SamplePerformance(self, time: datetime.datetime, value: float) -> None:
        """
        Runs on date changes, use this to log TPV and holdings values each day
        
        This method is protected.
        """
        ...

    def OrderEvent(self, newEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Log the order and order event to the dedicated log file for this regression algorithm
        
        :param newEvent: New order event details
        """
        ...

    def SetAlphaRuntimeStatistics(self, statistics: QuantConnect.AlphaRuntimeStatistics) -> None:
        """Perform daily logging of the alpha runtime statistics"""
        ...

    def SecurityType(self, types: System.Collections.Generic.List[QuantConnect.SecurityType]) -> None:
        """Send list of security asset types the algortihm uses to browser."""
        ...

    def DebugMessage(self, message: str) -> None:
        """
        Send a debug message back to the browser console.
        
        :param message: Message we'd like shown in console.
        """
        ...

    def ErrorMessage(self, message: str, stacktrace: str = ...) -> None:
        """
        Send an error message back to the browser highlighted in red with a stacktrace.
        
        :param message: Error message we'd like shown in console.
        :param stacktrace: Stacktrace information string
        """
        ...

    def LogMessage(self, message: str) -> None:
        """
        Send a logging message to the log list for storage.
        
        :param message: Message we'd in the log.
        """
        ...

    def RuntimeError(self, message: str, stacktrace: str = ...) -> None:
        """
        Send a runtime error message back to the browser highlighted with in red
        
        :param message: Error message.
        :param stacktrace: Stacktrace information string
        """
        ...

    def SystemDebugMessage(self, message: str) -> None:
        """
        Send a system debug message back to the browser console.
        
        :param message: Message we'd like shown in console.
        """
        ...

    def RuntimeStatistic(self, key: str, value: str) -> None:
        """
        Set the current runtime statistics of the algorithm.
        These are banner/title statistics which show at the top of the live trading results.
        
        :param key: Runtime headline statistic name
        :param value: Runtime headline statistic value
        """
        ...

    def AddToLogStore(self, message: str) -> None:
        """
        Save an algorithm message to the log store. Uses a different timestamped method of adding messaging to interweve debug and logging messages.
        
        This method is protected.
        
        :param message: String message to store
        """
        ...

    def OnSecuritiesChanged(self, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """Event fired each time that we add/remove securities from the data feed"""
        ...

    def ProcessSynchronousEvents(self, forceProcess: bool = False) -> None:
        """
        Runs at the end of each time loop. When HighFidelityLogging is enabled, we'll
        log each piece of data to allow for faster determination of regression causes
        """
        ...

    def SaveResults(self, name: str, result: QuantConnect.Result) -> None:
        """Save the results to disk"""
        ...

    def Exit(self) -> None:
        """
        Terminate the result thread and apply any required exit procedures.
        Save orders log files to disk.
        """
        ...

    def ConfigureConsoleTextWriter(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        We want to make algorithm messages end up in both the standard regression log file {algorithm}.{language}.log
        as well as the details log {algorithm}.{language}.details.log. The details log is focused on providing a log
        dedicated solely to the algorithm's behavior, void of all QuantConnect.Logging.Log messages
        
        This method is protected.
        """
        ...


class LiveTradingResultHandler(QuantConnect.Lean.Engine.Results.BaseResultsHandler, QuantConnect.Lean.Engine.Results.IResultHandler):
    """Live trading result handler implementation passes the messages to the QC live trading interface."""

    def __init__(self) -> None:
        """Creates a new instance"""
        ...

    def Initialize(self, job: QuantConnect.Packets.AlgorithmNodePacket, messagingHandler: QuantConnect.Interfaces.IMessagingHandler, api: QuantConnect.Interfaces.IApi, transactionHandler: QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler) -> None:
        """
        Initialize the result handler with this result packet.
        
        :param job: Algorithm job packet for this result handler
        :param messagingHandler: The handler responsible for communicating messages to listeners
        :param api: The api instance used for handling logs
        :param transactionHandler: The transaction handler used to get the algorithms Orders information
        """
        ...

    def Run(self) -> None:
        """
        Live trading result handler thread.
        
        This method is protected.
        """
        ...

    def StoreOrderEvents(self, utcTime: datetime.datetime, orderEvents: System.Collections.Generic.List[QuantConnect.Orders.OrderEvent]) -> None:
        """
        Stores the order events
        
        This method is protected.
        
        :param utcTime: The utc date associated with these order events
        :param orderEvents: The order events to store
        """
        ...

    def DebugMessage(self, message: str) -> None:
        """
        Send a live trading debug message to the live console.
        
        :param message: Message we'd like shown in console.
        """
        ...

    def SystemDebugMessage(self, message: str) -> None:
        """
        Send a live trading system debug message to the live console.
        
        :param message: Message we'd like shown in console.
        """
        ...

    def LogMessage(self, message: str) -> None:
        """
        Log string messages and send them to the console.
        
        :param message: String message wed like logged.
        """
        ...

    def AddToLogStore(self, message: str) -> None:
        """
        Save an algorithm message to the log store. Uses a different timestamped method of adding messaging to interweve debug and logging messages.
        
        This method is protected.
        
        :param message: String message to send to browser.
        """
        ...

    def ErrorMessage(self, message: str, stacktrace: str = ...) -> None:
        """
        Send an error message back to the browser console and highlight it read.
        
        :param message: Message we'd like shown in console.
        :param stacktrace: Stacktrace to show in the console.
        """
        ...

    def SecurityType(self, types: System.Collections.Generic.List[QuantConnect.SecurityType]) -> None:
        """
        Send a list of secutity types that the algorithm trades to the browser to show the market clock - is this market open or closed!
        
        :param types: List of security types
        """
        ...

    def RuntimeError(self, message: str, stacktrace: str = ...) -> None:
        """
        Send a runtime error back to the users browser and highlight it red.
        
        :param message: Runtime error message
        :param stacktrace: Associated error stack trace.
        """
        ...

    @typing.overload
    def Sample(self, chartName: str, seriesName: str, seriesIndex: int, seriesType: QuantConnect.SeriesType, time: datetime.datetime, value: float, unit: str = "$") -> None:
        """
        Add a sample to the chart specified by the chartName, and seriesName.
        
        This method is protected.
        
        :param chartName: String chart name to place the sample.
        :param seriesName: Series name for the chart.
        :param seriesIndex: Series chart index - which chart should this series belong
        :param seriesType: Series type for the chart.
        :param time: Time for the sample
        :param value: Value for the chart sample.
        :param unit: Unit for the chart axis
        """
        ...

    def SampleEquity(self, time: datetime.datetime, value: float) -> None:
        """
        Wrapper methond on sample to create the equity chart.
        
        This method is protected.
        
        :param time: Time of the sample.
        :param value: Equity value at this moment in time.
        """
        ...

    def SampleRange(self, updates: System.Collections.Generic.List[QuantConnect.Chart]) -> None:
        """
        Add a range of samples from the users algorithms to the end of our current list.
        
        This method is protected.
        
        :param updates: Chart updates since the last request.
        """
        ...

    def SetAlgorithm(self, algorithm: QuantConnect.Interfaces.IAlgorithm, startingPortfolioValue: float) -> None:
        """
        Set the algorithm of the result handler after its been initialized.
        
        :param algorithm: Algorithm object matching IAlgorithm interface
        :param startingPortfolioValue: Algorithm starting capital for statistics calculations
        """
        ...

    def SendStatusUpdate(self, status: QuantConnect.AlgorithmStatus, message: str = ...) -> None:
        """
        Send a algorithm status update to the user of the algorithms running state.
        
        :param status: Status enum of the algorithm.
        :param message: Optional string message describing reason for status change.
        """
        ...

    def RuntimeStatistic(self, key: str, value: str) -> None:
        """
        Set a dynamic runtime statistic to show in the (live) algorithm header
        
        :param key: Runtime headline statistic name
        :param value: Runtime headline statistic value
        """
        ...

    def SendFinalResult(self) -> None:
        """
        Send a final analysis result back to the IDE.
        
        This method is protected.
        """
        ...

    def SaveLogs(self, id: str, logs: System.Collections.Generic.List[QuantConnect.Logging.LogEntry]) -> str:
        """
        Process the log entries and save it to permanent storage
        
        :param id: Id that will be incorporated into the algorithm log name
        :param logs: Log list
        :returns: Returns the location of the logs.
        """
        ...

    def StoreResult(self, packet: QuantConnect.Packets.Packet) -> None:
        """
        Save the snapshot of the total results to storage.
        
        This method is protected.
        
        :param packet: Packet to store.
        """
        ...

    def OrderEvent(self, newEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        New order event for the algorithm
        
        :param newEvent: New event details
        """
        ...

    def Exit(self) -> None:
        """Terminate the result thread and apply any required exit procedures like sending final results"""
        ...

    def CreateSafeChartName(self, chartName: str) -> str:
        """
        Escape the chartname so that it can be saved to a file system
        
        This method is protected.
        
        :param chartName: The name of a chart
        :returns: The name of the chart will all escape all characters except RFC 2396 unreserved characters.
        """
        ...

    def ProcessSynchronousEvents(self, forceProcess: bool = False) -> None:
        """
        Process the synchronous result events, sampling and message reading.
        This method is triggered from the algorithm manager thread.
        """
        ...

    def OnSecuritiesChanged(self, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """
        Event fired each time that we add/remove securities from the data feed.
        On Security change we re determine when should we sample charts, if the user added Crypto, Forex or an extended market hours subscription
        we will always sample charts. Else, we will keep the exchange per market to query later on demand
        """
        ...

    @typing.overload
    def Sample(self, time: datetime.datetime, force: bool = False) -> None:
        """
        Samples portfolio equity, benchmark, and daily performance
        
        :param time: Current UTC time in the AlgorithmManager loop
        :param force: Force sampling of equity, benchmark, and performance to be
        """
        ...

    def GetPortfolioValue(self) -> float:
        """
        Gets the current portfolio value
        
        This method is protected.
        """
        ...

    def GetBenchmarkValue(self) -> float:
        """
        Gets the current benchmark value
        
        This method is protected.
        """
        ...


class CapacityEstimate(System.Object):
    """Estimates dollar volume capacity of algorithm (in account currency) using all Symbols in the portfolio."""

    @property
    def Capacity(self) -> float:
        """The total capacity of the strategy at a point in time"""
        ...

    @Capacity.setter
    def Capacity(self, value: float):
        """The total capacity of the strategy at a point in time"""
        ...

    def __init__(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        Initializes an instance of the class.
        
        :param algorithm: Used to get data at the current time step and access the portfolio state
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """Processes an order whenever it's encountered so that we can calculate the capacity"""
        ...

    def UpdateMarketCapacity(self, forceProcess: bool) -> None:
        """
        Updates the market capacity for any Symbols that require a market update.
        Sometimes, after the specified , we
        take a "snapshot" (point-in-time capacity) of the portfolio's capacity.
        
        This result will be written into the Algorithm Statistics via the BacktestingResultHandler
        """
        ...


