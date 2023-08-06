import datetime

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Custom.CBOE
import QuantConnect.Data.Market
import System.Collections.Generic


class CBOE(QuantConnect.Data.Market.TradeBar):
    """This class has no documentation."""

    def __init__(self) -> None:
        """Creates a new instance of the object"""
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """Gets the source location of the CBOE file"""
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reads the data from the source and creates a BaseData instance
        
        :param config: Configuration
        :param line: Line of data
        :param date: Date we're requesting data for
        :param isLiveMode: Is live mode
        :returns: New BaseData instance to be used in the algorithm.
        """
        ...

    def RequiresMapping(self) -> bool:
        """
        Determines whether the data source requires mapping
        
        :returns: false.
        """
        ...

    def IsSparseData(self) -> bool:
        """
        Determines if data source is sparse
        
        :returns: false.
        """
        ...

    def ToString(self) -> str:
        """
        Converts the instance to a string
        
        :returns: String containing open, high, low, close.
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


