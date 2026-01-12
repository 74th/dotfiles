#!/usr/local/bin/system-python
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args:
        print("error: project name is required", file=sys.stderr)
        sys.exit(1)

    project_name = args[0]

    origin_ch32fun_dir = Path("~/ghq/github.com/cnlohr/ch32fun").expanduser()
    if not origin_ch32fun_dir.exists():
        print(
            f"error: origin ch32fun directory not found: {origin_ch32fun_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    current_dir = Path.cwd()

    (current_dir / "ch32fun").mkdir(exist_ok=True)
    (current_dir / ".vscode").mkdir(exist_ok=True)
    (current_dir / "misc").mkdir(exist_ok=True)

    copied_files: list[tuple[str, str]] = [
        # ("examples/template/.vscode/c_cpp_properties.json", ".vscode"),
        ("examples/template/.vscode/settings.json", ".vscode"),
        # ("examples/template/Makefile", ""),
        ("examples/template/funconfig.h", ""),
        ("ch32fun/ch32fun.c", "ch32fun"),
        ("ch32fun/ch32fun.h", "ch32fun"),
        ("ch32fun/ch32fun.ld", "ch32fun"),
        # ("ch32fun/ch32fun.mk", "ch32fun"),
        ("ch32fun/ch32v003fun-bootloader.ld", "ch32fun"),
        ("ch32fun/ch32v003hw.h", "ch32fun"),
        ("extralibs/ch32v003_GPIO_branchless.h", "ch32fun"),
        ("LICENSE", "ch32fun"),
        ("misc/CH32V003xx.svd", "misc"),
        ("misc/LIBGCC_LICENSE", "misc"),
        ("misc/libgcc.a", "misc"),
    ]

    for src_rel_path, dest_subdir in copied_files:
        src_path = origin_ch32fun_dir / src_rel_path
        dest_path = current_dir / dest_subdir / Path(src_rel_path).name
        if not src_path.exists():
            print(f"error: source file not found: {src_path}", file=sys.stderr)
            sys.exit(1)
        dest_path.write_bytes(src_path.read_bytes())

    (current_dir / f"{project_name}.c").write_bytes(
        (origin_ch32fun_dir / "examples/template/template.c").read_bytes()
    )

    # Makefile
    makefile = (origin_ch32fun_dir / "examples/template/Makefile").read_text()
    makefile = makefile.replace(
        "TARGET:=template",
        f"""TARGET:={project_name}
CH32FUN=./ch32fun
MINICHLINK:=$(shell dirname $(shell which minichlink))""",
    )
    makefile = makefile.replace(
        "include ../../ch32fun/ch32fun.mk", "include ./ch32fun/ch32fun.mk"
    )
    (current_dir / "Makefile").write_text(makefile)

    # ch32fun.mk
    ch32funmk = (origin_ch32fun_dir / "ch32fun/ch32fun.mk").read_text()
    ch32funmk = ch32funmk.replace(
        "	make -C $(MINICHLINK) all", "#	make -C $(MINICHLINK) all"
    )
    (current_dir / "ch32fun" / "ch32fun.mk").write_text(ch32funmk)

    # .vscode/c_cpp_properties.json
    # Mac用の設定を追加したいので、全文保持する
    c_cpp_properties = """{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**",
                "${workspaceFolder}/ch32fun"
            ],
            "defines": [],
            "compilerPath": "/usr/bin/clang",
            "cppStandard": "c++20",
            "intelliSenseMode": "linux-clang-x64",
            "compilerArgs": [
                "-DCH32V003FUN_BASE"
            ],
            "configurationProvider": "ms-vscode.makefile-tools"
        },
        {
            "name": "macos",
            "includePath": [
                "${workspaceFolder}/**",
                "${workspaceFolder}/ch32fun"
            ],
            "defines": [
                "CH32V003",
                "CH32V003FUN_BASE"
            ],
            "compilerPath": "/opt/homebrew/bin/riscv64-unknown-elf-gcc",
            "cStandard": "gnu11",
            "cppStandard": "c++20",
            "intelliSenseMode": "linux-gcc-x64",
            "compilerArgs": [
                "-DCH32V003FUN_BASE"
            ],
            "configurationProvider": "ms-vscode.makefile-tools"
        },
        {
            "name": "Win32",
            "includePath": [
                "${workspaceFolder}/**",
                "${workspaceFolder}/ch32fun",
                "${workspaceFolder}/lib",
                "${workspaceFolder}/rv003usb"
            ],
            "defines": [
                "CH32V003",
                "CH32V003FUN_BASE"
            ],
            "compilerPath": "riscv64-unknown-elf-gcc-10.1.0.exe",
            "cppStandard": "c++20",
            "compilerArgs": [
                "-DCH32V003FUN_BASE"
            ],
            "configurationProvider": "ms-vscode.makefile-tools"
        }
    ],
    "version": 4,
    "enableConfigurationSquiggles": true
}"""
    (current_dir / ".vscode" / "c_cpp_properties.json").write_text(c_cpp_properties)


if __name__ == "__main__":
    main()
