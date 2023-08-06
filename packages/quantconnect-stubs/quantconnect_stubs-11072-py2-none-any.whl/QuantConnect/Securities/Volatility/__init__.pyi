import datetime

import QuantConnect.Data
import QuantConnect.Interfaces
import QuantConnect.Securities
import QuantConnect.Securities.Volatility
import System
import System.Collections.Generic


class BaseVolatilityModel(System.Object, QuantConnect.Securities.IVolatilityModel):
    """Represents a base model that computes the volatility of a security"""

    @property
    def SubscriptionDataConfigProvider(self) -> QuantConnect.Interfaces.ISubscriptionDataConfigProvider:
        """
        Provides access to registered SubscriptionDataConfig
        
        This field is protected.
        """
        ...

    @SubscriptionDataConfigProvider.setter
    def SubscriptionDataConfigProvider(self, value: QuantConnect.Interfaces.ISubscriptionDataConfigProvider):
        """
        Provides access to registered SubscriptionDataConfig
        
        This field is protected.
        """
        ...

    @property
    def Volatility(self) -> float:
        """Gets the volatility of the security as a percentage"""
        ...

    def SetSubscriptionDataConfigProvider(self, subscriptionDataConfigProvider: QuantConnect.Interfaces.ISubscriptionDataConfigProvider) -> None:
        """
        Sets the ISubscriptionDataConfigProvider instance to use.
        
        :param subscriptionDataConfigProvider: Provides access to registered SubscriptionDataConfig
        """
        ...

    def Update(self, security: QuantConnect.Securities.Security, data: QuantConnect.Data.BaseData) -> None:
        """
        Updates this model using the new price information in
        the specified security instance
        
        :param security: The security to calculate volatility for
        :param data: The new data used to update the model
        """
        ...

    def GetHistoryRequirements(self, security: QuantConnect.Securities.Security, utcTime: datetime.datetime) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.HistoryRequest]:
        """
        Returns history requirements for the volatility model expressed in the form of history request
        
        :param security: The security of the request
        :param utcTime: The date/time of the request
        :returns: History request object list, or empty if no requirements.
        """
        ...


