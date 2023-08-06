import abc
import typing

import System
import System.Collections
import System.Collections.Generic
import System.Globalization
import System.IO
import System.Runtime.Serialization
import System.Text

System_Text_Rune = typing.Any

System_Text_StringBuilder_AppendJoin_T = typing.TypeVar("System_Text_StringBuilder_AppendJoin_T")


class EncoderFallbackBuffer(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Remaining(self) -> int:
        ...

    @property
    def charStart(self) -> typing.Any:
        ...

    @charStart.setter
    def charStart(self, value: typing.Any):
        ...

    @property
    def charEnd(self) -> typing.Any:
        ...

    @charEnd.setter
    def charEnd(self, value: typing.Any):
        ...

    @property
    def encoder(self) -> System.Text.EncoderNLS:
        ...

    @encoder.setter
    def encoder(self, value: System.Text.EncoderNLS):
        ...

    @property
    def setEncoder(self) -> bool:
        ...

    @setEncoder.setter
    def setEncoder(self, value: bool):
        ...

    @property
    def bUsedEncoder(self) -> bool:
        ...

    @bUsedEncoder.setter
    def bUsedEncoder(self, value: bool):
        ...

    @property
    def bFallingBack(self) -> bool:
        ...

    @bFallingBack.setter
    def bFallingBack(self, value: bool):
        ...

    @property
    def iRecursionCount(self) -> int:
        ...

    @iRecursionCount.setter
    def iRecursionCount(self, value: int):
        ...

    @typing.overload
    def Fallback(self, charUnknown: str, index: int) -> bool:
        ...

    @typing.overload
    def Fallback(self, charUnknownHigh: str, charUnknownLow: str, index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class EncoderFallback(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    ReplacementFallback: System.Text.EncoderFallback

    ExceptionFallback: System.Text.EncoderFallback

    @property
    @abc.abstractmethod
    def MaxCharCount(self) -> int:
        ...

    def CreateFallbackBuffer(self) -> System.Text.EncoderFallbackBuffer:
        ...


class NormalizationForm(System.Enum):
    """This class has no documentation."""

    FormC = 1

    FormD = 2

    FormKC = 5

    FormKD = 6


class Encoder(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def _fallback(self) -> System.Text.EncoderFallback:
        ...

    @_fallback.setter
    def _fallback(self, value: System.Text.EncoderFallback):
        ...

    @property
    def _fallbackBuffer(self) -> System.Text.EncoderFallbackBuffer:
        ...

    @_fallbackBuffer.setter
    def _fallbackBuffer(self, value: System.Text.EncoderFallbackBuffer):
        ...

    @property
    def Fallback(self) -> System.Text.EncoderFallback:
        ...

    @Fallback.setter
    def Fallback(self, value: System.Text.EncoderFallback):
        ...

    @property
    def FallbackBuffer(self) -> System.Text.EncoderFallbackBuffer:
        ...

    @property
    def InternalHasFallbackBuffer(self) -> bool:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def Reset(self) -> None:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int, flush: bool) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.Any, count: int, flush: bool) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: System.ReadOnlySpan[str], flush: bool) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int, flush: bool) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int, flush: bool) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int], flush: bool) -> int:
        ...

    @typing.overload
    def Convert(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int, byteCount: int, flush: bool, charsUsed: int, bytesUsed: int, completed: bool) -> None:
        ...

    @typing.overload
    def Convert(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int, flush: bool, charsUsed: int, bytesUsed: int, completed: bool) -> None:
        ...

    @typing.overload
    def Convert(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int], flush: bool, charsUsed: int, bytesUsed: int, completed: bool) -> None:
        ...


class Encoding(System.Object, System.ICloneable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    Default: System.Text.Encoding

    MIMECONTF_MAILNEWS: int = ...

    MIMECONTF_BROWSER: int = ...

    MIMECONTF_SAVABLE_MAILNEWS: int = ...

    MIMECONTF_SAVABLE_BROWSER: int = ...

    CodePageASCII: int = 20127

    ISO_8859_1: int = 28591

    CodePageUTF7: int = 65000

    @property
    def _codePage(self) -> int:
        ...

    @_codePage.setter
    def _codePage(self, value: int):
        ...

    @property
    def _dataItem(self) -> System.Text.CodePageDataItem:
        ...

    @_dataItem.setter
    def _dataItem(self, value: System.Text.CodePageDataItem):
        ...

    @property
    def encoderFallback(self) -> System.Text.EncoderFallback:
        ...

    @encoderFallback.setter
    def encoderFallback(self, value: System.Text.EncoderFallback):
        ...

    @property
    def decoderFallback(self) -> System.Text.DecoderFallback:
        ...

    @decoderFallback.setter
    def decoderFallback(self, value: System.Text.DecoderFallback):
        ...

    @property
    def Preamble(self) -> System.ReadOnlySpan[int]:
        ...

    @property
    def BodyName(self) -> str:
        ...

    @property
    def EncodingName(self) -> str:
        ...

    @property
    def HeaderName(self) -> str:
        ...

    @property
    def WebName(self) -> str:
        ...

    @property
    def WindowsCodePage(self) -> int:
        ...

    @property
    def IsBrowserDisplay(self) -> bool:
        ...

    @property
    def IsBrowserSave(self) -> bool:
        ...

    @property
    def IsMailNewsDisplay(self) -> bool:
        ...

    @property
    def IsMailNewsSave(self) -> bool:
        ...

    @property
    def IsSingleByte(self) -> bool:
        ...

    @property
    def EncoderFallback(self) -> System.Text.EncoderFallback:
        ...

    @EncoderFallback.setter
    def EncoderFallback(self, value: System.Text.EncoderFallback):
        ...

    @property
    def DecoderFallback(self) -> System.Text.DecoderFallback:
        ...

    @DecoderFallback.setter
    def DecoderFallback(self, value: System.Text.DecoderFallback):
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @IsReadOnly.setter
    def IsReadOnly(self, value: bool):
        ...

    ASCII: System.Text.Encoding

    Latin1: System.Text.Encoding
    """Gets an encoding for the Latin1 character set (ISO-8859-1)."""

    @property
    def CodePage(self) -> int:
        ...

    @property
    def IsUTF8CodePage(self) -> bool:
        ...

    Unicode: System.Text.Encoding

    BigEndianUnicode: System.Text.Encoding

    UTF7: System.Text.Encoding

    UTF8: System.Text.Encoding

    UTF32: System.Text.Encoding

    @typing.overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, codePage: int) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, codePage: int, encoderFallback: System.Text.EncoderFallback, decoderFallback: System.Text.DecoderFallback) -> None:
        """This method is protected."""
        ...

    @staticmethod
    @typing.overload
    def Convert(srcEncoding: System.Text.Encoding, dstEncoding: System.Text.Encoding, bytes: typing.List[int]) -> typing.List[int]:
        ...

    @staticmethod
    @typing.overload
    def Convert(srcEncoding: System.Text.Encoding, dstEncoding: System.Text.Encoding, bytes: typing.List[int], index: int, count: int) -> typing.List[int]:
        ...

    @staticmethod
    def RegisterProvider(provider: System.Text.EncodingProvider) -> None:
        ...

    @staticmethod
    @typing.overload
    def GetEncoding(codepage: int) -> System.Text.Encoding:
        ...

    @staticmethod
    @typing.overload
    def GetEncoding(codepage: int, encoderFallback: System.Text.EncoderFallback, decoderFallback: System.Text.DecoderFallback) -> System.Text.Encoding:
        ...

    @staticmethod
    @typing.overload
    def GetEncoding(name: str) -> System.Text.Encoding:
        ...

    @staticmethod
    @typing.overload
    def GetEncoding(name: str, encoderFallback: System.Text.EncoderFallback, decoderFallback: System.Text.DecoderFallback) -> System.Text.Encoding:
        ...

    @staticmethod
    def GetEncodings() -> typing.List[System.Text.EncodingInfo]:
        """
        Get the EncodingInfo list from the runtime and all registered encoding providers
        
        :returns: The list of the EncodingProvider objects.
        """
        ...

    def GetPreamble(self) -> typing.List[int]:
        ...

    def Clone(self) -> System.Object:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.List[str]) -> int:
        ...

    @typing.overload
    def GetByteCount(self, s: str) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetByteCount(self, s: str, index: int, count: int) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: System.ReadOnlySpan[str]) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.List[str]) -> typing.List[int]:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.List[str], index: int, count: int) -> typing.List[int]:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, s: str) -> typing.List[int]:
        ...

    @typing.overload
    def GetBytes(self, s: str, index: int, count: int) -> typing.List[int]:
        ...

    @typing.overload
    def GetBytes(self, s: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int]) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.List[int]) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: System.ReadOnlySpan[int]) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.List[int]) -> typing.List[str]:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.List[int], index: int, count: int) -> typing.List[str]:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str]) -> int:
        ...

    @typing.overload
    def GetString(self, bytes: typing.Any, byteCount: int) -> str:
        ...

    @typing.overload
    def GetString(self, bytes: System.ReadOnlySpan[int]) -> str:
        ...

    @typing.overload
    def IsAlwaysNormalized(self) -> bool:
        ...

    @typing.overload
    def IsAlwaysNormalized(self, form: System.Text.NormalizationForm) -> bool:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    @typing.overload
    def GetString(self, bytes: typing.List[int]) -> str:
        ...

    @typing.overload
    def GetString(self, bytes: typing.List[int], index: int, count: int) -> str:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    @staticmethod
    def CreateTranscodingStream(innerStream: System.IO.Stream, innerStreamEncoding: System.Text.Encoding, outerStreamEncoding: System.Text.Encoding, leaveOpen: bool = False) -> System.IO.Stream:
        """
        Creates a Stream which serves to transcode data between an inner Encoding
        and an outer Encoding, similar to Convert.
        
        :param innerStream: The Stream to wrap.
        :param innerStreamEncoding: The Encoding associated with .
        :param outerStreamEncoding: The Encoding associated with the Stream returned by this method.
        :param leaveOpen: true if disposing the Stream returned by this method should not dispose .
        :returns: A Stream which transcodes the contents of  as .
        """
        ...


class DecoderFallbackBuffer(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Remaining(self) -> int:
        ...

    @property
    def byteStart(self) -> typing.Any:
        ...

    @byteStart.setter
    def byteStart(self, value: typing.Any):
        ...

    @property
    def charEnd(self) -> typing.Any:
        ...

    @charEnd.setter
    def charEnd(self, value: typing.Any):
        ...

    @property
    def _encoding(self) -> System.Text.Encoding:
        ...

    @_encoding.setter
    def _encoding(self, value: System.Text.Encoding):
        ...

    @property
    def _decoder(self) -> System.Text.DecoderNLS:
        ...

    @_decoder.setter
    def _decoder(self, value: System.Text.DecoderNLS):
        ...

    def Fallback(self, bytesUnknown: typing.List[int], index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class DecoderFallback(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    ReplacementFallback: System.Text.DecoderFallback

    ExceptionFallback: System.Text.DecoderFallback

    @property
    @abc.abstractmethod
    def MaxCharCount(self) -> int:
        ...

    def CreateFallbackBuffer(self) -> System.Text.DecoderFallbackBuffer:
        ...


class Decoder(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def _fallback(self) -> System.Text.DecoderFallback:
        ...

    @_fallback.setter
    def _fallback(self, value: System.Text.DecoderFallback):
        ...

    @property
    def _fallbackBuffer(self) -> System.Text.DecoderFallbackBuffer:
        ...

    @_fallbackBuffer.setter
    def _fallbackBuffer(self, value: System.Text.DecoderFallbackBuffer):
        ...

    @property
    def Fallback(self) -> System.Text.DecoderFallback:
        ...

    @Fallback.setter
    def Fallback(self, value: System.Text.DecoderFallback):
        ...

    @property
    def FallbackBuffer(self) -> System.Text.DecoderFallbackBuffer:
        ...

    @property
    def InternalHasFallbackBuffer(self) -> bool:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def Reset(self) -> None:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int, flush: bool) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.Any, count: int, flush: bool) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: System.ReadOnlySpan[int], flush: bool) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int, flush: bool) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int, flush: bool) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str], flush: bool) -> int:
        ...

    @typing.overload
    def Convert(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int, charCount: int, flush: bool, bytesUsed: int, charsUsed: int, completed: bool) -> None:
        ...

    @typing.overload
    def Convert(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int, flush: bool, bytesUsed: int, charsUsed: int, completed: bool) -> None:
        ...

    @typing.overload
    def Convert(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str], flush: bool, bytesUsed: int, charsUsed: int, completed: bool) -> None:
        ...


class ASCIIEncoding(System.Text.Encoding):
    """This class has no documentation."""

    s_default: System.Text.ASCIIEncoding.ASCIIEncodingSealed = ...

    @property
    def IsSingleByte(self) -> bool:
        ...

    def __init__(self) -> None:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: str) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: System.ReadOnlySpan[str]) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int]) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: System.ReadOnlySpan[int]) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str]) -> int:
        ...

    def GetString(self, bytes: typing.List[int], byteIndex: int, byteCount: int) -> str:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...


class EncoderExceptionFallback(System.Text.EncoderFallback):
    """This class has no documentation."""

    s_default: System.Text.EncoderExceptionFallback = ...

    @property
    def MaxCharCount(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def CreateFallbackBuffer(self) -> System.Text.EncoderFallbackBuffer:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class EncoderExceptionFallbackBuffer(System.Text.EncoderFallbackBuffer):
    """This class has no documentation."""

    @property
    def Remaining(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    @typing.overload
    def Fallback(self, charUnknown: str, index: int) -> bool:
        ...

    @typing.overload
    def Fallback(self, charUnknownHigh: str, charUnknownLow: str, index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...


class EncoderFallbackException(System.ArgumentException):
    """This class has no documentation."""

    @property
    def CharUnknown(self) -> str:
        ...

    @property
    def CharUnknownHigh(self) -> str:
        ...

    @property
    def CharUnknownLow(self) -> str:
        ...

    @property
    def Index(self) -> int:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...

    def IsUnknownSurrogate(self) -> bool:
        ...


class Rune(System.IComparable[System_Text_Rune], System.IEquatable[System_Text_Rune]):
    """Represents a Unicode scalar value ([ U+0000..U+D7FF ], inclusive; or [ U+E000..U+10FFFF ], inclusive)."""

    MaxUtf16CharsPerRune: int = 2

    MaxUtf8BytesPerRune: int = 4

    @property
    def IsAscii(self) -> bool:
        """
        Returns true if and only if this scalar value is ASCII ([ U+0000..U+007F ])
        and therefore representable by a single UTF-8 code unit.
        """
        ...

    @property
    def IsBmp(self) -> bool:
        """
        Returns true if and only if this scalar value is within the BMP ([ U+0000..U+FFFF ])
        and therefore representable by a single UTF-16 code unit.
        """
        ...

    @property
    def Plane(self) -> int:
        """Returns the Unicode plane (0 to 16, inclusive) which contains this scalar."""
        ...

    ReplacementChar: System.Text.Rune
    """A Rune instance that represents the Unicode replacement character U+FFFD."""

    @property
    def Utf16SequenceLength(self) -> int:
        """
        Returns the length in code units (char) of the
        UTF-16 sequence required to represent this scalar value.
        """
        ...

    @property
    def Utf8SequenceLength(self) -> int:
        """
        Returns the length in code units of the
        UTF-8 sequence required to represent this scalar value.
        """
        ...

    @property
    def Value(self) -> int:
        """Returns the Unicode scalar value as an integer."""
        ...

    @typing.overload
    def __init__(self, ch: str) -> None:
        """Creates a Rune from the provided UTF-16 code unit."""
        ...

    @typing.overload
    def __init__(self, highSurrogate: str, lowSurrogate: str) -> None:
        """Creates a Rune from the provided UTF-16 surrogate pair."""
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """Creates a Rune from the provided Unicode scalar value."""
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """Creates a Rune from the provided Unicode scalar value."""
        ...

    @typing.overload
    def CompareTo(self, other: System.Text.Rune) -> int:
        ...

    @staticmethod
    def DecodeFromUtf16(source: System.ReadOnlySpan[str], result: System.Text.Rune, charsConsumed: int) -> int:
        """
        Decodes the Rune at the beginning of the provided UTF-16 source buffer.
        
        :returns: If the source buffer begins with a valid UTF-16 encoded scalar value, returns , and outs via  the decoded  and via  the number of s used in the input buffer to encode the .  If the source buffer is empty or contains only a standalone UTF-16 high surrogate character, returns , and outs via  and via  the length of the input buffer.  If the source buffer begins with an ill-formed UTF-16 encoded scalar value, returns , and outs via  and via  the number of s used in the input buffer to encode the ill-formed sequence. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    def DecodeFromUtf8(source: System.ReadOnlySpan[int], result: System.Text.Rune, bytesConsumed: int) -> int:
        """
        Decodes the Rune at the beginning of the provided UTF-8 source buffer.
        
        :returns: If the source buffer begins with a valid UTF-8 encoded scalar value, returns , and outs via  the decoded  and via  the number of s used in the input buffer to encode the .  If the source buffer is empty or contains only a partial UTF-8 subsequence, returns , and outs via  and via  the length of the input buffer.  If the source buffer begins with an ill-formed UTF-8 encoded scalar value, returns , and outs via  and via  the number of s used in the input buffer to encode the ill-formed sequence. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    def DecodeLastFromUtf16(source: System.ReadOnlySpan[str], result: System.Text.Rune, charsConsumed: int) -> int:
        """
        Decodes the Rune at the end of the provided UTF-16 source buffer.
        
        :returns: This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    def DecodeLastFromUtf8(source: System.ReadOnlySpan[int], value: System.Text.Rune, bytesConsumed: int) -> int:
        """
        Decodes the Rune at the end of the provided UTF-8 source buffer.
        
        :returns: This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    def EncodeToUtf16(self, destination: System.Span[str]) -> int:
        """
        Encodes this Rune to a UTF-16 destination buffer.
        
        :param destination: The buffer to which to write this value as UTF-16.
        :returns: The number of chars written to .
        """
        ...

    def EncodeToUtf8(self, destination: System.Span[int]) -> int:
        """
        Encodes this Rune to a UTF-8 destination buffer.
        
        :param destination: The buffer to which to write this value as UTF-8.
        :returns: The number of bytes written to .
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def Equals(self, other: System.Text.Rune) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    @staticmethod
    def GetRuneAt(input: str, index: int) -> System.Text.Rune:
        """
        Gets the Rune which begins at index  in
        string .
        """
        ...

    @staticmethod
    @typing.overload
    def IsValid(value: int) -> bool:
        """
        Returns true iff  is a valid Unicode scalar
        value, i.e., is in [ U+0000..U+D7FF ], inclusive; or [ U+E000..U+10FFFF ], inclusive.
        """
        ...

    @staticmethod
    @typing.overload
    def IsValid(value: int) -> bool:
        """
        Returns true iff  is a valid Unicode scalar
        value, i.e., is in [ U+0000..U+D7FF ], inclusive; or [ U+E000..U+10FFFF ], inclusive.
        """
        ...

    def ToString(self) -> str:
        """Returns a string representation of this Rune instance."""
        ...

    @staticmethod
    @typing.overload
    def TryCreate(ch: str, result: System.Text.Rune) -> bool:
        """Attempts to create a Rune from the provided input value."""
        ...

    @staticmethod
    @typing.overload
    def TryCreate(highSurrogate: str, lowSurrogate: str, result: System.Text.Rune) -> bool:
        """
        Attempts to create a Rune from the provided UTF-16 surrogate pair.
        Returns false if the input values don't represent a well-formed UTF-16surrogate pair.
        """
        ...

    @staticmethod
    @typing.overload
    def TryCreate(value: int, result: System.Text.Rune) -> bool:
        """Attempts to create a Rune from the provided input value."""
        ...

    @staticmethod
    @typing.overload
    def TryCreate(value: int, result: System.Text.Rune) -> bool:
        """Attempts to create a Rune from the provided input value."""
        ...

    def TryEncodeToUtf16(self, destination: System.Span[str], charsWritten: int) -> bool:
        """
        Encodes this Rune to a UTF-16 destination buffer.
        
        :param destination: The buffer to which to write this value as UTF-16.
        :param charsWritten: The number of chars written to , or 0 if the destination buffer is not large enough to contain the output.
        :returns: True if the value was written to the buffer; otherwise, false.
        """
        ...

    def TryEncodeToUtf8(self, destination: System.Span[int], bytesWritten: int) -> bool:
        """
        Encodes this Rune to a destination buffer as UTF-8 bytes.
        
        :param destination: The buffer to which to write this value as UTF-8.
        :param bytesWritten: The number of bytes written to , or 0 if the destination buffer is not large enough to contain the output.
        :returns: True if the value was written to the buffer; otherwise, false.
        """
        ...

    @staticmethod
    def TryGetRuneAt(input: str, index: int, value: System.Text.Rune) -> bool:
        """
        Attempts to get the Rune which begins at index  in
        string .
        
        :returns: true if a scalar value was successfully extracted from the specified index, false if a value could not be extracted due to invalid data.
        """
        ...

    @staticmethod
    def GetNumericValue(value: System.Text.Rune) -> float:
        ...

    @staticmethod
    def GetUnicodeCategory(value: System.Text.Rune) -> int:
        """:returns: This method returns the int value of a member of the System.Globalization.UnicodeCategory enum."""
        ...

    @staticmethod
    def IsControl(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsDigit(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsLetter(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsLetterOrDigit(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsLower(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsNumber(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsPunctuation(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsSeparator(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsSymbol(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsUpper(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsWhiteSpace(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def ToLower(value: System.Text.Rune, culture: System.Globalization.CultureInfo) -> System.Text.Rune:
        ...

    @staticmethod
    def ToLowerInvariant(value: System.Text.Rune) -> System.Text.Rune:
        ...

    @staticmethod
    def ToUpper(value: System.Text.Rune, culture: System.Globalization.CultureInfo) -> System.Text.Rune:
        ...

    @staticmethod
    def ToUpperInvariant(value: System.Text.Rune) -> System.Text.Rune:
        ...

    @typing.overload
    def CompareTo(self, obj: typing.Any) -> int:
        ...


class SpanRuneEnumerator:
    """This class has no documentation."""

    @property
    def Current(self) -> System.Text.Rune:
        ...

    def GetEnumerator(self) -> System.Text.SpanRuneEnumerator:
        ...

    def MoveNext(self) -> bool:
        ...


class DecoderExceptionFallback(System.Text.DecoderFallback):
    """This class has no documentation."""

    s_default: System.Text.DecoderExceptionFallback = ...

    @property
    def MaxCharCount(self) -> int:
        ...

    def CreateFallbackBuffer(self) -> System.Text.DecoderFallbackBuffer:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class DecoderExceptionFallbackBuffer(System.Text.DecoderFallbackBuffer):
    """This class has no documentation."""

    @property
    def Remaining(self) -> int:
        ...

    def Fallback(self, bytesUnknown: typing.List[int], index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...


class DecoderFallbackException(System.ArgumentException):
    """This class has no documentation."""

    @property
    def BytesUnknown(self) -> typing.List[int]:
        ...

    @property
    def Index(self) -> int:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, bytesUnknown: typing.List[int], index: int) -> None:
        ...


class UTF32Encoding(System.Text.Encoding):
    """This class has no documentation."""

    s_default: System.Text.UTF32Encoding = ...

    s_bigEndianDefault: System.Text.UTF32Encoding = ...

    @property
    def Preamble(self) -> System.ReadOnlySpan[int]:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, bigEndian: bool, byteOrderMark: bool) -> None:
        ...

    @typing.overload
    def __init__(self, bigEndian: bool, byteOrderMark: bool, throwOnInvalidCharacters: bool) -> None:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetByteCount(self, s: str) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, s: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    def GetString(self, bytes: typing.List[int], index: int, count: int) -> str:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    def GetPreamble(self) -> typing.List[int]:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class UTF8Encoding(System.Text.Encoding):
    """This class has no documentation."""

    s_default: System.Text.UTF8Encoding.UTF8EncodingSealed = ...

    PreambleSpan: System.ReadOnlySpan[int]

    @property
    def Preamble(self) -> System.ReadOnlySpan[int]:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, encoderShouldEmitUTF8Identifier: bool) -> None:
        ...

    @typing.overload
    def __init__(self, encoderShouldEmitUTF8Identifier: bool, throwOnInvalidBytes: bool) -> None:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: str) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: System.ReadOnlySpan[str]) -> int:
        ...

    @typing.overload
    def GetBytes(self, s: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int]) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: System.ReadOnlySpan[int]) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str]) -> int:
        ...

    def GetString(self, bytes: typing.List[int], index: int, count: int) -> str:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    def GetPreamble(self) -> typing.List[int]:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class EncodingInfo(System.Object):
    """This class has no documentation."""

    @property
    def CodePage(self) -> int:
        """Get the encoding codepage number"""
        ...

    @property
    def Name(self) -> str:
        """Get the encoding name"""
        ...

    @property
    def DisplayName(self) -> str:
        """Get the encoding display name"""
        ...

    @property
    def Provider(self) -> System.Text.EncodingProvider:
        ...

    def __init__(self, provider: System.Text.EncodingProvider, codePage: int, name: str, displayName: str) -> None:
        """
        Construct an EncodingInfo object.
        
        :param provider: The EncodingProvider object which created this EncodingInfo object
        :param codePage: The encoding codepage
        :param name: The encoding name
        :param displayName: The encoding display name
        """
        ...

    def GetEncoding(self) -> System.Text.Encoding:
        """
        Get the Encoding object match the information in the EncodingInfo object
        
        :returns: The Encoding object.
        """
        ...

    def Equals(self, value: typing.Any) -> bool:
        """
        Compare this EncodingInfo object to other object.
        
        :param value: The other object to compare with this object
        :returns: True if the value object is EncodingInfo object and has a codepage equals to this EncodingInfo object codepage. Otherwise, it returns False.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Get a hashcode representing the current EncodingInfo object.
        
        :returns: The integer value representing the hash code of the EncodingInfo object.
        """
        ...


class EncodingProvider(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...

    @typing.overload
    def GetEncoding(self, name: str) -> System.Text.Encoding:
        ...

    @typing.overload
    def GetEncoding(self, codepage: int) -> System.Text.Encoding:
        ...

    @typing.overload
    def GetEncoding(self, name: str, encoderFallback: System.Text.EncoderFallback, decoderFallback: System.Text.DecoderFallback) -> System.Text.Encoding:
        ...

    @typing.overload
    def GetEncoding(self, codepage: int, encoderFallback: System.Text.EncoderFallback, decoderFallback: System.Text.DecoderFallback) -> System.Text.Encoding:
        ...

    def GetEncodings(self) -> System.Collections.Generic.IEnumerable[System.Text.EncodingInfo]:
        ...


class UTF7Encoding(System.Text.Encoding):
    """This class has no documentation."""

    s_default: System.Text.UTF7Encoding = ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, allowOptionals: bool) -> None:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetByteCount(self, s: str) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, s: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    def GetString(self, bytes: typing.List[int], index: int, count: int) -> str:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...


class StringBuilder(System.Object, System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    class ChunkEnumerator:
        """
        ChunkEnumerator supports both the IEnumerable and IEnumerator pattern so foreach
        works (see GetChunks).  It needs to be public (so the compiler can use it
        when building a foreach statement) but users typically don't use it explicitly.
        (which is why it is a nested type).
        """

        @property
        def Current(self) -> System.ReadOnlyMemory[str]:
            """Implements the IEnumerator pattern."""
            ...

        def GetEnumerator(self) -> System.Text.StringBuilder.ChunkEnumerator:
            """Implement IEnumerable.GetEnumerator() to return  'this' as the IEnumerator"""
            ...

        def MoveNext(self) -> bool:
            """Implements the IEnumerator pattern."""
            ...

    @property
    def m_ChunkChars(self) -> typing.List[str]:
        ...

    @m_ChunkChars.setter
    def m_ChunkChars(self, value: typing.List[str]):
        ...

    @property
    def m_ChunkPrevious(self) -> System.Text.StringBuilder:
        """The chunk that logically precedes this chunk."""
        ...

    @m_ChunkPrevious.setter
    def m_ChunkPrevious(self, value: System.Text.StringBuilder):
        """The chunk that logically precedes this chunk."""
        ...

    @property
    def m_ChunkLength(self) -> int:
        """
        The number of characters in this chunk.
        This is the number of elements in m_ChunkChars that are in use, from the start of the buffer.
        """
        ...

    @m_ChunkLength.setter
    def m_ChunkLength(self, value: int):
        """
        The number of characters in this chunk.
        This is the number of elements in m_ChunkChars that are in use, from the start of the buffer.
        """
        ...

    @property
    def m_ChunkOffset(self) -> int:
        """
        The logical offset of this chunk's characters in the string it is a part of.
        This is the sum of the number of characters in preceding blocks.
        """
        ...

    @m_ChunkOffset.setter
    def m_ChunkOffset(self, value: int):
        """
        The logical offset of this chunk's characters in the string it is a part of.
        This is the sum of the number of characters in preceding blocks.
        """
        ...

    @property
    def m_MaxCapacity(self) -> int:
        """The maximum capacity this builder is allowed to have."""
        ...

    @m_MaxCapacity.setter
    def m_MaxCapacity(self, value: int):
        """The maximum capacity this builder is allowed to have."""
        ...

    DefaultCapacity: int = 16
    """The default capacity of a StringBuilder."""

    MaxChunkSize: int = 8000

    @property
    def Capacity(self) -> int:
        ...

    @Capacity.setter
    def Capacity(self, value: int):
        ...

    @property
    def MaxCapacity(self) -> int:
        """Gets the maximum capacity this builder is allowed to have."""
        ...

    @property
    def Length(self) -> int:
        """Gets or sets the length of this builder."""
        ...

    @Length.setter
    def Length(self, value: int):
        """Gets or sets the length of this builder."""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Initializes a new instance of the StringBuilder class."""
        ...

    @typing.overload
    def __init__(self, capacity: int) -> None:
        """
        Initializes a new instance of the StringBuilder class.
        
        :param capacity: The initial capacity of this builder.
        """
        ...

    @typing.overload
    def __init__(self, value: str) -> None:
        """
        Initializes a new instance of the StringBuilder class.
        
        :param value: The initial contents of this builder.
        """
        ...

    @typing.overload
    def __init__(self, value: str, capacity: int) -> None:
        """
        Initializes a new instance of the StringBuilder class.
        
        :param value: The initial contents of this builder.
        :param capacity: The initial capacity of this builder.
        """
        ...

    @typing.overload
    def __init__(self, value: str, startIndex: int, length: int, capacity: int) -> None:
        """
        Initializes a new instance of the StringBuilder class.
        
        :param value: The initial contents of this builder.
        :param startIndex: The index to start in .
        :param length: The number of characters to read in .
        :param capacity: The initial capacity of this builder.
        """
        ...

    @typing.overload
    def __init__(self, capacity: int, maxCapacity: int) -> None:
        """
        Initializes a new instance of the StringBuilder class.
        
        :param capacity: The initial capacity of this builder.
        :param maxCapacity: The maximum capacity of this builder.
        """
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def EnsureCapacity(self, capacity: int) -> int:
        """
        Ensures that the capacity of this builder is at least the specified value.
        
        :param capacity: The new capacity for this builder.
        """
        ...

    @typing.overload
    def ToString(self) -> str:
        ...

    @typing.overload
    def ToString(self, startIndex: int, length: int) -> str:
        """
        Creates a string from a substring of this builder.
        
        :param startIndex: The index to start in this builder.
        :param length: The number of characters to read in this builder.
        """
        ...

    def Clear(self) -> System.Text.StringBuilder:
        ...

    def __getitem__(self, index: int) -> str:
        ...

    def __setitem__(self, index: int, value: str) -> None:
        ...

    def GetChunks(self) -> System.Text.StringBuilder.ChunkEnumerator:
        """
        GetChunks returns ChunkEnumerator that follows the IEnumerable pattern and
        thus can be used in a C# 'foreach' statements to retrieve the data in the StringBuilder
        as chunks (ReadOnlyMemory) of characters.  An example use is:
        
             foreach (ReadOnlyMemory<char> chunk in sb.GetChunks())
                foreach (char c in chunk.Span)
                    { /* operation on c }
        
        It is undefined what happens if the StringBuilder is modified while the chunk
        enumeration is incomplete.  StringBuilder is also not thread-safe, so operating
        on it with concurrent threads is illegal.  Finally the ReadOnlyMemory chunks returned
        are NOT guarenteed to remain unchanged if the StringBuilder is modified, so do
        not cache them for later use either.  This API's purpose is efficiently extracting
        the data of a CONSTANT StringBuilder.
        
        Creating a ReadOnlySpan from a ReadOnlyMemory  (the .Span property) is expensive
        compared to the fetching of the character, so create a local variable for the SPAN
        if you need to use it in a nested for statement.  For example
        
           foreach (ReadOnlyMemory<char> chunk in sb.GetChunks())
           {
                var span = chunk.Span;
                for (int i = 0; i < span.Length; i++)
                    { /* operation on span[i] */ }
           }
        """
        ...

    @typing.overload
    def Append(self, value: str, repeatCount: int) -> System.Text.StringBuilder:
        """
        Appends a character 0 or more times to the end of this builder.
        
        :param value: The character to append.
        :param repeatCount: The number of times to append .
        """
        ...

    @typing.overload
    def Append(self, value: typing.List[str], startIndex: int, charCount: int) -> System.Text.StringBuilder:
        """
        Appends a range of characters to the end of this builder.
        
        :param value: The characters to append.
        :param startIndex: The index to start in .
        :param charCount: The number of characters to read in .
        """
        ...

    @typing.overload
    def Append(self, value: str) -> System.Text.StringBuilder:
        """
        Appends a string to the end of this builder.
        
        :param value: The string to append.
        """
        ...

    @typing.overload
    def Append(self, value: str, startIndex: int, count: int) -> System.Text.StringBuilder:
        """
        Appends part of a string to the end of this builder.
        
        :param value: The string to append.
        :param startIndex: The index to start in .
        :param count: The number of characters to read in .
        """
        ...

    @typing.overload
    def Append(self, value: System.Text.StringBuilder) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: System.Text.StringBuilder, startIndex: int, count: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendLine(self) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendLine(self, value: str) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def CopyTo(self, sourceIndex: int, destination: typing.List[str], destinationIndex: int, count: int) -> None:
        ...

    @typing.overload
    def CopyTo(self, sourceIndex: int, destination: System.Span[str], count: int) -> None:
        ...

    @typing.overload
    def Insert(self, index: int, value: str, count: int) -> System.Text.StringBuilder:
        """
        Inserts a string 0 or more times into this builder at the specified position.
        
        :param index: The index to insert in this builder.
        :param value: The string to insert.
        :param count: The number of times to insert the string.
        """
        ...

    def Remove(self, startIndex: int, length: int) -> System.Text.StringBuilder:
        """Removes a range of characters from this builder."""
        ...

    @typing.overload
    def Append(self, value: bool) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: str) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: float) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: float) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: float) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: typing.List[str]) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: System.ReadOnlySpan[str]) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Append(self, value: System.ReadOnlyMemory[str]) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendJoin(self, separator: str, *values: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendJoin(self, separator: str, values: System.Collections.Generic.IEnumerable[System_Text_StringBuilder_AppendJoin_T]) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendJoin(self, separator: str, *values: str) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendJoin(self, separator: str, *values: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendJoin(self, separator: str, values: System.Collections.Generic.IEnumerable[System_Text_StringBuilder_AppendJoin_T]) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendJoin(self, separator: str, *values: str) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: str) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: bool) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: str) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: typing.List[str]) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: typing.List[str], startIndex: int, charCount: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: float) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: float) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: float) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Insert(self, index: int, value: System.ReadOnlySpan[str]) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendFormat(self, format: str, arg0: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendFormat(self, format: str, arg0: typing.Any, arg1: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendFormat(self, format: str, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendFormat(self, format: str, *args: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendFormat(self, provider: System.IFormatProvider, format: str, arg0: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendFormat(self, provider: System.IFormatProvider, format: str, arg0: typing.Any, arg1: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendFormat(self, provider: System.IFormatProvider, format: str, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def AppendFormat(self, provider: System.IFormatProvider, format: str, *args: typing.Any) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Replace(self, oldValue: str, newValue: str) -> System.Text.StringBuilder:
        """
        Replaces all instances of one string with another in this builder.
        
        :param oldValue: The string to replace.
        :param newValue: The string to replace  with.
        """
        ...

    @typing.overload
    def Equals(self, sb: System.Text.StringBuilder) -> bool:
        """
        Determines if the contents of this builder are equal to the contents of another builder.
        
        :param sb: The other builder.
        """
        ...

    @typing.overload
    def Equals(self, span: System.ReadOnlySpan[str]) -> bool:
        """
        Determines if the contents of this builder are equal to the contents of ReadOnlySpan{Char}.
        
        :param span: The ReadOnlySpan{Char}.
        """
        ...

    @typing.overload
    def Replace(self, oldValue: str, newValue: str, startIndex: int, count: int) -> System.Text.StringBuilder:
        """
        Replaces all instances of one string with another in part of this builder.
        
        :param oldValue: The string to replace.
        :param newValue: The string to replace  with.
        :param startIndex: The index to start in this builder.
        :param count: The number of characters to read in this builder.
        """
        ...

    @typing.overload
    def Replace(self, oldChar: str, newChar: str) -> System.Text.StringBuilder:
        """
        Replaces all instances of one character with another in this builder.
        
        :param oldChar: The character to replace.
        :param newChar: The character to replace  with.
        """
        ...

    @typing.overload
    def Replace(self, oldChar: str, newChar: str, startIndex: int, count: int) -> System.Text.StringBuilder:
        """
        Replaces all instances of one character with another in this builder.
        
        :param oldChar: The character to replace.
        :param newChar: The character to replace  with.
        :param startIndex: The index to start in this builder.
        :param count: The number of characters to read in this builder.
        """
        ...

    @typing.overload
    def Append(self, value: typing.Any, valueCount: int) -> System.Text.StringBuilder:
        """
        Appends a character buffer to this builder.
        
        :param value: The pointer to the start of the buffer.
        :param valueCount: The number of characters in the buffer.
        """
        ...


class EncoderReplacementFallback(System.Text.EncoderFallback):
    """This class has no documentation."""

    s_default: System.Text.EncoderReplacementFallback = ...

    @property
    def DefaultString(self) -> str:
        ...

    @property
    def MaxCharCount(self) -> int:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, replacement: str) -> None:
        ...

    def CreateFallbackBuffer(self) -> System.Text.EncoderFallbackBuffer:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class EncoderReplacementFallbackBuffer(System.Text.EncoderFallbackBuffer):
    """This class has no documentation."""

    @property
    def Remaining(self) -> int:
        ...

    def __init__(self, fallback: System.Text.EncoderReplacementFallback) -> None:
        ...

    @typing.overload
    def Fallback(self, charUnknown: str, index: int) -> bool:
        ...

    @typing.overload
    def Fallback(self, charUnknownHigh: str, charUnknownLow: str, index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class DecoderReplacementFallback(System.Text.DecoderFallback):
    """This class has no documentation."""

    s_default: System.Text.DecoderReplacementFallback = ...

    @property
    def DefaultString(self) -> str:
        ...

    @property
    def MaxCharCount(self) -> int:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, replacement: str) -> None:
        ...

    def CreateFallbackBuffer(self) -> System.Text.DecoderFallbackBuffer:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class DecoderReplacementFallbackBuffer(System.Text.DecoderFallbackBuffer):
    """This class has no documentation."""

    @property
    def Remaining(self) -> int:
        ...

    def __init__(self, fallback: System.Text.DecoderReplacementFallback) -> None:
        ...

    def Fallback(self, bytesUnknown: typing.List[int], index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class StringRuneEnumerator(System.Collections.Generic.IEnumerable[System.Text.Rune], typing.Iterable[System.Text.Rune]):
    """This class has no documentation."""

    @property
    def Current(self) -> System.Text.Rune:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Text.StringRuneEnumerator:
        ...

    def MoveNext(self) -> bool:
        ...

    def Dispose(self) -> None:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System.Text.Rune]:
        ...

    def Reset(self) -> None:
        ...


class UnicodeEncoding(System.Text.Encoding):
    """This class has no documentation."""

    s_bigEndianDefault: System.Text.UnicodeEncoding = ...

    s_littleEndianDefault: System.Text.UnicodeEncoding = ...

    CharSize: int = 2

    @property
    def Preamble(self) -> System.ReadOnlySpan[int]:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, bigEndian: bool, byteOrderMark: bool) -> None:
        ...

    @typing.overload
    def __init__(self, bigEndian: bool, byteOrderMark: bool, throwOnInvalidBytes: bool) -> None:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetByteCount(self, s: str) -> int:
        ...

    @typing.overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, s: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @typing.overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @typing.overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @typing.overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    def GetString(self, bytes: typing.List[int], index: int, count: int) -> str:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetPreamble(self) -> typing.List[int]:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


