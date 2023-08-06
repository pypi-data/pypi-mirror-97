import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Custom.USTreasury
import System.Collections.Generic


class USTreasuryYieldCurveRate(QuantConnect.Data.BaseData):
    """U.S. Treasury yield curve data"""

    @property
    def OneMonth(self) -> typing.Optional[float]:
        """One month yield curve"""
        ...

    @OneMonth.setter
    def OneMonth(self, value: typing.Optional[float]):
        """One month yield curve"""
        ...

    @property
    def TwoMonth(self) -> typing.Optional[float]:
        """Two month yield curve"""
        ...

    @TwoMonth.setter
    def TwoMonth(self, value: typing.Optional[float]):
        """Two month yield curve"""
        ...

    @property
    def ThreeMonth(self) -> typing.Optional[float]:
        """Three month yield curve"""
        ...

    @ThreeMonth.setter
    def ThreeMonth(self, value: typing.Optional[float]):
        """Three month yield curve"""
        ...

    @property
    def SixMonth(self) -> typing.Optional[float]:
        """Six month yield curve"""
        ...

    @SixMonth.setter
    def SixMonth(self, value: typing.Optional[float]):
        """Six month yield curve"""
        ...

    @property
    def OneYear(self) -> typing.Optional[float]:
        """One year yield curve"""
        ...

    @OneYear.setter
    def OneYear(self, value: typing.Optional[float]):
        """One year yield curve"""
        ...

    @property
    def TwoYear(self) -> typing.Optional[float]:
        """Two year yield curve"""
        ...

    @TwoYear.setter
    def TwoYear(self, value: typing.Optional[float]):
        """Two year yield curve"""
        ...

    @property
    def ThreeYear(self) -> typing.Optional[float]:
        """Three year yield curve"""
        ...

    @ThreeYear.setter
    def ThreeYear(self, value: typing.Optional[float]):
        """Three year yield curve"""
        ...

    @property
    def FiveYear(self) -> typing.Optional[float]:
        """Five year yield curve"""
        ...

    @FiveYear.setter
    def FiveYear(self, value: typing.Optional[float]):
        """Five year yield curve"""
        ...

    @property
    def SevenYear(self) -> typing.Optional[float]:
        """Seven year yield curve"""
        ...

    @SevenYear.setter
    def SevenYear(self, value: typing.Optional[float]):
        """Seven year yield curve"""
        ...

    @property
    def TenYear(self) -> typing.Optional[float]:
        """Ten year yield curve"""
        ...

    @TenYear.setter
    def TenYear(self, value: typing.Optional[float]):
        """Ten year yield curve"""
        ...

    @property
    def TwentyYear(self) -> typing.Optional[float]:
        """Twenty year yield curve"""
        ...

    @TwentyYear.setter
    def TwentyYear(self, value: typing.Optional[float]):
        """Twenty year yield curve"""
        ...

    @property
    def ThirtyYear(self) -> typing.Optional[float]:
        """Thirty year yield curve"""
        ...

    @ThirtyYear.setter
    def ThirtyYear(self, value: typing.Optional[float]):
        """Thirty year yield curve"""
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Specifies the location of the data and directs LEAN where to load the data from
        
        :param config: Subscription configuration
        :param date: Algorithm date
        :param isLiveMode: Is live mode
        :returns: Subscription data source object pointing LEAN to the data location.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reads and parses yield curve data from a csv file
        
        :param config: Subscription configuration
        :param line: CSV line containing yield curve data
        :param date: Date request was made for
        :param isLiveMode: Is live mode
        :returns: YieldCurve instance.
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Clones the object. This method implementation is required
        so that we don't have any null values for our properties
        when the user attempts to use it in backtesting/live trading
        
        :returns: Cloned instance.
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


