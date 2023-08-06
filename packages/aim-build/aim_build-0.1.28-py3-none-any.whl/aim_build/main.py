import argparse
import subprocess
import sys
import zipfile
from ninja_syntax import Writer
from typing import Optional
import toml
from aim_build.common import DEMO_ZIP_FILE_NAME
from aim_build import gccbuilds
from aim_build import msvcbuilds
from aim_build import osxbuilds
from aim_build.schema import target_schema
from aim_build.utils import *
from aim_build.version import __version__
from aim_build.gccbuildrules import add_compile,add_ar,add_exe,add_shared


def find_build(build_name, builds):
    for build in builds:
        if build["name"] == build_name:
            return build
    else:
        raise RuntimeError(f"Failed to find build with name: {build_name}")


def run_ninja(working_dir, build_name):
    command = ["ninja", "-C", str(working_dir), "-v", build_name]
    command_str = " ".join(command)
    # print(f'Executing "{command_str}"')

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    for line in iter(process.stdout.readline, b""):
        sys.stdout.write(line.decode("utf-8"))
    for line in iter(process.stderr.readline, b""):
        sys.stderr.write(line.decode("utf-8"))


def entry():
    # print("DEV")
    script_path = Path(__file__).parent

    # TODO: Get version automatically from the pyproject.toml file.
    parser = argparse.ArgumentParser(prog="aim", description=f"Version {__version__}")

    parser.add_argument("-v", "--version", action="version", version=__version__)
    sub_parser = parser.add_subparsers(dest="command", help="Commands")

    build_parser = sub_parser.add_parser(
        "list", help="displays the builds for the target"
    )
    build_parser.add_argument(
        "--target", type=str, required=True, help="path to target file directory"
    )

    init_parser = sub_parser.add_parser("init", help="creates a project structure")
    init_parser.add_argument(
        "--demo-files",
        help="create additional demo files",
        action="store_true"
    )

    build_parser = sub_parser.add_parser("build", help="executes a build")
    build_parser.add_argument("build", type=str, help="the build name")

    build_parser.add_argument(
        "--target", type=str, required=True, help="path to target file directory"
    )

    build_parser.add_argument(
        "--skip-ninja-regen",
        help="by-pass the ninja file generation step",
        action="store_true",
    )

    build_parser.add_argument(
        "--profile-build",
        help="forwards -ftime-trace to the compiler for emitting build profile information. View using chome://tracing.",
        action="store_true",
    )

    build_parser.add_argument(
       "--args",
        help="additional arguments forwarded to the compiler",
        nargs="*"
    )

    build_parser = sub_parser.add_parser(
        "clobber", help="deletes all build artifacts for the specified target"
    )
    build_parser.add_argument(
        "--target", type=str, required=True, help="path to target file directory"
    )
    args = parser.parse_args()
    mode = args.command
    if mode == "init":
        if args.demo_files:
            print("Initialising from demo project...")
            relative_dir = "demo/Calculator"
        else:
            relative_dir = "demo/Empty"

        zip_path = script_path / f"{DEMO_ZIP_FILE_NAME}"

        assert zip_path.exists(), f"Failed to find demo zip files: {str(zip_path)}"
        zip_file = zipfile.ZipFile(str(zip_path))

        run_init(zip_file, relative_dir)
    elif mode == "build":
        forwarding_args = [] if args.args is None else args.args
        if args.profile_build and "-ftime-trace" not in forwarding_args:
                forwarding_args.append("-ftime-trace")
        run_build(args.build, args.target, args.skip_ninja_regen, forwarding_args)
    elif mode == "list":
        run_list(args.target)
    elif mode == "clobber":
        run_clobber(args.target)
    else:
        import sys

        parser.print_help(sys.stdout)


def run_init(demo_zip: zipfile.ZipFile, subdir_name):
    project_dir = Path().cwd()
    dirs = ["include", "src", "lib", "tests", "builds"]
    dirs = [project_dir / x for x in dirs]
    print(f"Creating directories...")
    for a_dir in dirs:
        print(f"\t{str(a_dir)}")
        a_dir.mkdir(exist_ok=True)

    if demo_zip:
        print("Initialising from demo project...")
        for file_name in demo_zip.namelist():
            file_name = Path(file_name)
            if not str(file_name).startswith(subdir_name):
                continue

            with demo_zip.open(str(file_name)) as the_file:
                relative_path = file_name.relative_to(subdir_name)
                sys.stdout.write(f"\tCreating {str(relative_path)} ...")
                if relative_path.exists():
                    print("warning, file already exists.")
                    continue
                print("okay")

                relative_path.parent.mkdir(parents=True, exist_ok=True)
                relative_path.touch()
                relative_path.write_bytes(the_file.read())


def generate_flat_ninja_file(build_name, parsed_toml, project_dir, build_dir,args):
    compiler = parsed_toml["compiler"]
    archiver = parsed_toml["ar"]
    frontend = parsed_toml["compilerFrontend"]
    flags = parsed_toml.get("flags", [])
    flags = args + flags
    defines = parsed_toml.get("defines", [])
    project_ninja = build_dir / "build.ninja"

    builds = parsed_toml["builds"]

    with project_ninja.open("w+") as project_fd:
        project_writer = Writer(project_fd)
        # project_writer.include(str(build_dir / "rules.ninja"))
        add_compile(project_writer)
        add_ar(project_writer)
        add_exe(project_writer)
        add_shared(project_writer)

        for build_info in builds:
            current_build = build_info
            current_build["directory"] = project_dir
            current_build["build_dir"] = build_dir
            current_build["global_flags"] = flags
            current_build["global_defines"] = defines
            current_build["global_compiler"] = compiler
            current_build["global_archiver"] = archiver


            if frontend == "msvc":
                # builder = msvcbuilds.MSVCBuilds(compiler, compiler_c, archiver)
                assert False, "MSVC frontend is currently not supported."
            elif frontend == "osx":
                builder = osxbuilds.OsxBuilds()
            else:
                builder = gccbuilds.GCCBuilds()

            builder.build(build_info, parsed_toml, project_writer)


def run_build(build_name, target_path, skip_ninja_regen, args):
    print("Running build...")
    # build_dir = Path().cwd()
    build_dir = Path()

    if target_path:
        target_path = Path(target_path)
        if target_path.is_absolute():
            build_dir = target_path
        else:
            build_dir = build_dir / Path(target_path)

    toml_path = build_dir / "target.toml"

    with toml_path.open("r") as toml_file:
        parsed_toml = toml.loads(toml_file.read())

        builds = parsed_toml["builds"]
        the_build = find_build(build_name, builds)
        root_dir = parsed_toml["projectRoot"]
        project_dir = (build_dir / root_dir)
        assert project_dir.exists(), f"{str(project_dir)} does not exist."

        try:
            target_schema(parsed_toml, project_dir)
        except RuntimeError as e:
            print(f"Error: {e.args[0]}")
            exit(-1)

        if not skip_ninja_regen:
            print("Generating ninja files...")
            generate_flat_ninja_file(build_name, parsed_toml, project_dir, build_dir, args)
            with (build_dir.resolve() / "compile_commands.json").open("w+") as cc:
                command = ["ninja", "-C", str(build_dir.resolve()), "-t", "compdb"]
                subprocess.run(command, stdout=cc)

        run_ninja(build_dir, the_build["name"])


def run_list(target_path):
    build_dir = Path().cwd()

    if target_path:
        target_path = Path(target_path)
        if target_path.is_absolute():
            build_dir = target_path
        else:
            build_dir = build_dir / Path(target_path)

    toml_path = build_dir / "target.toml"

    with toml_path.open("r") as toml_file:
        parsed_toml = toml.loads(toml_file.read())

        builds = parsed_toml["builds"]

        frontend = parsed_toml["compilerFrontend"]

        if frontend == "msvc":
            # builder = msvcbuilds.MSVCBuilds("", "", "")
            assert False, "MSVC frontend is currently not supported."
        elif frontend == "osx":
            builder = osxbuilds.OsxBuilds()
        else:
            builder = gccbuilds.GCCBuilds()

        header = ["Item", "Name", "Build Rule", "Output Name"]
        table = []

        for number, build in enumerate(builds):
            if build["buildRule"] in ["libraryReference", "headerOnly"]:
                output_name = "n.a."
            else:
                output_name = builder.add_naming_convention(
                    build["outputName"], build["buildRule"]
                )
            row = [number, build["name"], build["buildRule"], output_name]
            table.append(row)

        from tabulate import tabulate

        print()
        print(tabulate(table, header))
        print()


def run_clobber(target_path):
    build_dir = Path().cwd()

    if target_path:
        target_path = Path(target_path)
        if target_path.is_absolute():
            build_dir = target_path
        else:
            build_dir = build_dir / Path(target_path)

    assert (build_dir / "target.toml").exists(), (
        f"Failed to find target.toml file in {str(build_dir)}.\n"
        "You might be trying to delete a directory that you want to keep."
    )

    print(f"Clobbering {str(build_dir)}...")

    dir_contents = build_dir.glob("*")
    for item in dir_contents:
        if item.name != "target.toml":
            print(f"Deleting {item.name}")
            if item.is_dir():
                import shutil

                shutil.rmtree(str(item))
            else:
                os.remove(str(item))


if __name__ == "__main__":
    entry()
