import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Custom
import System.Collections.Generic


class NullData(QuantConnect.Data.BaseData):
    """Represents a custom data type that works as a heartbeat of data in live mode"""

    @property
    def EndTime(self) -> datetime.datetime:
        """
        The end time of this data. Some data covers spans (trade bars)
        and as such we want to know the entire time span covered
        """
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """
        The end time of this data. Some data covers spans (trade bars)
        and as such we want to know the entire time span covered
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the URL string source of localhost as placeholder,
        since this custom data class does not use any data.
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: True if we're in live mode
        :returns: String URL of localhost.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Returns a new instance of the NullData. Its Value property is always 1
        and the Time property is the current date/time of the exchange.
        
        :param config: Subscription data config setup object
        :param line: Line of the source document.
        :param date: Date of the requested data
        :param isLiveMode: True if we're in live mode
        :returns: Instance of NullData.
        """
        ...


class Quandl(QuantConnect.Data.DynamicData):
    """
    Quandl Data Type - Import generic data from quandl, without needing to define Reader methods.
    This reads the headers of the data imported, and dynamically creates properties for the imported data.
    """

    IsAuthCodeSet: bool
    """Flag indicating whether or not the Quanl auth code has been set yet"""

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
        """Gets a time span of one day"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Default quandl constructor uses Close as its value column"""
        ...

    @typing.overload
    def __init__(self, valueColumnName: str) -> None:
        """
        Constructor for creating customized quandl instance which doesn't use "Close" as its value item.
        
        This method is protected.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Generic Reader Implementation for Quandl Data.
        
        :param config: Subscription configuration
        :param line: CSV line of data from the souce
        :param date: Date of the requested line
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Quandl Source Locator: Using the Quandl V1 API automatically set the URL for the dataset.
        
        :param config: Subscription configuration object
        :param date: Date of the data file we're looking for
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: STRING API Url for Quandl.
        """
        ...

    @staticmethod
    def SetAuthCode(authCode: str) -> None:
        """Set the auth code for the quandl set to the QuantConnect auth code."""
        ...


class FxcmVolume(QuantConnect.Data.BaseData):
    """
    FXCM Real FOREX Volume and Transaction data from its clients base, available for the following pairs:
        - EURUSD, USDJPY, GBPUSD, USDCHF, EURCHF, AUDUSD, USDCAD,
          NZDUSD, EURGBP, EURJPY, GBPJPY, EURAUD, EURCAD, AUDJPY
        FXCM only provides support for FX symbols which produced over 110 million average daily volume (ADV) during 2013.
        This limit is imposed to ensure we do not highlight low volume/low ticket symbols in addition to other financial
        reporting concerns.
    """

    @property
    def Transactions(self) -> int:
        """Sum of opening and closing Transactions for the entire time interval."""
        ...

    @Transactions.setter
    def Transactions(self, value: int):
        """Sum of opening and closing Transactions for the entire time interval."""
        ...

    @property
    def Volume(self) -> int:
        """
        Sum of opening and closing Volume for the entire time interval.
            The volume measured in the QUOTE CURRENCY.
        """
        ...

    @Volume.setter
    def Volume(self, value: int):
        """
        Sum of opening and closing Volume for the entire time interval.
            The volume measured in the QUOTE CURRENCY.
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

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects. Each data type creates its own factory method,
            and returns a new instance of the object
            each time it is called. The returned object is assumed to be time stamped in the config.ExchangeTimeZone.
        
        :param config: Subscription data config setup object
        :param line: Line of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Instance of the T:BaseData object generated by this line of the CSV.
        """
        ...


class USEnergyAPI(QuantConnect.Data.BaseData):
    """
    US Energy Information Administration provides extensive data on energy usage, import, export,
    and forecasting across all US energy sectors.
    https://www.eia.gov/opendata/
    """

    @property
    def EnergyDataPointCloseTime(self) -> datetime.datetime:
        """Represents the date/time when the analysis period stops"""
        ...

    @EnergyDataPointCloseTime.setter
    def EnergyDataPointCloseTime(self, value: datetime.datetime):
        """Represents the date/time when the analysis period stops"""
        ...

    @property
    def EndTime(self) -> datetime.datetime:
        """Analysis period (see EnergyDataPointCloseTime) plus a delay to make the data lag emit times realistic"""
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """Analysis period (see EnergyDataPointCloseTime) plus a delay to make the data lag emit times realistic"""
        ...

    AuthCode: str
    """Gets the EIA API token."""

    IsAuthCodeSet: bool
    """Returns true if the EIA API token has been set."""

    @staticmethod
    def SetAuthCode(authCode: str) -> None:
        """
        Sets the EIA API token.
        
        :param authCode: The EIA API token
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

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, content: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects.
        
        :param config: Subscription data config setup object
        :param content: Content of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Collection of USEnergyAPI objects.
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


