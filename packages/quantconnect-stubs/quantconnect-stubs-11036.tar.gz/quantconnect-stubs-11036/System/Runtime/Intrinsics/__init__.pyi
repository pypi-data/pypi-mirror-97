import typing

import System
import System.Numerics
import System.Runtime.Intrinsics

System_Runtime_Intrinsics_Vector128 = typing.Any
System_Runtime_Intrinsics_Vector256 = typing.Any
System_Runtime_Intrinsics_Vector64 = typing.Any

System_Runtime_Intrinsics_Vector128_GetElement_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_GetElement_T")
System_Runtime_Intrinsics_Vector128_WithElement_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_WithElement_T")
System_Runtime_Intrinsics_Vector128_ToScalar_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_ToScalar_T")
System_Runtime_Intrinsics_Vector128_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_T")
System_Runtime_Intrinsics_Vector128_As_U = typing.TypeVar("System_Runtime_Intrinsics_Vector128_As_U")
System_Runtime_Intrinsics_Vector128_As_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_As_T")
System_Runtime_Intrinsics_Vector128_AsByte_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsByte_T")
System_Runtime_Intrinsics_Vector128_AsDouble_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsDouble_T")
System_Runtime_Intrinsics_Vector128_AsInt16_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsInt16_T")
System_Runtime_Intrinsics_Vector128_AsInt32_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsInt32_T")
System_Runtime_Intrinsics_Vector128_AsInt64_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsInt64_T")
System_Runtime_Intrinsics_Vector128_AsSByte_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsSByte_T")
System_Runtime_Intrinsics_Vector128_AsSingle_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsSingle_T")
System_Runtime_Intrinsics_Vector128_AsUInt16_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsUInt16_T")
System_Runtime_Intrinsics_Vector128_AsUInt32_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsUInt32_T")
System_Runtime_Intrinsics_Vector128_AsUInt64_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsUInt64_T")
System_Runtime_Intrinsics_Vector128_AsVector128_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsVector128_T")
System_Runtime_Intrinsics_Vector128_AsVector_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_AsVector_T")
System_Runtime_Intrinsics_Vector128_GetLower_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_GetLower_T")
System_Runtime_Intrinsics_Vector128_WithLower_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_WithLower_T")
System_Runtime_Intrinsics_Vector128_GetUpper_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_GetUpper_T")
System_Runtime_Intrinsics_Vector128_WithUpper_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_WithUpper_T")
System_Runtime_Intrinsics_Vector128_ToVector256_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_ToVector256_T")
System_Runtime_Intrinsics_Vector128_ToVector256Unsafe_T = typing.TypeVar("System_Runtime_Intrinsics_Vector128_ToVector256Unsafe_T")
System_Runtime_Intrinsics_Vector256_GetElement_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_GetElement_T")
System_Runtime_Intrinsics_Vector256_WithElement_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_WithElement_T")
System_Runtime_Intrinsics_Vector256_ToScalar_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_ToScalar_T")
System_Runtime_Intrinsics_Vector256_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_T")
System_Runtime_Intrinsics_Vector256_As_U = typing.TypeVar("System_Runtime_Intrinsics_Vector256_As_U")
System_Runtime_Intrinsics_Vector256_As_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_As_T")
System_Runtime_Intrinsics_Vector256_AsByte_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsByte_T")
System_Runtime_Intrinsics_Vector256_AsDouble_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsDouble_T")
System_Runtime_Intrinsics_Vector256_AsInt16_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsInt16_T")
System_Runtime_Intrinsics_Vector256_AsInt32_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsInt32_T")
System_Runtime_Intrinsics_Vector256_AsInt64_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsInt64_T")
System_Runtime_Intrinsics_Vector256_AsSByte_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsSByte_T")
System_Runtime_Intrinsics_Vector256_AsSingle_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsSingle_T")
System_Runtime_Intrinsics_Vector256_AsUInt16_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsUInt16_T")
System_Runtime_Intrinsics_Vector256_AsUInt32_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsUInt32_T")
System_Runtime_Intrinsics_Vector256_AsUInt64_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsUInt64_T")
System_Runtime_Intrinsics_Vector256_AsVector256_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsVector256_T")
System_Runtime_Intrinsics_Vector256_AsVector_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_AsVector_T")
System_Runtime_Intrinsics_Vector256_GetLower_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_GetLower_T")
System_Runtime_Intrinsics_Vector256_WithLower_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_WithLower_T")
System_Runtime_Intrinsics_Vector256_GetUpper_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_GetUpper_T")
System_Runtime_Intrinsics_Vector256_WithUpper_T = typing.TypeVar("System_Runtime_Intrinsics_Vector256_WithUpper_T")
System_Runtime_Intrinsics_Vector64_GetElement_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_GetElement_T")
System_Runtime_Intrinsics_Vector64_WithElement_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_WithElement_T")
System_Runtime_Intrinsics_Vector64_ToScalar_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_ToScalar_T")
System_Runtime_Intrinsics_Vector64_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_T")
System_Runtime_Intrinsics_Vector64_As_U = typing.TypeVar("System_Runtime_Intrinsics_Vector64_As_U")
System_Runtime_Intrinsics_Vector64_As_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_As_T")
System_Runtime_Intrinsics_Vector64_AsByte_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_AsByte_T")
System_Runtime_Intrinsics_Vector64_AsDouble_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_AsDouble_T")
System_Runtime_Intrinsics_Vector64_AsInt16_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_AsInt16_T")
System_Runtime_Intrinsics_Vector64_AsInt32_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_AsInt32_T")
System_Runtime_Intrinsics_Vector64_AsInt64_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_AsInt64_T")
System_Runtime_Intrinsics_Vector64_AsSByte_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_AsSByte_T")
System_Runtime_Intrinsics_Vector64_AsSingle_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_AsSingle_T")
System_Runtime_Intrinsics_Vector64_AsUInt16_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_AsUInt16_T")
System_Runtime_Intrinsics_Vector64_AsUInt32_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_AsUInt32_T")
System_Runtime_Intrinsics_Vector64_AsUInt64_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_AsUInt64_T")
System_Runtime_Intrinsics_Vector64_ToVector128_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_ToVector128_T")
System_Runtime_Intrinsics_Vector64_ToVector128Unsafe_T = typing.TypeVar("System_Runtime_Intrinsics_Vector64_ToVector128Unsafe_T")


class Vector64(typing.Generic[System_Runtime_Intrinsics_Vector64_T], System.IEquatable[System_Runtime_Intrinsics_Vector64]):
    """This class has no documentation."""

    Count: int
    """Gets the number of T that are in a Vector64{T}."""

    Zero: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_T]
    """Gets a new Vector64{T} with all elements initialized to zero."""

    AllBitsSet: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_T]
    """Gets a new Vector64{T} with all bits set to 1."""

    @property
    def DisplayString(self) -> str:
        ...

    IsSupported: bool

    Size: int = 8

    @typing.overload
    def Equals(self, other: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_T]) -> bool:
        """
        Determines whether the specified Vector64{T} is equal to the current instance.
        
        :param other: The Vector64{T} to compare with the current instance.
        :returns: true if  is equal to the current instance; otherwise, false.
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Determines whether the specified object is equal to the current instance.
        
        :param obj: The object to compare with the current instance.
        :returns: true if  is a Vector64{T} and is equal to the current instance; otherwise, false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Gets the hash code for the instance.
        
        :returns: The hash code for the instance.
        """
        ...

    def ToString(self) -> str:
        """
        Converts the current instance to an equivalent string representation.
        
        :returns: An equivalent string representation of the current instance.
        """
        ...

    @staticmethod
    def As(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_As_T]) -> System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_As_U]:
        """
        Reinterprets a Vector64{T} as a new Vector64{U}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{U}.
        """
        ...

    @staticmethod
    def AsByte(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_AsByte_T]) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Reinterprets a Vector64{T} as a new Vector64{Byte}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{Byte}.
        """
        ...

    @staticmethod
    def AsDouble(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_AsDouble_T]) -> System.Runtime.Intrinsics.Vector64[float]:
        """
        Reinterprets a Vector64{T} as a new Vector64{Double}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{Double}.
        """
        ...

    @staticmethod
    def AsInt16(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_AsInt16_T]) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Reinterprets a Vector64{T} as a new Vector64{Int16}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{Int16}.
        """
        ...

    @staticmethod
    def AsInt32(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_AsInt32_T]) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Reinterprets a Vector64{T} as a new Vector64{Int32}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{Int32}.
        """
        ...

    @staticmethod
    def AsInt64(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_AsInt64_T]) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Reinterprets a Vector64{T} as a new Vector64{Int64}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{Int64}.
        """
        ...

    @staticmethod
    def AsSByte(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_AsSByte_T]) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Reinterprets a Vector64{T} as a new Vector64{SByte}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{SByte}.
        """
        ...

    @staticmethod
    def AsSingle(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_AsSingle_T]) -> System.Runtime.Intrinsics.Vector64[float]:
        """
        Reinterprets a Vector64{T} as a new Vector64{Single}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{Single}.
        """
        ...

    @staticmethod
    def AsUInt16(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_AsUInt16_T]) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Reinterprets a Vector64{T} as a new Vector64{UInt16}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{UInt16}.
        """
        ...

    @staticmethod
    def AsUInt32(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_AsUInt32_T]) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Reinterprets a Vector64{T} as a new Vector64{UInt32}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{UInt32}.
        """
        ...

    @staticmethod
    def AsUInt64(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_AsUInt64_T]) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Reinterprets a Vector64{T} as a new Vector64{UInt64}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector64{UInt64}.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Byte} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector64{Byte} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: float) -> System.Runtime.Intrinsics.Vector64[float]:
        """
        Creates a new Vector64{Double} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector64{Double} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Int16} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector64{Int16} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Int32} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector64{Int32} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Int64} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector64{Int64} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{SByte} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector64{SByte} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: float) -> System.Runtime.Intrinsics.Vector64[float]:
        """
        Creates a new Vector64{Single} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector64{Single} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{UInt16} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector64{UInt16} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{UInt32} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector64{UInt32} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{UInt64} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector64{UInt64} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Byte} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :returns: A new Vector64{Byte} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Int16} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :returns: A new Vector64{Int16} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Int32} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :returns: A new Vector64{Int32} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{SByte} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :returns: A new Vector64{SByte} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: float, e1: float) -> System.Runtime.Intrinsics.Vector64[float]:
        """
        Creates a new Vector64{Single} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :returns: A new Vector64{Single} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{UInt16} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :returns: A new Vector64{UInt16} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{UInt32} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :returns: A new Vector64{UInt32} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Byte} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{Byte} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: float) -> System.Runtime.Intrinsics.Vector64[float]:
        """
        Creates a new Vector64{Double} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{Double} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Int16} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{Int16} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Int32} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{Int32} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Int64} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{Int64} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{SByte} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{SByte} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: float) -> System.Runtime.Intrinsics.Vector64[float]:
        """
        Creates a new Vector64{Single} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{Single} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{UInt16} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{UInt16} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{UInt32} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{UInt32} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{UInt64} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{UInt64} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Byte} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{Byte} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Int16} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{Int16} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{Int32} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{Int32} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{SByte} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{SByte} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: float) -> System.Runtime.Intrinsics.Vector64[float]:
        """
        Creates a new Vector64{Single} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{Single} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{UInt16} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{UInt16} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector64[int]:
        """
        Creates a new Vector64{UInt32} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector64{UInt32} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    def GetElement(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_GetElement_T], index: int) -> System_Runtime_Intrinsics_Vector64_GetElement_T:
        """
        Gets the element at the specified index.
        
        :param vector: The vector to get the element from.
        :param index: The index of the element to get.
        :returns: The value of the element at .
        """
        ...

    @staticmethod
    def WithElement(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_WithElement_T], index: int, value: System_Runtime_Intrinsics_Vector64_WithElement_T) -> System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_WithElement_T]:
        """
        Creates a new Vector64{T} with the element at the specified index set to the specified value and the remaining elements set to the same value as that in the given vector.
        
        :param vector: The vector to get the remaining elements from.
        :param index: The index of the element to set.
        :param value: The value to set the element to.
        :returns: A Vector64{T} with the value of the element at  set to  and the remaining elements set to the same value as that in .
        """
        ...

    @staticmethod
    def ToScalar(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_ToScalar_T]) -> System_Runtime_Intrinsics_Vector64_ToScalar_T:
        """
        Converts the given vector to a scalar containing the value of the first element.
        
        :param vector: The vector to get the first element from.
        :returns: A scalar T containing the value of the first element.
        """
        ...

    @staticmethod
    def ToVector128(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_ToVector128_T]) -> System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector64_ToVector128_T]:
        """
        Converts the given vector to a new Vector128{T} with the lower 64-bits set to the value of the given vector and the upper 64-bits initialized to zero.
        
        :param vector: The vector to extend.
        :returns: A new Vector128{T} with the lower 64-bits set to the value of  and the upper 64-bits initialized to zero.
        """
        ...

    @staticmethod
    def ToVector128Unsafe(vector: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector64_ToVector128Unsafe_T]) -> System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector64_ToVector128Unsafe_T]:
        """
        Converts the given vector to a new Vector128{T} with the lower 64-bits set to the value of the given vector and the upper 64-bits left uninitialized.
        
        :param vector: The vector to extend.
        :returns: A new Vector128{T} with the lower 64-bits set to the value of  and the upper 64-bits left uninitialized.
        """
        ...


class Vector256(typing.Generic[System_Runtime_Intrinsics_Vector256_T], System.IEquatable[System_Runtime_Intrinsics_Vector256]):
    """This class has no documentation."""

    Size: int = 32

    Count: int
    """Gets the number of T that are in a Vector256{T}."""

    Zero: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_T]
    """Gets a new Vector256{T} with all elements initialized to zero."""

    AllBitsSet: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_T]
    """Gets a new Vector256{T} with all bits set to 1."""

    @property
    def DisplayString(self) -> str:
        ...

    IsSupported: bool

    @staticmethod
    def As(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_As_T]) -> System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_As_U]:
        """
        Reinterprets a Vector256{T} as a new Vector256{U}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{U}.
        """
        ...

    @staticmethod
    def AsByte(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsByte_T]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Reinterprets a Vector256{T} as a new Vector256{Byte}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{Byte}.
        """
        ...

    @staticmethod
    def AsDouble(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsDouble_T]) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Reinterprets a Vector256{T} as a new Vector256{Double}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{Double}.
        """
        ...

    @staticmethod
    def AsInt16(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsInt16_T]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Reinterprets a Vector256{T} as a new Vector256{Int16}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{Int16}.
        """
        ...

    @staticmethod
    def AsInt32(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsInt32_T]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Reinterprets a Vector256{T} as a new Vector256{Int32}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{Int32}.
        """
        ...

    @staticmethod
    def AsInt64(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsInt64_T]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Reinterprets a Vector256{T} as a new Vector256{Int64}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{Int64}.
        """
        ...

    @staticmethod
    def AsSByte(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsSByte_T]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Reinterprets a Vector256{T} as a new Vector256{SByte}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{SByte}.
        """
        ...

    @staticmethod
    def AsSingle(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsSingle_T]) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Reinterprets a Vector256{T} as a new Vector256{Single}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{Single}.
        """
        ...

    @staticmethod
    def AsUInt16(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsUInt16_T]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Reinterprets a Vector256{T} as a new Vector256{UInt16}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{UInt16}.
        """
        ...

    @staticmethod
    def AsUInt32(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsUInt32_T]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Reinterprets a Vector256{T} as a new Vector256{UInt32}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{UInt32}.
        """
        ...

    @staticmethod
    def AsUInt64(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsUInt64_T]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Reinterprets a Vector256{T} as a new Vector256{UInt64}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{UInt64}.
        """
        ...

    @staticmethod
    def AsVector256(value: System.Numerics.Vector[System_Runtime_Intrinsics_Vector256_AsVector256_T]) -> System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsVector256_T]:
        """
        Reinterprets a Vector{T} as a new Vector256{T}.
        
        :param value: The vector to reinterpret.
        :returns: reinterpreted as a new Vector256{T}.
        """
        ...

    @staticmethod
    def AsVector(value: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_AsVector_T]) -> System.Numerics.Vector[System_Runtime_Intrinsics_Vector256_AsVector_T]:
        """
        Reinterprets a Vector256{T} as a new Vector{T}.
        
        :param value: The vector to reinterpret.
        :returns: reinterpreted as a new Vector{T}.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Byte} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector256{Byte} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: float) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Creates a new Vector256{Double} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector256{Double} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int16} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector256{Int16} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int32} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector256{Int32} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int64} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector256{Int64} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{SByte} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector256{SByte} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: float) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Creates a new Vector256{Single} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector256{Single} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt16} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector256{UInt16} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt32} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector256{UInt32} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt64} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector256{UInt64} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int, e16: int, e17: int, e18: int, e19: int, e20: int, e21: int, e22: int, e23: int, e24: int, e25: int, e26: int, e27: int, e28: int, e29: int, e30: int, e31: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Byte} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :param e8: The value that element 8 will be initialized to.
        :param e9: The value that element 9 will be initialized to.
        :param e10: The value that element 10 will be initialized to.
        :param e11: The value that element 11 will be initialized to.
        :param e12: The value that element 12 will be initialized to.
        :param e13: The value that element 13 will be initialized to.
        :param e14: The value that element 14 will be initialized to.
        :param e15: The value that element 15 will be initialized to.
        :param e16: The value that element 16 will be initialized to.
        :param e17: The value that element 17 will be initialized to.
        :param e18: The value that element 18 will be initialized to.
        :param e19: The value that element 19 will be initialized to.
        :param e20: The value that element 20 will be initialized to.
        :param e21: The value that element 21 will be initialized to.
        :param e22: The value that element 22 will be initialized to.
        :param e23: The value that element 23 will be initialized to.
        :param e24: The value that element 24 will be initialized to.
        :param e25: The value that element 25 will be initialized to.
        :param e26: The value that element 26 will be initialized to.
        :param e27: The value that element 27 will be initialized to.
        :param e28: The value that element 28 will be initialized to.
        :param e29: The value that element 29 will be initialized to.
        :param e30: The value that element 30 will be initialized to.
        :param e31: The value that element 31 will be initialized to.
        :returns: A new Vector256{Byte} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: float, e1: float, e2: float, e3: float) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Creates a new Vector256{Double} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :returns: A new Vector256{Double} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int16} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :param e8: The value that element 8 will be initialized to.
        :param e9: The value that element 9 will be initialized to.
        :param e10: The value that element 10 will be initialized to.
        :param e11: The value that element 11 will be initialized to.
        :param e12: The value that element 12 will be initialized to.
        :param e13: The value that element 13 will be initialized to.
        :param e14: The value that element 14 will be initialized to.
        :param e15: The value that element 15 will be initialized to.
        :returns: A new Vector256{Int16} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int32} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :returns: A new Vector256{Int32} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int64} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :returns: A new Vector256{Int64} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int, e16: int, e17: int, e18: int, e19: int, e20: int, e21: int, e22: int, e23: int, e24: int, e25: int, e26: int, e27: int, e28: int, e29: int, e30: int, e31: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{SByte} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :param e8: The value that element 8 will be initialized to.
        :param e9: The value that element 9 will be initialized to.
        :param e10: The value that element 10 will be initialized to.
        :param e11: The value that element 11 will be initialized to.
        :param e12: The value that element 12 will be initialized to.
        :param e13: The value that element 13 will be initialized to.
        :param e14: The value that element 14 will be initialized to.
        :param e15: The value that element 15 will be initialized to.
        :param e16: The value that element 16 will be initialized to.
        :param e17: The value that element 17 will be initialized to.
        :param e18: The value that element 18 will be initialized to.
        :param e19: The value that element 19 will be initialized to.
        :param e20: The value that element 20 will be initialized to.
        :param e21: The value that element 21 will be initialized to.
        :param e22: The value that element 22 will be initialized to.
        :param e23: The value that element 23 will be initialized to.
        :param e24: The value that element 24 will be initialized to.
        :param e25: The value that element 25 will be initialized to.
        :param e26: The value that element 26 will be initialized to.
        :param e27: The value that element 27 will be initialized to.
        :param e28: The value that element 28 will be initialized to.
        :param e29: The value that element 29 will be initialized to.
        :param e30: The value that element 30 will be initialized to.
        :param e31: The value that element 31 will be initialized to.
        :returns: A new Vector256{SByte} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: float, e1: float, e2: float, e3: float, e4: float, e5: float, e6: float, e7: float) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Creates a new Vector256{Single} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :returns: A new Vector256{Single} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt16} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :param e8: The value that element 8 will be initialized to.
        :param e9: The value that element 9 will be initialized to.
        :param e10: The value that element 10 will be initialized to.
        :param e11: The value that element 11 will be initialized to.
        :param e12: The value that element 12 will be initialized to.
        :param e13: The value that element 13 will be initialized to.
        :param e14: The value that element 14 will be initialized to.
        :param e15: The value that element 15 will be initialized to.
        :returns: A new Vector256{UInt16} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt32} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :returns: A new Vector256{UInt32} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt64} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :returns: A new Vector256{UInt64} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Byte} instance from two Vector128{Byte} instances.
        
        :param lower: The value that the lower 128-bits will be initialized to.
        :param upper: The value that the upper 128-bits will be initialized to.
        :returns: A new Vector256{Byte} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector128[float], upper: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Creates a new Vector256{Double} instance from two Vector128{Double} instances.
        
        :param lower: The value that the lower 128-bits will be initialized to.
        :param upper: The value that the upper 128-bits will be initialized to.
        :returns: A new Vector256{Double} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int16} instance from two Vector128{Int16} instances.
        
        :param lower: The value that the lower 128-bits will be initialized to.
        :param upper: The value that the upper 128-bits will be initialized to.
        :returns: A new Vector256{Int16} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int32} instance from two Vector128{Int32} instances.
        
        :param lower: The value that the lower 128-bits will be initialized to.
        :param upper: The value that the upper 128-bits will be initialized to.
        :returns: A new Vector256{Int32} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int64} instance from two Vector128{Int64} instances.
        
        :param lower: The value that the lower 128-bits will be initialized to.
        :param upper: The value that the upper 128-bits will be initialized to.
        :returns: A new Vector256{Int64} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{SByte} instance from two Vector128{SByte} instances.
        
        :param lower: The value that the lower 128-bits will be initialized to.
        :param upper: The value that the upper 128-bits will be initialized to.
        :returns: A new Vector256{SByte} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector128[float], upper: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Creates a new Vector256{Single} instance from two Vector128{Single} instances.
        
        :param lower: The value that the lower 128-bits will be initialized to.
        :param upper: The value that the upper 128-bits will be initialized to.
        :returns: A new Vector256{Single} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt16} instance from two Vector128{UInt16} instances.
        
        :param lower: The value that the lower 128-bits will be initialized to.
        :param upper: The value that the upper 128-bits will be initialized to.
        :returns: A new Vector256{UInt16} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt32} instance from two Vector128{UInt32} instances.
        
        :param lower: The value that the lower 128-bits will be initialized to.
        :param upper: The value that the upper 128-bits will be initialized to.
        :returns: A new Vector256{UInt32} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt64} instance from two Vector128{UInt64} instances.
        
        :param lower: The value that the lower 128-bits will be initialized to.
        :param upper: The value that the upper 128-bits will be initialized to.
        :returns: A new Vector256{UInt64} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Byte} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Byte} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: float) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Creates a new Vector256{Double} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Double} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int16} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Int16} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int32} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Int32} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int64} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Int64} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{SByte} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{SByte} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: float) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Creates a new Vector256{Single} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Single} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt16} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{UInt16} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt32} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{UInt32} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt64} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{UInt64} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Byte} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Byte} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: float) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Creates a new Vector256{Double} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Double} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int16} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Int16} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int32} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Int32} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{Int64} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Int64} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{SByte} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{SByte} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: float) -> System.Runtime.Intrinsics.Vector256[float]:
        """
        Creates a new Vector256{Single} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{Single} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt16} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{UInt16} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt32} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{UInt32} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector256[int]:
        """
        Creates a new Vector256{UInt64} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector256{UInt64} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    def GetElement(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_GetElement_T], index: int) -> System_Runtime_Intrinsics_Vector256_GetElement_T:
        """
        Gets the element at the specified index.
        
        :param vector: The vector to get the element from.
        :param index: The index of the element to get.
        :returns: The value of the element at .
        """
        ...

    @staticmethod
    def WithElement(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_WithElement_T], index: int, value: System_Runtime_Intrinsics_Vector256_WithElement_T) -> System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_WithElement_T]:
        """
        Creates a new Vector256{T} with the element at the specified index set to the specified value and the remaining elements set to the same value as that in the given vector.
        
        :param vector: The vector to get the remaining elements from.
        :param index: The index of the element to set.
        :param value: The value to set the element to.
        :returns: A Vector256{T} with the value of the element at  set to  and the remaining elements set to the same value as that in .
        """
        ...

    @staticmethod
    def GetLower(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_GetLower_T]) -> System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector256_GetLower_T]:
        """
        Gets the value of the lower 128-bits as a new Vector128{T}.
        
        :param vector: The vector to get the lower 128-bits from.
        :returns: The value of the lower 128-bits as a new Vector128{T}.
        """
        ...

    @staticmethod
    def WithLower(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_WithLower_T], value: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector256_WithLower_T]) -> System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_WithLower_T]:
        """
        Creates a new Vector256{T} with the lower 128-bits set to the specified value and the upper 128-bits set to the same value as that in the given vector.
        
        :param vector: The vector to get the upper 128-bits from.
        :param value: The value of the lower 128-bits as a Vector128{T}.
        :returns: A new Vector256{T} with the lower 128-bits set to  and the upper 128-bits set to the same value as that in .
        """
        ...

    @staticmethod
    def GetUpper(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_GetUpper_T]) -> System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector256_GetUpper_T]:
        """
        Gets the value of the upper 128-bits as a new Vector128{T}.
        
        :param vector: The vector to get the upper 128-bits from.
        :returns: The value of the upper 128-bits as a new Vector128{T}.
        """
        ...

    @staticmethod
    def WithUpper(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_WithUpper_T], value: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector256_WithUpper_T]) -> System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_WithUpper_T]:
        """
        Creates a new Vector256{T} with the upper 128-bits set to the specified value and the upper 128-bits set to the same value as that in the given vector.
        
        :param vector: The vector to get the lower 128-bits from.
        :param value: The value of the upper 128-bits as a Vector128{T}.
        :returns: A new Vector256{T} with the upper 128-bits set to  and the lower 128-bits set to the same value as that in .
        """
        ...

    @staticmethod
    def ToScalar(vector: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_ToScalar_T]) -> System_Runtime_Intrinsics_Vector256_ToScalar_T:
        """
        Converts the given vector to a scalar containing the value of the first element.
        
        :param vector: The vector to get the first element from.
        :returns: A scalar T containing the value of the first element.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector256_T]) -> bool:
        """
        Determines whether the specified Vector256{T} is equal to the current instance.
        
        :param other: The Vector256{T} to compare with the current instance.
        :returns: true if  is equal to the current instance; otherwise, false.
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Determines whether the specified object is equal to the current instance.
        
        :param obj: The object to compare with the current instance.
        :returns: true if  is a Vector256{T} and is equal to the current instance; otherwise, false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Gets the hash code for the instance.
        
        :returns: The hash code for the instance.
        """
        ...

    def ToString(self) -> str:
        """
        Converts the current instance to an equivalent string representation.
        
        :returns: An equivalent string representation of the current instance.
        """
        ...


class Vector128(typing.Generic[System_Runtime_Intrinsics_Vector128_T], System.IEquatable[System_Runtime_Intrinsics_Vector128]):
    """This class has no documentation."""

    Count: int
    """Gets the number of T that are in a Vector128{T}."""

    Zero: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_T]
    """Gets a new Vector128{T} with all elements initialized to zero."""

    AllBitsSet: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_T]
    """Gets a new Vector128{T} with all bits set to 1."""

    @property
    def DisplayString(self) -> str:
        ...

    IsSupported: bool

    Size: int = 16

    @typing.overload
    def Equals(self, other: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_T]) -> bool:
        """
        Determines whether the specified Vector128{T} is equal to the current instance.
        
        :param other: The Vector128{T} to compare with the current instance.
        :returns: true if  is equal to the current instance; otherwise, false.
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Determines whether the specified object is equal to the current instance.
        
        :param obj: The object to compare with the current instance.
        :returns: true if  is a Vector128{T} and is equal to the current instance; otherwise, false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Gets the hash code for the instance.
        
        :returns: The hash code for the instance.
        """
        ...

    def ToString(self) -> str:
        """
        Converts the current instance to an equivalent string representation.
        
        :returns: An equivalent string representation of the current instance.
        """
        ...

    @staticmethod
    def As(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_As_T]) -> System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_As_U]:
        """
        Reinterprets a Vector128{T} as a new Vector128{U}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{U}.
        """
        ...

    @staticmethod
    def AsByte(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsByte_T]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Reinterprets a Vector128{T} as a new Vector128{Byte}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{Byte}.
        """
        ...

    @staticmethod
    def AsDouble(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsDouble_T]) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Reinterprets a Vector128{T} as a new Vector128{Double}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{Double}.
        """
        ...

    @staticmethod
    def AsInt16(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsInt16_T]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Reinterprets a Vector128{T} as a new Vector128{Int16}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{Int16}.
        """
        ...

    @staticmethod
    def AsInt32(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsInt32_T]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Reinterprets a Vector128{T} as a new Vector128{Int32}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{Int32}.
        """
        ...

    @staticmethod
    def AsInt64(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsInt64_T]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Reinterprets a Vector128{T} as a new Vector128{Int64}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{Int64}.
        """
        ...

    @staticmethod
    def AsSByte(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsSByte_T]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Reinterprets a Vector128{T} as a new Vector128{SByte}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{SByte}.
        """
        ...

    @staticmethod
    def AsSingle(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsSingle_T]) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Reinterprets a Vector128{T} as a new Vector128{Single}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{Single}.
        """
        ...

    @staticmethod
    def AsUInt16(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsUInt16_T]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Reinterprets a Vector128{T} as a new Vector128{UInt16}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{UInt16}.
        """
        ...

    @staticmethod
    def AsUInt32(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsUInt32_T]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Reinterprets a Vector128{T} as a new Vector128{UInt32}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{UInt32}.
        """
        ...

    @staticmethod
    def AsUInt64(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsUInt64_T]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Reinterprets a Vector128{T} as a new Vector128{UInt64}.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{UInt64}.
        """
        ...

    @staticmethod
    @typing.overload
    def AsVector128(value: System.Numerics.Vector2) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Reinterprets a Vector2 as a new Vector128{Single}.
        
        :param value: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{Single}.
        """
        ...

    @staticmethod
    @typing.overload
    def AsVector128(value: System.Numerics.Vector3) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Reinterprets a Vector3 as a new Vector128{Single}.
        
        :param value: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{Single}.
        """
        ...

    @staticmethod
    @typing.overload
    def AsVector128(value: System.Numerics.Vector4) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Reinterprets a Vector4 as a new Vector128{Single}.
        
        :param value: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{Single}.
        """
        ...

    @staticmethod
    @typing.overload
    def AsVector128(value: System.Numerics.Vector[System_Runtime_Intrinsics_Vector128_AsVector128_T]) -> System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsVector128_T]:
        """
        Reinterprets a Vector{T} as a new Vector128{T}.
        
        :param value: The vector to reinterpret.
        :returns: reinterpreted as a new Vector128{T}.
        """
        ...

    @staticmethod
    def AsVector2(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Numerics.Vector2:
        """
        Reinterprets a Vector128{Single} as a new Vector2.
        
        :param value: The vector to reinterpret.
        :returns: reinterpreted as a new Vector2.
        """
        ...

    @staticmethod
    def AsVector3(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Numerics.Vector3:
        """
        Reinterprets a Vector128{Single} as a new Vector3.
        
        :param value: The vector to reinterpret.
        :returns: reinterpreted as a new Vector3.
        """
        ...

    @staticmethod
    def AsVector4(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Numerics.Vector4:
        """
        Reinterprets a Vector128{Single} as a new Vector4.
        
        :param value: The vector to reinterpret.
        :returns: reinterpreted as a new Vector4.
        """
        ...

    @staticmethod
    def AsVector(value: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_AsVector_T]) -> System.Numerics.Vector[System_Runtime_Intrinsics_Vector128_AsVector_T]:
        """
        Reinterprets a Vector128{T} as a new Vector{T}.
        
        :param value: The vector to reinterpret.
        :returns: reinterpreted as a new Vector{T}.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Byte} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector128{Byte} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Creates a new Vector128{Double} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector128{Double} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int16} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector128{Int16} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int32} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector128{Int32} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int64} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector128{Int64} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{SByte} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector128{SByte} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Creates a new Vector128{Single} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector128{Single} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt16} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector128{UInt16} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt32} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector128{UInt32} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt64} instance with all elements initialized to the specified value.
        
        :param value: The value that all elements will be initialized to.
        :returns: A new Vector128{UInt64} with all elements initialized to .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Byte} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :param e8: The value that element 8 will be initialized to.
        :param e9: The value that element 9 will be initialized to.
        :param e10: The value that element 10 will be initialized to.
        :param e11: The value that element 11 will be initialized to.
        :param e12: The value that element 12 will be initialized to.
        :param e13: The value that element 13 will be initialized to.
        :param e14: The value that element 14 will be initialized to.
        :param e15: The value that element 15 will be initialized to.
        :returns: A new Vector128{Byte} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: float, e1: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Creates a new Vector128{Double} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :returns: A new Vector128{Double} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int16} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :returns: A new Vector128{Int16} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int32} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :returns: A new Vector128{Int32} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int64} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :returns: A new Vector128{Int64} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{SByte} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :param e8: The value that element 8 will be initialized to.
        :param e9: The value that element 9 will be initialized to.
        :param e10: The value that element 10 will be initialized to.
        :param e11: The value that element 11 will be initialized to.
        :param e12: The value that element 12 will be initialized to.
        :param e13: The value that element 13 will be initialized to.
        :param e14: The value that element 14 will be initialized to.
        :param e15: The value that element 15 will be initialized to.
        :returns: A new Vector128{SByte} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: float, e1: float, e2: float, e3: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Creates a new Vector128{Single} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :returns: A new Vector128{Single} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt16} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :param e4: The value that element 4 will be initialized to.
        :param e5: The value that element 5 will be initialized to.
        :param e6: The value that element 6 will be initialized to.
        :param e7: The value that element 7 will be initialized to.
        :returns: A new Vector128{UInt16} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int, e2: int, e3: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt32} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :param e2: The value that element 2 will be initialized to.
        :param e3: The value that element 3 will be initialized to.
        :returns: A new Vector128{UInt32} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(e0: int, e1: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt64} instance with each element initialized to the corresponding specified value.
        
        :param e0: The value that element 0 will be initialized to.
        :param e1: The value that element 1 will be initialized to.
        :returns: A new Vector128{UInt64} with each element initialized to corresponding specified value.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector64[int], upper: System.Runtime.Intrinsics.Vector64[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Byte} instance from two Vector64{Byte} instances.
        
        :param lower: The value that the lower 64-bits will be initialized to.
        :param upper: The value that the upper 64-bits will be initialized to.
        :returns: A new Vector128{Byte} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector64[float], upper: System.Runtime.Intrinsics.Vector64[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Creates a new Vector128{Double} instance from two Vector64{Double} instances.
        
        :param lower: The value that the lower 64-bits will be initialized to.
        :param upper: The value that the upper 64-bits will be initialized to.
        :returns: A new Vector128{Double} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector64[int], upper: System.Runtime.Intrinsics.Vector64[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int16} instance from two Vector64{Int16} instances.
        
        :param lower: The value that the lower 64-bits will be initialized to.
        :param upper: The value that the upper 64-bits will be initialized to.
        :returns: A new Vector128{Int16} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector64[int], upper: System.Runtime.Intrinsics.Vector64[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int32} instance from two Vector64{Int32} instances.
        
        :param lower: The value that the lower 64-bits will be initialized to.
        :param upper: The value that the upper 64-bits will be initialized to.
        :returns: A new Vector128{Int32} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector64[int], upper: System.Runtime.Intrinsics.Vector64[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int64} instance from two Vector64{Int64} instances.
        
        :param lower: The value that the lower 64-bits will be initialized to.
        :param upper: The value that the upper 64-bits will be initialized to.
        :returns: A new Vector128{Int64} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector64[int], upper: System.Runtime.Intrinsics.Vector64[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{SByte} instance from two Vector64{SByte} instances.
        
        :param lower: The value that the lower 64-bits will be initialized to.
        :param upper: The value that the upper 64-bits will be initialized to.
        :returns: A new Vector128{SByte} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector64[float], upper: System.Runtime.Intrinsics.Vector64[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Creates a new Vector128{Single} instance from two Vector64{Single} instances.
        
        :param lower: The value that the lower 64-bits will be initialized to.
        :param upper: The value that the upper 64-bits will be initialized to.
        :returns: A new Vector128{Single} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector64[int], upper: System.Runtime.Intrinsics.Vector64[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt16} instance from two Vector64{UInt16} instances.
        
        :param lower: The value that the lower 64-bits will be initialized to.
        :param upper: The value that the upper 64-bits will be initialized to.
        :returns: A new Vector128{UInt16} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector64[int], upper: System.Runtime.Intrinsics.Vector64[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt32} instance from two Vector64{UInt32} instances.
        
        :param lower: The value that the lower 64-bits will be initialized to.
        :param upper: The value that the upper 64-bits will be initialized to.
        :returns: A new Vector128{UInt32} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def Create(lower: System.Runtime.Intrinsics.Vector64[int], upper: System.Runtime.Intrinsics.Vector64[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt64} instance from two Vector64{UInt64} instances.
        
        :param lower: The value that the lower 64-bits will be initialized to.
        :param upper: The value that the upper 64-bits will be initialized to.
        :returns: A new Vector128{UInt64} initialized from  and .
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Byte} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Byte} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Creates a new Vector128{Double} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Double} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int16} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Int16} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int32} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Int32} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int64} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Int64} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{SByte} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{SByte} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Creates a new Vector128{Single} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Single} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt16} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{UInt16} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt32} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{UInt32} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalar(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt64} instance with the first element initialized to the specified value and the remaining elements initialized to zero.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{UInt64} instance with the first element initialized to  and the remaining elements initialized to zero.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Byte} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Byte} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Creates a new Vector128{Double} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Double} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int16} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Int16} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int32} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Int32} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{Int64} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Int64} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{SByte} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{SByte} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """
        Creates a new Vector128{Single} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{Single} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt16} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{UInt16} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt32} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{UInt32} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScalarUnsafe(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """
        Creates a new Vector128{UInt64} instance with the first element initialized to the specified value and the remaining elements left uninitialized.
        
        :param value: The value that element 0 will be initialized to.
        :returns: A new Vector128{UInt64} instance with the first element initialized to  and the remaining elements left uninitialized.
        """
        ...

    @staticmethod
    def GetElement(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_GetElement_T], index: int) -> System_Runtime_Intrinsics_Vector128_GetElement_T:
        """
        Gets the element at the specified index.
        
        :param vector: The vector to get the element from.
        :param index: The index of the element to get.
        :returns: The value of the element at .
        """
        ...

    @staticmethod
    def WithElement(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_WithElement_T], index: int, value: System_Runtime_Intrinsics_Vector128_WithElement_T) -> System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_WithElement_T]:
        """
        Creates a new Vector128{T} with the element at the specified index set to the specified value and the remaining elements set to the same value as that in the given vector.
        
        :param vector: The vector to get the remaining elements from.
        :param index: The index of the element to set.
        :param value: The value to set the element to.
        :returns: A Vector128{T} with the value of the element at  set to  and the remaining elements set to the same value as that in .
        """
        ...

    @staticmethod
    def GetLower(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_GetLower_T]) -> System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector128_GetLower_T]:
        """
        Gets the value of the lower 64-bits as a new Vector64{T}.
        
        :param vector: The vector to get the lower 64-bits from.
        :returns: The value of the lower 64-bits as a new Vector64{T}.
        """
        ...

    @staticmethod
    def WithLower(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_WithLower_T], value: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector128_WithLower_T]) -> System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_WithLower_T]:
        """
        Creates a new Vector128{T} with the lower 64-bits set to the specified value and the upper 64-bits set to the same value as that in the given vector.
        
        :param vector: The vector to get the upper 64-bits from.
        :param value: The value of the lower 64-bits as a Vector64{T}.
        :returns: A new Vector128{T} with the lower 64-bits set to  and the upper 64-bits set to the same value as that in .
        """
        ...

    @staticmethod
    def GetUpper(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_GetUpper_T]) -> System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector128_GetUpper_T]:
        """
        Gets the value of the upper 64-bits as a new Vector64{T}.
        
        :param vector: The vector to get the upper 64-bits from.
        :returns: The value of the upper 64-bits as a new Vector64{T}.
        """
        ...

    @staticmethod
    def WithUpper(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_WithUpper_T], value: System.Runtime.Intrinsics.Vector64[System_Runtime_Intrinsics_Vector128_WithUpper_T]) -> System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_WithUpper_T]:
        """
        Creates a new Vector128{T} with the upper 64-bits set to the specified value and the upper 64-bits set to the same value as that in the given vector.
        
        :param vector: The vector to get the lower 64-bits from.
        :param value: The value of the upper 64-bits as a Vector64{T}.
        :returns: A new Vector128{T} with the upper 64-bits set to  and the lower 64-bits set to the same value as that in .
        """
        ...

    @staticmethod
    def ToScalar(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_ToScalar_T]) -> System_Runtime_Intrinsics_Vector128_ToScalar_T:
        """
        Converts the given vector to a scalar containing the value of the first element.
        
        :param vector: The vector to get the first element from.
        :returns: A scalar T containing the value of the first element.
        """
        ...

    @staticmethod
    def ToVector256(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_ToVector256_T]) -> System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector128_ToVector256_T]:
        """
        Converts the given vector to a new Vector256{T} with the lower 128-bits set to the value of the given vector and the upper 128-bits initialized to zero.
        
        :param vector: The vector to extend.
        :returns: A new Vector256{T} with the lower 128-bits set to the value of  and the upper 128-bits initialized to zero.
        """
        ...

    @staticmethod
    def ToVector256Unsafe(vector: System.Runtime.Intrinsics.Vector128[System_Runtime_Intrinsics_Vector128_ToVector256Unsafe_T]) -> System.Runtime.Intrinsics.Vector256[System_Runtime_Intrinsics_Vector128_ToVector256Unsafe_T]:
        """
        Converts the given vector to a new Vector256{T} with the lower 128-bits set to the value of the given vector and the upper 128-bits left uninitialized.
        
        :param vector: The vector to extend.
        :returns: A new Vector256{T} with the lower 128-bits set to the value of  and the upper 128-bits left uninitialized.
        """
        ...


