import typing

import System
import System.Numerics

System_Numerics_Vector2 = typing.Any
System_Numerics_Vector4 = typing.Any
System_Numerics_Plane = typing.Any
System_Numerics_Vector = typing.Any
System_Numerics_Matrix3x2 = typing.Any
System_Numerics_Matrix4x4 = typing.Any
System_Numerics_Quaternion = typing.Any
System_Numerics_Vector3 = typing.Any

System_Numerics_Vector_Dot_T = typing.TypeVar("System_Numerics_Vector_Dot_T")
System_Numerics_Vector_Multiply_T = typing.TypeVar("System_Numerics_Vector_Multiply_T")
System_Numerics_Vector_T = typing.TypeVar("System_Numerics_Vector_T")
System_Numerics_Vector_ConditionalSelect_T = typing.TypeVar("System_Numerics_Vector_ConditionalSelect_T")
System_Numerics_Vector_Equals_T = typing.TypeVar("System_Numerics_Vector_Equals_T")
System_Numerics_Vector_EqualsAll_T = typing.TypeVar("System_Numerics_Vector_EqualsAll_T")
System_Numerics_Vector_EqualsAny_T = typing.TypeVar("System_Numerics_Vector_EqualsAny_T")
System_Numerics_Vector_LessThan_T = typing.TypeVar("System_Numerics_Vector_LessThan_T")
System_Numerics_Vector_LessThanAll_T = typing.TypeVar("System_Numerics_Vector_LessThanAll_T")
System_Numerics_Vector_LessThanAny_T = typing.TypeVar("System_Numerics_Vector_LessThanAny_T")
System_Numerics_Vector_LessThanOrEqual_T = typing.TypeVar("System_Numerics_Vector_LessThanOrEqual_T")
System_Numerics_Vector_LessThanOrEqualAll_T = typing.TypeVar("System_Numerics_Vector_LessThanOrEqualAll_T")
System_Numerics_Vector_LessThanOrEqualAny_T = typing.TypeVar("System_Numerics_Vector_LessThanOrEqualAny_T")
System_Numerics_Vector_GreaterThan_T = typing.TypeVar("System_Numerics_Vector_GreaterThan_T")
System_Numerics_Vector_GreaterThanAll_T = typing.TypeVar("System_Numerics_Vector_GreaterThanAll_T")
System_Numerics_Vector_GreaterThanAny_T = typing.TypeVar("System_Numerics_Vector_GreaterThanAny_T")
System_Numerics_Vector_GreaterThanOrEqual_T = typing.TypeVar("System_Numerics_Vector_GreaterThanOrEqual_T")
System_Numerics_Vector_GreaterThanOrEqualAll_T = typing.TypeVar("System_Numerics_Vector_GreaterThanOrEqualAll_T")
System_Numerics_Vector_GreaterThanOrEqualAny_T = typing.TypeVar("System_Numerics_Vector_GreaterThanOrEqualAny_T")
System_Numerics_Vector_Abs_T = typing.TypeVar("System_Numerics_Vector_Abs_T")
System_Numerics_Vector_Min_T = typing.TypeVar("System_Numerics_Vector_Min_T")
System_Numerics_Vector_Max_T = typing.TypeVar("System_Numerics_Vector_Max_T")
System_Numerics_Vector_SquareRoot_T = typing.TypeVar("System_Numerics_Vector_SquareRoot_T")
System_Numerics_Vector_Add_T = typing.TypeVar("System_Numerics_Vector_Add_T")
System_Numerics_Vector_Subtract_T = typing.TypeVar("System_Numerics_Vector_Subtract_T")
System_Numerics_Vector_Divide_T = typing.TypeVar("System_Numerics_Vector_Divide_T")
System_Numerics_Vector_Negate_T = typing.TypeVar("System_Numerics_Vector_Negate_T")
System_Numerics_Vector_BitwiseAnd_T = typing.TypeVar("System_Numerics_Vector_BitwiseAnd_T")
System_Numerics_Vector_BitwiseOr_T = typing.TypeVar("System_Numerics_Vector_BitwiseOr_T")
System_Numerics_Vector_OnesComplement_T = typing.TypeVar("System_Numerics_Vector_OnesComplement_T")
System_Numerics_Vector_Xor_T = typing.TypeVar("System_Numerics_Vector_Xor_T")
System_Numerics_Vector_AndNot_T = typing.TypeVar("System_Numerics_Vector_AndNot_T")
System_Numerics_Vector_AsVectorByte_T = typing.TypeVar("System_Numerics_Vector_AsVectorByte_T")
System_Numerics_Vector_AsVectorSByte_T = typing.TypeVar("System_Numerics_Vector_AsVectorSByte_T")
System_Numerics_Vector_AsVectorUInt16_T = typing.TypeVar("System_Numerics_Vector_AsVectorUInt16_T")
System_Numerics_Vector_AsVectorInt16_T = typing.TypeVar("System_Numerics_Vector_AsVectorInt16_T")
System_Numerics_Vector_AsVectorUInt32_T = typing.TypeVar("System_Numerics_Vector_AsVectorUInt32_T")
System_Numerics_Vector_AsVectorInt32_T = typing.TypeVar("System_Numerics_Vector_AsVectorInt32_T")
System_Numerics_Vector_AsVectorUInt64_T = typing.TypeVar("System_Numerics_Vector_AsVectorUInt64_T")
System_Numerics_Vector_AsVectorInt64_T = typing.TypeVar("System_Numerics_Vector_AsVectorInt64_T")
System_Numerics_Vector_AsVectorSingle_T = typing.TypeVar("System_Numerics_Vector_AsVectorSingle_T")
System_Numerics_Vector_AsVectorDouble_T = typing.TypeVar("System_Numerics_Vector_AsVectorDouble_T")
System_Numerics_Vector_As_TTo = typing.TypeVar("System_Numerics_Vector_As_TTo")
System_Numerics_Vector_As_TFrom = typing.TypeVar("System_Numerics_Vector_As_TFrom")


class Matrix3x2(System.IEquatable[System_Numerics_Matrix3x2]):
    """Represents a 3x2 matrix."""

    @property
    def M11(self) -> float:
        """The first element of the first row."""
        ...

    @M11.setter
    def M11(self, value: float):
        """The first element of the first row."""
        ...

    @property
    def M12(self) -> float:
        """The second element of the first row."""
        ...

    @M12.setter
    def M12(self, value: float):
        """The second element of the first row."""
        ...

    @property
    def M21(self) -> float:
        """The first element of the second row."""
        ...

    @M21.setter
    def M21(self, value: float):
        """The first element of the second row."""
        ...

    @property
    def M22(self) -> float:
        """The second element of the second row."""
        ...

    @M22.setter
    def M22(self, value: float):
        """The second element of the second row."""
        ...

    @property
    def M31(self) -> float:
        """The first element of the third row."""
        ...

    @M31.setter
    def M31(self, value: float):
        """The first element of the third row."""
        ...

    @property
    def M32(self) -> float:
        """The second element of the third row."""
        ...

    @M32.setter
    def M32(self, value: float):
        """The second element of the third row."""
        ...

    Identity: System.Numerics.Matrix3x2
    """Gets the multiplicative identity matrix."""

    @property
    def IsIdentity(self) -> bool:
        """Gets a value that indicates whether the current matrix is the identity matrix."""
        ...

    @property
    def Translation(self) -> System.Numerics.Vector2:
        """Gets or sets the translation component of this matrix."""
        ...

    @Translation.setter
    def Translation(self, value: System.Numerics.Vector2):
        """Gets or sets the translation component of this matrix."""
        ...

    def __init__(self, m11: float, m12: float, m21: float, m22: float, m31: float, m32: float) -> None:
        """
        Creates a 3x2 matrix from the specified components.
        
        :param m11: The value to assign to the first element in the first row.
        :param m12: The value to assign to the second element in the first row.
        :param m21: The value to assign to the first element in the second row.
        :param m22: The value to assign to the second element in the second row.
        :param m31: The value to assign to the first element in the third row.
        :param m32: The value to assign to the second element in the third row.
        """
        ...

    @staticmethod
    def Add(value1: System.Numerics.Matrix3x2, value2: System.Numerics.Matrix3x2) -> System.Numerics.Matrix3x2:
        """
        Adds each element in one matrix with its corresponding element in a second matrix.
        
        :param value1: The first matrix.
        :param value2: The second matrix.
        :returns: The matrix that contains the summed values of  and .
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotation(radians: float) -> System.Numerics.Matrix3x2:
        """
        Creates a rotation matrix using the given rotation in radians.
        
        :param radians: The amount of rotation, in radians.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotation(radians: float, centerPoint: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a rotation matrix using the specified rotation in radians and a center point.
        
        :param radians: The amount of rotation, in radians.
        :param centerPoint: The center point.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scales: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a scaling matrix from the specified vector scale.
        
        :param scales: The scale to use.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(xScale: float, yScale: float) -> System.Numerics.Matrix3x2:
        """
        Creates a scaling matrix from the specified X and Y components.
        
        :param xScale: The value to scale by on the X axis.
        :param yScale: The value to scale by on the Y axis.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(xScale: float, yScale: float, centerPoint: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a scaling matrix that is offset by a given center point.
        
        :param xScale: The value to scale by on the X axis.
        :param yScale: The value to scale by on the Y axis.
        :param centerPoint: The center point.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scales: System.Numerics.Vector2, centerPoint: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a scaling matrix from the specified vector scale with an offset from the specified center point.
        
        :param scales: The scale to use.
        :param centerPoint: The center offset.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scale: float) -> System.Numerics.Matrix3x2:
        """
        Creates a scaling matrix that scales uniformly with the given scale.
        
        :param scale: The uniform scale to use.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scale: float, centerPoint: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a scaling matrix that scales uniformly with the specified scale with an offset from the specified center.
        
        :param scale: The uniform scale to use.
        :param centerPoint: The center offset.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateSkew(radiansX: float, radiansY: float) -> System.Numerics.Matrix3x2:
        """
        Creates a skew matrix from the specified angles in radians.
        
        :param radiansX: The X angle, in radians.
        :param radiansY: The Y angle, in radians.
        :returns: The skew matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateSkew(radiansX: float, radiansY: float, centerPoint: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a skew matrix from the specified angles in radians and a center point.
        
        :param radiansX: The X angle, in radians.
        :param radiansY: The Y angle, in radians.
        :param centerPoint: The center point.
        :returns: The skew matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateTranslation(position: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a translation matrix from the specified 2-dimensional vector.
        
        :param position: The translation position.
        :returns: The translation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateTranslation(xPosition: float, yPosition: float) -> System.Numerics.Matrix3x2:
        """
        Creates a translation matrix from the specified X and Y components.
        
        :param xPosition: The X position.
        :param yPosition: The Y position.
        :returns: The translation matrix.
        """
        ...

    @staticmethod
    def Invert(matrix: System.Numerics.Matrix3x2, result: System.Numerics.Matrix3x2) -> bool:
        """
        Tries to invert the specified matrix. The return value indicates whether the operation succeeded.
        
        :param matrix: The matrix to invert.
        :param result: When this method returns, contains the inverted matrix if the operation succeeded.
        :returns: true if  was converted successfully; otherwise,  false.
        """
        ...

    @staticmethod
    def Lerp(matrix1: System.Numerics.Matrix3x2, matrix2: System.Numerics.Matrix3x2, amount: float) -> System.Numerics.Matrix3x2:
        """
        Performs a linear interpolation from one matrix to a second matrix based on a value that specifies the weighting of the second matrix.
        
        :param matrix1: The first matrix.
        :param matrix2: The second matrix.
        :param amount: The relative weighting of .
        :returns: The interpolated matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Matrix3x2, value2: System.Numerics.Matrix3x2) -> System.Numerics.Matrix3x2:
        """
        Multiplies two matrices together to compute the product.
        
        :param value1: The first matrix.
        :param value2: The second matrix.
        :returns: The product matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Matrix3x2, value2: float) -> System.Numerics.Matrix3x2:
        """
        Multiplies a matrix by a float to compute the product.
        
        :param value1: The matrix to scale.
        :param value2: The scaling value to use.
        :returns: The scaled matrix.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Matrix3x2) -> System.Numerics.Matrix3x2:
        """
        Negates the specified matrix by multiplying all its values by -1.
        
        :param value: The matrix to negate.
        :returns: The negated matrix.
        """
        ...

    @staticmethod
    def Subtract(value1: System.Numerics.Matrix3x2, value2: System.Numerics.Matrix3x2) -> System.Numerics.Matrix3x2:
        """
        Subtracts each element in a second matrix from its corresponding element in a first matrix.
        
        :param value1: The first matrix.
        :param value2: The second matrix.
        :returns: The matrix containing the values that result from subtracting each element in  from its corresponding element in .
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Returns a value that indicates whether this instance and a specified object are equal.
        
        :param obj: The object to compare with the current instance.
        :returns: true if the current instance and  are equal; otherwise, false. If  is null, the method returns false.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Matrix3x2) -> bool:
        """
        Returns a value that indicates whether this instance and another 3x2 matrix are equal.
        
        :param other: The other matrix.
        :returns: true if the two matrices are equal; otherwise, false.
        """
        ...

    def GetDeterminant(self) -> float:
        """
        Calculates the determinant for this matrix.
        
        :returns: The determinant.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents this matrix.
        
        :returns: The string representation of this matrix.
        """
        ...


class Vector3(System.IEquatable[System_Numerics_Vector3], System.IFormattable):
    """Represents a vector with three  single-precision floating-point values."""

    @property
    def X(self) -> float:
        """The X component of the vector."""
        ...

    @X.setter
    def X(self, value: float):
        """The X component of the vector."""
        ...

    @property
    def Y(self) -> float:
        """The Y component of the vector."""
        ...

    @Y.setter
    def Y(self, value: float):
        """The Y component of the vector."""
        ...

    @property
    def Z(self) -> float:
        """The Z component of the vector."""
        ...

    @Z.setter
    def Z(self, value: float):
        """The Z component of the vector."""
        ...

    Zero: System.Numerics.Vector3
    """Gets a vector whose 3 elements are equal to zero."""

    One: System.Numerics.Vector3
    """Gets a vector whose 3 elements are equal to one."""

    UnitX: System.Numerics.Vector3
    """Gets the vector (1,0,0)."""

    UnitY: System.Numerics.Vector3
    """Gets the vector (0,1,0)."""

    UnitZ: System.Numerics.Vector3
    """Gets the vector (0,0,1)."""

    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Creates a new System.Numerics.Vector3 object whose three elements have the same value.
        
        :param value: The value to assign to all three elements.
        """
        ...

    @typing.overload
    def __init__(self, value: System.Numerics.Vector2, z: float) -> None:
        """
        Creates a   new System.Numerics.Vector3 object from the specified System.Numerics.Vector2 object and the specified value.
        
        :param value: The vector with two elements.
        :param z: The additional value to assign to the System.Numerics.Vector3.Z field.
        """
        ...

    @typing.overload
    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Creates a vector whose elements have the specified values.
        
        :param x: The value to assign to the System.Numerics.Vector3.X field.
        :param y: The value to assign to the System.Numerics.Vector3.Y field.
        :param z: The value to assign to the System.Numerics.Vector3.Z field.
        """
        ...

    @staticmethod
    def Abs(value: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a vector whose elements are the absolute values of each of the specified vector's elements.
        
        :param value: A vector.
        :returns: The absolute value vector.
        """
        ...

    @staticmethod
    def Add(left: System.Numerics.Vector3, right: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Adds two vectors together.
        
        :param left: The first vector to add.
        :param right: The second vector to add.
        :returns: The summed vector.
        """
        ...

    @staticmethod
    def Clamp(value1: System.Numerics.Vector3, min: System.Numerics.Vector3, max: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Restricts a vector between a minimum and a maximum value.
        
        :param value1: The vector to restrict.
        :param min: The minimum value.
        :param max: The maximum value.
        :returns: The restricted vector.
        """
        ...

    @staticmethod
    def Cross(vector1: System.Numerics.Vector3, vector2: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Computes the cross product of two vectors.
        
        :param vector1: The first vector.
        :param vector2: The second vector.
        :returns: The cross product.
        """
        ...

    @staticmethod
    def Distance(value1: System.Numerics.Vector3, value2: System.Numerics.Vector3) -> float:
        """
        Computes the Euclidean distance between the two given points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance.
        """
        ...

    @staticmethod
    def DistanceSquared(value1: System.Numerics.Vector3, value2: System.Numerics.Vector3) -> float:
        """
        Returns the Euclidean distance squared between two specified points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance squared.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector3, right: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Divides the first vector by the second.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The vector resulting from the division.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector3, divisor: float) -> System.Numerics.Vector3:
        """
        Divides the specified vector by a specified scalar value.
        
        :param left: The vector.
        :param divisor: The scalar value.
        :returns: The vector that results from the division.
        """
        ...

    @staticmethod
    def Dot(vector1: System.Numerics.Vector3, vector2: System.Numerics.Vector3) -> float:
        """
        Returns the dot product of two vectors.
        
        :param vector1: The first vector.
        :param vector2: The second vector.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def Lerp(value1: System.Numerics.Vector3, value2: System.Numerics.Vector3, amount: float) -> System.Numerics.Vector3:
        """
        Performs a linear interpolation between two vectors based on the given weighting.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :param amount: A value between 0 and 1 that indicates the weight of .
        :returns: The interpolated vector.
        """
        ...

    @staticmethod
    def Max(value1: System.Numerics.Vector3, value2: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a vector whose elements are the maximum of each of the pairs of elements in two specified vectors.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :returns: The maximized vector.
        """
        ...

    @staticmethod
    def Min(value1: System.Numerics.Vector3, value2: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a vector whose elements are the minimum of each of the pairs of elements in two specified vectors.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :returns: The minimized vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector3, right: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a new vector whose values are the product of each pair of elements in two specified vectors.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The element-wise product vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector3, right: float) -> System.Numerics.Vector3:
        """
        Multiplies a vector by a specified scalar.
        
        :param left: The vector to multiply.
        :param right: The scalar value.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: float, right: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Multiplies a scalar value by a specified vector.
        
        :param left: The scaled value.
        :param right: The vector.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Negates a specified vector.
        
        :param value: The vector to negate.
        :returns: The negated vector.
        """
        ...

    @staticmethod
    def Normalize(value: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a vector with the same direction as the specified vector, but with a length of one.
        
        :param value: The vector to normalize.
        :returns: The normalized vector.
        """
        ...

    @staticmethod
    def Reflect(vector: System.Numerics.Vector3, normal: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns the reflection of a vector off a surface that has the specified normal.
        
        :param vector: The source vector.
        :param normal: The normal of the surface being reflected off.
        :returns: The reflected vector.
        """
        ...

    @staticmethod
    def SquareRoot(value: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a vector whose elements are the square root of each of a specified vector's elements.
        
        :param value: A vector.
        :returns: The square root vector.
        """
        ...

    @staticmethod
    def Subtract(left: System.Numerics.Vector3, right: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Subtracts the second vector from the first.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The difference vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(position: System.Numerics.Vector3, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector3:
        """
        Transforms a vector by a specified 4x4 matrix.
        
        :param position: The vector to transform.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(value: System.Numerics.Vector3, rotation: System.Numerics.Quaternion) -> System.Numerics.Vector3:
        """
        Transforms a vector by the specified Quaternion rotation value.
        
        :param value: The vector to rotate.
        :param rotation: The rotation to apply.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    def TransformNormal(normal: System.Numerics.Vector3, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector3:
        """
        Transforms a vector normal by the given 4x4 matrix.
        
        :param normal: The source vector.
        :param matrix: The matrix.
        :returns: The transformed vector.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float]) -> None:
        """
        Copies the elements of the vector to a specified array.
        
        :param array: The destination array.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float], index: int) -> None:
        """
        Copies the elements of the vector to a specified array starting at a specified index position.
        
        :param array: The destination array.
        :param index: The index at which to copy the first element of the vector.
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Returns a value that indicates whether this instance and a specified object are equal.
        
        :param obj: The object to compare with the current instance.
        :returns: true if the current instance and  are equal; otherwise, false. If  is null, the method returns false.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Vector3) -> bool:
        """
        Returns a value that indicates whether this instance and another vector are equal.
        
        :param other: The other vector.
        :returns: true if the two vectors are equal; otherwise, false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def Length(self) -> float:
        """
        Returns the length of this vector object.
        
        :returns: The vector's length.
        """
        ...

    def LengthSquared(self) -> float:
        """
        Returns the length of the vector squared.
        
        :returns: The vector's length squared.
        """
        ...

    @typing.overload
    def ToString(self) -> str:
        """
        Returns the string representation of the current instance using default formatting.
        
        :returns: The string representation of the current instance.
        """
        ...

    @typing.overload
    def ToString(self, format: str) -> str:
        """
        Returns the string representation of the current instance using the specified format string to format individual elements.
        
        :param format: A standard or custom numeric format string that defines the format of individual elements.
        :returns: The string representation of the current instance.
        """
        ...

    @typing.overload
    def ToString(self, format: str, formatProvider: System.IFormatProvider) -> str:
        """
        Returns the string representation of the current instance using the specified format string to format individual elements and the specified format provider to define culture-specific formatting.
        
        :param format: A standard or custom numeric format string that defines the format of individual elements.
        :param formatProvider: A format provider that supplies culture-specific formatting information.
        :returns: The string representation of the current instance.
        """
        ...


class Quaternion(System.IEquatable[System_Numerics_Quaternion]):
    """Represents a vector that is used to encode three-dimensional physical rotations."""

    @property
    def X(self) -> float:
        """The X value of the vector component of the quaternion."""
        ...

    @X.setter
    def X(self, value: float):
        """The X value of the vector component of the quaternion."""
        ...

    @property
    def Y(self) -> float:
        """The Y value of the vector component of the quaternion."""
        ...

    @Y.setter
    def Y(self, value: float):
        """The Y value of the vector component of the quaternion."""
        ...

    @property
    def Z(self) -> float:
        """The Z value of the vector component of the quaternion."""
        ...

    @Z.setter
    def Z(self, value: float):
        """The Z value of the vector component of the quaternion."""
        ...

    @property
    def W(self) -> float:
        """The rotation component of the quaternion."""
        ...

    @W.setter
    def W(self, value: float):
        """The rotation component of the quaternion."""
        ...

    Identity: System.Numerics.Quaternion
    """Gets a quaternion that represents no rotation."""

    @property
    def IsIdentity(self) -> bool:
        """Gets a value that indicates whether the current instance is the identity quaternion."""
        ...

    @typing.overload
    def __init__(self, x: float, y: float, z: float, w: float) -> None:
        """
        Constructs a quaternion from the specified components.
        
        :param x: The value to assign to the X component of the quaternion.
        :param y: The value to assign to the Y component of the quaternion.
        :param z: The value to assign to the Z component of the quaternion.
        :param w: The value to assign to the W component of the quaternion.
        """
        ...

    @typing.overload
    def __init__(self, vectorPart: System.Numerics.Vector3, scalarPart: float) -> None:
        """
        Creates a quaternion from the specified vector and rotation parts.
        
        :param vectorPart: The vector part of the quaternion.
        :param scalarPart: The rotation part of the quaternion.
        """
        ...

    @staticmethod
    def Add(value1: System.Numerics.Quaternion, value2: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Adds each element in one quaternion with its corresponding element in a second quaternion.
        
        :param value1: The first quaternion.
        :param value2: The second quaternion.
        :returns: The quaternion that contains the summed values of  and .
        """
        ...

    @staticmethod
    def Concatenate(value1: System.Numerics.Quaternion, value2: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Concatenates two quaternions.
        
        :param value1: The first quaternion rotation in the series.
        :param value2: The second quaternion rotation in the series.
        :returns: A new quaternion representing the concatenation of the  rotation followed by the  rotation.
        """
        ...

    @staticmethod
    def Conjugate(value: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Returns the conjugate of a specified quaternion.
        
        :param value: The quaternion.
        :returns: A new quaternion that is the conjugate of value.
        """
        ...

    @staticmethod
    def CreateFromAxisAngle(axis: System.Numerics.Vector3, angle: float) -> System.Numerics.Quaternion:
        """
        Creates a quaternion from a unit vector and an angle to rotate around the vector.
        
        :param axis: The unit vector to rotate around.
        :param angle: The angle, in radians, to rotate around the vector.
        :returns: The newly created quaternion.
        """
        ...

    @staticmethod
    def CreateFromRotationMatrix(matrix: System.Numerics.Matrix4x4) -> System.Numerics.Quaternion:
        """
        Creates a quaternion from the specified rotation matrix.
        
        :param matrix: The rotation matrix.
        :returns: The newly created quaternion.
        """
        ...

    @staticmethod
    def CreateFromYawPitchRoll(yaw: float, pitch: float, roll: float) -> System.Numerics.Quaternion:
        """
        Creates a new quaternion from the given yaw, pitch, and roll.
        
        :param yaw: The yaw angle, in radians, around the Y axis.
        :param pitch: The pitch angle, in radians, around the X axis.
        :param roll: The roll angle, in radians, around the Z axis.
        :returns: The resulting quaternion.
        """
        ...

    @staticmethod
    def Divide(value1: System.Numerics.Quaternion, value2: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Divides one quaternion by a second quaternion.
        
        :param value1: The dividend.
        :param value2: The divisor.
        :returns: The quaternion that results from dividing  by .
        """
        ...

    @staticmethod
    def Dot(quaternion1: System.Numerics.Quaternion, quaternion2: System.Numerics.Quaternion) -> float:
        """
        Calculates the dot product of two quaternions.
        
        :param quaternion1: The first quaternion.
        :param quaternion2: The second quaternion.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def Inverse(value: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Returns the inverse of a quaternion.
        
        :param value: The quaternion.
        :returns: The inverted quaternion.
        """
        ...

    @staticmethod
    def Lerp(quaternion1: System.Numerics.Quaternion, quaternion2: System.Numerics.Quaternion, amount: float) -> System.Numerics.Quaternion:
        """
        Performs a linear interpolation between two quaternions based on a value that specifies the weighting of the second quaternion.
        
        :param quaternion1: The first quaternion.
        :param quaternion2: The second quaternion.
        :param amount: The relative weight of  in the interpolation.
        :returns: The interpolated quaternion.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Quaternion, value2: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Returns the quaternion that results from multiplying two quaternions together.
        
        :param value1: The first quaternion.
        :param value2: The second quaternion.
        :returns: The product quaternion.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Quaternion, value2: float) -> System.Numerics.Quaternion:
        """
        Returns the quaternion that results from scaling all the components of a specified quaternion by a scalar factor.
        
        :param value1: The source quaternion.
        :param value2: The scalar value.
        :returns: The scaled quaternion.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Reverses the sign of each component of the quaternion.
        
        :param value: The quaternion to negate.
        :returns: The negated quaternion.
        """
        ...

    @staticmethod
    def Normalize(value: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Divides each component of a specified System.Numerics.Quaternion by its length.
        
        :param value: The quaternion to normalize.
        :returns: The normalized quaternion.
        """
        ...

    @staticmethod
    def Slerp(quaternion1: System.Numerics.Quaternion, quaternion2: System.Numerics.Quaternion, amount: float) -> System.Numerics.Quaternion:
        """
        Interpolates between two quaternions, using spherical linear interpolation.
        
        :param quaternion1: The first quaternion.
        :param quaternion2: The second quaternion.
        :param amount: The relative weight of the second quaternion in the interpolation.
        :returns: The interpolated quaternion.
        """
        ...

    @staticmethod
    def Subtract(value1: System.Numerics.Quaternion, value2: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Subtracts each element in a second quaternion from its corresponding element in a first quaternion.
        
        :param value1: The first quaternion.
        :param value2: The second quaternion.
        :returns: The quaternion containing the values that result from subtracting each element in  from its corresponding element in .
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Returns a value that indicates whether this instance and a specified object are equal.
        
        :param obj: The object to compare with the current instance.
        :returns: true if the current instance and  are equal; otherwise, false. If  is null, the method returns false.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Quaternion) -> bool:
        """
        Returns a value that indicates whether this instance and another quaternion are equal.
        
        :param other: The other quaternion.
        :returns: true if the two quaternions are equal; otherwise, false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def Length(self) -> float:
        """
        Calculates the length of the quaternion.
        
        :returns: The computed length of the quaternion.
        """
        ...

    def LengthSquared(self) -> float:
        """
        Calculates the squared length of the quaternion.
        
        :returns: The length squared of the quaternion.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents this quaternion.
        
        :returns: The string representation of this quaternion.
        """
        ...


class Matrix4x4(System.IEquatable[System_Numerics_Matrix4x4]):
    """Represents a 4x4 matrix."""

    @property
    def M11(self) -> float:
        """The first element of the first row."""
        ...

    @M11.setter
    def M11(self, value: float):
        """The first element of the first row."""
        ...

    @property
    def M12(self) -> float:
        """The second element of the first row."""
        ...

    @M12.setter
    def M12(self, value: float):
        """The second element of the first row."""
        ...

    @property
    def M13(self) -> float:
        """The third element of the first row."""
        ...

    @M13.setter
    def M13(self, value: float):
        """The third element of the first row."""
        ...

    @property
    def M14(self) -> float:
        """The fourth element of the first row."""
        ...

    @M14.setter
    def M14(self, value: float):
        """The fourth element of the first row."""
        ...

    @property
    def M21(self) -> float:
        """The first element of the second row."""
        ...

    @M21.setter
    def M21(self, value: float):
        """The first element of the second row."""
        ...

    @property
    def M22(self) -> float:
        """The second element of the second row."""
        ...

    @M22.setter
    def M22(self, value: float):
        """The second element of the second row."""
        ...

    @property
    def M23(self) -> float:
        """The third element of the second row."""
        ...

    @M23.setter
    def M23(self, value: float):
        """The third element of the second row."""
        ...

    @property
    def M24(self) -> float:
        """The fourth element of the second row."""
        ...

    @M24.setter
    def M24(self, value: float):
        """The fourth element of the second row."""
        ...

    @property
    def M31(self) -> float:
        """The first element of the third row."""
        ...

    @M31.setter
    def M31(self, value: float):
        """The first element of the third row."""
        ...

    @property
    def M32(self) -> float:
        """The second element of the third row."""
        ...

    @M32.setter
    def M32(self, value: float):
        """The second element of the third row."""
        ...

    @property
    def M33(self) -> float:
        """The third element of the third row."""
        ...

    @M33.setter
    def M33(self, value: float):
        """The third element of the third row."""
        ...

    @property
    def M34(self) -> float:
        """The fourth element of the third row."""
        ...

    @M34.setter
    def M34(self, value: float):
        """The fourth element of the third row."""
        ...

    @property
    def M41(self) -> float:
        """The first element of the fourth row."""
        ...

    @M41.setter
    def M41(self, value: float):
        """The first element of the fourth row."""
        ...

    @property
    def M42(self) -> float:
        """The second element of the fourth row."""
        ...

    @M42.setter
    def M42(self, value: float):
        """The second element of the fourth row."""
        ...

    @property
    def M43(self) -> float:
        """The third element of the fourth row."""
        ...

    @M43.setter
    def M43(self, value: float):
        """The third element of the fourth row."""
        ...

    @property
    def M44(self) -> float:
        """The fourth element of the fourth row."""
        ...

    @M44.setter
    def M44(self, value: float):
        """The fourth element of the fourth row."""
        ...

    Identity: System.Numerics.Matrix4x4
    """Gets the multiplicative identity matrix."""

    @property
    def IsIdentity(self) -> bool:
        """Indicates whether the current matrix is the identity matrix."""
        ...

    @property
    def Translation(self) -> System.Numerics.Vector3:
        """Gets or sets the translation component of this matrix."""
        ...

    @Translation.setter
    def Translation(self, value: System.Numerics.Vector3):
        """Gets or sets the translation component of this matrix."""
        ...

    @typing.overload
    def __init__(self, m11: float, m12: float, m13: float, m14: float, m21: float, m22: float, m23: float, m24: float, m31: float, m32: float, m33: float, m34: float, m41: float, m42: float, m43: float, m44: float) -> None:
        """
        Creates a 4x4 matrix from the specified components.
        
        :param m11: The value to assign to the first element in the first row.
        :param m12: The value to assign to the second element in the first row.
        :param m13: The value to assign to the third element in the first row.
        :param m14: The value to assign to the fourth element in the first row.
        :param m21: The value to assign to the first element in the second row.
        :param m22: The value to assign to the second element in the second row.
        :param m23: The value to assign to the third element in the second row.
        :param m24: The value to assign to the third element in the second row.
        :param m31: The value to assign to the first element in the third row.
        :param m32: The value to assign to the second element in the third row.
        :param m33: The value to assign to the third element in the third row.
        :param m34: The value to assign to the fourth element in the third row.
        :param m41: The value to assign to the first element in the fourth row.
        :param m42: The value to assign to the second element in the fourth row.
        :param m43: The value to assign to the third element in the fourth row.
        :param m44: The value to assign to the fourth element in the fourth row.
        """
        ...

    @typing.overload
    def __init__(self, value: System.Numerics.Matrix3x2) -> None:
        """
        Creates a System.Numerics.Matrix4x4 object from a specified System.Numerics.Matrix3x2 object.
        
        :param value: A 3x2 matrix.
        """
        ...

    @staticmethod
    def Add(value1: System.Numerics.Matrix4x4, value2: System.Numerics.Matrix4x4) -> System.Numerics.Matrix4x4:
        """
        Adds each element in one matrix with its corresponding element in a second matrix.
        
        :param value1: The first matrix.
        :param value2: The second matrix.
        :returns: The matrix that contains the summed values of  and .
        """
        ...

    @staticmethod
    def CreateBillboard(objectPosition: System.Numerics.Vector3, cameraPosition: System.Numerics.Vector3, cameraUpVector: System.Numerics.Vector3, cameraForwardVector: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a spherical billboard that rotates around a specified object position.
        
        :param objectPosition: The position of the object that the billboard will rotate around.
        :param cameraPosition: The position of the camera.
        :param cameraUpVector: The up vector of the camera.
        :param cameraForwardVector: The forward vector of the camera.
        :returns: The created billboard.
        """
        ...

    @staticmethod
    def CreateConstrainedBillboard(objectPosition: System.Numerics.Vector3, cameraPosition: System.Numerics.Vector3, rotateAxis: System.Numerics.Vector3, cameraForwardVector: System.Numerics.Vector3, objectForwardVector: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a cylindrical billboard that rotates around a specified axis.
        
        :param objectPosition: The position of the object that the billboard will rotate around.
        :param cameraPosition: The position of the camera.
        :param rotateAxis: The axis to rotate the billboard around.
        :param cameraForwardVector: The forward vector of the camera.
        :param objectForwardVector: The forward vector of the object.
        :returns: The billboard matrix.
        """
        ...

    @staticmethod
    def CreateFromAxisAngle(axis: System.Numerics.Vector3, angle: float) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix that rotates around an arbitrary vector.
        
        :param axis: The axis to rotate around.
        :param angle: The angle to rotate around , in radians.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    def CreateFromQuaternion(quaternion: System.Numerics.Quaternion) -> System.Numerics.Matrix4x4:
        """
        Creates a rotation matrix from the specified Quaternion rotation value.
        
        :param quaternion: The source Quaternion.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    def CreateFromYawPitchRoll(yaw: float, pitch: float, roll: float) -> System.Numerics.Matrix4x4:
        """
        Creates a rotation matrix from the specified yaw, pitch, and roll.
        
        :param yaw: The angle of rotation, in radians, around the Y axis.
        :param pitch: The angle of rotation, in radians, around the X axis.
        :param roll: The angle of rotation, in radians, around the Z axis.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    def CreateLookAt(cameraPosition: System.Numerics.Vector3, cameraTarget: System.Numerics.Vector3, cameraUpVector: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a view matrix.
        
        :param cameraPosition: The position of the camera.
        :param cameraTarget: The target towards which the camera is pointing.
        :param cameraUpVector: The direction that is "up" from the camera's point of view.
        :returns: The view matrix.
        """
        ...

    @staticmethod
    def CreateOrthographic(width: float, height: float, zNearPlane: float, zFarPlane: float) -> System.Numerics.Matrix4x4:
        """
        Creates an orthographic perspective matrix from the given view volume dimensions.
        
        :param width: The width of the view volume.
        :param height: The height of the view volume.
        :param zNearPlane: The minimum Z-value of the view volume.
        :param zFarPlane: The maximum Z-value of the view volume.
        :returns: The orthographic projection matrix.
        """
        ...

    @staticmethod
    def CreateOrthographicOffCenter(left: float, right: float, bottom: float, top: float, zNearPlane: float, zFarPlane: float) -> System.Numerics.Matrix4x4:
        """
        Creates a customized orthographic projection matrix.
        
        :param left: The minimum X-value of the view volume.
        :param right: The maximum X-value of the view volume.
        :param bottom: The minimum Y-value of the view volume.
        :param top: The maximum Y-value of the view volume.
        :param zNearPlane: The minimum Z-value of the view volume.
        :param zFarPlane: The maximum Z-value of the view volume.
        :returns: The orthographic projection matrix.
        """
        ...

    @staticmethod
    def CreatePerspective(width: float, height: float, nearPlaneDistance: float, farPlaneDistance: float) -> System.Numerics.Matrix4x4:
        """
        Creates a perspective projection matrix from the given view volume dimensions.
        
        :param width: The width of the view volume at the near view plane.
        :param height: The height of the view volume at the near view plane.
        :param nearPlaneDistance: The distance to the near view plane.
        :param farPlaneDistance: The distance to the far view plane.
        :returns: The perspective projection matrix.
        """
        ...

    @staticmethod
    def CreatePerspectiveFieldOfView(fieldOfView: float, aspectRatio: float, nearPlaneDistance: float, farPlaneDistance: float) -> System.Numerics.Matrix4x4:
        """
        Creates a perspective projection matrix based on a field of view, aspect ratio, and near and far view plane distances.
        
        :param fieldOfView: The field of view in the y direction, in radians.
        :param aspectRatio: The aspect ratio, defined as view space width divided by height.
        :param nearPlaneDistance: The distance to the near view plane.
        :param farPlaneDistance: The distance to the far view plane.
        :returns: The perspective projection matrix.
        """
        ...

    @staticmethod
    def CreatePerspectiveOffCenter(left: float, right: float, bottom: float, top: float, nearPlaneDistance: float, farPlaneDistance: float) -> System.Numerics.Matrix4x4:
        """
        Creates a customized perspective projection matrix.
        
        :param left: The minimum x-value of the view volume at the near view plane.
        :param right: The maximum x-value of the view volume at the near view plane.
        :param bottom: The minimum y-value of the view volume at the near view plane.
        :param top: The maximum y-value of the view volume at the near view plane.
        :param nearPlaneDistance: The distance to the near view plane.
        :param farPlaneDistance: The distance to the far view plane.
        :returns: The perspective projection matrix.
        """
        ...

    @staticmethod
    def CreateReflection(value: System.Numerics.Plane) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix that reflects the coordinate system about a specified plane.
        
        :param value: The plane about which to create a reflection.
        :returns: A new matrix expressing the reflection.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationX(radians: float) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the X axis.
        
        :param radians: The amount, in radians, by which to rotate around the X axis.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationX(radians: float, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the X axis from a center point.
        
        :param radians: The amount, in radians, by which to rotate around the X axis.
        :param centerPoint: The center point.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationY(radians: float) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the Y axis.
        
        :param radians: The amount, in radians, by which to rotate around the Y-axis.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationY(radians: float, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        The amount, in radians, by which to rotate around the Y axis from a center point.
        
        :param radians: The amount, in radians, by which to rotate around the Y-axis.
        :param centerPoint: The center point.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationZ(radians: float) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the Z axis.
        
        :param radians: The amount, in radians, by which to rotate around the Z-axis.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationZ(radians: float, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the Z axis from a center point.
        
        :param radians: The amount, in radians, by which to rotate around the Z-axis.
        :param centerPoint: The center point.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(xScale: float, yScale: float, zScale: float) -> System.Numerics.Matrix4x4:
        """
        Creates a scaling matrix from the specified X, Y, and Z components.
        
        :param xScale: The value to scale by on the X axis.
        :param yScale: The value to scale by on the Y axis.
        :param zScale: The value to scale by on the Z axis.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(xScale: float, yScale: float, zScale: float, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a scaling matrix that is offset by a given center point.
        
        :param xScale: The value to scale by on the X axis.
        :param yScale: The value to scale by on the Y axis.
        :param zScale: The value to scale by on the Z axis.
        :param centerPoint: The center point.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scales: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a scaling matrix from the specified vector scale.
        
        :param scales: The scale to use.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scales: System.Numerics.Vector3, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a scaling matrix with a center point.
        
        :param scales: The vector that contains the amount to scale on each axis.
        :param centerPoint: The center point.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scale: float) -> System.Numerics.Matrix4x4:
        """
        Creates a uniform scaling matrix that scale equally on each axis.
        
        :param scale: The uniform scaling factor.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scale: float, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a uniform scaling matrix that scales equally on each axis with a center point.
        
        :param scale: The uniform scaling factor.
        :param centerPoint: The center point.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    def CreateShadow(lightDirection: System.Numerics.Vector3, plane: System.Numerics.Plane) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix that flattens geometry into a specified plane as if casting a shadow from a specified light source.
        
        :param lightDirection: The direction from which the light that will cast the shadow is coming.
        :param plane: The plane onto which the new matrix should flatten geometry so as to cast a shadow.
        :returns: A new matrix that can be used to flatten geometry onto the specified plane from the specified direction.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateTranslation(position: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a translation matrix from the specified 3-dimensional vector.
        
        :param position: The amount to translate in each axis.
        :returns: The translation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateTranslation(xPosition: float, yPosition: float, zPosition: float) -> System.Numerics.Matrix4x4:
        """
        Creates a translation matrix from the specified X, Y, and Z components.
        
        :param xPosition: The amount to translate on the X axis.
        :param yPosition: The amount to translate on the Y axis.
        :param zPosition: The amount to translate on the Z axis.
        :returns: The translation matrix.
        """
        ...

    @staticmethod
    def CreateWorld(position: System.Numerics.Vector3, forward: System.Numerics.Vector3, up: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a world matrix with the specified parameters.
        
        :param position: The position of the object.
        :param forward: The forward direction of the object.
        :param up: The upward direction of the object. Its value is usually [0, 1, 0].
        :returns: The world matrix.
        """
        ...

    @staticmethod
    def Invert(matrix: System.Numerics.Matrix4x4, result: System.Numerics.Matrix4x4) -> bool:
        """
        Tries to invert the specified matrix. The return value indicates whether the operation succeeded.
        
        :param matrix: The matrix to invert.
        :param result: When this method returns, contains the inverted matrix if the operation succeeded.
        :returns: true if  was converted successfully; otherwise,  false.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Matrix4x4, value2: System.Numerics.Matrix4x4) -> System.Numerics.Matrix4x4:
        """
        Multiplies two matrices together to compute the product.
        
        :param value1: The first matrix.
        :param value2: The second matrix.
        :returns: The product matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Matrix4x4, value2: float) -> System.Numerics.Matrix4x4:
        """
        Multiplies a matrix by a float to compute the product.
        
        :param value1: The matrix to scale.
        :param value2: The scaling value to use.
        :returns: The scaled matrix.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Matrix4x4) -> System.Numerics.Matrix4x4:
        """
        Negates the specified matrix by multiplying all its values by -1.
        
        :param value: The matrix to negate.
        :returns: The negated matrix.
        """
        ...

    @staticmethod
    def Subtract(value1: System.Numerics.Matrix4x4, value2: System.Numerics.Matrix4x4) -> System.Numerics.Matrix4x4:
        """
        Subtracts each element in a second matrix from its corresponding element in a first matrix.
        
        :param value1: The first matrix.
        :param value2: The second matrix.
        :returns: The matrix containing the values that result from subtracting each element in  from its corresponding element in .
        """
        ...

    @staticmethod
    def Decompose(matrix: System.Numerics.Matrix4x4, scale: System.Numerics.Vector3, rotation: System.Numerics.Quaternion, translation: System.Numerics.Vector3) -> bool:
        """
        Attempts to extract the scale, translation, and rotation components from the given scale, rotation, or translation matrix. The return value indicates whether the operation succeeded.
        
        :param matrix: The source matrix.
        :param scale: When this method returns, contains the scaling component of the transformation matrix if the operation succeeded.
        :param rotation: When this method returns, contains the rotation component of the transformation matrix if the operation succeeded.
        :param translation: When the method returns, contains the translation component of the transformation matrix if the operation succeeded.
        :returns: true if  was decomposed successfully; otherwise,  false.
        """
        ...

    @staticmethod
    def Lerp(matrix1: System.Numerics.Matrix4x4, matrix2: System.Numerics.Matrix4x4, amount: float) -> System.Numerics.Matrix4x4:
        """
        Performs a linear interpolation from one matrix to a second matrix based on a value that specifies the weighting of the second matrix.
        
        :param matrix1: The first matrix.
        :param matrix2: The second matrix.
        :param amount: The relative weighting of .
        :returns: The interpolated matrix.
        """
        ...

    @staticmethod
    def Transform(value: System.Numerics.Matrix4x4, rotation: System.Numerics.Quaternion) -> System.Numerics.Matrix4x4:
        """
        Transforms the specified matrix by applying the specified Quaternion rotation.
        
        :param value: The matrix to transform.
        :param rotation: The rotation t apply.
        :returns: The transformed matrix.
        """
        ...

    @staticmethod
    def Transpose(matrix: System.Numerics.Matrix4x4) -> System.Numerics.Matrix4x4:
        """
        Transposes the rows and columns of a matrix.
        
        :param matrix: The matrix to transpose.
        :returns: The transposed matrix.
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Returns a value that indicates whether this instance and a specified object are equal.
        
        :param obj: The object to compare with the current instance.
        :returns: true if the current instance and  are equal; otherwise, false. If  is null, the method returns false.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Matrix4x4) -> bool:
        """
        Returns a value that indicates whether this instance and another 4x4 matrix are equal.
        
        :param other: The other matrix.
        :returns: true if the two matrices are equal; otherwise, false.
        """
        ...

    def GetDeterminant(self) -> float:
        """
        Calculates the determinant of the current 4x4 matrix.
        
        :returns: The determinant.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents this matrix.
        
        :returns: The string representation of this matrix.
        """
        ...


class Vector2(System.IEquatable[System_Numerics_Vector2], System.IFormattable):
    """Represents a vector with two single-precision floating-point values."""

    @property
    def X(self) -> float:
        """The X component of the vector."""
        ...

    @X.setter
    def X(self, value: float):
        """The X component of the vector."""
        ...

    @property
    def Y(self) -> float:
        """The Y component of the vector."""
        ...

    @Y.setter
    def Y(self, value: float):
        """The Y component of the vector."""
        ...

    Zero: System.Numerics.Vector2
    """Returns a vector whose 2 elements are equal to zero."""

    One: System.Numerics.Vector2
    """Gets a vector whose 2 elements are equal to one."""

    UnitX: System.Numerics.Vector2
    """Gets the vector (1,0)."""

    UnitY: System.Numerics.Vector2
    """Gets the vector (0,1)."""

    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Creates a new System.Numerics.Vector2 object whose two elements have the same value.
        
        :param value: The value to assign to both elements.
        """
        ...

    @typing.overload
    def __init__(self, x: float, y: float) -> None:
        """
        Creates a vector whose elements have the specified values.
        
        :param x: The value to assign to the System.Numerics.Vector2.X field.
        :param y: The value to assign to the System.Numerics.Vector2.Y field.
        """
        ...

    @staticmethod
    def Abs(value: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a vector whose elements are the absolute values of each of the specified vector's elements.
        
        :param value: A vector.
        :returns: The absolute value vector.
        """
        ...

    @staticmethod
    def Add(left: System.Numerics.Vector2, right: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Adds two vectors together.
        
        :param left: The first vector to add.
        :param right: The second vector to add.
        :returns: The summed vector.
        """
        ...

    @staticmethod
    def Clamp(value1: System.Numerics.Vector2, min: System.Numerics.Vector2, max: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Restricts a vector between a minimum and a maximum value.
        
        :param value1: The vector to restrict.
        :param min: The minimum value.
        :param max: The maximum value.
        :returns: The restricted vector.
        """
        ...

    @staticmethod
    def Distance(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2) -> float:
        """
        Computes the Euclidean distance between the two given points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance.
        """
        ...

    @staticmethod
    def DistanceSquared(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2) -> float:
        """
        Returns the Euclidean distance squared between two specified points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance squared.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector2, right: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Divides the first vector by the second.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The vector resulting from the division.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector2, divisor: float) -> System.Numerics.Vector2:
        """
        Divides the specified vector by a specified scalar value.
        
        :param left: The vector.
        :param divisor: The scalar value.
        :returns: The vector that results from the division.
        """
        ...

    @staticmethod
    def Dot(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2) -> float:
        """
        Returns the dot product of two vectors.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def Lerp(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2, amount: float) -> System.Numerics.Vector2:
        """
        Performs a linear interpolation between two vectors based on the given weighting.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :param amount: A value between 0 and 1 that indicates the weight of .
        :returns: The interpolated vector.
        """
        ...

    @staticmethod
    def Max(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a vector whose elements are the maximum of each of the pairs of elements in two specified vectors.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :returns: The maximized vector.
        """
        ...

    @staticmethod
    def Min(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a vector whose elements are the minimum of each of the pairs of elements in two specified vectors.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :returns: The minimized vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector2, right: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a new vector whose values are the product of each pair of elements in two specified vectors.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The element-wise product vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector2, right: float) -> System.Numerics.Vector2:
        """
        Multiplies a vector by a specified scalar.
        
        :param left: The vector to multiply.
        :param right: The scalar value.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: float, right: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Multiplies a scalar value by a specified vector.
        
        :param left: The scaled value.
        :param right: The vector.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Negates a specified vector.
        
        :param value: The vector to negate.
        :returns: The negated vector.
        """
        ...

    @staticmethod
    def Normalize(value: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a vector with the same direction as the specified vector, but with a length of one.
        
        :param value: The vector to normalize.
        :returns: The normalized vector.
        """
        ...

    @staticmethod
    def Reflect(vector: System.Numerics.Vector2, normal: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns the reflection of a vector off a surface that has the specified normal.
        
        :param vector: The source vector.
        :param normal: The normal of the surface being reflected off.
        :returns: The reflected vector.
        """
        ...

    @staticmethod
    def SquareRoot(value: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a vector whose elements are the square root of each of a specified vector's elements.
        
        :param value: A vector.
        :returns: The square root vector.
        """
        ...

    @staticmethod
    def Subtract(left: System.Numerics.Vector2, right: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Subtracts the second vector from the first.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The difference vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(position: System.Numerics.Vector2, matrix: System.Numerics.Matrix3x2) -> System.Numerics.Vector2:
        """
        Transforms a vector by a specified 3x2 matrix.
        
        :param position: The vector to transform.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(position: System.Numerics.Vector2, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector2:
        """
        Transforms a vector by a specified 4x4 matrix.
        
        :param position: The vector to transform.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(value: System.Numerics.Vector2, rotation: System.Numerics.Quaternion) -> System.Numerics.Vector2:
        """
        Transforms a vector by the specified Quaternion rotation value.
        
        :param value: The vector to rotate.
        :param rotation: The rotation to apply.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def TransformNormal(normal: System.Numerics.Vector2, matrix: System.Numerics.Matrix3x2) -> System.Numerics.Vector2:
        """
        Transforms a vector normal by the given 3x2 matrix.
        
        :param normal: The source vector.
        :param matrix: The matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def TransformNormal(normal: System.Numerics.Vector2, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector2:
        """
        Transforms a vector normal by the given 4x4 matrix.
        
        :param normal: The source vector.
        :param matrix: The matrix.
        :returns: The transformed vector.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float]) -> None:
        """
        Copies the elements of the vector to a specified array.
        
        :param array: The destination array.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float], index: int) -> None:
        """
        Copies the elements of the vector to a specified array starting at a specified index position.
        
        :param array: The destination array.
        :param index: The index at which to copy the first element of the vector.
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Returns a value that indicates whether this instance and a specified object are equal.
        
        :param obj: The object to compare with the current instance.
        :returns: true if the current instance and  are equal; otherwise, false. If  is null, the method returns false.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Vector2) -> bool:
        """
        Returns a value that indicates whether this instance and another vector are equal.
        
        :param other: The other vector.
        :returns: true if the two vectors are equal; otherwise, false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def Length(self) -> float:
        """
        Returns the length of the vector.
        
        :returns: The vector's length.
        """
        ...

    def LengthSquared(self) -> float:
        """
        Returns the length of the vector squared.
        
        :returns: The vector's length squared.
        """
        ...

    @typing.overload
    def ToString(self) -> str:
        """
        Returns the string representation of the current instance using default formatting.
        
        :returns: The string representation of the current instance.
        """
        ...

    @typing.overload
    def ToString(self, format: str) -> str:
        """
        Returns the string representation of the current instance using the specified format string to format individual elements.
        
        :param format: A standard or custom numeric format string that defines the format of individual elements.
        :returns: The string representation of the current instance.
        """
        ...

    @typing.overload
    def ToString(self, format: str, formatProvider: System.IFormatProvider) -> str:
        """
        Returns the string representation of the current instance using the specified format string to format individual elements and the specified format provider to define culture-specific formatting.
        
        :param format: A standard or custom numeric format string that defines the format of individual elements.
        :param formatProvider: A format provider that supplies culture-specific formatting information.
        :returns: The string representation of the current instance.
        """
        ...


class BitOperations(System.Object):
    """
    Utility methods for intrinsic bit-twiddling operations.
    The methods use hardware intrinsics when available on the underlying platform,
    otherwise they use optimized software fallbacks.
    """

    @staticmethod
    @typing.overload
    def IsPow2(value: int) -> bool:
        """
        Evaluate whether a given integral value is a power of 2.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def IsPow2(value: int) -> bool:
        """
        Evaluate whether a given integral value is a power of 2.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def IsPow2(value: int) -> bool:
        """
        Evaluate whether a given integral value is a power of 2.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def IsPow2(value: int) -> bool:
        """
        Evaluate whether a given integral value is a power of 2.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def LeadingZeroCount(value: int) -> int:
        """
        Count the number of leading zero bits in a mask.
        Similar in behavior to the x86 instruction LZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def LeadingZeroCount(value: int) -> int:
        """
        Count the number of leading zero bits in a mask.
        Similar in behavior to the x86 instruction LZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def Log2(value: int) -> int:
        """
        Returns the integer (floor) log of the specified value, base 2.
        Note that by convention, input value 0 returns 0 since log(0) is undefined.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def Log2(value: int) -> int:
        """
        Returns the integer (floor) log of the specified value, base 2.
        Note that by convention, input value 0 returns 0 since log(0) is undefined.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def PopCount(value: int) -> int:
        """
        Returns the population count (number of bits set) of a mask.
        Similar in behavior to the x86 instruction POPCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def PopCount(value: int) -> int:
        """
        Returns the population count (number of bits set) of a mask.
        Similar in behavior to the x86 instruction POPCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def TrailingZeroCount(value: int) -> int:
        """
        Count the number of trailing zero bits in an integer value.
        Similar in behavior to the x86 instruction TZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def TrailingZeroCount(value: int) -> int:
        """
        Count the number of trailing zero bits in an integer value.
        Similar in behavior to the x86 instruction TZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def TrailingZeroCount(value: int) -> int:
        """
        Count the number of trailing zero bits in a mask.
        Similar in behavior to the x86 instruction TZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def TrailingZeroCount(value: int) -> int:
        """
        Count the number of trailing zero bits in a mask.
        Similar in behavior to the x86 instruction TZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def RotateLeft(value: int, offset: int) -> int:
        """
        Rotates the specified value left by the specified number of bits.
        Similar in behavior to the x86 instruction ROL.
        
        :param value: The value to rotate.
        :param offset: The number of bits to rotate by. Any value outside the range [0..31] is treated as congruent mod 32.
        :returns: The rotated value.
        """
        ...

    @staticmethod
    @typing.overload
    def RotateLeft(value: int, offset: int) -> int:
        """
        Rotates the specified value left by the specified number of bits.
        Similar in behavior to the x86 instruction ROL.
        
        :param value: The value to rotate.
        :param offset: The number of bits to rotate by. Any value outside the range [0..63] is treated as congruent mod 64.
        :returns: The rotated value.
        """
        ...

    @staticmethod
    @typing.overload
    def RotateRight(value: int, offset: int) -> int:
        """
        Rotates the specified value right by the specified number of bits.
        Similar in behavior to the x86 instruction ROR.
        
        :param value: The value to rotate.
        :param offset: The number of bits to rotate by. Any value outside the range [0..31] is treated as congruent mod 32.
        :returns: The rotated value.
        """
        ...

    @staticmethod
    @typing.overload
    def RotateRight(value: int, offset: int) -> int:
        """
        Rotates the specified value right by the specified number of bits.
        Similar in behavior to the x86 instruction ROR.
        
        :param value: The value to rotate.
        :param offset: The number of bits to rotate by. Any value outside the range [0..63] is treated as congruent mod 64.
        :returns: The rotated value.
        """
        ...


class Vector4(System.IEquatable[System_Numerics_Vector4], System.IFormattable):
    """Represents a vector with four single-precision floating-point values."""

    @property
    def X(self) -> float:
        """The X component of the vector."""
        ...

    @X.setter
    def X(self, value: float):
        """The X component of the vector."""
        ...

    @property
    def Y(self) -> float:
        """The Y component of the vector."""
        ...

    @Y.setter
    def Y(self, value: float):
        """The Y component of the vector."""
        ...

    @property
    def Z(self) -> float:
        """The Z component of the vector."""
        ...

    @Z.setter
    def Z(self, value: float):
        """The Z component of the vector."""
        ...

    @property
    def W(self) -> float:
        """The W component of the vector."""
        ...

    @W.setter
    def W(self, value: float):
        """The W component of the vector."""
        ...

    Zero: System.Numerics.Vector4
    """Gets a vector whose 4 elements are equal to zero."""

    One: System.Numerics.Vector4
    """Gets a vector whose 4 elements are equal to one."""

    UnitX: System.Numerics.Vector4
    """Gets the vector (1,0,0,0)."""

    UnitY: System.Numerics.Vector4
    """Gets the vector (0,1,0,0)."""

    UnitZ: System.Numerics.Vector4
    """Gets the vector (0,0,1,0)."""

    UnitW: System.Numerics.Vector4
    """Gets the vector (0,0,0,1)."""

    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Creates a new System.Numerics.Vector4 object whose four elements have the same value.
        
        :param value: The value to assign to all four elements.
        """
        ...

    @typing.overload
    def __init__(self, value: System.Numerics.Vector2, z: float, w: float) -> None:
        """
        Creates a   new System.Numerics.Vector4 object from the specified System.Numerics.Vector2 object and a Z and a W component.
        
        :param value: The vector to use for the X and Y components.
        :param z: The Z component.
        :param w: The W component.
        """
        ...

    @typing.overload
    def __init__(self, value: System.Numerics.Vector3, w: float) -> None:
        """
        Constructs a new System.Numerics.Vector4 object from the specified System.Numerics.Vector3 object and a W component.
        
        :param value: The vector to use for the X, Y, and Z components.
        :param w: The W component.
        """
        ...

    @typing.overload
    def __init__(self, x: float, y: float, z: float, w: float) -> None:
        """
        Creates a vector whose elements have the specified values.
        
        :param x: The value to assign to the System.Numerics.Vector4.X field.
        :param y: The value to assign to the System.Numerics.Vector4.Y field.
        :param z: The value to assign to the System.Numerics.Vector4.Z field.
        :param w: The value to assign to the System.Numerics.Vector4.W field.
        """
        ...

    @staticmethod
    def Abs(value: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a vector whose elements are the absolute values of each of the specified vector's elements.
        
        :param value: A vector.
        :returns: The absolute value vector.
        """
        ...

    @staticmethod
    def Add(left: System.Numerics.Vector4, right: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Adds two vectors together.
        
        :param left: The first vector to add.
        :param right: The second vector to add.
        :returns: The summed vector.
        """
        ...

    @staticmethod
    def Clamp(value1: System.Numerics.Vector4, min: System.Numerics.Vector4, max: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Restricts a vector between a minimum and a maximum value.
        
        :param value1: The vector to restrict.
        :param min: The minimum value.
        :param max: The maximum value.
        :returns: The restricted vector.
        """
        ...

    @staticmethod
    def Distance(value1: System.Numerics.Vector4, value2: System.Numerics.Vector4) -> float:
        """
        Computes the Euclidean distance between the two given points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance.
        """
        ...

    @staticmethod
    def DistanceSquared(value1: System.Numerics.Vector4, value2: System.Numerics.Vector4) -> float:
        """
        Returns the Euclidean distance squared between two specified points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance squared.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector4, right: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Divides the first vector by the second.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The vector resulting from the division.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector4, divisor: float) -> System.Numerics.Vector4:
        """
        Divides the specified vector by a specified scalar value.
        
        :param left: The vector.
        :param divisor: The scalar value.
        :returns: The vector that results from the division.
        """
        ...

    @staticmethod
    def Dot(vector1: System.Numerics.Vector4, vector2: System.Numerics.Vector4) -> float:
        """
        Returns the dot product of two vectors.
        
        :param vector1: The first vector.
        :param vector2: The second vector.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def Lerp(value1: System.Numerics.Vector4, value2: System.Numerics.Vector4, amount: float) -> System.Numerics.Vector4:
        """
        Performs a linear interpolation between two vectors based on the given weighting.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :param amount: A value between 0 and 1 that indicates the weight of .
        :returns: The interpolated vector.
        """
        ...

    @staticmethod
    def Max(value1: System.Numerics.Vector4, value2: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a vector whose elements are the maximum of each of the pairs of elements in two specified vectors.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :returns: The maximized vector.
        """
        ...

    @staticmethod
    def Min(value1: System.Numerics.Vector4, value2: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a vector whose elements are the minimum of each of the pairs of elements in two specified vectors.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :returns: The minimized vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector4, right: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a new vector whose values are the product of each pair of elements in two specified vectors.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The element-wise product vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector4, right: float) -> System.Numerics.Vector4:
        """
        Multiplies a vector by a specified scalar.
        
        :param left: The vector to multiply.
        :param right: The scalar value.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: float, right: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Multiplies a scalar value by a specified vector.
        
        :param left: The scaled value.
        :param right: The vector.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Negates a specified vector.
        
        :param value: The vector to negate.
        :returns: The negated vector.
        """
        ...

    @staticmethod
    def Normalize(vector: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a vector with the same direction as the specified vector, but with a length of one.
        
        :param vector: The vector to normalize.
        :returns: The normalized vector.
        """
        ...

    @staticmethod
    def SquareRoot(value: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a vector whose elements are the square root of each of a specified vector's elements.
        
        :param value: A vector.
        :returns: The square root vector.
        """
        ...

    @staticmethod
    def Subtract(left: System.Numerics.Vector4, right: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Subtracts the second vector from the first.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The difference vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(position: System.Numerics.Vector2, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector4:
        """
        Transforms a two-dimensional vector by a specified 4x4 matrix.
        
        :param position: The vector to transform.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(value: System.Numerics.Vector2, rotation: System.Numerics.Quaternion) -> System.Numerics.Vector4:
        """
        Transforms a two-dimensional vector by the specified Quaternion rotation value.
        
        :param value: The vector to rotate.
        :param rotation: The rotation to apply.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(position: System.Numerics.Vector3, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector4:
        """
        Transforms a three-dimensional vector by a specified 4x4 matrix.
        
        :param position: The vector to transform.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(value: System.Numerics.Vector3, rotation: System.Numerics.Quaternion) -> System.Numerics.Vector4:
        """
        Transforms a three-dimensional vector by the specified Quaternion rotation value.
        
        :param value: The vector to rotate.
        :param rotation: The rotation to apply.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(vector: System.Numerics.Vector4, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector4:
        """
        Transforms a four-dimensional vector by a specified 4x4 matrix.
        
        :param vector: The vector to transform.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(value: System.Numerics.Vector4, rotation: System.Numerics.Quaternion) -> System.Numerics.Vector4:
        """
        Transforms a four-dimensional vector by the specified Quaternion rotation value.
        
        :param value: The vector to rotate.
        :param rotation: The rotation to apply.
        :returns: The transformed vector.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float]) -> None:
        """
        Copies the elements of the vector to a specified array.
        
        :param array: The destination array.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float], index: int) -> None:
        """
        Copies the elements of the vector to a specified array starting at a specified index position.
        
        :param array: The destination array.
        :param index: The index at which to copy the first element of the vector.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Vector4) -> bool:
        """
        Returns a value that indicates whether this instance and another vector are equal.
        
        :param other: The other vector.
        :returns: true if the two vectors are equal; otherwise, false.
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Returns a value that indicates whether this instance and a specified object are equal.
        
        :param obj: The object to compare with the current instance.
        :returns: true if the current instance and  are equal; otherwise, false. If  is null, the method returns false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def Length(self) -> float:
        """
        Returns the length of this vector object.
        
        :returns: The vector's length.
        """
        ...

    def LengthSquared(self) -> float:
        """
        Returns the length of the vector squared.
        
        :returns: The vector's length squared.
        """
        ...

    @typing.overload
    def ToString(self) -> str:
        """
        Returns the string representation of the current instance using default formatting.
        
        :returns: The string representation of the current instance.
        """
        ...

    @typing.overload
    def ToString(self, format: str) -> str:
        """
        Returns the string representation of the current instance using the specified format string to format individual elements.
        
        :param format: A standard or custom numeric format string that defines the format of individual elements.
        :returns: The string representation of the current instance.
        """
        ...

    @typing.overload
    def ToString(self, format: str, formatProvider: System.IFormatProvider) -> str:
        """
        Returns the string representation of the current instance using the specified format string to format individual elements and the specified format provider to define culture-specific formatting.
        
        :param format: A standard or custom numeric format string that defines the format of individual elements.
        :param formatProvider: A format provider that supplies culture-specific formatting information.
        :returns: The string representation of the current instance.
        """
        ...


class Plane(System.IEquatable[System_Numerics_Plane]):
    """Represents a plane in three-dimensional space."""

    @property
    def Normal(self) -> System.Numerics.Vector3:
        """The normal vector of the plane."""
        ...

    @Normal.setter
    def Normal(self, value: System.Numerics.Vector3):
        """The normal vector of the plane."""
        ...

    @property
    def D(self) -> float:
        """The distance of the plane along its normal from the origin."""
        ...

    @D.setter
    def D(self, value: float):
        """The distance of the plane along its normal from the origin."""
        ...

    @typing.overload
    def __init__(self, x: float, y: float, z: float, d: float) -> None:
        """
        Creates a System.Numerics.Plane object from the X, Y, and Z components of its normal, and its distance from the origin on that normal.
        
        :param x: The X component of the normal.
        :param y: The Y component of the normal.
        :param z: The Z component of the normal.
        :param d: The distance of the plane along its normal from the origin.
        """
        ...

    @typing.overload
    def __init__(self, normal: System.Numerics.Vector3, d: float) -> None:
        """
        Creates a System.Numerics.Plane object from a specified normal and the distance along the normal from the origin.
        
        :param normal: The plane's normal vector.
        :param d: The plane's distance from the origin along its normal vector.
        """
        ...

    @typing.overload
    def __init__(self, value: System.Numerics.Vector4) -> None:
        """
        Creates a System.Numerics.Plane object from a specified four-dimensional vector.
        
        :param value: A vector whose first three elements describe the normal vector, and whose System.Numerics.Vector4.W defines the distance along that normal from the origin.
        """
        ...

    @staticmethod
    def CreateFromVertices(point1: System.Numerics.Vector3, point2: System.Numerics.Vector3, point3: System.Numerics.Vector3) -> System.Numerics.Plane:
        """
        Creates a System.Numerics.Plane object that contains three specified points.
        
        :param point1: The first point defining the plane.
        :param point2: The second point defining the plane.
        :param point3: The third point defining the plane.
        :returns: The plane containing the three points.
        """
        ...

    @staticmethod
    def Dot(plane: System.Numerics.Plane, value: System.Numerics.Vector4) -> float:
        """
        Calculates the dot product of a plane and a 4-dimensional vector.
        
        :param plane: The plane.
        :param value: The four-dimensional vector.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def DotCoordinate(plane: System.Numerics.Plane, value: System.Numerics.Vector3) -> float:
        """
        Returns the dot product of a specified three-dimensional vector and the normal vector of this plane plus the distance (System.Numerics.Plane.D) value of the plane.
        
        :param plane: The plane.
        :param value: The 3-dimensional vector.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def DotNormal(plane: System.Numerics.Plane, value: System.Numerics.Vector3) -> float:
        """
        Returns the dot product of a specified three-dimensional vector and the System.Numerics.Plane.Normal vector of this plane.
        
        :param plane: The plane.
        :param value: The three-dimensional vector.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def Normalize(value: System.Numerics.Plane) -> System.Numerics.Plane:
        """
        Creates a new System.Numerics.Plane object whose normal vector is the source plane's normal vector normalized.
        
        :param value: The source plane.
        :returns: The normalized plane.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(plane: System.Numerics.Plane, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Plane:
        """
        Transforms a normalized plane by a 4x4 matrix.
        
        :param plane: The normalized plane to transform.
        :param matrix: The transformation matrix to apply to .
        :returns: The transformed plane.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(plane: System.Numerics.Plane, rotation: System.Numerics.Quaternion) -> System.Numerics.Plane:
        """
        Transforms a normalized plane by a Quaternion rotation.
        
        :param plane: The normalized plane to transform.
        :param rotation: The Quaternion rotation to apply to the plane.
        :returns: A new plane that results from applying the Quaternion rotation.
        """
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Returns a value that indicates whether this instance and a specified object are equal.
        
        :param obj: The object to compare with the current instance.
        :returns: true if the current instance and  are equal; otherwise, false. If  is null, the method returns false.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Plane) -> bool:
        """
        Returns a value that indicates whether this instance and another plane object are equal.
        
        :param other: The other plane.
        :returns: true if the two planes are equal; otherwise, false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def ToString(self) -> str:
        """
        Returns the string representation of this plane object.
        
        :returns: A string that represents this System.Numerics.Plane object.
        """
        ...


class Vector(typing.Generic[System_Numerics_Vector_T], System.IEquatable[System_Numerics_Vector], System.IFormattable):
    """This class has no documentation."""

    IsHardwareAccelerated: bool
    """Gets a value that indicates whether vector operations are subject to hardware acceleration through JIT intrinsic support."""

    Count: int
    """Returns the number of elements stored in the vector. This value is hardware dependent."""

    Zero: System.Numerics.Vector[System_Numerics_Vector_T]
    """Returns a vector containing all zeroes."""

    One: System.Numerics.Vector[System_Numerics_Vector_T]
    """Returns a vector containing all ones."""

    AllBitsSet: System.Numerics.Vector[System_Numerics_Vector_T]

    @staticmethod
    @typing.overload
    def ConditionalSelect(condition: System.Numerics.Vector[int], left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Creates a new single-precision vector with elements selected between two specified single-precision source vectors based on an integral mask vector.
        
        :param condition: The integral mask vector used to drive selection.
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The new vector with elements selected based on the mask.
        """
        ...

    @staticmethod
    @typing.overload
    def ConditionalSelect(condition: System.Numerics.Vector[int], left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Creates a new double-precision vector with elements selected between two specified double-precision source vectors based on an integral mask vector.
        
        :param condition: The integral mask vector used to drive selection.
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The new vector with elements selected based on the mask.
        """
        ...

    @staticmethod
    @typing.overload
    def ConditionalSelect(condition: System.Numerics.Vector[System_Numerics_Vector_ConditionalSelect_T], left: System.Numerics.Vector[System_Numerics_Vector_ConditionalSelect_T], right: System.Numerics.Vector[System_Numerics_Vector_ConditionalSelect_T]) -> System.Numerics.Vector[System_Numerics_Vector_ConditionalSelect_T]:
        """
        Creates a new vector of a specified type with elements selected between two specified source vectors of the same type based on an integral mask vector.
        
        :param condition: The integral mask vector used to drive selection.
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The new vector with elements selected based on the mask.
        """
        ...

    @staticmethod
    @typing.overload
    def Equals(left: System.Numerics.Vector[System_Numerics_Vector_Equals_T], right: System.Numerics.Vector[System_Numerics_Vector_Equals_T]) -> System.Numerics.Vector[System_Numerics_Vector_Equals_T]:
        """
        Returns a new vector of a specified type whose elements signal whether the elements in two specified vectors of the same type are equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Equals(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in two specified single-precision vectors are equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Equals(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in two specified integral vectors are equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Equals(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in two specified double-precision vectors are equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Equals(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in two specified long integer vectors are equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting long integer vector.
        """
        ...

    @staticmethod
    def EqualsAll(left: System.Numerics.Vector[System_Numerics_Vector_EqualsAll_T], right: System.Numerics.Vector[System_Numerics_Vector_EqualsAll_T]) -> bool:
        """
        Returns a value that indicates whether each pair of elements in the given vectors is equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: true if all elements in  and  are equal; otherwise, false.
        """
        ...

    @staticmethod
    def EqualsAny(left: System.Numerics.Vector[System_Numerics_Vector_EqualsAny_T], right: System.Numerics.Vector[System_Numerics_Vector_EqualsAny_T]) -> bool:
        """
        Returns a value that indicates whether any single pair of elements in the given vectors is equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: true if any element pair in  and  is equal; otherwise, false.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThan(left: System.Numerics.Vector[System_Numerics_Vector_LessThan_T], right: System.Numerics.Vector[System_Numerics_Vector_LessThan_T]) -> System.Numerics.Vector[System_Numerics_Vector_LessThan_T]:
        """
        Returns a new vector of a specified type whose elements signal whether the elements in one vector are less than their corresponding elements in the second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThan(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one single-precision vector are less than their corresponding elements in a second single-precision vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThan(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one integral vector are less than their corresponding elements in a second integral vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThan(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one double-precision floating-point vector are less than their corresponding elements in a second double-precision floating-point vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThan(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new long integer vector whose elements signal whether the elements in one long integer vector are less than their corresponding elements in a second long integer vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting long integer vector.
        """
        ...

    @staticmethod
    def LessThanAll(left: System.Numerics.Vector[System_Numerics_Vector_LessThanAll_T], right: System.Numerics.Vector[System_Numerics_Vector_LessThanAll_T]) -> bool:
        """
        Returns a value that indicates whether all of the elements in the first vector are less than their corresponding elements in the second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: true if all of the elements in  are less than the corresponding elements in ; otherwise,  false.
        """
        ...

    @staticmethod
    def LessThanAny(left: System.Numerics.Vector[System_Numerics_Vector_LessThanAny_T], right: System.Numerics.Vector[System_Numerics_Vector_LessThanAny_T]) -> bool:
        """
        Returns a value that indicates whether any element in the first vector is less than the corresponding element in the second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: true if any element in  is less than the corresponding element in ; otherwise,  false.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThanOrEqual(left: System.Numerics.Vector[System_Numerics_Vector_LessThanOrEqual_T], right: System.Numerics.Vector[System_Numerics_Vector_LessThanOrEqual_T]) -> System.Numerics.Vector[System_Numerics_Vector_LessThanOrEqual_T]:
        """
        Returns a new vector whose elements signal whether the elements in one vector are less than or equal to their corresponding elements in the second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThanOrEqual(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one single-precision floating-point vector are less than or equal to their corresponding elements in a second single-precision floating-point vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThanOrEqual(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one integral vector are less than or equal to their corresponding elements in a second integral vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThanOrEqual(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new long integer vector whose elements signal whether the elements in one long integer vector are less or equal to their corresponding elements in a second long integer vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting long integer vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThanOrEqual(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one double-precision floating-point vector are less than or equal to their corresponding elements in a second double-precision floating-point vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    def LessThanOrEqualAll(left: System.Numerics.Vector[System_Numerics_Vector_LessThanOrEqualAll_T], right: System.Numerics.Vector[System_Numerics_Vector_LessThanOrEqualAll_T]) -> bool:
        """
        Returns a value that indicates whether all elements in the first vector are less than or equal to their corresponding elements in the second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: true if all of the elements in  are less than or equal to the corresponding elements in ; otherwise,  false.
        """
        ...

    @staticmethod
    def LessThanOrEqualAny(left: System.Numerics.Vector[System_Numerics_Vector_LessThanOrEqualAny_T], right: System.Numerics.Vector[System_Numerics_Vector_LessThanOrEqualAny_T]) -> bool:
        """
        Returns a value that indicates whether any element in the first vector is less than or equal to the corresponding element in the second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: true if any element in  is less than or equal to the corresponding element in ; otherwise,  false.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThan(left: System.Numerics.Vector[System_Numerics_Vector_GreaterThan_T], right: System.Numerics.Vector[System_Numerics_Vector_GreaterThan_T]) -> System.Numerics.Vector[System_Numerics_Vector_GreaterThan_T]:
        """
        Returns a new vector whose elements signal whether the elements in one vector of a specified type are greater than their corresponding elements in the second vector of the same time.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThan(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one single-precision floating-point vector are greater than their corresponding elements in a second single-precision floating-point vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThan(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one integral vector are greater than their corresponding elements in a second integral vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThan(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one double-precision floating-point vector are greater than their corresponding elements in a second double-precision floating-point vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThan(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new long integer vector whose elements signal whether the elements in one long integer vector are greater than their corresponding elements in a second long integer vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting long integer vector.
        """
        ...

    @staticmethod
    def GreaterThanAll(left: System.Numerics.Vector[System_Numerics_Vector_GreaterThanAll_T], right: System.Numerics.Vector[System_Numerics_Vector_GreaterThanAll_T]) -> bool:
        """
        Returns a value that indicates whether all elements in the first vector are greater than the corresponding elements in the second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: true if all elements in  are greater than the corresponding elements in ; otherwise, false.
        """
        ...

    @staticmethod
    def GreaterThanAny(left: System.Numerics.Vector[System_Numerics_Vector_GreaterThanAny_T], right: System.Numerics.Vector[System_Numerics_Vector_GreaterThanAny_T]) -> bool:
        """
        Returns a value that indicates whether any element in the first vector is greater than the corresponding element in the second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: true if any element in  is greater than the corresponding element in ; otherwise,  false.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThanOrEqual(left: System.Numerics.Vector[System_Numerics_Vector_GreaterThanOrEqual_T], right: System.Numerics.Vector[System_Numerics_Vector_GreaterThanOrEqual_T]) -> System.Numerics.Vector[System_Numerics_Vector_GreaterThanOrEqual_T]:
        """
        Returns a new vector whose elements signal whether the elements in one vector of a specified type are greater than or equal to their corresponding elements in the second vector of the same type.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThanOrEqual(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one vector are greater than or equal to their corresponding elements in the single-precision floating-point second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThanOrEqual(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one integral vector are greater than or equal to their corresponding elements in the second integral vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThanOrEqual(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new long integer vector whose elements signal whether the elements in one long integer vector are greater than or equal to their corresponding elements in the second long integer vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting long integer vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThanOrEqual(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns a new integral vector whose elements signal whether the elements in one vector are greater than or equal to their corresponding elements in the second double-precision floating-point vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resulting integral vector.
        """
        ...

    @staticmethod
    def GreaterThanOrEqualAll(left: System.Numerics.Vector[System_Numerics_Vector_GreaterThanOrEqualAll_T], right: System.Numerics.Vector[System_Numerics_Vector_GreaterThanOrEqualAll_T]) -> bool:
        """
        Returns a value that indicates whether all elements in the first vector are greater than or equal to all the corresponding elements in the second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: true if all elements in  are greater than or equal to the corresponding elements in ; otherwise, false.
        """
        ...

    @staticmethod
    def GreaterThanOrEqualAny(left: System.Numerics.Vector[System_Numerics_Vector_GreaterThanOrEqualAny_T], right: System.Numerics.Vector[System_Numerics_Vector_GreaterThanOrEqualAny_T]) -> bool:
        """
        Returns a value that indicates whether any element in the first vector is greater than or equal to the corresponding element in the second vector.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: true if any element in  is greater than or equal to the corresponding element in ; otherwise,  false.
        """
        ...

    @staticmethod
    def Abs(value: System.Numerics.Vector[System_Numerics_Vector_Abs_T]) -> System.Numerics.Vector[System_Numerics_Vector_Abs_T]:
        """
        Returns a new vector whose elements are the absolute values of the given vector's elements.
        
        :param value: The source vector.
        :returns: The absolute value vector.
        """
        ...

    @staticmethod
    def Min(left: System.Numerics.Vector[System_Numerics_Vector_Min_T], right: System.Numerics.Vector[System_Numerics_Vector_Min_T]) -> System.Numerics.Vector[System_Numerics_Vector_Min_T]:
        """
        Returns a new vector whose elements are the minimum of each pair of elements in the two given vectors.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The minimum vector.
        """
        ...

    @staticmethod
    def Max(left: System.Numerics.Vector[System_Numerics_Vector_Max_T], right: System.Numerics.Vector[System_Numerics_Vector_Max_T]) -> System.Numerics.Vector[System_Numerics_Vector_Max_T]:
        """
        Returns a new vector whose elements are the maximum of each pair of elements in the two given vectors.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The maximum vector.
        """
        ...

    @staticmethod
    def Dot(left: System.Numerics.Vector[System_Numerics_Vector_Dot_T], right: System.Numerics.Vector[System_Numerics_Vector_Dot_T]) -> System_Numerics_Vector_Dot_T:
        """
        Returns the dot product of two vectors.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def SquareRoot(value: System.Numerics.Vector[System_Numerics_Vector_SquareRoot_T]) -> System.Numerics.Vector[System_Numerics_Vector_SquareRoot_T]:
        """
        Returns a new vector whose elements are the square roots of a specified vector's elements.
        
        :param value: The source vector.
        :returns: The square root vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Ceiling(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Returns a new vector whose elements are the smallest integral values that are greater than or equal to the given vector's elements.
        
        :param value: The source vector.
        :returns: The vector whose elements are the smallest integral values that are greater than or equal to the given vector's elements. If a value is equal to float.NaN, float.NegativeInfinity, or float.PositiveInfinity, that value is returned.
        """
        ...

    @staticmethod
    @typing.overload
    def Ceiling(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Returns a new vector whose elements are the smallest integral values that are greater than or equal to the given vector's elements.
        
        :param value: The source vector.
        :returns: The vector whose elements are the smallest integral values that are greater than or equal to the given vector's elements. If a value is equal to double.NaN, double.NegativeInfinity, or double.PositiveInfinity, that value is returned.
        """
        ...

    @staticmethod
    @typing.overload
    def Floor(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Returns a new vector whose elements are the largest integral values that are less than or equal to the given vector's elements.
        
        :param value: The source vector.
        :returns: The vector whose elements are the largest integral values that are less than or equal to the given vector's elements. If a value is equal to float.NaN, float.NegativeInfinity, or float.PositiveInfinity, that value is returned.
        """
        ...

    @staticmethod
    @typing.overload
    def Floor(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Returns a new vector whose elements are the largest integral values that are less than or equal to the given vector's elements.
        
        :param value: The source vector.
        :returns: The vector whose elements are the largest integral values that are less than or equal to the given vector's elements. If a value is equal to double.NaN, double.NegativeInfinity, or double.PositiveInfinity, that value is returned.
        """
        ...

    @staticmethod
    def Add(left: System.Numerics.Vector[System_Numerics_Vector_Add_T], right: System.Numerics.Vector[System_Numerics_Vector_Add_T]) -> System.Numerics.Vector[System_Numerics_Vector_Add_T]:
        """
        Returns a new vector whose values are the sum of each pair of elements from two given vectors.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The summed vector.
        """
        ...

    @staticmethod
    def Subtract(left: System.Numerics.Vector[System_Numerics_Vector_Subtract_T], right: System.Numerics.Vector[System_Numerics_Vector_Subtract_T]) -> System.Numerics.Vector[System_Numerics_Vector_Subtract_T]:
        """
        Returns a new vector whose values are the difference between the elements in the second vector and their corresponding elements in the first vector.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The difference vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector[System_Numerics_Vector_Multiply_T], right: System.Numerics.Vector[System_Numerics_Vector_Multiply_T]) -> System.Numerics.Vector[System_Numerics_Vector_Multiply_T]:
        """
        Returns a new vector whose values are the product of each pair of elements in two specified vectors.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The element-wise product vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector[System_Numerics_Vector_Multiply_T], right: System_Numerics_Vector_Multiply_T) -> System.Numerics.Vector[System_Numerics_Vector_Multiply_T]:
        """
        Returns a new vector whose values are the values of a specified vector each multiplied by a scalar value.
        
        :param left: The vector.
        :param right: The scalar value.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System_Numerics_Vector_Multiply_T, right: System.Numerics.Vector[System_Numerics_Vector_Multiply_T]) -> System.Numerics.Vector[System_Numerics_Vector_Multiply_T]:
        """
        Returns a new vector whose values are a scalar value multiplied by each of the values of a specified vector.
        
        :param left: The scalar value.
        :param right: The vector.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    def Divide(left: System.Numerics.Vector[System_Numerics_Vector_Divide_T], right: System.Numerics.Vector[System_Numerics_Vector_Divide_T]) -> System.Numerics.Vector[System_Numerics_Vector_Divide_T]:
        """
        Returns a new vector whose values are the result of dividing the first vector's elements by the corresponding elements in the second vector.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The divided vector.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Vector[System_Numerics_Vector_Negate_T]) -> System.Numerics.Vector[System_Numerics_Vector_Negate_T]:
        """
        Returns a new vector whose elements are the negation of the corresponding element in the specified vector.
        
        :param value: The source vector.
        :returns: The negated vector.
        """
        ...

    @staticmethod
    def BitwiseAnd(left: System.Numerics.Vector[System_Numerics_Vector_BitwiseAnd_T], right: System.Numerics.Vector[System_Numerics_Vector_BitwiseAnd_T]) -> System.Numerics.Vector[System_Numerics_Vector_BitwiseAnd_T]:
        """
        Returns a new vector by performing a bitwise And operation on each pair of elements in two vectors.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The resulting vector.
        """
        ...

    @staticmethod
    def BitwiseOr(left: System.Numerics.Vector[System_Numerics_Vector_BitwiseOr_T], right: System.Numerics.Vector[System_Numerics_Vector_BitwiseOr_T]) -> System.Numerics.Vector[System_Numerics_Vector_BitwiseOr_T]:
        """
        Returns a new vector by performing a bitwise Or operation on each pair of elements in two vectors.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The resulting vector.
        """
        ...

    @staticmethod
    def OnesComplement(value: System.Numerics.Vector[System_Numerics_Vector_OnesComplement_T]) -> System.Numerics.Vector[System_Numerics_Vector_OnesComplement_T]:
        """
        Returns a new vector whose elements are obtained by taking the one's complement of a specified vector's elements.
        
        :param value: The source vector.
        :returns: The resulting vector.
        """
        ...

    @staticmethod
    def Xor(left: System.Numerics.Vector[System_Numerics_Vector_Xor_T], right: System.Numerics.Vector[System_Numerics_Vector_Xor_T]) -> System.Numerics.Vector[System_Numerics_Vector_Xor_T]:
        """
        Returns a new vector by performing a bitwise exclusive Or (XOr) operation on each pair of elements in two vectors.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The resulting vector.
        """
        ...

    @staticmethod
    def AndNot(left: System.Numerics.Vector[System_Numerics_Vector_AndNot_T], right: System.Numerics.Vector[System_Numerics_Vector_AndNot_T]) -> System.Numerics.Vector[System_Numerics_Vector_AndNot_T]:
        """
        Returns a new vector by performing a bitwise And Not operation on each pair of corresponding elements in two vectors.
        
        :param left: The first vector.
        :param right: The second vector.
        :returns: The resulting vector.
        """
        ...

    @staticmethod
    def AsVectorByte(value: System.Numerics.Vector[System_Numerics_Vector_AsVectorByte_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of a specified vector into those of a vector of unsigned bytes.
        
        :param value: The source vector.
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorSByte(value: System.Numerics.Vector[System_Numerics_Vector_AsVectorSByte_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of a specified vector into those of a vector of signed bytes.
        
        :param value: The source vector.
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorUInt16(value: System.Numerics.Vector[System_Numerics_Vector_AsVectorUInt16_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of a specified vector into those of a vector of unsigned 16-bit integers.
        
        :param value: The source vector.
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorInt16(value: System.Numerics.Vector[System_Numerics_Vector_AsVectorInt16_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of a specified vector into those of a vector of 16-bit integers.
        
        :param value: The source vector.
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorUInt32(value: System.Numerics.Vector[System_Numerics_Vector_AsVectorUInt32_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of a specified vector into those of a vector of unsigned integers.
        
        :param value: The source vector.
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorInt32(value: System.Numerics.Vector[System_Numerics_Vector_AsVectorInt32_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of a specified vector into those of a vector of integers.
        
        :param value: The source vector.
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorUInt64(value: System.Numerics.Vector[System_Numerics_Vector_AsVectorUInt64_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of a specified vector into those of a vector of unsigned long integers.
        
        :param value: The source vector.
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorInt64(value: System.Numerics.Vector[System_Numerics_Vector_AsVectorInt64_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of a specified vector into those of a vector of long integers.
        
        :param value: The source vector.
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorSingle(value: System.Numerics.Vector[System_Numerics_Vector_AsVectorSingle_T]) -> System.Numerics.Vector[float]:
        """
        Reinterprets the bits of a specified vector into those of a single-precision floating-point vector.
        
        :param value: The source vector.
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorDouble(value: System.Numerics.Vector[System_Numerics_Vector_AsVectorDouble_T]) -> System.Numerics.Vector[float]:
        """
        Reinterprets the bits of a specified vector into those of a double-precision floating-point vector.
        
        :param value: The source vector.
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector<Byte> into two Vector<UInt16> instances.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector<UInt16> into two Vector<UInt32> instances.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector<UInt32> into two Vector<UInt64> instances.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector<SByte> into two Vector<Int16> instances.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector<Int16> into two Vector<Int32> instances.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector<Int32> into two Vector<Int64> instances.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[float], low: System.Numerics.Vector[float], high: System.Numerics.Vector[float]) -> None:
        """
        Widens a Vector<Single> into two Vector<Double> instances.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector<UInt16> instances into one Vector<Byte>.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        :returns: A Vector<Byte> containing elements narrowed from the source vectors.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector<UInt32> instances into one Vector<UInt16>.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        :returns: A Vector<UInt16> containing elements narrowed from the source vectors.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector<UInt64> instances into one Vector<UInt32>.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        :returns: A Vector<UInt32> containing elements narrowed from the source vectors.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector<Int16> instances into one Vector<SByte>.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        :returns: A Vector<SByte> containing elements narrowed from the source vectors.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector<Int32> instances into one Vector<Int16>.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        :returns: A Vector<Int16> containing elements narrowed from the source vectors.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector<Int64> instances into one Vector<Int32>.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        :returns: A Vector<Int32> containing elements narrowed from the source vectors.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[float], high: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Narrows two Vector<Double> instances into one Vector<Single>.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        :returns: A Vector<Single> containing elements narrowed from the source vectors.
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertToSingle(value: System.Numerics.Vector[int]) -> System.Numerics.Vector[float]:
        """
        Converts a Vector<Int32> to a Vector<Single>.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertToSingle(value: System.Numerics.Vector[int]) -> System.Numerics.Vector[float]:
        """
        Converts a Vector<UInt32> to a Vector<Single>.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertToDouble(value: System.Numerics.Vector[int]) -> System.Numerics.Vector[float]:
        """
        Converts a Vector<Int64> to a Vector<Double>.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertToDouble(value: System.Numerics.Vector[int]) -> System.Numerics.Vector[float]:
        """
        Converts a Vector<UInt64> to a Vector<Double>.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    def ConvertToInt32(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Converts a Vector<Single> to a Vector<Int32>.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    def ConvertToUInt32(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Converts a Vector<Single> to a Vector<UInt32>.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    def ConvertToInt64(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Converts a Vector<Double> to a Vector<Int64>.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    def ConvertToUInt64(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Converts a Vector<Double> to a Vector<UInt64>.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    def As(vector: System.Numerics.Vector[System_Numerics_Vector_As_TFrom]) -> System.Numerics.Vector[System_Numerics_Vector_As_TTo]:
        """
        Reinterprets a Vector{T} as a Vector{T} of new type.
        
        :param vector: The vector to reinterpret.
        :returns: reinterpreted as a new Vector{T}.
        """
        ...

    @typing.overload
    def __init__(self, value: System_Numerics_Vector_T) -> None:
        """Constructs a vector whose components are all ."""
        ...

    @typing.overload
    def __init__(self, values: typing.List[System_Numerics_Vector_T]) -> None:
        """Constructs a vector from the given array. The size of the given array must be at least Count."""
        ...

    @typing.overload
    def __init__(self, values: typing.List[System_Numerics_Vector_T], index: int) -> None:
        """
        Constructs a vector from the given array, starting from the given index.
        The array must contain at least Count from the given index.
        """
        ...

    @typing.overload
    def __init__(self, values: System.ReadOnlySpan[int]) -> None:
        """
        Constructs a vector from the given ReadOnlySpan{Byte}.
        The span must contain at least Vector{Byte}.Count elements.
        """
        ...

    @typing.overload
    def __init__(self, values: System.ReadOnlySpan[System_Numerics_Vector_T]) -> None:
        """
        Constructs a vector from the given ReadOnlySpan{T}.
        The span must contain at least Count elements.
        """
        ...

    @typing.overload
    def __init__(self, values: System.Span[System_Numerics_Vector_T]) -> None:
        """
        Constructs a vector from the given Span{T}.
        The span must contain at least Count elements.
        """
        ...

    @typing.overload
    def CopyTo(self, destination: System.Span[int]) -> None:
        """
        Copies the vector to the given Span{Byte}.
        The destination span must be at least size Vector{Byte}.Count.
        
        :param destination: The destination span which the values are copied into
        """
        ...

    @typing.overload
    def CopyTo(self, destination: System.Span[System_Numerics_Vector_T]) -> None:
        """
        Copies the vector to the given Span{T}.
        The destination span must be at least size Count.
        
        :param destination: The destination span which the values are copied into
        """
        ...

    @typing.overload
    def CopyTo(self, destination: typing.List[System_Numerics_Vector_T]) -> None:
        """
        Copies the vector to the given destination array.
        The destination array must be at least size Count.
        
        :param destination: The destination array which the values are copied into
        """
        ...

    @typing.overload
    def CopyTo(self, destination: typing.List[System_Numerics_Vector_T], startIndex: int) -> None:
        """
        Copies the vector to the given destination array.
        The destination array must be at least size Count.
        
        :param destination: The destination array which the values are copied into
        :param startIndex: The index to start copying to
        """
        ...

    def __getitem__(self, index: int) -> System_Numerics_Vector_T:
        """Returns the element at the given index."""
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Returns a boolean indicating whether the given Object is equal to this vector instance.
        
        :param obj: The Object to compare against.
        :returns: True if the Object is equal to this vector; False otherwise.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether the given vector is equal to this vector instance.
        
        :param other: The vector to compare this instance to.
        :returns: True if the other vector is equal to this instance; False otherwise.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    @typing.overload
    def ToString(self) -> str:
        """
        Returns a String representing this vector.
        
        :returns: The string representation.
        """
        ...

    @typing.overload
    def ToString(self, format: str) -> str:
        """
        Returns a String representing this vector, using the specified format string to format individual elements.
        
        :param format: The format of individual elements.
        :returns: The string representation.
        """
        ...

    @typing.overload
    def ToString(self, format: str, formatProvider: System.IFormatProvider) -> str:
        """
        Returns a String representing this vector, using the specified format string to format individual elements and the given IFormatProvider.
        
        :param format: The format of individual elements.
        :param formatProvider: The format provider to use when formatting elements.
        :returns: The string representation.
        """
        ...

    @typing.overload
    def TryCopyTo(self, destination: System.Span[int]) -> bool:
        """
        Attempts to copy the vector to the given Span{Byte}.
        The destination span must be at least size Vector{Byte}.Count.
        
        :param destination: The destination span which the values are copied into
        :returns: True if the source vector was successfully copied to . False if  is not large enough to hold the source vector.
        """
        ...

    @typing.overload
    def TryCopyTo(self, destination: System.Span[System_Numerics_Vector_T]) -> bool:
        """
        Attempts to copy the vector to the given Span{T}.
        The destination span must be at least size Count.
        
        :param destination: The destination span which the values are copied into
        :returns: True if the source vector was successfully copied to . False if  is not large enough to hold the source vector.
        """
        ...


