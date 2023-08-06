import datetime
import typing

import QuantConnect
import QuantConnect.Api
import QuantConnect.Interfaces
import QuantConnect.Packets
import QuantConnect.Statistics
import System
import System.Collections.Generic

JsonConverter = typing.Any

QuantConnect_Api_ApiConnection_TryRequest_T = typing.TypeVar("QuantConnect_Api_ApiConnection_TryRequest_T")


class ApiConnection(System.Object):
    """API Connection and Hash Manager"""

    @property
    def Client(self) -> typing.Any:
        """Authorized client to use for requests."""
        ...

    @Client.setter
    def Client(self, value: typing.Any):
        """Authorized client to use for requests."""
        ...

    @property
    def Connected(self) -> bool:
        """Return true if connected successfully."""
        ...

    def __init__(self, userId: int, token: str) -> None:
        """
        Create a new Api Connection Class.
        
        :param userId: User Id number from QuantConnect.com account. Found at www.quantconnect.com/account
        :param token: Access token for the QuantConnect account. Found at www.quantconnect.com/account
        """
        ...

    def TryRequest(self, request: typing.Any, result: QuantConnect_Api_ApiConnection_TryRequest_T) -> bool:
        """
        Place a secure request and get back an object of type T.
        
        :param result: Result object from the
        :returns: T typed object response.
        """
        ...


class RestResponse(System.Object):
    """Base API response class for the QuantConnect API."""

    @property
    def Success(self) -> bool:
        """Indicate if the API request was successful."""
        ...

    @Success.setter
    def Success(self, value: bool):
        """Indicate if the API request was successful."""
        ...

    @property
    def Errors(self) -> System.Collections.Generic.List[str]:
        """List of errors with the API call."""
        ...

    @Errors.setter
    def Errors(self, value: System.Collections.Generic.List[str]):
        """List of errors with the API call."""
        ...

    def __init__(self) -> None:
        """JSON Constructor"""
        ...


class Project(QuantConnect.Api.RestResponse):
    """Response from reading a project by id."""

    @property
    def ProjectId(self) -> int:
        """Project id"""
        ...

    @ProjectId.setter
    def ProjectId(self, value: int):
        """Project id"""
        ...

    @property
    def Name(self) -> str:
        """Name of the project"""
        ...

    @Name.setter
    def Name(self, value: str):
        """Name of the project"""
        ...

    @property
    def Created(self) -> datetime.datetime:
        """Date the project was created"""
        ...

    @Created.setter
    def Created(self, value: datetime.datetime):
        """Date the project was created"""
        ...

    @property
    def Modified(self) -> datetime.datetime:
        """Modified date for the project"""
        ...

    @Modified.setter
    def Modified(self, value: datetime.datetime):
        """Modified date for the project"""
        ...

    @property
    def Language(self) -> QuantConnect.Language:
        """Programming language of the project"""
        ...

    @Language.setter
    def Language(self, value: QuantConnect.Language):
        """Programming language of the project"""
        ...


class ProjectResponse(QuantConnect.Api.RestResponse):
    """Project list response"""

    @property
    def Projects(self) -> System.Collections.Generic.List[QuantConnect.Api.Project]:
        """List of projects for the authenticated user"""
        ...

    @Projects.setter
    def Projects(self, value: System.Collections.Generic.List[QuantConnect.Api.Project]):
        """List of projects for the authenticated user"""
        ...


class ProjectFile(System.Object):
    """File for a project"""

    @property
    def Name(self) -> str:
        """Name of a project file"""
        ...

    @Name.setter
    def Name(self, value: str):
        """Name of a project file"""
        ...

    @property
    def Code(self) -> str:
        """Contents of the project file"""
        ...

    @Code.setter
    def Code(self, value: str):
        """Contents of the project file"""
        ...

    @property
    def DateModified(self) -> datetime.datetime:
        """DateTime project file was modified"""
        ...

    @DateModified.setter
    def DateModified(self, value: datetime.datetime):
        """DateTime project file was modified"""
        ...


class ProjectFilesResponse(QuantConnect.Api.RestResponse):
    """Response received when reading all files of a project"""

    @property
    def Files(self) -> System.Collections.Generic.List[QuantConnect.Api.ProjectFile]:
        """List of project file information"""
        ...

    @Files.setter
    def Files(self, value: System.Collections.Generic.List[QuantConnect.Api.ProjectFile]):
        """List of project file information"""
        ...


class CompileState(System.Enum):
    """State of the compilation request"""

    InQueue = 0
    """Compile waiting in the queue to be processed."""

    BuildSuccess = 1
    """Compile was built successfully"""

    BuildError = 2
    """Build error, check logs for more information"""


class Compile(QuantConnect.Api.RestResponse):
    """Response from the compiler on a build event"""

    @property
    def CompileId(self) -> str:
        """Compile Id for a sucessful build"""
        ...

    @CompileId.setter
    def CompileId(self, value: str):
        """Compile Id for a sucessful build"""
        ...

    @property
    def State(self) -> QuantConnect.Api.CompileState:
        """True on successful compile"""
        ...

    @State.setter
    def State(self, value: QuantConnect.Api.CompileState):
        """True on successful compile"""
        ...

    @property
    def Logs(self) -> System.Collections.Generic.List[str]:
        """Logs of the compilation request"""
        ...

    @Logs.setter
    def Logs(self, value: System.Collections.Generic.List[str]):
        """Logs of the compilation request"""
        ...


class Backtest(QuantConnect.Api.RestResponse):
    """Backtest response packet from the QuantConnect.com API."""

    @property
    def Name(self) -> str:
        """Name of the backtest"""
        ...

    @Name.setter
    def Name(self, value: str):
        """Name of the backtest"""
        ...

    @property
    def Note(self) -> str:
        """Note on the backtest attached by the user"""
        ...

    @Note.setter
    def Note(self, value: str):
        """Note on the backtest attached by the user"""
        ...

    @property
    def BacktestId(self) -> str:
        """Assigned backtest Id"""
        ...

    @BacktestId.setter
    def BacktestId(self, value: str):
        """Assigned backtest Id"""
        ...

    @property
    def Completed(self) -> bool:
        """Boolean true when the backtest is completed."""
        ...

    @Completed.setter
    def Completed(self, value: bool):
        """Boolean true when the backtest is completed."""
        ...

    @property
    def Progress(self) -> float:
        """Progress of the backtest in percent 0-1."""
        ...

    @Progress.setter
    def Progress(self, value: float):
        """Progress of the backtest in percent 0-1."""
        ...

    @property
    def Error(self) -> str:
        """Backtest error message"""
        ...

    @Error.setter
    def Error(self, value: str):
        """Backtest error message"""
        ...

    @property
    def StackTrace(self) -> str:
        """Backtest error stacktrace"""
        ...

    @StackTrace.setter
    def StackTrace(self, value: str):
        """Backtest error stacktrace"""
        ...

    @property
    def Created(self) -> datetime.datetime:
        """Backtest creation date and time"""
        ...

    @Created.setter
    def Created(self, value: datetime.datetime):
        """Backtest creation date and time"""
        ...

    @property
    def RollingWindow(self) -> System.Collections.Generic.Dictionary[str, QuantConnect.Statistics.AlgorithmPerformance]:
        """Rolling window detailed statistics."""
        ...

    @RollingWindow.setter
    def RollingWindow(self, value: System.Collections.Generic.Dictionary[str, QuantConnect.Statistics.AlgorithmPerformance]):
        """Rolling window detailed statistics."""
        ...

    @property
    def TotalPerformance(self) -> QuantConnect.Statistics.AlgorithmPerformance:
        """Rolling window detailed statistics."""
        ...

    @TotalPerformance.setter
    def TotalPerformance(self, value: QuantConnect.Statistics.AlgorithmPerformance):
        """Rolling window detailed statistics."""
        ...

    @property
    def AlphaRuntimeStatistics(self) -> QuantConnect.AlphaRuntimeStatistics:
        """Contains population averages scores over the life of the algorithm"""
        ...

    @AlphaRuntimeStatistics.setter
    def AlphaRuntimeStatistics(self, value: QuantConnect.AlphaRuntimeStatistics):
        """Contains population averages scores over the life of the algorithm"""
        ...

    @property
    def Charts(self) -> System.Collections.Generic.IDictionary[str, QuantConnect.Chart]:
        """Charts updates for the live algorithm since the last result packet"""
        ...

    @Charts.setter
    def Charts(self, value: System.Collections.Generic.IDictionary[str, QuantConnect.Chart]):
        """Charts updates for the live algorithm since the last result packet"""
        ...

    @property
    def Statistics(self) -> System.Collections.Generic.IDictionary[str, str]:
        """Statistics information sent during the algorithm operations."""
        ...

    @Statistics.setter
    def Statistics(self, value: System.Collections.Generic.IDictionary[str, str]):
        """Statistics information sent during the algorithm operations."""
        ...

    @property
    def RuntimeStatistics(self) -> System.Collections.Generic.IDictionary[str, str]:
        """Runtime banner/updating statistics in the title banner of the live algorithm GUI."""
        ...

    @RuntimeStatistics.setter
    def RuntimeStatistics(self, value: System.Collections.Generic.IDictionary[str, str]):
        """Runtime banner/updating statistics in the title banner of the live algorithm GUI."""
        ...


class BacktestList(QuantConnect.Api.RestResponse):
    """Collection container for a list of backtests for a project"""

    @property
    def Backtests(self) -> System.Collections.Generic.List[QuantConnect.Api.Backtest]:
        """Collection of summarized backtest objects"""
        ...

    @Backtests.setter
    def Backtests(self, value: System.Collections.Generic.List[QuantConnect.Api.Backtest]):
        """Collection of summarized backtest objects"""
        ...


class LiveAlgorithm(QuantConnect.Api.RestResponse):
    """Live algorithm instance result from the QuantConnect Rest API."""

    @property
    def ProjectId(self) -> int:
        """Project id for the live instance"""
        ...

    @ProjectId.setter
    def ProjectId(self, value: int):
        """Project id for the live instance"""
        ...

    @property
    def DeployId(self) -> str:
        """Unique live algorithm deployment identifier (similar to a backtest id)."""
        ...

    @DeployId.setter
    def DeployId(self, value: str):
        """Unique live algorithm deployment identifier (similar to a backtest id)."""
        ...

    @property
    def Status(self) -> QuantConnect.AlgorithmStatus:
        """Algorithm status: running, stopped or runtime error."""
        ...

    @Status.setter
    def Status(self, value: QuantConnect.AlgorithmStatus):
        """Algorithm status: running, stopped or runtime error."""
        ...

    @property
    def Launched(self) -> datetime.datetime:
        """Datetime the algorithm was launched in UTC."""
        ...

    @Launched.setter
    def Launched(self, value: datetime.datetime):
        """Datetime the algorithm was launched in UTC."""
        ...

    @property
    def Stopped(self) -> typing.Optional[datetime.datetime]:
        """Datetime the algorithm was stopped in UTC, null if its still running."""
        ...

    @Stopped.setter
    def Stopped(self, value: typing.Optional[datetime.datetime]):
        """Datetime the algorithm was stopped in UTC, null if its still running."""
        ...

    @property
    def Brokerage(self) -> str:
        """Brokerage"""
        ...

    @Brokerage.setter
    def Brokerage(self, value: str):
        """Brokerage"""
        ...

    @property
    def Subscription(self) -> str:
        """Chart we're subscribed to"""
        ...

    @Subscription.setter
    def Subscription(self, value: str):
        """Chart we're subscribed to"""
        ...

    @property
    def Error(self) -> str:
        """Live algorithm error message from a crash or algorithm runtime error."""
        ...

    @Error.setter
    def Error(self, value: str):
        """Live algorithm error message from a crash or algorithm runtime error."""
        ...


class BaseLiveAlgorithmSettings(System.Object):
    """Base class for settings that must be configured per Brokerage to create new algorithms via the API."""

    @property
    def Id(self) -> str:
        """'Interactive' / 'FXCM' / 'Oanda' / 'Tradier' /'PaperTrading'"""
        ...

    @Id.setter
    def Id(self, value: str):
        """'Interactive' / 'FXCM' / 'Oanda' / 'Tradier' /'PaperTrading'"""
        ...

    @property
    def User(self) -> str:
        """Username associated with brokerage"""
        ...

    @User.setter
    def User(self, value: str):
        """Username associated with brokerage"""
        ...

    @property
    def Password(self) -> str:
        """Password associated with brokerage"""
        ...

    @Password.setter
    def Password(self, value: str):
        """Password associated with brokerage"""
        ...

    @property
    def Environment(self) -> int:
        """
        'live'/'paper'
        
        This property contains the int value of a member of the QuantConnect.BrokerageEnvironment enum.
        """
        ...

    @Environment.setter
    def Environment(self, value: int):
        """
        'live'/'paper'
        
        This property contains the int value of a member of the QuantConnect.BrokerageEnvironment enum.
        """
        ...

    @property
    def Account(self) -> str:
        """Account of the associated brokerage"""
        ...

    @Account.setter
    def Account(self, value: str):
        """Account of the associated brokerage"""
        ...

    @typing.overload
    def __init__(self, user: str, password: str, environment: QuantConnect.BrokerageEnvironment, account: str) -> None:
        """
        Constructor used by FXCM
        
        :param user: Username associated with brokerage
        :param password: Password associated with brokerage
        :param environment: 'live'/'paper'
        :param account: Account id for brokerage
        """
        ...

    @typing.overload
    def __init__(self, user: str, password: str) -> None:
        """
        Constructor used by Interactive Brokers
        
        :param user: Username associated with brokerage
        :param password: Password associated with brokerage
        """
        ...

    @typing.overload
    def __init__(self, environment: QuantConnect.BrokerageEnvironment, account: str) -> None:
        """
        The constructor used by Oanda
        
        :param environment: 'live'/'paper'
        :param account: Account id for brokerage
        """
        ...

    @typing.overload
    def __init__(self, account: str) -> None:
        """
        The constructor used by Tradier
        
        :param account: Account id for brokerage
        """
        ...

    @typing.overload
    def __init__(self) -> None:
        """The constructor used by Bitfinex"""
        ...


class LiveList(QuantConnect.Api.RestResponse):
    """List of the live algorithms running which match the requested status"""

    @property
    def Algorithms(self) -> System.Collections.Generic.List[QuantConnect.Api.LiveAlgorithm]:
        """Algorithm list matching the requested status."""
        ...

    @Algorithms.setter
    def Algorithms(self, value: System.Collections.Generic.List[QuantConnect.Api.LiveAlgorithm]):
        """Algorithm list matching the requested status."""
        ...


class LiveResultsData(System.Object):
    """Holds information about the state and operation of the live running algorithm"""

    @property
    def Version(self) -> int:
        """Results version"""
        ...

    @Version.setter
    def Version(self, value: int):
        """Results version"""
        ...

    @property
    def Resolution(self) -> int:
        """
        Temporal resolution of the results returned from the Api
        
        This property contains the int value of a member of the QuantConnect.Resolution enum.
        """
        ...

    @Resolution.setter
    def Resolution(self, value: int):
        """
        Temporal resolution of the results returned from the Api
        
        This property contains the int value of a member of the QuantConnect.Resolution enum.
        """
        ...

    @property
    def Results(self) -> QuantConnect.Packets.LiveResult:
        """Class to represent the data groups results return from the Api"""
        ...

    @Results.setter
    def Results(self, value: QuantConnect.Packets.LiveResult):
        """Class to represent the data groups results return from the Api"""
        ...


class LiveAlgorithmResults(QuantConnect.Api.RestResponse):
    """Details a live algorithm from the "live/read" Api endpoint"""

    @property
    def LiveResults(self) -> QuantConnect.Api.LiveResultsData:
        """Represents data about the live running algorithm returned from the server"""
        ...

    @LiveResults.setter
    def LiveResults(self, value: QuantConnect.Api.LiveResultsData):
        """Represents data about the live running algorithm returned from the server"""
        ...


class LiveLog(QuantConnect.Api.RestResponse):
    """Logs from a live algorithm"""

    @property
    def Logs(self) -> System.Collections.Generic.List[str]:
        """List of logs from the live algorithm"""
        ...

    @Logs.setter
    def Logs(self, value: System.Collections.Generic.List[str]):
        """List of logs from the live algorithm"""
        ...


class Link(QuantConnect.Api.RestResponse):
    """Response from reading purchased data"""

    @property
    def DataLink(self) -> str:
        """Link to the data"""
        ...

    @DataLink.setter
    def DataLink(self, value: str):
        """Link to the data"""
        ...


class BacktestReport(QuantConnect.Api.RestResponse):
    """Backtest Report Response wrapper"""

    @property
    def Report(self) -> str:
        """HTML data of the report with embedded base64 images"""
        ...

    @Report.setter
    def Report(self, value: str):
        """HTML data of the report with embedded base64 images"""
        ...


class NodePrices(System.Object):
    """Class for deserializing node prices from node object"""

    @property
    def Monthly(self) -> int:
        """The monthly price of the node in US dollars"""
        ...

    @Monthly.setter
    def Monthly(self, value: int):
        """The monthly price of the node in US dollars"""
        ...

    @property
    def Yearly(self) -> int:
        """The yearly prices of the node in US dollars"""
        ...

    @Yearly.setter
    def Yearly(self, value: int):
        """The yearly prices of the node in US dollars"""
        ...


class Node(System.Object):
    """
    Node class built for API endpoints nodes/read and nodes/create.
    Converts JSON properties from API response into data members for the class.
    Contains all relevant information on a Node to interact through API endpoints.
    """

    @property
    def Speed(self) -> float:
        """The nodes cpu clock speed in GHz"""
        ...

    @Speed.setter
    def Speed(self, value: float):
        """The nodes cpu clock speed in GHz"""
        ...

    @property
    def Prices(self) -> QuantConnect.Api.NodePrices:
        """
        The monthly and yearly prices of the node in US dollars,
        see NodePrices for type.
        """
        ...

    @Prices.setter
    def Prices(self, value: QuantConnect.Api.NodePrices):
        """
        The monthly and yearly prices of the node in US dollars,
        see NodePrices for type.
        """
        ...

    @property
    def CpuCount(self) -> int:
        """CPU core count of node"""
        ...

    @CpuCount.setter
    def CpuCount(self, value: int):
        """CPU core count of node"""
        ...

    @property
    def Ram(self) -> float:
        """Size of RAM in Gigabytes"""
        ...

    @Ram.setter
    def Ram(self, value: float):
        """Size of RAM in Gigabytes"""
        ...

    @property
    def Name(self) -> str:
        """Name of the node"""
        ...

    @Name.setter
    def Name(self, value: str):
        """Name of the node"""
        ...

    @property
    def SKU(self) -> str:
        """Node type identifier for configuration"""
        ...

    @SKU.setter
    def SKU(self, value: str):
        """Node type identifier for configuration"""
        ...

    @property
    def Description(self) -> str:
        """String description of the node"""
        ...

    @Description.setter
    def Description(self, value: str):
        """String description of the node"""
        ...

    @property
    def UsedBy(self) -> str:
        """User currently using the node"""
        ...

    @UsedBy.setter
    def UsedBy(self, value: str):
        """User currently using the node"""
        ...

    @property
    def ProjectName(self) -> str:
        """Project the node is being used for"""
        ...

    @ProjectName.setter
    def ProjectName(self, value: str):
        """Project the node is being used for"""
        ...

    @property
    def Busy(self) -> bool:
        """Boolean if the node is currently busy"""
        ...

    @Busy.setter
    def Busy(self, value: bool):
        """Boolean if the node is currently busy"""
        ...

    @property
    def Id(self) -> str:
        """Full ID of node"""
        ...

    @Id.setter
    def Id(self, value: str):
        """Full ID of node"""
        ...


class CreatedNode(QuantConnect.Api.RestResponse):
    """
    Rest api response wrapper for node/create, reads in the nodes information into a
    node object
    """

    @property
    def Node(self) -> QuantConnect.Api.Node:
        """The created node from node/create"""
        ...

    @Node.setter
    def Node(self, value: QuantConnect.Api.Node):
        """The created node from node/create"""
        ...


class NodeType(System.Enum):
    """
    NodeTypes enum for all possible options of target environments
    Used in conjuction with SKU class as a NodeType is a required parameter for SKU
    """

    Backtest = 0

    Research = 1

    Live = 2


class SKU(System.Object):
    """
    Class for generating a SKU for a node with a given configuration
    Every SKU is made up of 3 variables:
    - Target environment (L for live, B for Backtest, R for Research)
    - CPU core count
    - Dedicated RAM (GB)
    """

    @property
    def Cores(self) -> int:
        """The number of CPU cores in the node"""
        ...

    @Cores.setter
    def Cores(self, value: int):
        """The number of CPU cores in the node"""
        ...

    @property
    def Memory(self) -> int:
        """Size of RAM in GB of the Node"""
        ...

    @Memory.setter
    def Memory(self, value: int):
        """Size of RAM in GB of the Node"""
        ...

    @property
    def Target(self) -> QuantConnect.Api.NodeType:
        """Target environment for the node"""
        ...

    @Target.setter
    def Target(self, value: QuantConnect.Api.NodeType):
        """Target environment for the node"""
        ...

    def __init__(self, cores: int, memory: int, target: QuantConnect.Api.NodeType) -> None:
        """
        Constructs a SKU object out of the provided node configuration
        
        :param cores: Number of cores
        :param memory: Size of RAM in GBs
        :param target: Target Environment Live/Backtest/Research
        """
        ...

    def ToString(self) -> str:
        """
        Generates the SKU string for API calls based on the specifications of the node
        
        :returns: String representation of the SKU.
        """
        ...


class NodeList(QuantConnect.Api.RestResponse):
    """
    Rest api response wrapper for node/read, contains sets of node lists for each
    target environment. List are composed of Node objects.
    """

    @property
    def BacktestNodes(self) -> System.Collections.Generic.List[QuantConnect.Api.Node]:
        """Collection of backtest nodes"""
        ...

    @BacktestNodes.setter
    def BacktestNodes(self, value: System.Collections.Generic.List[QuantConnect.Api.Node]):
        """Collection of backtest nodes"""
        ...

    @property
    def ResearchNodes(self) -> System.Collections.Generic.List[QuantConnect.Api.Node]:
        """Collection of research nodes"""
        ...

    @ResearchNodes.setter
    def ResearchNodes(self, value: System.Collections.Generic.List[QuantConnect.Api.Node]):
        """Collection of research nodes"""
        ...

    @property
    def LiveNodes(self) -> System.Collections.Generic.List[QuantConnect.Api.Node]:
        """Collection of live nodes"""
        ...

    @LiveNodes.setter
    def LiveNodes(self, value: System.Collections.Generic.List[QuantConnect.Api.Node]):
        """Collection of live nodes"""
        ...


class Card(System.Object):
    """Credit card"""

    @property
    def Brand(self) -> str:
        """Credit card brand"""
        ...

    @Brand.setter
    def Brand(self, value: str):
        """Credit card brand"""
        ...

    @property
    def Expiration(self) -> datetime.datetime:
        """The credit card expiration"""
        ...

    @Expiration.setter
    def Expiration(self, value: datetime.datetime):
        """The credit card expiration"""
        ...

    @property
    def LastFourDigits(self) -> float:
        """The last 4 digits of the card"""
        ...

    @LastFourDigits.setter
    def LastFourDigits(self, value: float):
        """The last 4 digits of the card"""
        ...


class Account(QuantConnect.Api.RestResponse):
    """Account information for an organization"""

    @property
    def OrganizationId(self) -> str:
        """The organization Id"""
        ...

    @OrganizationId.setter
    def OrganizationId(self, value: str):
        """The organization Id"""
        ...

    @property
    def CreditBalance(self) -> float:
        """The current account balance"""
        ...

    @CreditBalance.setter
    def CreditBalance(self, value: float):
        """The current account balance"""
        ...

    @property
    def Card(self) -> QuantConnect.Api.Card:
        """The current organizations credit card"""
        ...

    @Card.setter
    def Card(self, value: QuantConnect.Api.Card):
        """The current organizations credit card"""
        ...


class Api(System.Object, QuantConnect.Interfaces.IApi, QuantConnect.Interfaces.IDownloadProvider):
    """QuantConnect.com Interaction Via API."""

    @property
    def ApiConnection(self) -> QuantConnect.Api.ApiConnection:
        """
        Returns the underlying API connection
        
        This property is protected.
        """
        ...

    @ApiConnection.setter
    def ApiConnection(self, value: QuantConnect.Api.ApiConnection):
        """
        Returns the underlying API connection
        
        This property is protected.
        """
        ...

    @property
    def Connected(self) -> bool:
        """Check if Api is successfully connected with correct credentials"""
        ...

    def Initialize(self, userId: int, token: str, dataFolder: str) -> None:
        """Initialize the API using the config.json file."""
        ...

    def CreateProject(self, name: str, language: QuantConnect.Language) -> QuantConnect.Api.ProjectResponse:
        """
        Create a project with the specified name and language via QuantConnect.com API
        
        :param name: Project name
        :param language: Programming language to use
        :returns: Project object from the API.
        """
        ...

    def ReadProject(self, projectId: int) -> QuantConnect.Api.ProjectResponse:
        """
        Get details about a single project
        
        :param projectId: Id of the project
        :returns: ProjectResponse that contains information regarding the project.
        """
        ...

    def ListProjects(self) -> QuantConnect.Api.ProjectResponse:
        """
        List details of all projects
        
        :returns: ProjectResponse that contains information regarding the project.
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

    def ReadProjectFiles(self, projectId: int) -> QuantConnect.Api.ProjectFilesResponse:
        """
        Read all files in a project
        
        :param projectId: Project id to which the file belongs
        :returns: ProjectFilesResponse that includes the information about all files in the project.
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
        Delete a project
        
        :param projectId: Project id we own and wish to delete
        :returns: RestResponse indicating success.
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
        :returns: Compile.
        """
        ...

    def CreateBacktest(self, projectId: int, compileId: str, backtestName: str) -> QuantConnect.Api.Backtest:
        """
        Create a new backtest request and get the id.
        
        :param projectId: Id for the project to backtest
        :param compileId: Compile id for the project
        :param backtestName: Name for the new backtest
        :returns: Backtestt.
        """
        ...

    def ReadBacktest(self, projectId: int, backtestId: str, getCharts: bool = True) -> QuantConnect.Api.Backtest:
        """
        Read out a backtest in the project id specified.
        
        :param projectId: Project id to read
        :param backtestId: Specific backtest id to read
        :param getCharts: True will return backtest charts
        :returns: Backtest.
        """
        ...

    def UpdateBacktest(self, projectId: int, backtestId: str, name: str = ..., note: str = ...) -> QuantConnect.Api.RestResponse:
        """
        Update a backtest name
        
        :param projectId: Project for the backtest we want to update
        :param backtestId: Backtest id we want to update
        :param name: Name we'd like to assign to the backtest
        :param note: Note attached to the backtest
        :returns: RestResponse.
        """
        ...

    def ListBacktests(self, projectId: int) -> QuantConnect.Api.BacktestList:
        """
        List all the backtests for a project
        
        :param projectId: Project id we'd like to get a list of backtest for
        :returns: BacktestList.
        """
        ...

    def DeleteBacktest(self, projectId: int, backtestId: str) -> QuantConnect.Api.RestResponse:
        """
        Delete a backtest from the specified project and backtestId.
        
        :param projectId: Project for the backtest we want to delete
        :param backtestId: Backtest id we want to delete
        :returns: RestResponse.
        """
        ...

    def CreateLiveAlgorithm(self, projectId: int, compileId: str, nodeId: str, baseLiveAlgorithmSettings: QuantConnect.Api.BaseLiveAlgorithmSettings, versionId: str = "-1") -> QuantConnect.Api.LiveAlgorithm:
        """
        Create a live algorithm.
        
        :param projectId: Id of the project on QuantConnect
        :param compileId: Id of the compilation on QuantConnect
        :param nodeId: Id of the node that will run the algorithm
        :param baseLiveAlgorithmSettings: Brokerage specific BaseLiveAlgorithmSettings.
        :param versionId: The version of the Lean used to run the algorithm.                         -1 is master, however, sometimes this can create problems with live deployments.                         If you experience problems using, try specifying the version of Lean you would like to use.
        :returns: Information regarding the new algorithm LiveAlgorithm.
        """
        ...

    def ListLiveAlgorithms(self, status: typing.Optional[QuantConnect.AlgorithmStatus] = None, startTime: typing.Optional[datetime.datetime] = None, endTime: typing.Optional[datetime.datetime] = None) -> QuantConnect.Api.LiveList:
        """
        Get a list of live running algorithms for user
        
        :param status: Filter the statuses of the algorithms returned from the api
        :param startTime: Earliest launched time of the algorithms returned by the Api
        :param endTime: Latest launched time of the algorithms returned by the Api
        :returns: LiveList.
        """
        ...

    def ReadLiveAlgorithm(self, projectId: int, deployId: str) -> QuantConnect.Api.LiveAlgorithmResults:
        """
        Read out a live algorithm in the project id specified.
        
        :param projectId: Project id to read
        :param deployId: Specific instance id to read
        :returns: LiveAlgorithmResults.
        """
        ...

    def LiquidateLiveAlgorithm(self, projectId: int) -> QuantConnect.Api.RestResponse:
        """
        Liquidate a live algorithm from the specified project and deployId.
        
        :param projectId: Project for the live instance we want to stop
        :returns: RestResponse.
        """
        ...

    def StopLiveAlgorithm(self, projectId: int) -> QuantConnect.Api.RestResponse:
        """
        Stop a live algorithm from the specified project and deployId.
        
        :param projectId: Project for the live instance we want to stop
        :returns: RestResponse.
        """
        ...

    def ReadLiveLogs(self, projectId: int, algorithmId: str, startTime: typing.Optional[datetime.datetime] = None, endTime: typing.Optional[datetime.datetime] = None) -> QuantConnect.Api.LiveLog:
        """
        Gets the logs of a specific live algorithm
        
        :param projectId: Project Id of the live running algorithm
        :param algorithmId: Algorithm Id of the live running algorithm
        :param startTime: No logs will be returned before this time
        :param endTime: No logs will be returned after this time
        :returns: LiveLog List of strings that represent the logs of the algorithm.
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

    def ReadBacktestReport(self, projectId: int, backtestId: str) -> QuantConnect.Api.BacktestReport:
        """
        Read out the report of a backtest in the project id specified.
        
        :param projectId: Project id to read
        :param backtestId: Specific backtest id to read
        :returns: BacktestReport.
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

    def GetAlgorithmStatus(self, algorithmId: str) -> QuantConnect.AlgorithmControl:
        """
        Get the algorithm status from the user with this algorithm id.
        
        :param algorithmId: String algorithm id we're searching for.
        :returns: Algorithm status enum.
        """
        ...

    def SetAlgorithmStatus(self, algorithmId: str, status: QuantConnect.AlgorithmStatus, message: str = ...) -> None:
        """
        Algorithm passes back its current status to the UX.
        
        :param algorithmId: String algorithm id we're setting.
        :param status: Status of the current algorithm
        :param message: Message for the algorithm status event
        :returns: Algorithm status enum.
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
        :param netReturn: Net return for the deployment
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

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    @staticmethod
    def CreateSecureHash(timestamp: int, token: str) -> str:
        """
        Generate a secure hash for the authorization headers.
        
        :returns: Time based hash of user token and timestamp.
        """
        ...

    def CreateNode(self, name: str, organizationId: str, sku: QuantConnect.Api.SKU) -> QuantConnect.Api.CreatedNode:
        """
        Create a new node in the organization, node configuration is defined by the
        SKU
        
        :param name: The name of the new node
        :param organizationId: ID of the organization
        :param sku: SKU Object representing configuration
        :returns: Returns CreatedNode which contains API response and Node.
        """
        ...

    def ReadNodes(self, organizationId: str) -> QuantConnect.Api.NodeList:
        """
        Reads the nodes associated with the organization, creating a
        NodeList for the response
        
        :param organizationId: ID of the organization
        :returns: NodeList containing Backtest, Research, and Live Nodes.
        """
        ...

    def UpdateNode(self, nodeId: str, newName: str, organizationId: str) -> QuantConnect.Api.RestResponse:
        """
        Update an organizations node with a new name
        
        :param nodeId: The node ID of the node you want to update
        :param newName: The new name for that node
        :param organizationId: ID of the organization
        :returns: RestResponse containing success response and errors.
        """
        ...

    def DeleteNode(self, nodeId: str, organizationId: str) -> QuantConnect.Api.RestResponse:
        """
        Delete a node from an organization, requires node ID.
        
        :param nodeId: The node ID of the node you want to delete
        :param organizationId: ID of the organization
        :returns: RestResponse containing success response and errors.
        """
        ...

    def StopNode(self, nodeId: str, organizationId: str) -> QuantConnect.Api.RestResponse:
        """
        Stop a running node in a organization
        
        :param nodeId: The node ID of the node you want to stop
        :param organizationId: ID of the organization
        :returns: RestResponse containing success response and errors.
        """
        ...

    def ReadAccount(self, organizationId: str = None) -> QuantConnect.Api.Account:
        """
        Will read the organization account status
        
        :param organizationId: The target organization id, if null will return default organization
        """
        ...


class AuthenticationResponse(QuantConnect.Api.RestResponse):
    """Verify if the credentials are OK."""


class Dividend(System.Object):
    """Dividend returned from the api"""

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """The Symbol"""
        ...

    @property
    def SymbolID(self) -> str:
        """The requested symbol ID"""
        ...

    @SymbolID.setter
    def SymbolID(self, value: str):
        """The requested symbol ID"""
        ...

    @property
    def Date(self) -> datetime.datetime:
        """The date of the dividend"""
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        """The date of the dividend"""
        ...

    @property
    def DividendPerShare(self) -> float:
        """The dividend distribution"""
        ...

    @DividendPerShare.setter
    def DividendPerShare(self, value: float):
        """The dividend distribution"""
        ...

    @property
    def ReferencePrice(self) -> float:
        """The reference price for the dividend"""
        ...

    @ReferencePrice.setter
    def ReferencePrice(self, value: float):
        """The reference price for the dividend"""
        ...


class DividendList(QuantConnect.Api.RestResponse):
    """Collection container for a list of dividend objects"""

    @property
    def Dividends(self) -> System.Collections.Generic.List[QuantConnect.Api.Dividend]:
        """The dividends list"""
        ...

    @Dividends.setter
    def Dividends(self, value: System.Collections.Generic.List[QuantConnect.Api.Dividend]):
        """The dividends list"""
        ...


class LiveAlgorithmApiSettingsWrapper(System.Object):
    """Helper class to put BaseLiveAlgorithmSettings in proper format."""

    @property
    def VersionId(self) -> str:
        """-1 is master"""
        ...

    @VersionId.setter
    def VersionId(self, value: str):
        """-1 is master"""
        ...

    @property
    def ProjectId(self) -> int:
        """Project id for the live instance"""
        ...

    @ProjectId.setter
    def ProjectId(self, value: int):
        """Project id for the live instance"""
        ...

    @property
    def CompileId(self) -> str:
        """Compile Id for the live algorithm"""
        ...

    @CompileId.setter
    def CompileId(self, value: str):
        """Compile Id for the live algorithm"""
        ...

    @property
    def NodeId(self) -> str:
        """Id of the node being used to run live algorithm"""
        ...

    @NodeId.setter
    def NodeId(self, value: str):
        """Id of the node being used to run live algorithm"""
        ...

    @property
    def Brokerage(self) -> QuantConnect.Api.BaseLiveAlgorithmSettings:
        """The API expects the settings as part of a brokerage object"""
        ...

    @Brokerage.setter
    def Brokerage(self, value: QuantConnect.Api.BaseLiveAlgorithmSettings):
        """The API expects the settings as part of a brokerage object"""
        ...

    def __init__(self, projectId: int, compileId: str, nodeId: str, settings: QuantConnect.Api.BaseLiveAlgorithmSettings, version: str = "-1") -> None:
        """
        Constructor for LiveAlgorithmApiSettingsWrapper
        
        :param projectId: Id of project from QuantConnect
        :param compileId: Id of compilation of project from QuantConnect
        :param nodeId: Server type to run live Algorithm
        :param settings: BaseLiveAlgorithmSettings  for a specific brokerage
        :param version: The version identifier
        """
        ...


class DefaultLiveAlgorithmSettings(QuantConnect.Api.BaseLiveAlgorithmSettings):
    """Default live algorithm settings"""

    def __init__(self, user: str, password: str, environment: QuantConnect.BrokerageEnvironment, account: str) -> None:
        """
        Constructor for default algorithms
        
        :param user: Username associated with brokerage
        :param password: Password associated with brokerage
        :param environment: 'live'/'paper'
        :param account: Account id for brokerage
        """
        ...


class FXCMLiveAlgorithmSettings(QuantConnect.Api.BaseLiveAlgorithmSettings):
    """Algorithm setting for trading with FXCM"""

    def __init__(self, user: str, password: str, environment: QuantConnect.BrokerageEnvironment, account: str) -> None:
        """
        Contructor for live trading with FXCM
        
        :param user: Username associated with brokerage
        :param password: Password associated with brokerage
        :param environment: 'live'/'paper'
        :param account: Account id for brokerage
        """
        ...


class InteractiveBrokersLiveAlgorithmSettings(QuantConnect.Api.BaseLiveAlgorithmSettings):
    """Live algorithm settings for trading with Interactive Brokers"""

    def __init__(self, user: str, password: str, account: str) -> None:
        """
        Contructor for live trading with IB.
        
        :param user: Username associated with brokerage
        :param password: Password of assciate brokerage
        :param account: Account id for brokerage
        """
        ...


class OandaLiveAlgorithmSettings(QuantConnect.Api.BaseLiveAlgorithmSettings):
    """Live algorithm settings for trading with Oanda"""

    @property
    def AccessToken(self) -> str:
        """Access token for Oanda"""
        ...

    @AccessToken.setter
    def AccessToken(self, value: str):
        """Access token for Oanda"""
        ...

    @property
    def DateIssued(self) -> str:
        """Date token was issued"""
        ...

    @DateIssued.setter
    def DateIssued(self, value: str):
        """Date token was issued"""
        ...

    def __init__(self, accessToken: str, environment: QuantConnect.BrokerageEnvironment, account: str) -> None:
        """
        Contructor for live trading with Oanda.
        
        :param accessToken: Access Token (specific for Oanda Brokerage)
        :param environment: 'live'/'paper'
        :param account: Account id for brokerage
        """
        ...


class TradierLiveAlgorithmSettings(QuantConnect.Api.BaseLiveAlgorithmSettings):
    """Live algorithm settings for trading with Tradier"""

    @property
    def AccessToken(self) -> str:
        """Access token for tradier brokerage"""
        ...

    @AccessToken.setter
    def AccessToken(self, value: str):
        """Access token for tradier brokerage"""
        ...

    @property
    def DateIssued(self) -> str:
        """Property specific to Tradier account.  See tradier account for more details."""
        ...

    @DateIssued.setter
    def DateIssued(self, value: str):
        """Property specific to Tradier account.  See tradier account for more details."""
        ...

    @property
    def RefreshToken(self) -> str:
        """Property specific to Tradier account.  See tradier account for more details."""
        ...

    @RefreshToken.setter
    def RefreshToken(self, value: str):
        """Property specific to Tradier account.  See tradier account for more details."""
        ...

    @property
    def Lifetime(self) -> str:
        """Property specific to Tradier account.  See tradier account for more details."""
        ...

    @Lifetime.setter
    def Lifetime(self, value: str):
        """Property specific to Tradier account.  See tradier account for more details."""
        ...

    def __init__(self, accessToken: str, dateIssued: str, refreshToken: str, account: str) -> None:
        """
        Contructor for live trading with Tradier.
        
        :param dateIssued: Specific for live trading with Tradier.  See Tradier account for more details.
        :param refreshToken: Specific for live trading with Tradier.  See Tradier account for more details.
        :param account: Account id for brokerage
        """
        ...


class BitfinexLiveAlgorithmSettings(QuantConnect.Api.BaseLiveAlgorithmSettings):
    """Live algorithm settings for trading with Bitfinex"""

    @property
    def Key(self) -> str:
        """Property specific to Bitfinex account. API Key"""
        ...

    @Key.setter
    def Key(self, value: str):
        """Property specific to Bitfinex account. API Key"""
        ...

    @property
    def Secret(self) -> str:
        """Property specific to Bitfinex account. API Secret Key"""
        ...

    @Secret.setter
    def Secret(self, value: str):
        """Property specific to Bitfinex account. API Secret Key"""
        ...

    def __init__(self, key: str, secret: str) -> None:
        """
        Constructor for live trading with Bitfinex
        
        :param key: Api key to Bitfinex account
        :param secret: Secret Api key to Bitfinex account
        """
        ...


class GDAXLiveAlgorithmSettings(QuantConnect.Api.BaseLiveAlgorithmSettings):
    """Live algorithm settings for trading with GDAX (Coinbase)"""

    @property
    def Key(self) -> str:
        """Property specific to GDAX account. API Key"""
        ...

    @Key.setter
    def Key(self, value: str):
        """Property specific to GDAX account. API Key"""
        ...

    @property
    def Secret(self) -> str:
        """Property specific to GDAX account. API Secret Key"""
        ...

    @Secret.setter
    def Secret(self, value: str):
        """Property specific to GDAX account. API Secret Key"""
        ...

    @property
    def Passphrase(self) -> str:
        """Property specific to GDAX account. API Passphrase"""
        ...

    @Passphrase.setter
    def Passphrase(self, value: str):
        """Property specific to GDAX account. API Passphrase"""
        ...

    def __init__(self, key: str, secret: str, passphrase: str) -> None:
        """
        Constructor for live trading with GDAX (Coinbase)
        
        :param key: Api key to GDAX account
        :param secret: Secret Api key to GDAX account
        :param passphrase: Passphrase to this API key
        """
        ...


class Split(System.Object):
    """Split returned from the api"""

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """The Symbol"""
        ...

    @property
    def SymbolID(self) -> str:
        """The requested symbol ID"""
        ...

    @SymbolID.setter
    def SymbolID(self, value: str):
        """The requested symbol ID"""
        ...

    @property
    def Date(self) -> datetime.datetime:
        """The date of the split"""
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        """The date of the split"""
        ...

    @property
    def SplitFactor(self) -> float:
        """The split factor"""
        ...

    @SplitFactor.setter
    def SplitFactor(self, value: float):
        """The split factor"""
        ...

    @property
    def ReferencePrice(self) -> float:
        """The reference price for the split"""
        ...

    @ReferencePrice.setter
    def ReferencePrice(self, value: float):
        """The reference price for the split"""
        ...


class SplitList(QuantConnect.Api.RestResponse):
    """Collection container for a list of split objects"""

    @property
    def Splits(self) -> System.Collections.Generic.List[QuantConnect.Api.Split]:
        """The splits list"""
        ...

    @Splits.setter
    def Splits(self, value: System.Collections.Generic.List[QuantConnect.Api.Split]):
        """The splits list"""
        ...


class BacktestResponseWrapper(QuantConnect.Api.RestResponse):
    """
    Wrapper class for Backtest/* endpoints JSON response
    Currently used by Backtest/Read and Backtest/Create
    """

    @property
    def Backtest(self) -> QuantConnect.Api.Backtest:
        """Backtest Object"""
        ...

    @Backtest.setter
    def Backtest(self, value: QuantConnect.Api.Backtest):
        """Backtest Object"""
        ...


class Prices(System.Object):
    """Prices rest response wrapper"""

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """The requested Symbol"""
        ...

    @Symbol.setter
    def Symbol(self, value: QuantConnect.Symbol):
        """The requested Symbol"""
        ...

    @property
    def SymbolID(self) -> str:
        """The requested symbol ID"""
        ...

    @SymbolID.setter
    def SymbolID(self, value: str):
        """The requested symbol ID"""
        ...

    @property
    def Price(self) -> float:
        """The requested price"""
        ...

    @Price.setter
    def Price(self, value: float):
        """The requested price"""
        ...

    @property
    def Updated(self) -> datetime.datetime:
        """UTC time the price was updated"""
        ...

    @Updated.setter
    def Updated(self, value: datetime.datetime):
        """UTC time the price was updated"""
        ...


class PricesList(QuantConnect.Api.RestResponse):
    """Collection container for a list of prices objects"""

    @property
    def Prices(self) -> System.Collections.Generic.List[QuantConnect.Api.Prices]:
        """Collection of prices objects"""
        ...

    @Prices.setter
    def Prices(self, value: System.Collections.Generic.List[QuantConnect.Api.Prices]):
        """Collection of prices objects"""
        ...


class LiveAlgorithmResultsJsonConverter(JsonConverter):
    """Custom JsonConverter for LiveResults data for live algorithms"""

    @property
    def CanWrite(self) -> bool:
        """Gets a value indicating whether this Newtonsoft.Json.JsonConverter can write JSON."""
        ...

    def WriteJson(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...

    def CanConvert(self, objectType: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param objectType: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...

    def ReadJson(self, reader: typing.Any, objectType: typing.Type, existingValue: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Reads the JSON representation of the object.
        
        :param reader: The Newtonsoft.Json.JsonReader to read from.
        :param objectType: Type of the object.
        :param existingValue: The existing value of object being read.
        :param serializer: The calling serializer.
        :returns: The object value.
        """
        ...

    @staticmethod
    def CreateLiveResultsFromJObject(jObject: typing.Any) -> QuantConnect.Api.LiveAlgorithmResults:
        """
        Custom parsing of live results data
        
        :param jObject: Json representing LiveResults
        """
        ...


