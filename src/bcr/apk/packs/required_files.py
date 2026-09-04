def get_required_files(config):
    requirements = {
        "local": {},
        "server": {},
    }

    add_enemy_requirements(config, requirements)
    add_unit_requirements(config, requirements)
    add_catcombo_requirements(config, requirements)

    return requirements


def add_enemy_requirements(config, requirements):
    requirements["local"].setdefault("DataLocal.pack", set()).add("t_unit.csv")


def add_unit_requirements(config, requirements):
    if config["unit"]["talent"]["randomize"]:
        requirements["local"].setdefault("DataLocal.pack", set()).add("SkillAcquisition.csv")


def add_catcombo_requirements(config, requirements):
    ...