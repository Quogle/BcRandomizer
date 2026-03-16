from pathlib import Path
import tomllib  # built-in TOML parser in Python 3.11+

CONFIG_FILE = Path("config.toml")

# Load TOML
with open(CONFIG_FILE, "rb") as f:
    config = tomllib.load(f)

# Example: access general seed
seed = config["general"]["seed"]
if not seed:
    import random
    seed = random.randint(100000000000, 999999999999)
print("Seed:", seed)

#access enemy ID swap settings
enemy_id_swap = config["enemy"]["id_swap"]
swap_to_similar = config["enemy"]["swap_to_similar_enemy"]
swap_ranges = config["enemy"]["swap_ranges"]

print("Enemy ID swap:", enemy_id_swap)
print("Swap to similar:", swap_to_similar)
print("Swap ranges:", swap_ranges)

#access trait setting
black_speed_boost = config["enemy"]["traits"]["gimmicks"]["black"]["speed_boost"]
print("Black speed boost:", black_speed_boost)