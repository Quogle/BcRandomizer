from pathlib import Path
from PySide6.QtGui import QIntValidator
import random

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QPlainTextEdit,
    QApplication,
)


from PySide6.QtCore import Signal, QObject, QThread

from ..helpers.config_helpers import *

from ...apk.extract import extract_apk
from ...apk.build import build_apk
from ...apk.zipalign import zipalign_apk
from ...apk.sign import sign_apk

from ...apk.packs.decrypt import decrypt_packs
from ...apk.packs.encrypt import encrypt_pack

from ...apk.server.downloader import download_server_files, process_server_files
from ...apk.packs.required_files import get_required_files

# True = decrypt only the files in decrypt_specifics
# False = decrypt every pack
DECRYPT_SPECIFICS = True

class RandomizeWorker(QObject):

    finished = Signal()
    error = Signal(str)
    log = Signal(str)

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

        extract_apk(
            apk_path,
            decoded_directory,
        )

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
            raise RuntimeError(
                "No .pack files found"
            )

        requirements = get_required_files(config)

        self.log.emit("Decrypting packs...")

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

        tsv_paths = sorted(
            decoded_directory.rglob("download_*.tsv")
        )

        self.log.emit(
            f"\nFound libnative.so: {lib_path}"
        )

        self.log.emit(
            f"Found {len(tsv_paths)} server TSV files:"
        )

        self.log.emit("Decrypting server packs...")

        for tsv in tsv_paths:
           print(f"  {tsv}")

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
            )

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

        self.log.emit(
            f"\nEncrypting: {pack_name}"
        )

        encrypt_pack(
            game_files_dir=game_files_directory,
            pack_name=pack_name,
            output_directory=pack_path.parent,
            cc="en",
        )

        self.log.emit("Building APK")

        build_apk(
            decoded_directory,
            rebuilt_apk,
        )

        self.log.emit("Zipaligning APK")

        zipalign_apk(
            rebuilt_apk,
            aligned_apk,
        )

        self.log.emit("Signing APK")

        sign_apk(
            aligned_apk,
            signed_apk,
        )

        self.log.emit("DONE")
        self.log.emit(
            f"Signed APK: {signed_apk}"
        )

class SetupWindow(QWidget):

    config_loaded = Signal()

    def __init__(self, config):
        super().__init__()

        self.config = config

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 22)
        layout.setSpacing(15)

        # Input APK
        input_layout = QHBoxLayout()

        input_label = QLabel("Input APK:")
        self.input_apk = QLineEdit()
        self.input_apk.setPlaceholderText("Select APK file...")
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

        ######## SEED INPUT FIELD ############################################################################

        seed_label = QLabel("Seed:")
        self.seed = QLineEdit()
        self.seed.setValidator(QIntValidator(-2147483648, 2147483647))

        connect_line_edit(
            self.seed,
            self.config["mod"],
            "seed",
        )

        id_label = QLabel("Mod ID:")
        self.id = QLineEdit()

        connect_line_edit(
            self.id,
            self.config["mod"],
            "id",
        )

        randomize_button = QPushButton("Randomize")

        randomize_button.clicked.connect(
            self.randomize
        )

        randomizer_layout.addWidget(seed_label)
        randomizer_layout.addWidget(self.seed)
        randomizer_layout.addWidget(id_label)
        randomizer_layout.addWidget(self.id)

        layout.addLayout(randomizer_layout)
        layout.addWidget(randomize_button)

        # console
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)

        layout.addWidget(self.console)

        layout.addStretch()

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

            self.seed.setText(
                "" if self.config["mod"]["seed"] is None
                else str(self.config["mod"]["seed"])
            )
            self.id.setText(self.config["mod"]["id"])

            self.config_loaded.emit()

    def log(self, message):
        self.console.appendPlainText(str(message))

    def randomize_error(self, message):
        self.log(f"ERROR: {message}")


    # Randomize Function 

    def randomize(self):

        seed_text = self.seed.text().strip()

        if seed_text:
            seed = int(seed_text)
        else:
            seed = random.randint(
                -2147483648,
                2147483647,
            )

        self.config["mod"]["seed"] = seed
        self.seed.setText(str(seed))

        self.log(f"Seed: {seed}")

        apk_path = self.input_apk.text().strip()

        if not apk_path:
            return

        self.thread = QThread(self)
        self.worker = RandomizeWorker(
            apk_path,
            self.config.copy(),
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.log.connect(
            self.log
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.worker.error.connect(
            self.randomize_error
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.start()