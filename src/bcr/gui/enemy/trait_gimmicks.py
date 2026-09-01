from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QCheckBox,
    QPushButton,
)

from PySide6.QtCore import Qt

from ..helpers.widgets import *
from ..helpers.config_helpers import *


class TraitGimmicks(QWidget):
    def __init__(self, config):
        super().__init__()

        self.config = config

        # Main layout for trait gimmicks widget
        self.layout = QVBoxLayout(self)

        trait_buttons_layout = QHBoxLayout()

        traits = [
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
        ]

        self.trait_buttons = []
        self.selected_trait_button = None
        self.selected_trait = "White"

        for trait in traits:
            button = QPushButton(trait)

            button.clicked.connect(
                lambda checked=False, t=trait:
                self.change_trait_gimmick(t)
            )

            trait_buttons_layout.addWidget(button)
            self.trait_buttons.append(button)

        self.layout.addLayout(trait_buttons_layout)

        self.trait_menu = QWidget()

        self.trait_menu_layout = QVBoxLayout(self.trait_menu)
        self.trait_menu_layout.setContentsMargins(0, 10, 0, 0)

        self.layout.addWidget(self.trait_menu)
        self.change_trait_gimmick("White")


    def create_trait_menu(self):
        menu = QWidget()

        menu_layout = QVBoxLayout(menu)
        menu_layout.setContentsMargins(12, 8, 12, 8)
        menu_layout.setSpacing(8)

        return menu, menu_layout

    # Trait Menu Switching
    def change_trait_gimmick(self, trait):

        self.selected_trait = trait

        # Reset previous selected button
        if self.selected_trait_button is not None:
            self.selected_trait_button.setStyleSheet("")

        # Find and highlight the selected button
        for button in self.trait_buttons:
            if button.text() == trait:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #9e42bf;
                        color: white;
                    }
                """)
                self.selected_trait_button = button
                break

        while self.trait_menu_layout.count():
            item = self.trait_menu_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

            elif item.layout() is not None:
                self.clear_layout(item.layout())

        # Create the menu for the selected trait
        if trait == "White":
            self.create_white_menu(self.trait_menu_layout)
        elif trait == "Red":
            self.create_red_menu(self.trait_menu_layout)
        elif trait == "Floating":
            self.create_floating_menu(self.trait_menu_layout)
        elif trait == "Dark":
            self.create_dark_menu(self.trait_menu_layout)
        elif trait == "Angel":
            self.create_angel_menu(self.trait_menu_layout)
        elif trait == "Alien":
            self.create_alien_menu(self.trait_menu_layout)
        elif trait == "Zombie":
            self.create_zombie_menu(self.trait_menu_layout)
        elif trait == "Relic":
            self.create_relic_menu(self.trait_menu_layout)
        elif trait == "Aku":
            self.create_aku_menu(self.trait_menu_layout)
        elif trait == "Metal":
            self.create_metal_menu(self.trait_menu_layout)



    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

            elif item.layout() is not None:
                self.clear_layout(item.layout())

    ###################################################################################################################
    # White
    ###################################################################################################################

    def create_white_menu(self, layout):

        menu, menu_layout = self.create_trait_menu()

        white_config = self.config["enemy"]["trait_gimmicks"]["white"]

        # Enabled
        self.white_enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.white_enabled,
            white_config,
            "enabled"
        )

        # Sage
        self.white_sage = QCheckBox("Make White Enemies Sage")
        connect_checkbox(
            self.white_sage,
            white_config,
            "sage"
        )

        # Sage Debuff Resist Multiplier
        resist_layout = QHBoxLayout()

        resist_label = QLabel("Sage Debuff Resist Multiplier:")

        self.white_sage_resist_mult = NoWheelSpinBox()
        self.white_sage_resist_mult.setRange(1, 100)
        self.white_sage_resist_mult.setSuffix("%")

        connect_value(
            self.white_sage_resist_mult,
            white_config,
            "sage_resist_mult"
        )

        resist_layout.addWidget(resist_label)
        resist_layout.addWidget(self.white_sage_resist_mult)
        resist_layout.addStretch()

        menu_layout.addWidget(self.white_enabled)
        menu_layout.addWidget(self.white_sage)
        menu_layout.addLayout(resist_layout)

        layout.addWidget(menu)

    ###################################################################################################################
    # Red Trait
    ###################################################################################################################

    def create_red_menu(self, layout):

        menu, menu_layout = self.create_trait_menu()

        red_config = self.config["enemy"]["trait_gimmicks"]["red"]

        self.red_enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.red_enabled,
            red_config,
            "enabled"
        )

        speed_layout = QHBoxLayout()
        speed_label = QLabel("Speed Multiplier")

        self.red_speed_mult = NoWheelDoubleSpinBox()
        self.red_speed_mult.setSingleStep(0.1)
        connect_value(
            self.red_speed_mult,
            red_config,
            "speed_mult"
        )

        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.red_speed_mult)

        kb_layout = QHBoxLayout()
        kb_label = QLabel("Knockback Multiplier")

        self.red_kb_mult = NoWheelDoubleSpinBox()
        self.red_kb_mult.setSingleStep(0.1)
        connect_value(
            self.red_kb_mult,
            red_config,
            "kb_mult"
        )

        kb_layout.addWidget(kb_label)
        kb_layout.addWidget(self.red_kb_mult)

        mult_rounding_layout = QHBoxLayout()
        mult_rounding_label = QLabel("Multiplier Rounding")

        self.red_mult_rounding = NoWheelQComboBox()
        self.red_mult_rounding.addItems([
            "Up",
            "Down",
        ])
        connect_combobox(
            self.red_mult_rounding,
            red_config,
            "mult_rounding"
        )

        mult_rounding_layout.addWidget(mult_rounding_label)
        mult_rounding_layout.addWidget(self.red_mult_rounding)

        menu_layout.addWidget(self.red_enabled)
        menu_layout.addLayout(speed_layout)
        menu_layout.addLayout(kb_layout)
        menu_layout.addLayout(mult_rounding_layout)

        layout.addWidget(menu)


    ###################################################################################################################
    # FLOATING TRAIT
    ###################################################################################################################
    def create_floating_menu(self, layout):

        menu, menu_layout = self.create_trait_menu()

        floating_config = self.config["enemy"]["trait_gimmicks"]["floating"]

        # Basic Floating settings
        self.floating_enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.floating_enabled,
            floating_config,
            "enabled"
        )
        menu_layout.addWidget(self.floating_enabled)

        # Ability Selection

        self.floating_abilities = WeightedList(
            floating_config["abilities"].items()
        )

        connect_weighted_list(
            self.floating_abilities,
            floating_config["abilities"]
        )

        menu_layout.addWidget(self.floating_abilities)

        # Dual Ability Chance
        dual_ability_layout = QHBoxLayout()

        dual_ability_label = QLabel("Dual Ability Chance:")
        dual_ability_value = QLabel()

        self.floating_dual_ability_chance = NoWheelSlider(Qt.Horizontal)
        self.floating_dual_ability_chance.setRange(0, 100)
        connect_value(
            self.floating_dual_ability_chance,
            floating_config,
            "dual_ability_chance"
        )

        dual_ability_value.setText(
            f"{floating_config['dual_ability_chance']}%"
        )

        self.floating_dual_ability_chance.valueChanged.connect(
            lambda value:
            dual_ability_value.setText(f"{value}%")
        )

        dual_ability_layout.addWidget(dual_ability_label)
        dual_ability_layout.addWidget(self.floating_dual_ability_chance)
        dual_ability_layout.addWidget(dual_ability_value)

        menu_layout.addLayout(dual_ability_layout)

        layout.addWidget(menu)

    ###################################################################################################################
    # DARK TRAIT
    ###################################################################################################################
    def create_dark_menu(self, layout):

        menu, menu_layout = self.create_trait_menu()

        dark_config = self.config["enemy"]["trait_gimmicks"]["dark"]

        # Basic Dark settings
        self.dark_enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.dark_enabled,
            dark_config,
            "enabled"
        )

        menu_layout.addWidget(self.dark_enabled)

        # ----------------------------------------------------------------------------------------------------
        # Speed Boost
        # ----------------------------------------------------------------------------------------------------

        speed_boost_label = QLabel("Speed Boost")
        speed_boost_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            margin-top: 8px;
        """)

        menu_layout.addWidget(speed_boost_label)

        self.dark_speed_boost_layout = QVBoxLayout()
        self.dark_speed_boost_layout.setSpacing(6)
        menu_layout.addLayout(self.dark_speed_boost_layout)

        for boost_config in dark_config["speed_boosts"]:
            self.add_dark_speed_boost(boost_config)

        add_speed_boost = QPushButton("+ Add Speed Boost")
        add_speed_boost.clicked.connect(
            lambda: self.add_dark_speed_boost()
        )

        menu_layout.addWidget(add_speed_boost)

        # ----------------------------------------------------------------------------------------------------
        # Knockback Multiplier
        # ----------------------------------------------------------------------------------------------------

        kb_layout = QHBoxLayout()

        kb_label = QLabel("Knockback Multiplier")
        kb_label.setFixedWidth(140)

        self.dark_kb_mult = NoWheelDoubleSpinBox()
        self.dark_kb_mult.setRange(0, 100)
        self.dark_kb_mult.setSingleStep(0.1)
        connect_value(
            self.dark_kb_mult,
            dark_config,
            "knockback_mult"
        )

        kb_layout.addWidget(kb_label)
        kb_layout.addWidget(self.dark_kb_mult)
        kb_layout.addStretch()

        menu_layout.addLayout(kb_layout)

        # ----------------------------------------------------------------------------------------------------
        # Knockback Rounding
        # ----------------------------------------------------------------------------------------------------

        rounding_layout = QHBoxLayout()
        rounding_label = QLabel("Multiplier Rounding")
        rounding_label.setFixedWidth(140)

        self.dark_mult_rounding = NoWheelQComboBox()
        self.dark_mult_rounding.addItems([
            "Up",
            "Down",
        ])
        connect_combobox(
            self.dark_mult_rounding,
            dark_config,
            "mult_rounding"
        )

        rounding_layout.addWidget(rounding_label)
        rounding_layout.addWidget(self.dark_mult_rounding)
        rounding_layout.addStretch()
        
        menu_layout.addLayout(rounding_layout)

        layout.addWidget(menu)


    def add_dark_speed_boost(self, boost_config=None):

        if boost_config is None:
            boost_config = {
                "threshold": 0,
                "multiplier": "Additive",
                "boost": 0,
            }

            self.config["enemy"]["trait_gimmicks"]["dark"]["speed_boosts"].append(
                boost_config
            )

        row = QWidget()

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(6)

        # Speed threshold
        threshold = NoWheelDoubleSpinBox()
        threshold.setRange(0.0, 9999.0)
        threshold.setSingleStep(0.1)
        threshold.setPrefix("Threshold: ")

        connect_value(
            threshold,
            boost_config,
            "threshold"
        )

        # Additive / Multiplicative
        multiplier = NoWheelQComboBox()
        multiplier.addItems([
            "Additive",
            "Multiplicative",
        ])

        connect_combobox(
            multiplier,
            boost_config,
            "multiplier"
        )

        # Boost amount
        boost = NoWheelDoubleSpinBox()
        boost.setRange(0, 9999.0)
        boost.setSingleStep(0.1)
        boost.setPrefix("Boost: ")

        connect_value(
            boost,
            boost_config,
            "boost"
        )

        # Remove
        remove = QPushButton("Remove")
        remove.clicked.connect(
            lambda: self.remove_dark_speed_boost(row, boost_config)
        )

        row_layout.addWidget(threshold)
        row_layout.addWidget(multiplier)
        row_layout.addWidget(boost)
        row_layout.addWidget(remove)

        self.dark_speed_boost_layout.addWidget(row)


    def remove_dark_speed_boost(self, row, boost_config):

        self.config["enemy"]["trait_gimmicks"]["dark"]["speed_boosts"].remove(
            boost_config
        )

        self.dark_speed_boost_layout.removeWidget(row)
        row.deleteLater()


    ##################################################################################################################
    # ANGEL TRAIT
    ##################################################################################################################

    def create_angel_menu(self, layout):

        menu, menu_layout = self.create_trait_menu()

        angel_config = self.config["enemy"]["trait_gimmicks"]["angel"]

        self.angel_enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.angel_enabled,
            angel_config,
            "enabled"
        )

        menu_layout.addWidget(self.angel_enabled)

        self.angel_balanced = QCheckBox("Balanced")
        connect_checkbox(
            self.angel_balanced,
            angel_config,
            "balanced"
        )        

        menu_layout.addWidget(self.angel_balanced)

        # Speed multiplier
        speed_layout = QHBoxLayout()

        speed_label = QLabel("Speed Multiplier:")
        speed_label.setFixedWidth(130)

        self.angel_speed_mult = NoWheelDoubleSpinBox()
        self.angel_speed_mult.setSingleStep(0.1)
        self.angel_speed_mult.setSuffix("x")
        connect_value(
            self.angel_speed_mult,
            angel_config,
            "speed_mult"
        )

        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.angel_speed_mult)
        speed_layout.addStretch()

        menu_layout.addLayout(speed_layout)

        # Attack multiplier
        attack_layout = QHBoxLayout()

        attack_label = QLabel("Attack Multiplier:")
        attack_label.setFixedWidth(130)

        self.angel_attack_mult = NoWheelDoubleSpinBox()
        self.angel_attack_mult.setSingleStep(0.1)
        self.angel_attack_mult.setSuffix("x")
        connect_value(
            self.angel_attack_mult,
            angel_config,
            "attack_mult"
        )

        attack_layout.addWidget(attack_label)
        attack_layout.addWidget(self.angel_attack_mult)
        attack_layout.addStretch()

        menu_layout.addLayout(attack_layout)

        # Health Multiplier
        health_layout = QHBoxLayout()

        health_label = QLabel("Health Multiplier:")
        health_label.setFixedWidth(130)

        self.angel_health_mult = NoWheelDoubleSpinBox()
        self.angel_health_mult.setSingleStep(0.1)
        self.angel_health_mult.setSuffix("x")
        connect_value(
            self.angel_health_mult,
            angel_config,
            "health_mult"
        )

        health_layout.addWidget(health_label)
        health_layout.addWidget(self.angel_health_mult)
        health_layout.addStretch()

        menu_layout.addLayout(health_layout)

        #Rounding

        rounding_layout = QHBoxLayout()
        rounding_label = QLabel("Multiplier Rounding")
        rounding_label.setFixedWidth(130)

        self.angel_rounding = NoWheelQComboBox()
        self.angel_rounding.addItems([
            "Up",
            "Down",
        ])
        connect_combobox(
            self.angel_rounding,
            angel_config,
            "rounding"
        )

        rounding_layout.addWidget(rounding_label)
        rounding_layout.addWidget(self.angel_rounding)
        rounding_layout.addStretch()
        
        menu_layout.addLayout(rounding_layout)


        layout.addWidget(menu)

    ##################################################################################################################
    # ALIEN TRAIT
    ##################################################################################################################
    def create_alien_menu(self, layout):

        menu, menu_layout = self.create_trait_menu()

        alien_config = self.config["enemy"]["trait_gimmicks"]["alien"]

        # Basic Alien settings
        self.alien_enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.alien_enabled,
            alien_config,
            "enabled"
        )

        menu_layout.addWidget(self.alien_enabled)

        # ----------------------------------------------------------------------------------------------------
        # Ability Selection
        # ----------------------------------------------------------------------------------------------------

        self.alien_abilities = WeightedList(
            alien_config["abilities"].items()
        )

        connect_weighted_list(
            self.alien_abilities,
            alien_config["abilities"]
        )

        menu_layout.addWidget(self.alien_abilities)

        # ----------------------------------------------------------------------------------------------------
        # Starred Frequency
        # ----------------------------------------------------------------------------------------------------

        starred_layout = QHBoxLayout()

        starred_label = QLabel("Starred Frequency")
        starred_label.setFixedWidth(220)

        self.alien_starred_frequency = NoWheelSlider(Qt.Horizontal)
        self.alien_starred_frequency.setRange(0, 100)
        connect_value(
            self.alien_starred_frequency,
            alien_config,
            "starred_frequency"
        )

        starred_value = QLabel()

        starred_value.setText(
            f"{alien_config["starred_frequency"]}%"
        )

        self.alien_starred_frequency.valueChanged.connect(
            lambda value:
            starred_value.setText(f"{value}%")
        )

        starred_layout.addWidget(starred_label)
        starred_layout.addWidget(self.alien_starred_frequency)
        starred_layout.addWidget(starred_value)

        menu_layout.addLayout(starred_layout)

        # ----------------------------------------------------------------------------------------------------
        # Warp Frequency
        # ----------------------------------------------------------------------------------------------------

        warp_layout = QHBoxLayout()

        warp_label = QLabel("Warp Frequency")
        warp_label.setFixedWidth(220)

        self.alien_warp_frequency = NoWheelSlider(Qt.Horizontal)
        self.alien_warp_frequency.setRange(0, 100)
        connect_value(
            self.alien_warp_frequency,
            alien_config,
            "warp_frequency"
        )

        warp_value = QLabel()
        warp_value.setText(
            f"{alien_config["warp_frequency"]}%"
        )

        self.alien_warp_frequency.valueChanged.connect(
            lambda value:
            warp_value.setText(f"{value}%")
        )

        warp_layout.addWidget(warp_label)
        warp_layout.addWidget(self.alien_warp_frequency)
        warp_layout.addWidget(warp_value)

        menu_layout.addLayout(warp_layout)

        # ----------------------------------------------------------------------------------------------------
        # Barrier Frequency
        # ----------------------------------------------------------------------------------------------------

        barrier_layout = QHBoxLayout()

        barrier_label = QLabel("Barrier Frequency")
        barrier_label.setFixedWidth(220)

        self.alien_barrier_frequency = NoWheelSlider(Qt.Horizontal)
        self.alien_barrier_frequency.setRange(0, 100)
        connect_value(
            self.alien_barrier_frequency,
            alien_config,
            "barrier_frequency"
        )

        barrier_value = QLabel()
        barrier_value.setText(
            f"{alien_config["barrier_frequency"]}%"
        )

        self.alien_barrier_frequency.valueChanged.connect(
            lambda value:
            barrier_value.setText(f"{value}%")
        )

        barrier_layout.addWidget(barrier_label)
        barrier_layout.addWidget(self.alien_barrier_frequency)
        barrier_layout.addWidget(barrier_value)

        menu_layout.addLayout(barrier_layout)

        layout.addWidget(menu)

    ##################################################################################################################
    # Zombie Trait
    ##################################################################################################################

    def create_zombie_menu(self, layout):

        menu, menu_layout = self.create_trait_menu()

        zombie_config = self.config["enemy"]["trait_gimmicks"]["zombie"]

        self.zombie_enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.zombie_enabled,
            zombie_config,
            "enabled"
        )

        self.zombie_balanced = QCheckBox("Balanced")
        connect_checkbox(
            self.zombie_balanced,
            zombie_config,
            "balanced"
        )

        menu_layout.addWidget(self.zombie_enabled)
        menu_layout.addWidget(self.zombie_balanced)

        # ----------------------------------------------------------------------------------------------------
        # Revive
        # ----------------------------------------------------------------------------------------------------

        revive_group = QGroupBox("Revive")
        revive_layout = QVBoxLayout(revive_group)

        self.zombie_grant_revive = QCheckBox("Grant Revive")
        connect_checkbox(
            self.zombie_grant_revive,
            zombie_config,
            "grant_revive"
        )

        revive_layout.addWidget(self.zombie_grant_revive)

        # ----------------------------------------------------------------------------------------------------
        # Revive Frequency
        # ----------------------------------------------------------------------------------------------------

        frequency_layout = QHBoxLayout()

        frequency_label = QLabel("Frequency:")
        frequency_value = QLabel()

        self.zombie_revive_frequency = NoWheelSlider(Qt.Horizontal)
        self.zombie_revive_frequency.setRange(0, 100)

        connect_value(
            self.zombie_revive_frequency,
            zombie_config,
            "revive_frequency"
        )

        frequency_value.setText(
            f"{zombie_config['revive_frequency']}%"
        )

        self.zombie_revive_frequency.valueChanged.connect(
            lambda value:
            frequency_value.setText(f"{value}%")
        )

        frequency_layout.addWidget(frequency_label)
        frequency_layout.addWidget(self.zombie_revive_frequency)
        frequency_layout.addWidget(frequency_value)

        revive_layout.addLayout(frequency_layout)

        # ----------------------------------------------------------------------------------------------------
        # Revive Types
        # ----------------------------------------------------------------------------------------------------

        revive_types_label = QLabel("Revive Types")
        revive_types_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            margin-top: 8px;
        """)

        revive_layout.addWidget(revive_types_label)

        self.revive_types_layout = QVBoxLayout()
        self.revive_types_layout.setSpacing(6)

        revive_layout.addLayout(self.revive_types_layout)

        for revive_config in zombie_config["revive_types"]:
            self.add_revive_type(revive_config)

        add_revive = QPushButton("+ Add Revive Type")
        add_revive.clicked.connect(
            lambda: self.add_revive_type()
        )

        revive_layout.addWidget(add_revive)

        menu_layout.addWidget(revive_group)

        # ----------------------------------------------------------------------------------------------------
        # Burrow
        # ----------------------------------------------------------------------------------------------------

        burrow_group = QGroupBox("Burrow")
        burrow_layout = QVBoxLayout(burrow_group)

        self.zombie_grant_burrow = QCheckBox("Grant Burrow")
        connect_checkbox(
            self.zombie_grant_burrow,
            zombie_config,
            "grant_burrow"
        )

        burrow_layout.addWidget(self.zombie_grant_burrow)

        # ----------------------------------------------------------------------------------------------------
        # Burrow Frequency
        # ----------------------------------------------------------------------------------------------------

        burrow_frequency_layout = QHBoxLayout()

        burrow_frequency_label = QLabel("Frequency:")
        burrow_frequency_value = QLabel()

        self.zombie_burrow_frequency = NoWheelSlider(Qt.Horizontal)
        self.zombie_burrow_frequency.setRange(0, 100)

        connect_value(
            self.zombie_burrow_frequency,
            zombie_config,
            "burrow_frequency"
        )

        burrow_frequency_value.setText(
            f"{zombie_config['burrow_frequency']}%"
        )

        self.zombie_burrow_frequency.valueChanged.connect(
            lambda value:
            burrow_frequency_value.setText(f"{value}%")
        )

        burrow_frequency_layout.addWidget(
            burrow_frequency_label
        )
        burrow_frequency_layout.addWidget(
            self.zombie_burrow_frequency
        )
        burrow_frequency_layout.addWidget(
            burrow_frequency_value
        )

        burrow_layout.addLayout(burrow_frequency_layout)

        # ----------------------------------------------------------------------------------------------------
        # Burrow Types
        # ----------------------------------------------------------------------------------------------------

        burrow_types_label = QLabel("Burrow Types")
        burrow_types_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            margin-top: 8px;
        """)

        burrow_layout.addWidget(burrow_types_label)

        self.burrow_types_layout = QVBoxLayout()
        self.burrow_types_layout.setSpacing(6)

        burrow_layout.addLayout(self.burrow_types_layout)

        for burrow_config in zombie_config["burrow_types"]:
            self.add_burrow_type(burrow_config)

        add_burrow = QPushButton("+ Add Burrow Type")
        add_burrow.clicked.connect(
            lambda: self.add_burrow_type()
        )

        burrow_layout.addWidget(add_burrow)

        menu_layout.addWidget(burrow_group)

        layout.addWidget(menu)


    # ----------------------------------------------------------------------------------------------------
    # Revive Type
    # ----------------------------------------------------------------------------------------------------

    def add_revive_type(self, revive_config=None):

        zombie_config = self.config["enemy"]["trait_gimmicks"]["zombie"]

        if revive_config is None:
            revive_config = {
                "count": 0,
                "hp": 0,
                "delay": 0,
                "weight": 0,
            }

            zombie_config["revive_types"].append(
                revive_config
            )

        row = QWidget()

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(6)

        # Count
        count = NoWheelSpinBox()
        count.setRange(-1, 999)
        count.setPrefix("Count: ")

        connect_value(
            count,
            revive_config,
            "count"
        )

        # HP
        hp = NoWheelSpinBox()
        hp.setRange(1, 100)
        hp.setSuffix("% HP")

        connect_value(
            hp,
            revive_config,
            "hp"
        )

        # Delay
        delay = NoWheelSpinBox()
        delay.setRange(0, 99999)
        delay.setSuffix(" delay")

        connect_value(
            delay,
            revive_config,
            "delay"
        )

        # Weight
        weight = NoWheelSpinBox()
        weight.setRange(0, 999)
        weight.setPrefix("Weight: ")

        connect_value(
            weight,
            revive_config,
            "weight"
        )

        # Remove
        remove = QPushButton("Remove")
        remove.clicked.connect(
            lambda:
            self.remove_revive_type(row, revive_config)
        )

        row_layout.addWidget(count)
        row_layout.addWidget(hp)
        row_layout.addWidget(delay)
        row_layout.addWidget(weight)
        row_layout.addWidget(remove)

        self.revive_types_layout.addWidget(row)


    def remove_revive_type(self, row, revive_config):

        zombie_config = self.config["enemy"]["trait_gimmicks"]["zombie"]

        zombie_config["revive_types"].remove(
            revive_config
        )

        self.revive_types_layout.removeWidget(row)
        row.deleteLater()


    # ----------------------------------------------------------------------------------------------------
    # Burrow Type Management
    # ----------------------------------------------------------------------------------------------------

    def add_burrow_type(self, burrow_config=None):

        zombie_config = self.config["enemy"]["trait_gimmicks"]["zombie"]

        if burrow_config is None:
            burrow_config = {
                "count": 0,
                "distance": 0,
                "weight": 0,
            }

            zombie_config["burrow_types"].append(
                burrow_config
            )

        row = QWidget()

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(6)

        # Count
        count = NoWheelSpinBox()
        count.setRange(-1, 999)
        count.setPrefix("Count: ")

        connect_value(
            count,
            burrow_config,
            "count"
        )

        # Distance
        distance = NoWheelSpinBox()
        distance.setRange(0, 99999)
        distance.setPrefix("Distance ×4: ")

        connect_value(
            distance,
            burrow_config,
            "distance"
        )

        # Weight
        weight = NoWheelSpinBox()
        weight.setRange(0, 999)
        weight.setPrefix("Weight: ")

        connect_value(
            weight,
            burrow_config,
            "weight"
        )

        # Remove
        remove = QPushButton("Remove")
        remove.clicked.connect(
            lambda:
            self.remove_burrow_type(row, burrow_config)
        )

        row_layout.addWidget(count)
        row_layout.addWidget(distance)
        row_layout.addWidget(weight)
        row_layout.addWidget(remove)

        self.burrow_types_layout.addWidget(row)


    def remove_burrow_type(self, row, burrow_config):

        zombie_config = self.config["enemy"]["trait_gimmicks"]["zombie"]

        zombie_config["burrow_types"].remove(
            burrow_config
        )

        self.burrow_types_layout.removeWidget(row)
        row.deleteLater()

    ##################################################################################################################
    # Relic Trait
    ##################################################################################################################

    def create_relic_menu(self, layout):

        menu, menu_layout = self.create_trait_menu()

        relic_config = self.config["enemy"]["trait_gimmicks"]["relic"]

        self.relic_enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.relic_enabled,
            relic_config,
            "enabled"
        )

        menu_layout.addWidget(self.relic_enabled)

        self.relic_curse = QCheckBox("Curse")
        connect_checkbox(
            self.relic_curse,
            relic_config,
            "curse"
        )

        menu_layout.addWidget(self.relic_curse)

        self.relic_pierce = QCheckBox("Pierce")
        connect_checkbox(
            self.relic_pierce,
            relic_config,
            "pierce"
        )

        menu_layout.addWidget(self.relic_pierce)

        ##### Pierce Attack Percent #####
        relic_pierce_attack_layout = QHBoxLayout()

        relic_pierce_attack_label = QLabel("Pierce Attack %")
        relic_pierce_attack_label.setFixedWidth(220)
        relic_pierce_attack_value = QLabel()

        self.relic_pierce_attack = NoWheelSlider(Qt.Horizontal)
        self.relic_pierce_attack.setRange(0, 200)
        connect_value(
            self.relic_pierce_attack,
            relic_config,
            "pierce_attack"
        )

        relic_pierce_attack_value.setText(
            f"{relic_config['pierce_attack']}%"
        )

        self.relic_pierce_attack.valueChanged.connect(
            lambda value:
            relic_pierce_attack_value.setText(f"{value}%")
        )

        relic_pierce_attack_layout.addWidget(relic_pierce_attack_label)
        relic_pierce_attack_layout.addWidget(self.relic_pierce_attack)
        relic_pierce_attack_layout.addWidget(relic_pierce_attack_value)

        menu_layout.addLayout(relic_pierce_attack_layout)

        ##### Pierce Range Percent #####
        relic_pierce_range_layout = QHBoxLayout()

        relic_pierce_range_label = QLabel("Pierce Range %")
        relic_pierce_range_label.setFixedWidth(220)

        self.relic_pierce_range = NoWheelSlider(Qt.Horizontal)
        self.relic_pierce_range.setRange(0, 200)
        connect_value(
            self.relic_pierce_range,
            relic_config,
            "pierce_range"
        )

        relic_pierce_range_value = QLabel()

        relic_pierce_range_value.setText(
            f"{relic_config['pierce_range']}%"
        )

        self.relic_pierce_range.valueChanged.connect(
            lambda value:
            relic_pierce_range_value.setText(f"{value}%")
        )

        relic_pierce_range_layout.addWidget(relic_pierce_range_label)
        relic_pierce_range_layout.addWidget(self.relic_pierce_range)
        relic_pierce_range_layout.addWidget(relic_pierce_range_value)

        menu_layout.addLayout(relic_pierce_range_layout)

        layout.addWidget(menu)


    ##################################################################################################################
    # Aku Trait
    ##################################################################################################################

    def create_aku_menu(self, layout):

        menu, menu_layout = self.create_trait_menu()

        aku_config = self.config["enemy"]["trait_gimmicks"]["aku"]

        self.aku_enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.aku_enabled,
            aku_config,
            "enabled"
        )

        menu_layout.addWidget(self.aku_enabled)

        ##### Shield Frequency #####
        aku_shield_frequency_layout = QHBoxLayout()

        aku_shield_frequency_label = QLabel("Shield Frequency")
        aku_shield_frequency_label.setFixedWidth(220)

        self.aku_shield_frequency = NoWheelSlider(Qt.Horizontal)
        self.aku_shield_frequency.setRange(0, 100)
        connect_value(
            self.aku_shield_frequency,
            aku_config,
            "shield_frequency"
        )

        aku_shield_frequency_value = QLabel()

        aku_shield_frequency_value.setText(
            f"{aku_config['shield_frequency']}%"
        )

        self.aku_shield_frequency.valueChanged.connect(
            lambda value:
            aku_shield_frequency_value.setText(f"{value}%")
        )

        aku_shield_frequency_layout.addWidget(aku_shield_frequency_label)
        aku_shield_frequency_layout.addWidget(self.aku_shield_frequency)
        aku_shield_frequency_layout.addWidget(aku_shield_frequency_value)

        menu_layout.addLayout(aku_shield_frequency_layout)

        ##### Death Surge Frequency #####
        aku_ds_frequency_layout = QHBoxLayout()

        aku_ds_frequency_label = QLabel("Death Surge Frequency")
        aku_ds_frequency_label.setFixedWidth(220)

        self.aku_ds_frequency = NoWheelSlider(Qt.Horizontal)
        self.aku_ds_frequency.setRange(0, 100)
        connect_value(
            self.aku_ds_frequency,
            aku_config,
            "ds_frequency"
        )

        aku_ds_frequency_value = QLabel()

        aku_ds_frequency_value.setText(
            f"{aku_config['ds_frequency']}%"
        )

        self.aku_ds_frequency.valueChanged.connect(
            lambda value:
            aku_ds_frequency_value.setText(f"{value}%")
        )

        aku_ds_frequency_layout.addWidget(aku_ds_frequency_label)
        aku_ds_frequency_layout.addWidget(self.aku_ds_frequency)
        aku_ds_frequency_layout.addWidget(aku_ds_frequency_value)

        menu_layout.addLayout(aku_ds_frequency_layout)

        ##### Death Surge Ability Frequency #####
        aku_ds_ability_frequency_layout = QHBoxLayout()

        aku_ds_ability_frequency_label = QLabel("Death Surge Ability Frequency")
        aku_ds_ability_frequency_label.setFixedWidth(220)

        self.aku_ds_ability_frequency = NoWheelSlider(Qt.Horizontal)
        self.aku_ds_ability_frequency.setRange(0, 100)
        connect_value(
            self.aku_ds_ability_frequency,
            aku_config,
            "ds_ability_frequency"
        )

        aku_ds_ability_frequency_value = QLabel()

        aku_ds_ability_frequency_value.setText(
            f"{aku_config['ds_ability_frequency']}%"
        )

        self.aku_ds_ability_frequency.valueChanged.connect(
            lambda value:
            aku_ds_ability_frequency_value.setText(f"{value}%")
        )

        aku_ds_ability_frequency_layout.addWidget(aku_ds_ability_frequency_label)
        aku_ds_ability_frequency_layout.addWidget(self.aku_ds_ability_frequency)
        aku_ds_ability_frequency_layout.addWidget(aku_ds_ability_frequency_value)

        menu_layout.addLayout(aku_ds_ability_frequency_layout)

        #### Death Surge Ability Mini ####
        self.aku_ds_ability_mini = QCheckBox("Death Surge With Abilities Become Mini")
        connect_checkbox(
            self.aku_ds_ability_mini,
            aku_config,
            "ds_ability_mini"
        )

        menu_layout.addWidget(self.aku_ds_ability_mini)


        layout.addWidget(menu)


    ##################################################################################################################
    # Metal Trait
    ##################################################################################################################

    def create_metal_menu(self, layout):

        menu, menu_layout = self.create_trait_menu()

        metal_config = self.config["enemy"]["trait_gimmicks"]["metal"]

        self.metal_enabled = QCheckBox("Enabled")
        connect_checkbox(
            self.metal_enabled,
            metal_config,
            "enabled"
        )

        menu_layout.addWidget(self.metal_enabled)

        layout.addWidget(menu)