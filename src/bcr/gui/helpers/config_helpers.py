import json


def save_config(config, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


def load_config(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def connect_checkbox(widget, config, key):
    widget.setChecked(config[key])

    widget.stateChanged.connect(
        lambda state: config.__setitem__(
            key,
            widget.isChecked()
        )
    )

def connect_value(widget, config, key):
    widget.setValue(config[key])

    widget.valueChanged.connect(
        lambda value: config.__setitem__(
            key,
            value
        )
    )

def connect_combobox(widget, config, key):
    widget.setCurrentText(config[key])

    widget.currentTextChanged.connect(
        lambda value: config.__setitem__(
            key,
            value
        )
    )

def connect_weighted_list(widget, config):
    for name, spinbox in widget.items.items():
        spinbox.setValue(config[name])

        spinbox.valueChanged.connect(
            lambda value, name=name:
            config.__setitem__(
                name,
                value
            )
        )