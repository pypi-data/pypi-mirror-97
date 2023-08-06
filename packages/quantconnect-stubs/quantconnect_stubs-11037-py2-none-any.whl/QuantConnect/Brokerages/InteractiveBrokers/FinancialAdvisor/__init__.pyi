import QuantConnect.Brokerages.InteractiveBrokers.Client
import QuantConnect.Brokerages.InteractiveBrokers.FinancialAdvisor
import System
import System.Collections.Generic


class AccountAlias(System.Object):
    """Represents an alias for an account"""

    @property
    def Account(self) -> str:
        """The account code"""
        ...

    @Account.setter
    def Account(self, value: str):
        """The account code"""
        ...

    @property
    def Alias(self) -> str:
        """The alias for the account"""
        ...

    @Alias.setter
    def Alias(self, value: str):
        """The alias for the account"""
        ...


class Group(System.Object):
    """Represents a group of accounts"""

    @property
    def Name(self) -> str:
        """The name of the group"""
        ...

    @Name.setter
    def Name(self, value: str):
        """The name of the group"""
        ...

    @property
    def Accounts(self) -> System.Collections.Generic.List[str]:
        """The list of accounts in the group"""
        ...

    @Accounts.setter
    def Accounts(self, value: System.Collections.Generic.List[str]):
        """The list of accounts in the group"""
        ...


class Allocation(System.Object):
    """Represents an allocation"""

    @property
    def Account(self) -> str:
        """The account code"""
        ...

    @Account.setter
    def Account(self, value: str):
        """The account code"""
        ...

    @property
    def Amount(self) -> float:
        """The amount for the allocation"""
        ...

    @Amount.setter
    def Amount(self, value: float):
        """The amount for the allocation"""
        ...


class AllocationProfile(System.Object):
    """Represents an allocation profile"""

    @property
    def Name(self) -> str:
        """The name of the profile"""
        ...

    @Name.setter
    def Name(self, value: str):
        """The name of the profile"""
        ...

    @property
    def Type(self) -> str:
        """The type of the profile"""
        ...

    @Type.setter
    def Type(self, value: str):
        """The type of the profile"""
        ...

    @property
    def Allocations(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.InteractiveBrokers.FinancialAdvisor.Allocation]:
        """The list of allocations in the profile"""
        ...

    @Allocations.setter
    def Allocations(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.InteractiveBrokers.FinancialAdvisor.Allocation]):
        """The list of allocations in the profile"""
        ...


class FinancialAdvisorConfiguration(System.Object):
    """Contains configuration data for a Financial Advisor"""

    @property
    def MasterAccount(self) -> str:
        """The financial advisor master account code"""
        ...

    @MasterAccount.setter
    def MasterAccount(self, value: str):
        """The financial advisor master account code"""
        ...

    @property
    def SubAccounts(self) -> System.Collections.Generic.IEnumerable[str]:
        """The sub-account codes managed by the financial advisor"""
        ...

    def Clear(self) -> None:
        """Clears this instance of FinancialAdvisorConfiguration"""
        ...

    def Load(self, client: QuantConnect.Brokerages.InteractiveBrokers.Client.InteractiveBrokersClient) -> bool:
        """
        Downloads the financial advisor configuration
        
        :param client: The IB client
        :returns: true if successfully completed.
        """
        ...


