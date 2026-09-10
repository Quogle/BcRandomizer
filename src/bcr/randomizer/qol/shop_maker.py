import tadbcmc.data.enums.item as item
import tadbcmc.pieces.qol as qol
from ...config.defaults import DEFAULT_CONFIG






#this has no option for infinite items but also what the hell is shop buff
def make_shop(config=DEFAULT_CONFIG):
    """ does all the things pertaining to shop in the config """
    ambigus_shop_buff = config["qol"]["shop_buff"]
    cheaper_items = config["qol"]["cheaper_items"]
    leadership = config["qol"]["leadership_in_shop"]
    ototo_helper = config["qol"]["ototo_helper_in_shop"]
    cheaper_catamin = config["qol"]["cheaper_catamin"]
    infinites = True
    if not (ambigus_shop_buff or cheaper_items or cheaper_catamin or leadership or ototo_helper):
        return  #its doing nothing afterall no sense in editing shop
    #first step is Im gonna remove everything from the shop and only add back the vanilla items and catamin
    qol.clear_shop()
    qol.set_shop_item(item.shop.speed_up,9,50)
    qol.set_shop_item(item.shop.radar,2,90)
    qol.set_shop_item(item.shop.rich,7,150)
    qol.set_shop_item(item.shop.cpu,20,180)
    qol.set_shop_item(item.shop.cat_jobs,5,300)
    qol.set_shop_item(item.shop.sniper,3,90)
    qol.set_shop_item(item.shop.catamin_a,3,30)
    qol.set_shop_item(item.shop.catamin_b,3,80)
    qol.set_shop_item(item.shop.catamin_c,3,150)
    #now I can actually do all the individual things
    if cheaper_items:
        qol.set_shop_item(item.shop.speed_up,1000,10)
        qol.set_shop_item(item.shop.radar,48,50)
        qol.set_shop_item(item.shop.rich,50,30)
        qol.set_shop_item(item.shop.cpu,1000,30)
        qol.set_shop_item(item.shop.cat_jobs,100,30)
        qol.set_shop_item(item.shop.sniper,100,50)
    if cheaper_catamin:
        qol.set_shop_item(item.shop.catamin_a,30,30)
        qol.set_shop_item(item.shop.catamin_b,30,60)
        qol.set_shop_item(item.shop.catamin_c,30,90)
    if leadership:
        qol.set_shop_item(item.shop.leadership,300,10)
    if ototo_helper:
        qol.set_shop_item(item.shop.engineer,5,5)
    if infinites:
        qol.set_shop_item(item.shop.endless_cpu,1,10)
        qol.set_shop_item(item.shop.endless_rich,1,10)
        qol.set_shop_item(item.shop.endless_sniper,1,10)
















