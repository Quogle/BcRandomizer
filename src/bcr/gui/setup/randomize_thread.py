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
from ...config import paths as internalPaths
from ...randomizer.gameplay.zombie_fix import fix_zombie
import traceback
from ...randomizer import file_local

#from ...randomizer import randomize as randomize_function

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

        self.apk_path = apk_path #idk where to change this path if it should be changed at all
        self.config = config

    def run(self):
        try:
            self.randomize_process()
            self.finished.emit()

        except Exception:
            traceback.print_exc()
            self.error.emit(traceback.format_exc())

    def randomize_process(self):

        apk_path = self.apk_path
        config = self.config

        signed_apk = Path(f"{self.config['mod']['id']}.apk")

        if EXTRACT_APK:
            self.log.emit("Extracting APK...")
            extract_apk(apk_path,internalPaths.DECOMPILED,)

        pack_paths = [
            path
            for path in internalPaths.DECOMPILED.rglob("*.pack")
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
                output_directory=internalPaths.DECRYPTED / "vanilla_files",
                wanted_files=requirements["local"],
                use_pack_directory=False,
            )
        else:
            decrypt_packs(
                pack_paths=pack_paths,
                cc="en",
                output_directory=internalPaths.DECRYPTED,
            )

        tsv_paths = sorted(internalPaths.DECOMPILED.rglob("download_*.tsv"))

        self.log.emit(f"\nFound libnative.so: {internalPaths.LIBPATH}")

        self.log.emit(f"Found {len(tsv_paths)} server TSV files:")

        self.log.emit("Decrypting server packs...")

        for tsv in tsv_paths:
           print(f"  {tsv}")

        ########## DECRYPT SERVER FILES ##########################################################################

        if not SKIP_SERVER:

            if not DECRYPT_SPECIFICS:

                download_server_files(
                    lib_path=internalPaths.LIBPATH,
                    tsv_paths=tsv_paths,
                    country_code="en",
                    output_directory=internalPaths.SERVERDIRECTORY,
                )

                server_pack_paths = list(
                    internalPaths.SERVERDIRECTORY.rglob("*.pack")
                )

                self.log.emit(
                    f"\nFound {len(server_pack_paths)} server pack files:"
                )

                for pack in server_pack_paths:
                    self.log.emit(f"  {pack}")

                decrypt_packs(
                    pack_paths=server_pack_paths,
                    cc="en",
                    output_directory=internalPaths.SERVERFILES,
                )

            else:

                process_server_files(
                    lib_path=internalPaths.LIBPATH,
                    tsv_paths=tsv_paths,
                    country_code="en",
                    server_directory=internalPaths.SERVERDIRECTORY,
                    output_directory=internalPaths.VANILLAFILES,
                    wanted_files=requirements["server"],
                    use_pack_directory=False,
                    log=self.log.emit,
                )

        pack_name = internalPaths.DOWNLOADLOCALPACK.stem

        internalPaths.DOWNLOADLOCAL.mkdir(
            parents=True,
            exist_ok=True,
        )

        # TODO RANDOMIZER CODE HEY DAB IM ADDING IT HERE
        # randomize_function.randomize_according_to_config(config=config,log=self.log.emit)
        fix_zombie()


        self.log.emit(
            f"\nEncrypting: {pack_name}"
        )

        encrypt_pack(
            game_files_dir=internalPaths.DOWNLOADLOCAL,
            pack_name=pack_name,
            output_directory=internalPaths.DOWNLOADLOCALPACK.parent,
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
            internalPaths.DECOMPILED,
            internalPaths.REBUILTAPK,
        )

        self.log.emit("Zipaligning APK")

        zipalign_apk(internalPaths.REBUILTAPK,internalPaths.ALIGNEDAPK,)

        self.log.emit("Signing APK")

        sign_apk(internalPaths.ALIGNEDAPK,signed_apk,)
        self.log.emit(f"Signed APK: {signed_apk}")
        
        self.html_log.emit('<span style="color: lime;">Randomization Complete.</span>')
        self.html_log.emit('<span style="color: orange;">MAKE SURE TO SAVE YOUR CONFIG IF YOU HAVENT!</span>')