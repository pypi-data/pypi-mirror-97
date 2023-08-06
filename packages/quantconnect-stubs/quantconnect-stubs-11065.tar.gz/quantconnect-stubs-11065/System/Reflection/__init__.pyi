import abc
import typing

import System
import System.Collections.Generic
import System.Globalization
import System.IO
import System.Reflection
import System.Runtime.Serialization

System_Reflection_TypeFilter = typing.Any
System_Reflection_ModuleResolveEventHandler = typing.Any

System_Reflection_MethodInfo_CreateDelegate_T = typing.TypeVar("System_Reflection_MethodInfo_CreateDelegate_T")
System_Reflection_CustomAttributeExtensions_GetCustomAttribute_T = typing.TypeVar("System_Reflection_CustomAttributeExtensions_GetCustomAttribute_T")
System_Reflection_CustomAttributeExtensions_GetCustomAttributes_T = typing.TypeVar("System_Reflection_CustomAttributeExtensions_GetCustomAttributes_T")


class AssemblySignatureKeyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def PublicKey(self) -> str:
        ...

    @property
    def Countersignature(self) -> str:
        ...

    def __init__(self, publicKey: str, countersignature: str) -> None:
        ...


class ICustomAttributeProvider(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @typing.overload
    def GetCustomAttributes(self, inherit: bool) -> typing.List[System.Object]:
        ...

    @typing.overload
    def GetCustomAttributes(self, attributeType: typing.Type, inherit: bool) -> typing.List[System.Object]:
        ...

    def IsDefined(self, attributeType: typing.Type, inherit: bool) -> bool:
        ...


class MemberInfo(System.Object, System.Reflection.ICustomAttributeProvider, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def MemberType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.MemberTypes enum."""
        ...

    @property
    @abc.abstractmethod
    def Name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def DeclaringType(self) -> typing.Type:
        ...

    @property
    @abc.abstractmethod
    def ReflectedType(self) -> typing.Type:
        ...

    @property
    def Module(self) -> System.Reflection.Module:
        ...

    @property
    def CustomAttributes(self) -> System.Collections.Generic.IEnumerable[System.Reflection.CustomAttributeData]:
        ...

    @property
    def IsCollectible(self) -> bool:
        ...

    @property
    def MetadataToken(self) -> int:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def HasSameMetadataDefinitionAs(self, other: System.Reflection.MemberInfo) -> bool:
        ...

    def IsDefined(self, attributeType: typing.Type, inherit: bool) -> bool:
        ...

    @typing.overload
    def GetCustomAttributes(self, inherit: bool) -> typing.List[System.Object]:
        ...

    @typing.overload
    def GetCustomAttributes(self, attributeType: typing.Type, inherit: bool) -> typing.List[System.Object]:
        ...

    def GetCustomAttributesData(self) -> System.Collections.Generic.IList[System.Reflection.CustomAttributeData]:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class LocalVariableInfo(System.Object):
    """This class has no documentation."""

    @property
    def LocalType(self) -> typing.Type:
        ...

    @property
    def LocalIndex(self) -> int:
        ...

    @property
    def IsPinned(self) -> bool:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def ToString(self) -> str:
        ...


class ExceptionHandlingClause(System.Object):
    """This class has no documentation."""

    @property
    def Flags(self) -> int:
        """This property contains the int value of a member of the System.Reflection.ExceptionHandlingClauseOptions enum."""
        ...

    @property
    def TryOffset(self) -> int:
        ...

    @property
    def TryLength(self) -> int:
        ...

    @property
    def HandlerOffset(self) -> int:
        ...

    @property
    def HandlerLength(self) -> int:
        ...

    @property
    def FilterOffset(self) -> int:
        ...

    @property
    def CatchType(self) -> typing.Type:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def ToString(self) -> str:
        ...


class MethodBody(System.Object):
    """This class has no documentation."""

    @property
    def LocalSignatureMetadataToken(self) -> int:
        ...

    @property
    def LocalVariables(self) -> System.Collections.Generic.IList[System.Reflection.LocalVariableInfo]:
        ...

    @property
    def MaxStackSize(self) -> int:
        ...

    @property
    def InitLocals(self) -> bool:
        ...

    @property
    def ExceptionHandlingClauses(self) -> System.Collections.Generic.IList[System.Reflection.ExceptionHandlingClause]:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def GetILAsByteArray(self) -> typing.List[int]:
        ...


class BindingFlags(System.Enum):
    """This class has no documentation."""

    Default = ...

    IgnoreCase = ...

    DeclaredOnly = ...

    Instance = ...

    Static = ...

    Public = ...

    NonPublic = ...

    FlattenHierarchy = ...

    InvokeMethod = ...

    CreateInstance = ...

    GetField = ...

    SetField = ...

    GetProperty = ...

    SetProperty = ...

    PutDispProperty = ...

    PutRefDispProperty = ...

    ExactBinding = ...

    SuppressChangeType = ...

    OptionalParamBinding = ...

    IgnoreReturn = ...

    DoNotWrapExceptions = ...


class ParameterAttributes(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = ...

    In = ...

    Out = ...

    Lcid = ...

    Retval = ...

    Optional = ...

    HasDefault = ...

    HasFieldMarshal = ...

    Reserved3 = ...

    Reserved4 = ...

    ReservedMask = ...


class ParameterInfo(System.Object, System.Reflection.ICustomAttributeProvider, System.Runtime.Serialization.IObjectReference):
    """This class has no documentation."""

    @property
    def Attributes(self) -> int:
        """This property contains the int value of a member of the System.Reflection.ParameterAttributes enum."""
        ...

    @property
    def Member(self) -> System.Reflection.MemberInfo:
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def ParameterType(self) -> typing.Type:
        ...

    @property
    def Position(self) -> int:
        ...

    @property
    def IsIn(self) -> bool:
        ...

    @property
    def IsLcid(self) -> bool:
        ...

    @property
    def IsOptional(self) -> bool:
        ...

    @property
    def IsOut(self) -> bool:
        ...

    @property
    def IsRetval(self) -> bool:
        ...

    @property
    def DefaultValue(self) -> System.Object:
        ...

    @property
    def RawDefaultValue(self) -> System.Object:
        ...

    @property
    def HasDefaultValue(self) -> bool:
        ...

    @property
    def CustomAttributes(self) -> System.Collections.Generic.IEnumerable[System.Reflection.CustomAttributeData]:
        ...

    @property
    def MetadataToken(self) -> int:
        ...

    @property
    def AttrsImpl(self) -> System.Reflection.ParameterAttributes:
        """This field is protected."""
        ...

    @AttrsImpl.setter
    def AttrsImpl(self, value: System.Reflection.ParameterAttributes):
        """This field is protected."""
        ...

    @property
    def ClassImpl(self) -> typing.Type:
        """This field is protected."""
        ...

    @ClassImpl.setter
    def ClassImpl(self, value: typing.Type):
        """This field is protected."""
        ...

    @property
    def DefaultValueImpl(self) -> System.Object:
        """This field is protected."""
        ...

    @DefaultValueImpl.setter
    def DefaultValueImpl(self, value: System.Object):
        """This field is protected."""
        ...

    @property
    def MemberImpl(self) -> System.Reflection.MemberInfo:
        """This field is protected."""
        ...

    @MemberImpl.setter
    def MemberImpl(self, value: System.Reflection.MemberInfo):
        """This field is protected."""
        ...

    @property
    def NameImpl(self) -> str:
        """This field is protected."""
        ...

    @NameImpl.setter
    def NameImpl(self, value: str):
        """This field is protected."""
        ...

    @property
    def PositionImpl(self) -> int:
        """This field is protected."""
        ...

    @PositionImpl.setter
    def PositionImpl(self, value: int):
        """This field is protected."""
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def IsDefined(self, attributeType: typing.Type, inherit: bool) -> bool:
        ...

    def GetCustomAttributesData(self) -> System.Collections.Generic.IList[System.Reflection.CustomAttributeData]:
        ...

    @typing.overload
    def GetCustomAttributes(self, inherit: bool) -> typing.List[System.Object]:
        ...

    @typing.overload
    def GetCustomAttributes(self, attributeType: typing.Type, inherit: bool) -> typing.List[System.Object]:
        ...

    def GetOptionalCustomModifiers(self) -> typing.List[typing.Type]:
        ...

    def GetRequiredCustomModifiers(self) -> typing.List[typing.Type]:
        ...

    def GetRealObject(self, context: System.Runtime.Serialization.StreamingContext) -> System.Object:
        ...

    def ToString(self) -> str:
        ...


class MethodBase(System.Reflection.MemberInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Attributes(self) -> int:
        """This property contains the int value of a member of the System.Reflection.MethodAttributes enum."""
        ...

    @property
    def MethodImplementationFlags(self) -> int:
        """This property contains the int value of a member of the System.Reflection.MethodImplAttributes enum."""
        ...

    @property
    def CallingConvention(self) -> int:
        """This property contains the int value of a member of the System.Reflection.CallingConventions enum."""
        ...

    @property
    def IsAbstract(self) -> bool:
        ...

    @property
    def IsConstructor(self) -> bool:
        ...

    @property
    def IsFinal(self) -> bool:
        ...

    @property
    def IsHideBySig(self) -> bool:
        ...

    @property
    def IsSpecialName(self) -> bool:
        ...

    @property
    def IsStatic(self) -> bool:
        ...

    @property
    def IsVirtual(self) -> bool:
        ...

    @property
    def IsAssembly(self) -> bool:
        ...

    @property
    def IsFamily(self) -> bool:
        ...

    @property
    def IsFamilyAndAssembly(self) -> bool:
        ...

    @property
    def IsFamilyOrAssembly(self) -> bool:
        ...

    @property
    def IsPrivate(self) -> bool:
        ...

    @property
    def IsPublic(self) -> bool:
        ...

    @property
    def IsConstructedGenericMethod(self) -> bool:
        ...

    @property
    def IsGenericMethod(self) -> bool:
        ...

    @property
    def IsGenericMethodDefinition(self) -> bool:
        ...

    @property
    def ContainsGenericParameters(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def MethodHandle(self) -> System.RuntimeMethodHandle:
        ...

    @property
    def IsSecurityCritical(self) -> bool:
        ...

    @property
    def IsSecuritySafeCritical(self) -> bool:
        ...

    @property
    def IsSecurityTransparent(self) -> bool:
        ...

    MethodNameBufferSize: int = 100

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def GetParameters(self) -> typing.List[System.Reflection.ParameterInfo]:
        ...

    def GetMethodImplementationFlags(self) -> int:
        """:returns: This method returns the int value of a member of the System.Reflection.MethodImplAttributes enum."""
        ...

    def GetMethodBody(self) -> System.Reflection.MethodBody:
        ...

    def GetGenericArguments(self) -> typing.List[typing.Type]:
        ...

    @typing.overload
    def Invoke(self, obj: typing.Any, parameters: typing.List[System.Object]) -> System.Object:
        ...

    @typing.overload
    def Invoke(self, obj: typing.Any, invokeAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, parameters: typing.List[System.Object], culture: System.Globalization.CultureInfo) -> System.Object:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    @staticmethod
    @typing.overload
    def GetMethodFromHandle(handle: System.RuntimeMethodHandle) -> System.Reflection.MethodBase:
        ...

    @staticmethod
    @typing.overload
    def GetMethodFromHandle(handle: System.RuntimeMethodHandle, declaringType: System.RuntimeTypeHandle) -> System.Reflection.MethodBase:
        ...

    @staticmethod
    def GetCurrentMethod() -> System.Reflection.MethodBase:
        ...


class MethodInfo(System.Reflection.MethodBase, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def GenericParameterCount(self) -> int:
        ...

    @property
    def MemberType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.MemberTypes enum."""
        ...

    @property
    def ReturnParameter(self) -> System.Reflection.ParameterInfo:
        ...

    @property
    def ReturnType(self) -> typing.Type:
        ...

    @property
    @abc.abstractmethod
    def ReturnTypeCustomAttributes(self) -> System.Reflection.ICustomAttributeProvider:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def GetGenericArguments(self) -> typing.List[typing.Type]:
        ...

    def GetGenericMethodDefinition(self) -> System.Reflection.MethodInfo:
        ...

    def MakeGenericMethod(self, *typeArguments: typing.Type) -> System.Reflection.MethodInfo:
        ...

    def GetBaseDefinition(self) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def CreateDelegate(self, delegateType: typing.Type) -> System.Delegate:
        ...

    @typing.overload
    def CreateDelegate(self, delegateType: typing.Type, target: typing.Any) -> System.Delegate:
        ...

    @typing.overload
    def CreateDelegate(self) -> System_Reflection_MethodInfo_CreateDelegate_T:
        """Creates a delegate of the given type 'T' from this method."""
        ...

    @typing.overload
    def CreateDelegate(self, target: typing.Any) -> System_Reflection_MethodInfo_CreateDelegate_T:
        """Creates a delegate of the given type 'T' with the specified target from this method."""
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class StrongNameKeyPair(System.Object, System.Runtime.Serialization.IDeserializationCallback, System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    @property
    def PublicKey(self) -> typing.List[int]:
        ...

    @typing.overload
    def __init__(self, keyPairFile: System.IO.FileStream) -> None:
        ...

    @typing.overload
    def __init__(self, keyPairArray: typing.List[int]) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, keyPairContainer: str) -> None:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def OnDeserialization(self, sender: typing.Any) -> None:
        ...


class AssemblyName(System.Object, System.ICloneable, System.Runtime.Serialization.IDeserializationCallback, System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def Version(self) -> System.Version:
        ...

    @Version.setter
    def Version(self, value: System.Version):
        ...

    @property
    def CultureInfo(self) -> System.Globalization.CultureInfo:
        ...

    @CultureInfo.setter
    def CultureInfo(self, value: System.Globalization.CultureInfo):
        ...

    @property
    def CultureName(self) -> str:
        ...

    @CultureName.setter
    def CultureName(self, value: str):
        ...

    @property
    def CodeBase(self) -> str:
        ...

    @CodeBase.setter
    def CodeBase(self, value: str):
        ...

    @property
    def EscapedCodeBase(self) -> str:
        ...

    @property
    def ProcessorArchitecture(self) -> int:
        """This property contains the int value of a member of the System.Reflection.ProcessorArchitecture enum."""
        ...

    @ProcessorArchitecture.setter
    def ProcessorArchitecture(self, value: int):
        """This property contains the int value of a member of the System.Reflection.ProcessorArchitecture enum."""
        ...

    @property
    def ContentType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.AssemblyContentType enum."""
        ...

    @ContentType.setter
    def ContentType(self, value: int):
        """This property contains the int value of a member of the System.Reflection.AssemblyContentType enum."""
        ...

    @property
    def Flags(self) -> int:
        """This property contains the int value of a member of the System.Reflection.AssemblyNameFlags enum."""
        ...

    @Flags.setter
    def Flags(self, value: int):
        """This property contains the int value of a member of the System.Reflection.AssemblyNameFlags enum."""
        ...

    @property
    def HashAlgorithm(self) -> System.Reflection.AssemblyHashAlgorithm:
        ...

    @HashAlgorithm.setter
    def HashAlgorithm(self, value: System.Reflection.AssemblyHashAlgorithm):
        ...

    @property
    def VersionCompatibility(self) -> int:
        """This property contains the int value of a member of the System.Configuration.Assemblies.AssemblyVersionCompatibility enum."""
        ...

    @VersionCompatibility.setter
    def VersionCompatibility(self, value: int):
        """This property contains the int value of a member of the System.Configuration.Assemblies.AssemblyVersionCompatibility enum."""
        ...

    @property
    def KeyPair(self) -> System.Reflection.StrongNameKeyPair:
        ...

    @KeyPair.setter
    def KeyPair(self, value: System.Reflection.StrongNameKeyPair):
        ...

    @property
    def FullName(self) -> str:
        ...

    c_DummyChar: str = ...

    @typing.overload
    def __init__(self) -> None:
        ...

    def Clone(self) -> System.Object:
        ...

    @staticmethod
    def GetAssemblyName(assemblyFile: str) -> System.Reflection.AssemblyName:
        ...

    def GetPublicKey(self) -> typing.List[int]:
        ...

    def SetPublicKey(self, publicKey: typing.List[int]) -> None:
        ...

    def GetPublicKeyToken(self) -> typing.List[int]:
        ...

    def SetPublicKeyToken(self, publicKeyToken: typing.List[int]) -> None:
        ...

    def ToString(self) -> str:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def OnDeserialization(self, sender: typing.Any) -> None:
        ...

    @staticmethod
    def ReferenceMatchesDefinition(reference: System.Reflection.AssemblyName, definition: System.Reflection.AssemblyName) -> bool:
        """
        Compares the simple names disregarding Version, Culture and PKT. While this clearly does not
        match the intent of this api, this api has been broken this way since its debut and we cannot
        change its behavior now.
        """
        ...

    @typing.overload
    def __init__(self, assemblyName: str) -> None:
        ...


class FieldInfo(System.Reflection.MemberInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def MemberType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.MemberTypes enum."""
        ...

    @property
    @abc.abstractmethod
    def Attributes(self) -> int:
        """This property contains the int value of a member of the System.Reflection.FieldAttributes enum."""
        ...

    @property
    @abc.abstractmethod
    def FieldType(self) -> typing.Type:
        ...

    @property
    def IsInitOnly(self) -> bool:
        ...

    @property
    def IsLiteral(self) -> bool:
        ...

    @property
    def IsNotSerialized(self) -> bool:
        ...

    @property
    def IsPinvokeImpl(self) -> bool:
        ...

    @property
    def IsSpecialName(self) -> bool:
        ...

    @property
    def IsStatic(self) -> bool:
        ...

    @property
    def IsAssembly(self) -> bool:
        ...

    @property
    def IsFamily(self) -> bool:
        ...

    @property
    def IsFamilyAndAssembly(self) -> bool:
        ...

    @property
    def IsFamilyOrAssembly(self) -> bool:
        ...

    @property
    def IsPrivate(self) -> bool:
        ...

    @property
    def IsPublic(self) -> bool:
        ...

    @property
    def IsSecurityCritical(self) -> bool:
        ...

    @property
    def IsSecuritySafeCritical(self) -> bool:
        ...

    @property
    def IsSecurityTransparent(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def FieldHandle(self) -> System.RuntimeFieldHandle:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def GetValue(self, obj: typing.Any) -> System.Object:
        ...

    @typing.overload
    def SetValue(self, obj: typing.Any, value: typing.Any) -> None:
        ...

    @typing.overload
    def SetValue(self, obj: typing.Any, value: typing.Any, invokeAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, culture: System.Globalization.CultureInfo) -> None:
        ...

    def SetValueDirect(self, obj: System.TypedReference, value: typing.Any) -> None:
        ...

    def GetValueDirect(self, obj: System.TypedReference) -> System.Object:
        ...

    def GetRawConstantValue(self) -> System.Object:
        ...

    def GetOptionalCustomModifiers(self) -> typing.List[typing.Type]:
        ...

    def GetRequiredCustomModifiers(self) -> typing.List[typing.Type]:
        ...

    @staticmethod
    @typing.overload
    def GetFieldFromHandle(handle: System.RuntimeFieldHandle) -> System.Reflection.FieldInfo:
        ...

    @staticmethod
    @typing.overload
    def GetFieldFromHandle(handle: System.RuntimeFieldHandle, declaringType: System.RuntimeTypeHandle) -> System.Reflection.FieldInfo:
        ...


class PropertyInfo(System.Reflection.MemberInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def MemberType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.MemberTypes enum."""
        ...

    @property
    @abc.abstractmethod
    def PropertyType(self) -> typing.Type:
        ...

    @property
    @abc.abstractmethod
    def Attributes(self) -> int:
        """This property contains the int value of a member of the System.Reflection.PropertyAttributes enum."""
        ...

    @property
    def IsSpecialName(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def CanRead(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def CanWrite(self) -> bool:
        ...

    @property
    def GetMethod(self) -> System.Reflection.MethodInfo:
        ...

    @property
    def SetMethod(self) -> System.Reflection.MethodInfo:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def GetIndexParameters(self) -> typing.List[System.Reflection.ParameterInfo]:
        ...

    @typing.overload
    def GetAccessors(self) -> typing.List[System.Reflection.MethodInfo]:
        ...

    @typing.overload
    def GetAccessors(self, nonPublic: bool) -> typing.List[System.Reflection.MethodInfo]:
        ...

    @typing.overload
    def GetGetMethod(self) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetGetMethod(self, nonPublic: bool) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetSetMethod(self) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetSetMethod(self, nonPublic: bool) -> System.Reflection.MethodInfo:
        ...

    def GetOptionalCustomModifiers(self) -> typing.List[typing.Type]:
        ...

    def GetRequiredCustomModifiers(self) -> typing.List[typing.Type]:
        ...

    @typing.overload
    def GetValue(self, obj: typing.Any) -> System.Object:
        ...

    @typing.overload
    def GetValue(self, obj: typing.Any, index: typing.List[System.Object]) -> System.Object:
        ...

    @typing.overload
    def GetValue(self, obj: typing.Any, invokeAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, index: typing.List[System.Object], culture: System.Globalization.CultureInfo) -> System.Object:
        ...

    def GetConstantValue(self) -> System.Object:
        ...

    def GetRawConstantValue(self) -> System.Object:
        ...

    @typing.overload
    def SetValue(self, obj: typing.Any, value: typing.Any) -> None:
        ...

    @typing.overload
    def SetValue(self, obj: typing.Any, value: typing.Any, index: typing.List[System.Object]) -> None:
        ...

    @typing.overload
    def SetValue(self, obj: typing.Any, value: typing.Any, invokeAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, index: typing.List[System.Object], culture: System.Globalization.CultureInfo) -> None:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class ParameterModifier:
    """This class has no documentation."""

    def __init__(self, parameterCount: int) -> None:
        ...

    def __getitem__(self, index: int) -> bool:
        ...

    def __setitem__(self, index: int, value: bool) -> None:
        ...


class Binder(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def BindToField(self, bindingAttr: System.Reflection.BindingFlags, match: typing.List[System.Reflection.FieldInfo], value: typing.Any, culture: System.Globalization.CultureInfo) -> System.Reflection.FieldInfo:
        ...

    def BindToMethod(self, bindingAttr: System.Reflection.BindingFlags, match: typing.List[System.Reflection.MethodBase], args: typing.List[System.Object], modifiers: typing.List[System.Reflection.ParameterModifier], culture: System.Globalization.CultureInfo, names: typing.List[str], state: typing.Any) -> System.Reflection.MethodBase:
        ...

    def ChangeType(self, value: typing.Any, type: typing.Type, culture: System.Globalization.CultureInfo) -> System.Object:
        ...

    def ReorderArgumentArray(self, args: typing.List[System.Object], state: typing.Any) -> None:
        ...

    def SelectMethod(self, bindingAttr: System.Reflection.BindingFlags, match: typing.List[System.Reflection.MethodBase], types: typing.List[typing.Type], modifiers: typing.List[System.Reflection.ParameterModifier]) -> System.Reflection.MethodBase:
        ...

    def SelectProperty(self, bindingAttr: System.Reflection.BindingFlags, match: typing.List[System.Reflection.PropertyInfo], returnType: typing.Type, indexes: typing.List[typing.Type], modifiers: typing.List[System.Reflection.ParameterModifier]) -> System.Reflection.PropertyInfo:
        ...


class IReflectableType(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetTypeInfo(self) -> System.Reflection.TypeInfo:
        ...


class EventInfo(System.Reflection.MemberInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def MemberType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.MemberTypes enum."""
        ...

    @property
    @abc.abstractmethod
    def Attributes(self) -> int:
        """This property contains the int value of a member of the System.Reflection.EventAttributes enum."""
        ...

    @property
    def IsSpecialName(self) -> bool:
        ...

    @property
    def AddMethod(self) -> System.Reflection.MethodInfo:
        ...

    @property
    def RemoveMethod(self) -> System.Reflection.MethodInfo:
        ...

    @property
    def RaiseMethod(self) -> System.Reflection.MethodInfo:
        ...

    @property
    def IsMulticast(self) -> bool:
        ...

    @property
    def EventHandlerType(self) -> typing.Type:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def GetOtherMethods(self) -> typing.List[System.Reflection.MethodInfo]:
        ...

    @typing.overload
    def GetOtherMethods(self, nonPublic: bool) -> typing.List[System.Reflection.MethodInfo]:
        ...

    @typing.overload
    def GetAddMethod(self) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetRemoveMethod(self) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetRaiseMethod(self) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetAddMethod(self, nonPublic: bool) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetRemoveMethod(self, nonPublic: bool) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetRaiseMethod(self, nonPublic: bool) -> System.Reflection.MethodInfo:
        ...

    def AddEventHandler(self, target: typing.Any, handler: System.Delegate) -> None:
        ...

    def RemoveEventHandler(self, target: typing.Any, handler: System.Delegate) -> None:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class ConstructorInfo(System.Reflection.MethodBase, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def MemberType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.MemberTypes enum."""
        ...

    ConstructorName: str = ".ctor"

    TypeConstructorName: str = ".cctor"

    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def Invoke(self, parameters: typing.List[System.Object]) -> System.Object:
        ...

    @typing.overload
    def Invoke(self, invokeAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, parameters: typing.List[System.Object], culture: System.Globalization.CultureInfo) -> System.Object:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class TypeInfo(typing.Type, System.Reflection.IReflectableType, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def GenericTypeParameters(self) -> typing.List[typing.Type]:
        ...

    @property
    def DeclaredConstructors(self) -> System.Collections.Generic.IEnumerable[System.Reflection.ConstructorInfo]:
        ...

    @property
    def DeclaredEvents(self) -> System.Collections.Generic.IEnumerable[System.Reflection.EventInfo]:
        ...

    @property
    def DeclaredFields(self) -> System.Collections.Generic.IEnumerable[System.Reflection.FieldInfo]:
        ...

    @property
    def DeclaredMembers(self) -> System.Collections.Generic.IEnumerable[System.Reflection.MemberInfo]:
        ...

    @property
    def DeclaredMethods(self) -> System.Collections.Generic.IEnumerable[System.Reflection.MethodInfo]:
        ...

    @property
    def DeclaredNestedTypes(self) -> System.Collections.Generic.IEnumerable[System.Reflection.TypeInfo]:
        ...

    @property
    def DeclaredProperties(self) -> System.Collections.Generic.IEnumerable[System.Reflection.PropertyInfo]:
        ...

    @property
    def ImplementedInterfaces(self) -> System.Collections.Generic.IEnumerable[typing.Type]:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def GetTypeInfo(self) -> System.Reflection.TypeInfo:
        ...

    def AsType(self) -> typing.Type:
        ...

    def GetDeclaredEvent(self, name: str) -> System.Reflection.EventInfo:
        ...

    def GetDeclaredField(self, name: str) -> System.Reflection.FieldInfo:
        ...

    def GetDeclaredMethod(self, name: str) -> System.Reflection.MethodInfo:
        ...

    def GetDeclaredNestedType(self, name: str) -> System.Reflection.TypeInfo:
        ...

    def GetDeclaredProperty(self, name: str) -> System.Reflection.PropertyInfo:
        ...

    def GetDeclaredMethods(self, name: str) -> System.Collections.Generic.IEnumerable[System.Reflection.MethodInfo]:
        ...

    def IsAssignableFrom(self, typeInfo: System.Reflection.TypeInfo) -> bool:
        ...


class Assembly(System.Object, System.Reflection.ICustomAttributeProvider, System.Runtime.Serialization.ISerializable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def DefinedTypes(self) -> System.Collections.Generic.IEnumerable[System.Reflection.TypeInfo]:
        ...

    @property
    def ExportedTypes(self) -> System.Collections.Generic.IEnumerable[typing.Type]:
        ...

    @property
    def CodeBase(self) -> str:
        ...

    @property
    def EntryPoint(self) -> System.Reflection.MethodInfo:
        ...

    @property
    def FullName(self) -> str:
        ...

    @property
    def ImageRuntimeVersion(self) -> str:
        ...

    @property
    def IsDynamic(self) -> bool:
        ...

    @property
    def Location(self) -> str:
        ...

    @property
    def ReflectionOnly(self) -> bool:
        ...

    @property
    def IsCollectible(self) -> bool:
        ...

    @property
    def IsFullyTrusted(self) -> bool:
        ...

    @property
    def CustomAttributes(self) -> System.Collections.Generic.IEnumerable[System.Reflection.CustomAttributeData]:
        ...

    @property
    def EscapedCodeBase(self) -> str:
        ...

    @property
    def ModuleResolve(self) -> typing.List[System_Reflection_ModuleResolveEventHandler]:
        ...

    @ModuleResolve.setter
    def ModuleResolve(self, value: typing.List[System_Reflection_ModuleResolveEventHandler]):
        ...

    @property
    def ManifestModule(self) -> System.Reflection.Module:
        ...

    @property
    def Modules(self) -> System.Collections.Generic.IEnumerable[System.Reflection.Module]:
        ...

    @property
    def GlobalAssemblyCache(self) -> bool:
        ...

    @property
    def HostContext(self) -> int:
        ...

    @property
    def SecurityRuleSet(self) -> int:
        """This property contains the int value of a member of the System.Security.SecurityRuleSet enum."""
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def GetTypes(self) -> typing.List[typing.Type]:
        ...

    def GetExportedTypes(self) -> typing.List[typing.Type]:
        ...

    def GetForwardedTypes(self) -> typing.List[typing.Type]:
        ...

    def GetManifestResourceInfo(self, resourceName: str) -> System.Reflection.ManifestResourceInfo:
        ...

    def GetManifestResourceNames(self) -> typing.List[str]:
        ...

    @typing.overload
    def GetManifestResourceStream(self, name: str) -> System.IO.Stream:
        ...

    @typing.overload
    def GetManifestResourceStream(self, type: typing.Type, name: str) -> System.IO.Stream:
        ...

    @typing.overload
    def GetName(self) -> System.Reflection.AssemblyName:
        ...

    @typing.overload
    def GetName(self, copiedName: bool) -> System.Reflection.AssemblyName:
        ...

    @typing.overload
    def GetType(self, name: str) -> typing.Type:
        ...

    @typing.overload
    def GetType(self, name: str, throwOnError: bool) -> typing.Type:
        ...

    @typing.overload
    def GetType(self, name: str, throwOnError: bool, ignoreCase: bool) -> typing.Type:
        ...

    def IsDefined(self, attributeType: typing.Type, inherit: bool) -> bool:
        ...

    def GetCustomAttributesData(self) -> System.Collections.Generic.IList[System.Reflection.CustomAttributeData]:
        ...

    @typing.overload
    def GetCustomAttributes(self, inherit: bool) -> typing.List[System.Object]:
        ...

    @typing.overload
    def GetCustomAttributes(self, attributeType: typing.Type, inherit: bool) -> typing.List[System.Object]:
        ...

    @typing.overload
    def CreateInstance(self, typeName: str) -> System.Object:
        ...

    @typing.overload
    def CreateInstance(self, typeName: str, ignoreCase: bool) -> System.Object:
        ...

    @typing.overload
    def CreateInstance(self, typeName: str, ignoreCase: bool, bindingAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, args: typing.List[System.Object], culture: System.Globalization.CultureInfo, activationAttributes: typing.List[System.Object]) -> System.Object:
        ...

    def GetModule(self, name: str) -> System.Reflection.Module:
        ...

    @typing.overload
    def GetModules(self) -> typing.List[System.Reflection.Module]:
        ...

    @typing.overload
    def GetModules(self, getResourceModules: bool) -> typing.List[System.Reflection.Module]:
        ...

    @typing.overload
    def GetLoadedModules(self) -> typing.List[System.Reflection.Module]:
        ...

    @typing.overload
    def GetLoadedModules(self, getResourceModules: bool) -> typing.List[System.Reflection.Module]:
        ...

    def GetReferencedAssemblies(self) -> typing.List[System.Reflection.AssemblyName]:
        ...

    @typing.overload
    def GetSatelliteAssembly(self, culture: System.Globalization.CultureInfo) -> System.Reflection.Assembly:
        ...

    @typing.overload
    def GetSatelliteAssembly(self, culture: System.Globalization.CultureInfo, version: System.Version) -> System.Reflection.Assembly:
        ...

    def GetFile(self, name: str) -> System.IO.FileStream:
        ...

    @typing.overload
    def GetFiles(self) -> typing.List[System.IO.FileStream]:
        ...

    @typing.overload
    def GetFiles(self, getResourceModules: bool) -> typing.List[System.IO.FileStream]:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def ToString(self) -> str:
        ...

    def Equals(self, o: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    @staticmethod
    def CreateQualifiedName(assemblyName: str, typeName: str) -> str:
        ...

    @staticmethod
    def GetAssembly(type: typing.Type) -> System.Reflection.Assembly:
        ...

    @staticmethod
    def GetEntryAssembly() -> System.Reflection.Assembly:
        ...

    @staticmethod
    @typing.overload
    def Load(rawAssembly: typing.List[int]) -> System.Reflection.Assembly:
        ...

    @staticmethod
    @typing.overload
    def Load(rawAssembly: typing.List[int], rawSymbolStore: typing.List[int]) -> System.Reflection.Assembly:
        ...

    @staticmethod
    def LoadFile(path: str) -> System.Reflection.Assembly:
        ...

    @staticmethod
    @typing.overload
    def LoadFrom(assemblyFile: str) -> System.Reflection.Assembly:
        ...

    @staticmethod
    @typing.overload
    def LoadFrom(assemblyFile: str, hashValue: typing.List[int], hashAlgorithm: System.Reflection.AssemblyHashAlgorithm) -> System.Reflection.Assembly:
        ...

    @staticmethod
    def UnsafeLoadFrom(assemblyFile: str) -> System.Reflection.Assembly:
        ...

    @typing.overload
    def LoadModule(self, moduleName: str, rawModule: typing.List[int]) -> System.Reflection.Module:
        ...

    @typing.overload
    def LoadModule(self, moduleName: str, rawModule: typing.List[int], rawSymbolStore: typing.List[int]) -> System.Reflection.Module:
        ...

    @staticmethod
    @typing.overload
    def ReflectionOnlyLoad(rawAssembly: typing.List[int]) -> System.Reflection.Assembly:
        ...

    @staticmethod
    @typing.overload
    def ReflectionOnlyLoad(assemblyString: str) -> System.Reflection.Assembly:
        ...

    @staticmethod
    def ReflectionOnlyLoadFrom(assemblyFile: str) -> System.Reflection.Assembly:
        ...

    @staticmethod
    def LoadWithPartialName(partialName: str) -> System.Reflection.Assembly:
        ...

    @staticmethod
    def GetExecutingAssembly() -> System.Reflection.Assembly:
        ...

    @staticmethod
    def GetCallingAssembly() -> System.Reflection.Assembly:
        ...

    @staticmethod
    @typing.overload
    def Load(assemblyString: str) -> System.Reflection.Assembly:
        ...

    @staticmethod
    @typing.overload
    def Load(assemblyRef: System.Reflection.AssemblyName) -> System.Reflection.Assembly:
        ...


class ResourceLocation(System.Enum):
    """This class has no documentation."""

    ContainedInAnotherAssembly = 2

    ContainedInManifestFile = 4

    Embedded = 1


class ManifestResourceInfo(System.Object):
    """This class has no documentation."""

    @property
    def ReferencedAssembly(self) -> System.Reflection.Assembly:
        ...

    @property
    def FileName(self) -> str:
        ...

    @property
    def ResourceLocation(self) -> int:
        """This property contains the int value of a member of the System.Reflection.ResourceLocation enum."""
        ...

    def __init__(self, containingAssembly: System.Reflection.Assembly, containingFileName: str, resourceLocation: System.Reflection.ResourceLocation) -> None:
        ...


class InterfaceMapping:
    """This class has no documentation."""

    @property
    def TargetType(self) -> typing.Type:
        ...

    @TargetType.setter
    def TargetType(self, value: typing.Type):
        ...

    @property
    def InterfaceType(self) -> typing.Type:
        ...

    @InterfaceType.setter
    def InterfaceType(self, value: typing.Type):
        ...

    @property
    def TargetMethods(self) -> typing.List[System.Reflection.MethodInfo]:
        ...

    @TargetMethods.setter
    def TargetMethods(self, value: typing.List[System.Reflection.MethodInfo]):
        ...

    @property
    def InterfaceMethods(self) -> typing.List[System.Reflection.MethodInfo]:
        ...

    @InterfaceMethods.setter
    def InterfaceMethods(self, value: typing.List[System.Reflection.MethodInfo]):
        ...


class RuntimeReflectionExtensions(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetRuntimeFields(type: typing.Type) -> System.Collections.Generic.IEnumerable[System.Reflection.FieldInfo]:
        ...

    @staticmethod
    def GetRuntimeMethods(type: typing.Type) -> System.Collections.Generic.IEnumerable[System.Reflection.MethodInfo]:
        ...

    @staticmethod
    def GetRuntimeProperties(type: typing.Type) -> System.Collections.Generic.IEnumerable[System.Reflection.PropertyInfo]:
        ...

    @staticmethod
    def GetRuntimeEvents(type: typing.Type) -> System.Collections.Generic.IEnumerable[System.Reflection.EventInfo]:
        ...

    @staticmethod
    def GetRuntimeField(type: typing.Type, name: str) -> System.Reflection.FieldInfo:
        ...

    @staticmethod
    def GetRuntimeMethod(type: typing.Type, name: str, parameters: typing.List[typing.Type]) -> System.Reflection.MethodInfo:
        ...

    @staticmethod
    def GetRuntimeProperty(type: typing.Type, name: str) -> System.Reflection.PropertyInfo:
        ...

    @staticmethod
    def GetRuntimeEvent(type: typing.Type, name: str) -> System.Reflection.EventInfo:
        ...

    @staticmethod
    def GetRuntimeBaseDefinition(method: System.Reflection.MethodInfo) -> System.Reflection.MethodInfo:
        ...

    @staticmethod
    def GetRuntimeInterfaceMap(typeInfo: System.Reflection.TypeInfo, interfaceType: typing.Type) -> System.Reflection.InterfaceMapping:
        ...

    @staticmethod
    def GetMethodInfo(del: System.Delegate) -> System.Reflection.MethodInfo:
        ...


class AssemblyKeyFileAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def KeyFile(self) -> str:
        ...

    def __init__(self, keyFile: str) -> None:
        ...


class EventAttributes(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = ...

    SpecialName = ...

    RTSpecialName = ...

    ReservedMask = ...


class AssemblyInformationalVersionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def InformationalVersion(self) -> str:
        ...

    def __init__(self, informationalVersion: str) -> None:
        ...


class AssemblyCompanyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Company(self) -> str:
        ...

    def __init__(self, company: str) -> None:
        ...


class AssemblyCopyrightAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Copyright(self) -> str:
        ...

    def __init__(self, copyright: str) -> None:
        ...


class AssemblyAlgorithmIdAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def AlgorithmId(self) -> int:
        ...

    @typing.overload
    def __init__(self, algorithmId: System.Reflection.AssemblyHashAlgorithm) -> None:
        ...

    @typing.overload
    def __init__(self, algorithmId: int) -> None:
        ...


class PropertyAttributes(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = ...

    SpecialName = ...

    RTSpecialName = ...

    HasDefault = ...

    Reserved2 = ...

    Reserved3 = ...

    Reserved4 = ...

    ReservedMask = ...


class AssemblyNameProxy(System.MarshalByRefObject):
    """This class has no documentation."""

    def GetAssemblyName(self, assemblyFile: str) -> System.Reflection.AssemblyName:
        ...


class AssemblyKeyNameAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def KeyName(self) -> str:
        ...

    def __init__(self, keyName: str) -> None:
        ...


class IntrospectionExtensions(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetTypeInfo(type: typing.Type) -> System.Reflection.TypeInfo:
        ...


class PortableExecutableKinds(System.Enum):
    """This class has no documentation."""

    NotAPortableExecutableImage = ...

    ILOnly = ...

    Required32Bit = ...

    PE32Plus = ...

    Unmanaged32Bit = ...

    Preferred32Bit = ...


class ImageFileMachine(System.Enum):
    """This class has no documentation."""

    I386 = ...

    IA64 = ...

    AMD64 = ...

    ARM = ...


class CallingConventions(System.Enum):
    """This class has no documentation."""

    Standard = ...

    VarArgs = ...

    Any = ...

    HasThis = ...

    ExplicitThis = ...


class Module(System.Object, System.Reflection.ICustomAttributeProvider, System.Runtime.Serialization.ISerializable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def Assembly(self) -> System.Reflection.Assembly:
        ...

    @property
    def FullyQualifiedName(self) -> str:
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def MDStreamVersion(self) -> int:
        ...

    @property
    def ModuleVersionId(self) -> System.Guid:
        ...

    @property
    def ScopeName(self) -> str:
        ...

    @property
    def ModuleHandle(self) -> System.ModuleHandle:
        ...

    @property
    def CustomAttributes(self) -> System.Collections.Generic.IEnumerable[System.Reflection.CustomAttributeData]:
        ...

    @property
    def MetadataToken(self) -> int:
        ...

    FilterTypeName: System_Reflection_TypeFilter = ...

    FilterTypeNameIgnoreCase: System_Reflection_TypeFilter = ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def GetModuleHandleImpl(self) -> System.ModuleHandle:
        """This method is protected."""
        ...

    def GetPEKind(self, peKind: System.Reflection.PortableExecutableKinds, machine: System.Reflection.ImageFileMachine) -> None:
        ...

    def IsResource(self) -> bool:
        ...

    def IsDefined(self, attributeType: typing.Type, inherit: bool) -> bool:
        ...

    def GetCustomAttributesData(self) -> System.Collections.Generic.IList[System.Reflection.CustomAttributeData]:
        ...

    @typing.overload
    def GetCustomAttributes(self, inherit: bool) -> typing.List[System.Object]:
        ...

    @typing.overload
    def GetCustomAttributes(self, attributeType: typing.Type, inherit: bool) -> typing.List[System.Object]:
        ...

    @typing.overload
    def GetMethod(self, name: str) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetMethod(self, name: str, types: typing.List[typing.Type]) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetMethod(self, name: str, bindingAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, callConvention: System.Reflection.CallingConventions, types: typing.List[typing.Type], modifiers: typing.List[System.Reflection.ParameterModifier]) -> System.Reflection.MethodInfo:
        ...

    def GetMethodImpl(self, name: str, bindingAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, callConvention: System.Reflection.CallingConventions, types: typing.List[typing.Type], modifiers: typing.List[System.Reflection.ParameterModifier]) -> System.Reflection.MethodInfo:
        """This method is protected."""
        ...

    @typing.overload
    def GetMethods(self) -> typing.List[System.Reflection.MethodInfo]:
        ...

    @typing.overload
    def GetMethods(self, bindingFlags: System.Reflection.BindingFlags) -> typing.List[System.Reflection.MethodInfo]:
        ...

    @typing.overload
    def GetField(self, name: str) -> System.Reflection.FieldInfo:
        ...

    @typing.overload
    def GetField(self, name: str, bindingAttr: System.Reflection.BindingFlags) -> System.Reflection.FieldInfo:
        ...

    @typing.overload
    def GetFields(self) -> typing.List[System.Reflection.FieldInfo]:
        ...

    @typing.overload
    def GetFields(self, bindingFlags: System.Reflection.BindingFlags) -> typing.List[System.Reflection.FieldInfo]:
        ...

    def GetTypes(self) -> typing.List[typing.Type]:
        ...

    @typing.overload
    def GetType(self, className: str) -> typing.Type:
        ...

    @typing.overload
    def GetType(self, className: str, ignoreCase: bool) -> typing.Type:
        ...

    @typing.overload
    def GetType(self, className: str, throwOnError: bool, ignoreCase: bool) -> typing.Type:
        ...

    def FindTypes(self, filter: System_Reflection_TypeFilter, filterCriteria: typing.Any) -> typing.List[typing.Type]:
        ...

    @typing.overload
    def ResolveField(self, metadataToken: int) -> System.Reflection.FieldInfo:
        ...

    @typing.overload
    def ResolveField(self, metadataToken: int, genericTypeArguments: typing.List[typing.Type], genericMethodArguments: typing.List[typing.Type]) -> System.Reflection.FieldInfo:
        ...

    @typing.overload
    def ResolveMember(self, metadataToken: int) -> System.Reflection.MemberInfo:
        ...

    @typing.overload
    def ResolveMember(self, metadataToken: int, genericTypeArguments: typing.List[typing.Type], genericMethodArguments: typing.List[typing.Type]) -> System.Reflection.MemberInfo:
        ...

    @typing.overload
    def ResolveMethod(self, metadataToken: int) -> System.Reflection.MethodBase:
        ...

    @typing.overload
    def ResolveMethod(self, metadataToken: int, genericTypeArguments: typing.List[typing.Type], genericMethodArguments: typing.List[typing.Type]) -> System.Reflection.MethodBase:
        ...

    def ResolveSignature(self, metadataToken: int) -> typing.List[int]:
        ...

    def ResolveString(self, metadataToken: int) -> str:
        ...

    @typing.overload
    def ResolveType(self, metadataToken: int) -> typing.Type:
        ...

    @typing.overload
    def ResolveType(self, metadataToken: int, genericTypeArguments: typing.List[typing.Type], genericMethodArguments: typing.List[typing.Type]) -> typing.Type:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def Equals(self, o: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def ToString(self) -> str:
        ...


class AssemblyDelaySignAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def DelaySign(self) -> bool:
        ...

    def __init__(self, delaySign: bool) -> None:
        ...


class ReflectionContext(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def MapAssembly(self, assembly: System.Reflection.Assembly) -> System.Reflection.Assembly:
        ...

    def MapType(self, type: System.Reflection.TypeInfo) -> System.Reflection.TypeInfo:
        ...

    def GetTypeForObject(self, value: typing.Any) -> System.Reflection.TypeInfo:
        ...


class AssemblyContentType(System.Enum):
    """This class has no documentation."""

    Default = 0

    WindowsRuntime = 1


class ReflectionTypeLoadException(System.SystemException, System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    @property
    def Types(self) -> typing.List[typing.Type]:
        ...

    @property
    def LoaderExceptions(self) -> typing.List[System.Exception]:
        ...

    @property
    def Message(self) -> str:
        ...

    @typing.overload
    def __init__(self, classes: typing.List[typing.Type], exceptions: typing.List[System.Exception]) -> None:
        ...

    @typing.overload
    def __init__(self, classes: typing.List[typing.Type], exceptions: typing.List[System.Exception], message: str) -> None:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def ToString(self) -> str:
        ...


class ProcessorArchitecture(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = ...

    MSIL = ...

    X86 = ...

    IA64 = ...

    Amd64 = ...

    Arm = ...


class FieldAttributes(System.Enum):
    """This class has no documentation."""

    FieldAccessMask = ...

    PrivateScope = ...

    Private = ...

    FamANDAssem = ...

    Assembly = ...

    Family = ...

    FamORAssem = ...

    Public = ...

    Static = ...

    InitOnly = ...

    Literal = ...

    NotSerialized = ...

    SpecialName = ...

    PinvokeImpl = ...

    RTSpecialName = ...

    HasFieldMarshal = ...

    HasDefault = ...

    HasFieldRVA = ...

    ReservedMask = ...


class TargetParameterCountException(System.ApplicationException):
    """This class has no documentation."""

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...


class CustomAttributeTypedArgument:
    """This class has no documentation."""

    @property
    def ArgumentType(self) -> typing.Type:
        ...

    @property
    def Value(self) -> System.Object:
        ...

    @typing.overload
    def __init__(self, argumentType: typing.Type, value: typing.Any) -> None:
        ...

    @typing.overload
    def __init__(self, value: typing.Any) -> None:
        ...

    def ToString(self) -> str:
        ...

    def GetHashCode(self) -> int:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...


class AssemblyDescriptionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Description(self) -> str:
        ...

    def __init__(self, description: str) -> None:
        ...


class MethodImplAttributes(System.Enum):
    """This class has no documentation."""

    CodeTypeMask = ...

    IL = ...

    Native = ...

    OPTIL = ...

    Runtime = ...

    ManagedMask = ...

    Unmanaged = ...

    Managed = ...

    ForwardRef = ...

    PreserveSig = ...

    InternalCall = ...

    Synchronized = ...

    NoInlining = ...

    AggressiveInlining = ...

    NoOptimization = ...

    AggressiveOptimization = ...

    MaxMethodImplVal = ...


class AssemblyCultureAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Culture(self) -> str:
        ...

    def __init__(self, culture: str) -> None:
        ...


class AssemblyVersionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Version(self) -> str:
        ...

    def __init__(self, version: str) -> None:
        ...


class DefaultMemberAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def MemberName(self) -> str:
        ...

    def __init__(self, memberName: str) -> None:
        ...


class InvalidFilterCriteriaException(System.ApplicationException):
    """This class has no documentation."""

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
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class CustomAttributeNamedArgument:
    """This class has no documentation."""

    @property
    def ArgumentType(self) -> typing.Type:
        ...

    @property
    def MemberInfo(self) -> System.Reflection.MemberInfo:
        ...

    @property
    def TypedValue(self) -> System.Reflection.CustomAttributeTypedArgument:
        ...

    @property
    def MemberName(self) -> str:
        ...

    @property
    def IsField(self) -> bool:
        ...

    @typing.overload
    def __init__(self, memberInfo: System.Reflection.MemberInfo, value: typing.Any) -> None:
        ...

    @typing.overload
    def __init__(self, memberInfo: System.Reflection.MemberInfo, typedArgument: System.Reflection.CustomAttributeTypedArgument) -> None:
        ...

    def ToString(self) -> str:
        ...

    def GetHashCode(self) -> int:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...


class TargetException(System.ApplicationException):
    """This class has no documentation."""

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
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class ObfuscationAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def StripAfterObfuscation(self) -> bool:
        ...

    @StripAfterObfuscation.setter
    def StripAfterObfuscation(self, value: bool):
        ...

    @property
    def Exclude(self) -> bool:
        ...

    @Exclude.setter
    def Exclude(self, value: bool):
        ...

    @property
    def ApplyToMembers(self) -> bool:
        ...

    @ApplyToMembers.setter
    def ApplyToMembers(self, value: bool):
        ...

    @property
    def Feature(self) -> str:
        ...

    @Feature.setter
    def Feature(self, value: str):
        ...

    def __init__(self) -> None:
        ...


class Missing(System.Object, System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    Value: System.Reflection.Missing = ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...


class Pointer(System.Object, System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    @staticmethod
    def Box(ptr: typing.Any, type: typing.Type) -> System.Object:
        ...

    @staticmethod
    def Unbox(ptr: typing.Any) -> typing.Any:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...


class TargetInvocationException(System.ApplicationException):
    """This class has no documentation."""

    @typing.overload
    def __init__(self, inner: System.Exception) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...


class GenericParameterAttributes(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = ...

    VarianceMask = ...

    Covariant = ...

    Contravariant = ...

    SpecialConstraintMask = ...

    ReferenceTypeConstraint = ...

    NotNullableValueTypeConstraint = ...

    DefaultConstructorConstraint = ...


class CustomAttributeFormatException(System.FormatException):
    """This class has no documentation."""

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
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """This method is protected."""
        ...


class ObfuscateAssemblyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def AssemblyIsPrivate(self) -> bool:
        ...

    @property
    def StripAfterObfuscation(self) -> bool:
        ...

    @StripAfterObfuscation.setter
    def StripAfterObfuscation(self, value: bool):
        ...

    def __init__(self, assemblyIsPrivate: bool) -> None:
        ...


class AssemblyProductAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Product(self) -> str:
        ...

    def __init__(self, product: str) -> None:
        ...


class AssemblyTitleAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Title(self) -> str:
        ...

    def __init__(self, title: str) -> None:
        ...


class AssemblyTrademarkAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Trademark(self) -> str:
        ...

    def __init__(self, trademark: str) -> None:
        ...


class AssemblyFileVersionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Version(self) -> str:
        ...

    def __init__(self, version: str) -> None:
        ...


class ExceptionHandlingClauseOptions(System.Enum):
    """This class has no documentation."""

    Clause = ...

    Filter = ...

    Finally = ...

    Fault = ...


class AssemblyMetadataAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Key(self) -> str:
        ...

    @property
    def Value(self) -> str:
        ...

    def __init__(self, key: str, value: str) -> None:
        ...


class AssemblyNameFlags(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = ...

    PublicKey = ...

    EnableJITcompileOptimizer = ...

    EnableJITcompileTracking = ...

    Retargetable = ...


class AssemblyFlagsAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Flags(self) -> int:
        ...

    @property
    def AssemblyFlags(self) -> int:
        ...

    @typing.overload
    def __init__(self, flags: int) -> None:
        ...

    @typing.overload
    def __init__(self, assemblyFlags: int) -> None:
        ...

    @typing.overload
    def __init__(self, assemblyFlags: System.Reflection.AssemblyNameFlags) -> None:
        ...


class AmbiguousMatchException(System.SystemException):
    """This class has no documentation."""

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        ...

    @typing.overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...


class MethodAttributes(System.Enum):
    """This class has no documentation."""

    MemberAccessMask = ...

    PrivateScope = ...

    Private = ...

    FamANDAssem = ...

    Assembly = ...

    Family = ...

    FamORAssem = ...

    Public = ...

    Static = ...

    Final = ...

    Virtual = ...

    HideBySig = ...

    CheckAccessOnOverride = ...

    VtableLayoutMask = ...

    ReuseSlot = ...

    NewSlot = ...

    Abstract = ...

    SpecialName = ...

    PinvokeImpl = ...

    UnmanagedExport = ...

    RTSpecialName = ...

    HasSecurity = ...

    RequireSecObject = ...

    ReservedMask = ...


class AssemblyDefaultAliasAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def DefaultAlias(self) -> str:
        ...

    def __init__(self, defaultAlias: str) -> None:
        ...


class ResourceAttributes(System.Enum):
    """This class has no documentation."""

    Public = ...

    Private = ...


class CustomAttributeExtensions(System.Object):
    """This class has no documentation."""

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.Assembly, attributeType: typing.Type) -> System.Attribute:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.Module, attributeType: typing.Type) -> System.Attribute:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.MemberInfo, attributeType: typing.Type) -> System.Attribute:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.ParameterInfo, attributeType: typing.Type) -> System.Attribute:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.Assembly) -> System_Reflection_CustomAttributeExtensions_GetCustomAttribute_T:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.Module) -> System_Reflection_CustomAttributeExtensions_GetCustomAttribute_T:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.MemberInfo) -> System_Reflection_CustomAttributeExtensions_GetCustomAttribute_T:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.ParameterInfo) -> System_Reflection_CustomAttributeExtensions_GetCustomAttribute_T:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.MemberInfo, attributeType: typing.Type, inherit: bool) -> System.Attribute:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.ParameterInfo, attributeType: typing.Type, inherit: bool) -> System.Attribute:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.MemberInfo, inherit: bool) -> System_Reflection_CustomAttributeExtensions_GetCustomAttribute_T:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttribute(element: System.Reflection.ParameterInfo, inherit: bool) -> System_Reflection_CustomAttributeExtensions_GetCustomAttribute_T:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.Assembly) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.Module) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.MemberInfo) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.ParameterInfo) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.MemberInfo, inherit: bool) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.ParameterInfo, inherit: bool) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.Assembly, attributeType: typing.Type) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.Module, attributeType: typing.Type) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.MemberInfo, attributeType: typing.Type) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.ParameterInfo, attributeType: typing.Type) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.Assembly) -> System.Collections.Generic.IEnumerable[System_Reflection_CustomAttributeExtensions_GetCustomAttributes_T]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.Module) -> System.Collections.Generic.IEnumerable[System_Reflection_CustomAttributeExtensions_GetCustomAttributes_T]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.MemberInfo) -> System.Collections.Generic.IEnumerable[System_Reflection_CustomAttributeExtensions_GetCustomAttributes_T]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.ParameterInfo) -> System.Collections.Generic.IEnumerable[System_Reflection_CustomAttributeExtensions_GetCustomAttributes_T]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.MemberInfo, attributeType: typing.Type, inherit: bool) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.ParameterInfo, attributeType: typing.Type, inherit: bool) -> System.Collections.Generic.IEnumerable[System.Attribute]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.MemberInfo, inherit: bool) -> System.Collections.Generic.IEnumerable[System_Reflection_CustomAttributeExtensions_GetCustomAttributes_T]:
        ...

    @staticmethod
    @typing.overload
    def GetCustomAttributes(element: System.Reflection.ParameterInfo, inherit: bool) -> System.Collections.Generic.IEnumerable[System_Reflection_CustomAttributeExtensions_GetCustomAttributes_T]:
        ...

    @staticmethod
    @typing.overload
    def IsDefined(element: System.Reflection.Assembly, attributeType: typing.Type) -> bool:
        ...

    @staticmethod
    @typing.overload
    def IsDefined(element: System.Reflection.Module, attributeType: typing.Type) -> bool:
        ...

    @staticmethod
    @typing.overload
    def IsDefined(element: System.Reflection.MemberInfo, attributeType: typing.Type) -> bool:
        ...

    @staticmethod
    @typing.overload
    def IsDefined(element: System.Reflection.ParameterInfo, attributeType: typing.Type) -> bool:
        ...

    @staticmethod
    @typing.overload
    def IsDefined(element: System.Reflection.MemberInfo, attributeType: typing.Type, inherit: bool) -> bool:
        ...

    @staticmethod
    @typing.overload
    def IsDefined(element: System.Reflection.ParameterInfo, attributeType: typing.Type, inherit: bool) -> bool:
        ...


class MemberTypes(System.Enum):
    """This class has no documentation."""

    Constructor = ...

    Event = ...

    Field = ...

    Method = ...

    Property = ...

    TypeInfo = ...

    Custom = ...

    NestedType = ...

    All = ...


class TypeDelegator(System.Reflection.TypeInfo):
    """This class has no documentation."""

    @property
    def typeImpl(self) -> typing.Type:
        """This field is protected."""
        ...

    @typeImpl.setter
    def typeImpl(self, value: typing.Type):
        """This field is protected."""
        ...

    @property
    def GUID(self) -> System.Guid:
        ...

    @property
    def MetadataToken(self) -> int:
        ...

    @property
    def Module(self) -> System.Reflection.Module:
        ...

    @property
    def Assembly(self) -> System.Reflection.Assembly:
        ...

    @property
    def TypeHandle(self) -> System.RuntimeTypeHandle:
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def FullName(self) -> str:
        ...

    @property
    def Namespace(self) -> str:
        ...

    @property
    def AssemblyQualifiedName(self) -> str:
        ...

    @property
    def BaseType(self) -> typing.Type:
        ...

    @property
    def IsTypeDefinition(self) -> bool:
        ...

    @property
    def IsSZArray(self) -> bool:
        ...

    @property
    def IsVariableBoundArray(self) -> bool:
        ...

    @property
    def IsGenericTypeParameter(self) -> bool:
        ...

    @property
    def IsGenericMethodParameter(self) -> bool:
        ...

    @property
    def IsByRefLike(self) -> bool:
        ...

    @property
    def IsConstructedGenericType(self) -> bool:
        ...

    @property
    def IsCollectible(self) -> bool:
        ...

    @property
    def UnderlyingSystemType(self) -> typing.Type:
        ...

    def IsAssignableFrom(self, typeInfo: System.Reflection.TypeInfo) -> bool:
        ...

    @typing.overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, delegatingType: typing.Type) -> None:
        ...

    def InvokeMember(self, name: str, invokeAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, target: typing.Any, args: typing.List[System.Object], modifiers: typing.List[System.Reflection.ParameterModifier], culture: System.Globalization.CultureInfo, namedParameters: typing.List[str]) -> System.Object:
        ...

    def GetConstructorImpl(self, bindingAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, callConvention: System.Reflection.CallingConventions, types: typing.List[typing.Type], modifiers: typing.List[System.Reflection.ParameterModifier]) -> System.Reflection.ConstructorInfo:
        """This method is protected."""
        ...

    def GetConstructors(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.ConstructorInfo]:
        ...

    def GetMethodImpl(self, name: str, bindingAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, callConvention: System.Reflection.CallingConventions, types: typing.List[typing.Type], modifiers: typing.List[System.Reflection.ParameterModifier]) -> System.Reflection.MethodInfo:
        """This method is protected."""
        ...

    def GetMethods(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.MethodInfo]:
        ...

    def GetField(self, name: str, bindingAttr: System.Reflection.BindingFlags) -> System.Reflection.FieldInfo:
        ...

    def GetFields(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.FieldInfo]:
        ...

    def GetInterface(self, name: str, ignoreCase: bool) -> typing.Type:
        ...

    def GetInterfaces(self) -> typing.List[typing.Type]:
        ...

    def GetEvent(self, name: str, bindingAttr: System.Reflection.BindingFlags) -> System.Reflection.EventInfo:
        ...

    @typing.overload
    def GetEvents(self) -> typing.List[System.Reflection.EventInfo]:
        ...

    def GetPropertyImpl(self, name: str, bindingAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, returnType: typing.Type, types: typing.List[typing.Type], modifiers: typing.List[System.Reflection.ParameterModifier]) -> System.Reflection.PropertyInfo:
        """This method is protected."""
        ...

    def GetProperties(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.PropertyInfo]:
        ...

    @typing.overload
    def GetEvents(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.EventInfo]:
        ...

    def GetNestedTypes(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[typing.Type]:
        ...

    def GetNestedType(self, name: str, bindingAttr: System.Reflection.BindingFlags) -> typing.Type:
        ...

    def GetMember(self, name: str, type: System.Reflection.MemberTypes, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.MemberInfo]:
        ...

    def GetMembers(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.MemberInfo]:
        ...

    def GetAttributeFlagsImpl(self) -> int:
        """
        This method is protected.
        
        :returns: This method returns the int value of a member of the System.Reflection.TypeAttributes enum.
        """
        ...

    def IsArrayImpl(self) -> bool:
        """This method is protected."""
        ...

    def IsPrimitiveImpl(self) -> bool:
        """This method is protected."""
        ...

    def IsByRefImpl(self) -> bool:
        """This method is protected."""
        ...

    def IsPointerImpl(self) -> bool:
        """This method is protected."""
        ...

    def IsValueTypeImpl(self) -> bool:
        """This method is protected."""
        ...

    def IsCOMObjectImpl(self) -> bool:
        """This method is protected."""
        ...

    def GetElementType(self) -> typing.Type:
        ...

    def HasElementTypeImpl(self) -> bool:
        """This method is protected."""
        ...

    @typing.overload
    def GetCustomAttributes(self, inherit: bool) -> typing.List[System.Object]:
        ...

    @typing.overload
    def GetCustomAttributes(self, attributeType: typing.Type, inherit: bool) -> typing.List[System.Object]:
        ...

    def IsDefined(self, attributeType: typing.Type, inherit: bool) -> bool:
        ...

    def GetInterfaceMap(self, interfaceType: typing.Type) -> System.Reflection.InterfaceMapping:
        ...


class IReflect(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def UnderlyingSystemType(self) -> typing.Type:
        ...

    @typing.overload
    def GetMethod(self, name: str, bindingAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, types: typing.List[typing.Type], modifiers: typing.List[System.Reflection.ParameterModifier]) -> System.Reflection.MethodInfo:
        ...

    @typing.overload
    def GetMethod(self, name: str, bindingAttr: System.Reflection.BindingFlags) -> System.Reflection.MethodInfo:
        ...

    def GetMethods(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.MethodInfo]:
        ...

    def GetField(self, name: str, bindingAttr: System.Reflection.BindingFlags) -> System.Reflection.FieldInfo:
        ...

    def GetFields(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.FieldInfo]:
        ...

    @typing.overload
    def GetProperty(self, name: str, bindingAttr: System.Reflection.BindingFlags) -> System.Reflection.PropertyInfo:
        ...

    @typing.overload
    def GetProperty(self, name: str, bindingAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, returnType: typing.Type, types: typing.List[typing.Type], modifiers: typing.List[System.Reflection.ParameterModifier]) -> System.Reflection.PropertyInfo:
        ...

    def GetProperties(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.PropertyInfo]:
        ...

    def GetMember(self, name: str, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.MemberInfo]:
        ...

    def GetMembers(self, bindingAttr: System.Reflection.BindingFlags) -> typing.List[System.Reflection.MemberInfo]:
        ...

    def InvokeMember(self, name: str, invokeAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, target: typing.Any, args: typing.List[System.Object], modifiers: typing.List[System.Reflection.ParameterModifier], culture: System.Globalization.CultureInfo, namedParameters: typing.List[str]) -> System.Object:
        ...


class TypeAttributes(System.Enum):
    """This class has no documentation."""

    VisibilityMask = ...

    NotPublic = ...

    Public = ...

    NestedPublic = ...

    NestedPrivate = ...

    NestedFamily = ...

    NestedAssembly = ...

    NestedFamANDAssem = ...

    NestedFamORAssem = ...

    LayoutMask = ...

    AutoLayout = ...

    SequentialLayout = ...

    ExplicitLayout = ...

    ClassSemanticsMask = ...

    Class = ...

    Interface = ...

    Abstract = ...

    Sealed = ...

    SpecialName = ...

    Import = ...

    Serializable = ...

    WindowsRuntime = ...

    StringFormatMask = ...

    AnsiClass = ...

    UnicodeClass = ...

    AutoClass = ...

    CustomFormatClass = ...

    CustomFormatMask = ...

    BeforeFieldInit = ...

    RTSpecialName = ...

    HasSecurity = ...

    ReservedMask = ...


class AssemblyConfigurationAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Configuration(self) -> str:
        ...

    def __init__(self, configuration: str) -> None:
        ...


