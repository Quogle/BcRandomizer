from func.edit_xml import edit_manifest
from func.compile_apk import compile, zipalign, sign
from func.decompile_apk import find_apk, decompile
from func.replace_icon import replace_icon

import tomllib
from pathlib import Path

CONFIG_PATH = Path("config.toml")

apk = find_apk()
decompile(apk)
edit_manifest()
replace_icon()

#extract pack files here
#randomizer code
#encrypt dl here

input("Press Enter to continue...")

compile()
zipalign()
sign()

#hi
