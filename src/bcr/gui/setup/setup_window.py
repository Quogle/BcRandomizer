from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
)

from PySide6.QtCore import Signal

from ..helpers.config_helpers import save_config, load_config, update_config

from ...apk.extract import extract_apk
from ...apk.build import build_apk
from ...apk.zipalign import zipalign_apk
from ...apk.sign import sign_apk

from ...apk.packs.decrypt_specifics import decrypt_specifics
from ...apk.packs.decrypt import decrypt_packs
from ...apk.packs.encrypt import encrypt_pack

from ...apk.server.downloader import download_server_files, process_server_files
from ...apk.packs.required_files import get_required_files

# True = decrypt only the files in decrypt_specifics
# False = decrypt every pack
DECRYPT_SPECIFICS = True

class SetupWindow(QWidget):

    config_loaded = Signal()

    def __init__(self, config):
        super().__init__()

        self.config = config

        layout = QVBoxLayout(self)

        # Input APK
        input_layout = QHBoxLayout()

        input_label = QLabel("Input APK:")
        self.input_apk = QLineEdit()
        input_button = QPushButton("Browse")

        input_button.clicked.connect(
            self.select_input_apk
        )

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_apk)
        input_layout.addWidget(input_button)

        layout.addLayout(input_layout)

  
        # Config Laytout
        config_layout = QHBoxLayout()

        load_button = QPushButton("Load Config")
        save_button = QPushButton("Save Config")

        load_button.clicked.connect(
            self.load_configuration
        )

        save_button.clicked.connect(
            self.save_configuration
        )

        config_layout.addWidget(load_button)
        config_layout.addWidget(save_button)

        layout.addLayout(config_layout)

        randomizer_layout = QHBoxLayout()

        seed_label = QLabel("Seed:")
        self.seed = QLineEdit()

        randomize_button = QPushButton("Randomize")

        randomize_button.clicked.connect(
            self.randomize
        )

        randomizer_layout.addWidget(seed_label)
        randomizer_layout.addWidget(self.seed)
        randomizer_layout.addWidget(randomize_button)

        layout.addLayout(randomizer_layout)

        ######### TEST BUTTON ############################################################################

        test_button = QPushButton("Test")
        test_button.clicked.connect(self.test_config)
        layout.addWidget(test_button)

        layout.addStretch()

    def test_config(self):
        weaken_weight = self.config["enemy"]["ability"]["weights"]["weaken"]
        print(weaken_weight)

    # APK Selection
    def select_input_apk(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select APK",
            "",
            "APK Files (*.apk)",
        )

        if path:
            self.input_apk.setText(path)

    # Config
    def save_configuration(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Configuration",
            "",
            "JSON Files (*.json)",
        )

        if path:
            save_config(
                self.config,
                path,
            )

    def load_configuration(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Configuration",
            "",
            "JSON Files (*.json)",
        )

        if path:
            loaded_config = load_config(path)
            update_config(self.config, loaded_config)
            self.config_loaded.emit()


    # Randomize Function

    def randomize(self):

        apk_path = self.input_apk.text().strip()

        if not apk_path:
            return

        workspace = Path("workspace")
        decoded_directory = (workspace/"decoded")
        decrypted_directory = (workspace/"decrypted")
        rebuilt_apk = (workspace/"rebuilt.apk")
        aligned_apk = (workspace/"aligned.apk")
        signed_apk = (workspace/"signed.apk")

        # Extract APK
        print("Extracting APK")

        extract_apk(apk_path,decoded_directory,)

        # Find pack files
        pack_paths = [
            path
            for path in decoded_directory.rglob("*.pack")
            if "_" not in path.stem
        ]

        print(
            f"\nFound {len(pack_paths)} pack files:"
        )

        for pack in pack_paths:
            print(f"  {pack}")

        if not pack_paths:
            raise RuntimeError(
                "No .pack files found"
            )

        requirements = get_required_files(self.config)

        # Decrypt packs
        print("Decrypting packs")

        if DECRYPT_SPECIFICS:
            decrypt_packs(
                pack_paths=pack_paths,
                cc="en",
                output_directory=decrypted_directory/"vanilla_files",
                wanted_files=requirements["local"],
                use_pack_directory=False,
            )
        else:
            decrypt_packs(
                pack_paths=pack_paths, 
                cc="en", 
                output_directory=decrypted_directory,
                )

        # Download server files

        server_directory = (workspace/"en_server")

        lib_path = (decoded_directory/"lib"/"x86_64"/"libnative-lib.so")

        tsv_paths = sorted(
            decoded_directory.rglob("download_*.tsv")
        )

        print(
            f"\nFound libnative.so: {lib_path}"
        )

        print(
            f"Found {len(tsv_paths)} server TSV files:"
        )

        for tsv in tsv_paths:
            print(f"  {tsv}")

        if (DECRYPT_SPECIFICS == False):
            download_server_files(
                lib_path=lib_path,
                tsv_paths=tsv_paths,
                country_code="en",
                output_directory=server_directory,
            )

            # Decrypt server packs

            server_pack_paths = list(server_directory.rglob("*.pack"))

            print(f"\nFound {len(server_pack_paths)} server pack files:")

            for pack in server_pack_paths:
                print(f"  {pack}")

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
                output_directory=decrypted_directory/ "vanilla_files",
                wanted_files=requirements["server"],
                use_pack_directory=False,
            )

        # DownloadLocal
        pack_path = (
            decoded_directory
            / "assets"
            / "DownloadLocal.pack"
        )

        pack_name = pack_path.stem

        game_files_directory = (
            decrypted_directory / pack_name
        )

        game_files_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # RANDOMIZER CODE

        # TODO: Make Randomizer Code

        # Re-encrypt DownloadLocal

        print(
            f"\nEncrypting: {pack_name}"
        )

        encrypt_pack(
            game_files_dir=game_files_directory,
            pack_name=pack_name,
            output_directory=pack_path.parent,
            cc="en",
        )

        print(
            (pack_path.parent / "DownloadLocal.list").read_bytes()
        )


        # Build APK
        print("Building APK")

        build_apk(
            decoded_directory,
            rebuilt_apk,
        )

        # Zipalign
        print("Zipaligning APK")

        zipalign_apk(
            rebuilt_apk,
            aligned_apk,
        )

        # Sign
        print("Signing APK")

        sign_apk(
            aligned_apk,
            signed_apk,
        )


        print("DONE")
        print(f"Signed APK: {signed_apk}")