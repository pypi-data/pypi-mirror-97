import datetime
import typing

import System
import System.Buffers
import System.Buffers.Text


class Utf8Parser(System.Object):
    """Methods to parse common data types to Utf8 strings."""

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: int, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a SByte at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: int, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses an Int16 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: int, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses an Int32 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: int, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses an Int64 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: datetime.timedelta, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a TimeSpan at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: float, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a Single at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: float, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a Double at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: bool, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a Boolean at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: float, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a Decimal at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: System.Guid, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a Guid at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: datetime.datetime, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a DateTime at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: System.DateTimeOffset, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a DateTimeOffset at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: int, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a Byte at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: int, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a UInt16 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: int, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a UInt32 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(source: System.ReadOnlySpan[int], value: int, bytesConsumed: int, standardFormat: str = ...) -> bool:
        """
        Parses a UInt64 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...


class Utf8Formatter(System.Object):
    """Methods to format common data types as Utf8 strings."""

    @staticmethod
    @typing.overload
    def TryFormat(value: System.Guid, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: datetime.timedelta, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a TimeSpan as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a Byte as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats an SByte as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a Unt16 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats an Int16 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a UInt32 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats an Int32 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a UInt64 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats an Int64 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: float, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a Double as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: float, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a Single as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: bool, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a Boolean as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: System.DateTimeOffset, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a DateTimeOffset as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: datetime.datetime, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a DateTime as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @typing.overload
    def TryFormat(value: float, destination: System.Span[int], bytesWritten: int, format: System.Buffers.StandardFormat = ...) -> bool:
        """
        Formats a Decimal as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...


