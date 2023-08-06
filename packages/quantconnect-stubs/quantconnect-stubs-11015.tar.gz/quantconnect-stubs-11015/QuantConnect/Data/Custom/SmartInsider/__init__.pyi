import abc
import datetime
import typing

import QuantConnect.Data
import QuantConnect.Data.Custom.SmartInsider
import System


class SmartInsiderExecutionEntity(System.Enum):
    """Entity that intends to or executed the transaction"""

    Issuer = 0
    """Issuer of the stock"""

    Subsidiary = 1
    """Subsidiary of the issuer"""

    Broker = 2
    """
    Brokers are commonly used to repurchase shares under mandate to avoid insider
    information rules and to allow repurchases to carry on through close periods
    """

    EmployerBenefitTrust = 3
    """Unknown - Transaction"""

    EmployeeBenefitTrust = 4
    """To cater for shares which will need to be transferred to employees as part of remunerative plans"""

    ThirdParty = 5
    """Undisclosed independent third party. Likely to be a broker."""

    Error = 6
    """The field was not found in this enum"""


class SmartInsiderEventType(System.Enum):
    """Describes what will or has taken place in an execution"""

    Authorization = 0
    """Notification that the board has gained the authority to repurchase"""

    Intention = 1
    """Notification of the board that shares will be repurchased."""

    Transaction = 2
    """Repurchase transactions that have been actioned."""

    UpwardsRevision = 3
    """Increase in the scope of the existing plan (extended date, increased value, etc.)"""

    DownwardsRevision = 4
    """Decrease in the scope of the existing plan (shortened date, reduced value, etc.)"""

    RevisedDetails = 5
    """General change of details of the plan (max/min price alteration, etc.)"""

    Cancellation = 6
    """Total cancellation of the plan"""

    SeekAuthorization = 7
    """Announcement by a company that the board of directors or management will be seeking to obtain authorisation for a repurchase plan."""

    PlanSuspension = 8
    """Announcement by a company that a plan of repurchase has been suspended. Further details of the suspension are included in the note."""

    PlanReStarted = 9
    """Announcement by a company that a suspended plan has been re-started. Further details of the suspension are included in the note."""

    NotSpecified = 10
    """Announcement by a company not specified and/or not documented in the other categories. Further details are included in the note."""


class SmartInsiderEvent(QuantConnect.Data.BaseData, metaclass=abc.ABCMeta):
    """
    SmartInsider Intention and Transaction events. These are fields
    that are shared between intentions and transactions.
    """

    @property
    def TransactionID(self) -> str:
        """Proprietary unique field. Not nullable"""
        ...

    @TransactionID.setter
    def TransactionID(self, value: str):
        """Proprietary unique field. Not nullable"""
        ...

    @property
    def EventType(self) -> typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderEventType]:
        """Description of what has or will take place in an execution"""
        ...

    @EventType.setter
    def EventType(self, value: typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderEventType]):
        """Description of what has or will take place in an execution"""
        ...

    @property
    def LastUpdate(self) -> datetime.datetime:
        """The date when a transaction is updated after it has been reported. Not nullable"""
        ...

    @LastUpdate.setter
    def LastUpdate(self, value: datetime.datetime):
        """The date when a transaction is updated after it has been reported. Not nullable"""
        ...

    @property
    def LastIDsUpdate(self) -> typing.Optional[datetime.datetime]:
        ...

    @LastIDsUpdate.setter
    def LastIDsUpdate(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def ISIN(self) -> str:
        """Industry classification number"""
        ...

    @ISIN.setter
    def ISIN(self, value: str):
        """Industry classification number"""
        ...

    @property
    def USDMarketCap(self) -> typing.Optional[float]:
        """The market capitalization at the time of the transaction stated in US Dollars"""
        ...

    @USDMarketCap.setter
    def USDMarketCap(self, value: typing.Optional[float]):
        """The market capitalization at the time of the transaction stated in US Dollars"""
        ...

    @property
    def CompanyID(self) -> typing.Optional[int]:
        """Smart Insider proprietary identifier for the company"""
        ...

    @CompanyID.setter
    def CompanyID(self, value: typing.Optional[int]):
        """Smart Insider proprietary identifier for the company"""
        ...

    @property
    def ICBIndustry(self) -> str:
        """FTSE Russell Sector Classification"""
        ...

    @ICBIndustry.setter
    def ICBIndustry(self, value: str):
        """FTSE Russell Sector Classification"""
        ...

    @property
    def ICBSuperSector(self) -> str:
        """FTSE Russell Sector Classification"""
        ...

    @ICBSuperSector.setter
    def ICBSuperSector(self, value: str):
        """FTSE Russell Sector Classification"""
        ...

    @property
    def ICBSector(self) -> str:
        """FTSE Russell Sector Classification"""
        ...

    @ICBSector.setter
    def ICBSector(self, value: str):
        """FTSE Russell Sector Classification"""
        ...

    @property
    def ICBSubSector(self) -> str:
        """FTSE Russell Sector Classification"""
        ...

    @ICBSubSector.setter
    def ICBSubSector(self, value: str):
        """FTSE Russell Sector Classification"""
        ...

    @property
    def ICBCode(self) -> typing.Optional[int]:
        """Numeric code that is the most granular level in ICB classification"""
        ...

    @ICBCode.setter
    def ICBCode(self, value: typing.Optional[int]):
        """Numeric code that is the most granular level in ICB classification"""
        ...

    @property
    def CompanyName(self) -> str:
        """Company name. PLC is always excluded"""
        ...

    @CompanyName.setter
    def CompanyName(self, value: str):
        """Company name. PLC is always excluded"""
        ...

    @property
    def PreviousResultsAnnouncementDate(self) -> typing.Optional[datetime.datetime]:
        """Announcement date of last results, this will be the end date of the last "Close Period\""""
        ...

    @PreviousResultsAnnouncementDate.setter
    def PreviousResultsAnnouncementDate(self, value: typing.Optional[datetime.datetime]):
        """Announcement date of last results, this will be the end date of the last "Close Period\""""
        ...

    @property
    def NextResultsAnnouncementsDate(self) -> typing.Optional[datetime.datetime]:
        """Announcement date of next results, this will be the end date of the next "Close Period\""""
        ...

    @NextResultsAnnouncementsDate.setter
    def NextResultsAnnouncementsDate(self, value: typing.Optional[datetime.datetime]):
        """Announcement date of next results, this will be the end date of the next "Close Period\""""
        ...

    @property
    def NextCloseBegin(self) -> typing.Optional[datetime.datetime]:
        """Start date of next trading embargo ahead of scheduled results announcment"""
        ...

    @NextCloseBegin.setter
    def NextCloseBegin(self, value: typing.Optional[datetime.datetime]):
        """Start date of next trading embargo ahead of scheduled results announcment"""
        ...

    @property
    def LastCloseEnded(self) -> typing.Optional[datetime.datetime]:
        """Date trading embargo (Close Period) is lifted as results are made public"""
        ...

    @LastCloseEnded.setter
    def LastCloseEnded(self, value: typing.Optional[datetime.datetime]):
        """Date trading embargo (Close Period) is lifted as results are made public"""
        ...

    @property
    def SecurityDescription(self) -> str:
        """Type of security. Does not contain nominal value"""
        ...

    @SecurityDescription.setter
    def SecurityDescription(self, value: str):
        """Type of security. Does not contain nominal value"""
        ...

    @property
    def TickerCountry(self) -> str:
        """Country of local identifier, denoting where the trade took place"""
        ...

    @TickerCountry.setter
    def TickerCountry(self, value: str):
        """Country of local identifier, denoting where the trade took place"""
        ...

    @property
    def TickerSymbol(self) -> str:
        """Local market identifier"""
        ...

    @TickerSymbol.setter
    def TickerSymbol(self, value: str):
        """Local market identifier"""
        ...

    @property
    def AnnouncementDate(self) -> typing.Optional[datetime.datetime]:
        """Date Transaction was entered onto our system. Where a transaction is after the London market close (usually 4.30pm) this will be stated as the next day"""
        ...

    @AnnouncementDate.setter
    def AnnouncementDate(self, value: typing.Optional[datetime.datetime]):
        """Date Transaction was entered onto our system. Where a transaction is after the London market close (usually 4.30pm) this will be stated as the next day"""
        ...

    @property
    def TimeReleased(self) -> typing.Optional[datetime.datetime]:
        """Time the announcement first appeared on a Regulatory News Service or other disclosure system and became available to the market, time stated is local market time"""
        ...

    @TimeReleased.setter
    def TimeReleased(self, value: typing.Optional[datetime.datetime]):
        """Time the announcement first appeared on a Regulatory News Service or other disclosure system and became available to the market, time stated is local market time"""
        ...

    @property
    def TimeProcessed(self) -> typing.Optional[datetime.datetime]:
        """Time the transaction was entered into Smart Insider systems and appeared on their website, time stated is local to London, UK"""
        ...

    @TimeProcessed.setter
    def TimeProcessed(self, value: typing.Optional[datetime.datetime]):
        """Time the transaction was entered into Smart Insider systems and appeared on their website, time stated is local to London, UK"""
        ...

    @property
    def TimeReleasedUtc(self) -> typing.Optional[datetime.datetime]:
        """Time the announcement first appeared on a Regulatory News Service or other disclosure system and became available to the market. Time stated is GMT standard"""
        ...

    @TimeReleasedUtc.setter
    def TimeReleasedUtc(self, value: typing.Optional[datetime.datetime]):
        """Time the announcement first appeared on a Regulatory News Service or other disclosure system and became available to the market. Time stated is GMT standard"""
        ...

    @property
    def TimeProcessedUtc(self) -> typing.Optional[datetime.datetime]:
        """Time the transaction was entered onto our systems and appeared on our website. Time stated is GMT standard"""
        ...

    @TimeProcessedUtc.setter
    def TimeProcessedUtc(self, value: typing.Optional[datetime.datetime]):
        """Time the transaction was entered onto our systems and appeared on our website. Time stated is GMT standard"""
        ...

    @property
    def AnnouncedIn(self) -> str:
        """Market in which the transaction was announced, this can reference more than one country"""
        ...

    @AnnouncedIn.setter
    def AnnouncedIn(self, value: str):
        """Market in which the transaction was announced, this can reference more than one country"""
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, tsvLine: str) -> None:
        """
        Parses a line of TSV (tab delimited) from Smart Insider data
        
        :param tsvLine: Tab delimited line of data
        """
        ...

    def ToLine(self) -> str:
        """
        Converts data to TSV
        
        :returns: String of TSV.
        """
        ...

    def FromRawData(self, line: str) -> None:
        """
        Derived class instances populate their fields from raw TSV
        
        :param line: Line of raw TSV (raw with fields 46, 36, 14, 7 removed in descending order)
        """
        ...

    def DataTimeZone(self) -> typing.Any:
        """
        Specifies the timezone of this data source
        
        :returns: Timezone.
        """
        ...

    @staticmethod
    def ParseDate(date: str) -> datetime.datetime:
        """
        Attempts to normalize and parse SmartInsider dates that include a time component.
        
        :param date: Date string to parse
        :returns: DateTime object.
        """
        ...


class SmartInsiderExecution(System.Enum):
    """Describes how the transaction was executed"""

    Market = 0
    """Took place via the open market"""

    TenderOffer = 1
    """Via a companywide tender offer to all shareholders"""

    OffMarket = 2
    """Under a specific agreement between the issuer and shareholder"""

    Error = 3
    """Field is not in this enum"""


class SmartInsiderExecutionHolding(System.Enum):
    """Details regarding the way holdings will be or were processed in a buyback execution"""

    Treasury = 0
    """Held in treasury until they are sold back to the market"""

    Cancellation = 1
    """Immediately cancelled"""

    Trust = 2
    """Held in trust, generally to cover employee renumerative plans"""

    SatisfyEmployeeTax = 3
    """Shares will be used to satisfy employee tax liabilities"""

    NotReported = 4
    """Not disclosed by the issuer in the announcements"""

    SatisfyStockVesting = 5
    """Shares will be used to satisfy vesting of employee stock"""

    Error = 6
    """The field was not found in the enum, or is representative of a SatisfyStockVesting entry."""


class SmartInsiderIntention(QuantConnect.Data.Custom.SmartInsider.SmartInsiderEvent):
    """Smart Insider Intentions - Intention to execute a stock buyback and details about the future event"""

    @property
    def Execution(self) -> typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecution]:
        """Describes how the transaction was executed"""
        ...

    @Execution.setter
    def Execution(self, value: typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecution]):
        """Describes how the transaction was executed"""
        ...

    @property
    def ExecutionEntity(self) -> typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecutionEntity]:
        """Describes which entity intends to execute the transaction"""
        ...

    @ExecutionEntity.setter
    def ExecutionEntity(self, value: typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecutionEntity]):
        """Describes which entity intends to execute the transaction"""
        ...

    @property
    def ExecutionHolding(self) -> typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecutionHolding]:
        """Describes what will be done with those shares following repurchase"""
        ...

    @ExecutionHolding.setter
    def ExecutionHolding(self, value: typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecutionHolding]):
        """Describes what will be done with those shares following repurchase"""
        ...

    @property
    def Amount(self) -> typing.Optional[int]:
        """Number of shares to be or authorised to be traded"""
        ...

    @Amount.setter
    def Amount(self, value: typing.Optional[int]):
        """Number of shares to be or authorised to be traded"""
        ...

    @property
    def ValueCurrency(self) -> str:
        """Currency of the value of shares to be/Authorised to be traded (ISO Code)"""
        ...

    @ValueCurrency.setter
    def ValueCurrency(self, value: str):
        """Currency of the value of shares to be/Authorised to be traded (ISO Code)"""
        ...

    @property
    def AmountValue(self) -> typing.Optional[int]:
        """Value of shares to be authorised to be traded"""
        ...

    @AmountValue.setter
    def AmountValue(self, value: typing.Optional[int]):
        """Value of shares to be authorised to be traded"""
        ...

    @property
    def Percentage(self) -> typing.Optional[float]:
        """Percentage of oustanding shares to be authorised to be traded"""
        ...

    @Percentage.setter
    def Percentage(self, value: typing.Optional[float]):
        """Percentage of oustanding shares to be authorised to be traded"""
        ...

    @property
    def AuthorizationStartDate(self) -> typing.Optional[datetime.datetime]:
        """start of the period the intention/authorisation applies to"""
        ...

    @AuthorizationStartDate.setter
    def AuthorizationStartDate(self, value: typing.Optional[datetime.datetime]):
        """start of the period the intention/authorisation applies to"""
        ...

    @property
    def AuthorizationEndDate(self) -> typing.Optional[datetime.datetime]:
        """End of the period the intention/authorisation applies to"""
        ...

    @AuthorizationEndDate.setter
    def AuthorizationEndDate(self, value: typing.Optional[datetime.datetime]):
        """End of the period the intention/authorisation applies to"""
        ...

    @property
    def PriceCurrency(self) -> str:
        """Currency of min/max prices (ISO Code)"""
        ...

    @PriceCurrency.setter
    def PriceCurrency(self, value: str):
        """Currency of min/max prices (ISO Code)"""
        ...

    @property
    def MinimumPrice(self) -> typing.Optional[float]:
        """Minimum price shares will or may be purchased at"""
        ...

    @MinimumPrice.setter
    def MinimumPrice(self, value: typing.Optional[float]):
        """Minimum price shares will or may be purchased at"""
        ...

    @property
    def MaximumPrice(self) -> typing.Optional[float]:
        """Maximum price shares will or may be purchased at"""
        ...

    @MaximumPrice.setter
    def MaximumPrice(self, value: typing.Optional[float]):
        """Maximum price shares will or may be purchased at"""
        ...

    @property
    def NoteText(self) -> str:
        """Free text which explains further details about the trade"""
        ...

    @NoteText.setter
    def NoteText(self, value: str):
        """Free text which explains further details about the trade"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Empty constructor required for Slice.Get{T}()"""
        ...

    @typing.overload
    def __init__(self, line: str) -> None:
        """
        Constructs instance of this via a *formatted* TSV line (tab delimited)
        
        :param line: Line of formatted TSV data
        """
        ...

    def FromRawData(self, line: str) -> None:
        """
        Constructs a new instance from unformatted TSV data
        
        :param line: Line of raw TSV (raw with fields 46, 36, 14, 7 removed in descending order)
        :returns: Instance of the object.
        """
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
        Loads and reads the data to be used in LEAN
        
        :param config: Subscription configuration
        :param line: TSV line
        :param date: Algorithm date
        :param isLiveMode: Is live mode
        :returns: Instance of the object.
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Clones the object to a new instance. This method
        is required for custom data sources that make use
        of properties with more complex types since otherwise
        the values will default to null using the default clone method
        
        :returns: A new cloned instance of this object.
        """
        ...

    def ToLine(self) -> str:
        """
        Converts the data to TSV
        
        :returns: String of TSV.
        """
        ...


class SmartInsiderTransaction(QuantConnect.Data.Custom.SmartInsider.SmartInsiderEvent):
    """Smart Insider Transaction - Execution of a stock buyback and details about the event occurred"""

    @property
    def BuybackDate(self) -> typing.Optional[datetime.datetime]:
        """Date traded through the market"""
        ...

    @BuybackDate.setter
    def BuybackDate(self, value: typing.Optional[datetime.datetime]):
        """Date traded through the market"""
        ...

    @property
    def Execution(self) -> typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecution]:
        """Describes how transaction was executed"""
        ...

    @Execution.setter
    def Execution(self, value: typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecution]):
        """Describes how transaction was executed"""
        ...

    @property
    def ExecutionEntity(self) -> typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecutionEntity]:
        """Describes which entity carried out the transaction"""
        ...

    @ExecutionEntity.setter
    def ExecutionEntity(self, value: typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecutionEntity]):
        """Describes which entity carried out the transaction"""
        ...

    @property
    def ExecutionHolding(self) -> typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecutionHolding]:
        """Describes what will be done with those shares following repurchase"""
        ...

    @ExecutionHolding.setter
    def ExecutionHolding(self, value: typing.Optional[QuantConnect.Data.Custom.SmartInsider.SmartInsiderExecutionHolding]):
        """Describes what will be done with those shares following repurchase"""
        ...

    @property
    def Currency(self) -> str:
        """Currency of transation (ISO Code)"""
        ...

    @Currency.setter
    def Currency(self, value: str):
        """Currency of transation (ISO Code)"""
        ...

    @property
    def ExecutionPrice(self) -> typing.Optional[float]:
        """Denominated in Currency of Transaction"""
        ...

    @ExecutionPrice.setter
    def ExecutionPrice(self, value: typing.Optional[float]):
        """Denominated in Currency of Transaction"""
        ...

    @property
    def Amount(self) -> typing.Optional[float]:
        """Number of shares traded"""
        ...

    @Amount.setter
    def Amount(self, value: typing.Optional[float]):
        """Number of shares traded"""
        ...

    @property
    def GBPValue(self) -> typing.Optional[float]:
        """Currency conversion rates are updated daily and values are calculated at rate prevailing on the trade date"""
        ...

    @GBPValue.setter
    def GBPValue(self, value: typing.Optional[float]):
        """Currency conversion rates are updated daily and values are calculated at rate prevailing on the trade date"""
        ...

    @property
    def EURValue(self) -> typing.Optional[float]:
        """Currency conversion rates are updated daily and values are calculated at rate prevailing on the trade date"""
        ...

    @EURValue.setter
    def EURValue(self, value: typing.Optional[float]):
        """Currency conversion rates are updated daily and values are calculated at rate prevailing on the trade date"""
        ...

    @property
    def USDValue(self) -> typing.Optional[float]:
        """Currency conversion rates are updated daily and values are calculated at rate prevailing on the trade date"""
        ...

    @USDValue.setter
    def USDValue(self, value: typing.Optional[float]):
        """Currency conversion rates are updated daily and values are calculated at rate prevailing on the trade date"""
        ...

    @property
    def NoteText(self) -> str:
        """Free text which expains futher details about the trade"""
        ...

    @NoteText.setter
    def NoteText(self, value: str):
        """Free text which expains futher details about the trade"""
        ...

    @property
    def BuybackPercentage(self) -> typing.Optional[float]:
        """Percentage of value of the trade as part of the issuers total Market Cap"""
        ...

    @BuybackPercentage.setter
    def BuybackPercentage(self, value: typing.Optional[float]):
        """Percentage of value of the trade as part of the issuers total Market Cap"""
        ...

    @property
    def VolumePercentage(self) -> typing.Optional[float]:
        """Percentage of the volume traded on the day of the buyback."""
        ...

    @VolumePercentage.setter
    def VolumePercentage(self, value: typing.Optional[float]):
        """Percentage of the volume traded on the day of the buyback."""
        ...

    @property
    def ConversionRate(self) -> typing.Optional[float]:
        """Rate used to calculate 'Value (GBP)' from 'Price' multiplied by 'Amount'. Will be 1 where Currency is also 'GBP'"""
        ...

    @ConversionRate.setter
    def ConversionRate(self, value: typing.Optional[float]):
        """Rate used to calculate 'Value (GBP)' from 'Price' multiplied by 'Amount'. Will be 1 where Currency is also 'GBP'"""
        ...

    @property
    def AmountAdjustedFactor(self) -> typing.Optional[float]:
        """Multiplier which can be applied to 'Amount' field to account for subsequent corporate action"""
        ...

    @AmountAdjustedFactor.setter
    def AmountAdjustedFactor(self, value: typing.Optional[float]):
        """Multiplier which can be applied to 'Amount' field to account for subsequent corporate action"""
        ...

    @property
    def PriceAdjustedFactor(self) -> typing.Optional[float]:
        """Multiplier which can be applied to 'Price' and 'LastClose' fields to account for subsequent corporate actions"""
        ...

    @PriceAdjustedFactor.setter
    def PriceAdjustedFactor(self, value: typing.Optional[float]):
        """Multiplier which can be applied to 'Price' and 'LastClose' fields to account for subsequent corporate actions"""
        ...

    @property
    def TreasuryHolding(self) -> typing.Optional[int]:
        """Post trade holding of the Treasury or Trust in the security traded"""
        ...

    @TreasuryHolding.setter
    def TreasuryHolding(self, value: typing.Optional[int]):
        """Post trade holding of the Treasury or Trust in the security traded"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Empty contsructor required for Slice.Get{T}()"""
        ...

    @typing.overload
    def __init__(self, line: str) -> None:
        """
        Creates an instance of the object by taking a formatted TSV line
        
        :param line: Line of formatted TSV
        """
        ...

    def FromRawData(self, line: str) -> None:
        """
        Creates an instance of the object by taking a formatted TSV line
        
        :param line: Line of formatted TSV
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Specifies the location of the data and directs LEAN where to load the data from
        
        :param config: Subscription configuration
        :param date: Date
        :param isLiveMode: Is live mode
        :returns: Subscription data source object pointing LEAN to the data location.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reads the data into LEAN for use in algorithms
        
        :param config: Subscription configuration
        :param line: Line of TSV
        :param date: Algorithm date
        :param isLiveMode: Is live mode
        :returns: Instance of the object.
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Clones the object to a new instance. This method
        is required for custom data sources that make use
        of properties with more complex types since otherwise
        the values will default to null using the default clone method
        
        :returns: A new cloned instance of this object.
        """
        ...

    def ToLine(self) -> str:
        """
        Converts the data to TSV
        
        :returns: String of TSV.
        """
        ...


