import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Custom.SEC
import System
import System.Collections.Generic

IsoDateTimeConverter = typing.Any


class SECReportFormerCompany(System.Object):
    """This class has no documentation."""

    @property
    def FormerConformedName(self) -> str:
        """Previous company name"""
        ...

    @FormerConformedName.setter
    def FormerConformedName(self, value: str):
        """Previous company name"""
        ...

    @property
    def Changed(self) -> datetime.datetime:
        """Date the company name was changed to a new name"""
        ...

    @Changed.setter
    def Changed(self, value: datetime.datetime):
        """Date the company name was changed to a new name"""
        ...


class SECReportMailAddress(System.Object):
    """This class has no documentation."""

    @property
    def StreetOne(self) -> str:
        """Mailing street address"""
        ...

    @StreetOne.setter
    def StreetOne(self, value: str):
        """Mailing street address"""
        ...

    @property
    def StreetTwo(self) -> str:
        """Mailing street address 2"""
        ...

    @StreetTwo.setter
    def StreetTwo(self, value: str):
        """Mailing street address 2"""
        ...

    @property
    def City(self) -> str:
        """City"""
        ...

    @City.setter
    def City(self, value: str):
        """City"""
        ...

    @property
    def State(self) -> str:
        """US State"""
        ...

    @State.setter
    def State(self, value: str):
        """US State"""
        ...

    @property
    def Zip(self) -> str:
        """ZIP code. Not an integer because ZIP codes with dashes and letters exist"""
        ...

    @Zip.setter
    def Zip(self, value: str):
        """ZIP code. Not an integer because ZIP codes with dashes and letters exist"""
        ...


class SECReportDateTimeConverter(IsoDateTimeConverter):
    """Specifies format for parsing DateTime values from SEC data"""

    def __init__(self) -> None:
        ...


class SECReportCompanyData(System.Object):
    """This class has no documentation."""

    @property
    def ConformedName(self) -> str:
        """Current company name"""
        ...

    @ConformedName.setter
    def ConformedName(self, value: str):
        """Current company name"""
        ...

    @property
    def Cik(self) -> str:
        """Company's Central Index Key. Used to uniquely identify company filings in SEC's EDGAR system"""
        ...

    @Cik.setter
    def Cik(self, value: str):
        """Company's Central Index Key. Used to uniquely identify company filings in SEC's EDGAR system"""
        ...

    @property
    def AssignedSic(self) -> str:
        """Standard Industrial Classification"""
        ...

    @AssignedSic.setter
    def AssignedSic(self, value: str):
        """Standard Industrial Classification"""
        ...

    @property
    def IrsNumber(self) -> str:
        """Employer Identification Number"""
        ...

    @IrsNumber.setter
    def IrsNumber(self, value: str):
        """Employer Identification Number"""
        ...

    @property
    def StateOfIncorporation(self) -> str:
        """State of incorporation"""
        ...

    @StateOfIncorporation.setter
    def StateOfIncorporation(self, value: str):
        """State of incorporation"""
        ...

    @property
    def FiscalYearEnd(self) -> str:
        """Day fiscal year ends for given company. Formatted as MMdd"""
        ...

    @FiscalYearEnd.setter
    def FiscalYearEnd(self, value: str):
        """Day fiscal year ends for given company. Formatted as MMdd"""
        ...


class SECReportFilingValues(System.Object):
    """This class has no documentation."""

    @property
    def FormType(self) -> str:
        """SEC Form Type (e.g. 10-Q, 8-K, S-1, etc.)"""
        ...

    @FormType.setter
    def FormType(self, value: str):
        """SEC Form Type (e.g. 10-Q, 8-K, S-1, etc.)"""
        ...

    @property
    def Act(self) -> str:
        """Identification of the act(s) under which certain IM filings are made. The form type may be filed under more than one act. Required in each filing values tag nest."""
        ...

    @Act.setter
    def Act(self, value: str):
        """Identification of the act(s) under which certain IM filings are made. The form type may be filed under more than one act. Required in each filing values tag nest."""
        ...

    @property
    def FileNumber(self) -> str:
        """SEC filing number"""
        ...

    @FileNumber.setter
    def FileNumber(self, value: str):
        """SEC filing number"""
        ...

    @property
    def FilmNumber(self) -> str:
        """Used to access documents in the SEC's Virtual Private Reference Room (VPRR)"""
        ...

    @FilmNumber.setter
    def FilmNumber(self, value: str):
        """Used to access documents in the SEC's Virtual Private Reference Room (VPRR)"""
        ...


class SECReportBusinessAddress(System.Object):
    """This class has no documentation."""

    @property
    def StreetOne(self) -> str:
        """Street Address 1"""
        ...

    @StreetOne.setter
    def StreetOne(self, value: str):
        """Street Address 1"""
        ...

    @property
    def StreetTwo(self) -> str:
        """Street Address 2"""
        ...

    @StreetTwo.setter
    def StreetTwo(self, value: str):
        """Street Address 2"""
        ...

    @property
    def City(self) -> str:
        """City"""
        ...

    @City.setter
    def City(self, value: str):
        """City"""
        ...

    @property
    def State(self) -> str:
        """US State"""
        ...

    @State.setter
    def State(self, value: str):
        """US State"""
        ...

    @property
    def Zip(self) -> str:
        """ZIP Code"""
        ...

    @Zip.setter
    def Zip(self, value: str):
        """ZIP Code"""
        ...

    @property
    def Phone(self) -> str:
        """Business phone number"""
        ...

    @Phone.setter
    def Phone(self, value: str):
        """Business phone number"""
        ...


class SECReportFiler(System.Object):
    """This class has no documentation."""

    @property
    def CompanyData(self) -> QuantConnect.Data.Custom.SEC.SECReportCompanyData:
        """SEC data containing company data such as company name, cik, etc."""
        ...

    @CompanyData.setter
    def CompanyData(self, value: QuantConnect.Data.Custom.SEC.SECReportCompanyData):
        """SEC data containing company data such as company name, cik, etc."""
        ...

    @property
    def Values(self) -> System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportFilingValues]:
        """Information regarding the filing itself"""
        ...

    @Values.setter
    def Values(self, value: System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportFilingValues]):
        """Information regarding the filing itself"""
        ...

    @property
    def BusinessAddress(self) -> System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportBusinessAddress]:
        """Information related to the business' address"""
        ...

    @BusinessAddress.setter
    def BusinessAddress(self, value: System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportBusinessAddress]):
        """Information related to the business' address"""
        ...

    @property
    def MailingAddress(self) -> System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportMailAddress]:
        """Company mailing address information"""
        ...

    @MailingAddress.setter
    def MailingAddress(self, value: System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportMailAddress]):
        """Company mailing address information"""
        ...

    @property
    def FormerCompanies(self) -> System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportFormerCompany]:
        """
        Former company names. Default to empty list in order to not have null values
        in the case that the company has never had a former name
        """
        ...

    @FormerCompanies.setter
    def FormerCompanies(self, value: System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportFormerCompany]):
        """
        Former company names. Default to empty list in order to not have null values
        in the case that the company has never had a former name
        """
        ...


class SECReportDocument(System.Object):
    """This class has no documentation."""

    @property
    def FormType(self) -> str:
        """Report document type, e.g. 10-Q, 8-K, S-1"""
        ...

    @FormType.setter
    def FormType(self, value: str):
        """Report document type, e.g. 10-Q, 8-K, S-1"""
        ...

    @property
    def Sequence(self) -> int:
        """Nth attachment to the form filed"""
        ...

    @Sequence.setter
    def Sequence(self, value: int):
        """Nth attachment to the form filed"""
        ...

    @property
    def Filename(self) -> str:
        """File name that the file had when it was uploaded"""
        ...

    @Filename.setter
    def Filename(self, value: str):
        """File name that the file had when it was uploaded"""
        ...

    @property
    def Description(self) -> str:
        """Attachment content(s) description"""
        ...

    @Description.setter
    def Description(self, value: str):
        """Attachment content(s) description"""
        ...

    @property
    def Text(self) -> str:
        """
        Content of the attachment. This is the field that will most likely contain
        information related to financial reports. Sometimes, XML will
        be present in the data. If the first line starts with "<XML>", then
        XML data will be present in the contents of the document
        """
        ...

    @Text.setter
    def Text(self, value: str):
        """
        Content of the attachment. This is the field that will most likely contain
        information related to financial reports. Sometimes, XML will
        be present in the data. If the first line starts with "<XML>", then
        XML data will be present in the contents of the document
        """
        ...


class SECReportSubmission(System.Object):
    """This class has no documentation."""

    @property
    def AccessionNumber(self) -> str:
        """Number used to access document filings on the SEC website"""
        ...

    @AccessionNumber.setter
    def AccessionNumber(self, value: str):
        """Number used to access document filings on the SEC website"""
        ...

    @property
    def FormType(self) -> str:
        """SEC form type"""
        ...

    @FormType.setter
    def FormType(self, value: str):
        """SEC form type"""
        ...

    @property
    def PublicDocumentCount(self) -> str:
        """Number of documents made public by the SEC"""
        ...

    @PublicDocumentCount.setter
    def PublicDocumentCount(self, value: str):
        """Number of documents made public by the SEC"""
        ...

    @property
    def Period(self) -> datetime.datetime:
        """End date of reporting period of filing. Optional."""
        ...

    @Period.setter
    def Period(self, value: datetime.datetime):
        """End date of reporting period of filing. Optional."""
        ...

    @property
    def Items(self) -> System.Collections.Generic.List[str]:
        """Identifies 1 or more items declared in 8-K filings. Optional & Repeatable."""
        ...

    @Items.setter
    def Items(self, value: System.Collections.Generic.List[str]):
        """Identifies 1 or more items declared in 8-K filings. Optional & Repeatable."""
        ...

    @property
    def FilingDate(self) -> datetime.datetime:
        """Date report was filed with the SEC"""
        ...

    @FilingDate.setter
    def FilingDate(self, value: datetime.datetime):
        """Date report was filed with the SEC"""
        ...

    @property
    def FilingDateChange(self) -> datetime.datetime:
        """Date when the last Post Acceptance occurred. Optional."""
        ...

    @FilingDateChange.setter
    def FilingDateChange(self, value: datetime.datetime):
        """Date when the last Post Acceptance occurred. Optional."""
        ...

    @property
    def MadeAvailableAt(self) -> datetime.datetime:
        """
        Exact time the report was filed with the SEC and made available to the public (plus 10 minute delay).
        This field is NOT included with the raw SEC report, and should be added during post processing of the data
        """
        ...

    @MadeAvailableAt.setter
    def MadeAvailableAt(self, value: datetime.datetime):
        """
        Exact time the report was filed with the SEC and made available to the public (plus 10 minute delay).
        This field is NOT included with the raw SEC report, and should be added during post processing of the data
        """
        ...

    @property
    def Filers(self) -> System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportFiler]:
        """Contains information regarding who the filer of the report is."""
        ...

    @Filers.setter
    def Filers(self, value: System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportFiler]):
        """Contains information regarding who the filer of the report is."""
        ...

    @property
    def Documents(self) -> System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportDocument]:
        """Attachments/content associated with the report"""
        ...

    @Documents.setter
    def Documents(self, value: System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportDocument]):
        """Attachments/content associated with the report"""
        ...


class ISECReport(QuantConnect.Data.IBaseData, metaclass=abc.ABCMeta):
    """
    Base interface for all SEC report types.
    Using an interface, we can retrieve all report types with a single
    call to Slice.Get{T}()
    """

    @property
    @abc.abstractmethod
    def Report(self) -> QuantConnect.Data.Custom.SEC.SECReportSubmission:
        """Contents of the actual SEC report"""
        ...


class SECReport10K(QuantConnect.Data.BaseData, QuantConnect.Data.Custom.SEC.ISECReport):
    """
    SEC 10-K report (annual earnings) BaseData implementation.
    Using this class, you can retrieve SEC report data for a security if it exists.
    If the ticker you want no longer trades, you can also use the CIK of the company
    you want data for as well except for currently traded stocks. This may change in the future.
    """

    @property
    def Report(self) -> QuantConnect.Data.Custom.SEC.SECReportSubmission:
        """Contents of the actual SEC report"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Empty constructor required for Slice.Get{T}()"""
        ...

    @typing.overload
    def __init__(self, report: QuantConnect.Data.Custom.SEC.SECReportSubmission) -> None:
        """
        Constructor used to initialize instance with the given report
        
        :param report: SEC report submission
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Returns a subscription data source pointing towards SEC 10-K report data
        
        :param config: User configuration
        :param date: Date data has been requested for
        :param isLiveMode: Is livetrading
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Parses the data into BaseData
        
        :param config: User subscription config
        :param line: Line of source file to parse
        :param date: Date data was requested for
        :param isLiveMode: Is livetrading mode
        """
        ...

    def RequiresMapping(self) -> bool:
        """
        Indicates if there is support for mapping
        
        :returns: True indicates mapping should be used.
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Clones the current object into a new object
        
        :returns: BaseData clone of the current object.
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


class SECReport8K(QuantConnect.Data.BaseData, QuantConnect.Data.Custom.SEC.ISECReport):
    """
    SEC 8-K report (important investor notices) BaseData implementation.
    Using this class, you can retrieve SEC report data for a security if it exists.
    If the ticker you want no longer trades, you can also use the CIK of the company
    you want data for as well except for currently traded stocks. This may change in the future.
    """

    @property
    def Report(self) -> QuantConnect.Data.Custom.SEC.SECReportSubmission:
        """Contents of the actual SEC report"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Empty constructor required for Slice.Get{T}()"""
        ...

    @typing.overload
    def __init__(self, report: QuantConnect.Data.Custom.SEC.SECReportSubmission) -> None:
        """
        Constructor used to initialize instance with the given report
        
        :param report: SEC report submission
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Returns a subscription data source pointing towards SEC 8-K report data
        
        :param config: User configuration
        :param date: Date data has been requested for
        :param isLiveMode: Is livetrading
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Parses the data into instance of BaseData
        
        :param config: User subscription config
        :param line: Line of source file to parse
        :param date: Date data was requested for
        :param isLiveMode: Is live trading mode
        """
        ...

    def RequiresMapping(self) -> bool:
        """
        Indicates if there is support for mapping
        
        :returns: True indicates mapping should be used.
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Clones the current object into a new object
        
        :returns: BaseData clone of the current object.
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


class SECReportIndexItem(System.Object):
    """This class has no documentation."""

    @property
    def LastModified(self) -> datetime.datetime:
        """Date the SEC submission was published"""
        ...

    @LastModified.setter
    def LastModified(self, value: datetime.datetime):
        """Date the SEC submission was published"""
        ...

    @property
    def Name(self) -> str:
        """Name of folder/file. Usually accession number"""
        ...

    @Name.setter
    def Name(self, value: str):
        """Name of folder/file. Usually accession number"""
        ...

    @property
    def FileType(self) -> str:
        """Specifies what kind of file the entry is"""
        ...

    @FileType.setter
    def FileType(self, value: str):
        """Specifies what kind of file the entry is"""
        ...

    @property
    def Size(self) -> str:
        """Size of the file. Empty if directory"""
        ...

    @Size.setter
    def Size(self, value: str):
        """Size of the file. Empty if directory"""
        ...


class SECReportIndexDirectory(System.Object):
    """This class has no documentation."""

    @property
    def Items(self) -> System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportIndexItem]:
        """Contains additional metadata regarding files present on the server"""
        ...

    @Items.setter
    def Items(self, value: System.Collections.Generic.List[QuantConnect.Data.Custom.SEC.SECReportIndexItem]):
        """Contains additional metadata regarding files present on the server"""
        ...

    @property
    def Name(self) -> str:
        """Path directory"""
        ...

    @Name.setter
    def Name(self, value: str):
        """Path directory"""
        ...

    @property
    def ParentDirectory(self) -> str:
        """Parent directory (if one exists)"""
        ...

    @ParentDirectory.setter
    def ParentDirectory(self, value: str):
        """Parent directory (if one exists)"""
        ...


class SECReportIndexFile(System.Object):
    """This class has no documentation."""

    @property
    def Directory(self) -> QuantConnect.Data.Custom.SEC.SECReportIndexDirectory:
        """First and only root entry of SEC index.json"""
        ...

    @Directory.setter
    def Directory(self, value: QuantConnect.Data.Custom.SEC.SECReportIndexDirectory):
        """First and only root entry of SEC index.json"""
        ...


class SECReport10Q(QuantConnect.Data.BaseData, QuantConnect.Data.Custom.SEC.ISECReport):
    """
    SEC 10-Q report (quarterly earnings) BaseData implementation.
    Using this class, you can retrieve SEC report data for a security if it exists.
    If the ticker you want no longer trades, you can also use the CIK of the company
    you want data for as well except for currently traded stocks. This may change in the future.
    """

    @property
    def Report(self) -> QuantConnect.Data.Custom.SEC.SECReportSubmission:
        """Contents of the actual SEC report"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Empty constructor required for Slice.Get{T}()"""
        ...

    @typing.overload
    def __init__(self, report: QuantConnect.Data.Custom.SEC.SECReportSubmission) -> None:
        """
        Constructor used to initialize instance with the given report
        
        :param report: SEC report submission
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Returns a subscription data source pointing towards SEC 10-Q report data
        
        :param config: User configuration
        :param date: Date data has been requested for
        :param isLiveMode: Is livetrading
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Parses the data into BaseData
        
        :param config: User subscription config
        :param line: Line of source file to parse
        :param date: Date data was requested for
        :param isLiveMode: Is livetrading mode
        """
        ...

    def RequiresMapping(self) -> bool:
        """
        Indicates if there is support for mapping
        
        :returns: True indicates mapping should be used.
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Clones the current object into a new object
        
        :returns: BaseData clone of the current object.
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


class SECReportFactory(System.Object):
    """This class has no documentation."""

    def CreateSECReport(self, xmlText: str) -> QuantConnect.Data.Custom.SEC.ISECReport:
        """
        Factory method creates SEC report by deserializing XML formatted SEC data to SECReportSubmission
        
        :param xmlText: XML text containing SEC data
        """
        ...


