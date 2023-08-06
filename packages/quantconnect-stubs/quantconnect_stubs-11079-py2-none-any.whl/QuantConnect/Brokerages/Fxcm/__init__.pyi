import datetime
import typing

import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Brokerages.Fxcm
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Securities
import System
import System.Collections.Generic

IGenericMessageListener = typing.Any
System_EventHandler = typing.Any


class FxcmSymbolMapper(System.Object, QuantConnect.Brokerages.ISymbolMapper):
    """Provides the mapping between Lean symbols and FXCM symbols."""

    KnownSymbols: System.Collections.Generic.List[QuantConnect.Symbol]
    """List of all known symbols for FXCM"""

    def GetBrokerageSymbol(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """
        Converts a Lean symbol instance to an FXCM symbol
        
        :param symbol: A Lean symbol instance
        :returns: The FXCM symbol.
        """
        ...

    def GetLeanSymbol(self, brokerageSymbol: str, securityType: QuantConnect.SecurityType, market: str, expirationDate: datetime.datetime = ..., strike: float = 0, optionRight: QuantConnect.OptionRight = 0) -> QuantConnect.Symbol:
        """
        Converts an FXCM symbol to a Lean symbol instance
        
        :param brokerageSymbol: The FXCM symbol
        :param securityType: The security type
        :param market: The market
        :param expirationDate: Expiration date of the security(if applicable)
        :param strike: The strike of the security (if applicable)
        :param optionRight: The option right of the security (if applicable)
        :returns: A new Lean Symbol instance.
        """
        ...

    def GetBrokerageSecurityType(self, brokerageSymbol: str) -> int:
        """
        Returns the security type for an FXCM symbol
        
        :param brokerageSymbol: The FXCM symbol
        :returns: The security type. This method returns the int value of a member of the QuantConnect.SecurityType enum.
        """
        ...

    def GetLeanSecurityType(self, leanSymbol: str) -> int:
        """
        Returns the security type for a Lean symbol
        
        :param leanSymbol: The Lean symbol
        :returns: The security type. This method returns the int value of a member of the QuantConnect.SecurityType enum.
        """
        ...

    def IsKnownBrokerageSymbol(self, brokerageSymbol: str) -> bool:
        """
        Checks if the symbol is supported by FXCM
        
        :param brokerageSymbol: The FXCM symbol
        :returns: True if FXCM supports the symbol.
        """
        ...

    def IsKnownLeanSymbol(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Checks if the symbol is supported by FXCM
        
        :param symbol: The Lean symbol
        :returns: True if FXCM supports the symbol.
        """
        ...

    @staticmethod
    def ConvertFxcmSymbolToLeanSymbol(fxcmSymbol: str) -> str:
        """Converts an FXCM symbol to a Lean symbol string"""
        ...


class FxcmBrokerage(QuantConnect.Brokerages.Brokerage, QuantConnect.Interfaces.IDataQueueHandler, IGenericMessageListener):
    """FXCM brokerage - private helper functions"""

    @property
    def HistoryResponseTimeout(self) -> int:
        """Gets/sets a timeout for history requests (in milliseconds)"""
        ...

    @HistoryResponseTimeout.setter
    def HistoryResponseTimeout(self, value: int):
        """Gets/sets a timeout for history requests (in milliseconds)"""
        ...

    @property
    def MaximumHistoryRetryAttempts(self) -> int:
        """Gets/sets the maximum number of retries for a history request"""
        ...

    @MaximumHistoryRetryAttempts.setter
    def MaximumHistoryRetryAttempts(self, value: int):
        """Gets/sets the maximum number of retries for a history request"""
        ...

    @property
    def EnableOnlyHistoryRequests(self) -> bool:
        """
        Gets/sets a value to enable only history requests to this brokerage
        Set to true in parallel downloaders to avoid loading accounts, orders, positions etc. at connect time
        """
        ...

    @EnableOnlyHistoryRequests.setter
    def EnableOnlyHistoryRequests(self, value: bool):
        """
        Gets/sets a value to enable only history requests to this brokerage
        Set to true in parallel downloaders to avoid loading accounts, orders, positions etc. at connect time
        """
        ...

    @property
    def IsConnected(self) -> bool:
        ...

    @staticmethod
    def OrderIsClosed(orderStatus: str) -> bool:
        """
        Returns true if the specified order is considered close, otherwise false
        
        This method is protected.
        """
        ...

    @staticmethod
    def ToFxcmInterval(resolution: QuantConnect.Resolution) -> typing.Any:
        """
        Converts a LEAN Resolution to an IFXCMTimingInterval
        
        :param resolution: The resolution to convert
        """
        ...

    @staticmethod
    def ToJavaDateUtc(utcDateTime: datetime.datetime) -> typing.Any:
        """
        Converts a Java Date value to a UTC DateTime value
        
        :param utcDateTime: The UTC DateTime value
        :returns: A UTC Java Date value.
        """
        ...

    def GetBidAndAsk(self, fxcmSymbols: System.Collections.Generic.List[str]) -> System.Collections.Generic.List[QuantConnect.Data.Market.Tick]:
        """
        Provides as public access to this data without requiring consumers to reference
        IKVM libraries
        """
        ...

    @typing.overload
    def messageArrived(self, message: typing.Any) -> None:
        ...

    @typing.overload
    def messageArrived(self, message: typing.Any) -> None:
        ...

    def __init__(self, orderProvider: QuantConnect.Securities.IOrderProvider, securityProvider: QuantConnect.Securities.ISecurityProvider, aggregator: QuantConnect.Data.IDataAggregator, server: str, terminal: str, userName: str, password: str, accountId: str) -> None:
        """
        Creates a new instance of the FxcmBrokerage class
        
        :param orderProvider: The order provider
        :param securityProvider: The holdings provider
        :param aggregator: Consolidate ticks
        :param server: The url of the server
        :param terminal: The terminal name
        :param userName: The user name (login id)
        :param password: The user password
        :param accountId: The account id
        """
        ...

    def Connect(self) -> None:
        """Connects the client to the broker's remote servers"""
        ...

    def Disconnect(self) -> None:
        """Disconnects the client from the broker's remote servers"""
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """
        Gets all open orders on the account.
        NOTE: The order objects returned do not have QC order IDs.
        
        :returns: The open orders returned from FXCM.
        """
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """
        Gets all holdings for the account
        
        :returns: The current holdings from the account.
        """
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """
        Gets the current cash balance for each currency held in the brokerage account
        
        :returns: The current cash balance for each currency available for trading.
        """
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Places a new order and assigns a new broker ID to the order
        
        :param order: The order to be placed
        :returns: True if the request for a new order has been placed, false otherwise.
        """
        ...

    def UpdateOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Updates the order with the same id
        
        :param order: The new order information
        :returns: True if the request was made for the order to be updated, false otherwise.
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was made for the order to be canceled, false otherwise.
        """
        ...

    def GetHistory(self, request: QuantConnect.Data.HistoryRequest) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Gets the history for the requested security
        
        :param request: The historical data request
        :returns: An enumerable of bars covering the span specified in the request.
        """
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        ...

    def Subscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig, newDataAvailableHandler: System_EventHandler) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """
        Subscribe to the specified configuration
        
        :param dataConfig: defines the parameters to subscribe to a data feed
        :param newDataAvailableHandler: handler to be fired on new data available
        :returns: The new enumerator for this subscription request.
        """
        ...

    def Unsubscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """
        Removes the specified configuration
        
        :param dataConfig: Subscription config to be removed
        """
        ...


class FxcmBrokerageFactory(QuantConnect.Brokerages.BrokerageFactory):
    """Provides an implementation of IBrokerageFactory that produces a FxcmBrokerage"""

    @property
    def BrokerageData(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Gets the brokerage data required to run the brokerage from configuration/disk"""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the FxcmBrokerageFactory class"""
        ...

    def GetBrokerageModel(self, orderProvider: QuantConnect.Securities.IOrderProvider) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        Gets a new instance of the FxcmBrokerageModel
        
        :param orderProvider: The order provider
        """
        ...

    def CreateBrokerage(self, job: QuantConnect.Packets.LiveNodePacket, algorithm: QuantConnect.Interfaces.IAlgorithm) -> QuantConnect.Interfaces.IBrokerage:
        """
        Creates a new IBrokerage instance
        
        :param job: The job packet to create the brokerage for
        :param algorithm: The algorithm instance
        :returns: A new brokerage instance.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def CreateBrokerageMessageHandler(self, algorithm: QuantConnect.Interfaces.IAlgorithm, job: QuantConnect.Packets.AlgorithmNodePacket, api: QuantConnect.Interfaces.IApi) -> QuantConnect.Brokerages.IBrokerageMessageHandler:
        """Gets a brokerage message handler"""
        ...


