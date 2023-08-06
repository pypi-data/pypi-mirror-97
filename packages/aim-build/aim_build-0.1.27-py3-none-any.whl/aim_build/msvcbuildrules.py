from aim_build.typedefs import StringList


def add_compile(nfw):
    command = f"$compiler $defines $includes /showIncludes $flags -c $in /Fo$out"
    nfw.rule(
        name="compile",
        description="Compile source files to object files",
        deps="msvc",
        command=command,
    )
    nfw.newline()


def add_ar(nfw):
    nfw.rule(
        name="ar",
        description="Combine object files into an archive",
        command="llvm-ar cr $out $in",
    )
    nfw.newline()


def add_exe(nfw):
    command = (
        f"$compiler $defines $flags $includes $in /link /out:$exe_name $linker_args"
    )
    nfw.rule(name="exe", description="Build an executable.", command=command)
    nfw.newline()


def add_shared(nfw):

    command = f"$compiler $defines $flags $includes $in /link /DLL /out:$lib_name $linker_args"
    nfw.rule(name="shared", description="Build an shared library.", command=command)
    nfw.newline()
