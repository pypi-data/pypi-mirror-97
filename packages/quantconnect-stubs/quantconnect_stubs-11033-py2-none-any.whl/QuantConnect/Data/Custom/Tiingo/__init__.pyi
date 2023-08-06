import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Custom.Tiingo
import QuantConnect.Data.Market
import System
import System.Collections.Generic

JsonConverter = typing.Any


class TiingoNews(QuantConnect.Data.IndexedBaseData):
    """
    Tiingo news data
    https://api.tiingo.com/documentation/news
    """

    @property
    def Source(self) -> str:
        """The domain the news source is from."""
        ...

    @Source.setter
    def Source(self, value: str):
        """The domain the news source is from."""
        ...

    @property
    def CrawlDate(self) -> datetime.datetime:
        """
        The datetime the news story was added to Tiingos database in UTC.
        This is always recorded by Tiingo and the news source has no input on this date.
        """
        ...

    @CrawlDate.setter
    def CrawlDate(self, value: datetime.datetime):
        """
        The datetime the news story was added to Tiingos database in UTC.
        This is always recorded by Tiingo and the news source has no input on this date.
        """
        ...

    @property
    def Url(self) -> str:
        """URL of the news article."""
        ...

    @Url.setter
    def Url(self, value: str):
        """URL of the news article."""
        ...

    @property
    def PublishedDate(self) -> datetime.datetime:
        """
        The datetime the news story was published in UTC. This is usually reported by the news source and not by Tiingo.
        If the news source does not declare a published date, Tiingo will use the time the news story was discovered by our crawler farm.
        """
        ...

    @PublishedDate.setter
    def PublishedDate(self, value: datetime.datetime):
        """
        The datetime the news story was published in UTC. This is usually reported by the news source and not by Tiingo.
        If the news source does not declare a published date, Tiingo will use the time the news story was discovered by our crawler farm.
        """
        ...

    @property
    def Tags(self) -> System.Collections.Generic.List[str]:
        """Tags that are mapped and discovered by Tiingo."""
        ...

    @Tags.setter
    def Tags(self, value: System.Collections.Generic.List[str]):
        """Tags that are mapped and discovered by Tiingo."""
        ...

    @property
    def Description(self) -> str:
        """Long-form description of the news story."""
        ...

    @Description.setter
    def Description(self, value: str):
        """Long-form description of the news story."""
        ...

    @property
    def Title(self) -> str:
        """Title of the news article."""
        ...

    @Title.setter
    def Title(self, value: str):
        """Title of the news article."""
        ...

    @property
    def ArticleID(self) -> str:
        """Unique identifier specific to the news article."""
        ...

    @ArticleID.setter
    def ArticleID(self, value: str):
        """Unique identifier specific to the news article."""
        ...

    @property
    def Symbols(self) -> System.Collections.Generic.List[QuantConnect.Symbol]:
        """What symbols are mentioned in the news story."""
        ...

    @Symbols.setter
    def Symbols(self, value: System.Collections.Generic.List[QuantConnect.Symbol]):
        """What symbols are mentioned in the news story."""
        ...

    def GetSourceForAnIndex(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, index: str, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Returns the source for a given index value
        
        :param config: Configuration object
        :param date: Date of this source file
        :param index: The index value for which we want to fetch the source
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: The SubscriptionDataSource instance to use.
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        For backtesting returns the index source for a date
        For live trading will return the source url to use, not using the index mechanism
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: The SubscriptionDataSource instance to use.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, content: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects. Each data type creates its own factory method,
            and returns a new instance of the object
            each time it is called. The returned object is assumed to be time stamped in the config.ExchangeTimeZone.
        
        :param config: Subscription data config setup object
        :param content: Content of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Instance of the T:BaseData object generated by this line of the CSV.
        """
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


class Tiingo(System.Object):
    """Helper class for Tiingo configuration"""

    AuthCode: str
    """Gets the Tiingo API token."""

    IsAuthCodeSet: bool
    """Returns true if the Tiingo API token has been set."""

    @staticmethod
    def SetAuthCode(authCode: str) -> None:
        """
        Sets the Tiingo API token.
        
        :param authCode: The Tiingo API token
        """
        ...


class TiingoSymbolMapper(System.Object):
    """Helper class to map a Lean format ticker to Tiingo format"""

    @staticmethod
    def GetTiingoTicker(symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """Maps a given Symbol instance to it's Tiingo equivalent"""
        ...

    @staticmethod
    def GetLeanTicker(ticker: str) -> str:
        """Maps a given Tiingo ticker to Lean equivalent"""
        ...


class TiingoNewsJsonConverter(JsonConverter):
    """
    Helper json converter class used to convert a list of Tiingo news data
    into List{TiingoNews}
    """

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str] = None) -> None:
        """
        Creates a new instance of the json converter
        
        :param symbol: The Symbol instance associated with this news
        """
        ...

    def WriteJson(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
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

    def CanConvert(self, objectType: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param objectType: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...

    @staticmethod
    def DeserializeNews(token: typing.Any) -> QuantConnect.Data.Custom.Tiingo.TiingoNews:
        """
        Helper method to deserialize a single json Tiingo news
        
        :param token: The json token containing the Tiingo news to deserialize
        :returns: The deserialized TiingoNews instance.
        """
        ...


class TiingoPrice(QuantConnect.Data.Market.TradeBar):
    """
    Tiingo daily price data
    https://api.tiingo.com/docs/tiingo/daily
    """

    @property
    def EndTime(self) -> datetime.datetime:
        """
        The end time of this data. Some data covers spans (trade bars) and as such we want
        to know the entire time span covered
        """
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """
        The end time of this data. Some data covers spans (trade bars) and as such we want
        to know the entire time span covered
        """
        ...

    @property
    def Period(self) -> datetime.timedelta:
        """The period of this trade bar, (second, minute, daily, ect...)"""
        ...

    @Period.setter
    def Period(self, value: datetime.timedelta):
        """The period of this trade bar, (second, minute, daily, ect...)"""
        ...

    @property
    def Date(self) -> datetime.datetime:
        """The date this data pertains to"""
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        """The date this data pertains to"""
        ...

    @property
    def Open(self) -> float:
        """The actual (not adjusted) open price of the asset on the specific date"""
        ...

    @Open.setter
    def Open(self, value: float):
        """The actual (not adjusted) open price of the asset on the specific date"""
        ...

    @property
    def High(self) -> float:
        """The actual (not adjusted) high price of the asset on the specific date"""
        ...

    @High.setter
    def High(self, value: float):
        """The actual (not adjusted) high price of the asset on the specific date"""
        ...

    @property
    def Low(self) -> float:
        """The actual (not adjusted) low price of the asset on the specific date"""
        ...

    @Low.setter
    def Low(self, value: float):
        """The actual (not adjusted) low price of the asset on the specific date"""
        ...

    @property
    def Close(self) -> float:
        """The actual (not adjusted) closing price of the asset on the specific date"""
        ...

    @Close.setter
    def Close(self, value: float):
        """The actual (not adjusted) closing price of the asset on the specific date"""
        ...

    @property
    def Volume(self) -> float:
        """The actual (not adjusted) number of shares traded during the day"""
        ...

    @Volume.setter
    def Volume(self, value: float):
        """The actual (not adjusted) number of shares traded during the day"""
        ...

    @property
    def AdjustedOpen(self) -> float:
        """The adjusted opening price of the asset on the specific date. Returns null if not available."""
        ...

    @AdjustedOpen.setter
    def AdjustedOpen(self, value: float):
        """The adjusted opening price of the asset on the specific date. Returns null if not available."""
        ...

    @property
    def AdjustedHigh(self) -> float:
        """The adjusted high price of the asset on the specific date. Returns null if not available."""
        ...

    @AdjustedHigh.setter
    def AdjustedHigh(self, value: float):
        """The adjusted high price of the asset on the specific date. Returns null if not available."""
        ...

    @property
    def AdjustedLow(self) -> float:
        """The adjusted low price of the asset on the specific date. Returns null if not available."""
        ...

    @AdjustedLow.setter
    def AdjustedLow(self, value: float):
        """The adjusted low price of the asset on the specific date. Returns null if not available."""
        ...

    @property
    def AdjustedClose(self) -> float:
        """The adjusted close price of the asset on the specific date. Returns null if not available."""
        ...

    @AdjustedClose.setter
    def AdjustedClose(self, value: float):
        """The adjusted close price of the asset on the specific date. Returns null if not available."""
        ...

    @property
    def AdjustedVolume(self) -> int:
        """The adjusted number of shares traded during the day - adjusted for splits. Returns null if not available"""
        ...

    @AdjustedVolume.setter
    def AdjustedVolume(self, value: int):
        """The adjusted number of shares traded during the day - adjusted for splits. Returns null if not available"""
        ...

    @property
    def Dividend(self) -> float:
        """The dividend paid out on "date" (note that "date" will be the "exDate" for the dividend)"""
        ...

    @Dividend.setter
    def Dividend(self, value: float):
        """The dividend paid out on "date" (note that "date" will be the "exDate" for the dividend)"""
        ...

    @property
    def SplitFactor(self) -> float:
        """
        A factor used when a company splits or reverse splits. On days where there is ONLY a split (no dividend payment),
        you can calculate the adjusted close as follows: adjClose = "Previous Close"/splitFactor
        """
        ...

    @SplitFactor.setter
    def SplitFactor(self, value: float):
        """
        A factor used when a company splits or reverse splits. On days where there is ONLY a split (no dividend payment),
        you can calculate the adjusted close as follows: adjClose = "Previous Close"/splitFactor
        """
        ...

    def __init__(self) -> None:
        """Initializes an instance of the TiingoPrice class."""
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the URL string source of the file. This will be converted to a stream
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: String URL of source file.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, content: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects. Each data type creates its own factory method,
            and returns a new instance of the object
            each time it is called. The returned object is assumed to be time stamped in the config.ExchangeTimeZone.
        
        :param config: Subscription data config setup object
        :param content: Content of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Instance of the T:BaseData object generated by this line of the CSV.
        """
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

    def DefaultResolution(self) -> int:
        """
        Gets the default resolution for this data and security type
        
        :returns: This method returns the int value of a member of the QuantConnect.Resolution enum.
        """
        ...

    def SupportedResolutions(self) -> System.Collections.Generic.List[QuantConnect.Resolution]:
        """Gets the supported resolution for this data and security type"""
        ...


class TiingoDailyData(QuantConnect.Data.Custom.Tiingo.TiingoPrice):
    """
    Tiingo daily price data
    https://api.tiingo.com/docs/tiingo/daily
    """


