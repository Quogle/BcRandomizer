""" module responsible for setting the conditions required by tadbcmc\n
doesnt need to be used just needs to be imported """
import tadbcmc.core.file_handler as fh
import bcr.config.paths as paths
import os
""" this module should be imported into any module actively running code that depends on tadbcmc
it is required for file search to function correctly """
fh.set_file_dir(
    DownloadLocal=paths.DOWNLOADLOCAL,
    Vanilla_store=paths.VANILLAFILES,
    Modded_files=paths.MODDEDGAMEFILES,
    Cache_files=paths.GAMECACHEFILES
)
fh.set_search_function("all in one dir")
fh.set_cache_removal(remove_cache_on_exit=False)
fh._reestablish_modded_files(
    sprite_files_path=paths.TRAITSPRITES,
    make_directories=True,
)