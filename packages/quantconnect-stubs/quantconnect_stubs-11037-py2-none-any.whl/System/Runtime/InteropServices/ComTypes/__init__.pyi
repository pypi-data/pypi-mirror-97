import abc
import typing

import System
import System.Runtime.InteropServices.ComTypes


class IConnectionPointContainer(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def EnumConnectionPoints(self, ppEnum: System.Runtime.InteropServices.ComTypes.IEnumConnectionPoints) -> None:
        ...

    def FindConnectionPoint(self, riid: System.Guid, ppCP: System.Runtime.InteropServices.ComTypes.IConnectionPoint) -> None:
        ...


class CONNECTDATA:
    """This class has no documentation."""

    @property
    def pUnk(self) -> System.Object:
        ...

    @pUnk.setter
    def pUnk(self, value: System.Object):
        ...

    @property
    def dwCookie(self) -> int:
        ...

    @dwCookie.setter
    def dwCookie(self, value: int):
        ...


class IEnumConnections(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Next(self, celt: int, rgelt: typing.List[System.Runtime.InteropServices.ComTypes.CONNECTDATA], pceltFetched: System.IntPtr) -> int:
        ...

    def Skip(self, celt: int) -> int:
        ...

    def Reset(self) -> None:
        ...

    def Clone(self, ppenum: System.Runtime.InteropServices.ComTypes.IEnumConnections) -> None:
        ...


class IConnectionPoint(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetConnectionInterface(self, pIID: System.Guid) -> None:
        ...

    def GetConnectionPointContainer(self, ppCPC: System.Runtime.InteropServices.ComTypes.IConnectionPointContainer) -> None:
        ...

    def Advise(self, pUnkSink: typing.Any, pdwCookie: int) -> None:
        ...

    def Unadvise(self, dwCookie: int) -> None:
        ...

    def EnumConnections(self, ppEnum: System.Runtime.InteropServices.ComTypes.IEnumConnections) -> None:
        ...


class IEnumConnectionPoints(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Next(self, celt: int, rgelt: typing.List[System.Runtime.InteropServices.ComTypes.IConnectionPoint], pceltFetched: System.IntPtr) -> int:
        ...

    def Skip(self, celt: int) -> int:
        ...

    def Reset(self) -> None:
        ...

    def Clone(self, ppenum: System.Runtime.InteropServices.ComTypes.IEnumConnectionPoints) -> None:
        ...


class FILETIME:
    """This class has no documentation."""

    @property
    def dwLowDateTime(self) -> int:
        ...

    @dwLowDateTime.setter
    def dwLowDateTime(self, value: int):
        ...

    @property
    def dwHighDateTime(self) -> int:
        ...

    @dwHighDateTime.setter
    def dwHighDateTime(self, value: int):
        ...


class STATSTG:
    """This class has no documentation."""

    @property
    def pwcsName(self) -> str:
        ...

    @pwcsName.setter
    def pwcsName(self, value: str):
        ...

    @property
    def type(self) -> int:
        ...

    @type.setter
    def type(self, value: int):
        ...

    @property
    def cbSize(self) -> int:
        ...

    @cbSize.setter
    def cbSize(self, value: int):
        ...

    @property
    def mtime(self) -> System.Runtime.InteropServices.ComTypes.FILETIME:
        ...

    @mtime.setter
    def mtime(self, value: System.Runtime.InteropServices.ComTypes.FILETIME):
        ...

    @property
    def ctime(self) -> System.Runtime.InteropServices.ComTypes.FILETIME:
        ...

    @ctime.setter
    def ctime(self, value: System.Runtime.InteropServices.ComTypes.FILETIME):
        ...

    @property
    def atime(self) -> System.Runtime.InteropServices.ComTypes.FILETIME:
        ...

    @atime.setter
    def atime(self, value: System.Runtime.InteropServices.ComTypes.FILETIME):
        ...

    @property
    def grfMode(self) -> int:
        ...

    @grfMode.setter
    def grfMode(self, value: int):
        ...

    @property
    def grfLocksSupported(self) -> int:
        ...

    @grfLocksSupported.setter
    def grfLocksSupported(self, value: int):
        ...

    @property
    def clsid(self) -> System.Guid:
        ...

    @clsid.setter
    def clsid(self, value: System.Guid):
        ...

    @property
    def grfStateBits(self) -> int:
        ...

    @grfStateBits.setter
    def grfStateBits(self, value: int):
        ...

    @property
    def reserved(self) -> int:
        ...

    @reserved.setter
    def reserved(self, value: int):
        ...


class IStream(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Read(self, pv: typing.List[int], cb: int, pcbRead: System.IntPtr) -> None:
        ...

    def Write(self, pv: typing.List[int], cb: int, pcbWritten: System.IntPtr) -> None:
        ...

    def Seek(self, dlibMove: int, dwOrigin: int, plibNewPosition: System.IntPtr) -> None:
        ...

    def SetSize(self, libNewSize: int) -> None:
        ...

    def CopyTo(self, pstm: System.Runtime.InteropServices.ComTypes.IStream, cb: int, pcbRead: System.IntPtr, pcbWritten: System.IntPtr) -> None:
        ...

    def Commit(self, grfCommitFlags: int) -> None:
        ...

    def Revert(self) -> None:
        ...

    def LockRegion(self, libOffset: int, cb: int, dwLockType: int) -> None:
        ...

    def UnlockRegion(self, libOffset: int, cb: int, dwLockType: int) -> None:
        ...

    def Stat(self, pstatstg: System.Runtime.InteropServices.ComTypes.STATSTG, grfStatFlag: int) -> None:
        ...

    def Clone(self, ppstm: System.Runtime.InteropServices.ComTypes.IStream) -> None:
        ...


class IEnumString(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Next(self, celt: int, rgelt: typing.List[str], pceltFetched: System.IntPtr) -> int:
        ...

    def Skip(self, celt: int) -> int:
        ...

    def Reset(self) -> None:
        ...

    def Clone(self, ppenum: System.Runtime.InteropServices.ComTypes.IEnumString) -> None:
        ...


class DESCKIND(System.Enum):
    """This class has no documentation."""

    DESCKIND_NONE = 0

    DESCKIND_FUNCDESC = ...

    DESCKIND_VARDESC = ...

    DESCKIND_TYPECOMP = ...

    DESCKIND_IMPLICITAPPOBJ = ...

    DESCKIND_MAX = ...


class BINDPTR:
    """This class has no documentation."""

    @property
    def lpfuncdesc(self) -> System.IntPtr:
        ...

    @lpfuncdesc.setter
    def lpfuncdesc(self, value: System.IntPtr):
        ...

    @property
    def lpvardesc(self) -> System.IntPtr:
        ...

    @lpvardesc.setter
    def lpvardesc(self, value: System.IntPtr):
        ...

    @property
    def lptcomp(self) -> System.IntPtr:
        ...

    @lptcomp.setter
    def lptcomp(self, value: System.IntPtr):
        ...


class ITypeComp(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Bind(self, szName: str, lHashVal: int, wFlags: int, ppTInfo: System.Runtime.InteropServices.ComTypes.ITypeInfo, pDescKind: System.Runtime.InteropServices.ComTypes.DESCKIND, pBindPtr: System.Runtime.InteropServices.ComTypes.BINDPTR) -> None:
        ...

    def BindType(self, szName: str, lHashVal: int, ppTInfo: System.Runtime.InteropServices.ComTypes.ITypeInfo, ppTComp: System.Runtime.InteropServices.ComTypes.ITypeComp) -> None:
        ...


class IMPLTYPEFLAGS(System.Enum):
    """This class has no documentation."""

    IMPLTYPEFLAG_FDEFAULT = ...

    IMPLTYPEFLAG_FSOURCE = ...

    IMPLTYPEFLAG_FRESTRICTED = ...

    IMPLTYPEFLAG_FDEFAULTVTABLE = ...


class DISPPARAMS:
    """This class has no documentation."""

    @property
    def rgvarg(self) -> System.IntPtr:
        ...

    @rgvarg.setter
    def rgvarg(self, value: System.IntPtr):
        ...

    @property
    def rgdispidNamedArgs(self) -> System.IntPtr:
        ...

    @rgdispidNamedArgs.setter
    def rgdispidNamedArgs(self, value: System.IntPtr):
        ...

    @property
    def cArgs(self) -> int:
        ...

    @cArgs.setter
    def cArgs(self, value: int):
        ...

    @property
    def cNamedArgs(self) -> int:
        ...

    @cNamedArgs.setter
    def cNamedArgs(self, value: int):
        ...


class INVOKEKIND(System.Enum):
    """This class has no documentation."""

    INVOKE_FUNC = ...

    INVOKE_PROPERTYGET = ...

    INVOKE_PROPERTYPUT = ...

    INVOKE_PROPERTYPUTREF = ...


class TYPEKIND(System.Enum):
    """This class has no documentation."""

    TKIND_ENUM = 0

    TKIND_RECORD = ...

    TKIND_MODULE = ...

    TKIND_INTERFACE = ...

    TKIND_DISPATCH = ...

    TKIND_COCLASS = ...

    TKIND_ALIAS = ...

    TKIND_UNION = ...

    TKIND_MAX = ...


class ITypeLib(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetTypeInfoCount(self) -> int:
        ...

    def GetTypeInfo(self, index: int, ppTI: System.Runtime.InteropServices.ComTypes.ITypeInfo) -> None:
        ...

    def GetTypeInfoType(self, index: int, pTKind: System.Runtime.InteropServices.ComTypes.TYPEKIND) -> None:
        ...

    def GetTypeInfoOfGuid(self, guid: System.Guid, ppTInfo: System.Runtime.InteropServices.ComTypes.ITypeInfo) -> None:
        ...

    def GetLibAttr(self, ppTLibAttr: System.IntPtr) -> None:
        ...

    def GetTypeComp(self, ppTComp: System.Runtime.InteropServices.ComTypes.ITypeComp) -> None:
        ...

    def GetDocumentation(self, index: int, strName: str, strDocString: str, dwHelpContext: int, strHelpFile: str) -> None:
        ...

    def IsName(self, szNameBuf: str, lHashVal: int) -> bool:
        ...

    def FindName(self, szNameBuf: str, lHashVal: int, ppTInfo: typing.List[System.Runtime.InteropServices.ComTypes.ITypeInfo], rgMemId: typing.List[int], pcFound: int) -> None:
        ...

    def ReleaseTLibAttr(self, pTLibAttr: System.IntPtr) -> None:
        ...


class ITypeInfo(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetTypeAttr(self, ppTypeAttr: System.IntPtr) -> None:
        ...

    def GetTypeComp(self, ppTComp: System.Runtime.InteropServices.ComTypes.ITypeComp) -> None:
        ...

    def GetFuncDesc(self, index: int, ppFuncDesc: System.IntPtr) -> None:
        ...

    def GetVarDesc(self, index: int, ppVarDesc: System.IntPtr) -> None:
        ...

    def GetNames(self, memid: int, rgBstrNames: typing.List[str], cMaxNames: int, pcNames: int) -> None:
        ...

    def GetRefTypeOfImplType(self, index: int, href: int) -> None:
        ...

    def GetImplTypeFlags(self, index: int, pImplTypeFlags: System.Runtime.InteropServices.ComTypes.IMPLTYPEFLAGS) -> None:
        ...

    def GetIDsOfNames(self, rgszNames: typing.List[str], cNames: int, pMemId: typing.List[int]) -> None:
        ...

    def Invoke(self, pvInstance: typing.Any, memid: int, wFlags: int, pDispParams: System.Runtime.InteropServices.ComTypes.DISPPARAMS, pVarResult: System.IntPtr, pExcepInfo: System.IntPtr, puArgErr: int) -> None:
        ...

    def GetDocumentation(self, index: int, strName: str, strDocString: str, dwHelpContext: int, strHelpFile: str) -> None:
        ...

    def GetDllEntry(self, memid: int, invKind: System.Runtime.InteropServices.ComTypes.INVOKEKIND, pBstrDllName: System.IntPtr, pBstrName: System.IntPtr, pwOrdinal: System.IntPtr) -> None:
        ...

    def GetRefTypeInfo(self, hRef: int, ppTI: System.Runtime.InteropServices.ComTypes.ITypeInfo) -> None:
        ...

    def AddressOfMember(self, memid: int, invKind: System.Runtime.InteropServices.ComTypes.INVOKEKIND, ppv: System.IntPtr) -> None:
        ...

    def CreateInstance(self, pUnkOuter: typing.Any, riid: System.Guid, ppvObj: typing.Any) -> None:
        ...

    def GetMops(self, memid: int, pBstrMops: str) -> None:
        ...

    def GetContainingTypeLib(self, ppTLB: System.Runtime.InteropServices.ComTypes.ITypeLib, pIndex: int) -> None:
        ...

    def ReleaseTypeAttr(self, pTypeAttr: System.IntPtr) -> None:
        ...

    def ReleaseFuncDesc(self, pFuncDesc: System.IntPtr) -> None:
        ...

    def ReleaseVarDesc(self, pVarDesc: System.IntPtr) -> None:
        ...


class ITypeInfo2(System.Runtime.InteropServices.ComTypes.ITypeInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetTypeAttr(self, ppTypeAttr: System.IntPtr) -> None:
        ...

    def GetTypeComp(self, ppTComp: System.Runtime.InteropServices.ComTypes.ITypeComp) -> None:
        ...

    def GetFuncDesc(self, index: int, ppFuncDesc: System.IntPtr) -> None:
        ...

    def GetVarDesc(self, index: int, ppVarDesc: System.IntPtr) -> None:
        ...

    def GetNames(self, memid: int, rgBstrNames: typing.List[str], cMaxNames: int, pcNames: int) -> None:
        ...

    def GetRefTypeOfImplType(self, index: int, href: int) -> None:
        ...

    def GetImplTypeFlags(self, index: int, pImplTypeFlags: System.Runtime.InteropServices.ComTypes.IMPLTYPEFLAGS) -> None:
        ...

    def GetIDsOfNames(self, rgszNames: typing.List[str], cNames: int, pMemId: typing.List[int]) -> None:
        ...

    def Invoke(self, pvInstance: typing.Any, memid: int, wFlags: int, pDispParams: System.Runtime.InteropServices.ComTypes.DISPPARAMS, pVarResult: System.IntPtr, pExcepInfo: System.IntPtr, puArgErr: int) -> None:
        ...

    def GetDocumentation(self, index: int, strName: str, strDocString: str, dwHelpContext: int, strHelpFile: str) -> None:
        ...

    def GetDllEntry(self, memid: int, invKind: System.Runtime.InteropServices.ComTypes.INVOKEKIND, pBstrDllName: System.IntPtr, pBstrName: System.IntPtr, pwOrdinal: System.IntPtr) -> None:
        ...

    def GetRefTypeInfo(self, hRef: int, ppTI: System.Runtime.InteropServices.ComTypes.ITypeInfo) -> None:
        ...

    def AddressOfMember(self, memid: int, invKind: System.Runtime.InteropServices.ComTypes.INVOKEKIND, ppv: System.IntPtr) -> None:
        ...

    def CreateInstance(self, pUnkOuter: typing.Any, riid: System.Guid, ppvObj: typing.Any) -> None:
        ...

    def GetMops(self, memid: int, pBstrMops: str) -> None:
        ...

    def GetContainingTypeLib(self, ppTLB: System.Runtime.InteropServices.ComTypes.ITypeLib, pIndex: int) -> None:
        ...

    def ReleaseTypeAttr(self, pTypeAttr: System.IntPtr) -> None:
        ...

    def ReleaseFuncDesc(self, pFuncDesc: System.IntPtr) -> None:
        ...

    def ReleaseVarDesc(self, pVarDesc: System.IntPtr) -> None:
        ...

    def GetTypeKind(self, pTypeKind: System.Runtime.InteropServices.ComTypes.TYPEKIND) -> None:
        ...

    def GetTypeFlags(self, pTypeFlags: int) -> None:
        ...

    def GetFuncIndexOfMemId(self, memid: int, invKind: System.Runtime.InteropServices.ComTypes.INVOKEKIND, pFuncIndex: int) -> None:
        ...

    def GetVarIndexOfMemId(self, memid: int, pVarIndex: int) -> None:
        ...

    def GetCustData(self, guid: System.Guid, pVarVal: typing.Any) -> None:
        ...

    def GetFuncCustData(self, index: int, guid: System.Guid, pVarVal: typing.Any) -> None:
        ...

    def GetParamCustData(self, indexFunc: int, indexParam: int, guid: System.Guid, pVarVal: typing.Any) -> None:
        ...

    def GetVarCustData(self, index: int, guid: System.Guid, pVarVal: typing.Any) -> None:
        ...

    def GetImplTypeCustData(self, index: int, guid: System.Guid, pVarVal: typing.Any) -> None:
        ...

    def GetDocumentation2(self, memid: int, pbstrHelpString: str, pdwHelpStringContext: int, pbstrHelpStringDll: str) -> None:
        ...

    def GetAllCustData(self, pCustData: System.IntPtr) -> None:
        ...

    def GetAllFuncCustData(self, index: int, pCustData: System.IntPtr) -> None:
        ...

    def GetAllParamCustData(self, indexFunc: int, indexParam: int, pCustData: System.IntPtr) -> None:
        ...

    def GetAllVarCustData(self, index: int, pCustData: System.IntPtr) -> None:
        ...

    def GetAllImplTypeCustData(self, index: int, pCustData: System.IntPtr) -> None:
        ...


class IEnumMoniker(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Next(self, celt: int, rgelt: typing.List[System.Runtime.InteropServices.ComTypes.IMoniker], pceltFetched: System.IntPtr) -> int:
        ...

    def Skip(self, celt: int) -> int:
        ...

    def Reset(self) -> None:
        ...

    def Clone(self, ppenum: System.Runtime.InteropServices.ComTypes.IEnumMoniker) -> None:
        ...


class IMoniker(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetClassID(self, pClassID: System.Guid) -> None:
        ...

    def IsDirty(self) -> int:
        ...

    def Load(self, pStm: System.Runtime.InteropServices.ComTypes.IStream) -> None:
        ...

    def Save(self, pStm: System.Runtime.InteropServices.ComTypes.IStream, fClearDirty: bool) -> None:
        ...

    def GetSizeMax(self, pcbSize: int) -> None:
        ...

    def BindToObject(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmkToLeft: System.Runtime.InteropServices.ComTypes.IMoniker, riidResult: System.Guid, ppvResult: typing.Any) -> None:
        ...

    def BindToStorage(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmkToLeft: System.Runtime.InteropServices.ComTypes.IMoniker, riid: System.Guid, ppvObj: typing.Any) -> None:
        ...

    def Reduce(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, dwReduceHowFar: int, ppmkToLeft: System.Runtime.InteropServices.ComTypes.IMoniker, ppmkReduced: System.Runtime.InteropServices.ComTypes.IMoniker) -> None:
        ...

    def ComposeWith(self, pmkRight: System.Runtime.InteropServices.ComTypes.IMoniker, fOnlyIfNotGeneric: bool, ppmkComposite: System.Runtime.InteropServices.ComTypes.IMoniker) -> None:
        ...

    def Enum(self, fForward: bool, ppenumMoniker: System.Runtime.InteropServices.ComTypes.IEnumMoniker) -> None:
        ...

    def IsEqual(self, pmkOtherMoniker: System.Runtime.InteropServices.ComTypes.IMoniker) -> int:
        ...

    def Hash(self, pdwHash: int) -> None:
        ...

    def IsRunning(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmkToLeft: System.Runtime.InteropServices.ComTypes.IMoniker, pmkNewlyRunning: System.Runtime.InteropServices.ComTypes.IMoniker) -> int:
        ...

    def GetTimeOfLastChange(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmkToLeft: System.Runtime.InteropServices.ComTypes.IMoniker, pFileTime: System.Runtime.InteropServices.ComTypes.FILETIME) -> None:
        ...

    def Inverse(self, ppmk: System.Runtime.InteropServices.ComTypes.IMoniker) -> None:
        ...

    def CommonPrefixWith(self, pmkOther: System.Runtime.InteropServices.ComTypes.IMoniker, ppmkPrefix: System.Runtime.InteropServices.ComTypes.IMoniker) -> None:
        ...

    def RelativePathTo(self, pmkOther: System.Runtime.InteropServices.ComTypes.IMoniker, ppmkRelPath: System.Runtime.InteropServices.ComTypes.IMoniker) -> None:
        ...

    def GetDisplayName(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmkToLeft: System.Runtime.InteropServices.ComTypes.IMoniker, ppszDisplayName: str) -> None:
        ...

    def ParseDisplayName(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmkToLeft: System.Runtime.InteropServices.ComTypes.IMoniker, pszDisplayName: str, pchEaten: int, ppmkOut: System.Runtime.InteropServices.ComTypes.IMoniker) -> None:
        ...

    def IsSystemMoniker(self, pdwMksys: int) -> int:
        ...


class IRunningObjectTable(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Register(self, grfFlags: int, punkObject: typing.Any, pmkObjectName: System.Runtime.InteropServices.ComTypes.IMoniker) -> int:
        ...

    def Revoke(self, dwRegister: int) -> None:
        ...

    def IsRunning(self, pmkObjectName: System.Runtime.InteropServices.ComTypes.IMoniker) -> int:
        ...

    def GetObject(self, pmkObjectName: System.Runtime.InteropServices.ComTypes.IMoniker, ppunkObject: typing.Any) -> int:
        ...

    def NoteChangeTime(self, dwRegister: int, pfiletime: System.Runtime.InteropServices.ComTypes.FILETIME) -> None:
        ...

    def GetTimeOfLastChange(self, pmkObjectName: System.Runtime.InteropServices.ComTypes.IMoniker, pfiletime: System.Runtime.InteropServices.ComTypes.FILETIME) -> int:
        ...

    def EnumRunning(self, ppenumMoniker: System.Runtime.InteropServices.ComTypes.IEnumMoniker) -> None:
        ...


class ITypeLib2(System.Runtime.InteropServices.ComTypes.ITypeLib, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetTypeInfoCount(self) -> int:
        ...

    def GetTypeInfo(self, index: int, ppTI: System.Runtime.InteropServices.ComTypes.ITypeInfo) -> None:
        ...

    def GetTypeInfoType(self, index: int, pTKind: System.Runtime.InteropServices.ComTypes.TYPEKIND) -> None:
        ...

    def GetTypeInfoOfGuid(self, guid: System.Guid, ppTInfo: System.Runtime.InteropServices.ComTypes.ITypeInfo) -> None:
        ...

    def GetLibAttr(self, ppTLibAttr: System.IntPtr) -> None:
        ...

    def GetTypeComp(self, ppTComp: System.Runtime.InteropServices.ComTypes.ITypeComp) -> None:
        ...

    def GetDocumentation(self, index: int, strName: str, strDocString: str, dwHelpContext: int, strHelpFile: str) -> None:
        ...

    def IsName(self, szNameBuf: str, lHashVal: int) -> bool:
        ...

    def FindName(self, szNameBuf: str, lHashVal: int, ppTInfo: typing.List[System.Runtime.InteropServices.ComTypes.ITypeInfo], rgMemId: typing.List[int], pcFound: int) -> None:
        ...

    def ReleaseTLibAttr(self, pTLibAttr: System.IntPtr) -> None:
        ...

    def GetCustData(self, guid: System.Guid, pVarVal: typing.Any) -> None:
        ...

    def GetDocumentation2(self, index: int, pbstrHelpString: str, pdwHelpStringContext: int, pbstrHelpStringDll: str) -> None:
        ...

    def GetLibStatistics(self, pcUniqueNames: System.IntPtr, pcchUniqueNames: int) -> None:
        ...

    def GetAllCustData(self, pCustData: System.IntPtr) -> None:
        ...


class BIND_OPTS:
    """This class has no documentation."""

    @property
    def cbStruct(self) -> int:
        ...

    @cbStruct.setter
    def cbStruct(self, value: int):
        ...

    @property
    def grfFlags(self) -> int:
        ...

    @grfFlags.setter
    def grfFlags(self, value: int):
        ...

    @property
    def grfMode(self) -> int:
        ...

    @grfMode.setter
    def grfMode(self, value: int):
        ...

    @property
    def dwTickCountDeadline(self) -> int:
        ...

    @dwTickCountDeadline.setter
    def dwTickCountDeadline(self, value: int):
        ...


class IBindCtx(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def RegisterObjectBound(self, punk: typing.Any) -> None:
        ...

    def RevokeObjectBound(self, punk: typing.Any) -> None:
        ...

    def ReleaseBoundObjects(self) -> None:
        ...

    def SetBindOptions(self, pbindopts: System.Runtime.InteropServices.ComTypes.BIND_OPTS) -> None:
        ...

    def GetBindOptions(self, pbindopts: System.Runtime.InteropServices.ComTypes.BIND_OPTS) -> None:
        ...

    def GetRunningObjectTable(self, pprot: System.Runtime.InteropServices.ComTypes.IRunningObjectTable) -> None:
        ...

    def RegisterObjectParam(self, pszKey: str, punk: typing.Any) -> None:
        ...

    def GetObjectParam(self, pszKey: str, ppunk: typing.Any) -> None:
        ...

    def EnumObjectParam(self, ppenum: System.Runtime.InteropServices.ComTypes.IEnumString) -> None:
        ...

    def RevokeObjectParam(self, pszKey: str) -> int:
        ...


class IPersistFile(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def GetClassID(self, pClassID: System.Guid) -> None:
        ...

    def IsDirty(self) -> int:
        ...

    def Load(self, pszFileName: str, dwMode: int) -> None:
        ...

    def Save(self, pszFileName: str, fRemember: bool) -> None:
        ...

    def SaveCompleted(self, pszFileName: str) -> None:
        ...

    def GetCurFile(self, ppszFileName: str) -> None:
        ...


class TYPEFLAGS(System.Enum):
    """This class has no documentation."""

    TYPEFLAG_FAPPOBJECT = ...

    TYPEFLAG_FCANCREATE = ...

    TYPEFLAG_FLICENSED = ...

    TYPEFLAG_FPREDECLID = ...

    TYPEFLAG_FHIDDEN = ...

    TYPEFLAG_FCONTROL = ...

    TYPEFLAG_FDUAL = ...

    TYPEFLAG_FNONEXTENSIBLE = ...

    TYPEFLAG_FOLEAUTOMATION = ...

    TYPEFLAG_FRESTRICTED = ...

    TYPEFLAG_FAGGREGATABLE = ...

    TYPEFLAG_FREPLACEABLE = ...

    TYPEFLAG_FDISPATCHABLE = ...

    TYPEFLAG_FREVERSEBIND = ...

    TYPEFLAG_FPROXY = ...


class TYPEDESC:
    """This class has no documentation."""

    @property
    def lpValue(self) -> System.IntPtr:
        ...

    @lpValue.setter
    def lpValue(self, value: System.IntPtr):
        ...

    @property
    def vt(self) -> int:
        ...

    @vt.setter
    def vt(self, value: int):
        ...


class IDLFLAG(System.Enum):
    """This class has no documentation."""

    IDLFLAG_NONE = ...

    IDLFLAG_FIN = ...

    IDLFLAG_FOUT = ...

    IDLFLAG_FLCID = ...

    IDLFLAG_FRETVAL = ...


class IDLDESC:
    """This class has no documentation."""

    @property
    def dwReserved(self) -> System.IntPtr:
        ...

    @dwReserved.setter
    def dwReserved(self, value: System.IntPtr):
        ...

    @property
    def wIDLFlags(self) -> System.Runtime.InteropServices.ComTypes.IDLFLAG:
        ...

    @wIDLFlags.setter
    def wIDLFlags(self, value: System.Runtime.InteropServices.ComTypes.IDLFLAG):
        ...


class TYPEATTR:
    """This class has no documentation."""

    MEMBER_ID_NIL: int = ...

    @property
    def guid(self) -> System.Guid:
        ...

    @guid.setter
    def guid(self, value: System.Guid):
        ...

    @property
    def lcid(self) -> int:
        ...

    @lcid.setter
    def lcid(self, value: int):
        ...

    @property
    def dwReserved(self) -> int:
        ...

    @dwReserved.setter
    def dwReserved(self, value: int):
        ...

    @property
    def memidConstructor(self) -> int:
        ...

    @memidConstructor.setter
    def memidConstructor(self, value: int):
        ...

    @property
    def memidDestructor(self) -> int:
        ...

    @memidDestructor.setter
    def memidDestructor(self, value: int):
        ...

    @property
    def lpstrSchema(self) -> System.IntPtr:
        ...

    @lpstrSchema.setter
    def lpstrSchema(self, value: System.IntPtr):
        ...

    @property
    def cbSizeInstance(self) -> int:
        ...

    @cbSizeInstance.setter
    def cbSizeInstance(self, value: int):
        ...

    @property
    def typekind(self) -> System.Runtime.InteropServices.ComTypes.TYPEKIND:
        ...

    @typekind.setter
    def typekind(self, value: System.Runtime.InteropServices.ComTypes.TYPEKIND):
        ...

    @property
    def cFuncs(self) -> int:
        ...

    @cFuncs.setter
    def cFuncs(self, value: int):
        ...

    @property
    def cVars(self) -> int:
        ...

    @cVars.setter
    def cVars(self, value: int):
        ...

    @property
    def cImplTypes(self) -> int:
        ...

    @cImplTypes.setter
    def cImplTypes(self, value: int):
        ...

    @property
    def cbSizeVft(self) -> int:
        ...

    @cbSizeVft.setter
    def cbSizeVft(self, value: int):
        ...

    @property
    def cbAlignment(self) -> int:
        ...

    @cbAlignment.setter
    def cbAlignment(self, value: int):
        ...

    @property
    def wTypeFlags(self) -> System.Runtime.InteropServices.ComTypes.TYPEFLAGS:
        ...

    @wTypeFlags.setter
    def wTypeFlags(self, value: System.Runtime.InteropServices.ComTypes.TYPEFLAGS):
        ...

    @property
    def wMajorVerNum(self) -> int:
        ...

    @wMajorVerNum.setter
    def wMajorVerNum(self, value: int):
        ...

    @property
    def wMinorVerNum(self) -> int:
        ...

    @wMinorVerNum.setter
    def wMinorVerNum(self, value: int):
        ...

    @property
    def tdescAlias(self) -> System.Runtime.InteropServices.ComTypes.TYPEDESC:
        ...

    @tdescAlias.setter
    def tdescAlias(self, value: System.Runtime.InteropServices.ComTypes.TYPEDESC):
        ...

    @property
    def idldescType(self) -> System.Runtime.InteropServices.ComTypes.IDLDESC:
        ...

    @idldescType.setter
    def idldescType(self, value: System.Runtime.InteropServices.ComTypes.IDLDESC):
        ...


class FUNCKIND(System.Enum):
    """This class has no documentation."""

    FUNC_VIRTUAL = 0

    FUNC_PUREVIRTUAL = 1

    FUNC_NONVIRTUAL = 2

    FUNC_STATIC = 3

    FUNC_DISPATCH = 4


class CALLCONV(System.Enum):
    """This class has no documentation."""

    CC_CDECL = 1

    CC_MSCPASCAL = 2

    CC_PASCAL = ...

    CC_MACPASCAL = 3

    CC_STDCALL = 4

    CC_RESERVED = 5

    CC_SYSCALL = 6

    CC_MPWCDECL = 7

    CC_MPWPASCAL = 8

    CC_MAX = 9


class PARAMFLAG(System.Enum):
    """This class has no documentation."""

    PARAMFLAG_NONE = 0

    PARAMFLAG_FIN = ...

    PARAMFLAG_FOUT = ...

    PARAMFLAG_FLCID = ...

    PARAMFLAG_FRETVAL = ...

    PARAMFLAG_FOPT = ...

    PARAMFLAG_FHASDEFAULT = ...

    PARAMFLAG_FHASCUSTDATA = ...


class PARAMDESC:
    """This class has no documentation."""

    @property
    def lpVarValue(self) -> System.IntPtr:
        ...

    @lpVarValue.setter
    def lpVarValue(self, value: System.IntPtr):
        ...

    @property
    def wParamFlags(self) -> System.Runtime.InteropServices.ComTypes.PARAMFLAG:
        ...

    @wParamFlags.setter
    def wParamFlags(self, value: System.Runtime.InteropServices.ComTypes.PARAMFLAG):
        ...


class ELEMDESC:
    """This class has no documentation."""

    class DESCUNION:
        """This class has no documentation."""

        @property
        def idldesc(self) -> System.Runtime.InteropServices.ComTypes.IDLDESC:
            ...

        @idldesc.setter
        def idldesc(self, value: System.Runtime.InteropServices.ComTypes.IDLDESC):
            ...

        @property
        def paramdesc(self) -> System.Runtime.InteropServices.ComTypes.PARAMDESC:
            ...

        @paramdesc.setter
        def paramdesc(self, value: System.Runtime.InteropServices.ComTypes.PARAMDESC):
            ...

    @property
    def tdesc(self) -> System.Runtime.InteropServices.ComTypes.TYPEDESC:
        ...

    @tdesc.setter
    def tdesc(self, value: System.Runtime.InteropServices.ComTypes.TYPEDESC):
        ...

    @property
    def desc(self) -> System.Runtime.InteropServices.ComTypes.ELEMDESC.DESCUNION:
        ...

    @desc.setter
    def desc(self, value: System.Runtime.InteropServices.ComTypes.ELEMDESC.DESCUNION):
        ...


class FUNCDESC:
    """This class has no documentation."""

    @property
    def memid(self) -> int:
        ...

    @memid.setter
    def memid(self, value: int):
        ...

    @property
    def lprgscode(self) -> System.IntPtr:
        ...

    @lprgscode.setter
    def lprgscode(self, value: System.IntPtr):
        ...

    @property
    def lprgelemdescParam(self) -> System.IntPtr:
        ...

    @lprgelemdescParam.setter
    def lprgelemdescParam(self, value: System.IntPtr):
        ...

    @property
    def funckind(self) -> System.Runtime.InteropServices.ComTypes.FUNCKIND:
        ...

    @funckind.setter
    def funckind(self, value: System.Runtime.InteropServices.ComTypes.FUNCKIND):
        ...

    @property
    def invkind(self) -> System.Runtime.InteropServices.ComTypes.INVOKEKIND:
        ...

    @invkind.setter
    def invkind(self, value: System.Runtime.InteropServices.ComTypes.INVOKEKIND):
        ...

    @property
    def callconv(self) -> System.Runtime.InteropServices.ComTypes.CALLCONV:
        ...

    @callconv.setter
    def callconv(self, value: System.Runtime.InteropServices.ComTypes.CALLCONV):
        ...

    @property
    def cParams(self) -> int:
        ...

    @cParams.setter
    def cParams(self, value: int):
        ...

    @property
    def cParamsOpt(self) -> int:
        ...

    @cParamsOpt.setter
    def cParamsOpt(self, value: int):
        ...

    @property
    def oVft(self) -> int:
        ...

    @oVft.setter
    def oVft(self, value: int):
        ...

    @property
    def cScodes(self) -> int:
        ...

    @cScodes.setter
    def cScodes(self, value: int):
        ...

    @property
    def elemdescFunc(self) -> System.Runtime.InteropServices.ComTypes.ELEMDESC:
        ...

    @elemdescFunc.setter
    def elemdescFunc(self, value: System.Runtime.InteropServices.ComTypes.ELEMDESC):
        ...

    @property
    def wFuncFlags(self) -> int:
        ...

    @wFuncFlags.setter
    def wFuncFlags(self, value: int):
        ...


class VARKIND(System.Enum):
    """This class has no documentation."""

    VAR_PERINSTANCE = ...

    VAR_STATIC = ...

    VAR_CONST = ...

    VAR_DISPATCH = ...


class VARDESC:
    """This class has no documentation."""

    class DESCUNION:
        """This class has no documentation."""

        @property
        def oInst(self) -> int:
            ...

        @oInst.setter
        def oInst(self, value: int):
            ...

        @property
        def lpvarValue(self) -> System.IntPtr:
            ...

        @lpvarValue.setter
        def lpvarValue(self, value: System.IntPtr):
            ...

    @property
    def memid(self) -> int:
        ...

    @memid.setter
    def memid(self, value: int):
        ...

    @property
    def lpstrSchema(self) -> str:
        ...

    @lpstrSchema.setter
    def lpstrSchema(self, value: str):
        ...

    @property
    def desc(self) -> System.Runtime.InteropServices.ComTypes.VARDESC.DESCUNION:
        ...

    @desc.setter
    def desc(self, value: System.Runtime.InteropServices.ComTypes.VARDESC.DESCUNION):
        ...

    @property
    def elemdescVar(self) -> System.Runtime.InteropServices.ComTypes.ELEMDESC:
        ...

    @elemdescVar.setter
    def elemdescVar(self, value: System.Runtime.InteropServices.ComTypes.ELEMDESC):
        ...

    @property
    def wVarFlags(self) -> int:
        ...

    @wVarFlags.setter
    def wVarFlags(self, value: int):
        ...

    @property
    def varkind(self) -> System.Runtime.InteropServices.ComTypes.VARKIND:
        ...

    @varkind.setter
    def varkind(self, value: System.Runtime.InteropServices.ComTypes.VARKIND):
        ...


class EXCEPINFO:
    """This class has no documentation."""

    @property
    def wCode(self) -> int:
        ...

    @wCode.setter
    def wCode(self, value: int):
        ...

    @property
    def wReserved(self) -> int:
        ...

    @wReserved.setter
    def wReserved(self, value: int):
        ...

    @property
    def bstrSource(self) -> str:
        ...

    @bstrSource.setter
    def bstrSource(self, value: str):
        ...

    @property
    def bstrDescription(self) -> str:
        ...

    @bstrDescription.setter
    def bstrDescription(self, value: str):
        ...

    @property
    def bstrHelpFile(self) -> str:
        ...

    @bstrHelpFile.setter
    def bstrHelpFile(self, value: str):
        ...

    @property
    def dwHelpContext(self) -> int:
        ...

    @dwHelpContext.setter
    def dwHelpContext(self, value: int):
        ...

    @property
    def pvReserved(self) -> System.IntPtr:
        ...

    @pvReserved.setter
    def pvReserved(self, value: System.IntPtr):
        ...

    @property
    def pfnDeferredFillIn(self) -> System.IntPtr:
        ...

    @pfnDeferredFillIn.setter
    def pfnDeferredFillIn(self, value: System.IntPtr):
        ...

    @property
    def scode(self) -> int:
        ...

    @scode.setter
    def scode(self, value: int):
        ...


class FUNCFLAGS(System.Enum):
    """This class has no documentation."""

    FUNCFLAG_FRESTRICTED = ...

    FUNCFLAG_FSOURCE = ...

    FUNCFLAG_FBINDABLE = ...

    FUNCFLAG_FREQUESTEDIT = ...

    FUNCFLAG_FDISPLAYBIND = ...

    FUNCFLAG_FDEFAULTBIND = ...

    FUNCFLAG_FHIDDEN = ...

    FUNCFLAG_FUSESGETLASTERROR = ...

    FUNCFLAG_FDEFAULTCOLLELEM = ...

    FUNCFLAG_FUIDEFAULT = ...

    FUNCFLAG_FNONBROWSABLE = ...

    FUNCFLAG_FREPLACEABLE = ...

    FUNCFLAG_FIMMEDIATEBIND = ...


class VARFLAGS(System.Enum):
    """This class has no documentation."""

    VARFLAG_FREADONLY = ...

    VARFLAG_FSOURCE = ...

    VARFLAG_FBINDABLE = ...

    VARFLAG_FREQUESTEDIT = ...

    VARFLAG_FDISPLAYBIND = ...

    VARFLAG_FDEFAULTBIND = ...

    VARFLAG_FHIDDEN = ...

    VARFLAG_FRESTRICTED = ...

    VARFLAG_FDEFAULTCOLLELEM = ...

    VARFLAG_FUIDEFAULT = ...

    VARFLAG_FNONBROWSABLE = ...

    VARFLAG_FREPLACEABLE = ...

    VARFLAG_FIMMEDIATEBIND = ...


class SYSKIND(System.Enum):
    """This class has no documentation."""

    SYS_WIN16 = 0

    SYS_WIN32 = ...

    SYS_MAC = ...

    SYS_WIN64 = ...


class LIBFLAGS(System.Enum):
    """This class has no documentation."""

    LIBFLAG_FRESTRICTED = ...

    LIBFLAG_FCONTROL = ...

    LIBFLAG_FHIDDEN = ...

    LIBFLAG_FHASDISKIMAGE = ...


class TYPELIBATTR:
    """This class has no documentation."""

    @property
    def guid(self) -> System.Guid:
        ...

    @guid.setter
    def guid(self, value: System.Guid):
        ...

    @property
    def lcid(self) -> int:
        ...

    @lcid.setter
    def lcid(self, value: int):
        ...

    @property
    def syskind(self) -> System.Runtime.InteropServices.ComTypes.SYSKIND:
        ...

    @syskind.setter
    def syskind(self, value: System.Runtime.InteropServices.ComTypes.SYSKIND):
        ...

    @property
    def wMajorVerNum(self) -> int:
        ...

    @wMajorVerNum.setter
    def wMajorVerNum(self, value: int):
        ...

    @property
    def wMinorVerNum(self) -> int:
        ...

    @wMinorVerNum.setter
    def wMinorVerNum(self, value: int):
        ...

    @property
    def wLibFlags(self) -> System.Runtime.InteropServices.ComTypes.LIBFLAGS:
        ...

    @wLibFlags.setter
    def wLibFlags(self, value: System.Runtime.InteropServices.ComTypes.LIBFLAGS):
        ...


class IEnumVARIANT(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Next(self, celt: int, rgVar: typing.List[System.Object], pceltFetched: System.IntPtr) -> int:
        ...

    def Skip(self, celt: int) -> int:
        ...

    def Reset(self) -> int:
        ...

    def Clone(self) -> System.Runtime.InteropServices.ComTypes.IEnumVARIANT:
        ...


