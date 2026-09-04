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

class UnitWindow(QWidget):
    def refresh_from_config(self):
        self.randomization.refresh_from_config()

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