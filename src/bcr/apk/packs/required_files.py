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
    requirements["server"].add(r"^\d{3}_f\.png$")


def add_catcombo_requirements(config, requirements):
    ...