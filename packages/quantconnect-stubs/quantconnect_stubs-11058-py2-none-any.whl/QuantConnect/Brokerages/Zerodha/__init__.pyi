import datetime
import typing

import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Brokerages.Zerodha
import QuantConnect.Brokerages.Zerodha.Messages
import QuantConnect.Data
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Securities
import System
import System.Collections
import System.Collections.Concurrent
import System.Collections.Generic
import System.IO
import System.Net

System_EventHandler = typing.Any


class Kite(System.Object):
    """The API client class. In production, you may initialize a single instance of this class per `APIKey`."""

    def __init__(self, APIKey: str, AccessToken: str = None, Root: str = None, Timeout: int = 7000, Proxy: typing.Any = None, Pool: int = 2) -> None:
        """
        Initialize a new Kite Connect client instance.
        
        :param APIKey: API Key issued to you
        :param AccessToken: The token obtained after the login flow in exchange for the `RequestToken` . Pre-login, this will default to None,but once you have obtained it, you should persist it in a database or session to pass to the Kite Connect class initialisation for subsequent requests.
        :param Root: API end point root. Unless you explicitly want to send API requests to a non-default endpoint, this can be ignored.
        :param Timeout: Time in milliseconds for which  the API client will wait for a request to complete before it fails
        :param Proxy: To set proxy for http request. Should be an object of WebProxy.
        :param Pool: Number of connections to server. Client will reuse the connections if they are alive.
        """
        ...

    def SetSessionExpiryHook(self, Method: System.Action) -> None:
        """
        Set a callback hook for session (`TokenException` -- timeout, expiry etc.) errors.
        An `AccessToken` (login session) can become invalid for a number of
        reasons, but it doesn't make sense for the client to
        try and catch it during every API call.
        A callback method that handles session errors
        can be set here and when the client encounters
        a token error at any point, it'll be called.
        This callback, for instance, can log the user out of the UI,
        clear session cookies, or initiate a fresh login.
        
        :param Method: Action to be invoked when session becomes invalid.
        """
        ...

    def SetAccessToken(self, AccessToken: str) -> None:
        """
        Set the `AccessToken` received after a successful authentication.
        
        :param AccessToken: Access token for the session.
        """
        ...

    def GenerateSession(self, RequestToken: str, AppSecret: str) -> QuantConnect.Brokerages.Zerodha.Messages.User:
        """
        Do the token exchange with the `RequestToken` obtained after the login flow,
        and retrieve the `AccessToken` required for all subsequent requests.The
        response contains not just the `AccessToken`, but metadata for
        the user who has authenticated.
        
        :param RequestToken: Token obtained from the GET paramers after a successful login redirect.
        :param AppSecret: API secret issued with the API key.
        :returns: User structure with tokens and profile data.
        """
        ...

    def InvalidateAccessToken(self, AccessToken: str = None) -> System.Collections.Generic.Dictionary[str, typing.Any]:
        """
        Kill the session by invalidating the access token
        
        :param AccessToken: Access token to invalidate. Default is the active access token.
        :returns: Json response in the form of nested string dictionary.
        """
        ...

    def InvalidateRefreshToken(self, RefreshToken: str) -> System.Collections.Generic.Dictionary[str, typing.Any]:
        """
        Invalidates RefreshToken
        
        :param RefreshToken: RefreshToken to invalidate
        :returns: Json response in the form of nested string dictionary.
        """
        ...

    def RenewAccessToken(self, RefreshToken: str, AppSecret: str) -> QuantConnect.Brokerages.Zerodha.Messages.TokenSet:
        """
        Renew AccessToken using RefreshToken
        
        :param RefreshToken: RefreshToken to renew the AccessToken.
        :param AppSecret: API secret issued with the API key.
        :returns: TokenRenewResponse that contains new AccessToken and RefreshToken.
        """
        ...

    def GetProfile(self) -> QuantConnect.Brokerages.Zerodha.Messages.Profile:
        """
        Gets currently logged in user details
        
        :returns: User profile.
        """
        ...

    @typing.overload
    def GetMargins(self) -> QuantConnect.Brokerages.Zerodha.Messages.UserMarginsResponse:
        """
        Get account balance and cash margin details for all segments.
        
        :returns: User margin response with both equity and commodity margins.
        """
        ...

    @typing.overload
    def GetMargins(self, Segment: str) -> QuantConnect.Brokerages.Zerodha.Messages.UserMargin:
        """
        Get account balance and cash margin details for a particular segment.
        
        :param Segment: Trading segment (eg: equity or commodity)
        :returns: Margins for specified segment.
        """
        ...

    def PlaceOrder(self, Exchange: str, TradingSymbol: str, TransactionType: str, Quantity: int, Price: typing.Optional[float] = None, Product: str = None, OrderType: str = None, Validity: str = None, DisclosedQuantity: typing.Optional[int] = None, TriggerPrice: typing.Optional[float] = None, SquareOffValue: typing.Optional[float] = None, StoplossValue: typing.Optional[float] = None, TrailingStoploss: typing.Optional[float] = None, Variety: str = ..., Tag: str = ...) -> typing.Any:
        """
        Place an order
        
        :param Exchange: Name of the exchange
        :param TradingSymbol: Tradingsymbol of the instrument
        :param TransactionType: BUY or SELL
        :param Quantity: Quantity to transact
        :param Price: For LIMIT orders
        :param Product: Margin product applied to the order (margin is blocked based on this)
        :param OrderType: Order type (MARKET, LIMIT etc.)
        :param Validity: Order validity
        :param DisclosedQuantity: Quantity to disclose publicly (for equity trades)
        :param TriggerPrice: For SL, SL-M etc.
        :param SquareOffValue: Price difference at which the order should be squared off and profit booked (eg: Order price is 100. Profit target is 102. So squareoff = 2)
        :param StoplossValue: Stoploss difference at which the order should be squared off (eg: Order price is 100. Stoploss target is 98. So stoploss = 2)
        :param TrailingStoploss: Incremental value by which stoploss price changes when market moves in your favor by the same incremental value from the entry price (optional)
        :param Variety: You can place orders of varieties; regular orders, after market orders, cover orders etc.
        :param Tag: An optional tag to apply to an order to identify it (alphanumeric, max 8 chars)
        :returns: Json response in the form of nested string dictionary.
        """
        ...

    def ModifyOrder(self, OrderId: str, ParentOrderId: str = None, Exchange: str = None, TradingSymbol: str = None, TransactionType: str = None, Quantity: typing.Optional[int] = None, Price: typing.Optional[float] = None, Product: str = None, OrderType: str = None, Validity: str = ..., DisclosedQuantity: typing.Optional[int] = None, TriggerPrice: typing.Optional[float] = None, Variety: str = ...) -> typing.Any:
        """
        Modify an open order.
        
        :param OrderId: Id of the order to be modified
        :param ParentOrderId: Id of the parent order (obtained from the /orders call) as BO is a multi-legged order
        :param Exchange: Name of the exchange
        :param TradingSymbol: Tradingsymbol of the instrument
        :param TransactionType: BUY or SELL
        :param Quantity: Quantity to transact
        :param Price: For LIMIT orders
        :param Product: Margin product applied to the order (margin is blocked based on this)
        :param OrderType: Order type (MARKET, LIMIT etc.)
        :param Validity: Order validity
        :param DisclosedQuantity: Quantity to disclose publicly (for equity trades)
        :param TriggerPrice: For SL, SL-M etc.
        :param Variety: You can place orders of varieties; regular orders, after market orders, cover orders etc.
        :returns: Json response in the form of nested string dictionary.
        """
        ...

    def CancelOrder(self, OrderId: str, Variety: str = ..., ParentOrderId: str = None) -> typing.Any:
        """
        Cancel an order
        
        :param OrderId: Id of the order to be cancelled
        :param Variety: You can place orders of varieties; regular orders, after market orders, cover orders etc.
        :param ParentOrderId: Id of the parent order (obtained from the /orders call) as BO is a multi-legged order
        :returns: Json response in the form of nested string dictionary.
        """
        ...

    def GetOrders(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.Order]:
        """
        Gets the collection of orders from the orderbook.
        
        :returns: List of orders.
        """
        ...

    def GetOrderHistory(self, OrderId: str) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.Order]:
        """
        Gets information about given OrderId.
        
        :param OrderId: Unique order id
        :returns: List of order objects.
        """
        ...

    def GetOrderTrades(self, OrderId: str = None) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.Trade]:
        """
        Retreive the list of trades executed (all or ones under a particular order).
        An order can be executed in tranches based on market conditions.
        These trades are individually recorded under an order.
        
        :param OrderId: is the ID of the order (optional) whose trades are to be retrieved. If no `OrderId` is specified, all trades for the day are returned.
        :returns: List of trades of given order.
        """
        ...

    def GetPositions(self) -> QuantConnect.Brokerages.Zerodha.Messages.PositionResponse:
        """
        Retrieve the list of positions.
        
        :returns: Day and net positions.
        """
        ...

    def GetHoldings(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.Holding]:
        """
        Retrieve the list of equity holdings.
        
        :returns: List of holdings.
        """
        ...

    def ConvertPosition(self, Exchange: str, TradingSymbol: str, TransactionType: str, PositionType: str, Quantity: typing.Optional[int], OldProduct: str, NewProduct: str) -> System.Collections.Generic.Dictionary[str, typing.Any]:
        """
        Modify an open position's product type.
        
        :param Exchange: Name of the exchange
        :param TradingSymbol: Tradingsymbol of the instrument
        :param TransactionType: BUY or SELL
        :param PositionType: overnight or day
        :param Quantity: Quantity to convert
        :param OldProduct: Existing margin product of the position
        :param NewProduct: Margin product to convert to
        :returns: Json response in the form of nested string dictionary.
        """
        ...

    def GetInstruments(self, Exchange: str = None) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.CsvInstrument]:
        """
        Retrieve the list of market instruments available to trade.
        Note that the results could be large, several hundred KBs in size,
        with tens of thousands of entries in the list.
        
        :param Exchange: Name of the exchange
        :returns: List of instruments.
        """
        ...

    def GetQuote(self, InstrumentIds: typing.List[str]) -> System.Collections.Generic.Dictionary[str, QuantConnect.Brokerages.Zerodha.Messages.Quote]:
        """
        Retrieve quote and market depth of upto 200 instruments
        
        :returns: Dictionary of all Quote objects with keys as in InstrumentId.
        """
        ...

    def GetOHLC(self, InstrumentId: typing.List[str]) -> System.Collections.Generic.Dictionary[str, QuantConnect.Brokerages.Zerodha.Messages.OHLC]:
        """
        Retrieve LTP and OHLC of upto 200 instruments
        
        :param InstrumentId: Indentification of instrument in the form of EXCHANGE:TRADINGSYMBOL (eg: NSE:INFY) or InstrumentToken (eg: 408065)
        :returns: Dictionary of all OHLC objects with keys as in InstrumentId.
        """
        ...

    def GetLTP(self, InstrumentId: typing.List[str]) -> System.Collections.Generic.Dictionary[str, QuantConnect.Brokerages.Zerodha.Messages.LTP]:
        """
        Retrieve LTP of upto 200 instruments
        
        :param InstrumentId: Indentification of instrument in the form of EXCHANGE:TRADINGSYMBOL (eg: NSE:INFY) or InstrumentToken (eg: 408065)
        :returns: Dictionary with InstrumentId as key and LTP as value.
        """
        ...

    def GetHistoricalData(self, InstrumentToken: str, FromDate: datetime.datetime, ToDate: datetime.datetime, Interval: str, Continuous: bool = False, OI: bool = False) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.Historical]:
        """
        Retrieve historical data (candles) for an instrument.
        
        :param InstrumentToken: Identifier for the instrument whose historical records you want to fetch. This is obtained with the instrument list API.
        :param FromDate: Date in format yyyy-MM-dd for fetching candles between two days. Date in format yyyy-MM-dd hh:mm:ss for fetching candles between two timestamps.
        :param ToDate: Date in format yyyy-MM-dd for fetching candles between two days. Date in format yyyy-MM-dd hh:mm:ss for fetching candles between two timestamps.
        :param Interval: The candle record interval. Possible values are: minute, day, 3minute, 5minute, 10minute, 15minute, 30minute, 60minute
        :param Continuous: Pass true to get continous data of expired instruments.
        :param OI: Pass true to get open interest data.
        :returns: List of Historical objects.
        """
        ...

    def GetTriggerRange(self, InstrumentId: typing.List[str], TrasactionType: str) -> System.Collections.Generic.Dictionary[str, QuantConnect.Brokerages.Zerodha.Messages.TrigerRange]:
        """
        Retrieve the buy/sell trigger range for Cover Orders.
        
        :param InstrumentId: Indentification of instrument in the form of EXCHANGE:TRADINGSYMBOL (eg: NSE:INFY) or InstrumentToken (eg: 408065)
        :param TrasactionType: BUY or SELL
        :returns: List of trigger ranges for given instrument ids for given transaction type.
        """
        ...

    def GetGTTs(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.GTT]:
        ...

    def GetGTT(self, GTTId: int) -> QuantConnect.Brokerages.Zerodha.Messages.GTT:
        """
        Retrieve a single GTT
        
        :param GTTId: Id of the GTT
        :returns: GTT info.
        """
        ...

    def PlaceGTT(self, gttParams: QuantConnect.Brokerages.Zerodha.Messages.GTTParams) -> System.Collections.Generic.Dictionary[str, typing.Any]:
        """
        Place a GTT order
        
        :param gttParams: Contains the parameters for the GTT order
        :returns: Json response in the form of nested string dictionary.
        """
        ...

    def ModifyGTT(self, GTTId: int, gttParams: QuantConnect.Brokerages.Zerodha.Messages.GTTParams) -> System.Collections.Generic.Dictionary[str, typing.Any]:
        """
        Modify a GTT order
        
        :param GTTId: Id of the GTT to be modified
        :param gttParams: Contains the parameters for the GTT order
        :returns: Json response in the form of nested string dictionary.
        """
        ...

    def CancelGTT(self, GTTId: int) -> System.Collections.Generic.Dictionary[str, typing.Any]:
        """
        Cancel a GTT order
        
        :param GTTId: Id of the GTT to be modified
        :returns: Json response in the form of nested string dictionary.
        """
        ...


class MessageData(System.Object):
    """Message Data"""

    @property
    def Data(self) -> typing.List[int]:
        ...

    @Data.setter
    def Data(self, value: typing.List[int]):
        ...

    @property
    def MessageType(self) -> typing.Any:
        ...

    @MessageType.setter
    def MessageType(self, value: typing.Any):
        ...

    @property
    def Count(self) -> int:
        ...

    @Count.setter
    def Count(self, value: int):
        ...


class ZerodhaWebSocketClientWrapper(System.Object):
    """This class has no documentation."""

    @property
    def IsOpen(self) -> bool:
        """Wraps IsAlive"""
        ...

    @property
    def Message(self) -> typing.List[System_EventHandler]:
        """Wraps message event"""
        ...

    @Message.setter
    def Message(self, value: typing.List[System_EventHandler]):
        """Wraps message event"""
        ...

    @property
    def Error(self) -> typing.List[System_EventHandler]:
        """Wraps error event"""
        ...

    @Error.setter
    def Error(self, value: typing.List[System_EventHandler]):
        """Wraps error event"""
        ...

    @property
    def Open(self) -> typing.List[System_EventHandler]:
        """Wraps open method"""
        ...

    @Open.setter
    def Open(self, value: typing.List[System_EventHandler]):
        """Wraps open method"""
        ...

    @property
    def Closed(self) -> typing.List[System_EventHandler]:
        """Wraps close method"""
        ...

    @Closed.setter
    def Closed(self, value: typing.List[System_EventHandler]):
        """Wraps close method"""
        ...

    @property
    def ReadyState(self) -> typing.Any:
        """Wraps ReadyState"""
        ...

    def Initialize(self, url: str) -> None:
        """Wraps constructor"""
        ...

    def Send(self, data: str) -> None:
        """Wraps send method"""
        ...

    def Connect(self) -> None:
        """Wraps Connect method"""
        ...

    def Close(self) -> None:
        """Wraps Close method"""
        ...

    def OnMessage(self, e: QuantConnect.Brokerages.Zerodha.MessageData) -> None:
        """
        Event invocator for the Message event
        
        This method is protected.
        """
        ...

    def OnError(self, e: QuantConnect.Brokerages.WebSocketError) -> None:
        """
        Event invocator for the Error event
        
        This method is protected.
        """
        ...

    def OnOpen(self) -> None:
        """
        Event invocator for the Open event
        
        This method is protected.
        """
        ...

    def OnClose(self, e: QuantConnect.Brokerages.WebSocketCloseData) -> None:
        """
        Event invocator for the Close event
        
        This method is protected.
        """
        ...


class ZerodhaBrokerage(QuantConnect.Brokerages.Brokerage, QuantConnect.Interfaces.IDataQueueHandler):
    """Zerodha Brokerage implementation"""

    @property
    def WebSocket(self) -> QuantConnect.Brokerages.Zerodha.ZerodhaWebSocketClientWrapper:
        """
        The websockets client instance
        
        This field is protected.
        """
        ...

    @WebSocket.setter
    def WebSocket(self, value: QuantConnect.Brokerages.Zerodha.ZerodhaWebSocketClientWrapper):
        """
        The websockets client instance
        
        This field is protected.
        """
        ...

    @property
    def JsonSettings(self) -> typing.Any:
        """
        standard json parsing settings
        
        This field is protected.
        """
        ...

    @JsonSettings.setter
    def JsonSettings(self, value: typing.Any):
        """
        standard json parsing settings
        
        This field is protected.
        """
        ...

    @property
    def CachedOrderIDs(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.Order]:
        """A list of currently active orders"""
        ...

    @CachedOrderIDs.setter
    def CachedOrderIDs(self, value: System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.Order]):
        """A list of currently active orders"""
        ...

    @property
    def ChannelList(self) -> System.Collections.Generic.Dictionary[str, QuantConnect.Data.Channel]:
        """
        A list of currently subscribed channels
        
        This field is protected.
        """
        ...

    @ChannelList.setter
    def ChannelList(self, value: System.Collections.Generic.Dictionary[str, QuantConnect.Data.Channel]):
        """
        A list of currently subscribed channels
        
        This field is protected.
        """
        ...

    @property
    def ApiSecret(self) -> str:
        """
        The api secret
        
        This field is protected.
        """
        ...

    @ApiSecret.setter
    def ApiSecret(self, value: str):
        """
        The api secret
        
        This field is protected.
        """
        ...

    @property
    def ApiKey(self) -> str:
        """
        The api key
        
        This field is protected.
        """
        ...

    @ApiKey.setter
    def ApiKey(self, value: str):
        """
        The api key
        
        This field is protected.
        """
        ...

    @property
    def LastHeartbeatUtcTime(self) -> datetime.datetime:
        """
        Timestamp of most recent heartbeat message
        
        This field is protected.
        """
        ...

    @LastHeartbeatUtcTime.setter
    def LastHeartbeatUtcTime(self, value: datetime.datetime):
        """
        Timestamp of most recent heartbeat message
        
        This field is protected.
        """
        ...

    @property
    def AccountBaseCurrency(self) -> str:
        ...

    @AccountBaseCurrency.setter
    def AccountBaseCurrency(self, value: str):
        ...

    @property
    def IsConnected(self) -> bool:
        """Checks if the websocket connection is connected or in the process of connecting"""
        ...

    def __init__(self, tradingSegment: str, zerodhaProductType: str, apiKey: str, apiSecret: str, algorithm: QuantConnect.Interfaces.IAlgorithm, securityProvider: QuantConnect.Securities.ISecurityProvider, aggregator: QuantConnect.Data.IDataAggregator) -> None:
        ...

    @typing.overload
    def Subscribe(self, symbols: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]) -> None:
        """
        Subscribes to the requested symbols (using an individual streaming channel)
        
        :param symbols: The list of symbols to subscribe
        """
        ...

    def GetQuote(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect.Brokerages.Zerodha.Messages.Quote:
        """
        Gets Quote using Zerodha API
        
        :returns: Quote.
        """
        ...

    def LockStream(self) -> None:
        """Lock the streaming processing while we're sending orders as sometimes they fill before the REST call returns."""
        ...

    def UnlockStream(self) -> None:
        """Unlock stream and process all backed up messages."""
        ...

    def Connect(self) -> None:
        """Connects to Zerodha wss"""
        ...

    def Disconnect(self) -> None:
        """Closes the websockets connection"""
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
        :returns: True if the request was submitted for cancellation, false otherwise.
        """
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """Gets all orders not yet closed"""
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """Gets all open positions"""
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """Gets the total account cash balance for specified account type"""
        ...

    def GetHistory(self, request: QuantConnect.Data.HistoryRequest) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Gets the history for the requested security
        
        :param request: The historical data request
        :returns: An enumerable of bars covering the span specified in the request.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        ...

    @typing.overload
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
        UnSubscribe to the specified configuration
        
        :param dataConfig: defines the parameters to subscribe to a data feed
        """
        ...


class ZerodhaBrokerageFactory(QuantConnect.Brokerages.BrokerageFactory):
    """Factory method to create Zerodha Websockets brokerage"""

    @property
    def BrokerageData(self) -> System.Collections.Generic.Dictionary[str, str]:
        """provides brokerage connection data"""
        ...

    def __init__(self) -> None:
        """Factory constructor"""
        ...

    def Dispose(self) -> None:
        """Not required"""
        ...

    def GetBrokerageModel(self, orderProvider: QuantConnect.Securities.IOrderProvider) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        The brokerage model
        
        :param orderProvider: The order provider
        """
        ...

    def CreateBrokerage(self, job: QuantConnect.Packets.LiveNodePacket, algorithm: QuantConnect.Interfaces.IAlgorithm) -> QuantConnect.Interfaces.IBrokerage:
        """Create the Brokerage instance"""
        ...


class ZerodhaSymbolMapper(System.Object, QuantConnect.Brokerages.ISymbolMapper):
    """Provides the mapping between Lean symbols and Zerodha symbols."""

    @property
    def KnownSymbols(self) -> System.Collections.Generic.List[QuantConnect.Symbol]:
        """Symbols that are Tradable"""
        ...

    KnownSymbolsList: System.Collections.Generic.List[QuantConnect.Symbol] = ...
    """The list of known Zerodha symbols."""

    ZerodhaInstrumentsList: System.Collections.Generic.Dictionary[str, int] = ...
    """The list of known Zerodha symbols."""

    def __init__(self, kite: QuantConnect.Brokerages.Zerodha.Kite, exchange: str = ...) -> None:
        """Constructs default instance of the Zerodha Sybol Mapper"""
        ...

    def GetTradableInstrumentsList(self, kite: QuantConnect.Brokerages.Zerodha.Kite, exchange: str = ...) -> System.Collections.Generic.List[QuantConnect.Symbol]:
        """
        Get list of tradable symbol
        
        :param kite: Kite
        :param exchange: Exchange
        """
        ...

    def GetBrokerageSymbol(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """
        Converts a Lean symbol instance to an Zerodha symbol
        
        :param symbol: A Lean symbol instance
        :returns: The Zerodha symbol.
        """
        ...

    @typing.overload
    def GetLeanSymbol(self, brokerageSymbol: str, securityType: QuantConnect.SecurityType, market: str, expirationDate: datetime.datetime = ..., strike: float = 0, optionRight: QuantConnect.OptionRight = ...) -> QuantConnect.Symbol:
        """
        Converts an Zerodha symbol to a Lean symbol instance
        
        :param brokerageSymbol: The Zerodha symbol
        :param securityType: The security type
        :param market: The market
        :param expirationDate: Expiration date of the security(if applicable)
        :param strike: The strike of the security (if applicable)
        :param optionRight: The option right of the security (if applicable)
        :returns: A new Lean Symbol instance.
        """
        ...

    @typing.overload
    def GetLeanSymbol(self, brokerageSymbol: str) -> QuantConnect.Symbol:
        """
        Converts an Zerodha symbol to a Lean symbol instance
        
        :param brokerageSymbol: The Zerodha symbol
        :returns: A new Lean Symbol instance.
        """
        ...

    def GetZerodhaInstrumentToken(self, brokerageSymbol: str, market: str) -> int:
        """
        Converts an Zerodha symbol to a Zerodha Instrument Token instance
        
        :param brokerageSymbol: The Zerodha symbol
        :param market: The trading market
        :returns: A new Lean Symbol instance.
        """
        ...

    @staticmethod
    def IsKnownBrokerageSymbol(brokerageSymbol: str) -> bool:
        ...

    def IsKnownLeanSymbol(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        :param symbol: The Lean symbol
        :returns: True if Zerodha supports the symbol.
        """
        ...

    def ConvertZerodhaSymbolToLeanSymbol(self, ZerodhaSymbol: int) -> QuantConnect.Symbol:
        """Converts an Zerodha symbol to a Lean symbol string"""
        ...


class KiteException(System.Exception):
    """KiteAPI Exceptions"""

    @property
    def status(self) -> System.Net.HttpStatusCode:
        ...

    @status.setter
    def status(self, value: System.Net.HttpStatusCode):
        ...

    def __init__(self, message: str, httpStatus: System.Net.HttpStatusCode, innerException: System.Exception = None) -> None:
        ...


class GeneralException(QuantConnect.Brokerages.Zerodha.KiteException):
    """General Exceptions"""

    def __init__(self, message: str, httpStatus: System.Net.HttpStatusCode = ..., innerException: System.Exception = None) -> None:
        ...


class TokenException(QuantConnect.Brokerages.Zerodha.KiteException):
    """Token Exceptions"""

    def __init__(self, message: str, httpStatus: System.Net.HttpStatusCode = ..., innerException: System.Exception = None) -> None:
        ...


class PermissionException(QuantConnect.Brokerages.Zerodha.KiteException):
    """Permission Exceptions"""

    def __init__(self, message: str, httpStatus: System.Net.HttpStatusCode = ..., innerException: System.Exception = None) -> None:
        ...


class OrderException(QuantConnect.Brokerages.Zerodha.KiteException):
    """Order Exceptions"""

    def __init__(self, message: str, httpStatus: System.Net.HttpStatusCode = ..., innerException: System.Exception = None) -> None:
        ...


class InputException(QuantConnect.Brokerages.Zerodha.KiteException):
    """InputExceptions"""

    def __init__(self, message: str, httpStatus: System.Net.HttpStatusCode = ..., innerException: System.Exception = None) -> None:
        ...


class DataException(QuantConnect.Brokerages.Zerodha.KiteException):
    """DataExceptions"""

    def __init__(self, message: str, httpStatus: System.Net.HttpStatusCode = ..., innerException: System.Exception = None) -> None:
        ...


class NetworkException(QuantConnect.Brokerages.Zerodha.KiteException):
    """Network Exceptions"""

    def __init__(self, message: str, httpStatus: System.Net.HttpStatusCode = ..., innerException: System.Exception = None) -> None:
        ...


class KiteProductType(System.Enum):
    """Types of product supported by Kite"""

    MIS = 0

    CNC = 1

    NRML = 2


class KiteOrderType(System.Enum):
    """Types of order supported by Kite"""

    MARKET = 0

    LIMIT = 1

    SLM = 2

    SL = 3


class Constants(System.Object):
    """This class has no documentation."""

    PRODUCT_MIS: str = "MIS"

    PRODUCT_CNC: str = "CNC"

    PRODUCT_NRML: str = "NRML"

    ORDER_TYPE_MARKET: str = "MARKET"

    ORDER_TYPE_LIMIT: str = "LIMIT"

    ORDER_TYPE_SLM: str = "SL-M"

    ORDER_TYPE_SL: str = "SL"

    ORDER_STATUS_COMPLETE: str = "COMPLETE"

    ORDER_STATUS_CANCELLED: str = "CANCELLED"

    ORDER_STATUS_REJECTED: str = "REJECTED"

    VARIETY_REGULAR: str = "regular"

    VARIETY_BO: str = "bo"

    VARIETY_CO: str = "co"

    VARIETY_AMO: str = "amo"

    TRANSACTION_TYPE_BUY: str = "BUY"

    TRANSACTION_TYPE_SELL: str = "SELL"

    VALIDITY_DAY: str = "DAY"

    VALIDITY_IOC: str = "IOC"

    EXCHANGE_NSE: str = "NSE"

    EXCHANGE_BSE: str = "BSE"

    EXCHANGE_NFO: str = "NFO"

    EXCHANGE_CDS: str = "CDS"

    EXCHANGE_BFO: str = "BFO"

    EXCHANGE_MCX: str = "MCX"

    MARGIN_EQUITY: str = "equity"

    MARGIN_COMMODITY: str = "commodity"

    MODE_FULL: str = "full"

    MODE_QUOTE: str = "quote"

    MODE_LTP: str = "ltp"

    POSITION_DAY: str = "day"

    POSITION_OVERNIGHT: str = "overnight"

    INTERVAL_MINUTE: str = "minute"

    INTERVAL_3MINUTE: str = "3minute"

    INTERVAL_5MINUTE: str = "5minute"

    INTERVAL_10MINUTE: str = "10minute"

    INTERVAL_15MINUTE: str = "15minute"

    INTERVAL_30MINUTE: str = "30minute"

    INTERVAL_60MINUTE: str = "60minute"

    INTERVAL_DAY: str = "day"

    GTT_ACTIVE: str = "active"

    GTT_TRIGGERED: str = "triggered"

    GTT_DISABLED: str = "disabled"

    GTT_EXPIRED: str = "expired"

    GTT_CANCELLED: str = "cancelled"

    GTT_REJECTED: str = "rejected"

    GTT_DELETED: str = "deleted"

    GTT_TRIGGER_OCO: str = "two-leg"

    GTT_TRIGGER_SINGLE: str = "single"


class ZerodhaWebSocketWrapper(QuantConnect.Brokerages.Zerodha.ZerodhaWebSocketClientWrapper):
    """Wrapper class for a Zerodha websocket connection"""

    @property
    def ConnectionId(self) -> str:
        """The unique Id for the connection"""
        ...

    @property
    def ConnectionHandler(self) -> QuantConnect.Brokerages.IConnectionHandler:
        """The handler for the connection"""
        ...

    def __init__(self, connectionHandler: QuantConnect.Brokerages.IConnectionHandler) -> None:
        """Initializes a new instance of the ZerodhaWebSocketWrapper class."""
        ...


class Utils(System.Object):
    """This class has no documentation."""

    @staticmethod
    def StringToDate(dateString: str) -> typing.Optional[datetime.datetime]:
        """
        Convert string to Date object
        
        :param dateString: Date string.
        :returns: Date object/.
        """
        ...

    @staticmethod
    def JsonSerialize(obj: typing.Any) -> str:
        """
        Serialize C# object to JSON string.
        
        :param obj: C# object to serialize.
        :returns: JSON string/.
        """
        ...

    @staticmethod
    def JsonDeserialize(Json: str) -> typing.Any:
        """
        Deserialize Json string to nested string dictionary.
        
        :param Json: Json string to deserialize.
        :returns: Json in the form of nested string dictionary.
        """
        ...

    @staticmethod
    def DoubleToDecimal(obj: typing.Any) -> typing.Any:
        """
        Recursively traverses an object and converts double fields to decimal.
        This is used in Json deserialization. JavaScriptSerializer converts floats
        in exponential notation to double and everthing else to double. This function
        makes everything decimal. Currently supports only Dictionary and Array as input.
        
        :param obj: Input object.
        :returns: Object with decimals instead of doubles.
        """
        ...

    @staticmethod
    def StreamFromString(value: str) -> System.IO.MemoryStream:
        """
        Wraps a string inside a stream
        
        :param value: string data
        :returns: Stream that reads input string.
        """
        ...

    @staticmethod
    def AddIfNotNull(Params: System.Collections.Generic.Dictionary[str, typing.Any], Key: str, Value: str) -> None:
        """
        Helper function to add parameter to the request only if it is not null or empty
        
        :param Params: Dictionary to add the key-value pair
        :param Key: Key of the parameter
        :param Value: Value of the parameter
        """
        ...

    @staticmethod
    def BuildParam(Key: str, Value: typing.Any) -> str:
        """
        Creates key=value with url encoded value
        
        :param Key: Key
        :param Value: Value
        :returns: Combined string.
        """
        ...

    @staticmethod
    def UnixToDateTime(unixTimeStamp: int) -> datetime.datetime:
        ...

    @staticmethod
    def ToDecimalList(arrayList: System.Collections.ArrayList) -> System.Collections.Generic.List[float]:
        ...


