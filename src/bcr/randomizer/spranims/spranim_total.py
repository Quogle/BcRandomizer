
from ...config.defaults import DEFAULT_CONFIG

from ..spranims import enemy_sprites
from ..spranims import enemy_burrow_animations




#still broken for testing purposes since witch fix is broken
def total(config=DEFAULT_CONFIG,log=None,debug=False):
    """  """
    #enemy trait sprites should be done if trait rand enemy mode is not none
    enemy_trait_rand_mode = config["trait"]["enemy"]["randomize"]["randomization_mode"].lower()
    if enemy_trait_rand_mode != "none":
        do_witch = config["gameplay"]["modifications"]["old_zombies"]
        do_witch = False
        enemy_sprites.get_enemy_sprites(kill_previous=True,consider_zombie_as_witch=do_witch,debug=debug)
    #enemy burrow sprites should also only run if e trait rand mode is not none?
    if enemy_trait_rand_mode != "none":
        enemy_burrow_animations.make_burrow_anims(kill_existing=True,debug=debug) #do I need to check if anim files exist?
        












