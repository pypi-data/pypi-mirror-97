import abc
import typing

import Microsoft.Win32.SafeHandles
import System
import System.IO
import System.Runtime.InteropServices
import System.Runtime.Serialization
import System.Text
import System.Threading
import System.Threading.Tasks

System_AsyncCallback = typing.Any
ValueTask = typing.Any

System_IO_UnmanagedMemoryAccessor_Read_T = typing.TypeVar("System_IO_UnmanagedMemoryAccessor_Read_T")
System_IO_UnmanagedMemoryAccessor_Write_T = typing.TypeVar("System_IO_UnmanagedMemoryAccessor_Write_T")
System_IO_UnmanagedMemoryAccessor_ReadArray_T = typing.TypeVar("System_IO_UnmanagedMemoryAccessor_ReadArray_T")
System_IO_UnmanagedMemoryAccessor_WriteArray_T = typing.TypeVar("System_IO_UnmanagedMemoryAccessor_WriteArray_T")


class IOException(System.SystemException):
    """This class has no documentation."""

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, hresult: int) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class PathTooLongException(System.IO.IOException):
    """This class has no documentation."""

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
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class SeekOrigin(System.Enum):
    """This class has no documentation."""

    Begin = 0

    Current = 1

    End = 2


class Stream(System.MarshalByRefObject, System.IDisposable, System.IAsyncDisposable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    Null: System.IO.Stream = ...

    @property
    @abc.abstractmethod
    def CanRead(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def CanWrite(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def CanSeek(self) -> bool:
        ...

    @property
    def CanTimeout(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def Length(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def Position(self) -> int:
        ...

    @Position.setter
    @abc.abstractmethod
    def Position(self, value: int):
        ...

    @property
    def ReadTimeout(self) -> int:
        ...

    @ReadTimeout.setter
    def ReadTimeout(self, value: int):
        ...

    @property
    def WriteTimeout(self) -> int:
        ...

    @WriteTimeout.setter
    def WriteTimeout(self, value: int):
        ...

    @typing.overload
    def CopyTo(self, destination: System.IO.Stream) -> None:
        ...

    @typing.overload
    def CopyTo(self, destination: System.IO.Stream, bufferSize: int) -> None:
        ...

    @typing.overload
    def CopyToAsync(self, destination: System.IO.Stream) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def CopyToAsync(self, destination: System.IO.Stream, bufferSize: int) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def CopyToAsync(self, destination: System.IO.Stream, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def CopyToAsync(self, destination: System.IO.Stream, bufferSize: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    def Close(self) -> None:
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    def DisposeAsync(self) -> System.Threading.Tasks.ValueTask:
        ...

    def Flush(self) -> None:
        ...

    @typing.overload
    def FlushAsync(self) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def FlushAsync(self, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    def __init__(self) -> None:
        ...

    def CreateWaitHandle(self) -> System.Threading.WaitHandle:
        """This method is protected."""
        ...

    def BeginRead(self, buffer: typing.List[int], offset: int, count: int, callback: System_AsyncCallback, state: typing.Any) -> System.IAsyncResult:
        ...

    def EndRead(self, asyncResult: System.IAsyncResult) -> int:
        ...

    @typing.overload
    def ReadAsync(self, buffer: typing.List[int], offset: int, count: int) -> System.Threading.Tasks.Task[int]:
        ...

    @typing.overload
    def ReadAsync(self, buffer: typing.List[int], offset: int, count: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[int]:
        ...

    @typing.overload
    def ReadAsync(self, buffer: System.Memory[int], cancellationToken: System.Threading.CancellationToken = ...) -> ValueTask:
        ...

    def BeginWrite(self, buffer: typing.List[int], offset: int, count: int, callback: System_AsyncCallback, state: typing.Any) -> System.IAsyncResult:
        ...

    def EndWrite(self, asyncResult: System.IAsyncResult) -> None:
        ...

    @typing.overload
    def WriteAsync(self, buffer: typing.List[int], offset: int, count: int) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, buffer: typing.List[int], offset: int, count: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, buffer: System.ReadOnlyMemory[int], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.ValueTask:
        ...

    def Seek(self, offset: int, origin: System.IO.SeekOrigin) -> int:
        ...

    def SetLength(self, value: int) -> None:
        ...

    @typing.overload
    def Read(self, buffer: typing.List[int], offset: int, count: int) -> int:
        ...

    @typing.overload
    def Read(self, buffer: System.Span[int]) -> int:
        ...

    def ReadByte(self) -> int:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[int], offset: int, count: int) -> None:
        ...

    @typing.overload
    def Write(self, buffer: System.ReadOnlySpan[int]) -> None:
        ...

    def WriteByte(self, value: int) -> None:
        ...

    @staticmethod
    def Synchronized(stream: System.IO.Stream) -> System.IO.Stream:
        ...

    def ObjectInvariant(self) -> None:
        """This method is protected."""
        ...

    @staticmethod
    def ValidateBufferArguments(buffer: typing.List[int], offset: int, count: int) -> None:
        """
        Validates arguments provided to reading and writing methods on Stream.
        
        This method is protected.
        
        :param buffer: The array "buffer" argument passed to the reading or writing method.
        :param offset: The integer "offset" argument passed to the reading or writing method.
        :param count: The integer "count" argument passed to the reading or writing method.
        """
        ...

    @staticmethod
    def ValidateCopyToArguments(destination: System.IO.Stream, bufferSize: int) -> None:
        """
        Validates arguments provided to the CopyTo(Stream, int) or CopyToAsync(Stream, int, CancellationToken) methods.
        
        This method is protected.
        
        :param destination: The Stream "destination" argument passed to the copy method.
        :param bufferSize: The integer "bufferSize" argument passed to the copy method.
        """
        ...


class FileMode(System.Enum):
    """This class has no documentation."""

    CreateNew = 1

    Create = 2

    Open = 3

    OpenOrCreate = 4

    Truncate = 5

    Append = 6


class FileOptions(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    WriteThrough = ...

    Asynchronous = ...

    RandomAccess = ...

    DeleteOnClose = ...

    SequentialScan = ...

    Encrypted = ...


class FileLoadException(System.IO.IOException):
    """This class has no documentation."""

    @property
    def Message(self) -> str:
        ...

    @property
    def FileName(self) -> str:
        ...

    @property
    def FusionLog(self) -> str:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, fileName: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, fileName: str, inner: System.Exception) -> None:
        ...

    def ToString(self) -> str:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...


class BufferedStream(System.IO.Stream):
    """
    One of the design goals here is to prevent the buffer from getting in the way and slowing
    down underlying stream accesses when it is not needed. If you always read & write for sizes
    greater than the internal buffer size, then this class may not even allocate the internal buffer.
    See a large comment in Write for the details of the write buffer heuristic.
    
    This class buffers reads & writes in a shared buffer.
    (If you maintained two buffers separately, one operation would always trash the other buffer
    anyways, so we might as well use one buffer.)
    The assumption here is you will almost always be doing a series of reads or writes, but rarely
    alternate between the two of them on the same stream.
    
    Class Invariants:
    The class has one buffer, shared for reading & writing.
    It can only be used for one or the other at any point in time - not both.
    The following should be true:
    
      * 0 <= _readPos <= _readLen < _bufferSize
      * 0 <= _writePos < _bufferSize
      * _readPos == _readLen && _readPos > 0 implies the read buffer is valid, but we're at the end of the buffer.
      * _readPos == _readLen == 0 means the read buffer contains garbage.
      * Either _writePos can be greater than 0, or _readLen & _readPos can be greater than zero,
        but neither can be greater than zero at the same time.
     
    This class will never cache more bytes than the max specified buffer size.
    However, it may use a temporary buffer of up to twice the size in order to combine several IO operations on
    the underlying stream into a single operation. This is because we assume that memory copies are significantly
    faster than IO operations on the underlying stream (if this was not true, using buffering is never appropriate).
    The max size of this "shadow" buffer is limited as to not allocate it on the LOH.
    Shadowing is always transient. Even when using this technique, this class still guarantees that the number of
    bytes cached (not yet written to the target stream or not yet consumed by the user) is never larger than the
    actual specified buffer size.
    """

    @property
    def UnderlyingStream(self) -> System.IO.Stream:
        ...

    @property
    def BufferSize(self) -> int:
        ...

    @property
    def CanRead(self) -> bool:
        ...

    @property
    def CanWrite(self) -> bool:
        ...

    @property
    def CanSeek(self) -> bool:
        ...

    @property
    def Length(self) -> int:
        ...

    @property
    def Position(self) -> int:
        ...

    @Position.setter
    def Position(self, value: int):
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream, bufferSize: int) -> None:
        ...

    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    def DisposeAsync(self) -> System.Threading.Tasks.ValueTask:
        ...

    def Flush(self) -> None:
        ...

    def FlushAsync(self, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def Read(self, buffer: typing.List[int], offset: int, count: int) -> int:
        ...

    @typing.overload
    def Read(self, destination: System.Span[int]) -> int:
        ...

    @typing.overload
    def ReadAsync(self, buffer: typing.List[int], offset: int, count: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[int]:
        ...

    @typing.overload
    def ReadAsync(self, buffer: System.Memory[int], cancellationToken: System.Threading.CancellationToken = ...) -> ValueTask:
        ...

    def BeginRead(self, buffer: typing.List[int], offset: int, count: int, callback: System_AsyncCallback, state: typing.Any) -> System.IAsyncResult:
        ...

    def EndRead(self, asyncResult: System.IAsyncResult) -> int:
        ...

    def ReadByte(self) -> int:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[int], offset: int, count: int) -> None:
        ...

    @typing.overload
    def Write(self, buffer: System.ReadOnlySpan[int]) -> None:
        ...

    @typing.overload
    def WriteAsync(self, buffer: typing.List[int], offset: int, count: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, buffer: System.ReadOnlyMemory[int], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.ValueTask:
        ...

    def BeginWrite(self, buffer: typing.List[int], offset: int, count: int, callback: System_AsyncCallback, state: typing.Any) -> System.IAsyncResult:
        ...

    def EndWrite(self, asyncResult: System.IAsyncResult) -> None:
        ...

    def WriteByte(self, value: int) -> None:
        ...

    def Seek(self, offset: int, origin: System.IO.SeekOrigin) -> int:
        ...

    def SetLength(self, value: int) -> None:
        ...

    def CopyTo(self, destination: System.IO.Stream, bufferSize: int) -> None:
        ...

    def CopyToAsync(self, destination: System.IO.Stream, bufferSize: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...


class DirectoryNotFoundException(System.IO.IOException):
    """This class has no documentation."""

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
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class EndOfStreamException(System.IO.IOException):
    """This class has no documentation."""

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
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class TextReader(System.MarshalByRefObject, System.IDisposable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    Null: System.IO.TextReader = ...

    @property
    def t(self) -> typing.Any:
        ...

    @t.setter
    def t(self, value: typing.Any):
        ...

    @typing.overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    def Close(self) -> None:
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    def Peek(self) -> int:
        ...

    @typing.overload
    def Read(self) -> int:
        ...

    @typing.overload
    def Read(self, buffer: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def Read(self, buffer: System.Span[str]) -> int:
        ...

    def ReadToEnd(self) -> str:
        ...

    @typing.overload
    def ReadBlock(self, buffer: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def ReadBlock(self, buffer: System.Span[str]) -> int:
        ...

    def ReadLine(self) -> str:
        ...

    def ReadLineAsync(self) -> System.Threading.Tasks.Task[str]:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    def ReadToEndAsync(self) -> System.Threading.Tasks.Task[str]:
        ...

    @typing.overload
    def ReadAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task[int]:
        ...

    @typing.overload
    def ReadAsync(self, buffer: System.Memory[str], cancellationToken: System.Threading.CancellationToken = ...) -> ValueTask:
        ...


class FileAccess(System.Enum):
    """This class has no documentation."""

    Read = 1

    Write = 2

    ReadWrite = 3


class UnmanagedMemoryStream(System.IO.Stream):
    """This class has no documentation."""

    @property
    def CanRead(self) -> bool:
        """Returns true if the stream can be read; otherwise returns false."""
        ...

    @property
    def CanSeek(self) -> bool:
        """Returns true if the stream can seek; otherwise returns false."""
        ...

    @property
    def CanWrite(self) -> bool:
        """Returns true if the stream can be written to; otherwise returns false."""
        ...

    @property
    def Length(self) -> int:
        """Number of bytes in the stream."""
        ...

    @property
    def Capacity(self) -> int:
        """Number of bytes that can be written to the stream."""
        ...

    @property
    def Position(self) -> int:
        """ReadByte will read byte at the Position in the stream"""
        ...

    @Position.setter
    def Position(self, value: int):
        """ReadByte will read byte at the Position in the stream"""
        ...

    @property
    def PositionPointer(self) -> typing.Any:
        """Pointer to memory at the current Position in the stream."""
        ...

    @PositionPointer.setter
    def PositionPointer(self, value: typing.Any):
        """Pointer to memory at the current Position in the stream."""
        ...

    @typing.overload
    def __init__(self) -> None:
        """
        Creates a closed stream.
        
        This method is protected.
        """
        ...

    @typing.overload
    def __init__(self, buffer: System.Runtime.InteropServices.SafeBuffer, offset: int, length: int) -> None:
        """Creates a stream over a SafeBuffer."""
        ...

    @typing.overload
    def __init__(self, buffer: System.Runtime.InteropServices.SafeBuffer, offset: int, length: int, access: System.IO.FileAccess) -> None:
        """Creates a stream over a SafeBuffer."""
        ...

    @typing.overload
    def Initialize(self, buffer: System.Runtime.InteropServices.SafeBuffer, offset: int, length: int, access: System.IO.FileAccess) -> None:
        """
        Subclasses must call this method (or the other overload) to properly initialize all instance fields.
        
        This method is protected.
        """
        ...

    @typing.overload
    def __init__(self, pointer: typing.Any, length: int) -> None:
        """Creates a stream over a byte*."""
        ...

    @typing.overload
    def __init__(self, pointer: typing.Any, length: int, capacity: int, access: System.IO.FileAccess) -> None:
        """Creates a stream over a byte*."""
        ...

    @typing.overload
    def Initialize(self, pointer: typing.Any, length: int, capacity: int, access: System.IO.FileAccess) -> None:
        """
        Subclasses must call this method (or the other overload) to properly initialize all instance fields.
        
        This method is protected.
        """
        ...

    def Dispose(self, disposing: bool) -> None:
        """
        Closes the stream. The stream's memory needs to be dealt with separately.
        
        This method is protected.
        """
        ...

    def Flush(self) -> None:
        """Since it's a memory stream, this method does nothing."""
        ...

    def FlushAsync(self, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        """Since it's a memory stream, this method does nothing specific."""
        ...

    @typing.overload
    def Read(self, buffer: typing.List[int], offset: int, count: int) -> int:
        """
        Reads bytes from stream and puts them into the buffer
        
        :param buffer: Buffer to read the bytes to.
        :param offset: Starting index in the buffer.
        :param count: Maximum number of bytes to read.
        :returns: Number of bytes actually read.
        """
        ...

    @typing.overload
    def Read(self, buffer: System.Span[int]) -> int:
        ...

    @typing.overload
    def ReadAsync(self, buffer: typing.List[int], offset: int, count: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[int]:
        """
        Reads bytes from stream and puts them into the buffer
        
        :param buffer: Buffer to read the bytes to.
        :param offset: Starting index in the buffer.
        :param count: Maximum number of bytes to read.
        :param cancellationToken: Token that can be used to cancel this operation.
        :returns: Task that can be used to access the number of bytes actually read.
        """
        ...

    @typing.overload
    def ReadAsync(self, buffer: System.Memory[int], cancellationToken: System.Threading.CancellationToken = ...) -> ValueTask:
        """
        Reads bytes from stream and puts them into the buffer
        
        :param buffer: Buffer to read the bytes to.
        :param cancellationToken: Token that can be used to cancel this operation.
        """
        ...

    def ReadByte(self) -> int:
        """Returns the byte at the stream current Position and advances the Position."""
        ...

    def Seek(self, offset: int, loc: System.IO.SeekOrigin) -> int:
        """
        Advanced the Position to specific location in the stream.
        
        :param offset: Offset from the loc parameter.
        :param loc: Origin for the offset parameter.
        """
        ...

    def SetLength(self, value: int) -> None:
        """Sets the Length of the stream."""
        ...

    @typing.overload
    def Write(self, buffer: typing.List[int], offset: int, count: int) -> None:
        """
        Writes buffer into the stream
        
        :param buffer: Buffer that will be written.
        :param offset: Starting index in the buffer.
        :param count: Number of bytes to write.
        """
        ...

    @typing.overload
    def Write(self, buffer: System.ReadOnlySpan[int]) -> None:
        ...

    @typing.overload
    def WriteAsync(self, buffer: typing.List[int], offset: int, count: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        """
        Writes buffer into the stream. The operation completes synchronously.
        
        :param buffer: Buffer that will be written.
        :param offset: Starting index in the buffer.
        :param count: Number of bytes to write.
        :param cancellationToken: Token that can be used to cancel the operation.
        :returns: Task that can be awaited.
        """
        ...

    @typing.overload
    def WriteAsync(self, buffer: System.ReadOnlyMemory[int], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.ValueTask:
        """
        Writes buffer into the stream. The operation completes synchronously.
        
        :param buffer: Buffer that will be written.
        :param cancellationToken: Token that can be used to cancel the operation.
        """
        ...

    def WriteByte(self, value: int) -> None:
        """Writes a byte to the stream and advances the current Position."""
        ...


class UnmanagedMemoryAccessor(System.Object, System.IDisposable):
    """This class has no documentation."""

    @property
    def Capacity(self) -> int:
        ...

    @property
    def CanRead(self) -> bool:
        ...

    @property
    def CanWrite(self) -> bool:
        ...

    @property
    def IsOpen(self) -> bool:
        """This property is protected."""
        ...

    @typing.overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, buffer: System.Runtime.InteropServices.SafeBuffer, offset: int, capacity: int) -> None:
        ...

    @typing.overload
    def __init__(self, buffer: System.Runtime.InteropServices.SafeBuffer, offset: int, capacity: int, access: System.IO.FileAccess) -> None:
        ...

    def Initialize(self, buffer: System.Runtime.InteropServices.SafeBuffer, offset: int, capacity: int, access: System.IO.FileAccess) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    def ReadBoolean(self, position: int) -> bool:
        ...

    def ReadByte(self, position: int) -> int:
        ...

    def ReadChar(self, position: int) -> str:
        ...

    def ReadInt16(self, position: int) -> int:
        ...

    def ReadInt32(self, position: int) -> int:
        ...

    def ReadInt64(self, position: int) -> int:
        ...

    def ReadDecimal(self, position: int) -> float:
        ...

    def ReadSingle(self, position: int) -> float:
        ...

    def ReadDouble(self, position: int) -> float:
        ...

    def ReadSByte(self, position: int) -> int:
        ...

    def ReadUInt16(self, position: int) -> int:
        ...

    def ReadUInt32(self, position: int) -> int:
        ...

    def ReadUInt64(self, position: int) -> int:
        ...

    def Read(self, position: int, structure: System_IO_UnmanagedMemoryAccessor_Read_T) -> None:
        ...

    def ReadArray(self, position: int, array: typing.List[System_IO_UnmanagedMemoryAccessor_ReadArray_T], offset: int, count: int) -> int:
        ...

    @typing.overload
    def Write(self, position: int, value: bool) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: int) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: str) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: int) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: int) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: int) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: float) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: float) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: float) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: int) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: int) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: int) -> None:
        ...

    @typing.overload
    def Write(self, position: int, value: int) -> None:
        ...

    @typing.overload
    def Write(self, position: int, structure: System_IO_UnmanagedMemoryAccessor_Write_T) -> None:
        ...

    def WriteArray(self, position: int, array: typing.List[System_IO_UnmanagedMemoryAccessor_WriteArray_T], offset: int, count: int) -> None:
        ...


class StringReader(System.IO.TextReader):
    """This class has no documentation."""

    def __init__(self, s: str) -> None:
        ...

    def Close(self) -> None:
        ...

    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    def Peek(self) -> int:
        ...

    @typing.overload
    def Read(self) -> int:
        ...

    @typing.overload
    def Read(self, buffer: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def Read(self, buffer: System.Span[str]) -> int:
        ...

    def ReadBlock(self, buffer: System.Span[str]) -> int:
        ...

    def ReadToEnd(self) -> str:
        ...

    def ReadLine(self) -> str:
        ...

    def ReadLineAsync(self) -> System.Threading.Tasks.Task[str]:
        ...

    def ReadToEndAsync(self) -> System.Threading.Tasks.Task[str]:
        ...

    @typing.overload
    def ReadBlockAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task[int]:
        ...

    @typing.overload
    def ReadBlockAsync(self, buffer: System.Memory[str], cancellationToken: System.Threading.CancellationToken = ...) -> ValueTask:
        ...

    @typing.overload
    def ReadAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task[int]:
        ...

    @typing.overload
    def ReadAsync(self, buffer: System.Memory[str], cancellationToken: System.Threading.CancellationToken = ...) -> ValueTask:
        ...


class TextWriter(System.MarshalByRefObject, System.IDisposable, System.IAsyncDisposable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    Null: System.IO.TextWriter = ...

    @property
    def CoreNewLine(self) -> typing.List[str]:
        """
        This is the 'NewLine' property expressed as a char[].
        It is exposed to subclasses as a protected field for read-only
        purposes.  You should only modify it by using the 'NewLine' property.
        In particular you should never modify the elements of the array
        as they are shared among many instances of TextWriter.
        
        This field is protected.
        """
        ...

    @CoreNewLine.setter
    def CoreNewLine(self, value: typing.List[str]):
        """
        This is the 'NewLine' property expressed as a char[].
        It is exposed to subclasses as a protected field for read-only
        purposes.  You should only modify it by using the 'NewLine' property.
        In particular you should never modify the elements of the array
        as they are shared among many instances of TextWriter.
        
        This field is protected.
        """
        ...

    @property
    def FormatProvider(self) -> System.IFormatProvider:
        ...

    @property
    @abc.abstractmethod
    def Encoding(self) -> System.Text.Encoding:
        ...

    @property
    def NewLine(self) -> str:
        """
        Returns the line terminator string used by this TextWriter. The default line
        terminator string is Environment.NewLine, which is platform specific.
        On Windows this is a carriage return followed by a line feed ("\\r\\n").
        On OSX and Linux this is a line feed ("\\n").
        """
        ...

    @NewLine.setter
    def NewLine(self, value: str):
        """
        Returns the line terminator string used by this TextWriter. The default line
        terminator string is Environment.NewLine, which is platform specific.
        On Windows this is a carriage return followed by a line feed ("\\r\\n").
        On OSX and Linux this is a line feed ("\\n").
        """
        ...

    @property
    def t(self) -> typing.Any:
        ...

    @t.setter
    def t(self, value: typing.Any):
        ...

    @typing.overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, formatProvider: System.IFormatProvider) -> None:
        """This method is protected."""
        ...

    def Close(self) -> None:
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    def DisposeAsync(self) -> System.Threading.Tasks.ValueTask:
        ...

    def Flush(self) -> None:
        ...

    @typing.overload
    def Write(self, value: str) -> None:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[str]) -> None:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[str], index: int, count: int) -> None:
        ...

    @typing.overload
    def Write(self, buffer: System.ReadOnlySpan[str]) -> None:
        ...

    @typing.overload
    def Write(self, value: bool) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: float) -> None:
        ...

    @typing.overload
    def Write(self, value: float) -> None:
        ...

    @typing.overload
    def Write(self, value: float) -> None:
        ...

    @typing.overload
    def Write(self, value: str) -> None:
        ...

    @typing.overload
    def Write(self, value: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, value: System.Text.StringBuilder) -> None:
        """
        Equivalent to Write(stringBuilder.ToString()) however it uses the
        StringBuilder.GetChunks() method to avoid creating the intermediate string
        
        :param value: The string (as a StringBuilder) to write to the stream
        """
        ...

    @typing.overload
    def Write(self, format: str, arg0: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, arg0: typing.Any, arg1: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, *arg: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: str) -> None:
        ...

    @typing.overload
    def WriteLine(self, buffer: typing.List[str]) -> None:
        ...

    @typing.overload
    def WriteLine(self, buffer: typing.List[str], index: int, count: int) -> None:
        ...

    @typing.overload
    def WriteLine(self, buffer: System.ReadOnlySpan[str]) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: bool) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: int) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: int) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: int) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: int) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: float) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: float) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: float) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: str) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: System.Text.StringBuilder) -> None:
        """
        Equivalent to WriteLine(stringBuilder.ToString()) however it uses the
        StringBuilder.GetChunks() method to avoid creating the intermediate string
        """
        ...

    @typing.overload
    def WriteLine(self, value: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, arg0: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, arg0: typing.Any, arg1: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, *arg: typing.Any) -> None:
        ...

    def WriteAsync(self, value: str) -> System.Threading.Tasks.Task:
        ...


class StringWriter(System.IO.TextWriter):
    """This class has no documentation."""

    @property
    def Encoding(self) -> System.Text.Encoding:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, formatProvider: System.IFormatProvider) -> None:
        ...

    @typing.overload
    def __init__(self, sb: System.Text.StringBuilder) -> None:
        ...

    @typing.overload
    def __init__(self, sb: System.Text.StringBuilder, formatProvider: System.IFormatProvider) -> None:
        ...

    def Close(self) -> None:
        ...

    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    def GetStringBuilder(self) -> System.Text.StringBuilder:
        ...

    @typing.overload
    def Write(self, value: str) -> None:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[str], index: int, count: int) -> None:
        ...

    @typing.overload
    def Write(self, buffer: System.ReadOnlySpan[str]) -> None:
        ...

    @typing.overload
    def Write(self, value: str) -> None:
        ...

    @typing.overload
    def Write(self, value: System.Text.StringBuilder) -> None:
        ...

    @typing.overload
    def WriteLine(self, buffer: System.ReadOnlySpan[str]) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: System.Text.StringBuilder) -> None:
        ...

    @typing.overload
    def WriteAsync(self, value: str) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, value: str) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, buffer: System.ReadOnlyMemory[str], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, value: System.Text.StringBuilder, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self, value: str) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self, value: str) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self, value: System.Text.StringBuilder, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self, buffer: System.ReadOnlyMemory[str], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task:
        ...

    def FlushAsync(self) -> System.Threading.Tasks.Task:
        ...

    def ToString(self) -> str:
        ...


class Path(System.Object):
    """This class has no documentation."""

    IsCaseSensitive: bool
    """Gets whether the system is case-sensitive."""

    DirectorySeparatorChar: str = ...

    AltDirectorySeparatorChar: str = ...

    VolumeSeparatorChar: str = ...

    PathSeparator: str = ...

    InvalidPathChars: typing.List[str] = ...

    StringComparison: int
    """
    Returns a comparison that can be used to compare file and directory names for equality.
    
    This property contains the int value of a member of the System.StringComparison enum.
    """

    @staticmethod
    @typing.overload
    def GetInvalidFileNameChars() -> typing.List[str]:
        ...

    @staticmethod
    @typing.overload
    def GetInvalidPathChars() -> typing.List[str]:
        ...

    @staticmethod
    @typing.overload
    def GetFullPath(path: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def GetFullPath(path: str, basePath: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def GetTempPath() -> str:
        ...

    @staticmethod
    @typing.overload
    def GetTempFileName() -> str:
        ...

    @staticmethod
    @typing.overload
    def IsPathRooted(path: str) -> bool:
        ...

    @staticmethod
    @typing.overload
    def IsPathRooted(path: System.ReadOnlySpan[str]) -> bool:
        ...

    @staticmethod
    @typing.overload
    def GetPathRoot(path: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def GetPathRoot(path: System.ReadOnlySpan[str]) -> System.ReadOnlySpan[str]:
        ...

    @staticmethod
    @typing.overload
    def GetInvalidFileNameChars() -> typing.List[str]:
        ...

    @staticmethod
    @typing.overload
    def GetInvalidPathChars() -> typing.List[str]:
        ...

    @staticmethod
    @typing.overload
    def GetFullPath(path: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def GetFullPath(path: str, basePath: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def GetTempPath() -> str:
        ...

    @staticmethod
    @typing.overload
    def GetTempFileName() -> str:
        ...

    @staticmethod
    @typing.overload
    def IsPathRooted(path: str) -> bool:
        ...

    @staticmethod
    @typing.overload
    def IsPathRooted(path: System.ReadOnlySpan[str]) -> bool:
        ...

    @staticmethod
    @typing.overload
    def GetPathRoot(path: str) -> str:
        """Returns the path root or null if path is empty or null."""
        ...

    @staticmethod
    @typing.overload
    def GetPathRoot(path: System.ReadOnlySpan[str]) -> System.ReadOnlySpan[str]:
        ...

    @staticmethod
    def ChangeExtension(path: str, extension: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def GetDirectoryName(path: str) -> str:
        """
        Returns the directory portion of a file path. This method effectively
        removes the last segment of the given file path, i.e. it returns a
        string consisting of all characters up to but not including the last
        backslash ("\\") in the file path. The returned value is null if the
        specified path is null, empty, or a root (such as "\\", "C:", or
        "\\\\server\\share").
        """
        ...

    @staticmethod
    @typing.overload
    def GetDirectoryName(path: System.ReadOnlySpan[str]) -> System.ReadOnlySpan[str]:
        """
        Returns the directory portion of a file path. The returned value is empty
        if the specified path is null, empty, or a root (such as "\\", "C:", or
        "\\\\server\\share").
        """
        ...

    @staticmethod
    @typing.overload
    def GetExtension(path: str) -> str:
        """
        Returns the extension of the given path. The returned value includes the period (".") character of the
        extension except when you have a terminal period when you get string.Empty, such as ".exe" or ".cpp".
        The returned value is null if the given path is null or empty if the given path does not include an
        extension.
        """
        ...

    @staticmethod
    @typing.overload
    def GetExtension(path: System.ReadOnlySpan[str]) -> System.ReadOnlySpan[str]:
        """Returns the extension of the given path."""
        ...

    @staticmethod
    @typing.overload
    def GetFileName(path: str) -> str:
        """
        Returns the name and extension parts of the given path. The resulting string contains
        the characters of path that follow the last separator in path. The resulting string is
        null if path is null.
        """
        ...

    @staticmethod
    @typing.overload
    def GetFileName(path: System.ReadOnlySpan[str]) -> System.ReadOnlySpan[str]:
        """The returned ReadOnlySpan contains the characters of the path that follows the last separator in path."""
        ...

    @staticmethod
    @typing.overload
    def GetFileNameWithoutExtension(path: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def GetFileNameWithoutExtension(path: System.ReadOnlySpan[str]) -> System.ReadOnlySpan[str]:
        """Returns the characters between the last separator and last (.) in the path."""
        ...

    @staticmethod
    def GetRandomFileName() -> str:
        """
        Returns a cryptographically strong random 8.3 string that can be
        used as either a folder name or a file name.
        """
        ...

    @staticmethod
    @typing.overload
    def IsPathFullyQualified(path: str) -> bool:
        """
        Returns true if the path is fixed to a specific drive or UNC path. This method does no
        validation of the path (URIs will be returned as relative as a result).
        Returns false if the path specified is relative to the current drive or working directory.
        """
        ...

    @staticmethod
    @typing.overload
    def IsPathFullyQualified(path: System.ReadOnlySpan[str]) -> bool:
        ...

    @staticmethod
    @typing.overload
    def HasExtension(path: str) -> bool:
        """
        Tests if a path's file name includes a file extension. A trailing period
        is not considered an extension.
        """
        ...

    @staticmethod
    @typing.overload
    def HasExtension(path: System.ReadOnlySpan[str]) -> bool:
        ...

    @staticmethod
    @typing.overload
    def Combine(path1: str, path2: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def Combine(path1: str, path2: str, path3: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def Combine(path1: str, path2: str, path3: str, path4: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def Combine(*paths: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def Join(path1: System.ReadOnlySpan[str], path2: System.ReadOnlySpan[str]) -> str:
        ...

    @staticmethod
    @typing.overload
    def Join(path1: System.ReadOnlySpan[str], path2: System.ReadOnlySpan[str], path3: System.ReadOnlySpan[str]) -> str:
        ...

    @staticmethod
    @typing.overload
    def Join(path1: System.ReadOnlySpan[str], path2: System.ReadOnlySpan[str], path3: System.ReadOnlySpan[str], path4: System.ReadOnlySpan[str]) -> str:
        ...

    @staticmethod
    @typing.overload
    def Join(path1: str, path2: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def Join(path1: str, path2: str, path3: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def Join(path1: str, path2: str, path3: str, path4: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def Join(*paths: str) -> str:
        ...

    @staticmethod
    @typing.overload
    def TryJoin(path1: System.ReadOnlySpan[str], path2: System.ReadOnlySpan[str], destination: System.Span[str], charsWritten: int) -> bool:
        ...

    @staticmethod
    @typing.overload
    def TryJoin(path1: System.ReadOnlySpan[str], path2: System.ReadOnlySpan[str], path3: System.ReadOnlySpan[str], destination: System.Span[str], charsWritten: int) -> bool:
        ...

    @staticmethod
    def GetRelativePath(relativeTo: str, path: str) -> str:
        """
        Create a relative path from one path to another. Paths will be resolved before calculating the difference.
        Default path comparison for the active platform will be used (OrdinalIgnoreCase for Windows or Mac, Ordinal for Unix).
        
        :param relativeTo: The source path the output should be relative to. This path is always considered to be a directory.
        :param path: The destination path.
        :returns: The relative path or  if the paths don't share the same root.
        """
        ...

    @staticmethod
    @typing.overload
    def TrimEndingDirectorySeparator(path: str) -> str:
        """Trims one trailing directory separator beyond the root of the path."""
        ...

    @staticmethod
    @typing.overload
    def TrimEndingDirectorySeparator(path: System.ReadOnlySpan[str]) -> System.ReadOnlySpan[str]:
        """Trims one trailing directory separator beyond the root of the path."""
        ...

    @staticmethod
    @typing.overload
    def EndsInDirectorySeparator(path: System.ReadOnlySpan[str]) -> bool:
        """Returns true if the path ends in a directory separator."""
        ...

    @staticmethod
    @typing.overload
    def EndsInDirectorySeparator(path: str) -> bool:
        """Returns true if the path ends in a directory separator."""
        ...


class StreamReader(System.IO.TextReader):
    """This class has no documentation."""

    Null: System.IO.StreamReader = ...

    @property
    def CurrentEncoding(self) -> System.Text.Encoding:
        ...

    @property
    def BaseStream(self) -> System.IO.Stream:
        ...

    @property
    def EndOfStream(self) -> bool:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream, detectEncodingFromByteOrderMarks: bool) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream, encoding: System.Text.Encoding) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream, encoding: System.Text.Encoding, detectEncodingFromByteOrderMarks: bool) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream, encoding: System.Text.Encoding, detectEncodingFromByteOrderMarks: bool, bufferSize: int) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream, encoding: System.Text.Encoding = None, detectEncodingFromByteOrderMarks: bool = True, bufferSize: int = -1, leaveOpen: bool = False) -> None:
        ...

    @typing.overload
    def __init__(self, path: str) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, detectEncodingFromByteOrderMarks: bool) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, encoding: System.Text.Encoding) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, encoding: System.Text.Encoding, detectEncodingFromByteOrderMarks: bool) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, encoding: System.Text.Encoding, detectEncodingFromByteOrderMarks: bool, bufferSize: int) -> None:
        ...

    def Close(self) -> None:
        ...

    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    def DiscardBufferedData(self) -> None:
        ...

    def Peek(self) -> int:
        ...

    @typing.overload
    def Read(self) -> int:
        ...

    @typing.overload
    def Read(self, buffer: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def Read(self, buffer: System.Span[str]) -> int:
        ...

    def ReadToEnd(self) -> str:
        ...

    @typing.overload
    def ReadBlock(self, buffer: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def ReadBlock(self, buffer: System.Span[str]) -> int:
        ...

    def ReadLine(self) -> str:
        ...

    def ReadLineAsync(self) -> System.Threading.Tasks.Task[str]:
        ...

    def ReadToEndAsync(self) -> System.Threading.Tasks.Task[str]:
        ...

    @typing.overload
    def ReadAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task[int]:
        ...

    @typing.overload
    def ReadAsync(self, buffer: System.Memory[str], cancellationToken: System.Threading.CancellationToken = ...) -> ValueTask:
        ...

    @typing.overload
    def ReadBlockAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task[int]:
        ...

    @typing.overload
    def ReadBlockAsync(self, buffer: System.Memory[str], cancellationToken: System.Threading.CancellationToken = ...) -> ValueTask:
        ...


class FileShare(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    Read = 1

    Write = 2

    ReadWrite = 3

    Delete = 4

    Inheritable = ...


class FileStream(System.IO.Stream):
    """This class has no documentation."""

    DefaultBufferSize: int = 4096

    @property
    def Handle(self) -> System.IntPtr:
        ...

    @property
    def CanRead(self) -> bool:
        """Gets a value indicating whether the current stream supports reading."""
        ...

    @property
    def CanWrite(self) -> bool:
        """Gets a value indicating whether the current stream supports writing."""
        ...

    @property
    def SafeFileHandle(self) -> Microsoft.Win32.SafeHandles.SafeFileHandle:
        ...

    @property
    def Name(self) -> str:
        """Gets the path that was passed to the constructor."""
        ...

    @property
    def IsAsync(self) -> bool:
        """Gets a value indicating whether the stream was opened for I/O to be performed synchronously or asynchronously."""
        ...

    @property
    def Length(self) -> int:
        """Gets the length of the stream in bytes."""
        ...

    @property
    def Position(self) -> int:
        """Gets or sets the position within the current stream"""
        ...

    @Position.setter
    def Position(self, value: int):
        """Gets or sets the position within the current stream"""
        ...

    @property
    def CanSeek(self) -> bool:
        ...

    @typing.overload
    def __init__(self, handle: System.IntPtr, access: System.IO.FileAccess) -> None:
        ...

    @typing.overload
    def __init__(self, handle: System.IntPtr, access: System.IO.FileAccess, ownsHandle: bool) -> None:
        ...

    @typing.overload
    def __init__(self, handle: System.IntPtr, access: System.IO.FileAccess, ownsHandle: bool, bufferSize: int) -> None:
        ...

    @typing.overload
    def __init__(self, handle: System.IntPtr, access: System.IO.FileAccess, ownsHandle: bool, bufferSize: int, isAsync: bool) -> None:
        ...

    @typing.overload
    def __init__(self, handle: Microsoft.Win32.SafeHandles.SafeFileHandle, access: System.IO.FileAccess) -> None:
        ...

    @typing.overload
    def __init__(self, handle: Microsoft.Win32.SafeHandles.SafeFileHandle, access: System.IO.FileAccess, bufferSize: int) -> None:
        ...

    @typing.overload
    def __init__(self, handle: Microsoft.Win32.SafeHandles.SafeFileHandle, access: System.IO.FileAccess, bufferSize: int, isAsync: bool) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, mode: System.IO.FileMode) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, mode: System.IO.FileMode, access: System.IO.FileAccess) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, mode: System.IO.FileMode, access: System.IO.FileAccess, share: System.IO.FileShare) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, mode: System.IO.FileMode, access: System.IO.FileAccess, share: System.IO.FileShare, bufferSize: int) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, mode: System.IO.FileMode, access: System.IO.FileAccess, share: System.IO.FileShare, bufferSize: int, useAsync: bool) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, mode: System.IO.FileMode, access: System.IO.FileAccess, share: System.IO.FileShare, bufferSize: int, options: System.IO.FileOptions) -> None:
        ...

    def Lock(self, position: int, length: int) -> None:
        ...

    def Unlock(self, position: int, length: int) -> None:
        ...

    def FlushAsync(self, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def Read(self, buffer: typing.List[int], offset: int, count: int) -> int:
        ...

    @typing.overload
    def Read(self, buffer: System.Span[int]) -> int:
        ...

    @typing.overload
    def ReadAsync(self, buffer: typing.List[int], offset: int, count: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[int]:
        ...

    @typing.overload
    def ReadAsync(self, buffer: System.Memory[int], cancellationToken: System.Threading.CancellationToken = ...) -> ValueTask:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[int], offset: int, count: int) -> None:
        ...

    @typing.overload
    def Write(self, buffer: System.ReadOnlySpan[int]) -> None:
        ...

    @typing.overload
    def WriteAsync(self, buffer: typing.List[int], offset: int, count: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, buffer: System.ReadOnlyMemory[int], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.ValueTask:
        ...

    @typing.overload
    def Flush(self) -> None:
        """Clears buffers for this stream and causes any buffered data to be written to the file."""
        ...

    @typing.overload
    def Flush(self, flushToDisk: bool) -> None:
        """
        Clears buffers for this stream, and if  is true,
        causes any buffered data to be written to the file.
        """
        ...

    def SetLength(self, value: int) -> None:
        """
        Sets the length of this stream to the given value.
        
        :param value: The new length of the stream.
        """
        ...

    def ReadByte(self) -> int:
        """
        Reads a byte from the file stream.  Returns the byte cast to an int
        or -1 if reading from the end of the stream.
        """
        ...

    def WriteByte(self, value: int) -> None:
        """
        Writes a byte to the current position in the stream and advances the position
        within the stream by one byte.
        
        :param value: The byte to write to the stream.
        """
        ...

    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    def DisposeAsync(self) -> System.Threading.Tasks.ValueTask:
        ...

    def CopyToAsync(self, destination: System.IO.Stream, bufferSize: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    def BeginRead(self, buffer: typing.List[int], offset: int, count: int, callback: System_AsyncCallback, state: typing.Any) -> System.IAsyncResult:
        ...

    def EndRead(self, asyncResult: System.IAsyncResult) -> int:
        ...

    def BeginWrite(self, buffer: typing.List[int], offset: int, count: int, callback: System_AsyncCallback, state: typing.Any) -> System.IAsyncResult:
        ...

    def EndWrite(self, asyncResult: System.IAsyncResult) -> None:
        ...

    def Seek(self, offset: int, origin: System.IO.SeekOrigin) -> int:
        ...


class BinaryWriter(System.Object, System.IDisposable, System.IAsyncDisposable):
    """This class has no documentation."""

    Null: System.IO.BinaryWriter = ...

    @property
    def OutStream(self) -> System.IO.Stream:
        """This field is protected."""
        ...

    @OutStream.setter
    def OutStream(self, value: System.IO.Stream):
        """This field is protected."""
        ...

    @property
    def BaseStream(self) -> System.IO.Stream:
        ...

    @typing.overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, output: System.IO.Stream) -> None:
        ...

    @typing.overload
    def __init__(self, output: System.IO.Stream, encoding: System.Text.Encoding) -> None:
        ...

    @typing.overload
    def __init__(self, output: System.IO.Stream, encoding: System.Text.Encoding, leaveOpen: bool) -> None:
        ...

    def Close(self) -> None:
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    def DisposeAsync(self) -> System.Threading.Tasks.ValueTask:
        ...

    def Flush(self) -> None:
        ...

    def Seek(self, offset: int, origin: System.IO.SeekOrigin) -> int:
        ...

    @typing.overload
    def Write(self, value: bool) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[int]) -> None:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[int], index: int, count: int) -> None:
        ...

    @typing.overload
    def Write(self, ch: str) -> None:
        ...

    @typing.overload
    def Write(self, chars: typing.List[str]) -> None:
        ...

    @typing.overload
    def Write(self, chars: typing.List[str], index: int, count: int) -> None:
        ...

    @typing.overload
    def Write(self, value: float) -> None:
        ...

    @typing.overload
    def Write(self, value: float) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: float) -> None:
        ...

    @typing.overload
    def Write(self, value: System.Half) -> None:
        ...

    @typing.overload
    def Write(self, value: str) -> None:
        ...

    @typing.overload
    def Write(self, buffer: System.ReadOnlySpan[int]) -> None:
        ...

    @typing.overload
    def Write(self, chars: System.ReadOnlySpan[str]) -> None:
        ...

    def Write7BitEncodedInt(self, value: int) -> None:
        ...

    def Write7BitEncodedInt64(self, value: int) -> None:
        ...


class MemoryStream(System.IO.Stream):
    """This class has no documentation."""

    @property
    def CanRead(self) -> bool:
        ...

    @property
    def CanSeek(self) -> bool:
        ...

    @property
    def CanWrite(self) -> bool:
        ...

    @property
    def Capacity(self) -> int:
        ...

    @Capacity.setter
    def Capacity(self, value: int):
        ...

    @property
    def Length(self) -> int:
        ...

    @property
    def Position(self) -> int:
        ...

    @Position.setter
    def Position(self, value: int):
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, capacity: int) -> None:
        ...

    @typing.overload
    def __init__(self, buffer: typing.List[int]) -> None:
        ...

    @typing.overload
    def __init__(self, buffer: typing.List[int], writable: bool) -> None:
        ...

    @typing.overload
    def __init__(self, buffer: typing.List[int], index: int, count: int) -> None:
        ...

    @typing.overload
    def __init__(self, buffer: typing.List[int], index: int, count: int, writable: bool) -> None:
        ...

    @typing.overload
    def __init__(self, buffer: typing.List[int], index: int, count: int, writable: bool, publiclyVisible: bool) -> None:
        ...

    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    def Flush(self) -> None:
        ...

    def FlushAsync(self, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    def GetBuffer(self) -> typing.List[int]:
        ...

    def TryGetBuffer(self, buffer: System.ArraySegment[int]) -> bool:
        ...

    @typing.overload
    def Read(self, buffer: typing.List[int], offset: int, count: int) -> int:
        ...

    @typing.overload
    def Read(self, buffer: System.Span[int]) -> int:
        ...

    @typing.overload
    def ReadAsync(self, buffer: typing.List[int], offset: int, count: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task[int]:
        ...

    @typing.overload
    def ReadAsync(self, buffer: System.Memory[int], cancellationToken: System.Threading.CancellationToken = ...) -> ValueTask:
        ...

    def ReadByte(self) -> int:
        ...

    def CopyTo(self, destination: System.IO.Stream, bufferSize: int) -> None:
        ...

    def CopyToAsync(self, destination: System.IO.Stream, bufferSize: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    def Seek(self, offset: int, loc: System.IO.SeekOrigin) -> int:
        ...

    def SetLength(self, value: int) -> None:
        ...

    def ToArray(self) -> typing.List[int]:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[int], offset: int, count: int) -> None:
        ...

    @typing.overload
    def Write(self, buffer: System.ReadOnlySpan[int]) -> None:
        ...

    @typing.overload
    def WriteAsync(self, buffer: typing.List[int], offset: int, count: int, cancellationToken: System.Threading.CancellationToken) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, buffer: System.ReadOnlyMemory[int], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.ValueTask:
        ...

    def WriteByte(self, value: int) -> None:
        ...

    def WriteTo(self, stream: System.IO.Stream) -> None:
        ...


class FileNotFoundException(System.IO.IOException):
    """This class has no documentation."""

    @property
    def Message(self) -> str:
        ...

    @property
    def FileName(self) -> str:
        ...

    @property
    def FusionLog(self) -> str:
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
    def __init__(self, message: str, fileName: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, fileName: str, innerException: System.Exception) -> None:
        ...

    def ToString(self) -> str:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...


class InvalidDataException(System.SystemException):
    """This class has no documentation."""

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...


class HandleInheritability(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    Inheritable = 1


class StreamWriter(System.IO.TextWriter):
    """This class has no documentation."""

    Null: System.IO.StreamWriter = ...

    @property
    def AutoFlush(self) -> bool:
        ...

    @AutoFlush.setter
    def AutoFlush(self, value: bool):
        ...

    @property
    def BaseStream(self) -> System.IO.Stream:
        ...

    @property
    def Encoding(self) -> System.Text.Encoding:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream, encoding: System.Text.Encoding) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream, encoding: System.Text.Encoding, bufferSize: int) -> None:
        ...

    @typing.overload
    def __init__(self, stream: System.IO.Stream, encoding: System.Text.Encoding = None, bufferSize: int = -1, leaveOpen: bool = False) -> None:
        ...

    @typing.overload
    def __init__(self, path: str) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, append: bool) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, append: bool, encoding: System.Text.Encoding) -> None:
        ...

    @typing.overload
    def __init__(self, path: str, append: bool, encoding: System.Text.Encoding, bufferSize: int) -> None:
        ...

    def Close(self) -> None:
        ...

    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    def DisposeAsync(self) -> System.Threading.Tasks.ValueTask:
        ...

    def Flush(self) -> None:
        ...

    @typing.overload
    def Write(self, value: str) -> None:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[str]) -> None:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[str], index: int, count: int) -> None:
        ...

    @typing.overload
    def Write(self, buffer: System.ReadOnlySpan[str]) -> None:
        ...

    @typing.overload
    def Write(self, value: str) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: str) -> None:
        ...

    @typing.overload
    def WriteLine(self, buffer: System.ReadOnlySpan[str]) -> None:
        ...

    @typing.overload
    def Write(self, format: str, arg0: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, arg0: typing.Any, arg1: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, *arg: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, arg0: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, arg0: typing.Any, arg1: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, *arg: typing.Any) -> None:
        ...

    @typing.overload
    def WriteAsync(self, value: str) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, value: str) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteAsync(self, buffer: System.ReadOnlyMemory[str], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self, value: str) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self, value: str) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self, buffer: System.ReadOnlyMemory[str], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task:
        ...

    def FlushAsync(self) -> System.Threading.Tasks.Task:
        ...


class FileAttributes(System.Enum):
    """This class has no documentation."""

    ReadOnly = ...

    Hidden = ...

    System = ...

    Directory = ...

    Archive = ...

    Device = ...

    Normal = ...

    Temporary = ...

    SparseFile = ...

    ReparsePoint = ...

    Compressed = ...

    Offline = ...

    NotContentIndexed = ...

    Encrypted = ...

    IntegrityStream = ...

    NoScrubData = ...


class BinaryReader(System.Object, System.IDisposable):
    """This class has no documentation."""

    @property
    def BaseStream(self) -> System.IO.Stream:
        ...

    @typing.overload
    def __init__(self, input: System.IO.Stream) -> None:
        ...

    @typing.overload
    def __init__(self, input: System.IO.Stream, encoding: System.Text.Encoding) -> None:
        ...

    @typing.overload
    def __init__(self, input: System.IO.Stream, encoding: System.Text.Encoding, leaveOpen: bool) -> None:
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    def Close(self) -> None:
        ...

    def PeekChar(self) -> int:
        ...

    @typing.overload
    def Read(self) -> int:
        ...

    def ReadByte(self) -> int:
        ...

    def ReadSByte(self) -> int:
        ...

    def ReadBoolean(self) -> bool:
        ...

    def ReadChar(self) -> str:
        ...

    def ReadInt16(self) -> int:
        ...

    def ReadUInt16(self) -> int:
        ...

    def ReadInt32(self) -> int:
        ...

    def ReadUInt32(self) -> int:
        ...

    def ReadInt64(self) -> int:
        ...

    def ReadUInt64(self) -> int:
        ...

    def ReadHalf(self) -> System.Half:
        ...

    def ReadSingle(self) -> float:
        ...

    def ReadDouble(self) -> float:
        ...

    def ReadDecimal(self) -> float:
        ...

    def ReadString(self) -> str:
        ...

    @typing.overload
    def Read(self, buffer: typing.List[str], index: int, count: int) -> int:
        ...

    @typing.overload
    def Read(self, buffer: System.Span[str]) -> int:
        ...

    def ReadChars(self, count: int) -> typing.List[str]:
        ...

    @typing.overload
    def Read(self, buffer: typing.List[int], index: int, count: int) -> int:
        ...

    @typing.overload
    def Read(self, buffer: System.Span[int]) -> int:
        ...

    def ReadBytes(self, count: int) -> typing.List[int]:
        ...

    def FillBuffer(self, numBytes: int) -> None:
        """This method is protected."""
        ...

    def Read7BitEncodedInt(self) -> int:
        ...

    def Read7BitEncodedInt64(self) -> int:
        ...


