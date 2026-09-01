import tadbcmc.core.file_handler as fh
""" this module should be imported into any module actively running code that depends on tadbcmc
it is required for file search to function correctly """

fh.set_file_dir(
    DownloadLocal="C:\\Users\\tad\\Documents\\code\\bcc_windows\\mods\\quogle_npc\\patch",
    Game_files="C:\\Users\\tad\\Documents\\code\\bcc_windows\\game",
    Vanilla_store="C:\\Users\\tad\\Documents\\code\\bcc_windows\\store",
    Modded_files="C:\\Users\\tad\\Documents\\code\\bcc_windows\\modded_files"
)