from pathlib import Path
import subprocess

TOOLS_DIR = Path(__file__).resolve().parents[3] / "tools"

APKSIGNER_PATH = (
    TOOLS_DIR/"windows"/"build-tools"/"apksigner.bat"
)

KEYSTORE_PATH = (
    TOOLS_DIR/"keystore"/"bcrando.jks"
)


def sign_apk(input_apk,output_apk):

    input_apk = Path(input_apk)
    output_apk = Path(output_apk)

    if not input_apk.is_file():
        raise FileNotFoundError(
            f"APK not found: {input_apk}"
        )

    if not APKSIGNER_PATH.is_file():
        raise FileNotFoundError(
            f"apksigner not found: {APKSIGNER_PATH}"
        )

    if not KEYSTORE_PATH.is_file():
        raise FileNotFoundError(
            f"Keystore not found: {KEYSTORE_PATH}"
        )

    output_apk.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        str(APKSIGNER_PATH),
        "sign",
        "--ks",
        str(KEYSTORE_PATH),
        "--ks-pass",
        "pass:modkey",
        "--out",
        str(output_apk),
        str(input_apk),
    ]

    subprocess.run(
        command,
        check=True,
    )

    return output_apk