from pathlib import Path

from PySide6.QtCore import Signal, QObject

from ...apk.extract import extract_apk
from ...apk.build import build_apk
from ...apk.zipalign import zipalign_apk
from ...apk.sign import sign_apk

from ...apk.packs.decrypt import decrypt_packs
from ...apk.packs.encrypt import encrypt_pack
from ...apk.server.downloader import download_server_files,process_server_files
from ...apk.packs.required_files import get_required_files
from ...apk.edit_xml import edit_manifest
from ...apk.replace_icon import replace_icon

# True = decrypt only the files in decrypt_specifics
# False = decrypt every pack
DECRYPT_SPECIFICS = True
SKIP_SERVER = True

class RandomizeThread(QObject):

    finished = Signal()
    error = Signal(str)
    log = Signal(str)
    html_log = Signal(str)

    def __init__(self, apk_path, config):
        super().__init__()

        self.apk_path = apk_path
        self.config = config

    def run(self):
        try:
            self.randomize_process()
            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))

    def randomize_process(self):

        apk_path = self.apk_path
        config = self.config

        workspace = Path("workspace")
        decoded_directory = workspace / "decoded"
        decrypted_directory = workspace / "decrypted"
        rebuilt_apk = workspace / "rebuilt.apk"
        aligned_apk = workspace / "aligned.apk"
        signed_apk = workspace / "signed.apk"

        self.log.emit("Extracting APK...")

        extract_apk(apk_path,decoded_directory,)

        pack_paths = [
            path
            for path in decoded_directory.rglob("*.pack")
            if "_" not in path.stem
        ]

        self.log.emit(
            f"\nFound {len(pack_paths)} pack files:"
        )

        for pack in pack_paths:
            print(f"  {pack}")

        if not pack_paths:
            raise RuntimeError("No .pack files found")

        requirements = get_required_files(config)

        self.log.emit("Decrypting Local packs...")

        if DECRYPT_SPECIFICS:
            decrypt_packs(
                pack_paths=pack_paths,
                cc="en",
                output_directory=decrypted_directory / "vanilla_files",
                wanted_files=requirements["local"],
                use_pack_directory=False,
            )
        else:
            decrypt_packs(
                pack_paths=pack_paths,
                cc="en",
                output_directory=decrypted_directory,
            )

        server_directory = workspace / "en_server"

        lib_path = (
            decoded_directory
            / "lib"
            / "x86_64"
            / "libnative-lib.so"
        )

        tsv_paths = sorted(decoded_directory.rglob("download_*.tsv"))

        self.log.emit(f"\nFound libnative.so: {lib_path}")

        self.log.emit(f"Found {len(tsv_paths)} server TSV files:")

        self.log.emit("Decrypting server packs...")

        for tsv in tsv_paths:
           print(f"  {tsv}")

        ########## DECRYPT SERVER FILES ##########################################################################

        if not SKIP_SERVER:

            if not DECRYPT_SPECIFICS:

                download_server_files(
                    lib_path=lib_path,
                    tsv_paths=tsv_paths,
                    country_code="en",
                    output_directory=server_directory,
                )

                server_pack_paths = list(
                    server_directory.rglob("*.pack")
                )

                self.log.emit(
                    f"\nFound {len(server_pack_paths)} server pack files:"
                )

                for pack in server_pack_paths:
                    self.log.emit(f"  {pack}")

                decrypt_packs(
                    pack_paths=server_pack_paths,
                    cc="en",
                    output_directory=decrypted_directory / "server",
                )

            else:

                process_server_files(
                    lib_path=lib_path,
                    tsv_paths=tsv_paths,
                    country_code="en",
                    server_directory=server_directory,
                    output_directory=decrypted_directory / "vanilla_files",
                    wanted_files=requirements["server"],
                    use_pack_directory=False,
                    log=self.log.emit,
                )

        pack_path = (
            decoded_directory
            / "assets"
            / "DownloadLocal.pack"
        )

        pack_name = pack_path.stem

        game_files_directory = (decrypted_directory/pack_name)

        game_files_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # TODO RANDOMIZER CODE

        self.log.emit(
            f"\nEncrypting: {pack_name}"
        )

        encrypt_pack(
            game_files_dir=game_files_directory,
            pack_name=pack_name,
            output_directory=pack_path.parent,
            cc="en",
        )


        # APK ICON
        self.log.emit("Replacing app icon")
        replace_icon()

        # EDIT XML
        self.log.emit("Setting mod ID")
        edit_manifest(config["mod"]["id"])


        self.log.emit("Building APK")

        build_apk(
            decoded_directory,
            rebuilt_apk,
        )

        self.log.emit("Zipaligning APK")

        zipalign_apk(rebuilt_apk,aligned_apk,)

        self.log.emit("Signing APK")

        sign_apk(aligned_apk,signed_apk,)

        self.html_log.emit('<span style="color: lime;">Randomization Complete.</span>')
        self.log.emit(f"Signed APK: {signed_apk}")
        self.html_log.emit('<span style="color: orange;">MAKE SURE TO SAVE YOUR CONFIG IF YOU HAVENT!</span>')