import typing

import QuantConnect.Brokerages.Binance.Messages
import System


class AccountInformation(System.Object):
    """This class has no documentation."""

    class Balance(System.Object):
        """This class has no documentation."""

        @property
        def Asset(self) -> str:
            ...

        @Asset.setter
        def Asset(self, value: str):
            ...

        @property
        def Free(self) -> float:
            ...

        @Free.setter
        def Free(self, value: float):
            ...

        @property
        def Locked(self) -> float:
            ...

        @Locked.setter
        def Locked(self, value: float):
            ...

        @property
        def Amount(self) -> float:
            ...

    @property
    def Balances(self) -> typing.List[QuantConnect.Brokerages.Binance.Messages.AccountInformation.Balance]:
        ...

    @Balances.setter
    def Balances(self, value: typing.List[QuantConnect.Brokerages.Binance.Messages.AccountInformation.Balance]):
        ...


class PriceTicker(System.Object):
    """This class has no documentation."""

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...


class Order(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> str:
        ...

    @Id.setter
    def Id(self, value: str):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def StopPrice(self) -> float:
        ...

    @StopPrice.setter
    def StopPrice(self, value: float):
        ...

    @property
    def OriginalAmount(self) -> float:
        ...

    @OriginalAmount.setter
    def OriginalAmount(self, value: float):
        ...

    @property
    def ExecutedAmount(self) -> float:
        ...

    @ExecutedAmount.setter
    def ExecutedAmount(self, value: float):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def Quantity(self) -> float:
        ...


class OpenOrder(QuantConnect.Brokerages.Binance.Messages.Order):
    """This class has no documentation."""

    @property
    def Time(self) -> int:
        ...

    @Time.setter
    def Time(self, value: int):
        ...


class NewOrder(QuantConnect.Brokerages.Binance.Messages.Order):
    """This class has no documentation."""

    @property
    def TransactionTime(self) -> int:
        ...

    @TransactionTime.setter
    def TransactionTime(self, value: int):
        ...


class EventType(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    OrderBook = 1

    Trade = 2

    Execution = 3


class ErrorMessage(System.Object):
    """This class has no documentation."""

    @property
    def Code(self) -> int:
        ...

    @Code.setter
    def Code(self, value: int):
        ...

    @property
    def Message(self) -> str:
        ...

    @Message.setter
    def Message(self, value: str):
        ...


class BestBidAskQuote(System.Object):
    """This class has no documentation."""

    @property
    def OrderBookUpdateId(self) -> int:
        ...

    @OrderBookUpdateId.setter
    def OrderBookUpdateId(self, value: int):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def BestBidPrice(self) -> float:
        ...

    @BestBidPrice.setter
    def BestBidPrice(self, value: float):
        ...

    @property
    def BestBidSize(self) -> float:
        ...

    @BestBidSize.setter
    def BestBidSize(self, value: float):
        ...

    @property
    def BestAskPrice(self) -> float:
        ...

    @BestAskPrice.setter
    def BestAskPrice(self, value: float):
        ...

    @property
    def BestAskSize(self) -> float:
        ...

    @BestAskSize.setter
    def BestAskSize(self, value: float):
        ...


class BaseMessage(System.Object):
    """This class has no documentation."""

    # Cannot convert property @Event to Python

    @property
    def EventName(self) -> str:
        ...

    @EventName.setter
    def EventName(self, value: str):
        ...

    @property
    def Time(self) -> int:
        ...

    @Time.setter
    def Time(self, value: int):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...


class Trade(QuantConnect.Brokerages.Binance.Messages.BaseMessage):
    """This class has no documentation."""

    # Cannot convert property @Event to Python

    @property
    def Time(self) -> int:
        ...

    @Time.setter
    def Time(self, value: int):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Quantity(self) -> float:
        ...

    @Quantity.setter
    def Quantity(self, value: float):
        ...


class Execution(QuantConnect.Brokerages.Binance.Messages.BaseMessage):
    """This class has no documentation."""

    # Cannot convert property @Event to Python

    @property
    def OrderId(self) -> str:
        ...

    @OrderId.setter
    def OrderId(self, value: str):
        ...

    @property
    def TradeId(self) -> str:
        ...

    @TradeId.setter
    def TradeId(self, value: str):
        ...

    @property
    def Ignore(self) -> str:
        ...

    @Ignore.setter
    def Ignore(self, value: str):
        ...

    @property
    def ExecutionType(self) -> str:
        ...

    @ExecutionType.setter
    def ExecutionType(self, value: str):
        ...

    @property
    def OrderStatus(self) -> str:
        ...

    @OrderStatus.setter
    def OrderStatus(self, value: str):
        ...

    @property
    def TransactionTime(self) -> int:
        ...

    @TransactionTime.setter
    def TransactionTime(self, value: int):
        ...

    @property
    def LastExecutedPrice(self) -> float:
        ...

    @LastExecutedPrice.setter
    def LastExecutedPrice(self, value: float):
        ...

    @property
    def LastExecutedQuantity(self) -> float:
        ...

    @LastExecutedQuantity.setter
    def LastExecutedQuantity(self, value: float):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def Fee(self) -> float:
        ...

    @Fee.setter
    def Fee(self, value: float):
        ...

    @property
    def FeeCurrency(self) -> str:
        ...

    @FeeCurrency.setter
    def FeeCurrency(self, value: str):
        ...

    @property
    def Direction(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Orders.OrderDirection enum."""
        ...


class Kline(System.Object):
    """This class has no documentation."""

    @property
    def OpenTime(self) -> int:
        ...

    @property
    def Open(self) -> float:
        ...

    @property
    def Close(self) -> float:
        ...

    @property
    def High(self) -> float:
        ...

    @property
    def Low(self) -> float:
        ...

    @property
    def Volume(self) -> float:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, msts: int, close: float) -> None:
        ...

    @typing.overload
    def __init__(self, entries: typing.List[System.Object]) -> None:
        ...


