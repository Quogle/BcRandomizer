from pathlib import Path
import subprocess


TOOLS_DIR = Path(__file__).resolve().parents[3] / "tools"
APKTOOL_PATH = TOOLS_DIR/"apktool.jar"


def build_apk(decoded_directory,output_apk):

    decoded_directory = Path(decoded_directory)
    output_apk = Path(output_apk)

    if not decoded_directory.is_dir():
        raise FileNotFoundError(
            f"Decoded APK directory not found: {decoded_directory}"
        )

    if not APKTOOL_PATH.is_file():
        raise FileNotFoundError(
            f"APKTool not found: {APKTOOL_PATH}"
        )

    output_apk.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        "java",
        "-jar",
        str(APKTOOL_PATH),
        "b",
        str(decoded_directory),
        "-o",
        str(output_apk),
    ]

    subprocess.run(
        command,
        check=True,
    )

    return output_apk