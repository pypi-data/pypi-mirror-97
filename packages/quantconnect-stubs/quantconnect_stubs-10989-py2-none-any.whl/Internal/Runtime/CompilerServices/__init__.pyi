import typing

import Internal.Runtime.CompilerServices
import System

Internal_Runtime_CompilerServices_Unsafe_AsPointer_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_AsPointer_T")
Internal_Runtime_CompilerServices_Unsafe_As_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_As_T")
Internal_Runtime_CompilerServices_Unsafe_As_TFrom = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_As_TFrom")
Internal_Runtime_CompilerServices_Unsafe_Add_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_Add_T")
Internal_Runtime_CompilerServices_Unsafe_AreSame_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_AreSame_T")
Internal_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T")
Internal_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T")
Internal_Runtime_CompilerServices_Unsafe_ReadUnaligned_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_ReadUnaligned_T")
Internal_Runtime_CompilerServices_Unsafe_WriteUnaligned_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_WriteUnaligned_T")
Internal_Runtime_CompilerServices_Unsafe_AddByteOffset_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_AddByteOffset_T")
Internal_Runtime_CompilerServices_Unsafe_Read_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_Read_T")
Internal_Runtime_CompilerServices_Unsafe_Write_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_Write_T")
Internal_Runtime_CompilerServices_Unsafe_AsRef_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_AsRef_T")
Internal_Runtime_CompilerServices_Unsafe_ByteOffset_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_ByteOffset_T")
Internal_Runtime_CompilerServices_Unsafe_IsNullRef_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_IsNullRef_T")
Internal_Runtime_CompilerServices_Unsafe_SkipInit_T = typing.TypeVar("Internal_Runtime_CompilerServices_Unsafe_SkipInit_T")


class Unsafe(System.Object):
    """This class has no documentation."""

    @staticmethod
    def AsPointer(value: Internal_Runtime_CompilerServices_Unsafe_AsPointer_T) -> typing.Any:
        """Returns a pointer to the given by-ref parameter."""
        ...

    @staticmethod
    def SizeOf() -> int:
        """Returns the size of an object of the given type parameter."""
        ...

    @staticmethod
    @typing.overload
    def As(value: typing.Any) -> Internal_Runtime_CompilerServices_Unsafe_As_T:
        """Casts the given object to the specified type, performs no dynamic type checking."""
        ...

    @staticmethod
    @typing.overload
    def As(source: Internal_Runtime_CompilerServices_Unsafe_As_TFrom) -> typing.Any:
        """Reinterprets the given reference as a reference to a value of type TTo."""
        ...

    @staticmethod
    @typing.overload
    def Add(source: Internal_Runtime_CompilerServices_Unsafe_Add_T, elementOffset: int) -> typing.Any:
        """Adds an element offset to the given reference."""
        ...

    @staticmethod
    @typing.overload
    def Add(source: Internal_Runtime_CompilerServices_Unsafe_Add_T, elementOffset: System.IntPtr) -> typing.Any:
        """Adds an element offset to the given reference."""
        ...

    @staticmethod
    @typing.overload
    def Add(source: typing.Any, elementOffset: int) -> typing.Any:
        """Adds an element offset to the given pointer."""
        ...

    @staticmethod
    def AreSame(left: Internal_Runtime_CompilerServices_Unsafe_AreSame_T, right: Internal_Runtime_CompilerServices_Unsafe_AreSame_T) -> bool:
        """Determines whether the specified references point to the same location."""
        ...

    @staticmethod
    def IsAddressGreaterThan(left: Internal_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T, right: Internal_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T) -> bool:
        """
        Determines whether the memory address referenced by  is greater than
        the memory address referenced by .
        """
        ...

    @staticmethod
    def IsAddressLessThan(left: Internal_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T, right: Internal_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T) -> bool:
        """
        Determines whether the memory address referenced by  is less than
        the memory address referenced by .
        """
        ...

    @staticmethod
    def InitBlockUnaligned(startAddress: int, value: int, byteCount: int) -> None:
        """
        Initializes a block of memory at the given location with a given initial value
        without assuming architecture dependent alignment of the address.
        """
        ...

    @staticmethod
    @typing.overload
    def ReadUnaligned(source: typing.Any) -> Internal_Runtime_CompilerServices_Unsafe_ReadUnaligned_T:
        """Reads a value of type T from the given location."""
        ...

    @staticmethod
    @typing.overload
    def ReadUnaligned(source: int) -> Internal_Runtime_CompilerServices_Unsafe_ReadUnaligned_T:
        """Reads a value of type T from the given location."""
        ...

    @staticmethod
    @typing.overload
    def WriteUnaligned(destination: typing.Any, value: Internal_Runtime_CompilerServices_Unsafe_WriteUnaligned_T) -> None:
        """Writes a value of type T to the given location."""
        ...

    @staticmethod
    @typing.overload
    def WriteUnaligned(destination: int, value: Internal_Runtime_CompilerServices_Unsafe_WriteUnaligned_T) -> None:
        """Writes a value of type T to the given location."""
        ...

    @staticmethod
    def AddByteOffset(source: Internal_Runtime_CompilerServices_Unsafe_AddByteOffset_T, byteOffset: System.IntPtr) -> typing.Any:
        """Adds an byte offset to the given reference."""
        ...

    @staticmethod
    @typing.overload
    def Read(source: typing.Any) -> Internal_Runtime_CompilerServices_Unsafe_Read_T:
        """Reads a value of type T from the given location."""
        ...

    @staticmethod
    @typing.overload
    def Read(source: int) -> Internal_Runtime_CompilerServices_Unsafe_Read_T:
        """Reads a value of type T from the given location."""
        ...

    @staticmethod
    @typing.overload
    def Write(destination: typing.Any, value: Internal_Runtime_CompilerServices_Unsafe_Write_T) -> None:
        """Writes a value of type T to the given location."""
        ...

    @staticmethod
    @typing.overload
    def Write(destination: int, value: Internal_Runtime_CompilerServices_Unsafe_Write_T) -> None:
        """Writes a value of type T to the given location."""
        ...

    @staticmethod
    @typing.overload
    def AsRef(source: typing.Any) -> typing.Any:
        """Reinterprets the given location as a reference to a value of type T."""
        ...

    @staticmethod
    @typing.overload
    def AsRef(source: Internal_Runtime_CompilerServices_Unsafe_AsRef_T) -> typing.Any:
        """Reinterprets the given location as a reference to a value of type T."""
        ...

    @staticmethod
    def ByteOffset(origin: Internal_Runtime_CompilerServices_Unsafe_ByteOffset_T, target: Internal_Runtime_CompilerServices_Unsafe_ByteOffset_T) -> System.IntPtr:
        """Determines the byte offset from origin to target from the given references."""
        ...

    @staticmethod
    def NullRef() -> typing.Any:
        """Returns a by-ref to type T that is a null reference."""
        ...

    @staticmethod
    def IsNullRef(source: Internal_Runtime_CompilerServices_Unsafe_IsNullRef_T) -> bool:
        """Returns if a given by-ref to type T is a null reference."""
        ...

    @staticmethod
    def SkipInit(value: Internal_Runtime_CompilerServices_Unsafe_SkipInit_T) -> None:
        """Bypasses definite assignment rules by taking advantage of out semantics."""
        ...


