DEFAULT_CONFIG = {
    "enemy": {
        "id_swap": {
            "enabled": False,
            "keep_class": True, # Tries to swap enemies with enemies of the same class; ie backliner becomes different backliner
            "balanced_swap": True, # Randomizer will try to swap enemies with those of similar strength
            "balance_strictness": 10,
            "max_id": -1,   # Highest enemy id that can be selected for swapping. This is so enemies dont completely change every update. -1 to ignore this
            "adjust_magnifications": True, # Adjusts the new enemy's magnification to better match the original enemy's stats
            "include_eoc": False, # eoc cant have mags adjusted so I wouldnt recommend this one

        },
        "ability": {
            "randomize_abilities": False, # Randomizes enemy abilities, keeps the original amount
            "min_abilities": 0, # Minimum number of abilities an enemy can have
            # TODO MAKE WEIGHTS FOR EVERY FUCKING ABILITY GAHHHHHHHHHHHHHHH
        },
        "traits":{
            "mode": "randomize", # none / swap / randomize'
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
    }
}