import datetime
import typing

import QuantConnect.Data
import QuantConnect.Data.Custom.Estimize
import System


class EstimizeRelease(QuantConnect.Data.BaseData):
    """Financial releases for the specified company"""

    @property
    def Id(self) -> str:
        """The unique identifier for the release"""
        ...

    @Id.setter
    def Id(self, value: str):
        """The unique identifier for the release"""
        ...

    @property
    def FiscalYear(self) -> int:
        """The fiscal year for the release"""
        ...

    @FiscalYear.setter
    def FiscalYear(self, value: int):
        """The fiscal year for the release"""
        ...

    @property
    def FiscalQuarter(self) -> int:
        """The fiscal quarter for the release"""
        ...

    @FiscalQuarter.setter
    def FiscalQuarter(self, value: int):
        """The fiscal quarter for the release"""
        ...

    @property
    def ReleaseDate(self) -> datetime.datetime:
        """The date of the release"""
        ...

    @ReleaseDate.setter
    def ReleaseDate(self, value: datetime.datetime):
        """The date of the release"""
        ...

    @property
    def EndTime(self) -> datetime.datetime:
        """The date of the release"""
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """The date of the release"""
        ...

    @property
    def Eps(self) -> typing.Optional[float]:
        """The earnings per share for the specified fiscal quarter"""
        ...

    @Eps.setter
    def Eps(self, value: typing.Optional[float]):
        """The earnings per share for the specified fiscal quarter"""
        ...

    @property
    def Value(self) -> float:
        """The earnings per share for the specified fiscal quarter"""
        ...

    @Value.setter
    def Value(self, value: float):
        """The earnings per share for the specified fiscal quarter"""
        ...

    @property
    def Revenue(self) -> typing.Optional[float]:
        """The revenue for the specified fiscal quarter"""
        ...

    @Revenue.setter
    def Revenue(self, value: typing.Optional[float]):
        """The revenue for the specified fiscal quarter"""
        ...

    @property
    def WallStreetEpsEstimate(self) -> typing.Optional[float]:
        """The estimated EPS from Wall Street"""
        ...

    @WallStreetEpsEstimate.setter
    def WallStreetEpsEstimate(self, value: typing.Optional[float]):
        """The estimated EPS from Wall Street"""
        ...

    @property
    def WallStreetRevenueEstimate(self) -> typing.Optional[float]:
        """The estimated revenue from Wall Street"""
        ...

    @WallStreetRevenueEstimate.setter
    def WallStreetRevenueEstimate(self, value: typing.Optional[float]):
        """The estimated revenue from Wall Street"""
        ...

    @property
    def ConsensusEpsEstimate(self) -> typing.Optional[float]:
        """The mean EPS consensus by the Estimize community"""
        ...

    @ConsensusEpsEstimate.setter
    def ConsensusEpsEstimate(self, value: typing.Optional[float]):
        """The mean EPS consensus by the Estimize community"""
        ...

    @property
    def ConsensusRevenueEstimate(self) -> typing.Optional[float]:
        """The mean revenue consensus by the Estimize community"""
        ...

    @ConsensusRevenueEstimate.setter
    def ConsensusRevenueEstimate(self, value: typing.Optional[float]):
        """The mean revenue consensus by the Estimize community"""
        ...

    @property
    def ConsensusWeightedEpsEstimate(self) -> typing.Optional[float]:
        """The weighted EPS consensus by the Estimize community"""
        ...

    @ConsensusWeightedEpsEstimate.setter
    def ConsensusWeightedEpsEstimate(self, value: typing.Optional[float]):
        """The weighted EPS consensus by the Estimize community"""
        ...

    @property
    def ConsensusWeightedRevenueEstimate(self) -> typing.Optional[float]:
        """The weighted revenue consensus by the Estimize community"""
        ...

    @ConsensusWeightedRevenueEstimate.setter
    def ConsensusWeightedRevenueEstimate(self, value: typing.Optional[float]):
        """The weighted revenue consensus by the Estimize community"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """
        Without a default constructor, Json.NET will call the
        other constructor with `null` for the string parameter
        """
        ...

    @typing.overload
    def __init__(self, csvLine: str) -> None:
        """
        Creates EstimizeRelease instance from a line of CSV
        
        :param csvLine: CSV line
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the Subscription Data Source gained from the URL
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Subscription Data Source.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects.
        
        :param config: Subscription data config setup object
        :param line: Content of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Estimize Release object.
        """
        ...

    def ToString(self) -> str:
        """Formats a string with the Estimize Release information."""
        ...

    def RequiresMapping(self) -> bool:
        """
        Indicates if there is support for mapping
        
        :returns: True indicates mapping should be used.
        """
        ...

    def DataTimeZone(self) -> typing.Any:
        """
        Specifies the data time zone for this data type. This is useful for custom data types
        
        :returns: The DateTimeZone of this data type.
        """
        ...


class EstimizeEstimate(QuantConnect.Data.BaseData):
    """Financial estimates for the specified company"""

    @property
    def Id(self) -> str:
        """The unique identifier for the estimate"""
        ...

    @Id.setter
    def Id(self, value: str):
        """The unique identifier for the estimate"""
        ...

    @property
    def Ticker(self) -> str:
        """The ticker of the company being estimated"""
        ...

    @Ticker.setter
    def Ticker(self, value: str):
        """The ticker of the company being estimated"""
        ...

    @property
    def FiscalYear(self) -> int:
        """The fiscal year of the quarter being estimated"""
        ...

    @FiscalYear.setter
    def FiscalYear(self, value: int):
        """The fiscal year of the quarter being estimated"""
        ...

    @property
    def FiscalQuarter(self) -> int:
        """The fiscal quarter of the quarter being estimated"""
        ...

    @FiscalQuarter.setter
    def FiscalQuarter(self, value: int):
        """The fiscal quarter of the quarter being estimated"""
        ...

    @property
    def CreatedAt(self) -> datetime.datetime:
        """The time that the estimate was created (UTC)"""
        ...

    @CreatedAt.setter
    def CreatedAt(self, value: datetime.datetime):
        """The time that the estimate was created (UTC)"""
        ...

    @property
    def EndTime(self) -> datetime.datetime:
        """The time that the estimate was created (UTC)"""
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """The time that the estimate was created (UTC)"""
        ...

    @property
    def Eps(self) -> typing.Optional[float]:
        """The estimated earnings per share for the company in the specified fiscal quarter"""
        ...

    @Eps.setter
    def Eps(self, value: typing.Optional[float]):
        """The estimated earnings per share for the company in the specified fiscal quarter"""
        ...

    @property
    def Value(self) -> float:
        """The estimated earnings per share for the company in the specified fiscal quarter"""
        ...

    @Value.setter
    def Value(self, value: float):
        """The estimated earnings per share for the company in the specified fiscal quarter"""
        ...

    @property
    def Revenue(self) -> typing.Optional[float]:
        """The estimated revenue for the company in the specified fiscal quarter"""
        ...

    @Revenue.setter
    def Revenue(self, value: typing.Optional[float]):
        """The estimated revenue for the company in the specified fiscal quarter"""
        ...

    @property
    def UserName(self) -> str:
        """The unique identifier for the author of the estimate"""
        ...

    @UserName.setter
    def UserName(self, value: str):
        """The unique identifier for the author of the estimate"""
        ...

    @property
    def AnalystId(self) -> str:
        """The author of the estimate"""
        ...

    @AnalystId.setter
    def AnalystId(self, value: str):
        """The author of the estimate"""
        ...

    @property
    def Flagged(self) -> bool:
        """
        A boolean value which indicates whether we have flagged this estimate internally as erroneous
        (spam, wrong accounting standard, etc)
        """
        ...

    @Flagged.setter
    def Flagged(self, value: bool):
        """
        A boolean value which indicates whether we have flagged this estimate internally as erroneous
        (spam, wrong accounting standard, etc)
        """
        ...

    @typing.overload
    def __init__(self) -> None:
        """Required for successful Json.NET deserialization"""
        ...

    @typing.overload
    def __init__(self, csvLine: str) -> None:
        """
        Creates a new instance of EstimizeEstimate from a CSV line
        
        :param csvLine: CSV line
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the Subscription Data Source gained from the URL
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Subscription Data Source.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects.
        
        :param config: Subscription data config setup object
        :param line: Content of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Estimize Estimate object.
        """
        ...

    def ToString(self) -> str:
        """Formats a string with the Estimize Estimate information."""
        ...

    def RequiresMapping(self) -> bool:
        """
        Indicates if there is support for mapping
        
        :returns: True indicates mapping should be used.
        """
        ...

    def DataTimeZone(self) -> typing.Any:
        """
        Specifies the data time zone for this data type. This is useful for custom data types
        
        :returns: The DateTimeZone of this data type.
        """
        ...


class Source(System.Enum):
    """Source of the Consensus"""

    WallStreet = 0
    """Consensus from Wall Street"""

    Estimize = 1
    """Consensus from Estimize"""


class Type(System.Enum):
    """Type of the consensus"""

    Eps = 0
    """Consensus on earnings per share value"""

    Revenue = 1
    """Consensus on revenue value"""


class EstimizeConsensus(QuantConnect.Data.BaseData):
    """Consensus of the specified release"""

    @property
    def Id(self) -> str:
        """The unique identifier for the estimate"""
        ...

    @Id.setter
    def Id(self, value: str):
        """The unique identifier for the estimate"""
        ...

    @property
    def Source(self) -> typing.Optional[QuantConnect.Data.Custom.Estimize.Source]:
        """Consensus source (Wall Street or Estimize)"""
        ...

    @Source.setter
    def Source(self, value: typing.Optional[QuantConnect.Data.Custom.Estimize.Source]):
        """Consensus source (Wall Street or Estimize)"""
        ...

    @property
    def Type(self) -> typing.Optional[QuantConnect.Data.Custom.Estimize.Type]:
        """Type of Consensus (EPS or Revenue)"""
        ...

    @Type.setter
    def Type(self, value: typing.Optional[QuantConnect.Data.Custom.Estimize.Type]):
        """Type of Consensus (EPS or Revenue)"""
        ...

    @property
    def Mean(self) -> typing.Optional[float]:
        """The mean of the distribution of estimates (the "consensus")"""
        ...

    @Mean.setter
    def Mean(self, value: typing.Optional[float]):
        """The mean of the distribution of estimates (the "consensus")"""
        ...

    @property
    def Value(self) -> float:
        """The mean of the distribution of estimates (the "consensus")"""
        ...

    @Value.setter
    def Value(self, value: float):
        """The mean of the distribution of estimates (the "consensus")"""
        ...

    @property
    def High(self) -> typing.Optional[float]:
        """The highest estimate in the distribution"""
        ...

    @High.setter
    def High(self, value: typing.Optional[float]):
        """The highest estimate in the distribution"""
        ...

    @property
    def Low(self) -> typing.Optional[float]:
        """The lowest estimate in the distribution"""
        ...

    @Low.setter
    def Low(self, value: typing.Optional[float]):
        """The lowest estimate in the distribution"""
        ...

    @property
    def StandardDeviation(self) -> typing.Optional[float]:
        """The standard deviation of the distribution"""
        ...

    @StandardDeviation.setter
    def StandardDeviation(self, value: typing.Optional[float]):
        """The standard deviation of the distribution"""
        ...

    @property
    def Count(self) -> typing.Optional[int]:
        """The number of estimates in the distribution"""
        ...

    @Count.setter
    def Count(self, value: typing.Optional[int]):
        """The number of estimates in the distribution"""
        ...

    @property
    def UpdatedAt(self) -> datetime.datetime:
        """The timestamp of this consensus (UTC)"""
        ...

    @UpdatedAt.setter
    def UpdatedAt(self, value: datetime.datetime):
        """The timestamp of this consensus (UTC)"""
        ...

    @property
    def FiscalYear(self) -> typing.Optional[int]:
        """The fiscal year for the release"""
        ...

    @FiscalYear.setter
    def FiscalYear(self, value: typing.Optional[int]):
        """The fiscal year for the release"""
        ...

    @property
    def FiscalQuarter(self) -> typing.Optional[int]:
        """The fiscal quarter for the release"""
        ...

    @FiscalQuarter.setter
    def FiscalQuarter(self, value: typing.Optional[int]):
        """The fiscal quarter for the release"""
        ...

    @property
    def EndTime(self) -> datetime.datetime:
        """The timestamp of this consensus (UTC)"""
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """The timestamp of this consensus (UTC)"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Empty constructor required for successful Json.NET deserialization"""
        ...

    @typing.overload
    def __init__(self, csvLine: str) -> None:
        """
        Creates an instance from CSV lines
        
        :param csvLine: CSV file
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the Subscription Data Source gained from the URL
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Subscription Data Source.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects.
        
        :param config: Subscription data config setup object
        :param line: Content of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Estimize consensus object.
        """
        ...

    def ToString(self) -> str:
        """Formats a string with the Estimize Estimate information."""
        ...

    def RequiresMapping(self) -> bool:
        """
        Indicates if there is support for mapping
        
        :returns: True indicates mapping should be used.
        """
        ...

    def DataTimeZone(self) -> typing.Any:
        """
        Specifies the data time zone for this data type. This is useful for custom data types
        
        :returns: The DateTimeZone of this data type.
        """
        ...


