import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Api
import QuantConnect.Benchmarks
import QuantConnect.Brokerages
import QuantConnect.Data
import QuantConnect.Data.Auxiliary
import QuantConnect.Data.Market
import QuantConnect.Data.UniverseSelection
import QuantConnect.Interfaces
import QuantConnect.Notifications
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Scheduling
import QuantConnect.Securities
import QuantConnect.Securities.Future
import QuantConnect.Securities.Option
import QuantConnect.Statistics
import QuantConnect.Storage
import System
import System.Collections.Concurrent
import System.Collections.Generic
import System.IO
import System.Threading

System_EventHandler = typing.Any
QuantConnect_Interfaces_AlgorithmEvent = typing.Any

QuantConnect_Interfaces_IExtendedDictionary_TValue = typing.TypeVar("QuantConnect_Interfaces_IExtendedDictionary_TValue")
QuantConnect_Interfaces_IExtendedDictionary_TKey = typing.TypeVar("QuantConnect_Interfaces_IExtendedDictionary_TKey")
QuantConnect_Interfaces_IBusyCollection_T = typing.TypeVar("QuantConnect_Interfaces_IBusyCollection_T")


class IMessagingHandler(System.IDisposable, metaclass=abc.ABCMeta):
    """
    Messaging System Plugin Interface.
    Provides a common messaging pattern between desktop and cloud implementations of QuantConnect.
    """

    @property
    @abc.abstractmethod
    def HasSubscribers(self) -> bool:
        """
        Gets or sets whether this messaging handler has any current subscribers.
        When set to false, messages won't be sent.
        """
        ...

    @HasSubscribers.setter
    @abc.abstractmethod
    def HasSubscribers(self, value: bool):
        """
        Gets or sets whether this messaging handler has any current subscribers.
        When set to false, messages won't be sent.
        """
        ...

    def Initialize(self) -> None:
        """Initialize the Messaging System Plugin."""
        ...

    def SetAuthentication(self, job: QuantConnect.Packets.AlgorithmNodePacket) -> None:
        """Set the user communication channel"""
        ...

    def Send(self, packet: QuantConnect.Packets.Packet) -> None:
        """
        Send any message with a base type of Packet.
        
        :param packet: Packet of data to send via the messaging system plugin
        """
        ...

    def SendNotification(self, notification: QuantConnect.Notifications.Notification) -> None:
        """
        Send any notification with a base type of Notification.
        
        :param notification: The notification to be sent.
        """
        ...


class IDataCacheProvider(System.IDisposable, metaclass=abc.ABCMeta):
    """Defines a cache for data"""

    @property
    @abc.abstractmethod
    def IsDataEphemeral(self) -> bool:
        """Property indicating the data is temporary in nature and should not be cached"""
        ...

    def Fetch(self, key: str) -> System.IO.Stream:
        """
        Fetch data from the cache
        
        :param key: A string representing the key of the cached data
        :returns: An Stream of the cached data.
        """
        ...

    def Store(self, key: str, data: typing.List[int]) -> None:
        """
        Store the data in the cache
        
        :param key: The source of the data, used as a key to retrieve data in the cache
        :param data: The data to cache as a byte array
        """
        ...


class IPrimaryExchangeProvider(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetPrimaryExchange(self, securityIdentifier: QuantConnect.SecurityIdentifier) -> int:
        """
        Gets the primary exchange for a given security identifier
        
        :param securityIdentifier: The security identifier to get the primary exchange for
        :returns: Returns the primary exchange or null if not found. This method returns the int value of a member of the QuantConnect.PrimaryExchange enum.
        """
        ...


class IDataProviderEvents(metaclass=abc.ABCMeta):
    """Events related to data providers"""

    @property
    @abc.abstractmethod
    def InvalidConfigurationDetected(self) -> typing.List[System_EventHandler]:
        """Event fired when an invalid configuration has been detected"""
        ...

    @InvalidConfigurationDetected.setter
    @abc.abstractmethod
    def InvalidConfigurationDetected(self, value: typing.List[System_EventHandler]):
        """Event fired when an invalid configuration has been detected"""
        ...

    @property
    @abc.abstractmethod
    def NumericalPrecisionLimited(self) -> typing.List[System_EventHandler]:
        """Event fired when the numerical precision in the factor file has been limited"""
        ...

    @NumericalPrecisionLimited.setter
    @abc.abstractmethod
    def NumericalPrecisionLimited(self, value: typing.List[System_EventHandler]):
        """Event fired when the numerical precision in the factor file has been limited"""
        ...

    @property
    @abc.abstractmethod
    def DownloadFailed(self) -> typing.List[System_EventHandler]:
        """Event fired when there was an error downloading a remote file"""
        ...

    @DownloadFailed.setter
    @abc.abstractmethod
    def DownloadFailed(self, value: typing.List[System_EventHandler]):
        """Event fired when there was an error downloading a remote file"""
        ...

    @property
    @abc.abstractmethod
    def ReaderErrorDetected(self) -> typing.List[System_EventHandler]:
        """Event fired when there was an error reading the data"""
        ...

    @ReaderErrorDetected.setter
    @abc.abstractmethod
    def ReaderErrorDetected(self, value: typing.List[System_EventHandler]):
        """Event fired when there was an error reading the data"""
        ...

    @property
    @abc.abstractmethod
    def StartDateLimited(self) -> typing.List[System_EventHandler]:
        """Event fired when the start date has been limited"""
        ...

    @StartDateLimited.setter
    @abc.abstractmethod
    def StartDateLimited(self, value: typing.List[System_EventHandler]):
        """Event fired when the start date has been limited"""
        ...


class ISecurityInitializerProvider(metaclass=abc.ABCMeta):
    """Reduced interface which provides an instance which implements ISecurityInitializer"""

    @property
    @abc.abstractmethod
    def SecurityInitializer(self) -> QuantConnect.Securities.ISecurityInitializer:
        """Gets an instance that is to be used to initialize newly created securities."""
        ...


class ISubscriptionDataConfigProvider(metaclass=abc.ABCMeta):
    """Reduced interface which provides access to registered SubscriptionDataConfig"""

    def GetSubscriptionDataConfigs(self, symbol: typing.Union[QuantConnect.Symbol, str], includeInternalConfigs: bool = False) -> System.Collections.Generic.List[QuantConnect.Data.SubscriptionDataConfig]:
        """Gets a list of all registered SubscriptionDataConfig for a given Symbol"""
        ...


class ISubscriptionDataConfigService(QuantConnect.Interfaces.ISubscriptionDataConfigProvider, metaclass=abc.ABCMeta):
    """
    This interface exposes methods for creating a list of SubscriptionDataConfig for a given
    configuration
    """

    @property
    @abc.abstractmethod
    def AvailableDataTypes(self) -> System.Collections.Generic.Dictionary[QuantConnect.SecurityType, System.Collections.Generic.List[QuantConnect.TickType]]:
        """Gets the available data types"""
        ...

    @typing.overload
    def Add(self, dataType: typing.Type, symbol: typing.Union[QuantConnect.Symbol, str], resolution: typing.Optional[QuantConnect.Resolution] = None, fillForward: bool = True, extendedMarketHours: bool = False, isFilteredSubscription: bool = True, isInternalFeed: bool = False, isCustomData: bool = False, dataNormalizationMode: QuantConnect.DataNormalizationMode = ...) -> QuantConnect.Data.SubscriptionDataConfig:
        """
        Creates and adds a list of SubscriptionDataConfig for a given symbol and configuration.
        Can optionally pass in desired subscription data type to use.
        If the config already existed will return existing instance instead
        """
        ...

    @typing.overload
    def Add(self, symbol: typing.Union[QuantConnect.Symbol, str], resolution: typing.Optional[QuantConnect.Resolution] = None, fillForward: bool = True, extendedMarketHours: bool = False, isFilteredSubscription: bool = True, isInternalFeed: bool = False, isCustomData: bool = False, subscriptionDataTypes: System.Collections.Generic.List[System.Tuple[typing.Type, QuantConnect.TickType]] = None, dataNormalizationMode: QuantConnect.DataNormalizationMode = ...) -> System.Collections.Generic.List[QuantConnect.Data.SubscriptionDataConfig]:
        """
        Creates and adds a list of SubscriptionDataConfig for a given symbol and configuration.
        Can optionally pass in desired subscription data types to use.
        If the config already existed will return existing instance instead
        """
        ...

    def LookupSubscriptionConfigDataTypes(self, symbolSecurityType: QuantConnect.SecurityType, resolution: QuantConnect.Resolution, isCanonical: bool) -> System.Collections.Generic.List[System.Tuple[typing.Type, QuantConnect.TickType]]:
        """
        Get the data feed types for a given SecurityTypeResolution
        
        :param symbolSecurityType: The SecurityType used to determine the types
        :param resolution: The resolution of the data requested
        :param isCanonical: Indicates whether the security is Canonical (future and options)
        :returns: Types that should be added to the SubscriptionDataConfig.
        """
        ...


class ITimeInForceHandler(metaclass=abc.ABCMeta):
    """Handles the time in force for an order"""

    def IsOrderExpired(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> bool:
        """
        Checks if an order is expired
        
        :param security: The security matching the order
        :param order: The order to be checked
        :returns: Returns true if the order has expired, false otherwise.
        """
        ...

    def IsFillValid(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, fill: QuantConnect.Orders.OrderEvent) -> bool:
        """
        Checks if an order fill is valid
        
        :param security: The security matching the order
        :param order: The order to be checked
        :param fill: The order fill to be checked
        :returns: Returns true if the order fill can be emitted, false otherwise.
        """
        ...


class IHistoryProvider(QuantConnect.Interfaces.IDataProviderEvents, metaclass=abc.ABCMeta):
    """Provides historical data to an algorithm at runtime"""

    @property
    @abc.abstractmethod
    def DataPointCount(self) -> int:
        """Gets the total number of data points emitted by this history provider"""
        ...

    def Initialize(self, parameters: QuantConnect.Data.HistoryProviderInitializeParameters) -> None:
        """
        Initializes this history provider to work for the specified job
        
        :param parameters: The initialization parameters
        """
        ...

    def GetHistory(self, requests: System.Collections.Generic.IEnumerable[QuantConnect.Data.HistoryRequest], sliceTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Slice]:
        """
        Gets the history for the requested securities
        
        :param requests: The historical data requests
        :param sliceTimeZone: The time zone used when time stamping the slice instances
        :returns: An enumerable of the slices of data covering the span specified in each request.
        """
        ...


class IRegressionAlgorithmDefinition(metaclass=abc.ABCMeta):
    """
    Defines a C# algorithm as a regression algorithm to be run as part of the test suite.
    This interface also allows the algorithm to declare that it has versions in other languages
    that should yield identical results.
    """

    @property
    @abc.abstractmethod
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    @abc.abstractmethod
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    @abc.abstractmethod
    def ExpectedStatistics(self) -> System.Collections.Generic.Dictionary[str, str]:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...


class IAlgorithmSettings(metaclass=abc.ABCMeta):
    """User settings for the algorithm which can be changed in the IAlgorithm.Initialize method"""

    @property
    @abc.abstractmethod
    def RebalancePortfolioOnSecurityChanges(self) -> typing.Optional[bool]:
        """True if should rebalance portfolio on security changes. True by default"""
        ...

    @RebalancePortfolioOnSecurityChanges.setter
    @abc.abstractmethod
    def RebalancePortfolioOnSecurityChanges(self, value: typing.Optional[bool]):
        """True if should rebalance portfolio on security changes. True by default"""
        ...

    @property
    @abc.abstractmethod
    def RebalancePortfolioOnInsightChanges(self) -> typing.Optional[bool]:
        """True if should rebalance portfolio on new insights or expiration of insights. True by default"""
        ...

    @RebalancePortfolioOnInsightChanges.setter
    @abc.abstractmethod
    def RebalancePortfolioOnInsightChanges(self, value: typing.Optional[bool]):
        """True if should rebalance portfolio on new insights or expiration of insights. True by default"""
        ...

    @property
    @abc.abstractmethod
    def MaxAbsolutePortfolioTargetPercentage(self) -> float:
        """The absolute maximum valid total portfolio value target percentage"""
        ...

    @MaxAbsolutePortfolioTargetPercentage.setter
    @abc.abstractmethod
    def MaxAbsolutePortfolioTargetPercentage(self, value: float):
        """The absolute maximum valid total portfolio value target percentage"""
        ...

    @property
    @abc.abstractmethod
    def MinAbsolutePortfolioTargetPercentage(self) -> float:
        """The absolute minimum valid total portfolio value target percentage"""
        ...

    @MinAbsolutePortfolioTargetPercentage.setter
    @abc.abstractmethod
    def MinAbsolutePortfolioTargetPercentage(self, value: float):
        """The absolute minimum valid total portfolio value target percentage"""
        ...

    @property
    @abc.abstractmethod
    def FreePortfolioValue(self) -> float:
        """
        Gets/sets the SetHoldings buffers value.
        The buffer is used for orders not to be rejected due to volatility when using SetHoldings and CalculateOrderQuantity
        """
        ...

    @FreePortfolioValue.setter
    @abc.abstractmethod
    def FreePortfolioValue(self, value: float):
        """
        Gets/sets the SetHoldings buffers value.
        The buffer is used for orders not to be rejected due to volatility when using SetHoldings and CalculateOrderQuantity
        """
        ...

    @property
    @abc.abstractmethod
    def FreePortfolioValuePercentage(self) -> float:
        """
        Gets/sets the SetHoldings buffers value percentage.
        This percentage will be used to set the FreePortfolioValue
        based on the SecurityPortfolioManager.TotalPortfolioValue
        """
        ...

    @FreePortfolioValuePercentage.setter
    @abc.abstractmethod
    def FreePortfolioValuePercentage(self, value: float):
        """
        Gets/sets the SetHoldings buffers value percentage.
        This percentage will be used to set the FreePortfolioValue
        based on the SecurityPortfolioManager.TotalPortfolioValue
        """
        ...

    @property
    @abc.abstractmethod
    def LiquidateEnabled(self) -> bool:
        """Gets/sets if Liquidate() is enabled"""
        ...

    @LiquidateEnabled.setter
    @abc.abstractmethod
    def LiquidateEnabled(self, value: bool):
        """Gets/sets if Liquidate() is enabled"""
        ...

    @property
    @abc.abstractmethod
    def DataSubscriptionLimit(self) -> int:
        """Gets/sets the maximum number of concurrent market data subscriptions available"""
        ...

    @DataSubscriptionLimit.setter
    @abc.abstractmethod
    def DataSubscriptionLimit(self, value: int):
        """Gets/sets the maximum number of concurrent market data subscriptions available"""
        ...

    @property
    @abc.abstractmethod
    def StalePriceTimeSpan(self) -> datetime.timedelta:
        """Gets the minimum time span elapsed to consider a market fill price as stale (defaults to one hour)"""
        ...

    @StalePriceTimeSpan.setter
    @abc.abstractmethod
    def StalePriceTimeSpan(self, value: datetime.timedelta):
        """Gets the minimum time span elapsed to consider a market fill price as stale (defaults to one hour)"""
        ...


class IStreamReader(System.IDisposable, metaclass=abc.ABCMeta):
    """Defines a transport mechanism for data from its source into various reader methods"""

    @property
    @abc.abstractmethod
    def TransportMedium(self) -> int:
        """
        Gets the transport medium of this stream reader
        
        This property contains the int value of a member of the QuantConnect.SubscriptionTransportMedium enum.
        """
        ...

    @property
    @abc.abstractmethod
    def EndOfStream(self) -> bool:
        """Gets whether or not there's more data to be read in the stream"""
        ...

    @property
    @abc.abstractmethod
    def StreamReader(self) -> System.IO.StreamReader:
        """Direct access to the StreamReader instance"""
        ...

    @property
    @abc.abstractmethod
    def ShouldBeRateLimited(self) -> bool:
        """Gets whether or not this stream reader should be rate limited"""
        ...

    def ReadLine(self) -> str:
        """Gets the next line/batch of content from the stream"""
        ...


class IApi(System.IDisposable, metaclass=abc.ABCMeta):
    """API for QuantConnect.com"""

    def Initialize(self, userId: int, token: str, dataFolder: str) -> None:
        """Initialize the control system"""
        ...

    def CreateProject(self, name: str, language: QuantConnect.Language) -> QuantConnect.Api.ProjectResponse:
        """
        Create a project with the specified name and language via QuantConnect.com API
        
        :param name: Project name
        :param language: Programming language to use
        :returns: ProjectResponse that includes information about the newly created project.
        """
        ...

    def ReadProject(self, projectId: int) -> QuantConnect.Api.ProjectResponse:
        """
        Read in a project from the QuantConnect.com API.
        
        :param projectId: Project id you own
        :returns: ProjectResponse about a specific project.
        """
        ...

    def AddProjectFile(self, projectId: int, name: str, content: str) -> QuantConnect.Api.ProjectFilesResponse:
        """
        Add a file to a project
        
        :param projectId: The project to which the file should be added
        :param name: The name of the new file
        :param content: The content of the new file
        :returns: ProjectFilesResponse that includes information about the newly created file.
        """
        ...

    def UpdateProjectFileName(self, projectId: int, oldFileName: str, newFileName: str) -> QuantConnect.Api.RestResponse:
        """
        Update the name of a file
        
        :param projectId: Project id to which the file belongs
        :param oldFileName: The current name of the file
        :param newFileName: The new name for the file
        :returns: RestResponse indicating success.
        """
        ...

    def UpdateProjectFileContent(self, projectId: int, fileName: str, newFileContents: str) -> QuantConnect.Api.RestResponse:
        """
        Update the contents of a file
        
        :param projectId: Project id to which the file belongs
        :param fileName: The name of the file that should be updated
        :param newFileContents: The new contents of the file
        :returns: RestResponse indicating success.
        """
        ...

    def ReadProjectFile(self, projectId: int, fileName: str) -> QuantConnect.Api.ProjectFilesResponse:
        """
        Read a file in a project
        
        :param projectId: Project id to which the file belongs
        :param fileName: The name of the file
        :returns: ProjectFilesResponse that includes the file information.
        """
        ...

    def ReadProjectFiles(self, projectId: int) -> QuantConnect.Api.ProjectFilesResponse:
        """
        Read all files in a project
        
        :param projectId: Project id to which the file belongs
        :returns: ProjectFilesResponse that includes the information about all files in the project.
        """
        ...

    def DeleteProjectFile(self, projectId: int, name: str) -> QuantConnect.Api.RestResponse:
        """
        Delete a file in a project
        
        :param projectId: Project id to which the file belongs
        :param name: The name of the file that should be deleted
        :returns: ProjectFilesResponse that includes the information about all files in the project.
        """
        ...

    def DeleteProject(self, projectId: int) -> QuantConnect.Api.RestResponse:
        """
        Delete a specific project owned by the user from QuantConnect.com
        
        :param projectId: Project id we own and wish to delete
        :returns: RestResponse indicating success.
        """
        ...

    def ListProjects(self) -> QuantConnect.Api.ProjectResponse:
        """
        Read back a list of all projects on the account for a user.
        
        :returns: Container for list of projects.
        """
        ...

    def CreateCompile(self, projectId: int) -> QuantConnect.Api.Compile:
        """
        Create a new compile job request for this project id.
        
        :param projectId: Project id we wish to compile.
        :returns: Compile object result.
        """
        ...

    def ReadCompile(self, projectId: int, compileId: str) -> QuantConnect.Api.Compile:
        """
        Read a compile packet job result.
        
        :param projectId: Project id we sent for compile
        :param compileId: Compile id return from the creation request
        :returns: Compile object result.
        """
        ...

    def CreateBacktest(self, projectId: int, compileId: str, backtestName: str) -> QuantConnect.Api.Backtest:
        """Create a new backtest from a specified projectId and compileId"""
        ...

    def ReadBacktest(self, projectId: int, backtestId: str, getCharts: bool = True) -> QuantConnect.Api.Backtest:
        """
        Read out the full result of a specific backtest
        
        :param projectId: Project id for the backtest we'd like to read
        :param backtestId: Backtest id for the backtest we'd like to read
        :param getCharts: True will return backtest charts
        :returns: Backtest result object.
        """
        ...

    def UpdateBacktest(self, projectId: int, backtestId: str, backtestName: str = ..., backtestNote: str = ...) -> QuantConnect.Api.RestResponse:
        """
        Update the backtest name
        
        :param projectId: Project id to update
        :param backtestId: Backtest id to update
        :param backtestName: New backtest name to set
        :param backtestNote: Note attached to the backtest
        :returns: Rest response on success.
        """
        ...

    def DeleteBacktest(self, projectId: int, backtestId: str) -> QuantConnect.Api.RestResponse:
        """
        Delete a backtest from the specified project and backtestId.
        
        :param projectId: Project for the backtest we want to delete
        :param backtestId: Backtest id we want to delete
        :returns: RestResponse on success.
        """
        ...

    def ListBacktests(self, projectId: int) -> QuantConnect.Api.BacktestList:
        """
        Get a list of backtests for a specific project id
        
        :param projectId: Project id to search
        :returns: BacktestList container for list of backtests.
        """
        ...

    def ReadLiveLogs(self, projectId: int, algorithmId: str, startTime: typing.Optional[datetime.datetime] = None, endTime: typing.Optional[datetime.datetime] = None) -> QuantConnect.Api.LiveLog:
        """
        Gets the logs of a specific live algorithm
        
        :param projectId: Project Id of the live running algorithm
        :param algorithmId: Algorithm Id of the live running algorithm
        :param startTime: No logs will be returned before this time. Should be in UTC
        :param endTime: No logs will be returned after this time. Should be in UTC
        :returns: List of strings that represent the logs of the algorithm.
        """
        ...

    def ReadDataLink(self, symbol: typing.Union[QuantConnect.Symbol, str], resolution: QuantConnect.Resolution, date: datetime.datetime) -> QuantConnect.Api.Link:
        """
        Gets the link to the downloadable data.
        
        :param symbol: Symbol of security of which data will be requested.
        :param resolution: Resolution of data requested.
        :param date: Date of the data requested.
        :returns: Link to the downloadable data.
        """
        ...

    def DownloadData(self, symbol: typing.Union[QuantConnect.Symbol, str], resolution: QuantConnect.Resolution, date: datetime.datetime) -> bool:
        """
        Method to download and save the data purchased through QuantConnect
        
        :param symbol: Symbol of security of which data will be requested.
        :param resolution: Resolution of data requested.
        :param date: Date of the data requested.
        :returns: A bool indicating whether the data was successfully downloaded or not.
        """
        ...

    def CreateLiveAlgorithm(self, projectId: int, compileId: str, serverType: str, baseLiveAlgorithmSettings: QuantConnect.Api.BaseLiveAlgorithmSettings, versionId: str = "-1") -> QuantConnect.Api.LiveAlgorithm:
        """
        Create a new live algorithm for a logged in user.
        
        :param projectId: Id of the project on QuantConnect
        :param compileId: Id of the compilation on QuantConnect
        :param serverType: Type of server instance that will run the algorithm
        :param baseLiveAlgorithmSettings: Brokerage specific BaseLiveAlgorithmSettings.
        :param versionId: The version identifier
        :returns: Information regarding the new algorithm LiveAlgorithm.
        """
        ...

    def ListLiveAlgorithms(self, status: typing.Optional[QuantConnect.AlgorithmStatus] = None, startTime: typing.Optional[datetime.datetime] = None, endTime: typing.Optional[datetime.datetime] = None) -> QuantConnect.Api.LiveList:
        """
        Get a list of live running algorithms for a logged in user.
        
        :param status: Filter the statuses of the algorithms returned from the api
        :param startTime: Earliest launched time of the algorithms returned by the Api
        :param endTime: Latest launched time of the algorithms returned by the Api
        :returns: List of live algorithm instances.
        """
        ...

    def ReadLiveAlgorithm(self, projectId: int, deployId: str) -> QuantConnect.Api.LiveAlgorithmResults:
        """
        Read out a live algorithm in the project id specified.
        
        :param projectId: Project id to read
        :param deployId: Specific instance id to read
        :returns: Live object with the results.
        """
        ...

    def LiquidateLiveAlgorithm(self, projectId: int) -> QuantConnect.Api.RestResponse:
        """
        Liquidate a live algorithm from the specified project.
        
        :param projectId: Project for the live instance we want to stop
        """
        ...

    def StopLiveAlgorithm(self, projectId: int) -> QuantConnect.Api.RestResponse:
        """
        Stop a live algorithm from the specified project.
        
        :param projectId: Project for the live algo we want to delete
        """
        ...

    def GetAlgorithmStatus(self, algorithmId: str) -> QuantConnect.AlgorithmControl:
        ...

    def SetAlgorithmStatus(self, algorithmId: str, status: QuantConnect.AlgorithmStatus, message: str = ...) -> None:
        """
        Set the algorithm status from the worker to update the UX e.g. if there was an error.
        
        :param algorithmId: Algorithm id we're setting.
        :param status: Status enum of the current worker
        :param message: Message for the algorithm status event
        """
        ...

    def SendStatistics(self, algorithmId: str, unrealized: float, fees: float, netProfit: float, holdings: float, equity: float, netReturn: float, volume: float, trades: int, sharpe: float) -> None:
        """
        Send the statistics to storage for performance tracking.
        
        :param algorithmId: Identifier for algorithm
        :param unrealized: Unrealized gainloss
        :param fees: Total fees
        :param netProfit: Net profi
        :param holdings: Algorithm holdings
        :param equity: Total equity
        :param netReturn: Algorithm return
        :param volume: Volume traded
        :param trades: Total trades since inception
        :param sharpe: Sharpe ratio since inception
        """
        ...

    def SendUserEmail(self, algorithmId: str, subject: str, body: str) -> None:
        """
        Send an email to the user associated with the specified algorithm id
        
        :param algorithmId: The algorithm id
        :param subject: The email subject
        :param body: The email message body
        """
        ...

    def Download(self, address: str, headers: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[str, str]], userName: str, password: str) -> str:
        """
        Local implementation for downloading data to algorithms
        
        :param address: URL to download
        :param headers: KVP headers
        :param userName: Username for basic authentication
        :param password: Password for basic authentication
        """
        ...


class IDataChannelProvider(metaclass=abc.ABCMeta):
    """Specifies data channel settings"""

    def ShouldStreamSubscription(self, job: QuantConnect.Packets.LiveNodePacket, config: QuantConnect.Data.SubscriptionDataConfig) -> bool:
        """True if this subscription configuration should be streamed"""
        ...


class IAccountCurrencyProvider(metaclass=abc.ABCMeta):
    """A reduced interface for an account currency provider"""

    @property
    @abc.abstractmethod
    def AccountCurrency(self) -> str:
        """Gets the account currency"""
        ...


class ITimeKeeper(metaclass=abc.ABCMeta):
    """Interface implemented by TimeKeeper"""

    @property
    @abc.abstractmethod
    def UtcTime(self) -> datetime.datetime:
        """Gets the current time in UTC"""
        ...

    def AddTimeZone(self, timeZone: typing.Any) -> None:
        """Adds the specified time zone to this time keeper"""
        ...

    def GetLocalTimeKeeper(self, timeZone: typing.Any) -> QuantConnect.LocalTimeKeeper:
        """
        Gets the LocalTimeKeeper instance for the specified time zone
        
        :param timeZone: The time zone whose LocalTimeKeeper we seek
        :returns: The LocalTimeKeeper instance for the specified time zone.
        """
        ...


class ITradeBuilder(metaclass=abc.ABCMeta):
    """Generates trades from executions and market price updates"""

    @property
    @abc.abstractmethod
    def ClosedTrades(self) -> System.Collections.Generic.List[QuantConnect.Statistics.Trade]:
        """The list of closed trades"""
        ...

    def SetLiveMode(self, live: bool) -> None:
        """
        Sets the live mode flag
        
        :param live: The live mode flag
        """
        ...

    def HasOpenPosition(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Returns true if there is an open position for the symbol
        
        :param symbol: The symbol
        :returns: true if there is an open position for the symbol.
        """
        ...

    def SetMarketPrice(self, symbol: typing.Union[QuantConnect.Symbol, str], price: float) -> None:
        """Sets the current market price for the symbol"""
        ...

    def ProcessFill(self, fill: QuantConnect.Orders.OrderEvent, securityConversionRate: float, feeInAccountCurrency: float, multiplier: float = 1.0) -> None:
        """
        Processes a new fill, eventually creating new trades
        
        :param fill: The new fill order event
        :param securityConversionRate: The current security market conversion rate into the account currency
        :param feeInAccountCurrency: The current order fee in the account currency
        :param multiplier: The contract multiplier
        """
        ...


class IOptionChainProvider(metaclass=abc.ABCMeta):
    """Provides the full option chain for a given underlying."""

    def GetOptionContractList(self, symbol: typing.Union[QuantConnect.Symbol, str], date: datetime.datetime) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Gets the list of option contracts for a given underlying symbol
        
        :param symbol: The underlying symbol
        :param date: The date for which to request the option chain (only used in backtesting)
        :returns: The list of option contracts.
        """
        ...


class IFutureChainProvider(metaclass=abc.ABCMeta):
    """Provides the full future chain for a given underlying."""

    def GetFutureContractList(self, symbol: typing.Union[QuantConnect.Symbol, str], date: datetime.datetime) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Gets the list of future contracts for a given underlying symbol
        
        :param symbol: The underlying symbol
        :param date: The date for which to request the future chain (only used in backtesting)
        :returns: The list of future contracts.
        """
        ...


class IObjectStore(System.IDisposable, System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[str, typing.List[int]]], metaclass=abc.ABCMeta):
    """Provides object storage for data persistence."""

    @property
    @abc.abstractmethod
    def ErrorRaised(self) -> typing.List[System_EventHandler]:
        """Event raised each time there's an error"""
        ...

    @ErrorRaised.setter
    @abc.abstractmethod
    def ErrorRaised(self, value: typing.List[System_EventHandler]):
        """Event raised each time there's an error"""
        ...

    def Initialize(self, algorithmName: str, userId: int, projectId: int, userToken: str, controls: QuantConnect.Packets.Controls) -> None:
        """
        Initializes the object store
        
        :param algorithmName: The algorithm name
        :param userId: The user id
        :param projectId: The project id
        :param userToken: The user token
        :param controls: The job controls instance
        """
        ...

    def ContainsKey(self, key: str) -> bool:
        """
        Determines whether the store contains data for the specified key
        
        :param key: The object key
        :returns: True if the key was found.
        """
        ...

    def ReadBytes(self, key: str) -> typing.List[int]:
        """
        Returns the object data for the specified key
        
        :param key: The object key
        :returns: A byte array containing the data.
        """
        ...

    def SaveBytes(self, key: str, contents: typing.List[int]) -> bool:
        """
        Saves the object data for the specified key
        
        :param key: The object key
        :param contents: The object data
        :returns: True if the save operation was successful.
        """
        ...

    def Delete(self, key: str) -> bool:
        """
        Deletes the object data for the specified key
        
        :param key: The object key
        :returns: True if the delete operation was successful.
        """
        ...

    def GetFilePath(self, key: str) -> str:
        """
        Returns the file path for the specified key
        
        :param key: The object key
        :returns: The path for the file.
        """
        ...


class IAlgorithm(QuantConnect.Interfaces.ISecurityInitializerProvider, QuantConnect.Interfaces.IAccountCurrencyProvider, metaclass=abc.ABCMeta):
    """
    Interface for QuantConnect algorithm implementations. All algorithms must implement these
    basic members to allow interaction with the Lean Backtesting Engine.
    """

    @property
    @abc.abstractmethod
    def InsightsGenerated(self) -> typing.List[QuantConnect_Interfaces_AlgorithmEvent]:
        """Event fired when an algorithm generates a insight"""
        ...

    @InsightsGenerated.setter
    @abc.abstractmethod
    def InsightsGenerated(self, value: typing.List[QuantConnect_Interfaces_AlgorithmEvent]):
        """Event fired when an algorithm generates a insight"""
        ...

    @property
    @abc.abstractmethod
    def TimeKeeper(self) -> QuantConnect.Interfaces.ITimeKeeper:
        """Gets the time keeper instance"""
        ...

    @property
    @abc.abstractmethod
    def SubscriptionManager(self) -> QuantConnect.Data.SubscriptionManager:
        """
        Data subscription manager controls the information and subscriptions the algorithms recieves.
        Subscription configurations can be added through the Subscription Manager.
        """
        ...

    @property
    @abc.abstractmethod
    def Securities(self) -> QuantConnect.Securities.SecurityManager:
        """
        Security object collection class stores an array of objects representing representing each security/asset
        we have a subscription for.
        """
        ...

    @property
    @abc.abstractmethod
    def UniverseManager(self) -> QuantConnect.Securities.UniverseManager:
        """Gets the collection of universes for the algorithm"""
        ...

    @property
    @abc.abstractmethod
    def Portfolio(self) -> QuantConnect.Securities.SecurityPortfolioManager:
        """
        Security portfolio management class provides wrapper and helper methods for the Security.Holdings class such as
        IsLong, IsShort, TotalProfit
        """
        ...

    @property
    @abc.abstractmethod
    def Transactions(self) -> QuantConnect.Securities.SecurityTransactionManager:
        """Security transaction manager class controls the store and processing of orders."""
        ...

    @property
    @abc.abstractmethod
    def BrokerageModel(self) -> QuantConnect.Brokerages.IBrokerageModel:
        """Gets the brokerage model used to emulate a real brokerage"""
        ...

    @property
    @abc.abstractmethod
    def BrokerageMessageHandler(self) -> QuantConnect.Brokerages.IBrokerageMessageHandler:
        """
        Gets the brokerage message handler used to decide what to do
        with each message sent from the brokerage
        """
        ...

    @BrokerageMessageHandler.setter
    @abc.abstractmethod
    def BrokerageMessageHandler(self, value: QuantConnect.Brokerages.IBrokerageMessageHandler):
        """
        Gets the brokerage message handler used to decide what to do
        with each message sent from the brokerage
        """
        ...

    @property
    @abc.abstractmethod
    def Notify(self) -> QuantConnect.Notifications.NotificationManager:
        """Notification manager for storing and processing live event messages"""
        ...

    @property
    @abc.abstractmethod
    def Schedule(self) -> QuantConnect.Scheduling.ScheduleManager:
        """Gets schedule manager for adding/removing scheduled events"""
        ...

    @property
    @abc.abstractmethod
    def HistoryProvider(self) -> QuantConnect.Interfaces.IHistoryProvider:
        """Gets or sets the history provider for the algorithm"""
        ...

    @HistoryProvider.setter
    @abc.abstractmethod
    def HistoryProvider(self, value: QuantConnect.Interfaces.IHistoryProvider):
        """Gets or sets the history provider for the algorithm"""
        ...

    @property
    @abc.abstractmethod
    def Status(self) -> int:
        """
        Gets or sets the current status of the algorithm
        
        This property contains the int value of a member of the QuantConnect.AlgorithmStatus enum.
        """
        ...

    @Status.setter
    @abc.abstractmethod
    def Status(self, value: int):
        """
        Gets or sets the current status of the algorithm
        
        This property contains the int value of a member of the QuantConnect.AlgorithmStatus enum.
        """
        ...

    @property
    @abc.abstractmethod
    def IsWarmingUp(self) -> bool:
        """Gets whether or not this algorithm is still warming up"""
        ...

    @property
    @abc.abstractmethod
    def Name(self) -> str:
        """Public name for the algorithm."""
        ...

    @Name.setter
    @abc.abstractmethod
    def Name(self, value: str):
        """Public name for the algorithm."""
        ...

    @property
    @abc.abstractmethod
    def Time(self) -> datetime.datetime:
        """Current date/time in the algorithm's local time zone"""
        ...

    @property
    @abc.abstractmethod
    def TimeZone(self) -> typing.Any:
        """Gets the time zone of the algorithm"""
        ...

    @property
    @abc.abstractmethod
    def UtcTime(self) -> datetime.datetime:
        """Current date/time in UTC."""
        ...

    @property
    @abc.abstractmethod
    def StartDate(self) -> datetime.datetime:
        """Algorithm start date for backtesting, set by the SetStartDate methods."""
        ...

    @property
    @abc.abstractmethod
    def EndDate(self) -> datetime.datetime:
        """Get Requested Backtest End Date"""
        ...

    @property
    @abc.abstractmethod
    def AlgorithmId(self) -> str:
        """AlgorithmId for the backtest"""
        ...

    @property
    @abc.abstractmethod
    def LiveMode(self) -> bool:
        """Algorithm is running on a live server."""
        ...

    @property
    @abc.abstractmethod
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the subscription settings to be used when adding securities via universe selection"""
        ...

    @property
    @abc.abstractmethod
    def DebugMessages(self) -> System.Collections.Concurrent.ConcurrentQueue[str]:
        """Debug messages from the strategy:"""
        ...

    @property
    @abc.abstractmethod
    def ErrorMessages(self) -> System.Collections.Concurrent.ConcurrentQueue[str]:
        """Error messages from the strategy:"""
        ...

    @property
    @abc.abstractmethod
    def LogMessages(self) -> System.Collections.Concurrent.ConcurrentQueue[str]:
        """Log messages from the strategy:"""
        ...

    @property
    @abc.abstractmethod
    def RunTimeError(self) -> System.Exception:
        """Gets the run time error from the algorithm, or null if none was encountered."""
        ...

    @RunTimeError.setter
    @abc.abstractmethod
    def RunTimeError(self, value: System.Exception):
        """Gets the run time error from the algorithm, or null if none was encountered."""
        ...

    @property
    @abc.abstractmethod
    def RuntimeStatistics(self) -> System.Collections.Concurrent.ConcurrentDictionary[str, str]:
        """Customizable dynamic statistics displayed during live trading:"""
        ...

    @property
    @abc.abstractmethod
    def Benchmark(self) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Gets the function used to define the benchmark. This function will return
        the value of the benchmark at a requested date/time
        """
        ...

    @property
    @abc.abstractmethod
    def TradeBuilder(self) -> QuantConnect.Interfaces.ITradeBuilder:
        """Gets the Trade Builder to generate trades from executions"""
        ...

    @property
    @abc.abstractmethod
    def Settings(self) -> QuantConnect.Interfaces.IAlgorithmSettings:
        """Gets the user settings for the algorithm"""
        ...

    @property
    @abc.abstractmethod
    def OptionChainProvider(self) -> QuantConnect.Interfaces.IOptionChainProvider:
        """Gets the option chain provider, used to get the list of option contracts for an underlying symbol"""
        ...

    @property
    @abc.abstractmethod
    def FutureChainProvider(self) -> QuantConnect.Interfaces.IFutureChainProvider:
        """Gets the future chain provider, used to get the list of future contracts for an underlying symbol"""
        ...

    @property
    @abc.abstractmethod
    def ObjectStore(self) -> QuantConnect.Storage.ObjectStore:
        """Gets the object store, used for persistence"""
        ...

    @property
    @abc.abstractmethod
    def CurrentSlice(self) -> QuantConnect.Data.Slice:
        """Returns the current Slice object"""
        ...

    def Initialize(self) -> None:
        """Initialise the Algorithm and Prepare Required Data:"""
        ...

    def PostInitialize(self) -> None:
        """
        Called by setup handlers after Initialize and allows the algorithm a chance to organize
        the data gather in the Initialize method
        """
        ...

    def OnWarmupFinished(self) -> None:
        """Called when the algorithm has completed initialization and warm up."""
        ...

    def GetParameter(self, name: str) -> str:
        """
        Gets the parameter with the specified name. If a parameter
        with the specified name does not exist, null is returned
        
        :param name: The name of the parameter to get
        :returns: The value of the specified parameter, or null if not found.
        """
        ...

    def SetParameters(self, parameters: System.Collections.Generic.Dictionary[str, str]) -> None:
        """
        Sets the parameters from the dictionary
        
        :param parameters: Dictionary containing the parameter names to values
        """
        ...

    def Shortable(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float) -> bool:
        """
        Checks if the provided asset is shortable at the brokerage
        
        :param symbol: Symbol to check if it is shortable
        :param quantity: Order quantity to check if shortable
        """
        ...

    def SetBrokerageModel(self, brokerageModel: QuantConnect.Brokerages.IBrokerageModel) -> None:
        """
        Sets the brokerage model used to resolve transaction models, settlement models,
        and brokerage specified ordering behaviors.
        
        :param brokerageModel: The brokerage model used to emulate the real brokerage
        """
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnFrameworkData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Used to send data updates to algorithm framework models
        
        :param slice: The current data slice
        """
        ...

    def OnSecuritiesChanged(self, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """
        Event fired each time that we add/remove securities from the data feed
        
        :param changes: Security additions/removals for this time step
        """
        ...

    def OnFrameworkSecuritiesChanged(self, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """
        Used to send security changes to algorithm framework models
        
        :param changes: Security additions/removals for this time step
        """
        ...

    def OnEndOfTimeStep(self) -> None:
        """
        Invoked at the end of every time step. This allows the algorithm
        to process events before advancing to the next time step.
        """
        ...

    def Debug(self, message: str) -> None:
        """Send debug message"""
        ...

    def Log(self, message: str) -> None:
        """
        Save entry to the Log
        
        :param message: String message
        """
        ...

    def Error(self, message: str) -> None:
        """
        Send an error message for the algorithm
        
        :param message: String message
        """
        ...

    def OnMarginCall(self, requests: System.Collections.Generic.List[QuantConnect.Orders.SubmitOrderRequest]) -> None:
        """
        Margin call event handler. This method is called right before the margin call orders are placed in the market.
        
        :param requests: The orders to be executed to bring this algorithm within margin limits
        """
        ...

    def OnMarginCallWarning(self) -> None:
        """Margin call warning event handler. This method is called when Portfolio.MarginRemaining is under 5% of your Portfolio.TotalPortfolioValue"""
        ...

    @typing.overload
    def OnEndOfDay(self) -> None:
        """Call this method at the end of each day of data."""
        ...

    @typing.overload
    def OnEndOfDay(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> None:
        """Call this method at the end of each day of data."""
        ...

    def OnEndOfAlgorithm(self) -> None:
        """Call this event at the end of the algorithm running."""
        ...

    def OnOrderEvent(self, newEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        EXPERTS ONLY:: [-!-Async Code-!-]
        New order event handler: on order status changes (filled, partially filled, cancelled etc).
        
        :param newEvent: Event information
        """
        ...

    def OnAssignmentOrderEvent(self, assignmentEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Option assignment event handler. On an option assignment event for short legs the resulting information is passed to this method.
        
        :param assignmentEvent: Option exercise event details containing details of the assignment
        """
        ...

    def OnBrokerageMessage(self, messageEvent: QuantConnect.Brokerages.BrokerageMessageEvent) -> None:
        """Brokerage message event handler. This method is called for all types of brokerage messages."""
        ...

    def OnBrokerageDisconnect(self) -> None:
        """Brokerage disconnected event handler. This method is called when the brokerage connection is lost."""
        ...

    def OnBrokerageReconnect(self) -> None:
        """Brokerage reconnected event handler. This method is called when the brokerage connection is restored after a disconnection."""
        ...

    def SetDateTime(self, time: datetime.datetime) -> None:
        """Set the DateTime Frontier: This is the master time and is"""
        ...

    def SetStartDate(self, start: datetime.datetime) -> None:
        """
        Set the start date for the backtest
        
        :param start: Datetime Start date for backtest
        """
        ...

    def SetEndDate(self, end: datetime.datetime) -> None:
        """
        Set the end date for a backtest.
        
        :param end: Datetime value for end date
        """
        ...

    def SetAlgorithmId(self, algorithmId: str) -> None:
        """
        Set the algorithm Id for this backtest or live run. This can be used to identify the order and equity records.
        
        :param algorithmId: unique 32 character identifier for backtest or live server
        """
        ...

    def SetLocked(self) -> None:
        """Set the algorithm as initialized and locked. No more cash or security changes."""
        ...

    def GetLocked(self) -> bool:
        """Gets whether or not this algorithm has been locked and fully initialized"""
        ...

    def AddChart(self, chart: QuantConnect.Chart) -> None:
        """
        Add a Chart object to algorithm collection
        
        :param chart: Chart object to add to collection.
        """
        ...

    def GetChartUpdates(self, clearChartData: bool = False) -> System.Collections.Generic.List[QuantConnect.Chart]:
        """
        Get the chart updates since the last request:
        
        :returns: List of Chart Updates.
        """
        ...

    def AddSecurity(self, securityType: QuantConnect.SecurityType, symbol: str, resolution: typing.Optional[QuantConnect.Resolution], market: str, fillDataForward: bool, leverage: float, extendedMarketHours: bool) -> QuantConnect.Securities.Security:
        """
        Set a required SecurityType-symbol and resolution for algorithm
        
        :param securityType: SecurityType Enum: Equity, Commodity, FOREX or Future
        :param symbol: Symbol Representation of the MarketType, e.g. AAPL
        :param resolution: Resolution of the MarketType required: MarketData, Second or Minute
        :param market: The market the requested security belongs to, such as 'usa' or 'fxcm'
        :param fillDataForward: If true, returns the last available data even if none in that timeslice.
        :param leverage: leverage for this security
        :param extendedMarketHours: ExtendedMarketHours send in data from 4am - 8pm, not used for FOREX
        """
        ...

    def AddFutureContract(self, symbol: typing.Union[QuantConnect.Symbol, str], resolution: typing.Optional[QuantConnect.Resolution] = None, fillDataForward: bool = True, leverage: float = 0) -> QuantConnect.Securities.Future.Future:
        """
        Creates and adds a new single Future contract to the algorithm
        
        :param symbol: The futures contract symbol
        :param resolution: The Resolution of market data, Tick, Second, Minute, Hour, or Daily. Default is Resolution.Minute
        :param fillDataForward: If true, returns the last available data even if none in that timeslice. Default is true
        :param leverage: The requested leverage for this equity. Default is set by SecurityInitializer
        :returns: The new Future security.
        """
        ...

    def AddOptionContract(self, symbol: typing.Union[QuantConnect.Symbol, str], resolution: typing.Optional[QuantConnect.Resolution] = None, fillDataForward: bool = True, leverage: float = 0) -> QuantConnect.Securities.Option.Option:
        """
        Creates and adds a new single Option contract to the algorithm
        
        :param symbol: The option contract symbol
        :param resolution: The Resolution of market data, Tick, Second, Minute, Hour, or Daily. Default is Resolution.Minute
        :param fillDataForward: If true, returns the last available data even if none in that timeslice. Default is true
        :param leverage: The requested leverage for this equity. Default is set by SecurityInitializer
        :returns: The new Option security.
        """
        ...

    def RemoveSecurity(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Removes the security with the specified symbol. This will cancel all
        open orders and then liquidate any existing holdings
        
        :param symbol: The symbol of the security to be removed
        """
        ...

    def SetAccountCurrency(self, accountCurrency: str) -> None:
        """
        Sets the account currency cash symbol this algorithm is to manage.
        
        :param accountCurrency: The account currency cash symbol to set
        """
        ...

    @typing.overload
    def SetCash(self, startingCash: float) -> None:
        """
        Set the starting capital for the strategy
        
        :param startingCash: decimal starting capital, default $100,000
        """
        ...

    @typing.overload
    def SetCash(self, symbol: str, startingCash: float, conversionRate: float = 0) -> None:
        """
        Set the cash for the specified symbol
        
        :param symbol: The cash symbol to set
        :param startingCash: Decimal cash value of portfolio
        :param conversionRate: The current conversion rate for the
        """
        ...

    def Liquidate(self, symbolToLiquidate: typing.Union[QuantConnect.Symbol, str] = None, tag: str = "Liquidated") -> System.Collections.Generic.List[int]:
        """
        Liquidate your portfolio holdings:
        
        :param symbolToLiquidate: Specific asset to liquidate, defaults to all.
        :param tag: Custom tag to know who is calling this.
        :returns: list of order ids.
        """
        ...

    def SetLiveMode(self, live: bool) -> None:
        """
        Set live mode state of the algorithm run: Public setter for the algorithm property LiveMode.
        
        :param live: Bool live mode flag
        """
        ...

    def SetFinishedWarmingUp(self) -> None:
        """Sets IsWarmingUp to false to indicate this algorithm has finished its warm up"""
        ...

    def GetWarmupHistoryRequests(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.HistoryRequest]:
        """Gets the date/time warmup should begin"""
        ...

    def SetMaximumOrders(self, max: int) -> None:
        """
        Set the maximum number of orders the algortihm is allowed to process.
        
        :param max: Maximum order count int
        """
        ...

    def SetBrokerageMessageHandler(self, handler: QuantConnect.Brokerages.IBrokerageMessageHandler) -> None:
        """
        Sets the implementation used to handle messages from the brokerage.
        The default implementation will forward messages to debug or error
        and when a BrokerageMessageType.Error occurs, the algorithm
        is stopped.
        
        :param handler: The message handler to use
        """
        ...

    def SetHistoryProvider(self, historyProvider: QuantConnect.Interfaces.IHistoryProvider) -> None:
        """
        Set the historical data provider
        
        :param historyProvider: Historical data provider
        """
        ...

    def SetRunTimeError(self, exception: System.Exception) -> None:
        """
        Set the runtime error
        
        :param exception: Represents error that occur during execution
        """
        ...

    def SetStatus(self, status: QuantConnect.AlgorithmStatus) -> None:
        """
        Set the state of a live deployment
        
        :param status: Live deployment status
        """
        ...

    def SetAvailableDataTypes(self, availableDataTypes: System.Collections.Generic.Dictionary[QuantConnect.SecurityType, System.Collections.Generic.List[QuantConnect.TickType]]) -> None:
        """
        Set the available TickType supported by each SecurityType in SecurityManager
        
        :param availableDataTypes: >The different TickType each Security supports
        """
        ...

    def SetOptionChainProvider(self, optionChainProvider: QuantConnect.Interfaces.IOptionChainProvider) -> None:
        """
        Sets the option chain provider, used to get the list of option contracts for an underlying symbol
        
        :param optionChainProvider: The option chain provider
        """
        ...

    def SetFutureChainProvider(self, futureChainProvider: QuantConnect.Interfaces.IFutureChainProvider) -> None:
        """
        Sets the future chain provider, used to get the list of future contracts for an underlying symbol
        
        :param futureChainProvider: The future chain provider
        """
        ...

    def SetCurrentSlice(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Sets the current slice
        
        :param slice: The Slice object
        """
        ...

    def SetApi(self, api: QuantConnect.Interfaces.IApi) -> None:
        """
        Provide the API for the algorithm.
        
        :param api: Initiated API
        """
        ...

    def SetObjectStore(self, objectStore: QuantConnect.Interfaces.IObjectStore) -> None:
        """
        Sets the object store
        
        :param objectStore: The object store
        """
        ...


class IBrokerageCashSynchronizer(metaclass=abc.ABCMeta):
    """Defines live brokerage cash synchronization operations."""

    @property
    @abc.abstractmethod
    def LastSyncDateTimeUtc(self) -> datetime.datetime:
        """Gets the datetime of the last sync (UTC)"""
        ...

    def ShouldPerformCashSync(self, currentTimeUtc: datetime.datetime) -> bool:
        """
        Returns whether the brokerage should perform the cash synchronization
        
        :param currentTimeUtc: The current time (UTC)
        :returns: True if the cash sync should be performed.
        """
        ...

    def DisableCashSync(self) -> None:
        """Disable cash sync entirely"""
        ...

    def PerformCashSync(self, algorithm: QuantConnect.Interfaces.IAlgorithm, currentTimeUtc: datetime.datetime, getTimeSinceLastFill: typing.Callable[[], datetime.timedelta]) -> bool:
        """
        Synchronizes the cashbook with the brokerage account
        
        :param algorithm: The algorithm instance
        :param currentTimeUtc: The current time (UTC)
        :param getTimeSinceLastFill: A function which returns the time elapsed since the last fill
        :returns: True if the cash sync was performed successfully.
        """
        ...


class IAlgorithmSubscriptionManager(QuantConnect.Interfaces.ISubscriptionDataConfigService, metaclass=abc.ABCMeta):
    """AlgorithmSubscriptionManager interface will manage the subscriptions for the SubscriptionManager"""

    @property
    @abc.abstractmethod
    def SubscriptionManagerSubscriptions(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.SubscriptionDataConfig]:
        """Gets all the current data config subscriptions that are being processed for the SubscriptionManager"""
        ...

    def SubscriptionManagerCount(self) -> int:
        """Returns the amount of data config subscriptions processed for the SubscriptionManager"""
        ...


class IDataProvider(metaclass=abc.ABCMeta):
    """
    Fetches a remote file for a security.
    Must save the file to Globals.DataFolder.
    """

    def Fetch(self, key: str) -> System.IO.Stream:
        """
        Retrieves data to be used in an algorithm
        
        :param key: A string representing where the data is stored
        :returns: A Stream of the data requested.
        """
        ...


class IDataQueueHandler(System.IDisposable, metaclass=abc.ABCMeta):
    """Task requestor interface with cloud system"""

    @property
    @abc.abstractmethod
    def IsConnected(self) -> bool:
        """Returns whether the data provider is connected"""
        ...

    def Subscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig, newDataAvailableHandler: System_EventHandler) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """
        Subscribe to the specified configuration
        
        :param dataConfig: defines the parameters to subscribe to a data feed
        :param newDataAvailableHandler: handler to be fired on new data available
        :returns: The new enumerator for this subscription request.
        """
        ...

    def Unsubscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """
        Removes the specified configuration
        
        :param dataConfig: Subscription config to be removed
        """
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Sets the job we're subscribing for
        
        :param job: Job we're subscribing for
        """
        ...


class IExtendedDictionary(typing.Generic[QuantConnect_Interfaces_IExtendedDictionary_TKey, QuantConnect_Interfaces_IExtendedDictionary_TValue], metaclass=abc.ABCMeta):
    """Represents a generic collection of key/value pairs that implements python dictionary methods."""

    def clear(self) -> None:
        """Removes all keys and values from the IExtendedDictionary{TKey, TValue}."""
        ...

    def copy(self) -> typing.Any:
        """
        Creates a shallow copy of the IExtendedDictionary{TKey, TValue}.
        
        :returns: Returns a shallow copy of the dictionary. It doesn't modify the original dictionary.
        """
        ...

    @typing.overload
    def fromkeys(self, sequence: typing.List[QuantConnect_Interfaces_IExtendedDictionary_TKey]) -> typing.Any:
        """
        Creates a new dictionary from the given sequence of elements.
        
        :param sequence: Sequence of elements which is to be used as keys for the new dictionary
        :returns: Returns a new dictionary with the given sequence of elements as the keys of the dictionary.
        """
        ...

    @typing.overload
    def fromkeys(self, sequence: typing.List[QuantConnect_Interfaces_IExtendedDictionary_TKey], value: QuantConnect_Interfaces_IExtendedDictionary_TValue) -> typing.Any:
        """
        Creates a new dictionary from the given sequence of elements with a value provided by the user.
        
        :param sequence: Sequence of elements which is to be used as keys for the new dictionary
        :param value: Value which is set to each each element of the dictionary
        :returns: Returns a new dictionary with the given sequence of elements as the keys of the dictionary. Each element of the newly created dictionary is set to the provided value.
        """
        ...

    @typing.overload
    def get(self, key: QuantConnect_Interfaces_IExtendedDictionary_TKey) -> QuantConnect_Interfaces_IExtendedDictionary_TValue:
        """
        Returns the value for the specified key if key is in dictionary.
        
        :param key: Key to be searched in the dictionary
        :returns: The value for the specified key if key is in dictionary. None if the key is not found and value is not specified.
        """
        ...

    @typing.overload
    def get(self, key: QuantConnect_Interfaces_IExtendedDictionary_TKey, value: QuantConnect_Interfaces_IExtendedDictionary_TValue) -> QuantConnect_Interfaces_IExtendedDictionary_TValue:
        """
        Returns the value for the specified key if key is in dictionary.
        
        :param key: Key to be searched in the dictionary
        :param value: Value to be returned if the key is not found. The default value is null.
        :returns: The value for the specified key if key is in dictionary. value if the key is not found and value is specified.
        """
        ...

    def items(self) -> typing.Any:
        """
        Returns a view object that displays a list of dictionary's (key, value) tuple pairs.
        
        :returns: Returns a view object that displays a list of a given dictionary's (key, value) tuple pair.
        """
        ...

    def keys(self) -> typing.Any:
        """
        Returns a view object that displays a list of all the keys in the dictionary
        
        :returns: Returns a view object that displays a list of all the keys. When the dictionary is changed, the view object also reflect these changes.
        """
        ...

    def popitem(self) -> typing.Any:
        """
        Returns and removes an arbitrary element (key, value) pair from the dictionary.
        
        :returns: Returns an arbitrary element (key, value) pair from the dictionary removes an arbitrary element(the same element which is returned) from the dictionary. Note: Arbitrary elements and random elements are not same.The popitem() doesn't return a random element.
        """
        ...

    @typing.overload
    def setdefault(self, key: QuantConnect_Interfaces_IExtendedDictionary_TKey) -> QuantConnect_Interfaces_IExtendedDictionary_TValue:
        """
        Returns the value of a key (if the key is in dictionary). If not, it inserts key with a value to the dictionary.
        
        :param key: Key with null/None value is inserted to the dictionary if key is not in the dictionary.
        :returns: The value of the key if it is in the dictionary None if key is not in the dictionary.
        """
        ...

    @typing.overload
    def setdefault(self, key: QuantConnect_Interfaces_IExtendedDictionary_TKey, default_value: QuantConnect_Interfaces_IExtendedDictionary_TValue) -> QuantConnect_Interfaces_IExtendedDictionary_TValue:
        """
        Returns the value of a key (if the key is in dictionary). If not, it inserts key with a value to the dictionary.
        
        :param key: Key with a value default_value is inserted to the dictionary if key is not in the dictionary.
        :param default_value: Default value
        :returns: The value of the key if it is in the dictionary default_value if key is not in the dictionary and default_value is specified.
        """
        ...

    @typing.overload
    def pop(self, key: QuantConnect_Interfaces_IExtendedDictionary_TKey) -> QuantConnect_Interfaces_IExtendedDictionary_TValue:
        """
        Removes and returns an element from a dictionary having the given key.
        
        :param key: Key which is to be searched for removal
        :returns: If key is found - removed/popped element from the dictionary If key is not found - KeyError exception is raised.
        """
        ...

    @typing.overload
    def pop(self, key: QuantConnect_Interfaces_IExtendedDictionary_TKey, default_value: QuantConnect_Interfaces_IExtendedDictionary_TValue) -> QuantConnect_Interfaces_IExtendedDictionary_TValue:
        """
        Removes and returns an element from a dictionary having the given key.
        
        :param key: Key which is to be searched for removal
        :param default_value: Value which is to be returned when the key is not in the dictionary
        :returns: If key is found - removed/popped element from the dictionary If key is not found - value specified as the second argument(default).
        """
        ...

    def update(self, other: typing.Any) -> None:
        """
        Updates the dictionary with the elements from the another dictionary object or from an iterable of key/value pairs.
        The update() method adds element(s) to the dictionary if the key is not in the dictionary.If the key is in the dictionary, it updates the key with the new value.
        
        :param other: Takes either a dictionary or an iterable object of key/value pairs (generally tuples).
        """
        ...

    def values(self) -> typing.Any:
        """
        Returns a view object that displays a list of all the values in the dictionary.
        
        :returns: Returns a view object that displays a list of all values in a given dictionary.
        """
        ...


class IDownloadProvider(metaclass=abc.ABCMeta):
    """Wrapper on the API for downloading data for an algorithm."""

    def Download(self, address: str, headers: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[str, str]], userName: str, password: str) -> str:
        """
        Method for downloading data for an algorithm
        
        :param address: Source URL to download from
        :param headers: Headers to pass to the site
        :param userName: Username for basic authentication
        :param password: Password for basic authentication
        :returns: String contents of file.
        """
        ...


class IDataPermissionManager(metaclass=abc.ABCMeta):
    """Entity in charge of handling data permissions"""

    @property
    @abc.abstractmethod
    def DataChannelProvider(self) -> QuantConnect.Interfaces.IDataChannelProvider:
        """The data channel provider instance"""
        ...

    def Initialize(self, job: QuantConnect.Packets.AlgorithmNodePacket) -> None:
        """
        Initialize the data permission manager
        
        :param job: The job packet
        """
        ...

    def AssertConfiguration(self, subscriptionDataConfig: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """
        Will assert the requested configuration is valid for the current job
        
        :param subscriptionDataConfig: The data subscription configuration to assert
        """
        ...

    def GetResolution(self, preferredResolution: QuantConnect.Resolution) -> int:
        """
        Gets a valid resolution to use for internal subscriptions
        
        :returns: A permitted resolution for internal subscriptions. This method returns the int value of a member of the QuantConnect.Resolution enum.
        """
        ...


class ISecurityPrice(metaclass=abc.ABCMeta):
    """
    Reduced interface which allows setting and accessing
    price properties for a Security
    """

    @property
    @abc.abstractmethod
    def Price(self) -> float:
        """Get the current value of the security."""
        ...

    @property
    @abc.abstractmethod
    def Close(self) -> float:
        """If this uses trade bar data, return the most recent close."""
        ...

    @property
    @abc.abstractmethod
    def Volume(self) -> float:
        """Access to the volume of the equity today"""
        ...

    @property
    @abc.abstractmethod
    def BidPrice(self) -> float:
        """Gets the most recent bid price if available"""
        ...

    @property
    @abc.abstractmethod
    def BidSize(self) -> float:
        """Gets the most recent bid size if available"""
        ...

    @property
    @abc.abstractmethod
    def AskPrice(self) -> float:
        """Gets the most recent ask price if available"""
        ...

    @property
    @abc.abstractmethod
    def AskSize(self) -> float:
        """Gets the most recent ask size if available"""
        ...

    @property
    @abc.abstractmethod
    def OpenInterest(self) -> int:
        """Access to the open interest of the security today"""
        ...

    @property
    @abc.abstractmethod
    def Symbol(self) -> QuantConnect.Symbol:
        """Symbol for the asset."""
        ...

    def SetMarketPrice(self, data: QuantConnect.Data.BaseData) -> None:
        """
        Update any security properties based on the latest market data and time
        
        :param data: New data packet from LEAN
        """
        ...

    def Update(self, data: System.Collections.Generic.IReadOnlyList[QuantConnect.Data.BaseData], dataType: typing.Type, containsFillForwardData: typing.Optional[bool]) -> None:
        """
        Updates all of the security properties, such as price/OHLCV/bid/ask based
        on the data provided. Data is also stored into the security's data cache
        
        :param data: The security update data
        :param dataType: The data type
        :param containsFillForwardData: Flag indicating whether  contains any fill forward bar or not
        """
        ...

    def GetLastData(self) -> QuantConnect.Data.BaseData:
        """
        Get the last price update set to the security.
        
        :returns: BaseData object for this security.
        """
        ...


class IOptionPrice(QuantConnect.Interfaces.ISecurityPrice, metaclass=abc.ABCMeta):
    """
    Reduced interface for accessing Option
    specific price properties and methods
    """

    @property
    @abc.abstractmethod
    def Underlying(self) -> QuantConnect.Interfaces.ISecurityPrice:
        """Gets a reduced interface of the underlying security object."""
        ...

    def EvaluatePriceModel(self, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> QuantConnect.Securities.Option.OptionPriceModelResult:
        """
        Evaluates the specified option contract to compute a theoretical price, IV and greeks
        
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: An instance of OptionPriceModelResult containing the theoretical price of the specified option contract.
        """
        ...


class IJobQueueHandler(metaclass=abc.ABCMeta):
    """Task requestor interface with cloud system"""

    def Initialize(self, api: QuantConnect.Interfaces.IApi) -> None:
        """Initialize the internal state"""
        ...

    def NextJob(self, algorithmPath: str) -> QuantConnect.Packets.AlgorithmNodePacket:
        """
        Request the next task to run through the engine:
        
        :returns: Algorithm job to process.
        """
        ...

    def AcknowledgeJob(self, job: QuantConnect.Packets.AlgorithmNodePacket) -> None:
        """
        Signal task complete
        
        :param job: Work to do.
        """
        ...


class IOrderProperties(metaclass=abc.ABCMeta):
    """Contains additional properties and settings for an order"""

    @property
    @abc.abstractmethod
    def TimeInForce(self) -> QuantConnect.Orders.TimeInForce:
        """Defines the length of time over which an order will continue working before it is cancelled"""
        ...

    @TimeInForce.setter
    @abc.abstractmethod
    def TimeInForce(self, value: QuantConnect.Orders.TimeInForce):
        """Defines the length of time over which an order will continue working before it is cancelled"""
        ...

    def Clone(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Returns a new instance clone of this object"""
        ...


class IMapFileProvider(metaclass=abc.ABCMeta):
    """Provides instances of MapFileResolver at run time"""

    def Get(self, market: str) -> QuantConnect.Data.Auxiliary.MapFileResolver:
        """
        Gets a MapFileResolver representing all the map
        files for the specified market
        
        :param market: The equity market, for example, 'usa'
        :returns: A MapFileResolver containing all map files for the specified market.
        """
        ...


class IPriceProvider(metaclass=abc.ABCMeta):
    """Provides access to price data for a given asset"""

    def GetLastPrice(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> float:
        """
        Gets the latest price for a given asset
        
        :param symbol: The symbol
        :returns: The latest price.
        """
        ...


class IDataQueueUniverseProvider(metaclass=abc.ABCMeta):
    """
    This interface allows interested parties to lookup or enumerate the available symbols. Data source exposes it if this feature is available.
    Availability of a symbol doesn't imply that it is possible to trade it. This is a data source specific interface, not broker specific.
    """

    def LookupSymbols(self, symbol: typing.Union[QuantConnect.Symbol, str], includeExpired: bool, securityCurrency: str = None) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Method returns a collection of Symbols that are available at the data source.
        
        :param symbol: Symbol to lookup
        :param includeExpired: Include expired contracts
        :param securityCurrency: Expected security currency(if any)
        :returns: Enumerable of Symbols, that are associated with the provided Symbol.
        """
        ...

    def CanPerformSelection(self) -> bool:
        """
        Returns whether selection can take place or not.
        
        :returns: True if selection can take place.
        """
        ...


class IFactorFileProvider(metaclass=abc.ABCMeta):
    """Provides instances of FactorFile at run time"""

    def Get(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect.Data.Auxiliary.FactorFile:
        """
        Gets a FactorFile instance for the specified symbol, or null if not found
        
        :param symbol: The security's symbol whose factor file we seek
        :returns: The resolved factor file, or null if not found.
        """
        ...


class IBrokerage(QuantConnect.Interfaces.IBrokerageCashSynchronizer, System.IDisposable, metaclass=abc.ABCMeta):
    """
    Brokerage interface that defines the operations all brokerages must implement. The IBrokerage implementation
    must have a matching IBrokerageFactory implementation.
    """

    @property
    @abc.abstractmethod
    def OrderStatusChanged(self) -> typing.List[System_EventHandler]:
        """Event that fires each time an order is filled"""
        ...

    @OrderStatusChanged.setter
    @abc.abstractmethod
    def OrderStatusChanged(self, value: typing.List[System_EventHandler]):
        """Event that fires each time an order is filled"""
        ...

    @property
    @abc.abstractmethod
    def OptionPositionAssigned(self) -> typing.List[System_EventHandler]:
        """Event that fires each time a short option position is assigned"""
        ...

    @OptionPositionAssigned.setter
    @abc.abstractmethod
    def OptionPositionAssigned(self, value: typing.List[System_EventHandler]):
        """Event that fires each time a short option position is assigned"""
        ...

    @property
    @abc.abstractmethod
    def AccountChanged(self) -> typing.List[System_EventHandler]:
        """Event that fires each time a user's brokerage account is changed"""
        ...

    @AccountChanged.setter
    @abc.abstractmethod
    def AccountChanged(self, value: typing.List[System_EventHandler]):
        """Event that fires each time a user's brokerage account is changed"""
        ...

    @property
    @abc.abstractmethod
    def Message(self) -> typing.List[System_EventHandler]:
        """Event that fires when a message is received from the brokerage"""
        ...

    @Message.setter
    @abc.abstractmethod
    def Message(self, value: typing.List[System_EventHandler]):
        """Event that fires when a message is received from the brokerage"""
        ...

    @property
    @abc.abstractmethod
    def Name(self) -> str:
        """Gets the name of the brokerage"""
        ...

    @property
    @abc.abstractmethod
    def IsConnected(self) -> bool:
        """Returns true if we're currently connected to the broker"""
        ...

    @property
    @abc.abstractmethod
    def AccountInstantlyUpdated(self) -> bool:
        """Specifies whether the brokerage will instantly update account balances"""
        ...

    @property
    @abc.abstractmethod
    def AccountBaseCurrency(self) -> str:
        """Returns the brokerage account's base currency"""
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """
        Gets all open orders on the account
        
        :returns: The open orders returned from IB.
        """
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """
        Gets all holdings for the account
        
        :returns: The current holdings from the account.
        """
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """
        Gets the current cash balance for each currency held in the brokerage account
        
        :returns: The current cash balance for each currency available for trading.
        """
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Places a new order and assigns a new broker ID to the order
        
        :param order: The order to be placed
        :returns: True if the request for a new order has been placed, false otherwise.
        """
        ...

    def UpdateOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Updates the order with the same id
        
        :param order: The new order information
        :returns: True if the request was made for the order to be updated, false otherwise.
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was made for the order to be canceled, false otherwise.
        """
        ...

    def Connect(self) -> None:
        """Connects the client to the broker's remote servers"""
        ...

    def Disconnect(self) -> None:
        """Disconnects the client from the broker's remote servers"""
        ...

    def GetHistory(self, request: QuantConnect.Data.HistoryRequest) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Gets the history for the requested security
        
        :param request: The historical data request
        :returns: An enumerable of bars covering the span specified in the request.
        """
        ...


class IBrokerageFactory(System.IDisposable, metaclass=abc.ABCMeta):
    """Defines factory types for brokerages. Every IBrokerage is expected to also implement an IBrokerageFactory."""

    @property
    @abc.abstractmethod
    def BrokerageType(self) -> typing.Type:
        """Gets the type of brokerage produced by this factory"""
        ...

    @property
    @abc.abstractmethod
    def BrokerageData(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Gets the brokerage data required to run the brokerage from configuration/disk"""
        ...

    def GetBrokerageModel(self, orderProvider: QuantConnect.Securities.IOrderProvider) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        Gets a brokerage model that can be used to model this brokerage's unique behaviors
        
        :param orderProvider: The order provider
        """
        ...

    def CreateBrokerage(self, job: QuantConnect.Packets.LiveNodePacket, algorithm: QuantConnect.Interfaces.IAlgorithm) -> QuantConnect.Interfaces.IBrokerage:
        """
        Creates a new IBrokerage instance
        
        :param job: The job packet to create the brokerage for
        :param algorithm: The algorithm instance
        :returns: A new brokerage instance.
        """
        ...

    def CreateBrokerageMessageHandler(self, algorithm: QuantConnect.Interfaces.IAlgorithm, job: QuantConnect.Packets.AlgorithmNodePacket, api: QuantConnect.Interfaces.IApi) -> QuantConnect.Brokerages.IBrokerageMessageHandler:
        """Gets a brokerage message handler"""
        ...


class ObjectStoreErrorRaisedEventArgs(System.EventArgs):
    """Event arguments for the IObjectStore.ErrorRaised event"""

    @property
    def Error(self) -> System.Exception:
        """Gets the Exception that was raised"""
        ...

    def __init__(self, error: System.Exception) -> None:
        """
        Initializes a new instance of the ObjectStoreErrorRaisedEventArgs class
        
        :param error: The error that was raised
        """
        ...


class ISecurityService(metaclass=abc.ABCMeta):
    """This interface exposes methods for creating a new Security"""

    @typing.overload
    def CreateSecurity(self, symbol: typing.Union[QuantConnect.Symbol, str], subscriptionDataConfigList: System.Collections.Generic.List[QuantConnect.Data.SubscriptionDataConfig], leverage: float = 0, addToSymbolCache: bool = True) -> QuantConnect.Securities.Security:
        """Creates a new security"""
        ...

    @typing.overload
    def CreateSecurity(self, symbol: typing.Union[QuantConnect.Symbol, str], subscriptionDataConfig: QuantConnect.Data.SubscriptionDataConfig, leverage: float = 0, addToSymbolCache: bool = True) -> QuantConnect.Securities.Security:
        """Creates a new security"""
        ...


class IBusyCollection(typing.Generic[QuantConnect_Interfaces_IBusyCollection_T], System.IDisposable, metaclass=abc.ABCMeta):
    """Interface used to handle items being processed and communicate busy state"""

    @property
    @abc.abstractmethod
    def WaitHandle(self) -> System.Threading.WaitHandle:
        """
        Gets a wait handle that can be used to wait until this instance is done
        processing all of it's item
        """
        ...

    @property
    @abc.abstractmethod
    def Count(self) -> int:
        """Gets the number of items held within this collection"""
        ...

    @property
    @abc.abstractmethod
    def IsBusy(self) -> bool:
        """Returns true if processing, false otherwise"""
        ...

    @typing.overload
    def Add(self, item: QuantConnect_Interfaces_IBusyCollection_T) -> None:
        """
        Adds the items to this collection
        
        :param item: The item to be added
        """
        ...

    @typing.overload
    def Add(self, item: QuantConnect_Interfaces_IBusyCollection_T, cancellationToken: System.Threading.CancellationToken) -> None:
        """
        Adds the items to this collection
        
        :param item: The item to be added
        :param cancellationToken: A cancellation token to observer
        """
        ...

    def CompleteAdding(self) -> None:
        """Marks the collection as not accepting any more additions"""
        ...

    @typing.overload
    def GetConsumingEnumerable(self) -> System.Collections.Generic.IEnumerable[QuantConnect_Interfaces_IBusyCollection_T]:
        """
        Provides a consuming enumerable for items in this collection.
        
        :returns: An enumerable that removes and returns items from the collection.
        """
        ...

    @typing.overload
    def GetConsumingEnumerable(self, cancellationToken: System.Threading.CancellationToken) -> System.Collections.Generic.IEnumerable[QuantConnect_Interfaces_IBusyCollection_T]:
        """
        Provides a consuming enumerable for items in this collection.
        
        :param cancellationToken: A cancellation token to observer
        :returns: An enumerable that removes and returns items from the collection.
        """
        ...


class IShortableProvider(metaclass=abc.ABCMeta):
    """Defines a short list/easy-to-borrow provider"""

    def AllShortableSymbols(self, localTime: datetime.datetime) -> System.Collections.Generic.Dictionary[QuantConnect.Symbol, int]:
        """
        Gets all shortable Symbols at the given time
        
        :param localTime: Local time of the algorithm
        :returns: All shortable Symbols including the quantity shortable as a positive number at the given time. Null if all Symbols are shortable without restrictions.
        """
        ...

    def ShortableQuantity(self, symbol: typing.Union[QuantConnect.Symbol, str], localTime: datetime.datetime) -> typing.Optional[int]:
        """
        Gets the quantity shortable for a Symbol.
        
        :param symbol: Symbol to check shortable quantity
        :param localTime: Local time of the algorithm
        :returns: The quantity shortable for the given Symbol as a positive number. Null if the Symbol is shortable without restrictions.
        """
        ...


