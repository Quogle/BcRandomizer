from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QGroupBox,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
)
from PySide6.QtCore import Qt
from src.bcr.gui.themes.dark import DARK_THEME
from .trait_gimmicks import TraitGimmicks
from .randomization import EnemyRandomization
from .ability import AbilityRandomization

class EnemyWindow(QWidget):
    def refresh_from_config(self):
        self.trait_gimmicks.refresh_from_config()
        self.enemy_randomization.refresh_from_config()
        self.ability_randomization.refresh_from_config()

    def __init__(self, config):
        super().__init__()

        self.config = config

        self.setStyleSheet(DARK_THEME)

        # --------------------------------------------------
        # Main layout
        # --------------------------------------------------

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)

        scroll.setWidget(content)

        main_layout.addWidget(scroll)

        # --------------------------------------------------
        # Trait Randomization
        # --------------------------------------------------

        trait_randomization = QGroupBox("Trait Randomization")
        trait_randomization_layout = QVBoxLayout(trait_randomization)

        # Trait Randomization Mode
        mode_layout = QHBoxLayout()

        mode_label = QLabel("Mode:")
        mode_label.setToolTip(
            "Controls how enemy traits are randomized"
        )

        mode_combo = QComboBox()
        mode_combo.addItem("None")
        mode_combo.setItemData(
            0,
            "Traits are unchanged.",
            Qt.ToolTipRole
        )

        mode_combo.addItem("Swap")
        mode_combo.setItemData(
            1,
            "Globally swaps traits between enemies.\n"
            "Example: zenemies become Dark.",
            Qt.ToolTipRole
        )

        mode_combo.addItem("Randomize")
        mode_combo.setItemData(
            2,
            "Gives each enemy a randomly selected trait.",
            Qt.ToolTipRole
        )
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(mode_combo)
        mode_layout.addStretch()

        trait_randomization_layout.addLayout(mode_layout)

        # Give traitless enemies traits
        give_traitless = QCheckBox(
            "Give untraited enemies traits"
        )
        give_traitless.setChecked(True)

        trait_randomization_layout.addWidget(give_traitless)

        # --------------------------------------------------
        # Specified Swaps
        # --------------------------------------------------

        swaps_label = QLabel("Specified Swaps")

        swaps_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            margin-top: 10px;
        """)

        trait_randomization_layout.addWidget(swaps_label)

        # Container for dynamically-created swap rows
        self.swaps_layout = QVBoxLayout()
        self.swaps_layout.setSpacing(6)

        trait_randomization_layout.addLayout(self.swaps_layout)

        # Add Swap button
        add_swap = QPushButton("+ Add Swap")
        add_swap.clicked.connect(self.add_swap)

        trait_randomization_layout.addWidget(add_swap)

        content_layout.addWidget(trait_randomization)

        # --------------------------------------------------
        # TRAIT GIMMICKS
        # --------------------------------------------------

        trait_gimmicks = QGroupBox("Trait Gimmicks")
        trait_gimmicks_layout = QVBoxLayout(trait_gimmicks)

        self.trait_gimmicks = TraitGimmicks(self.config)
        trait_gimmicks_layout.addWidget(self.trait_gimmicks)

        content_layout.addWidget(trait_gimmicks)

        # --------------------------------------------------
        # Enemy Randomization
        # --------------------------------------------------

        randomization_settings = QGroupBox("Enemy Randomization")
        randomization_settings_layout = QVBoxLayout(randomization_settings)

        self.enemy_randomization = EnemyRandomization(self.config)
        randomization_settings_layout.addWidget(self.enemy_randomization)

        content_layout.addWidget(randomization_settings)

        # --------------------------------------------------
        # Abilities
        # --------------------------------------------------

        ability_settings = QGroupBox("Ability Randomization")
        ability_settings_layout = QVBoxLayout(ability_settings)

        self.ability_randomization = AbilityRandomization(self.config)
        ability_settings_layout.addWidget(self.ability_randomization)

        content_layout.addWidget(ability_settings)

    # ======================================================
    # Specified Swaps
    # ======================================================

    def add_swap(self):
        row_widget = QWidget()

        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)

        # From traitfr
        from_combo = QComboBox()
        from_combo.addItems([
            "White",
            "Red",
            "Floating",
            "Dark",
            "Metal",
            "Angel",
            "Alien",
            "Zombie",
            "Relic",
            "Aku",
        ])

        # Arrow
        arrow = QLabel("→")
        arrow.setFixedWidth(20)

        # To trait
        to_combo = QComboBox()
        to_combo.addItems([
            "White",
            "Red",
            "Floating",
            "Dark",
            "Metal",
            "Angel",
            "Alien",
            "Zombie",
            "Relic",
            "Aku",
        ])

        # Remove button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(
            lambda: self.remove_swap(row_widget)
        )

        row_layout.addWidget(from_combo)
        row_layout.addWidget(arrow)
        row_layout.addWidget(to_combo)
        row_layout.addWidget(remove_button)
        row_layout.addStretch()

        self.swaps_layout.addWidget(row_widget)

    def remove_swap(self, row_widget):
        row_widget.deleteLater()