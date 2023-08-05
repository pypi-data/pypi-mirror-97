import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Auxiliary
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Securities
import System
import System.Collections
import System.Collections.Generic

QuantConnect_Data_Auxiliary_MapFileRow = typing.Any
QuantConnect_Data_Auxiliary_MapFileResolver_MapFileRowEntry = typing.Any


class MapFileRow(System.Object, System.IEquatable[QuantConnect_Data_Auxiliary_MapFileRow]):
    """Represents a single row in a map_file. This is a csv file ordered as {date, mapped symbol}"""

    @property
    def Date(self) -> datetime.datetime:
        """Gets the date associated with this data"""
        ...

    @property
    def MappedSymbol(self) -> str:
        """Gets the mapped symbol"""
        ...

    @property
    def PrimaryExchange(self) -> int:
        """
        Gets the mapped symbol
        
        This property contains the int value of a member of the QuantConnect.PrimaryExchange enum.
        """
        ...

    @typing.overload
    def __init__(self, date: datetime.datetime, mappedSymbol: str, primaryExchange: str = ...) -> None:
        """Initializes a new instance of the MapFileRow class."""
        ...

    @typing.overload
    def __init__(self, date: datetime.datetime, mappedSymbol: str, primaryExchange: QuantConnect.PrimaryExchange) -> None:
        """Initializes a new instance of the MapFileRow class."""
        ...

    @staticmethod
    @typing.overload
    def Read(permtick: str, market: str) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFileRow]:
        """Reads in the map_file for the specified equity symbol"""
        ...

    @staticmethod
    @typing.overload
    def Read(path: str) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFileRow]:
        """Reads in the map_file at the specified path"""
        ...

    @staticmethod
    def Parse(line: str) -> QuantConnect.Data.Auxiliary.MapFileRow:
        """Parses the specified line into a MapFileRow"""
        ...

    @typing.overload
    def Equals(self, other: QuantConnect.Data.Auxiliary.MapFileRow) -> bool:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Determines whether the specified System.Object is equal to the current System.Object.
        
        :param obj: The object to compare with the current object.
        :returns: true if the specified object  is equal to the current object; otherwise, false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Serves as a hash function for a particular type.
        
        :returns: A hash code for the current System.Object.
        """
        ...

    def ToCsv(self) -> str:
        ...

    def ToString(self) -> str:
        ...


class FactorFileRow(System.Object):
    """Defines a single row in a factor_factor file. This is a csv file ordered as {date, price factor, split factor, reference price}"""

    @property
    def Date(self) -> datetime.datetime:
        """Gets the date associated with this data"""
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        """Gets the date associated with this data"""
        ...

    @property
    def PriceFactor(self) -> float:
        """Gets the price factor associated with this data"""
        ...

    @PriceFactor.setter
    def PriceFactor(self, value: float):
        """Gets the price factor associated with this data"""
        ...

    @property
    def SplitFactor(self) -> float:
        """Gets the split factor associated with the date"""
        ...

    @SplitFactor.setter
    def SplitFactor(self, value: float):
        """Gets the split factor associated with the date"""
        ...

    @property
    def PriceScaleFactor(self) -> float:
        """Gets the combined factor used to create adjusted prices from raw prices"""
        ...

    @PriceScaleFactor.setter
    def PriceScaleFactor(self, value: float):
        """Gets the combined factor used to create adjusted prices from raw prices"""
        ...

    @property
    def ReferencePrice(self) -> float:
        """Gets the raw closing value from the trading date before the updated factor takes effect"""
        ...

    @ReferencePrice.setter
    def ReferencePrice(self, value: float):
        """Gets the raw closing value from the trading date before the updated factor takes effect"""
        ...

    def __init__(self, date: datetime.datetime, priceFactor: float, splitFactor: float, referencePrice: float = 0) -> None:
        """Initializes a new instance of the FactorFileRow class"""
        ...

    @staticmethod
    def Read(permtick: str, market: str, factorFileMinimumDate: typing.Optional[datetime.datetime]) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.FactorFileRow]:
        """Reads in the factor file for the specified equity symbol"""
        ...

    @staticmethod
    def Parse(lines: System.Collections.Generic.IEnumerable[str], factorFileMinimumDate: typing.Optional[datetime.datetime]) -> System.Collections.Generic.List[QuantConnect.Data.Auxiliary.FactorFileRow]:
        """
        Parses the lines as factor files rows while properly handling inf entries
        
        :param lines: The lines from the factor file to be parsed
        :param factorFileMinimumDate: The minimum date from the factor file
        :returns: An enumerable of factor file rows.
        """
        ...

    @typing.overload
    def Apply(self, dividend: QuantConnect.Data.Market.Dividend, exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> QuantConnect.Data.Auxiliary.FactorFileRow:
        """
        Applies the dividend to this factor file row.
        This dividend date must be on or before the factor
        file row date
        
        :param dividend: The dividend to apply with reference price and distribution specified
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :returns: A new factor file row that applies the dividend to this row's factors.
        """
        ...

    @typing.overload
    def Apply(self, split: QuantConnect.Data.Market.Split, exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> QuantConnect.Data.Auxiliary.FactorFileRow:
        """
        Applies the split to this factor file row.
        This split date must be on or before the factor
        file row date
        
        :param split: The split to apply with reference price and split factor specified
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :returns: A new factor file row that applies the split to this row's factors.
        """
        ...

    def GetDividend(self, futureFactorFileRow: QuantConnect.Data.Auxiliary.FactorFileRow, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours, decimalPlaces: int = 2) -> QuantConnect.Data.Market.Dividend:
        """
        Creates a new dividend from this factor file row and the one chronologically in front of it
        This dividend may have a distribution of zero if this row doesn't represent a dividend
        
        :param futureFactorFileRow: The next factor file row in time
        :param symbol: The symbol to use for the dividend
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :param decimalPlaces: The number of decimal places to round the dividend's distribution to, defaulting to 2
        :returns: A new dividend instance.
        """
        ...

    def GetSplit(self, futureFactorFileRow: QuantConnect.Data.Auxiliary.FactorFileRow, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> QuantConnect.Data.Market.Split:
        """
        Creates a new split from this factor file row and the one chronologically in front of it
        This split may have a split factor of one if this row doesn't represent a split
        
        :param futureFactorFileRow: The next factor file row in time
        :param symbol: The symbol to use for the split
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :returns: A new split instance.
        """
        ...

    def ToCsv(self, source: str = None) -> str:
        """Writes this row to csv format"""
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class MapFile(System.Object, System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFileRow], typing.Iterable[QuantConnect.Data.Auxiliary.MapFileRow]):
    """Represents an entire map file for a specified symbol"""

    @property
    def Permtick(self) -> str:
        """Gets the entity's unique symbol, i.e OIH.1"""
        ...

    @property
    def DelistingDate(self) -> datetime.datetime:
        """Gets the last date in the map file which is indicative of a delisting event"""
        ...

    @property
    def FirstDate(self) -> datetime.datetime:
        """Gets the first date in this map file"""
        ...

    @property
    def FirstTicker(self) -> str:
        """Gets the first ticker for the security represented by this map file"""
        ...

    def __init__(self, permtick: str, data: System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFileRow]) -> None:
        """Initializes a new instance of the MapFile class."""
        ...

    def GetMappedSymbol(self, searchDate: datetime.datetime, defaultReturnValue: str = ...) -> str:
        """
        Memory overload search method for finding the mapped symbol for this date.
        
        :param searchDate: date for symbol we need to find.
        :param defaultReturnValue: Default return value if search was got no result.
        :returns: Symbol on this date.
        """
        ...

    def HasData(self, date: datetime.datetime) -> bool:
        """Determines if there's data for the requested date"""
        ...

    def ToCsvLines(self) -> System.Collections.Generic.IEnumerable[str]:
        """
        Reads and writes each MapFileRow
        
        :returns: Enumerable of csv lines.
        """
        ...

    @staticmethod
    def Read(permtick: str, market: str) -> QuantConnect.Data.Auxiliary.MapFile:
        """Reads in an entire map file for the requested symbol from the DataFolder"""
        ...

    def WriteToCsv(self, market: str) -> None:
        """
        Writes the map file to a CSV file
        
        :param market: The market to save the MapFile to
        """
        ...

    @staticmethod
    def GetMapFilePath(permtick: str, market: str) -> str:
        """
        Constructs the map file path for the specified market and symbol
        
        :param permtick: The symbol as on disk, OIH or OIH.1
        :param market: The market this symbol belongs to
        :returns: The file path to the requested map file.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.Auxiliary.MapFileRow]:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Returns an enumerator that iterates through a collection.
        
        :returns: An System.Collections.IEnumerator object that can be used to iterate through the collection.
        """
        ...

    @staticmethod
    def GetMapFiles(mapFileDirectory: str) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFile]:
        ...


class MapFileResolver(System.Object, System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFile], typing.Iterable[QuantConnect.Data.Auxiliary.MapFile]):
    """
    Provides a means of mapping a symbol at a point in time to the map file
    containing that share class's mapping information
    """

    class MapFileRowEntry(System.Object, System.IEquatable[QuantConnect_Data_Auxiliary_MapFileResolver_MapFileRowEntry]):
        """Combines the map file row with the map file path that produced the row"""

        @property
        def MapFileRow(self) -> QuantConnect.Data.Auxiliary.MapFileRow:
            """Gets the map file row"""
            ...

        @MapFileRow.setter
        def MapFileRow(self, value: QuantConnect.Data.Auxiliary.MapFileRow):
            """Gets the map file row"""
            ...

        @property
        def EntitySymbol(self) -> str:
            """Gets the full path to the map file that produced this row"""
            ...

        @EntitySymbol.setter
        def EntitySymbol(self, value: str):
            """Gets the full path to the map file that produced this row"""
            ...

        def __init__(self, entitySymbol: str, mapFileRow: QuantConnect.Data.Auxiliary.MapFileRow) -> None:
            """
            Initializes a new instance of the MapFileRowEntry class
            
            :param entitySymbol: The map file that produced this row
            :param mapFileRow: The map file row data
            """
            ...

        def Equals(self, other: QuantConnect.Data.Auxiliary.MapFileResolver.MapFileRowEntry) -> bool:
            """
            Indicates whether the current object is equal to another object of the same type.
            
            :param other: An object to compare with this object.
            :returns: true if the current object is equal to the  parameter; otherwise, false.
            """
            ...

        def ToString(self) -> str:
            """
            Returns a string that represents the current object.
            
            :returns: A string that represents the current object.
            """
            ...

    Empty: QuantConnect.Data.Auxiliary.MapFileResolver = ...
    """
    Gets an empty MapFileResolver, that is an instance that contains
    zero mappings
    """

    def __init__(self, mapFiles: System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFile]) -> None:
        """
        Initializes a new instance of the MapFileResolver by reading
        in all files in the specified directory.
        
        :param mapFiles: The data used to initialize this resolver.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(dataDirectory: str, market: str) -> QuantConnect.Data.Auxiliary.MapFileResolver:
        """
        Creates a new instance of the MapFileResolver class by reading all map files
        for the specified market into memory
        
        :param dataDirectory: The root data directory
        :param market: The equity market to produce a map file collection for
        :returns: The collection of map files capable of mapping equity symbols within the specified market.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(mapFileDirectory: str) -> QuantConnect.Data.Auxiliary.MapFileResolver:
        """
        Creates a new instance of the MapFileResolver class by reading all map files
        for the specified market into memory
        
        :param mapFileDirectory: The directory containing the map files
        :returns: The collection of map files capable of mapping equity symbols within the specified market.
        """
        ...

    def GetByPermtick(self, permtick: str) -> QuantConnect.Data.Auxiliary.MapFile:
        """
        Gets the map file matching the specified permtick
        
        :param permtick: The permtick to match on
        :returns: The map file matching the permtick, or null if not found.
        """
        ...

    def ResolveMapFile(self, symbol: str, date: datetime.datetime) -> QuantConnect.Data.Auxiliary.MapFile:
        """
        Resolves the map file path containing the mapping information for the symbol defined at
        
        :param symbol: The symbol as of  to be mapped
        :param date: The date associated with the
        :returns: The map file responsible for mapping the symbol, if no map file is found, null is returned.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.Auxiliary.MapFile]:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Returns an enumerator that iterates through a collection.
        
        :returns: An System.Collections.IEnumerator object that can be used to iterate through the collection.
        """
        ...


class QuoteConditionFlags(System.Enum):
    """Flag system for quote conditions"""

    # Cannot convert to Python: None = 0

    Regular = ...

    Slow = ...

    Gap = ...

    Closing = ...

    NewsDissemination = ...

    NewsPending = ...

    TradingRangeIndication = ...

    OrderImbalance = ...

    ClosedMarketMaker = ...

    VolatilityTradingPause = ...

    NonFirmQuote = ...

    OpeningQuote = ...

    DueToRelatedSecurity = ...

    Resume = ...

    InViewOfCommon = ...

    EquipmentChangeover = ...

    SubPennyTrading = ...

    NoOpenNoResume = ...

    LimitUpLimitDownPriceBand = ...

    RepublishedLimitUpLimitDownPriceBand = ...

    Manual = ...

    FastTrading = ...

    OrderInflux = ...


class LocalDiskMapFileProvider(System.Object, QuantConnect.Interfaces.IMapFileProvider):
    """
    Provides a default implementation of IMapFileProvider that reads from
    the local disk
    """

    def Get(self, market: str) -> QuantConnect.Data.Auxiliary.MapFileResolver:
        """
        Gets a MapFileResolver representing all the map
        files for the specified market
        
        :param market: The equity market, for example, 'usa'
        :returns: A MapFileRow containing all map files for the specified market.
        """
        ...


class TradeConditionFlags(System.Enum):
    """Flag system for trade conditions"""

    # Cannot convert to Python: None = 0

    Regular = ...

    Cash = ...

    NextDay = ...

    Seller = ...

    YellowFlag = ...

    IntermarketSweep = ...

    OpeningPrints = ...

    ClosingPrints = ...

    ReOpeningPrints = ...

    DerivativelyPriced = ...

    FormT = ...

    Sold = ...

    Stopped = ...

    ExtendedHours = ...

    OutOfSequence = ...

    Split = ...

    Acquisition = ...

    Bunched = ...

    StockOption = ...

    Distribution = ...

    AveragePrice = ...

    Cross = ...

    PriceVariation = ...

    Rule155 = ...

    OfficialClose = ...

    PriorReferencePrice = ...

    OfficialOpen = ...

    CapElection = ...

    AutoExecution = ...

    TradeThroughExempt = ...

    UndocumentedFlag = ...

    OddLot = ...


class MapFilePrimaryExchangeProvider(System.Object, QuantConnect.Interfaces.IPrimaryExchangeProvider):
    """Implementation of IPrimaryExchangeProvider from map files."""

    def __init__(self, mapFileProvider: QuantConnect.Interfaces.IMapFileProvider) -> None:
        ...

    def GetPrimaryExchange(self, securityIdentifier: QuantConnect.SecurityIdentifier) -> int:
        """
        Gets the primary exchange for a given security identifier
        
        :param securityIdentifier: The security identifier to get the primary exchange for
        :returns: Returns the primary exchange or null if not found. This method returns the int value of a member of the QuantConnect.PrimaryExchange enum.
        """
        ...


class MappingExtensions(System.Object):
    """Mapping extensions helper methods"""

    @staticmethod
    def ResolveMapFile(mapFileResolver: QuantConnect.Data.Auxiliary.MapFileResolver, symbol: typing.Union[QuantConnect.Symbol, str], dataType: typing.Type) -> QuantConnect.Data.Auxiliary.MapFile:
        """
        Helper method to resolve the mapping file to use.
        
        :param mapFileResolver: The map file resolver
        :param symbol: The symbol that we want to map
        :param dataType: The configuration data type SubscriptionDataConfig.Type
        :returns: The mapping file to use.
        """
        ...


class FactorFile(System.Object, System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.FactorFileRow], typing.Iterable[QuantConnect.Data.Auxiliary.FactorFileRow]):
    """Represents an entire factor file for a specified symbol"""

    @property
    def SortedFactorFileData(self) -> System.Collections.Generic.SortedList[datetime.datetime, QuantConnect.Data.Auxiliary.FactorFileRow]:
        """The factor file data rows sorted by date"""
        ...

    @SortedFactorFileData.setter
    def SortedFactorFileData(self, value: System.Collections.Generic.SortedList[datetime.datetime, QuantConnect.Data.Auxiliary.FactorFileRow]):
        """The factor file data rows sorted by date"""
        ...

    @property
    def FactorFileMinimumDate(self) -> typing.Optional[datetime.datetime]:
        """The minimum tradeable date for the symbol"""
        ...

    @FactorFileMinimumDate.setter
    def FactorFileMinimumDate(self, value: typing.Optional[datetime.datetime]):
        """The minimum tradeable date for the symbol"""
        ...

    @property
    def MostRecentFactorChange(self) -> datetime.datetime:
        """Gets the most recent factor change in the factor file"""
        ...

    @property
    def Permtick(self) -> str:
        """Gets the symbol this factor file represents"""
        ...

    def __init__(self, permtick: str, data: System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.FactorFileRow], factorFileMinimumDate: typing.Optional[datetime.datetime] = None) -> None:
        """Initializes a new instance of the FactorFile class."""
        ...

    @staticmethod
    def Read(permtick: str, market: str) -> QuantConnect.Data.Auxiliary.FactorFile:
        """Reads a FactorFile in from the Globals.DataFolder."""
        ...

    @staticmethod
    def Parse(permtick: str, lines: System.Collections.Generic.IEnumerable[str]) -> QuantConnect.Data.Auxiliary.FactorFile:
        """Parses the specified lines as a factor file"""
        ...

    def GetPriceScaleFactor(self, searchDate: datetime.datetime) -> float:
        """Gets the price scale factor that includes dividend and split adjustments for the specified search date"""
        ...

    def GetSplitFactor(self, searchDate: datetime.datetime) -> float:
        """Gets the split factor to be applied at the specified date"""
        ...

    def GetScalingFactors(self, searchDate: datetime.datetime) -> QuantConnect.Data.Auxiliary.FactorFileRow:
        """Gets price and split factors to be applied at the specified date"""
        ...

    @staticmethod
    def HasScalingFactors(permtick: str, market: str) -> bool:
        """Checks whether or not a symbol has scaling factors"""
        ...

    def HasDividendEventOnNextTradingDay(self, date: datetime.datetime, priceFactorRatio: float, referencePrice: float) -> bool:
        """
        Returns true if the specified date is the last trading day before a dividend event
        is to be fired
        
        :param date: The date to check the factor file for a dividend event
        :param priceFactorRatio: When this function returns true, this value will be populated with the price factor ratio required to scale the closing value (pf_i/pf_i+1)
        :param referencePrice: When this function returns true, this value will be populated with the reference raw price, which is the close of the provided date
        """
        ...

    def HasSplitEventOnNextTradingDay(self, date: datetime.datetime, splitFactor: float, referencePrice: float) -> bool:
        """
        Returns true if the specified date is the last trading day before a split event
        is to be fired
        
        :param date: The date to check the factor file for a split event
        :param splitFactor: When this function returns true, this value will be populated with the split factor ratio required to scale the closing value
        :param referencePrice: When this function returns true, this value will be populated with the reference raw price, which is the close of the provided date
        """
        ...

    def ToCsvLines(self) -> System.Collections.Generic.IEnumerable[str]:
        """
        Writes this factor file data to an enumerable of csv lines
        
        :returns: An enumerable of lines representing this factor file.
        """
        ...

    def WriteToCsv(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> None:
        """
        Write the factor file to the correct place in the default Data folder
        
        :param symbol: The symbol this factor file represents
        """
        ...

    def GetSplitsAndDividends(self, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours, decimalPlaces: int = 2) -> System.Collections.Generic.List[QuantConnect.Data.BaseData]:
        """
        Gets all of the splits and dividends represented by this factor file
        
        :param symbol: The symbol to ues for the dividend and split objects
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :param decimalPlaces: The number of decimal places to round the dividend's distribution to, defaulting to 2
        :returns: All splits and diviends represented by this factor file in chronological order.
        """
        ...

    def Apply(self, data: System.Collections.Generic.List[QuantConnect.Data.BaseData], exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> QuantConnect.Data.Auxiliary.FactorFile:
        """
        Creates a new factor file with the specified data applied.
        Only Dividend and Split data types
        will be used.
        
        :param data: The data to apply
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :returns: A new factor file that incorporates the specified dividend.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.Auxiliary.FactorFileRow]:
        """
        Returns an enumerator that iterates through the collection.
        
        :returns: A System.Collections.Generic.IEnumerator`1 that can be used to iterate through the collection.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Returns an enumerator that iterates through a collection.
        
        :returns: An System.Collections.IEnumerator object that can be used to iterate through the collection.
        """
        ...


class LocalDiskFactorFileProvider(System.Object, QuantConnect.Interfaces.IFactorFileProvider):
    """Provides an implementation of IFactorFileProvider that searches the local disk"""

    @typing.overload
    def __init__(self) -> None:
        """
        Initializes a new instance of LocalDiskFactorFileProvider that uses configuration
        to resolve an instance of IMapFileProvider from the Composer.Instance
        """
        ...

    @typing.overload
    def __init__(self, mapFileProvider: QuantConnect.Interfaces.IMapFileProvider) -> None:
        """
        Initializes a new instance of the LocalDiskFactorFileProvider using the specified
        map file provider
        
        :param mapFileProvider: The map file provider used to resolve permticks of securities
        """
        ...

    def Get(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect.Data.Auxiliary.FactorFile:
        """
        Gets a FactorFile instance for the specified symbol, or null if not found
        
        :param symbol: The security's symbol whose factor file we seek
        :returns: The resolved factor file, or null if not found.
        """
        ...


class ZipEntryName(QuantConnect.Data.BaseData):
    """Defines a data type that just produces data points from the zip entry names in a zip file"""

    def __init__(self) -> None:
        """Initializes a new instance of the ZipEntryName class"""
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects. Each data type creates its own factory method, and returns a new instance of the object
        each time it is called. The returned object is assumed to be time stamped in the config.ExchangeTimeZone.
        
        :param config: Subscription data config setup object
        :param line: Line of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Instance of the T:BaseData object generated by this line of the CSV.
        """
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


