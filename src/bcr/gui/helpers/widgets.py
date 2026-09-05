from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QSlider,
    QGridLayout
)


class NoWheelSlider(QSlider):

    def wheelEvent(self, event):
        event.ignore()

class NoWheelQComboBox(QComboBox):
    
    def wheelEvent(self, event):
        event.ignore()

class NoWheelSpinBox(QSpinBox):

    def wheelEvent(self, event):
        event.ignore()


class NoWheelDoubleSpinBox(QDoubleSpinBox):

    def wheelEvent(self, event):
        event.ignore()


class WeightedList(QWidget):

    def __init__(self, items=None):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

        self.items = {}

        if items:
            for name, weight in items:
                self.add_item(name, weight)

    def add_item(self, name, weight=1):

        row = QWidget()
        row_layout = QHBoxLayout(row)

        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)

        label = QLabel(name)

        weight_spin = NoWheelSpinBox()
        weight_spin.setRange(0, 999)
        weight_spin.setValue(weight)
        weight_spin.setPrefix("Weight: ")

        row_layout.addWidget(label)
        row_layout.addStretch()
        row_layout.addWidget(weight_spin)

        self.layout.addWidget(row)

        self.items[name] = weight_spin

    def get_weights(self):

        return {
            name: spin.value()
            for name, spin in self.items.items()
        }


class WeightedGrid(QWidget):

    def __init__(self, items=None, columns=2, names=None):
        super().__init__()

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(12)
        self.layout.setVerticalSpacing(6)

        self.columns = columns
        self.names = names or {}
        self.items = {}

        if items:
            for name, weight in items:
                self.add_item(name, weight)

    def add_item(self, name, weight=1):

        row = QWidget()
        row_layout = QHBoxLayout(row)

        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)

        label = QLabel(self.names.get(name, name))
        label.setStyleSheet("""
            padding: 0px 2px;
        """)

        weight_spin = NoWheelSpinBox()
        weight_spin.setRange(0, 999)
        weight_spin.setValue(weight)

        row_layout.addWidget(label)
        row_layout.addStretch()
        row_layout.addWidget(weight_spin)

        index = len(self.items)
        self.layout.addWidget(
            row,
            index // self.columns,
            index % self.columns
        )

        self.items[name] = weight_spin

    def get_weights(self):

        return {
            name: spin.value()
            for name, spin in self.items.items()
        }




