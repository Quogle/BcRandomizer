from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
)
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import QRegularExpression, Qt

from ..helpers.config_helpers import connect_line_edit


class Versions(QWidget):

    def __init__(self, config):
        super().__init__()

        self.config = config

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        title = QLabel("Version Lock")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 17px; font-weight: bold;")
        title.setContentsMargins(0, -6, 0, 0)
        layout.addWidget(title)

        layout.addSpacing(13)

        validator = QRegularExpressionValidator(
            QRegularExpression(r"[0-9.]*")
        )

        # UNIT ID
        unit_id_label = QLabel("Unit ID")
        unit_id_label.setFixedWidth(80)

        self.unit_id = QLineEdit()
        self.unit_id.setValidator(validator)
        self.unit_id.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        connect_line_edit(
            self.unit_id,
            self.config["mod"],
            "unit_id"
        )

        unit_id_layout = QHBoxLayout()
        unit_id_layout.addWidget(unit_id_label)
        unit_id_layout.addWidget(self.unit_id)

        layout.addLayout(unit_id_layout)

        # UNIT TRAIT
        unit_trait_label = QLabel("Unit Trait")
        unit_trait_label.setFixedWidth(80)

        self.unit_trait = QLineEdit()
        self.unit_trait.setValidator(validator)
        self.unit_trait.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        connect_line_edit(
            self.unit_trait,
            self.config["mod"],
            "unit_trait"
        )

        unit_trait_layout = QHBoxLayout()
        unit_trait_layout.addWidget(unit_trait_label)
        unit_trait_layout.addWidget(self.unit_trait)

        layout.addLayout(unit_trait_layout)

        # UNIT ABILITY
        unit_ability_label = QLabel("Unit Ability")
        unit_ability_label.setFixedWidth(80)

        self.unit_ability = QLineEdit()
        self.unit_ability.setValidator(validator)
        self.unit_ability.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        connect_line_edit(
            self.unit_ability,
            self.config["mod"],
            "unit_ability"
        )

        unit_ability_layout = QHBoxLayout()
        unit_ability_layout.addWidget(unit_ability_label)
        unit_ability_layout.addWidget(self.unit_ability)

        layout.addLayout(unit_ability_layout)

        # TALENTS
        talents_label = QLabel("Talents")
        talents_label.setFixedWidth(80)

        self.talents = QLineEdit()
        self.talents.setValidator(validator)
        self.talents.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        connect_line_edit(
            self.talents,
            self.config["mod"],
            "talents"
        )

        talents_layout = QHBoxLayout()
        talents_layout.addWidget(talents_label)
        talents_layout.addWidget(self.talents)

        layout.addLayout(talents_layout)

        # ENEMY ID
        enemy_id_label = QLabel("Enemy ID")
        enemy_id_label.setFixedWidth(80)

        self.enemy_id = QLineEdit()
        self.enemy_id.setValidator(validator)
        self.enemy_id.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        connect_line_edit(
            self.enemy_id,
            self.config["mod"],
            "enemy_id"
        )

        enemy_id_layout = QHBoxLayout()
        enemy_id_layout.addWidget(enemy_id_label)
        enemy_id_layout.addWidget(self.enemy_id)

        layout.addLayout(enemy_id_layout)

        # COMBOS
        combos_label = QLabel("Combos")
        combos_label.setFixedWidth(80)

        self.combos = QLineEdit()
        self.combos.setValidator(validator)
        self.combos.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        connect_line_edit(
            self.combos,
            self.config["mod"],
            "combos"
        )

        combos_layout = QHBoxLayout()
        combos_layout.addWidget(combos_label)
        combos_layout.addWidget(self.combos)

        layout.addLayout(combos_layout)

        # STAGES
        stages_label = QLabel("Stages")
        stages_label.setFixedWidth(80)

        self.stages = QLineEdit()
        self.stages.setValidator(validator)
        self.stages.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        connect_line_edit(
            self.stages,
            self.config["mod"],
            "stages"
        )

        stages_layout = QHBoxLayout()
        stages_layout.addWidget(stages_label)
        stages_layout.addWidget(self.stages)

        layout.addLayout(stages_layout)

        layout.addStretch()