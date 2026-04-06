from dev.func.edit_xml import edit_manifest
from dev.func.compile_apk import compile, zipalign, sign
from dev.func.decompile_apk import find_apk, decompile
from dev.func.replace_icon import replace_icon
from dev.func.create_download_local import create_download_local
from dev.randomizer.func.nyancombo import randomize_combos
from pathlib import Path

CONFIG_PATH = Path("config.toml")

apk = find_apk()
#decompile(apk)
edit_manifest()
replace_icon()

#extract pack files here
#randomizer code
#encrypt dl here

randomize_combos()

#input("Press Enter to continue...")

create_download_local()
compile()
zipalign()
sign()
