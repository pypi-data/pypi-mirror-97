import typing

import System
import System.Collections.Generic
import System.IO
import System.Reflection
import System.Runtime.Loader

System_AssemblyLoadEventHandler = typing.Any
System_ResolveEventHandler = typing.Any


class AssemblyLoadContext(System.Object):
    """This class has no documentation."""

    class ContextualReflectionScope(System.IDisposable):
        """Opaque disposable struct used to restore CurrentContextualReflectionContext"""

        def Dispose(self) -> None:
            ...

    @property
    def Assemblies(self) -> System.Collections.Generic.IEnumerable[System.Reflection.Assembly]:
        ...

    @property
    def ResolvingUnmanagedDll(self) -> typing.List[typing.Callable[[System.Reflection.Assembly, str], System.IntPtr]]:
        ...

    @ResolvingUnmanagedDll.setter
    def ResolvingUnmanagedDll(self, value: typing.List[typing.Callable[[System.Reflection.Assembly, str], System.IntPtr]]):
        ...

    @property
    def Resolving(self) -> typing.List[typing.Callable[[System.Runtime.Loader.AssemblyLoadContext, System.Reflection.AssemblyName], System.Reflection.Assembly]]:
        ...

    @Resolving.setter
    def Resolving(self, value: typing.List[typing.Callable[[System.Runtime.Loader.AssemblyLoadContext, System.Reflection.AssemblyName], System.Reflection.Assembly]]):
        ...

    @property
    def Unloading(self) -> typing.List[typing.Callable[[System.Runtime.Loader.AssemblyLoadContext], None]]:
        ...

    @Unloading.setter
    def Unloading(self, value: typing.List[typing.Callable[[System.Runtime.Loader.AssemblyLoadContext], None]]):
        ...

    AssemblyLoad: typing.List[System_AssemblyLoadEventHandler]

    TypeResolve: typing.List[System_ResolveEventHandler]

    ResourceResolve: typing.List[System_ResolveEventHandler]

    AssemblyResolve: typing.List[System_ResolveEventHandler]

    Default: System.Runtime.Loader.AssemblyLoadContext

    @property
    def IsCollectible(self) -> bool:
        ...

    @property
    def Name(self) -> str:
        ...

    All: System.Collections.Generic.IEnumerable[System.Runtime.Loader.AssemblyLoadContext]

    CurrentContextualReflectionContext: System.Runtime.Loader.AssemblyLoadContext
    """Nullable current AssemblyLoadContext used for context sensitive reflection APIs"""

    @property
    def NativeALC(self) -> System.IntPtr:
        ...

    @typing.overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, isCollectible: bool) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, name: str, isCollectible: bool = False) -> None:
        ...

    def ToString(self) -> str:
        ...

    @staticmethod
    def GetAssemblyName(assemblyPath: str) -> System.Reflection.AssemblyName:
        ...

    def Load(self, assemblyName: System.Reflection.AssemblyName) -> System.Reflection.Assembly:
        """This method is protected."""
        ...

    def LoadFromAssemblyName(self, assemblyName: System.Reflection.AssemblyName) -> System.Reflection.Assembly:
        ...

    def LoadFromAssemblyPath(self, assemblyPath: str) -> System.Reflection.Assembly:
        ...

    def LoadFromNativeImagePath(self, nativeImagePath: str, assemblyPath: str) -> System.Reflection.Assembly:
        ...

    @typing.overload
    def LoadFromStream(self, assembly: System.IO.Stream) -> System.Reflection.Assembly:
        ...

    @typing.overload
    def LoadFromStream(self, assembly: System.IO.Stream, assemblySymbols: System.IO.Stream) -> System.Reflection.Assembly:
        ...

    def LoadUnmanagedDllFromPath(self, unmanagedDllPath: str) -> System.IntPtr:
        """This method is protected."""
        ...

    def LoadUnmanagedDll(self, unmanagedDllName: str) -> System.IntPtr:
        """This method is protected."""
        ...

    def Unload(self) -> None:
        ...

    @typing.overload
    def EnterContextualReflection(self) -> System.Runtime.Loader.AssemblyLoadContext.ContextualReflectionScope:
        """
        Enter scope using this AssemblyLoadContext for ContextualReflection
        
        :returns: A disposable ContextualReflectionScope for use in a using block.
        """
        ...

    @staticmethod
    @typing.overload
    def EnterContextualReflection(activating: System.Reflection.Assembly) -> System.Runtime.Loader.AssemblyLoadContext.ContextualReflectionScope:
        """
        Enter scope using this AssemblyLoadContext for ContextualReflection
        
        :param activating: Set CurrentContextualReflectionContext to the AssemblyLoadContext which loaded activating.
        :returns: A disposable ContextualReflectionScope for use in a using block.
        """
        ...

    @staticmethod
    def GetLoadContext(assembly: System.Reflection.Assembly) -> System.Runtime.Loader.AssemblyLoadContext:
        ...

    def SetProfileOptimizationRoot(self, directoryPath: str) -> None:
        ...

    def StartProfileOptimization(self, profile: str) -> None:
        ...


class AssemblyDependencyResolver(System.Object):
    """This class has no documentation."""

    def __init__(self, componentAssemblyPath: str) -> None:
        ...

    def ResolveAssemblyToPath(self, assemblyName: System.Reflection.AssemblyName) -> str:
        ...

    def ResolveUnmanagedDllToPath(self, unmanagedDllName: str) -> str:
        ...


