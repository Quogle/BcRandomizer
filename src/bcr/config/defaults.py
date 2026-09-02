DEFAULT_CONFIG = {
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
            # TODO MAKE WEIGHTS FOR EVERY FUCKING ABILITY GAHHHHHHHHHHHHHHH
        },
        "trait":{
            "randomization_mode": "randomize", # none / swap / randomize'
            "specified_swaps": [
                # { "old": "red", "new": "black"} 
            ],
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
                "mult_rounding": "Up", # Up / Down
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
                        "distance": 1600,
                        "weight": 3,
                    },
                    {
                        "count": 3,
                        "distance": 2400,
                        "weight": 3,
                    },
                    {
                        "count": 1,
                        "distance": 6000,
                        "weight": 6,
                    },
                    {
                        "count": 1,
                        "distance": 4000,
                        "weight": 10,
                    },
                    {
                        "count": 1,
                        "distance": 3000,
                        "weight": 10,
                    },
                    {
                        "count": 1,
                        "distance": 2000,
                        "weight": 10,
                    },
                    {
                        "count": 1,
                        "distance": 1000,
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
        "id_swap": {
            "enabled": True,
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
            "randomization_mode": "Randomize", # none / swap / randomize'
            "specified_swaps": [
                # { "old": "red", "new": "black"} 
            ],
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
            "mult_weights": True, # If false, chooses between the 5 combo effect multipliers at equal chance  
            "custom_mult_weights": [
                {
                    "size": 1,
                    "sm": 1,
                    "m": 1,
                    "l": 1,
                    "xl": 1,
                    "down": 1,
                }
                # TODO figure out how I actually want to 
                # structure this and do the other 4 sizes
            ],
            "keep_unit_count": True, # combos stay the sam amount of units
            "count_weights": True, # use custom weights for unit count
            "custom_count_weights": [
                {
                    "1": 10,
                    "2": 25,
                    "3": 35,
                    "4": 20,
                    "5": 10
                }
            ]
        }
    }
}