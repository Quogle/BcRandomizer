import tadbcmc.core.game_files as game_files
from tadbcmc.data.filenames import *
import tadbcmc.core.seeded_randomization as srand
import tadbcmc.core.simple_funcs as simp
from ...config.defaults import DEFAULT_CONFIG

CAT_COUNT = len(game_files.get_cat_stats(vanilla=True))

def apply_stage_restrictions(config = DEFAULT_CONFIG):

    # TODO
    # make catamin stages have same restrictions as their normal ones
    # no restrictions on grind stages config

    r = srand.randinst(1000)
    map_categories = get_map_categories(config) 
    stage_count = game_files.get_number_of_stages_in_groups(update_counts=True)

    print("STAGE COUNT:")
    for category_id, maps in stage_count.items():
        print(f"Category {category_id}: {maps}")


    restrictions = game_files.file_reader("Stage_option.csv", vanilla=True)
    groups = game_files.file_reader("Charagroup.csv", vanilla=True)

    for category_id in map_categories:
        print(f"Processing category {category_id}")

        for map in range(len(stage_count[category_id])):
            print(f"    Processing map {map}")

            for stage in range(stage_count[category_id][map]):
                map_id = int(str(category_id) + f"{map:03}")    # format the map ID (ex: 13-category + 7-map = 13007)
                print(f"        Processing stage {map_id}, stage {stage}")

                if r.randrange(0, 100) < config["stage"]["restrictions"]["chance"]: # Roll for if stage gets a restriction
                    print(f"        Adding restriction to stage {map_id}, stage {stage}")

                    restriction = get_random_restriction(r, groups)
                    set_restriction(restrictions, map_id, 0, stage, restriction)

                    # Starred restrictions if enabled
                    if config["stage"]["restrictions"]["starred"]:
                        # Make restrictions different on each star level if enabled
                        if config["stage"]["restrictions"]["per_star"]:
                            restriction = get_random_restriction(r, groups)
                            set_restriction(restrictions, map_id, 1, stage, restriction)

                            restriction = get_random_restriction(r, groups)
                            set_restriction(restrictions, map_id, 2, stage, restriction)

                        else:   # share 1 star restrictions on 2 and 3 star if not
                            set_restriction(restrictions, map_id, 1, stage, restriction)
                            set_restriction(restrictions, map_id, 2, stage, restriction)

    game_files.file_writer("Charagroup.csv", groups)
    game_files.file_writer("Stage_option.csv", restrictions)


def set_restriction(restrictions, map_id, star, stage, restriction):
    row = [map_id, star, stage, *restriction]

    # Loop through existing restrictions to see if that stage already has restrictions to replace
    for i, existing in enumerate(restrictions):
        if int(existing[0]) == map_id and int(existing[1]) == star and int(existing[2]) == stage:
            restrictions[i] = row
            return

    restrictions.append(row)

def get_random_restriction(r, groups):

    restriction = [0,0,0,0,0,0]
    available = [0,1,2,3,4,5]       # restriction pointer

    while available:
        i = r.randrange(0, len(available))
        restriction_type = available.pop(i)

        if restriction_type == 0:
            restriction[0] = get_rarity_restriction(r)
        elif restriction_type == 1:
            restriction[1] = get_deploy_limit(r)
        elif restriction_type == 2:
            restriction[2] = get_row_limit()
        elif restriction_type == 3:
            restriction[3] = get_cost_lower_limit(r, restriction[4])
        elif restriction_type == 4:
            restriction[4] = get_cost_upper_limit(r, restriction[3])
        elif restriction_type == 5:
            restriction[5] = get_group_id(r, groups)

        if r.randrange(0, 100) >= 15:
            break

    return restriction

def get_rarity_restriction(r):
    available = [1, 2, 4, 8, 48]
    restriction = 0
    chances = [75, 25, 15]

    # Choose a non uber / legend rare rarity to be included
    i = r.randrange(0, 4)
    restriction += available.pop(i)

    chance_index = 0

    # Add more rarities based on the current chance
    while available and r.randrange(0, 100) < chances[chance_index]:
        i = r.randrange(0, len(available))
        restriction += available.pop(i)

        chance_index += 1

        if chance_index >= len(chances):
            break

    return restriction

def get_deploy_limit(r):
    if r.randrange(0, 100) < 20:
        return r.randrange(5, 11)
    return r.randrange(11, 41)

def get_row_limit():
    return 1

def get_cost_lower_limit(r, upper_limit=4000):
    if upper_limit == 0:
        upper_limit = 2600
    maximum = min(1800, upper_limit - 800)
    return r.randrange(0, (maximum - 300) // 5 + 1) * 5 + 300

def get_cost_upper_limit(r, lower_limit=0):
    minimum = max(1100, lower_limit + 800)
    return r.randrange(0, (4000 - minimum) // 5 + 1) * 5 + minimum

def get_group_id(r, groups):
    group_id = int(groups[-1][0]) + 1
    percent = r.randrange(8, 16) * 5    # percent between 40 and 75 in increments of 5

    group = [group_id, f"{percent}% of all units are available.", 0, 0]    # create the new group

    # add allowed cats to the group
    for cat_id in range(CAT_COUNT): 
        if r.randrange(0, 100) < percent:
            group.append(cat_id)

    groups.append(group)

    return group_id

def get_map_categories(config=DEFAULT_CONFIG):
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

