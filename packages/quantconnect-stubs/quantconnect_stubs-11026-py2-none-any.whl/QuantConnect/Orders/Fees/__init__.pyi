import abc
import datetime

import QuantConnect.Orders
import QuantConnect.Orders.Fees
import QuantConnect.Securities
import System


class OrderFee(System.Object):
    """Defines the result for IFeeModel.GetOrderFee"""

    @property
    def Value(self) -> QuantConnect.Securities.CashAmount:
        """Gets the order fee"""
        ...

    @Value.setter
    def Value(self, value: QuantConnect.Securities.CashAmount):
        """Gets the order fee"""
        ...

    Zero: QuantConnect.Orders.Fees.OrderFee = ...
    """Gets an instance of OrderFee that represents zero."""

    def __init__(self, orderFee: QuantConnect.Securities.CashAmount) -> None:
        """
        Initializes a new instance of the OrderFee class
        
        :param orderFee: The order fee
        """
        ...

    def ApplyToPortfolio(self, portfolio: QuantConnect.Securities.SecurityPortfolioManager, fill: QuantConnect.Orders.OrderEvent) -> None:
        """
        Applies the order fee to the given portfolio
        
        :param portfolio: The portfolio instance
        :param fill: The order fill event
        """
        ...

    def ToString(self) -> str:
        """This is for backward compatibility with old 'decimal' order fee"""
        ...


class OrderFeeParameters(System.Object):
    """Defines the parameters for IFeeModel.GetOrderFee"""

    @property
    def Security(self) -> QuantConnect.Securities.Security:
        """Gets the security"""
        ...

    @property
    def Order(self) -> QuantConnect.Orders.Order:
        """Gets the order"""
        ...

    def __init__(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> None:
        """
        Initializes a new instance of the OrderFeeParameters class
        
        :param security: The security
        :param order: The order
        """
        ...


class IFeeModel(metaclass=abc.ABCMeta):
    """Represents a model the simulates order fees"""

    def GetOrderFee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Gets the order fee associated with the specified order.
        
        :param parameters: A OrderFeeParameters object containing the security and order
        :returns: The cost of the order in a CashAmount instance.
        """
        ...


class FeeModelExtensions(System.Object):
    """
    Provide extension method for IFeeModel to enable
    backwards compatibility of invocations.
    """

    @staticmethod
    def GetOrderFee(model: QuantConnect.Orders.Fees.IFeeModel, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> float:
        """
        Gets the order fee associated with the specified order. This returns the cost
        of the transaction in the account currency
        
        :param model: The fee model
        :param security: The security matching the order
        :param order: The order to compute fees for
        :returns: The cost of the order in units of the account currency.
        """
        ...


class FeeModel(System.Object, QuantConnect.Orders.Fees.IFeeModel):
    """Base class for any order fee model"""

    def GetOrderFee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Gets the order fee associated with the specified order.
        
        :param parameters: A OrderFeeParameters object containing the security and order
        :returns: The cost of the order in a CashAmount instance.
        """
        ...


class FxcmFeeModel(QuantConnect.Orders.Fees.FeeModel):
    """Provides an implementation of FeeModel that models FXCM order fees"""

    def __init__(self, currency: str = "USD") -> None:
        """
        Creates a new instance
        
        :param currency: The currency of the order fee, for FXCM this is the account currency
        """
        ...

    def GetOrderFee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Get the fee for this order in units of the account currency
        
        :param parameters: A OrderFeeParameters object containing the security and order
        :returns: The cost of the order in units of the account currency.
        """
        ...


class AtreyuFeeModel(System.Object, QuantConnect.Orders.Fees.IFeeModel):
    """Provides an implementation of FeeModel that models Atreyu order fees"""

    def GetOrderFee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Get the fee for this order in quote currency
        
        :param parameters: A OrderFeeParameters object containing the security and order
        :returns: The cost of the order in quote currency.
        """
        ...


class GDAXFeeModel(QuantConnect.Orders.Fees.FeeModel):
    """Provides an implementation of FeeModel that models GDAX order fees"""

    def GetOrderFee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Get the fee for this order in quote currency
        
        :param parameters: A OrderFeeParameters object containing the security and order
        :returns: The cost of the order in quote currency.
        """
        ...

    @staticmethod
    def GetFeePercentage(utcTime: datetime.datetime, isMaker: bool) -> float:
        """
        Returns the maker/taker fee percentage effective at the requested date.
        
        :param utcTime: The date/time requested (UTC)
        :param isMaker: true if the maker percentage fee is requested, false otherwise
        :returns: The fee percentage effective at the requested date.
        """
        ...


class InteractiveBrokersFeeModel(QuantConnect.Orders.Fees.FeeModel):
    """Provides the default implementation of IFeeModel"""

    def __init__(self, monthlyForexTradeAmountInUSDollars: float = 0, monthlyOptionsTradeAmountInContracts: float = 0) -> None:
        """
        Initializes a new instance of the ImmediateFillModel
        
        :param monthlyForexTradeAmountInUSDollars: Monthly FX dollar volume traded
        :param monthlyOptionsTradeAmountInContracts: Monthly options contracts traded
        """
        ...

    def GetOrderFee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Gets the order fee associated with the specified order. This returns the cost
        of the transaction in the account currency
        
        :param parameters: A OrderFeeParameters object containing the security and order
        :returns: The cost of the order in units of the account currency.
        """
        ...


class ConstantFeeModel(QuantConnect.Orders.Fees.FeeModel):
    """Provides an order fee model that always returns the same order fee."""

    def __init__(self, fee: float, currency: str = "USD") -> None:
        """
        Initializes a new instance of the ConstantFeeModel class with the specified
        
        :param fee: The constant order fee used by the model
        :param currency: The currency of the order fee
        """
        ...

    def GetOrderFee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Returns the constant fee for the model in units of the account currency
        
        :param parameters: A OrderFeeParameters object containing the security and order
        :returns: The cost of the order in units of the account currency.
        """
        ...


class ModifiedFillQuantityOrderFee(QuantConnect.Orders.Fees.OrderFee):
    """An order fee where the fee quantity has already been subtracted from the filled quantity"""

    def __init__(self, orderFee: QuantConnect.Securities.CashAmount) -> None:
        """
        Initializes a new instance of the ModifiedFillQuantityOrderFee class
        
        :param orderFee: The order fee
        """
        ...

    def ApplyToPortfolio(self, portfolio: QuantConnect.Securities.SecurityPortfolioManager, fill: QuantConnect.Orders.OrderEvent) -> None:
        """
        Applies the order fee to the given portfolio
        
        :param portfolio: The portfolio instance
        :param fill: The order fill event
        """
        ...


class BinanceFeeModel(QuantConnect.Orders.Fees.FeeModel):
    """Provides an implementation of FeeModel that models Binance order fees"""

    MakerTier1Fee: float = 0.001
    """
    Tier 1 maker fees
    https://www.binance.com/en/fee/schedule
    """

    TakerTier1Fee: float = 0.001
    """
    Tier 1 taker fees
    https://www.binance.com/en/fee/schedule
    """

    def __init__(self, mFee: float = ..., tFee: float = ...) -> None:
        """
        Creates Binance fee model setting fees values
        
        :param mFee: Maker fee value
        :param tFee: Taker fee value
        """
        ...

    def GetOrderFee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Get the fee for this order in quote currency
        
        :param parameters: A OrderFeeParameters object containing the security and order
        :returns: The cost of the order in quote currency.
        """
        ...


class BitfinexFeeModel(QuantConnect.Orders.Fees.FeeModel):
    """Provides an implementation of FeeModel that models Bitfinex order fees"""

    MakerFee: float = 0.001
    """
    Tier 1 maker fees
    Maker fees are paid when you add liquidity to our order book by placing a limit order under the ticker price for buy and above the ticker price for sell.
    https://www.bitfinex.com/fees
    """

    TakerFee: float = 0.002
    """
    Tier 1 taker fees
    Taker fees are paid when you remove liquidity from our order book by placing any order that is executed against an order of the order book.
    Note: If you place a hidden order, you will always pay the taker fee. If you place a limit order that hits a hidden order, you will always pay the maker fee.
    https://www.bitfinex.com/fees
    """

    def GetOrderFee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Get the fee for this order in quote currency
        
        :param parameters: A OrderFeeParameters object containing the security and order
        :returns: The cost of the order in quote currency.
        """
        ...


class AlphaStreamsFeeModel(QuantConnect.Orders.Fees.FeeModel):
    """Provides an implementation of FeeModel that models order fees that alpha stream clients pay/receive"""

    def GetOrderFee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Gets the order fee associated with the specified order. This returns the cost
        of the transaction in the account currency
        
        :param parameters: A OrderFeeParameters object containing the security and order
        :returns: The cost of the order in units of the account currency.
        """
        ...


