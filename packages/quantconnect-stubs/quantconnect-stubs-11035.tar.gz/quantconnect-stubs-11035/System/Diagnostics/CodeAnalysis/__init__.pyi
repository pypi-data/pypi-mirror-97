import System
import System.Diagnostics.CodeAnalysis


class SuppressMessageAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Category(self) -> str:
        ...

    @property
    def CheckId(self) -> str:
        ...

    @property
    def Scope(self) -> str:
        ...

    @Scope.setter
    def Scope(self, value: str):
        ...

    @property
    def Target(self) -> str:
        ...

    @Target.setter
    def Target(self, value: str):
        ...

    @property
    def MessageId(self) -> str:
        ...

    @MessageId.setter
    def MessageId(self, value: str):
        ...

    @property
    def Justification(self) -> str:
        ...

    @Justification.setter
    def Justification(self, value: str):
        ...

    def __init__(self, category: str, checkId: str) -> None:
        ...


class RequiresAssemblyFilesAttribute(System.Attribute):
    """Indicates that the specified member requires assembly files to be on disk."""

    @property
    def Message(self) -> str:
        """
        Gets or sets an optional message that contains information about the need for
        assembly files to be on disk.
        """
        ...

    @Message.setter
    def Message(self, value: str):
        """
        Gets or sets an optional message that contains information about the need for
        assembly files to be on disk.
        """
        ...

    @property
    def Url(self) -> str:
        """
        Gets or sets an optional URL that contains more information about the member,
        why it requires assembly files to be on disk, and what options a consumer has
        to deal with it.
        """
        ...

    @Url.setter
    def Url(self, value: str):
        """
        Gets or sets an optional URL that contains more information about the member,
        why it requires assembly files to be on disk, and what options a consumer has
        to deal with it.
        """
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the RequiresAssemblyFilesAttribute class."""
        ...


