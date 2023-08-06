import typing

import System
import System.ComponentModel


class DefaultValueAttribute(System.Attribute):
    """Specifies the default value for a property."""

    @property
    def Value(self) -> System.Object:
        """Gets the default value of the property this attribute is bound to."""
        ...

    @typing.overload
    def __init__(self, type: typing.Type, value: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class, converting the specified value to the specified type, and using the U.S. English
        culture as the translation context.
        """
        ...

    @typing.overload
    def __init__(self, value: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a Unicode character.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using an 8-bit unsigned integer.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a 16-bit signed integer.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a 32-bit signed integer.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a 64-bit signed integer.
        """
        ...

    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a single-precision floating point number.
        """
        ...

    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a double-precision floating point number.
        """
        ...

    @typing.overload
    def __init__(self, value: bool) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a bool value.
        """
        ...

    @typing.overload
    def __init__(self, value: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a string.
        """
        ...

    @typing.overload
    def __init__(self, value: typing.Any) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a sbyte value.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a ushort value.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a uint value.
        """
        ...

    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.DefaultValueAttribute
        class using a ulong value.
        """
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def SetValue(self, value: typing.Any) -> None:
        """This method is protected."""
        ...


class EditorBrowsableState(System.Enum):
    """This class has no documentation."""

    Always = 0

    Never = 1

    Advanced = 2


class EditorBrowsableAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def State(self) -> int:
        """This property contains the int value of a member of the System.ComponentModel.EditorBrowsableState enum."""
        ...

    @typing.overload
    def __init__(self, state: System.ComponentModel.EditorBrowsableState) -> None:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


