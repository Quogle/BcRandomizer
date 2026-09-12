DEFAULT_CONFIG = {
    "mod": {
        "seed": None,
        "id": "bcrando"
    },
    "enemy": {
        "randomization": {
            # None          -   Enemies are not randomized
            # ID Swap       -   Every instance of doge is randomized into ____, etc
            # Fully Random  -   Randomization is different for every stage
            "type": "Fully Random", 
            "keep_class": True,             # peons stay as peons, basically enemies will randomize into similar types ish kinda?????
            "variant_swap": False,          # enemies will randomize into their variants if they have any
            "max_id": -1,                   # Highest enemy id that can be selected for swapping. This is so enemies dont completely change every update. -1 to ignore this
            "adjust_magnifications": True,  # Adjusts the new enemy's magnification to better match the original enemy's stats
            "include_eoc": False,           # eoc cant have mags adjusted so I wouldnt recommend this one

        },
        "ability": {
            "randomize_abilities": False, # Randomizes enemy abilities, keeps the original amount
            "min_abilities": 0, # Minimum number of abilities an enemy can have
            "weights": {
                "weaken" : 0,
                "freeze": 0,
                "slow": 0,
                "knockback": 0,
                "warp": 0,
                "curse": 0,
                "dodge": 0,
                "strengthen": 0,
                "survive": 0,
                "base_destroy": 0,
                "crit": 0,
                "savage": 0,
                "wave": 0,
                "mini_wave": 0,
                "surge": 0,
                "mini_surge": 0,
                "explosion": 0,
                "counter_surge": 0,
                "wave_block": 0,
                "single_atk": 0,
                "area_atk": 0,
                "long_distance": 0,
                "omni_strike": 0,
                "weaken_immune": 0,
                "freeze_immune": 0,
                "slow_immune": 0,
                "kb_immune": 0,
                "wave_immune": 0,
                "surge_immune": 0,
                "explosion_immune": 0,
                "warp_immune": 0,
                "curse_immune": 0,
                "toxic_immune": 0,
            },
        },
        "trait":{
            "randomization_mode": "randomize", # none / swap / randomize'
            "untraited_get_trait": True
        },
        "trait_gimmicks": {
            "white": {
                "enabled": True,
                "sage": True,
                "sage_resist_mult": 30,
            },

            "red": {
                "enabled": True,
                "speed_mult": 0.8,
                "kb_mult": 0.5,
                "mult_rounding": "Down", # Up / Down
            },

            "floating": {
                "enabled": True,
                "abilities": {
                    "Wave Immunity": 5,
                    "Surge Immunity": 5,
                    "Explosion Immunity": 3,
                    "Counter-Surge": 5,
                    "Wave Block": 3,
                },
                "dual_ability_chance": 40,
            },

            "dark": {
                "enabled": True,
                "speed_boosts": [
                    {
                        "threshold": 3.0,
                        "multiplier": "Additive",
                        "boost": 3.0,
                    },
                    {
                        "threshold": 15.0,
                        "multiplier": "Multiplicative",
                        "boost": 1.8,
                    },
                    {
                        "threshold": 1000.0,
                        "multiplier": "Multiplicative",
                        "boost": 1.5,
                    },
                ],
                "knockback_mult": 1.5,
                "mult_rounding": "Up",
            },

            "angel": {
                "enabled": True,
                "balanced": True,
                "speed_mult": 1.3,
                "attack_mult": 0.8,
                "health_mult": 1.3,
                "rounding": "Up",
            },

            "alien": {
                "enabled": True,
                "abilities": {
                    "Freeze": 5,
                    "Slow": 5,
                    "Knockback": 5,
                    "Weaken": 5,
                    "Wave": 2,
                    "Surge": 2,
                    "Explosion": 0,
                    "Critical Hit": 5,
                    "Savage Blow": 5,
                    "Lethal": 4,
                    "Base Destroyer": 5,
                    "Multihit": 3,
                },
                "starred_frequency": 30,
                "warp_frequency": 60,
                "barrier_frequency": 50,
            },

            "zombie": {
                "enabled": True,
                "balanced": True,
                "grant_revive": True,
                "revive_frequency": 100,
                "revive_types": [
                    {
                        "count": -1,
                        "hp": 100,
                        "delay": 30,
                        "weight": 5,
                    },
                    {
                        "count": -1,
                        "hp": 10,
                        "delay": 200,
                        "weight": 5,
                    },
                    {
                        "count": 3,
                        "hp": 50,
                        "delay": 90,
                        "weight": 10,
                    },
                    {
                        "count": 1,
                        "hp": 100,
                        "delay": 300,
                        "weight": 10,
                    },
                    {
                        "count": 1,
                        "hp": 50,
                        "delay": 240,
                        "weight": 10,
                    },
                    {
                        "count": 1,
                        "hp": 100,
                        "delay": 900,
                        "weight": 5,
                    },
                    {
                        "count": 2,
                        "hp": 10,
                        "delay": 30,
                        "weight": 5,
                    },
                    {
                        "count": 1,
                        "hp": 10,
                        "delay": 180,
                        "weight": 10,
                    },
                ],
                "grant_burrow": True,
                "burrow_frequency": 70,
                "burrow_types": [
                    {
                        "count": -1,
                        "distance": 400,
                        "weight": 3,
                    },
                    {
                        "count": 3,
                        "distance": 600,
                        "weight": 3,
                    },
                    {
                        "count": 1,
                        "distance": 1500,
                        "weight": 6,
                    },
                    {
                        "count": 1,
                        "distance": 1000,
                        "weight": 10,
                    },
                    {
                        "count": 1,
                        "distance": 750,
                        "weight": 10,
                    },
                    {
                        "count": 1,
                        "distance": 500,
                        "weight": 10,
                    },
                    {
                        "count": 1,
                        "distance": 250,
                        "weight": 5,
                    },
                ],
            },

            "relic": {
                "enabled": True,
                "curse": True,
                "pierce": True,
                "pierce_attack": 10,
                "pierce_range": 5,
            },

            "aku": {
                "enabled": True,
                "shield_frequency": 50,
                "ds_frequency": 50,
                "ds_ability_frequency": 50,
                "ds_ability_mini": True,
            },

            "metal": {
                "enabled": True,
            },
        }
    },
    "unit": {
        "randomization": {
            "enabled": True,        # randomizes units into other units
            "keep_rarity": False,   # Units will randomize into the same rarity
            "keep_uber_lr": True,   # Ubers and Legend Rares cannot randomize into lower rarities
        },
        "ability": {
            "randomize": True,
            "grant_trait_abilities": True, # Cats that gain zombie target get zkill, etc
            "remove_trait_abilities": True, # Cats that lose zombie target lose zkill, etc
            "zkill_frequency": 80,
            "curse_immune_frequency": 100,
            "shield_pierce_frequency": 20,
        },
        "trait": {
            "randomization_mode": "Randomize", # none / swap / randomize        # WILL ONLY RANDOMIZE TO TRAITS ENEMIES CAN HAVE
            "vary_form_traits": False, # Each form of a unit will randomize individually
            "avoid_old_traits": True # If possible unit will not randomize to target the same trait
        },
        "talent": {
            "randomize": True,
            "avoid_dupe_traits": True # Will not get a trait talent for a trait it already targets
            # TODO the rest
        }
    },
    "catcombo": {
        "randomize": {
            "enabled": True, # Randomize Cat Combos
            "units": True, # Randomize the units within catcombos
            "multipliers": True, # Randomize Combo Size DOWN, SM, M, L, XL
            "effects": True, # Randomize the effect of each combo
            "max_uber_count": 1, # Maximum amount of ubers / legend rares that can be put in a combo
        },
        "blacklist": {
            "collab": False, # collab unis can be in combos
            "version_exclusive": False,
            "unobtainable": False,
            "limited": False, # limited units such as capsule
        },
        "size": {
            "keep_unit_count": True, # combos stay the sam amount of units
                "custom_count_weights": {
                    "1": 10,
                    "2": 25,
                    "3": 35,
                    "4": 20,
                    "5": 10,
                },
           "custom_mult_weights": {
                1: {
                    "sm": 1,
                    "m": 1,
                    "l": 1,
                    "xl": 1,
                    "down": 1,
                },
                2: {
                    "sm": 1,
                    "m": 1,
                    "l": 1,
                    "xl": 1,
                    "down": 1,
                },
                3: {
                    "sm": 1,
                    "m": 1,
                    "l": 1,
                    "xl": 1,
                    "down": 1,
                },
                4: {
                    "sm": 1,
                    "m": 1,
                    "l": 1,
                    "xl": 1,
                    "down": 1,
                },
                5: {
                    "sm": 1,
                    "m": 1,
                    "l": 1,
                    "xl": 1,
                    "down": 1,
                }
            }
        }
    },
    "gameplay": {
        "modifications": {
            "metal_rework": True,
            "remove_behemoths": False,
            "behemoth_rebalance": False,
            "old_zombies": True,
            "buff_weak_aliens": True,
            "remove_itf_crystals": True,
            "remove_cotc_crystals": True,
        },
        "unit_reworks": {
            "courier": True,
            "critters":True,
            "collabs":True,
            "cop": True,
            "monenekos":True,
            "lugas":True,
            "seasonals":True,
        },
    },
    "qol": {
        "behemoth_cube_buff": True,
        "enigma_buff": True,
        "weekday_specials": True,
        "weekend_lils": True,
        "xp_stage_item_farming": True,
        "shop_buff": True,
        "cheaper_items": True,
        "leadership_in_shop": True,
        "ototo_helper_in_shop": True,
        "cheap_catamin": True,
        "unit_sell_increase": True,
        "free_orb_removal": True,
        "guarantee_advent_drops": True,

        "stage_changes": {
            "seasonals_in_sol": True,
            "collabs_in_sol_advents": True,
            "collab_tf_as_advents": True,
            "mission_collab_special_tf_drop": True,
            "buff_normal_catfruit_catamins": True,
            "split_normal_catfruit_stages": True,
            "jubilee_always_epic": True,
            "relic_aku_in_island": True,
            "orb_stage_has_strong_massive_resist": True,
            "orb_stage_has_ability_orb": True,
        },
        "drop_buffs": {
            "gstrange_buff": True,
            "growing_aku_buff": True,
            "growing_epic_buff": True,
            "sol_xp_buff": True,
            "weekend_stage_buff": True,
            "megablitz_buff": True,
            "colosseum_buff": True,
            "merciless_xp_buff": True,
            "material_stage_buff": True,
            "proving_grounds_buff": True,
            "hate_metal_hippoe_buff": True,
            "siege_buff": True,
            "facing_danger_buff": True,
            "orb_stage_buff": True,
        },
    },
    "funny": {
        "youcan_warning": False,
        "special_surprise": True,
        "angel_squirrel": False,
    }
}