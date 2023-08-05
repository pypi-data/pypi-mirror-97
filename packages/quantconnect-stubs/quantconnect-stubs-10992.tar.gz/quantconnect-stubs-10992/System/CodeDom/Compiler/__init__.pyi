import typing

import System
import System.CodeDom.Compiler
import System.IO
import System.Text
import System.Threading
import System.Threading.Tasks


class GeneratedCodeAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Tool(self) -> str:
        ...

    @property
    def Version(self) -> str:
        ...

    def __init__(self, tool: str, version: str) -> None:
        ...


class IndentedTextWriter(System.IO.TextWriter):
    """This class has no documentation."""

    DefaultTabString: str = "    "

    @property
    def Encoding(self) -> System.Text.Encoding:
        ...

    @property
    def NewLine(self) -> str:
        ...

    @NewLine.setter
    def NewLine(self, value: str):
        ...

    @property
    def Indent(self) -> int:
        ...

    @Indent.setter
    def Indent(self, value: int):
        ...

    @property
    def InnerWriter(self) -> System.IO.TextWriter:
        ...

    @typing.overload
    def __init__(self, writer: System.IO.TextWriter) -> None:
        ...

    @typing.overload
    def __init__(self, writer: System.IO.TextWriter, tabString: str) -> None:
        ...

    def Close(self) -> None:
        ...

    def DisposeAsync(self) -> System.Threading.Tasks.ValueTask:
        ...

    def Flush(self) -> None:
        ...

    def FlushAsync(self) -> System.Threading.Tasks.Task:
        ...

    def OutputTabs(self) -> None:
        """This method is protected."""
        ...

    def OutputTabsAsync(self) -> System.Threading.Tasks.Task:
        """
        Asynchronously outputs tabs to the underlying TextWriter based on the current Indent.
        
        This method is protected.
        
        :returns: A Task representing the asynchronous operation.
        """
        ...

    @typing.overload
    def Write(self, s: str) -> None:
        ...

    @typing.overload
    def Write(self, value: bool) -> None:
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
    def Write(self, value: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, arg0: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, arg0: typing.Any, arg1: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, *arg: typing.Any) -> None:
        ...

    @typing.overload
    def WriteAsync(self, value: str) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified char to the underlying TextWriter, inserting
        tabs at the start of every line.
        
        :param value: The char to write.
        :returns: A Task representing the asynchronous operation.
        """
        ...

    @typing.overload
    def WriteAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified number of chars from the specified buffer
        to the underlying TextWriter, starting at the specified index, and outputting tabs at the
        start of every new line.
        
        :param buffer: The array to write from.
        :param index: Index in the array to stort writing at.
        :param count: The number of characters to write.
        :returns: A Task representing the asynchronous operation.
        """
        ...

    @typing.overload
    def WriteAsync(self, value: str) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified value to the underlying TextWriter, inserting tabs at the
        start of every line.
        
        :param value: The value to write.
        :returns: A Task representing the asynchronous operation.
        """
        ...

    @typing.overload
    def WriteAsync(self, buffer: System.ReadOnlyMemory[str], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified buffer to the underlying TextWriter, inserting tabs at the
        start of every line.
        
        :param buffer: The buffer to write.
        :param cancellationToken: Token for canceling the operation.
        :returns: A Task representing the asynchronous operation.
        """
        ...

    @typing.overload
    def WriteAsync(self, value: System.Text.StringBuilder, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified StringBuilder to the underlying TextWriter, inserting tabs at the
        start of every line.
        
        :param value: The value to write.
        :param cancellationToken: Token for canceling the operation.
        :returns: A Task representing the asynchronous operation.
        """
        ...

    def WriteLineNoTabs(self, s: str) -> None:
        ...

    def WriteLineNoTabsAsync(self, s: str) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified text to the underlying TextWriter without inserting tabs.
        
        :param s: The text to write.
        :returns: A Task representing the asynchronous operation.
        """
        ...

    @typing.overload
    def WriteLine(self, s: str) -> None:
        ...

    @typing.overload
    def WriteLine(self) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: bool) -> None:
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
    def WriteLine(self, value: float) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: float) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: int) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: int) -> None:
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
    def WriteLine(self, format: str, *arg: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: int) -> None:
        ...

    @typing.overload
    def WriteLineAsync(self) -> System.Threading.Tasks.Task:
        ...

    @typing.overload
    def WriteLineAsync(self, value: str) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified char to the underlying TextWriter followed by a line terminator, inserting tabs
        at the start of every line.
        
        :param value: The value to write.
        :returns: A Task representing the asynchronous operation.
        """
        ...

    @typing.overload
    def WriteLineAsync(self, buffer: typing.List[str], index: int, count: int) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified number of characters from the specified buffer followed by a line terminator,
        to the underlying TextWriter, starting at the specified index within the buffer, inserting tabs at the start of every line.
        
        :param buffer: The buffer to write from.
        :param index: The index within the buffer to start writing at.
        :param count: The number of characters to write.
        :returns: A Task representing the asynchronous operation.
        """
        ...

    @typing.overload
    def WriteLineAsync(self, value: str) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified value followed by a line terminator to the underlying TextWriter, inserting
        tabs at the start of every line.
        
        :param value: The value to write.
        :returns: A Task representing the asynchronous operation.
        """
        ...

    @typing.overload
    def WriteLineAsync(self, buffer: System.ReadOnlyMemory[str], cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified buffer followed by a line terminator to the underlying TextWriter, inserting
        tabs at the start of every line.
        
        :param buffer: The buffer to write from.
        :param cancellationToken: Token for canceling the operation.
        :returns: A Task representing the asynchronous operation.
        """
        ...

    @typing.overload
    def WriteLineAsync(self, value: System.Text.StringBuilder, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task:
        """
        Asynchronously writes the specified text followed by a line terminator to the underlying TextWriter, inserting
        tabs at the start of every line.
        
        :param value: The text to write.
        :param cancellationToken: Token for canceling the operation.
        :returns: A Task representing the asynchronous operation.
        """
        ...


