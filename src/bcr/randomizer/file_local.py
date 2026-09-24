""" module responsible for setting the conditions required by tadbcmc\n
doesnt need to be used just needs to be imported """
import tadbcmc.core.file_handler as fh
import os
""" this module should be imported into any module actively running code that depends on tadbcmc
it is required for file search to function correctly """
fh.set_file_dir(
    DownloadLocal=os.path.join("workspace","decrypted","DownloadLocal"),
    Game_files="",
    Vanilla_store=os.path.join("workspace","decrypted","vanilla_files"),
    Modded_files=os.path.join("resources","assets",)
)
fh.set_search_function("all in one dir")