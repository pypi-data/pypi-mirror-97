import datetime
import typing

import QuantConnect.Brokerages.Zerodha.Messages
import System
import System.Collections.Generic


class DepthItem:
    """Market depth item structure"""

    @property
    def Quantity(self) -> int:
        ...

    @Quantity.setter
    def Quantity(self, value: int):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Orders(self) -> int:
        ...

    @Orders.setter
    def Orders(self, value: int):
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class Tick:
    """Tick data structure"""

    @property
    def Mode(self) -> str:
        ...

    @Mode.setter
    def Mode(self, value: str):
        ...

    @property
    def InstrumentToken(self) -> int:
        ...

    @InstrumentToken.setter
    def InstrumentToken(self, value: int):
        ...

    @property
    def Tradable(self) -> bool:
        ...

    @Tradable.setter
    def Tradable(self, value: bool):
        ...

    @property
    def LastPrice(self) -> float:
        ...

    @LastPrice.setter
    def LastPrice(self, value: float):
        ...

    @property
    def LastQuantity(self) -> int:
        ...

    @LastQuantity.setter
    def LastQuantity(self, value: int):
        ...

    @property
    def AveragePrice(self) -> float:
        ...

    @AveragePrice.setter
    def AveragePrice(self, value: float):
        ...

    @property
    def Volume(self) -> int:
        ...

    @Volume.setter
    def Volume(self, value: int):
        ...

    @property
    def BuyQuantity(self) -> int:
        ...

    @BuyQuantity.setter
    def BuyQuantity(self, value: int):
        ...

    @property
    def SellQuantity(self) -> int:
        ...

    @SellQuantity.setter
    def SellQuantity(self, value: int):
        ...

    @property
    def Open(self) -> float:
        ...

    @Open.setter
    def Open(self, value: float):
        ...

    @property
    def High(self) -> float:
        ...

    @High.setter
    def High(self, value: float):
        ...

    @property
    def Low(self) -> float:
        ...

    @Low.setter
    def Low(self, value: float):
        ...

    @property
    def Close(self) -> float:
        ...

    @Close.setter
    def Close(self, value: float):
        ...

    @property
    def Change(self) -> float:
        ...

    @Change.setter
    def Change(self, value: float):
        ...

    @property
    def Bids(self) -> typing.List[QuantConnect.Brokerages.Zerodha.Messages.DepthItem]:
        ...

    @Bids.setter
    def Bids(self, value: typing.List[QuantConnect.Brokerages.Zerodha.Messages.DepthItem]):
        ...

    @property
    def Offers(self) -> typing.List[QuantConnect.Brokerages.Zerodha.Messages.DepthItem]:
        ...

    @Offers.setter
    def Offers(self, value: typing.List[QuantConnect.Brokerages.Zerodha.Messages.DepthItem]):
        ...

    @property
    def LastTradeTime(self) -> typing.Optional[datetime.datetime]:
        ...

    @LastTradeTime.setter
    def LastTradeTime(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def OI(self) -> int:
        ...

    @OI.setter
    def OI(self, value: int):
        ...

    @property
    def OIDayHigh(self) -> int:
        ...

    @OIDayHigh.setter
    def OIDayHigh(self, value: int):
        ...

    @property
    def OIDayLow(self) -> int:
        ...

    @OIDayLow.setter
    def OIDayLow(self, value: int):
        ...

    @property
    def Timestamp(self) -> typing.Optional[datetime.datetime]:
        ...

    @Timestamp.setter
    def Timestamp(self, value: typing.Optional[datetime.datetime]):
        ...


class Historical:
    """Historical structure"""

    @property
    def TimeStamp(self) -> datetime.datetime:
        ...

    @property
    def Open(self) -> float:
        ...

    @property
    def High(self) -> float:
        ...

    @property
    def Low(self) -> float:
        ...

    @property
    def Close(self) -> float:
        ...

    @property
    def Volume(self) -> int:
        ...

    @property
    def OI(self) -> int:
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class Holding:
    """Holding structure"""

    @property
    def Product(self) -> str:
        ...

    @Product.setter
    def Product(self, value: str):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def LastPrice(self) -> float:
        ...

    @LastPrice.setter
    def LastPrice(self, value: float):
        ...

    @property
    def CollateralQuantity(self) -> int:
        ...

    @CollateralQuantity.setter
    def CollateralQuantity(self, value: int):
        ...

    @property
    def PNL(self) -> float:
        ...

    @PNL.setter
    def PNL(self, value: float):
        ...

    @property
    def ClosePrice(self) -> float:
        ...

    @ClosePrice.setter
    def ClosePrice(self, value: float):
        ...

    @property
    def AveragePrice(self) -> float:
        ...

    @AveragePrice.setter
    def AveragePrice(self, value: float):
        ...

    @property
    def TradingSymbol(self) -> str:
        ...

    @TradingSymbol.setter
    def TradingSymbol(self, value: str):
        ...

    @property
    def CollateralType(self) -> str:
        ...

    @CollateralType.setter
    def CollateralType(self, value: str):
        ...

    @property
    def T1Quantity(self) -> int:
        ...

    @T1Quantity.setter
    def T1Quantity(self, value: int):
        ...

    @property
    def InstrumentToken(self) -> int:
        ...

    @InstrumentToken.setter
    def InstrumentToken(self, value: int):
        ...

    @property
    def ISIN(self) -> str:
        ...

    @ISIN.setter
    def ISIN(self, value: str):
        ...

    @property
    def RealisedQuantity(self) -> int:
        ...

    @RealisedQuantity.setter
    def RealisedQuantity(self, value: int):
        ...

    @property
    def Quantity(self) -> int:
        ...

    @Quantity.setter
    def Quantity(self, value: int):
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class AvailableMargin:
    """Available margin structure"""

    @property
    def AdHocMargin(self) -> float:
        ...

    @AdHocMargin.setter
    def AdHocMargin(self, value: float):
        ...

    @property
    def Cash(self) -> float:
        ...

    @Cash.setter
    def Cash(self, value: float):
        ...

    @property
    def Collateral(self) -> float:
        ...

    @Collateral.setter
    def Collateral(self, value: float):
        ...

    @property
    def IntradayPayin(self) -> float:
        ...

    @IntradayPayin.setter
    def IntradayPayin(self, value: float):
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class UtilisedMargin:
    """Utilised margin structure"""

    @property
    def Debits(self) -> float:
        ...

    @Debits.setter
    def Debits(self, value: float):
        ...

    @property
    def Exposure(self) -> float:
        ...

    @Exposure.setter
    def Exposure(self, value: float):
        ...

    @property
    def M2MRealised(self) -> float:
        ...

    @M2MRealised.setter
    def M2MRealised(self, value: float):
        ...

    @property
    def M2MUnrealised(self) -> float:
        ...

    @M2MUnrealised.setter
    def M2MUnrealised(self, value: float):
        ...

    @property
    def OptionPremium(self) -> float:
        ...

    @OptionPremium.setter
    def OptionPremium(self, value: float):
        ...

    @property
    def Payout(self) -> float:
        ...

    @Payout.setter
    def Payout(self, value: float):
        ...

    @property
    def Span(self) -> float:
        ...

    @Span.setter
    def Span(self, value: float):
        ...

    @property
    def HoldingSales(self) -> float:
        ...

    @HoldingSales.setter
    def HoldingSales(self, value: float):
        ...

    @property
    def Turnover(self) -> float:
        ...

    @Turnover.setter
    def Turnover(self, value: float):
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class UserMargin:
    """UserMargin structure"""

    @property
    def Enabled(self) -> bool:
        ...

    @Enabled.setter
    def Enabled(self, value: bool):
        ...

    @property
    def Net(self) -> float:
        ...

    @Net.setter
    def Net(self, value: float):
        ...

    @property
    def Available(self) -> QuantConnect.Brokerages.Zerodha.Messages.AvailableMargin:
        ...

    @Available.setter
    def Available(self, value: QuantConnect.Brokerages.Zerodha.Messages.AvailableMargin):
        ...

    @property
    def Utilised(self) -> QuantConnect.Brokerages.Zerodha.Messages.UtilisedMargin:
        ...

    @Utilised.setter
    def Utilised(self, value: QuantConnect.Brokerages.Zerodha.Messages.UtilisedMargin):
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class UserMarginsResponse:
    """User margins response structure"""

    @property
    def Equity(self) -> QuantConnect.Brokerages.Zerodha.Messages.UserMargin:
        ...

    @Equity.setter
    def Equity(self, value: QuantConnect.Brokerages.Zerodha.Messages.UserMargin):
        ...

    @property
    def Commodity(self) -> QuantConnect.Brokerages.Zerodha.Messages.UserMargin:
        ...

    @Commodity.setter
    def Commodity(self, value: QuantConnect.Brokerages.Zerodha.Messages.UserMargin):
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class InstrumentMargin:
    """UserMargin structure"""

    @property
    def Tradingsymbol(self) -> str:
        ...

    @Tradingsymbol.setter
    def Tradingsymbol(self, value: str):
        ...

    @property
    def Margin(self) -> float:
        ...

    @Margin.setter
    def Margin(self, value: float):
        ...

    @property
    def COLower(self) -> float:
        ...

    @COLower.setter
    def COLower(self, value: float):
        ...

    @property
    def COUpper(self) -> float:
        ...

    @COUpper.setter
    def COUpper(self, value: float):
        ...

    @property
    def MISMultiplier(self) -> float:
        ...

    @MISMultiplier.setter
    def MISMultiplier(self, value: float):
        ...

    @property
    def MISMargin(self) -> float:
        ...

    @MISMargin.setter
    def MISMargin(self, value: float):
        ...

    @property
    def NRMLMargin(self) -> float:
        ...

    @NRMLMargin.setter
    def NRMLMargin(self, value: float):
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class Position:
    """Position structure"""

    @property
    def Product(self) -> str:
        ...

    @property
    def OvernightQuantity(self) -> int:
        ...

    @property
    def Exchange(self) -> str:
        ...

    @property
    def SellValue(self) -> float:
        ...

    @property
    def BuyM2M(self) -> float:
        ...

    @property
    def LastPrice(self) -> float:
        ...

    @property
    def TradingSymbol(self) -> str:
        ...

    @property
    def Realised(self) -> float:
        ...

    @property
    def PNL(self) -> float:
        ...

    @property
    def Multiplier(self) -> float:
        ...

    @property
    def SellQuantity(self) -> int:
        ...

    @property
    def SellM2M(self) -> float:
        ...

    @property
    def BuyValue(self) -> float:
        ...

    @property
    def BuyQuantity(self) -> int:
        ...

    @property
    def AveragePrice(self) -> float:
        ...

    @property
    def Unrealised(self) -> float:
        ...

    @property
    def Value(self) -> float:
        ...

    @property
    def BuyPrice(self) -> float:
        ...

    @property
    def SellPrice(self) -> float:
        ...

    @property
    def M2M(self) -> float:
        ...

    @property
    def InstrumentToken(self) -> int:
        ...

    @property
    def ClosePrice(self) -> float:
        ...

    @property
    def Quantity(self) -> int:
        ...

    @property
    def DayBuyQuantity(self) -> int:
        ...

    @property
    def DayBuyPrice(self) -> float:
        ...

    @property
    def DayBuyValue(self) -> float:
        ...

    @property
    def DaySellQuantity(self) -> int:
        ...

    @property
    def DaySellPrice(self) -> float:
        ...

    @property
    def DaySellValue(self) -> float:
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class PositionResponse:
    """Position response structure"""

    @property
    def Day(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.Position]:
        ...

    @property
    def Net(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.Position]:
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class Order:
    """Order structure"""

    @property
    def AveragePrice(self) -> float:
        ...

    @AveragePrice.setter
    def AveragePrice(self, value: float):
        ...

    @property
    def CancelledQuantity(self) -> int:
        ...

    @CancelledQuantity.setter
    def CancelledQuantity(self, value: int):
        ...

    @property
    def DisclosedQuantity(self) -> int:
        ...

    @DisclosedQuantity.setter
    def DisclosedQuantity(self, value: int):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def ExchangeOrderId(self) -> str:
        ...

    @ExchangeOrderId.setter
    def ExchangeOrderId(self, value: str):
        ...

    @property
    def ExchangeTimestamp(self) -> typing.Optional[datetime.datetime]:
        ...

    @ExchangeTimestamp.setter
    def ExchangeTimestamp(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def FilledQuantity(self) -> int:
        ...

    @FilledQuantity.setter
    def FilledQuantity(self, value: int):
        ...

    @property
    def InstrumentToken(self) -> int:
        ...

    @InstrumentToken.setter
    def InstrumentToken(self, value: int):
        ...

    @property
    def OrderId(self) -> str:
        ...

    @OrderId.setter
    def OrderId(self, value: str):
        ...

    @property
    def OrderTimestamp(self) -> typing.Optional[datetime.datetime]:
        ...

    @OrderTimestamp.setter
    def OrderTimestamp(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def OrderType(self) -> str:
        ...

    @OrderType.setter
    def OrderType(self, value: str):
        ...

    @property
    def ParentOrderId(self) -> str:
        ...

    @ParentOrderId.setter
    def ParentOrderId(self, value: str):
        ...

    @property
    def PendingQuantity(self) -> int:
        ...

    @PendingQuantity.setter
    def PendingQuantity(self, value: int):
        ...

    @property
    def PlacedBy(self) -> str:
        ...

    @PlacedBy.setter
    def PlacedBy(self, value: str):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Product(self) -> str:
        ...

    @Product.setter
    def Product(self, value: str):
        ...

    @property
    def Quantity(self) -> int:
        ...

    @Quantity.setter
    def Quantity(self, value: int):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def StatusMessage(self) -> str:
        ...

    @StatusMessage.setter
    def StatusMessage(self, value: str):
        ...

    @property
    def Tag(self) -> str:
        ...

    @Tag.setter
    def Tag(self, value: str):
        ...

    @property
    def Tradingsymbol(self) -> str:
        ...

    @Tradingsymbol.setter
    def Tradingsymbol(self, value: str):
        ...

    @property
    def TransactionType(self) -> str:
        ...

    @TransactionType.setter
    def TransactionType(self, value: str):
        ...

    @property
    def TriggerPrice(self) -> float:
        ...

    @TriggerPrice.setter
    def TriggerPrice(self, value: float):
        ...

    @property
    def Validity(self) -> str:
        ...

    @Validity.setter
    def Validity(self, value: str):
        ...

    @property
    def Variety(self) -> str:
        ...

    @Variety.setter
    def Variety(self, value: str):
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class ChannelSubscription:
    """This class has no documentation."""

    @property
    def ChannelId(self) -> str:
        ...

    @ChannelId.setter
    def ChannelId(self, value: str):
        ...

    @property
    def a(self) -> str:
        ...

    @a.setter
    def a(self, value: str):
        ...

    @property
    def v(self) -> typing.List[int]:
        ...

    @v.setter
    def v(self, value: typing.List[int]):
        ...


class ChannelUnsubscription:
    """This class has no documentation."""

    @property
    def ChannelId(self) -> str:
        ...

    @ChannelId.setter
    def ChannelId(self, value: str):
        ...

    @property
    def a(self) -> str:
        ...

    @a.setter
    def a(self, value: str):
        ...

    @property
    def v(self) -> typing.List[int]:
        ...

    @v.setter
    def v(self, value: typing.List[int]):
        ...


class GTTCondition:
    """GTTCondition structure"""

    @property
    def InstrumentToken(self) -> int:
        ...

    @InstrumentToken.setter
    def InstrumentToken(self, value: int):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def TradingSymbol(self) -> str:
        ...

    @TradingSymbol.setter
    def TradingSymbol(self, value: str):
        ...

    @property
    def TriggerValues(self) -> System.Collections.Generic.List[float]:
        ...

    @TriggerValues.setter
    def TriggerValues(self, value: System.Collections.Generic.List[float]):
        ...

    @property
    def LastPrice(self) -> float:
        ...

    @LastPrice.setter
    def LastPrice(self, value: float):
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class GTTOrderResult:
    """GTTOrderResult structure"""

    @property
    def OrderId(self) -> str:
        ...

    @OrderId.setter
    def OrderId(self, value: str):
        ...

    @property
    def RejectionReason(self) -> str:
        ...

    @RejectionReason.setter
    def RejectionReason(self, value: str):
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class GTTResult:
    """GTTResult structure"""

    @property
    def OrderResult(self) -> typing.Optional[QuantConnect.Brokerages.Zerodha.Messages.GTTOrderResult]:
        ...

    @OrderResult.setter
    def OrderResult(self, value: typing.Optional[QuantConnect.Brokerages.Zerodha.Messages.GTTOrderResult]):
        ...

    @property
    def Timestamp(self) -> str:
        ...

    @Timestamp.setter
    def Timestamp(self, value: str):
        ...

    @property
    def TriggeredAtPrice(self) -> float:
        ...

    @TriggeredAtPrice.setter
    def TriggeredAtPrice(self, value: float):
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class GTTOrder:
    """GTTOrder structure"""

    @property
    def TransactionType(self) -> str:
        ...

    @TransactionType.setter
    def TransactionType(self, value: str):
        ...

    @property
    def Product(self) -> str:
        ...

    @Product.setter
    def Product(self, value: str):
        ...

    @property
    def OrderType(self) -> str:
        ...

    @OrderType.setter
    def OrderType(self, value: str):
        ...

    @property
    def Quantity(self) -> int:
        ...

    @Quantity.setter
    def Quantity(self, value: int):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Result(self) -> typing.Optional[QuantConnect.Brokerages.Zerodha.Messages.GTTResult]:
        ...

    @Result.setter
    def Result(self, value: typing.Optional[QuantConnect.Brokerages.Zerodha.Messages.GTTResult]):
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class GTTMeta:
    """GTTMeta structure"""

    @property
    def RejectionReason(self) -> str:
        ...

    @RejectionReason.setter
    def RejectionReason(self, value: str):
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class GTT:
    """GTTOrder structure"""

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def Condition(self) -> typing.Optional[QuantConnect.Brokerages.Zerodha.Messages.GTTCondition]:
        ...

    @Condition.setter
    def Condition(self, value: typing.Optional[QuantConnect.Brokerages.Zerodha.Messages.GTTCondition]):
        ...

    @property
    def TriggerType(self) -> str:
        ...

    @TriggerType.setter
    def TriggerType(self, value: str):
        ...

    @property
    def Orders(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.GTTOrder]:
        ...

    @Orders.setter
    def Orders(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.GTTOrder]):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def CreatedAt(self) -> typing.Optional[datetime.datetime]:
        ...

    @CreatedAt.setter
    def CreatedAt(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def UpdatedAt(self) -> typing.Optional[datetime.datetime]:
        ...

    @UpdatedAt.setter
    def UpdatedAt(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def ExpiresAt(self) -> typing.Optional[datetime.datetime]:
        ...

    @ExpiresAt.setter
    def ExpiresAt(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def Meta(self) -> typing.Optional[QuantConnect.Brokerages.Zerodha.Messages.GTTMeta]:
        ...

    @Meta.setter
    def Meta(self, value: typing.Optional[QuantConnect.Brokerages.Zerodha.Messages.GTTMeta]):
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class GTTOrderParams:
    """GTTOrderParams structure"""

    @property
    def Quantity(self) -> int:
        ...

    @Quantity.setter
    def Quantity(self, value: int):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def OrderType(self) -> str:
        ...

    @OrderType.setter
    def OrderType(self, value: str):
        ...

    @property
    def Product(self) -> str:
        ...

    @Product.setter
    def Product(self, value: str):
        ...

    @property
    def TransactionType(self) -> str:
        ...

    @TransactionType.setter
    def TransactionType(self, value: str):
        ...


class GTTParams:
    """GTTParams structure"""

    @property
    def TradingSymbol(self) -> str:
        ...

    @TradingSymbol.setter
    def TradingSymbol(self, value: str):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def InstrumentToken(self) -> int:
        ...

    @InstrumentToken.setter
    def InstrumentToken(self, value: int):
        ...

    @property
    def TriggerType(self) -> str:
        ...

    @TriggerType.setter
    def TriggerType(self, value: str):
        ...

    @property
    def LastPrice(self) -> float:
        ...

    @LastPrice.setter
    def LastPrice(self, value: float):
        ...

    @property
    def Orders(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.GTTOrderParams]:
        ...

    @Orders.setter
    def Orders(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.GTTOrderParams]):
        ...

    @property
    def TriggerPrices(self) -> System.Collections.Generic.List[float]:
        ...

    @TriggerPrices.setter
    def TriggerPrices(self, value: System.Collections.Generic.List[float]):
        ...


class Instrument:
    """Instrument structure"""

    @property
    def InstrumentToken(self) -> int:
        ...

    @InstrumentToken.setter
    def InstrumentToken(self, value: int):
        ...

    @property
    def ExchangeToken(self) -> int:
        ...

    @ExchangeToken.setter
    def ExchangeToken(self, value: int):
        ...

    @property
    def TradingSymbol(self) -> str:
        ...

    @TradingSymbol.setter
    def TradingSymbol(self, value: str):
        ...

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def LastPrice(self) -> float:
        ...

    @LastPrice.setter
    def LastPrice(self, value: float):
        ...

    @property
    def TickSize(self) -> float:
        ...

    @TickSize.setter
    def TickSize(self, value: float):
        ...

    @property
    def Expiry(self) -> typing.Optional[datetime.datetime]:
        ...

    @Expiry.setter
    def Expiry(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def InstrumentType(self) -> str:
        ...

    @InstrumentType.setter
    def InstrumentType(self, value: str):
        ...

    @property
    def Segment(self) -> str:
        ...

    @Segment.setter
    def Segment(self, value: str):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def Strike(self) -> float:
        ...

    @Strike.setter
    def Strike(self, value: float):
        ...

    @property
    def LotSize(self) -> int:
        ...

    @LotSize.setter
    def LotSize(self, value: int):
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class CsvInstrument(System.Object):
    """Instrument structure"""

    @property
    def InstrumentToken(self) -> int:
        ...

    @InstrumentToken.setter
    def InstrumentToken(self, value: int):
        ...

    @property
    def ExchangeToken(self) -> int:
        ...

    @ExchangeToken.setter
    def ExchangeToken(self, value: int):
        ...

    @property
    def TradingSymbol(self) -> str:
        ...

    @TradingSymbol.setter
    def TradingSymbol(self, value: str):
        ...

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def LastPrice(self) -> float:
        ...

    @LastPrice.setter
    def LastPrice(self, value: float):
        ...

    @property
    def TickSize(self) -> float:
        ...

    @TickSize.setter
    def TickSize(self, value: float):
        ...

    @property
    def Expiry(self) -> typing.Optional[datetime.datetime]:
        ...

    @Expiry.setter
    def Expiry(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def InstrumentType(self) -> str:
        ...

    @InstrumentType.setter
    def InstrumentType(self, value: str):
        ...

    @property
    def Segment(self) -> str:
        ...

    @Segment.setter
    def Segment(self, value: str):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def Strike(self) -> float:
        ...

    @Strike.setter
    def Strike(self, value: float):
        ...

    @property
    def LotSize(self) -> int:
        ...

    @LotSize.setter
    def LotSize(self, value: int):
        ...


class Trade:
    """Trade structure"""

    @property
    def TradeId(self) -> str:
        ...

    @property
    def OrderId(self) -> str:
        ...

    @property
    def ExchangeOrderId(self) -> str:
        ...

    @property
    def Tradingsymbol(self) -> str:
        ...

    @property
    def Exchange(self) -> str:
        ...

    @property
    def InstrumentToken(self) -> int:
        ...

    @property
    def TransactionType(self) -> str:
        ...

    @property
    def Product(self) -> str:
        ...

    @property
    def AveragePrice(self) -> float:
        ...

    @property
    def Quantity(self) -> int:
        ...

    @property
    def FillTimestamp(self) -> typing.Optional[datetime.datetime]:
        ...

    @property
    def ExchangeTimestamp(self) -> typing.Optional[datetime.datetime]:
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class TrigerRange:
    """Trigger range structure"""

    @property
    def InstrumentToken(self) -> int:
        ...

    @property
    def Lower(self) -> float:
        ...

    @property
    def Upper(self) -> float:
        ...

    @property
    def Percentage(self) -> float:
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class User:
    """User structure"""

    @property
    def APIKey(self) -> str:
        ...

    @property
    def Products(self) -> typing.List[str]:
        ...

    @property
    def UserName(self) -> str:
        ...

    @property
    def UserShortName(self) -> str:
        ...

    @property
    def AvatarURL(self) -> str:
        ...

    @property
    def Broker(self) -> str:
        ...

    @property
    def AccessToken(self) -> str:
        ...

    @property
    def PublicToken(self) -> str:
        ...

    @property
    def RefreshToken(self) -> str:
        ...

    @property
    def UserType(self) -> str:
        ...

    @property
    def UserId(self) -> str:
        ...

    @property
    def LoginTime(self) -> typing.Optional[datetime.datetime]:
        ...

    @property
    def Exchanges(self) -> typing.List[str]:
        ...

    @property
    def OrderTypes(self) -> typing.List[str]:
        ...

    @property
    def Email(self) -> str:
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class TokenSet:
    """This class has no documentation."""

    @property
    def UserId(self) -> str:
        ...

    @property
    def AccessToken(self) -> str:
        ...

    @property
    def RefreshToken(self) -> str:
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class Profile:
    """User structure"""

    @property
    def Products(self) -> typing.List[str]:
        ...

    @property
    def UserName(self) -> str:
        ...

    @property
    def UserShortName(self) -> str:
        ...

    @property
    def AvatarURL(self) -> str:
        ...

    @property
    def Broker(self) -> str:
        ...

    @property
    def UserType(self) -> str:
        ...

    @property
    def Exchanges(self) -> typing.List[str]:
        ...

    @property
    def OrderTypes(self) -> typing.List[str]:
        ...

    @property
    def Email(self) -> str:
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class Quote:
    """Quote structure"""

    @property
    def InstrumentToken(self) -> int:
        ...

    @InstrumentToken.setter
    def InstrumentToken(self, value: int):
        ...

    @property
    def LastPrice(self) -> float:
        ...

    @LastPrice.setter
    def LastPrice(self, value: float):
        ...

    @property
    def LastQuantity(self) -> int:
        ...

    @LastQuantity.setter
    def LastQuantity(self, value: int):
        ...

    @property
    def AveragePrice(self) -> float:
        ...

    @AveragePrice.setter
    def AveragePrice(self, value: float):
        ...

    @property
    def Volume(self) -> int:
        ...

    @Volume.setter
    def Volume(self, value: int):
        ...

    @property
    def BuyQuantity(self) -> int:
        ...

    @BuyQuantity.setter
    def BuyQuantity(self, value: int):
        ...

    @property
    def SellQuantity(self) -> int:
        ...

    @SellQuantity.setter
    def SellQuantity(self, value: int):
        ...

    @property
    def Open(self) -> float:
        ...

    @Open.setter
    def Open(self, value: float):
        ...

    @property
    def High(self) -> float:
        ...

    @High.setter
    def High(self, value: float):
        ...

    @property
    def Low(self) -> float:
        ...

    @Low.setter
    def Low(self, value: float):
        ...

    @property
    def Close(self) -> float:
        ...

    @Close.setter
    def Close(self, value: float):
        ...

    @property
    def Change(self) -> float:
        ...

    @Change.setter
    def Change(self, value: float):
        ...

    @property
    def LowerCircuitLimit(self) -> float:
        ...

    @LowerCircuitLimit.setter
    def LowerCircuitLimit(self, value: float):
        ...

    @property
    def UpperCircuitLimit(self) -> float:
        ...

    @UpperCircuitLimit.setter
    def UpperCircuitLimit(self, value: float):
        ...

    @property
    def Bids(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.DepthItem]:
        ...

    @Bids.setter
    def Bids(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.DepthItem]):
        ...

    @property
    def Offers(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.DepthItem]:
        ...

    @Offers.setter
    def Offers(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Zerodha.Messages.DepthItem]):
        ...

    @property
    def LastTradeTime(self) -> typing.Optional[datetime.datetime]:
        ...

    @LastTradeTime.setter
    def LastTradeTime(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def OI(self) -> int:
        ...

    @OI.setter
    def OI(self, value: int):
        ...

    @property
    def OIDayHigh(self) -> int:
        ...

    @OIDayHigh.setter
    def OIDayHigh(self, value: int):
        ...

    @property
    def OIDayLow(self) -> int:
        ...

    @OIDayLow.setter
    def OIDayLow(self, value: int):
        ...

    @property
    def Timestamp(self) -> typing.Optional[datetime.datetime]:
        ...

    @Timestamp.setter
    def Timestamp(self, value: typing.Optional[datetime.datetime]):
        ...

    def __init__(self, data: typing.Any) -> None:
        ...


class OHLC:
    """OHLC Quote structure"""

    @property
    def InstrumentToken(self) -> int:
        ...

    @InstrumentToken.setter
    def InstrumentToken(self, value: int):
        ...

    @property
    def LastPrice(self) -> float:
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

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


class LTP:
    """LTP Quote structure"""

    @property
    def InstrumentToken(self) -> int:
        ...

    @InstrumentToken.setter
    def InstrumentToken(self, value: int):
        ...

    @property
    def LastPrice(self) -> float:
        ...

    def __init__(self, data: System.Collections.Generic.Dictionary[str, typing.Any]) -> None:
        ...


