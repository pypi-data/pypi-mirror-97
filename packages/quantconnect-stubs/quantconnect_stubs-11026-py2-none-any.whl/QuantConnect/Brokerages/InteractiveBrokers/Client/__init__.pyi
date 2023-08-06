import abc
import datetime
import typing

import QuantConnect.Brokerages.InteractiveBrokers.Client
import System

FamilyCode = typing.Any
DefaultEWrapper = typing.Any
System_EventHandler = typing.Any


class ManagedAccountsEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.ManagedAccounts event"""

    @property
    def AccountList(self) -> str:
        """A comma-separated string with the managed account ids."""
        ...

    def __init__(self, accountList: str) -> None:
        """Initializes a new instance of the ManagedAccountsEventArgs class"""
        ...


class NextValidIdEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.NextValidId event"""

    @property
    def OrderId(self) -> int:
        """The next available order ID received from TWS upon connection. Increment all successive orders by one based on this Id."""
        ...

    def __init__(self, orderId: int) -> None:
        """Initializes a new instance of the NextValidIdEventArgs class"""
        ...


class ReceiveFaEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.ReceiveFa event"""

    @property
    def FaDataType(self) -> int:
        """Specifies the type of Financial Advisor configuration data being received from TWS."""
        ...

    @property
    def FaXmlData(self) -> str:
        """The XML string containing the previously requested FA configuration information."""
        ...

    def __init__(self, faDataType: int, faXmlData: str) -> None:
        """Initializes a new instance of the ReceiveFaEventArgs class"""
        ...


class AccountDownloadEndEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.AccountDownloadEnd event"""

    @property
    def Account(self) -> str:
        """The account ID."""
        ...

    def __init__(self, account: str) -> None:
        """Initializes a new instance of the AccountDownloadEndEventArgs class"""
        ...


class ContractDetailsEventArgs(System.EventArgs):
    """
    Event arguments class for the following events:
    InteractiveBrokersClient.ContractDetailsInteractiveBrokersClient.BondContractDetails
    """

    @property
    def RequestId(self) -> int:
        """The ID of the data request. Ensures that responses are matched to requests if several requests are in process."""
        ...

    @property
    def ContractDetails(self) -> typing.Any:
        """This structure contains a full description of the contract being looked up."""
        ...

    def __init__(self, requestId: int, contractDetails: typing.Any) -> None:
        """Initializes a new instance of the ContractDetailsEventArgs class"""
        ...


class TickEventArgs(System.EventArgs, metaclass=abc.ABCMeta):
    """Base event arguments class for Tick events"""

    @property
    def TickerId(self) -> int:
        """The request's unique identifier."""
        ...

    @property
    def Field(self) -> int:
        """Specifies the type of data being received."""
        ...

    def __init__(self, tickerId: int, field: int) -> None:
        """
        Initializes a new instance of the TickEventArgs class
        
        This method is protected.
        """
        ...


class TickSizeEventArgs(QuantConnect.Brokerages.InteractiveBrokers.Client.TickEventArgs):
    """Event arguments class for the InteractiveBrokersClient.TickSize event"""

    @property
    def Size(self) -> int:
        """The actual size."""
        ...

    def __init__(self, tickerId: int, field: int, size: int) -> None:
        """Initializes a new instance of the TickSizeEventArgs class"""
        ...


class OrderStatusEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.OrderStatus event"""

    @property
    def OrderId(self) -> int:
        """The order Id that was specified previously in the call to placeOrder()"""
        ...

    @property
    def Status(self) -> str:
        """The order status."""
        ...

    @property
    def Filled(self) -> int:
        """Specifies the number of shares that have been executed."""
        ...

    @property
    def Remaining(self) -> int:
        """Specifies the number of shares still outstanding."""
        ...

    @property
    def AverageFillPrice(self) -> float:
        """
        The average price of the shares that have been executed.
        This parameter is valid only if the filled parameter value is greater than zero.
        Otherwise, the price parameter will be zero.
        """
        ...

    @property
    def PermId(self) -> int:
        """The TWS id used to identify orders. Remains the same over TWS sessions."""
        ...

    @property
    def ParentId(self) -> int:
        """The order ID of the parent order, used for bracket and auto trailing stop orders."""
        ...

    @property
    def LastFillPrice(self) -> float:
        """
        The last price of the shares that have been executed.
        This parameter is valid only if the filled parameter value is greater than zero.
        Otherwise, the price parameter will be zero.
        """
        ...

    @property
    def ClientId(self) -> int:
        """
        The ID of the client (or TWS) that placed the order.
        Note that TWS orders have a fixed clientId and orderId of 0 that distinguishes them from API orders.
        """
        ...

    @property
    def WhyHeld(self) -> str:
        """
        This field is used to identify an order held when TWS is trying to locate shares for a short sell.
        The value used to indicate this is 'locate'.
        """
        ...

    @property
    def MktCapPrice(self) -> float:
        """
        If an order has been capped, this indicates the current capped price.
        Requires TWS 967+ and API v973.04+. Python API specifically requires API v973.06+.
        """
        ...

    def __init__(self, orderId: int, status: str, filled: int, remaining: int, averageFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float) -> None:
        """Initializes a new instance of the OrderStatusEventArgs class"""
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class OpenOrderEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.OpenOrder event"""

    @property
    def OrderId(self) -> int:
        """The order Id assigned by TWS. Used to cancel or update the order."""
        ...

    @property
    def Contract(self) -> typing.Any:
        """The Contract class attributes describe the contract."""
        ...

    @property
    def Order(self) -> typing.Any:
        """The Order class attributes define the details of the order."""
        ...

    @property
    def OrderState(self) -> typing.Any:
        """The orderState attributes include margin and commissions fields for both pre and post trade data."""
        ...

    def __init__(self, orderId: int, contract: typing.Any, order: typing.Any, orderState: typing.Any) -> None:
        """Initializes a new instance of the OpenOrderEventArgs class"""
        ...

    def ToString(self) -> str:
        """Returns a string that represents the current object."""
        ...


class AgentDescription(System.Object):
    """Used for Rule 80A describes the type of trader."""

    Individual: str = "I"
    """An individual"""

    Agency: str = "A"
    """An Agency"""

    AgentOtherMember: str = "W"
    """An Agent or Other Member"""

    IndividualPtia: str = "J"
    """Individual PTIA"""

    AgencyPtia: str = "U"
    """Agency PTIA"""

    AgentOtherMemberPtia: str = "M"
    """Agether or Other Member PTIA"""

    IndividualPt: str = "K"
    """Individual PT"""

    AgencyPt: str = "Y"
    """Agency PT"""

    AgentOtherMemberPt: str = "N"
    """Agent Other Member PT"""

    # Cannot convert to Python: None: str = ...
    """No Description Provided"""


class ErrorEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.Error event"""

    @property
    def Id(self) -> int:
        """The request identifier that generated the error."""
        ...

    @property
    def Code(self) -> int:
        """The code identifying the error."""
        ...

    @property
    def Message(self) -> str:
        """The description of the error."""
        ...

    def __init__(self, id: int, code: int, message: str) -> None:
        """Initializes a new instance of the ErrorEventArgs class"""
        ...


class CurrentTimeUtcEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.CurrentTimeUtc event"""

    @property
    def CurrentTimeUtc(self) -> datetime.datetime:
        """The current system time on the IB server."""
        ...

    def __init__(self, currentTimeUtc: datetime.datetime) -> None:
        """Initializes a new instance of the CurrentTimeUtcEventArgs class"""
        ...


class TickPriceEventArgs(QuantConnect.Brokerages.InteractiveBrokers.Client.TickEventArgs):
    """Event arguments class for the InteractiveBrokersClient.TickPrice event"""

    @property
    def Price(self) -> float:
        """The actual price."""
        ...

    @property
    def TickAttributes(self) -> typing.Any:
        """The tick attributes."""
        ...

    def __init__(self, tickerId: int, field: int, price: float, attribs: typing.Any) -> None:
        """Initializes a new instance of the TickPriceEventArgs class"""
        ...


class HistoricalDataEndEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.HistoricalDataEnd event"""

    @property
    def RequestId(self) -> int:
        """The request's identifier."""
        ...

    @property
    def Start(self) -> str:
        """"""
        ...

    @property
    def End(self) -> str:
        """"""
        ...

    def __init__(self, requestId: int, start: str, end: str) -> None:
        """Initializes a new instance of the HistoricalDataEndEventArgs class"""
        ...


class ExecutionDetailsEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.ExecutionDetails event"""

    @property
    def RequestId(self) -> int:
        """The request's identifier."""
        ...

    @property
    def Contract(self) -> typing.Any:
        """This structure contains a full description of the contract that was executed."""
        ...

    @property
    def Execution(self) -> typing.Any:
        """This structure contains addition order execution details."""
        ...

    def __init__(self, requestId: int, contract: typing.Any, execution: typing.Any) -> None:
        """Initializes a new instance of the ExecutionDetailsEventArgs class"""
        ...

    def ToString(self) -> str:
        """Returns a string that represents the current object."""
        ...


class ActionSide(System.Object):
    """Order Action Side. Specifies whether securities should be bought or sold."""

    Buy: str = "BUY"
    """Security is to be bought."""

    Sell: str = "SELL"
    """Security is to be sold."""

    Undefined: str = ...
    """Undefined"""

    SShort: str = "SSHORT"
    """Sell Short as part of a combo leg"""

    SShortX: str = "SSHORTX"
    """
    Short Sale Exempt action.
    SSHORTX allows some orders to be marked as exempt from the new SEC Rule 201
    """


class BarSize(System.Object):
    """Historical Bar Size Requests"""

    OneSecond: str = "1 secs"
    """1 second bars"""

    FiveSeconds: str = "5 secs"
    """5 second bars"""

    FifteenSeconds: str = "15 secs"
    """15 second bars"""

    ThirtySeconds: str = "30 secs"
    """30 second bars"""

    OneMinute: str = "1 min"
    """1 minute bars"""

    TwoMinutes: str = "2 mins"
    """2 minute bars"""

    FiveMinutes: str = "5 mins"
    """5 minute bars"""

    FifteenMinutes: str = "15 mins"
    """15 minute bars"""

    ThirtyMinutes: str = "30 mins"
    """30 minute bars"""

    OneHour: str = "1 hour"
    """1 hour bars"""

    OneDay: str = "1 day"
    """1 day bars"""

    OneWeek: str = "1 week"
    """1 week bars"""

    OneMonth: str = "1 month"
    """1 month bars"""

    OneYear: str = "1 year"
    """1 year bars"""


class UpdatePortfolioEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.UpdatePortfolio event"""

    @property
    def Contract(self) -> typing.Any:
        """
        This structure contains a description of the contract which is being traded.
        The exchange field in a contract is not set for portfolio update.
        """
        ...

    @property
    def Position(self) -> int:
        """
        The number of positions held.
        If the position is 0, it means the position has just cleared.
        """
        ...

    @property
    def MarketPrice(self) -> float:
        """The unit price of the instrument."""
        ...

    @property
    def MarketValue(self) -> float:
        """The total market value of the instrument."""
        ...

    @property
    def AverageCost(self) -> float:
        """The average cost per share is calculated by dividing your cost (execution price + commission) by the quantity of your position."""
        ...

    @property
    def UnrealisedPnl(self) -> float:
        """The difference between the current market value of your open positions and the average cost, or Value - Average Cost."""
        ...

    @property
    def RealisedPnl(self) -> float:
        """Shows your profit on closed positions, which is the difference between your entry execution cost (execution price + commissions to open the position) and exit execution cost ((execution price + commissions to close the position)"""
        ...

    @property
    def AccountName(self) -> str:
        """The name of the account to which the message applies.  Useful for Financial Advisor sub-account messages."""
        ...

    def __init__(self, contract: typing.Any, position: int, marketPrice: float, marketValue: float, averageCost: float, unrealisedPnl: float, realisedPnl: float, accountName: str) -> None:
        """Initializes a new instance of the UpdatePortfolioEventArgs class"""
        ...


class SecurityType(System.Object):
    """Contract Security Types"""

    Stock: str = "STK"
    """Stock"""

    Option: str = "OPT"
    """Option"""

    Future: str = "FUT"
    """Future"""

    Index: str = "IND"
    """Index"""

    FutureOption: str = "FOP"
    """FOP = options on futures"""

    Cash: str = "CASH"
    """Cash"""

    Bag: str = "BAG"
    """For Combination Orders - must use combo leg details"""

    Bond: str = "BOND"
    """Bond"""

    Warrant: str = "WAR"
    """Warrant"""

    Commodity: str = "CMDTY"
    """Commodity"""

    Bill: str = "BILL"
    """Bill"""

    ContractForDifference: str = "CFD"
    """Contract For Difference"""

    Undefined: str = ...
    """Undefined Security Type"""


class RightType(System.Object):
    """Option Right Type (Put or Call)"""

    Put: str = "P"
    """Option type is a Put (Right to sell)"""

    Call: str = "C"
    """Option type is a Call (Right to buy)"""

    Undefined: str = ...
    """Option type is not defined (contract is not an option)."""


class TimeInForce(System.Object):
    """Order Time in Force Values"""

    Day: str = "DAY"
    """Day"""

    GoodTillCancel: str = "GTC"
    """Good Till Cancel"""

    ImmediateOrCancel: str = "IOC"
    """You can set the time in force for MARKET or LIMIT orders as IOC. This dictates that any portion of the order not executed immediately after it becomes available on the market will be cancelled."""

    FillOrKill: str = "FOK"
    """Setting FOK as the time in force dictates that the entire order must execute immediately or be canceled."""

    GoodTillDate: str = "GTD"
    """Good Till Date"""

    MarketOnOpen: str = "OPG"
    """Market On Open"""

    Undefined: str = ...
    """Undefined"""


class RequestEndEventArgs(System.EventArgs):
    """
    Event arguments class for the following events:
    InteractiveBrokersClient.AccountSummaryEndInteractiveBrokersClient.ContractDetailsEndInteractiveBrokersClient.ExecutionDetailsEnd
    """

    @property
    def RequestId(self) -> int:
        """The request's identifier."""
        ...

    def __init__(self, requestId: int) -> None:
        """Initializes a new instance of the RequestEndEventArgs class"""
        ...


class AccountSummaryEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.AccountSummary event"""

    @property
    def RequestId(self) -> int:
        """The request's identifier."""
        ...

    @property
    def Account(self) -> str:
        """The account id."""
        ...

    @property
    def Tag(self) -> str:
        """The account's attribute being received."""
        ...

    @property
    def Value(self) -> str:
        """The account's attribute's value."""
        ...

    @property
    def Currency(self) -> str:
        """The currency on which the value is expressed."""
        ...

    def __init__(self, reqId: int, account: str, tag: str, value: str, currency: str) -> None:
        """Initializes a new instance of the AccountSummaryEventArgs class"""
        ...


class OrderStatus(System.Object):
    """Order Status constants."""

    PendingSubmit: str = "PendingSubmit"
    """
    indicates that you have transmitted the order, but have not yet received
    confirmation that it has been accepted by the order destination.
    This order status is not sent by TWS and should be explicitly set by the API developer when an order is submitted.
    """

    PendingCancel: str = "PendingCancel"
    """
    PendingCancel - indicates that you have sent a request to cancel the order
    but have not yet received cancel confirmation from the order destination.
    At this point, your order is not confirmed canceled. You may still receive
    an execution while your cancellation request is pending.
    This order status is not sent by TWS and should be explicitly set by the API developer when an order is canceled.
    """

    PreSubmitted: str = "PreSubmitted"
    """
    indicates that a simulated order type has been accepted by the IB system and
    that this order has yet to be elected. The order is held in the IB system
    (and the status remains DARK BLUE) until the election criteria are met.
    At that time the order is transmitted to the order destination as specified
    (and the order status color will change).
    """

    Submitted: str = "Submitted"
    """indicates that your order has been accepted at the order destination and is working."""

    Cancelled: str = "Cancelled"
    """
    indicates that the balance of your order has been confirmed canceled by the IB system.
    This could occur unexpectedly when IB or the destination has rejected your order.
    """

    Filled: str = "Filled"
    """The order has been completely filled."""

    Inactive: str = "Inactive"
    """The Order is inactive"""

    PartiallyFilled: str = "PartiallyFilled"
    """The order is Partially Filled"""

    ApiPending: str = "ApiPending"
    """Api Pending"""

    ApiCancelled: str = "ApiCancelled"
    """Api Cancelled"""

    Error: str = "Error"
    """
    Indicates that there is an error with this order
    This order status is not sent by TWS and should be explicitly set by the API developer when an error has occured.
    """

    # Cannot convert to Python: None: str = ...
    """No Order Status"""


class UpdateAccountValueEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.UpdateAccountValue event"""

    @property
    def Key(self) -> str:
        """A string that indicates one type of account value."""
        ...

    @property
    def Value(self) -> str:
        """The value associated with the key."""
        ...

    @property
    def Currency(self) -> str:
        """Defines the currency type, in case the value is a currency type."""
        ...

    @property
    def AccountName(self) -> str:
        """The account. Useful for Financial Advisor sub-account messages."""
        ...

    def __init__(self, key: str, value: str, currency: str, accountName: str) -> None:
        """Initializes a new instance of the UpdateAccountValueEventArgs class"""
        ...


class FamilyCodesEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.FamilyCodes event"""

    @property
    def FamilyCodes(self) -> typing.List[FamilyCode]:
        """A comma-separated string with the managed account ids."""
        ...

    def __init__(self, familyCodes: typing.List[FamilyCode]) -> None:
        """Initializes a new instance of the FamilyCodesEventArgs class"""
        ...


class CommissionReportEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.CommissionReport event"""

    @property
    def CommissionReport(self) -> typing.Any:
        """The structure that contains commission details."""
        ...

    def __init__(self, commissionReport: typing.Any) -> None:
        """Initializes a new instance of the CommissionReportEventArgs class"""
        ...

    def ToString(self) -> str:
        """Returns a string that represents the current object."""
        ...


class HistoricalDataEventArgs(System.EventArgs):
    """Event arguments class for the InteractiveBrokersClient.HistoricalData event"""

    @property
    def RequestId(self) -> int:
        """The request's identifier."""
        ...

    @property
    def Bar(self) -> typing.Any:
        """The bar data."""
        ...

    def __init__(self, requestId: int, bar: typing.Any) -> None:
        """Initializes a new instance of the HistoricalDataEventArgs class"""
        ...


class InteractiveBrokersClient(DefaultEWrapper, System.IDisposable):
    """Event based implementation of Interactive Brokers EWrapper interface"""

    @property
    def Error(self) -> typing.List[System_EventHandler]:
        ...

    @Error.setter
    def Error(self, value: typing.List[System_EventHandler]):
        ...

    @property
    def CurrentTimeUtc(self) -> typing.List[System_EventHandler]:
        """CurrentTimeUtc event handler"""
        ...

    @CurrentTimeUtc.setter
    def CurrentTimeUtc(self, value: typing.List[System_EventHandler]):
        """CurrentTimeUtc event handler"""
        ...

    @property
    def TickPrice(self) -> typing.List[System_EventHandler]:
        """TickPrice event handler"""
        ...

    @TickPrice.setter
    def TickPrice(self, value: typing.List[System_EventHandler]):
        """TickPrice event handler"""
        ...

    @property
    def TickSize(self) -> typing.List[System_EventHandler]:
        """TickSize event handler"""
        ...

    @TickSize.setter
    def TickSize(self, value: typing.List[System_EventHandler]):
        """TickSize event handler"""
        ...

    @property
    def NextValidId(self) -> typing.List[System_EventHandler]:
        """NextValidId event handler"""
        ...

    @NextValidId.setter
    def NextValidId(self, value: typing.List[System_EventHandler]):
        """NextValidId event handler"""
        ...

    @property
    def ConnectionClosed(self) -> typing.List[System_EventHandler]:
        """ConnectionClosed event handler"""
        ...

    @ConnectionClosed.setter
    def ConnectionClosed(self, value: typing.List[System_EventHandler]):
        """ConnectionClosed event handler"""
        ...

    @property
    def AccountSummary(self) -> typing.List[System_EventHandler]:
        """AccountSummary event handler"""
        ...

    @AccountSummary.setter
    def AccountSummary(self, value: typing.List[System_EventHandler]):
        """AccountSummary event handler"""
        ...

    @property
    def AccountSummaryEnd(self) -> typing.List[System_EventHandler]:
        """AccountSummaryEnd event handler"""
        ...

    @AccountSummaryEnd.setter
    def AccountSummaryEnd(self, value: typing.List[System_EventHandler]):
        """AccountSummaryEnd event handler"""
        ...

    @property
    def BondContractDetails(self) -> typing.List[System_EventHandler]:
        """BondContractDetails event handler"""
        ...

    @BondContractDetails.setter
    def BondContractDetails(self, value: typing.List[System_EventHandler]):
        """BondContractDetails event handler"""
        ...

    @property
    def UpdateAccountValue(self) -> typing.List[System_EventHandler]:
        """UpdateAccountValue event handler"""
        ...

    @UpdateAccountValue.setter
    def UpdateAccountValue(self, value: typing.List[System_EventHandler]):
        """UpdateAccountValue event handler"""
        ...

    @property
    def UpdatePortfolio(self) -> typing.List[System_EventHandler]:
        """UpdatePortfolio event handler"""
        ...

    @UpdatePortfolio.setter
    def UpdatePortfolio(self, value: typing.List[System_EventHandler]):
        """UpdatePortfolio event handler"""
        ...

    @property
    def AccountDownloadEnd(self) -> typing.List[System_EventHandler]:
        """AccountDownloadEnd event handler"""
        ...

    @AccountDownloadEnd.setter
    def AccountDownloadEnd(self, value: typing.List[System_EventHandler]):
        """AccountDownloadEnd event handler"""
        ...

    @property
    def OrderStatus(self) -> typing.List[System_EventHandler]:
        """OrderStatus event handler"""
        ...

    @OrderStatus.setter
    def OrderStatus(self, value: typing.List[System_EventHandler]):
        """OrderStatus event handler"""
        ...

    @property
    def OpenOrder(self) -> typing.List[System_EventHandler]:
        """OpenOrder event handler"""
        ...

    @OpenOrder.setter
    def OpenOrder(self, value: typing.List[System_EventHandler]):
        """OpenOrder event handler"""
        ...

    @property
    def OpenOrderEnd(self) -> typing.List[System_EventHandler]:
        """OpenOrderEnd event handler"""
        ...

    @OpenOrderEnd.setter
    def OpenOrderEnd(self, value: typing.List[System_EventHandler]):
        """OpenOrderEnd event handler"""
        ...

    @property
    def ContractDetails(self) -> typing.List[System_EventHandler]:
        """ContractDetails event handler"""
        ...

    @ContractDetails.setter
    def ContractDetails(self, value: typing.List[System_EventHandler]):
        """ContractDetails event handler"""
        ...

    @property
    def ContractDetailsEnd(self) -> typing.List[System_EventHandler]:
        """ContractDetailsEnd event handler"""
        ...

    @ContractDetailsEnd.setter
    def ContractDetailsEnd(self, value: typing.List[System_EventHandler]):
        """ContractDetailsEnd event handler"""
        ...

    @property
    def ExecutionDetails(self) -> typing.List[System_EventHandler]:
        """ExecutionDetails event handler"""
        ...

    @ExecutionDetails.setter
    def ExecutionDetails(self, value: typing.List[System_EventHandler]):
        """ExecutionDetails event handler"""
        ...

    @property
    def ExecutionDetailsEnd(self) -> typing.List[System_EventHandler]:
        """ExecutionDetailsEnd event handler"""
        ...

    @ExecutionDetailsEnd.setter
    def ExecutionDetailsEnd(self, value: typing.List[System_EventHandler]):
        """ExecutionDetailsEnd event handler"""
        ...

    @property
    def CommissionReport(self) -> typing.List[System_EventHandler]:
        """CommissionReport event handler"""
        ...

    @CommissionReport.setter
    def CommissionReport(self, value: typing.List[System_EventHandler]):
        """CommissionReport event handler"""
        ...

    @property
    def HistoricalData(self) -> typing.List[System_EventHandler]:
        """HistoricalData event handler"""
        ...

    @HistoricalData.setter
    def HistoricalData(self, value: typing.List[System_EventHandler]):
        """HistoricalData event handler"""
        ...

    @property
    def HistoricalDataEnd(self) -> typing.List[System_EventHandler]:
        """HistoricalDataEnd event handler"""
        ...

    @HistoricalDataEnd.setter
    def HistoricalDataEnd(self, value: typing.List[System_EventHandler]):
        """HistoricalDataEnd event handler"""
        ...

    @property
    def PositionEnd(self) -> typing.List[System_EventHandler]:
        """PositionEnd event handler"""
        ...

    @PositionEnd.setter
    def PositionEnd(self, value: typing.List[System_EventHandler]):
        """PositionEnd event handler"""
        ...

    @property
    def ReceiveFa(self) -> typing.List[System_EventHandler]:
        """ReceiveFa event handler"""
        ...

    @ReceiveFa.setter
    def ReceiveFa(self, value: typing.List[System_EventHandler]):
        """ReceiveFa event handler"""
        ...

    @property
    def ConnectAck(self) -> typing.List[System_EventHandler]:
        """ConnectAck event handler"""
        ...

    @ConnectAck.setter
    def ConnectAck(self, value: typing.List[System_EventHandler]):
        """ConnectAck event handler"""
        ...

    @property
    def ManagedAccounts(self) -> typing.List[System_EventHandler]:
        """ManagedAccounts event handler"""
        ...

    @ManagedAccounts.setter
    def ManagedAccounts(self, value: typing.List[System_EventHandler]):
        """ManagedAccounts event handler"""
        ...

    @property
    def FamilyCodes(self) -> typing.List[System_EventHandler]:
        """FamilyCodes event handler"""
        ...

    @FamilyCodes.setter
    def FamilyCodes(self, value: typing.List[System_EventHandler]):
        """FamilyCodes event handler"""
        ...

    @property
    def Connected(self) -> bool:
        ...

    @property
    def ClientSocket(self) -> typing.Any:
        """Gets the instance of EClientSocket to access IB API methods"""
        ...

    def __init__(self, signal: typing.Any) -> None:
        """Initializes a new instance of the InteractiveBrokersClient class"""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    @typing.overload
    def error(self, e: System.Exception) -> None:
        ...

    @typing.overload
    def error(self, str: str) -> None:
        """
        This method is called when TWS wants to send an error message to the client. (V1).
        
        :param str: This is the text of the error message.
        """
        ...

    @typing.overload
    def error(self, id: int, errorCode: int, errorMsg: str) -> None:
        """
        This method is called when there is an error with the communication or when TWS wants to send a message to the client.
        
        :param id: The request identifier that generated the error.
        :param errorCode: The code identifying the error.
        :param errorMsg: The description of the error.
        """
        ...

    def currentTime(self, time: int) -> None:
        """
        This method receives the current system time on IB's server as a result of calling reqCurrentTime().
        
        :param time: The current system time on the IB server.
        """
        ...

    def tickPrice(self, tickerId: int, field: int, price: float, attribs: typing.Any) -> None:
        """
        Market data tick price callback, handles all price-related ticks.
        
        :param tickerId: The request's unique identifier.
        :param field: Specifies the type of price.
        :param price: The actual price.
        :param attribs: Tick attributes.
        """
        ...

    def tickSize(self, tickerId: int, field: int, size: int) -> None:
        """
        Market data tick size callback, handles all size-related ticks.
        
        :param tickerId: The request's unique identifier.
        :param field: The type of size being received.
        :param size: The actual size.
        """
        ...

    def nextValidId(self, orderId: int) -> None:
        """
        Receives the next valid Order ID.
        
        :param orderId: The next available order ID received from TWS upon connection. Increment all successive orders by one based on this Id.
        """
        ...

    def connectionClosed(self) -> None:
        """This method is called when TWS closes the sockets connection, or when TWS is shut down."""
        ...

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str) -> None:
        """
        Receives the account information.
        
        :param reqId: The request's identifier.
        :param account: The account id
        :param tag: The account's attribute being received.
        :param value: The account's attribute's value.
        :param currency: The currency on which the value is expressed.
        """
        ...

    def accountSummaryEnd(self, reqId: int) -> None:
        """
        This is called once all account information for a given reqAccountSummary() request are received.
        
        :param reqId: The request's identifier.
        """
        ...

    def bondContractDetails(self, reqId: int, contract: typing.Any) -> None:
        """
        Sends bond contract data when the reqContractDetails() method has been called for bonds.
        
        :param reqId: The ID of the data request.
        :param contract: This structure contains a full description of the bond contract being looked up.
        """
        ...

    def updateAccountValue(self, key: str, value: str, currency: str, accountName: str) -> None:
        """
        This callback receives the subscribed account's information in response to reqAccountUpdates().
        You can only subscribe to one account at a time.
        
        :param key: A string that indicates one type of account value.
        :param value: The value associated with the key.
        :param currency: Defines the currency type, in case the value is a currency type.
        :param accountName: The account. Useful for Financial Advisor sub-account messages.
        """
        ...

    def updatePortfolio(self, contract: typing.Any, position: float, marketPrice: float, marketValue: float, averageCost: float, unrealisedPnl: float, realisedPnl: float, accountName: str) -> None:
        """
        Receives the subscribed account's portfolio in response to reqAccountUpdates().
        If you want to receive the portfolios of all managed accounts, use reqPositions().
        
        :param contract: This structure contains a description of the contract which is being traded. The exchange field in a contract is not set for portfolio update.
        :param position: The number of positions held. If the position is 0, it means the position has just cleared.
        :param marketPrice: The unit price of the instrument.
        :param marketValue: The total market value of the instrument.
        :param averageCost: The average cost per share is calculated by dividing your cost (execution price + commission) by the quantity of your position.
        :param unrealisedPnl: The difference between the current market value of your open positions and the average cost, or Value - Average Cost.
        :param realisedPnl: Shows your profit on closed positions, which is the difference between your entry execution cost (execution price + commissions to open the position) and exit execution cost ((execution price + commissions to close the position)
        :param accountName: The name of the account to which the message applies.  Useful for Financial Advisor sub-account messages.
        """
        ...

    def accountDownloadEnd(self, account: str) -> None:
        """
        This event is called when the receipt of an account's information has been completed.
        
        :param account: The account ID.
        """
        ...

    def orderStatus(self, orderId: int, status: str, filled: float, remaining: float, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float) -> None:
        """
        This method is called whenever the status of an order changes. It is also called after reconnecting to TWS if the client has any open orders.
        
        :param orderId: The order Id that was specified previously in the call to placeOrder()
        :param status: The order status.
        :param filled: Specifies the number of shares that have been executed.
        :param remaining: Specifies the number of shares still outstanding.
        :param avgFillPrice: The average price of the shares that have been executed. This parameter is valid only if the filled parameter value is greater than zero. Otherwise, the price parameter will be zero.
        :param permId: The TWS id used to identify orders. Remains the same over TWS sessions.
        :param parentId: The order ID of the parent order, used for bracket and auto trailing stop orders.
        :param lastFillPrice: The last price of the shares that have been executed. This parameter is valid only if the filled parameter value is greater than zero. Otherwise, the price parameter will be zero.
        :param clientId: The ID of the client (or TWS) that placed the order. Note that TWS orders have a fixed clientId and orderId of 0 that distinguishes them from API orders.
        :param whyHeld: This field is used to identify an order held when TWS is trying to locate shares for a short sell. The value used to indicate this is 'locate'.
        :param mktCapPrice: If an order has been capped, this indicates the current capped price. Requires TWS 967+ and API v973.04+. Python API specifically requires API v973.06+.
        """
        ...

    def openOrder(self, orderId: int, contract: typing.Any, order: typing.Any, orderState: typing.Any) -> None:
        """
        This callback feeds in open orders.
        
        :param orderId: The order Id assigned by TWS. Used to cancel or update the order.
        :param contract: The Contract class attributes describe the contract.
        :param order: The Order class attributes define the details of the order.
        :param orderState: The orderState attributes include margin and commissions fields for both pre and post trade data.
        """
        ...

    def openOrderEnd(self) -> None:
        """This is called at the end of a given request for open orders."""
        ...

    def contractDetails(self, reqId: int, contractDetails: typing.Any) -> None:
        """
        Returns all contracts matching the requested parameters in reqContractDetails(). For example, you can receive an entire option chain.
        
        :param reqId: The ID of the data request. Ensures that responses are matched to requests if several requests are in process.
        :param contractDetails: This structure contains a full description of the contract being looked up.
        """
        ...

    def contractDetailsEnd(self, reqId: int) -> None:
        """
        This method is called once all contract details for a given request are received. This helps to define the end of an option chain.
        
        :param reqId: The Id of the data request.
        """
        ...

    def execDetails(self, reqId: int, contract: typing.Any, execution: typing.Any) -> None:
        """
        Returns executions from the last 24 hours as a response to reqExecutions(), or when an order is filled.
        
        :param reqId: The request's identifier.
        :param contract: This structure contains a full description of the contract that was executed.
        :param execution: This structure contains addition order execution details.
        """
        ...

    def execDetailsEnd(self, reqId: int) -> None:
        """
        This method is called once all executions have been sent to a client in response to reqExecutions().
        
        :param reqId: The request's identifier.
        """
        ...

    def commissionReport(self, commissionReport: typing.Any) -> None:
        """
        This callback returns the commission report portion of an execution and is triggered immediately after a trade execution, or by calling reqExecution().
        
        :param commissionReport: The structure that contains commission details.
        """
        ...

    def historicalData(self, reqId: int, bar: typing.Any) -> None:
        """
        Receives the historical data in response to reqHistoricalData().
        
        :param reqId: The request's identifier.
        :param bar: The bar data.
        """
        ...

    def historicalDataEnd(self, reqId: int, start: str, end: str) -> None:
        """
        Marks the ending of the historical bars reception.
        
        :param reqId: The request's identifier.
        """
        ...

    def positionEnd(self) -> None:
        """This is called once all position data for a given request are received and functions as an end marker for the position() data."""
        ...

    def receiveFA(self, faDataType: int, faXmlData: str) -> None:
        """
        This method receives Financial Advisor configuration information from TWS.
        
        :param faDataType: Specifies the type of Financial Advisor configuration data being received from TWS.
        :param faXmlData: The XML string containing the previously requested FA configuration information.
        """
        ...

    def connectAck(self) -> None:
        """Callback signifying completion of successful connection."""
        ...

    def managedAccounts(self, accountList: str) -> None:
        """
        Receives a comma-separated string with the managed account ids. Occurs automatically on initial API client connection.
        
        :param accountList: A comma-separated string with the managed account ids.
        """
        ...

    def familyCodes(self, familyCodes: typing.List[FamilyCode]) -> None:
        """
        Returns array of family codes
        
        :param familyCodes: An array of family codes.
        """
        ...

    def OnError(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.ErrorEventArgs) -> None:
        """This method is protected."""
        ...

    def OnCurrentTimeUtc(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.CurrentTimeUtcEventArgs) -> None:
        """
        CurrentTimeUtc event invocator
        
        This method is protected.
        """
        ...

    def OnTickPrice(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.TickPriceEventArgs) -> None:
        """
        TickPrice event invocator
        
        This method is protected.
        """
        ...

    def OnTickSize(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.TickSizeEventArgs) -> None:
        """
        TickSize event invocator
        
        This method is protected.
        """
        ...

    def OnNextValidId(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.NextValidIdEventArgs) -> None:
        """
        NextValidId event invocator
        
        This method is protected.
        """
        ...

    def OnConnectionClosed(self) -> None:
        """
        ConnectionClosed event invocator
        
        This method is protected.
        """
        ...

    def OnAccountSummary(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.AccountSummaryEventArgs) -> None:
        """
        AccountSummary event invocator
        
        This method is protected.
        """
        ...

    def OnAccountSummaryEnd(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.RequestEndEventArgs) -> None:
        """
        AccountSummaryEnd event invocator
        
        This method is protected.
        """
        ...

    def OnBondContractDetails(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.ContractDetailsEventArgs) -> None:
        """
        BondContractDetails event invocator
        
        This method is protected.
        """
        ...

    def OnUpdateAccountValue(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.UpdateAccountValueEventArgs) -> None:
        """
        UpdateAccountValue event invocator
        
        This method is protected.
        """
        ...

    def OnUpdatePortfolio(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.UpdatePortfolioEventArgs) -> None:
        """
        UpdatePortfolio event invocator
        
        This method is protected.
        """
        ...

    def OnAccountDownloadEnd(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.AccountDownloadEndEventArgs) -> None:
        """
        AccountDownloadEnd event invocator
        
        This method is protected.
        """
        ...

    def OnOrderStatus(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.OrderStatusEventArgs) -> None:
        """
        OrderStatus event invocator
        
        This method is protected.
        """
        ...

    def OnOpenOrder(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.OpenOrderEventArgs) -> None:
        """
        OpenOrder event invocator
        
        This method is protected.
        """
        ...

    def OnOpenOrderEnd(self) -> None:
        """
        OpenOrderEnd event invocator
        
        This method is protected.
        """
        ...

    def OnContractDetails(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.ContractDetailsEventArgs) -> None:
        """
        ContractDetails event invocator
        
        This method is protected.
        """
        ...

    def OnContractDetailsEnd(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.RequestEndEventArgs) -> None:
        """
        ContractDetailsEnd event invocator
        
        This method is protected.
        """
        ...

    def OnExecutionDetails(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.ExecutionDetailsEventArgs) -> None:
        """
        ExecutionDetails event invocator
        
        This method is protected.
        """
        ...

    def OnExecutionDetailsEnd(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.RequestEndEventArgs) -> None:
        """
        ExecutionDetailsEnd event invocator
        
        This method is protected.
        """
        ...

    def OnCommissionReport(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.CommissionReportEventArgs) -> None:
        """
        CommissionReport event invocator
        
        This method is protected.
        """
        ...

    def OnHistoricalData(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.HistoricalDataEventArgs) -> None:
        """
        HistoricalData event invocator
        
        This method is protected.
        """
        ...

    def OnHistoricalDataEnd(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.HistoricalDataEndEventArgs) -> None:
        """
        HistoricalDataEnd event invocator
        
        This method is protected.
        """
        ...

    def OnPositionEnd(self) -> None:
        """
        PositionEnd event invocator
        
        This method is protected.
        """
        ...

    def OnReceiveFa(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.ReceiveFaEventArgs) -> None:
        """
        ReceiveFa event invocator
        
        This method is protected.
        """
        ...

    def OnConnectAck(self) -> None:
        """
        ConnectAck event invocator
        
        This method is protected.
        """
        ...

    def OnManagedAccounts(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.ManagedAccountsEventArgs) -> None:
        """
        ManagedAccounts event invocator
        
        This method is protected.
        """
        ...

    def OnFamilyCodes(self, e: QuantConnect.Brokerages.InteractiveBrokers.Client.FamilyCodesEventArgs) -> None:
        """
        FamilyCodes event invocator
        
        This method is protected.
        """
        ...


class OrderType(System.Object):
    """Order Type string constants"""

    Market: str = "MKT"
    """
    A Market order is an order to buy or sell an asset at the bid or offer price currently available in the marketplace.
    Bonds, Forex, Futures, Future Options, Options, Stocks, Warrants
    """

    MarketOnClose: str = "MOC"
    """
    A market order that is submitted to execute as close to the closing price as possible.
    Non US Futures, Non US Options, Stocks
    """

    Limit: str = "LMT"
    """
    A limit order is an order to buy or sell a contract at a specified price or better.
    Bonds, Forex, Futures, Future Options, Options, Stocks, Warrants
    """

    LimitOnClose: str = "LOC"
    """
    An LOC (Limit-on-Close) order that executes at the closing price if the closing price is at or better than the submitted limit price, according to the rules of the specific exchange. Otherwise the order will be cancelled.
    Non US Futures , Stocks
    """

    PeggedToMarket: str = "PEGMKT"
    """
    An order that is pegged to buy on the best offer and sell on the best bid.
    Your order is pegged to buy on the best offer and sell on the best bid. You can also use an offset amount which is subtracted from the best offer for a buy order, and added to the best bid for a sell order.
    Stocks
    """

    Stop: str = "STP"
    """
    A Stop order becomes a market order to buy or sell securities or commodities once the specified stop price is attained or penetrated.
    Forex, Futures, Future Options, Options, Stocks, Warrants
    """

    StopLimit: str = "STP LMT"
    """
    A STOP-LIMIT order is similar to a stop order in that a stop price will activate the order. However, once activated, the stop-limit order becomes a buy limit or sell limit order and can only be executed at a specific price or better. It is a combination of both the stop order and the limit order.
    Forex, Futures, Options, Stocks
    """

    TrailingStop: str = "TRAIL"
    """
    A trailing stop for a sell order sets the stop price at a fixed amount below the market price. If the market price rises, the stop loss price rises by the increased amount, but if the stock price falls, the stop loss price remains the same. The reverse is true for a buy trailing stop order.
    Forex, Futures, Future Options, Options, Stocks, Warrants
    """

    Relative: str = "REL"
    """
    A Relative order derives its price from a combination of the market quote and a user-defined offset amount. The order is submitted as a limit order and modified according to the pricing logic until it is executed or you cancel the order.
    Options, Stocks
    """

    VolumeWeightedAveragePrice: str = "VWAP"
    """
    The VWAP for a stock is calculated by adding the dollars traded for every transaction in that stock ("price" x "number of shares traded") and dividing the total shares traded. By default, a VWAP order is computed from the open of the market to the market close, and is calculated by volume weighting all transactions during this time period. TWS allows you to modify the cut-off and expiration times using the Time in Force and Expiration Date fields, respectively.
    Stocks
    """

    TrailingStopLimit: str = "TRAILLIMIT"
    """
    A trailing stop limit for a sell order sets the stop price at a fixed amount below the market price and defines a limit price for the sell order. If the market price rises, the stop loss price rises by the increased amount, but if the stock price falls, the stop loss price remains the same. When the order triggers, a limit order is submitted at the price you defined. The reverse is true for a buy trailing stop limit order.
    Forex, Futures, Future Options, Options, Stocks, Warrants
    """

    Volatility: str = "VOL"
    """TWS Version 857 introduced volatility trading of options, and a new order type, "VOL." What happens with VOL orders is that the limit price that is sent to the exchange is computed by TWS as a function of a daily or annualized option volatility provided by the user. VOL orders can be placed for any US option that trades on the BOX exchange. VOL orders are eligible for dynamic management, a powerful new functionality wherein TWS can manage options orders in response to specifications set by the user."""

    # Cannot convert to Python: None: str = "NONE"
    """
    VOL orders only. Enter an order type to instruct TWS to submit a
    delta neutral trade on full or partial execution of the VOL order.
    For no hedge delta order to be sent, specify NONE.
    """

    Empty: str = ...
    """Used to initialize the delta Order Field."""

    Default: str = "Default"
    """Default - used for Delta Neutral Order Type"""

    Scale: str = "SCALE"
    """Scale Order."""

    MarketIfTouched: str = "MIT"
    """Market if Touched Order."""

    LimitIfTouched: str = "LIT"
    """Limit if Touched Order."""


