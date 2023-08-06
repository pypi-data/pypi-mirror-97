import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Custom.Benzinga
import System
import System.Collections.Generic

JsonConverter = typing.Any


class BenzingaNews(QuantConnect.Data.IndexedBaseData):
    """News data powered by Benzinga - https://docs.benzinga.io/benzinga/newsfeed-v2.html"""

    @property
    def Id(self) -> int:
        """Unique ID assigned to the article by Benzinga"""
        ...

    @Id.setter
    def Id(self, value: int):
        """Unique ID assigned to the article by Benzinga"""
        ...

    @property
    def Author(self) -> str:
        """Author of the article"""
        ...

    @Author.setter
    def Author(self, value: str):
        """Author of the article"""
        ...

    @property
    def CreatedAt(self) -> datetime.datetime:
        """Date the article was published"""
        ...

    @CreatedAt.setter
    def CreatedAt(self, value: datetime.datetime):
        """Date the article was published"""
        ...

    @property
    def UpdatedAt(self) -> datetime.datetime:
        """Date that the article was revised on"""
        ...

    @UpdatedAt.setter
    def UpdatedAt(self, value: datetime.datetime):
        """Date that the article was revised on"""
        ...

    @property
    def Title(self) -> str:
        """Title of the article published"""
        ...

    @Title.setter
    def Title(self, value: str):
        """Title of the article published"""
        ...

    @property
    def Teaser(self) -> str:
        """Summary of the article's contents"""
        ...

    @Teaser.setter
    def Teaser(self, value: str):
        """Summary of the article's contents"""
        ...

    @property
    def Contents(self) -> str:
        """Contents of the article"""
        ...

    @Contents.setter
    def Contents(self, value: str):
        """Contents of the article"""
        ...

    @property
    def Categories(self) -> System.Collections.Generic.List[str]:
        """Categories that relate to the article"""
        ...

    @Categories.setter
    def Categories(self, value: System.Collections.Generic.List[str]):
        """Categories that relate to the article"""
        ...

    @property
    def Symbols(self) -> System.Collections.Generic.List[QuantConnect.Symbol]:
        """Symbols that this news article mentions"""
        ...

    @Symbols.setter
    def Symbols(self, value: System.Collections.Generic.List[QuantConnect.Symbol]):
        """Symbols that this news article mentions"""
        ...

    @property
    def Tags(self) -> System.Collections.Generic.List[str]:
        """
        Additional tags that are not channels/categories, but are reoccuring
        themes including, but not limited to; analyst names, bills being talked
        about in Congress (Dodd-Frank), specific products (iPhone), politicians,
        celebrities, stock movements (i.e. 'Mid-day Losers' & 'Mid-day Gainers').
        """
        ...

    @Tags.setter
    def Tags(self, value: System.Collections.Generic.List[str]):
        """
        Additional tags that are not channels/categories, but are reoccuring
        themes including, but not limited to; analyst names, bills being talked
        about in Congress (Dodd-Frank), specific products (iPhone), politicians,
        celebrities, stock movements (i.e. 'Mid-day Losers' & 'Mid-day Gainers').
        """
        ...

    @property
    def EndTime(self) -> datetime.datetime:
        """Date that the article was revised on"""
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """Date that the article was revised on"""
        ...

    def GetSourceForAnIndex(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, index: str, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Determines the actual source from an index contained within a ticker folder
        
        :param config: Subscription configuration
        :param date: Date
        :param index: File to load data from
        :param isLiveMode: Is live mode
        :returns: SubscriptionDataSource pointing to the article.
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Gets the source of the index file
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: Is live mode
        :returns: SubscriptionDataSource indicating where data is located and how it's stored.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Creates an instance from a line of JSON containing article information read from the `content` directory
        
        :param config: Subscription configuration
        :param line: Line of data
        :param date: Date
        :param isLiveMode: Is live mode
        :returns: New instance of BenzingaNews.
        """
        ...

    def IsSparseData(self) -> bool:
        """
        Indicates whether the data source is sparse.
        If false, it will disable missing file logging.
        
        :returns: true.
        """
        ...

    def RequiresMapping(self) -> bool:
        """
        Indicates whether the data source can undergo
        rename events/is tied to equities.
        
        :returns: true.
        """
        ...

    def DataTimeZone(self) -> typing.Any:
        """
        Set the data time zone to UTC
        
        :returns: Time zone as UTC.
        """
        ...

    def DefaultResolution(self) -> int:
        """
        Sets the default resolution to Second
        
        :returns: Resolution.Second. This method returns the int value of a member of the QuantConnect.Resolution enum.
        """
        ...

    def SupportedResolutions(self) -> System.Collections.Generic.List[QuantConnect.Resolution]:
        """
        Gets a list of all the supported Resolutions
        
        :returns: All resolutions.
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Creates a clone of the instance
        
        :returns: A clone of the instance.
        """
        ...

    def ToString(self) -> str:
        """
        Converts the instance to string
        
        :returns: Article title and contents.
        """
        ...


class BenzingaNewsJsonConverter(JsonConverter):
    """
    Helper json converter class used to convert Benzinga news data
    into BenzingaNews
    
    An example schema of the data in a serialized format is provided
    to help you better understand this converter.
    """

    ShareClassMappedTickers: System.Collections.Generic.Dictionary[str, System.Collections.Generic.HashSet[str]] = ...
    """
    Sometimes "Berkshire Hathaway" is mentioned as "BRK" in the raw data, although it is
    separated into class A and B shares and should appear as BRK.A and BRK.B. Because our
    map file system does not perform the conversion from BRK -> { BRK.A, BRK.B }, we must
    provide them manually. Note that we don't dynamically try to locate class A and B shares
    because there can exist companies with the same base ticker that class A and B shares have.
    For example, CBS trades under "CBS" and "CBS.A", which means that if "CBS" appears, it will
    be automatically mapped to CBS. However, if we dynamically selected "CBS.A" - we might select
    a different company not associated with the ticker being referenced.
    """

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str] = None, liveMode: bool = False) -> None:
        """
        Creates a new instance of the json converter
        
        :param symbol: The Symbol instance associated with this news
        :param liveMode: True if live mode, false for backtesting
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
    def DeserializeNews(item: typing.Any, enableLogging: bool = False) -> QuantConnect.Data.Custom.Benzinga.BenzingaNews:
        """
        Helper method to deserialize a single json Benzinga news
        
        :param item: The json token containing the Benzinga news to deserialize
        :param enableLogging: true to enable logging (for debug purposes)
        :returns: The deserialized BenzingaNews instance.
        """
        ...


