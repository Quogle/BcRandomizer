import tomllib

CAT_CONFIG = "config\\cat config.toml"
ENEMY_CONFIG = "config\\enemy config.toml"
GAME_CONFIG = "config\\game config.toml"


def get_settings_dict():
    # Load TOML
    with open(CAT_CONFIG, "rb") as f:
        cat_config = tomllib.load(f)
        f.close()
    # Load TOML
    with open(ENEMY_CONFIG, "rb") as f:
        enemy_config = tomllib.load(f)
        f.close()
    # Load TOML
    with open(GAME_CONFIG, "rb") as f:
        game_config = tomllib.load(f)
        f.close()
    
    settings = {
        "cat":cat_config,
        "enemy":enemy_config,
        "game":game_config,
    }
    return settings









