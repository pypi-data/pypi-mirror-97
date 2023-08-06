import datetime
import typing

import QuantConnect.Data
import QuantConnect.Data.Custom.Quiver
import QuantConnect.Orders
import QuantConnect.Util
import System


class TransactionDirection(System.Enum):
    """Transaction direction"""

    Purchase = 0
    """Buy, equivalent to OrderDirection.Buy"""

    Sale = 1
    """Sell, equivalent to OrderDirection.Sell"""


class QuiverWikipedia(QuantConnect.Data.BaseData):
    """Wikipedia Page Views for the specified company"""

    @property
    def Date(self) -> datetime.datetime:
        """The date of the Page View count"""
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        """The date of the Page View count"""
        ...

    @property
    def PageViews(self) -> typing.Optional[float]:
        """The company's Wikipedia Page Views on the given date"""
        ...

    @PageViews.setter
    def PageViews(self, value: typing.Optional[float]):
        """The company's Wikipedia Page Views on the given date"""
        ...

    @property
    def WeekPercentChange(self) -> typing.Optional[float]:
        """
        The view count % change over the week prior to the date.
        Represented as a whole number (e.g. 100% = 100.0)
        """
        ...

    @WeekPercentChange.setter
    def WeekPercentChange(self, value: typing.Optional[float]):
        """
        The view count % change over the week prior to the date.
        Represented as a whole number (e.g. 100% = 100.0)
        """
        ...

    @property
    def MonthPercentChange(self) -> typing.Optional[float]:
        """
        The view count % change over the month prior to the date
        Represented as a whole number (e.g. 100% = 100.0)
        """
        ...

    @MonthPercentChange.setter
    def MonthPercentChange(self, value: typing.Optional[float]):
        """
        The view count % change over the month prior to the date
        Represented as a whole number (e.g. 100% = 100.0)
        """
        ...

    @typing.overload
    def __init__(self) -> None:
        """Required for successful Json.NET deserialization"""
        ...

    @typing.overload
    def __init__(self, csvLine: str) -> None:
        """
        Creates a new instance of QuiverWikipedia from a CSV line
        
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
        :returns: Quiver Wikipedia object.
        """
        ...

    def ToString(self) -> str:
        """Formats a string with the Quiver Wikipedia information."""
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


class Congress(System.Enum):
    """United States of America Legislative Branch House of Congress"""

    Senate = 0
    """The United States Senate"""

    Representatives = 1
    """The United States House of Representatives"""


class TransactionDirectionJsonConverter(QuantConnect.Util.TypeChangeJsonConverter[QuantConnect.Orders.OrderDirection, str]):
    """Converts Quiver Quantitative TransactionDirection to OrderDirection"""

    @typing.overload
    def Convert(self, value: QuantConnect.Orders.OrderDirection) -> str:
        """This method is protected."""
        ...

    @typing.overload
    def Convert(self, value: str) -> int:
        """
        This method is protected.
        
        :returns: This method returns the int value of a member of the QuantConnect.Orders.OrderDirection enum.
        """
        ...


class QuiverCongress(QuantConnect.Data.BaseData):
    """Personal stock transactions by U.S. Representatives"""

    @property
    def ReportDate(self) -> datetime.datetime:
        """The date the transaction was reported"""
        ...

    @ReportDate.setter
    def ReportDate(self, value: datetime.datetime):
        """The date the transaction was reported"""
        ...

    @property
    def TransactionDate(self) -> datetime.datetime:
        """The date the transaction took place"""
        ...

    @TransactionDate.setter
    def TransactionDate(self, value: datetime.datetime):
        """The date the transaction took place"""
        ...

    @property
    def Representative(self) -> str:
        """The Representative making the transaction"""
        ...

    @Representative.setter
    def Representative(self, value: str):
        """The Representative making the transaction"""
        ...

    @property
    def Transaction(self) -> int:
        """
        The type of transaction
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderDirection enum.
        """
        ...

    @Transaction.setter
    def Transaction(self, value: int):
        """
        The type of transaction
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderDirection enum.
        """
        ...

    @property
    def Amount(self) -> typing.Optional[float]:
        """The amount of the transaction (in USD)"""
        ...

    @Amount.setter
    def Amount(self, value: typing.Optional[float]):
        """The amount of the transaction (in USD)"""
        ...

    @property
    def House(self) -> int:
        """
        The House of Congress that the trader belongs to
        
        This property contains the int value of a member of the QuantConnect.Data.Custom.Quiver.Congress enum.
        """
        ...

    @House.setter
    def House(self, value: int):
        """
        The House of Congress that the trader belongs to
        
        This property contains the int value of a member of the QuantConnect.Data.Custom.Quiver.Congress enum.
        """
        ...

    @typing.overload
    def __init__(self) -> None:
        """Required for successful Json.NET deserialization"""
        ...

    @typing.overload
    def __init__(self, csvLine: str) -> None:
        """
        Creates a new instance of QuiverCongress from a CSV line
        
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
        :returns: Quiver Congress object.
        """
        ...

    def ToString(self) -> str:
        """Formats a string with the Quiver Congress information."""
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


class QuiverEventsBeta(QuantConnect.Data.BaseData):
    """Political beta for the specified company"""

    @property
    def Date(self) -> datetime.datetime:
        """The date of the events beta calculation"""
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        """The date of the events beta calculation"""
        ...

    @property
    def EventName(self) -> str:
        """Event name (e.g. PresidentialElection2020)"""
        ...

    @EventName.setter
    def EventName(self, value: str):
        """Event name (e.g. PresidentialElection2020)"""
        ...

    @property
    def FirstEventName(self) -> str:
        """Name for first outcome (e.g. TrumpVictory)"""
        ...

    @FirstEventName.setter
    def FirstEventName(self, value: str):
        """Name for first outcome (e.g. TrumpVictory)"""
        ...

    @property
    def SecondEventName(self) -> str:
        """Name for second outcome (e.g. BidenVictory)"""
        ...

    @SecondEventName.setter
    def SecondEventName(self, value: str):
        """Name for second outcome (e.g. BidenVictory)"""
        ...

    @property
    def FirstEventBeta(self) -> float:
        """Correlation between daily excess returns and daily changes in first event odds"""
        ...

    @FirstEventBeta.setter
    def FirstEventBeta(self, value: float):
        """Correlation between daily excess returns and daily changes in first event odds"""
        ...

    @property
    def FirstEventOdds(self) -> float:
        """Odds of the first event happening, based on betting markets"""
        ...

    @FirstEventOdds.setter
    def FirstEventOdds(self, value: float):
        """Odds of the first event happening, based on betting markets"""
        ...

    @property
    def SecondEventBeta(self) -> float:
        """Correlation between daily excess returns and daily changes in second event odds"""
        ...

    @SecondEventBeta.setter
    def SecondEventBeta(self, value: float):
        """Correlation between daily excess returns and daily changes in second event odds"""
        ...

    @property
    def SecondEventOdds(self) -> float:
        """Odds of the second event happening, based on betting markets"""
        ...

    @SecondEventOdds.setter
    def SecondEventOdds(self, value: float):
        """Odds of the second event happening, based on betting markets"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Required for successful Json.NET deserialization"""
        ...

    @typing.overload
    def __init__(self, csvLine: str) -> None:
        """
        Creates a new instance of QuiverPoliticalBeta from a CSV line
        
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
        :returns: Quiver Political Beta object.
        """
        ...

    def ToString(self) -> str:
        """Formats a string with the Quiver Events Beta information."""
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


class QuiverWallStreetBets(QuantConnect.Data.BaseData):
    """Mentions of the given company's ticker in the WallStreetBets daily discussion thread"""

    @property
    def Date(self) -> datetime.datetime:
        """Date of the daily discussion thread"""
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        """Date of the daily discussion thread"""
        ...

    @property
    def Mentions(self) -> int:
        """The number of mentions on the given date"""
        ...

    @Mentions.setter
    def Mentions(self, value: int):
        """The number of mentions on the given date"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Required for successful Json.NET deserialization"""
        ...

    @typing.overload
    def __init__(self, csvLine: str) -> None:
        """
        Creates a new instance of QuiverWallStreetBets from a CSV line
        
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
        :returns: Quiver WallStreetBets object.
        """
        ...

    def ToString(self) -> str:
        """Formats a string with the Quiver WallStreetBets information."""
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


