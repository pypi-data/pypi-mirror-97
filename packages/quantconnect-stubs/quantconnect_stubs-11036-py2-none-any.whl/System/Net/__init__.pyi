import typing

import System
import System.IO
import System.Net


class WebUtility(System.Object):
    """This class has no documentation."""

    @staticmethod
    @typing.overload
    def HtmlEncode(value: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def HtmlEncode(value: str, output: System.IO.TextWriter) -> None:
        ...

    @staticmethod
    @typing.overload
    def HtmlDecode(value: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def HtmlDecode(value: str, output: System.IO.TextWriter) -> None:
        ...

    @staticmethod
    def UrlEncode(value: str) -> str:
        ...

    @staticmethod
    def UrlEncodeToBytes(value: typing.List[int], offset: int, count: int) -> typing.List[int]:
        ...

    @staticmethod
    def UrlDecode(encodedValue: str) -> str:
        ...

    @staticmethod
    def UrlDecodeToBytes(encodedValue: typing.List[int], offset: int, count: int) -> typing.List[int]:
        ...


