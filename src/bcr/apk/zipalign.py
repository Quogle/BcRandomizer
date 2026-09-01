from pathlib import Path
import subprocess

TOOLS_DIR = Path(__file__).resolve().parents[3] / "tools"
ZIPALIGN_PATH = TOOLS_DIR/"windows"/"build-tools"/"zipalign.exe"


def zipalign_apk(input_apk,output_apk):

    input_apk = Path(input_apk)
    output_apk = Path(output_apk)

    if not input_apk.is_file():
        raise FileNotFoundError(
            f"APK not found: {input_apk}"
        )

    if not ZIPALIGN_PATH.is_file():
        raise FileNotFoundError(
            f"zipalign not found: {ZIPALIGN_PATH}"
        )

    output_apk.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        str(ZIPALIGN_PATH),
        "-f",
        "4",
        str(input_apk),
        str(output_apk),
    ]

    subprocess.run(
        command,
        check=True,
    )

    return output_apk