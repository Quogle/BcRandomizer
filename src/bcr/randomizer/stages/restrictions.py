import tadbcmc.core.game_files as game_files
from tadbcmc.data.filenames import *
import tadbcmc.core.seeded_randomization as srand
import tadbcmc.core.simple_funcs as simp
from ...config.defaults import DEFAULT_CONFIG

def apply_stage_restrictions(config = DEFAULT_CONFIG):

    # SHIT TO IMPLEMENT
    # chance to give stage a restriction
    # make catamin stages have same restrictions as their normal ones
    # do not put restrictions on grind stages config

    ...

def get_stage_categories(config=DEFAULT_CONFIG):
    ''' get which map kinds are enabled from the config and put their IDs into an array '''
    categories = []

    # Main Story Chapters
    if config["stage"]["restrictions"]["categories"]["eoc"] or config["stage"]["restrictions"]["categories"]["itf"] or config["stage"]["restrictions"]["categories"]["cotc"]:
        categories.append(MAIN_STORY_MAP_ID)
    if config["stage"]["restrictions"]["categories"]["eoc"]:
        categories.append(EOC_OUTBREAK_MAP_ID)
    if config["stage"]["restrictions"]["categories"]["itf"]:
        categories.append(ITF_OUTBREAK_MAP_ID)
    if config["stage"]["restrictions"]["categories"]["cotc"]:
        categories.append(COTC_OUTBREAK_MAP_ID)
        categories.append(FILIBUSTER_INVASION_MAP_ID)
        categories.append(FILIBUSTER_INVASION_OUTBREAK_MAP_ID)

    if config["stage"]["restrictions"]["categories"]["aku_realms"]:
        categories.append(AKU_REALMS_MAP_ID)

    # Event Stages
    if config["stage"]["restrictions"]["categories"]["event"]:
        categories.append(EVENT_STAGE_MAP_ID)
        categories.append(COLLAB_MAP_ID)
        categories.append(ENIGMA_MAP_ID)
        categories.append(GAUNTLET_MAP_ID)
        categories.append(COLLAB_GAUNTLET_MAP_ID)
        categories.append(BEHEMOTH_MAP_ID)

    # Tower
    if config["stage"]["restrictions"]["categories"]["towers"]:
        categories.append(TOWER_MAP_ID)

    # Legend Chapters
    if config["stage"]["restrictions"]["categories"]["sol"]:
        categories.append(SOL_MAP_ID)
    if config["stage"]["restrictions"]["categories"]["ul"]:
        categories.append(UL_MAP_ID)
    if config["stage"]["restrictions"]["categories"]["zl"]:
        categories.append(ZL_MAP_ID)

    # Dojo
    if config["stage"]["restrictions"]["categories"]["dojo"]:
        categories.append(CATCLAW_DOJO_MAP_ID)
        categories.append(RANKING_EVENT_MAP_ID)
        categories.append(CHALLENGE_MAP_ID)

    # idk why youd enable these
    if config["stage"]["restrictions"]["categories"]["labyrinth"]:
        categories.append(LABYRINTH_MAP_ID)
    if config["stage"]["restrictions"]["categories"]["colloseum"]:
        categories.append(COLLOSEUM_MAP_ID)

    return categories

