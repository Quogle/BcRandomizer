import sys
from copy import deepcopy
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
)

from .enemy.enemy_window import EnemyWindow
from .unit.unit_window import UnitWindow
from .combo.combo_window import ComboWindow
from .setup.setup_window import SetupWindow
from src.bcr.gui.themes.dark import DARK_THEME
from ..config.defaults import DEFAULT_CONFIG


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = deepcopy(DEFAULT_CONFIG)

        self.setWindowTitle("Battle Cats Randomizer")
        self.resize(1000, 600)

       
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Page area
        self.pages = QStackedWidget()

        # Right-side menu
        menu_layout = QVBoxLayout()

        buttons = [
            "Setup",
            "Units",
            "Enemies",
            "Cat Combos",
            "Gameplay",
            "Reworks",
            "QoL",
        ]

        self.menu_buttons = []

        for index, name in enumerate(buttons):
            button = QPushButton(name)
            button.setProperty("navButton", True)

            button.clicked.connect(
                lambda checked=False, i=index: self.change_page(i)
            )

            menu_layout.addWidget(button)
            self.menu_buttons.append(button)

        menu_layout.addStretch()

        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)
        menu_widget.setFixedWidth(180)

        main_layout.addWidget(menu_widget)
        main_layout.addWidget(self.pages)

        # Pages
        self.setup_page = SetupWindow(self.config)
        self.setup_page.config_loaded.connect(self.refresh_from_config)

        self.pages.addWidget(self.setup_page)       # Setup
        self.pages.addWidget(UnitWindow(self.config))       # Units
        self.pages.addWidget(EnemyWindow(self.config))   # Enemies
        self.pages.addWidget(ComboWindow(self.config))       # Cat Combos
        self.pages.addWidget(QWidget())       # Gameplay
        self.pages.addWidget(QWidget())       # Reworks
        self.pages.addWidget(QWidget())       # QoL

        # Start on the first page
        self.change_page(0)

    def change_page(self, index):
        self.pages.setCurrentIndex(index)

        self.refresh_from_config()

        for i, button in enumerate(self.menu_buttons):
            button.setProperty("active", i == index)
            button.style().unpolish(button)
            button.style().polish(button)


    def refresh_from_config(self):
        for page in range(self.pages.count()):
            widget = self.pages.widget(page)

            if hasattr(widget, "refresh_from_config"):
                widget.refresh_from_config()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()