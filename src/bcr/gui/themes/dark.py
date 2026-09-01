DARK_THEME = """
QWidget {
    background-color: #121314;
    color: #ffffff;
}

QMainWindow {
    background-color: #121314;
}

QLabel {
    background-color: transparent;
    color: #d9d9d9;
    font-size: 14px;
}

QPushButton[navButton="true"] {
    background-color: #383b3e;
    color: #ffffff;
    border: none;
    padding: 14px;
    text-align: left;
    font-size: 14px;
    border-radius: 6px;
}

QPushButton[navButton="true"]:hover {
    background-color: #4a4d50;
}

QPushButton[navButton="true"]:pressed {
    background-color: #55585b;
}

QPushButton[navButton="true"][active="true"] {
    background-color: #9e42bf;
    color: #ffffff;
}

QPushButton[navButton="true"]:focus {
    outline: none;
}

QPushButton {
    background-color: #383b3e;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 8px 12px;
}

QPushButton:hover {
    background-color: #4a4d50;
}

QPushButton:pressed {
    background-color: #55585b;
}

QPushButton:focus {
    outline: none;
}

QGroupBox {
    background-color: #191a1b;
    border: 1px solid #2b2e31;
    border-radius: 8px;
    margin-top: 14px;
    padding: 18px;
    font-size: 16px;
    font-weight: bold;
    color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 6px;
    color: #ffffff;
}

QCheckBox {
    background-color: transparent;
    color: #d9d9d9;
    spacing: 8px;
    font-size: 14px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    background-color: #24272a;
    border: 1px solid #383b3e;
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    background-color: #9e42bf;
    border: 1px solid #9e42bf;
    border-radius: 3px;
}

QComboBox {
    background-color: #24272a;
    color: #ffffff;
    border: 1px solid #383b3e;
    border-radius: 5px;
    padding: 5px 10px;
    min-width: 45px;
}

QComboBox:hover {
    border: 1px solid #9e42bf;
}

QComboBox:focus {
    border: 1px solid #383b3e;
}

QSpinBox {
    background-color: #24272a;
    color: #ffffff;
    border: 1px solid #383b3e;
    border-radius: 5px;
    padding: 4px 6px;
    min-width: 20px;
}

QSpinBox:hover {
    border: 1px solid #9e42bf;
}

QSpinBox:focus {
    border: 1px solid #383b3e;
}

QDoubleSpinBox {
    background-color: #24272a;
    color: #ffffff;
    border: 1px solid #383b3e;
    border-radius: 5px;
    padding: 4px 6px;
    min-width: 20px;
}

QDoubleSpinBox:hover {
    border: 1px solid #9e42bf;
}

QDoubleSpinBox:focus {
    border: 1px solid #383b3e;
}

QSlider::groove:horizontal {
    background: #383b3e;
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #9e42bf;
    width: 14px;
    height: 14px;
    margin: -4px 0;
    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background: #b04fd3;
}

QScrollArea {
    background-color: #121314;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: #121314;
}

QScrollBar:vertical {
    background-color: #191a1b;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #383b3e;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4a4d50;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}
"""