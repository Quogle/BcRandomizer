from pathlib import Path
import subprocess


TOOLS_DIR = Path(__file__).resolve().parents[3]/"resources"/"tools"
APKTOOL_PATH = TOOLS_DIR/"apktool.jar"


def extract_apk(apk_path,output_directory,):
    """
    Decode an APK using APKTool.

    Returns the path to the decoded APK directory.
    """

    apk_path = Path(apk_path)
    output_directory = Path(output_directory)

    if not apk_path.is_file():
        raise FileNotFoundError(
            f"APK not found: {apk_path}"
        )

    if not APKTOOL_PATH.is_file():
        raise FileNotFoundError(
            f"APKTool not found: {APKTOOL_PATH}"
        )

    output_directory.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        "java",
        "-jar",
        str(APKTOOL_PATH),
        "d",
        str(apk_path),
        "-o",
        str(output_directory),
        "-f",
    ]

    subprocess.run(
        command,
        check=True,
    )

    return output_directory