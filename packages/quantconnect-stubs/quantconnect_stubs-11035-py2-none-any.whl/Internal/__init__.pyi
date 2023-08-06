import typing

import Internal
import System


class Console(System.Object):
    """This class has no documentation."""

    @staticmethod
    @typing.overload
    def WriteLine(s: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLine() -> None:
        ...

    @staticmethod
    @typing.overload
    def Write(s: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def Write(s: str) -> None:
        ...


