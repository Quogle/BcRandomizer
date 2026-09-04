import re

def get_required_files(config):
    requirements = {
        "local": set(),
        "server": set(),
    }


    add_enemy_requirements(config, requirements)
    add_unit_requirements(config, requirements)
    add_catcombo_requirements(config, requirements)

    return requirements


def add_enemy_requirements(config, requirements):
    requirements["local"].add("t_unit.csv")


def add_unit_requirements(config, requirements):
    if config["unit"]["talent"]["randomize"]:
        requirements["local"].add("SkillAcquisition.csv")

    # TODO add required config settings

    requirements["server"].add(r"^udi\d{3}_[fcsu]\.png$")  # udi001_f.png
    requirements["server"].add(r"^uni\d{3}_[fcsu]00\.png$")  # uni001_f00.png
    requirements["server"].add(r"^\d{3}_[fcsu]\.png$")  # 001_f.png
    requirements["server"].add(r"^\d{3}_[fcsu]\.(imgcut|mamodel)$")  # 001_f.imgcut / 001_f.mamodel
    requirements["server"].add(r"^\d{3}_[fcsu]\d{2}\.maanim$")  # 001_f00.maanim
    requirements["server"].add(r"^gatyachara_\d{3}_[fz]\.png$")  # gatyachara_001_f.png

    requirements["local"].add(r"^unit\d{3}\.csv$")  # unitXXX.csv
    requirements["local"].add("unitbuy.csv")
    requirements["local"].add("SkillAcquisition.csv")
    requirements["local"].add("equipmentslot.csv")
    requirements["local"].add("unitLevel.csv")
    requirements["local"].add("unitLimit.csv")

    requirements["local"].add(r"^Unit_Explanation\d{3}_en\.csv$")  # Unit_Explanation001_en.csv


def add_catcombo_requirements(config, requirements):
    ...