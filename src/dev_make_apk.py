import bcr.apk.make_apk as make_apk
from bcr.config.defaults import DEFAULT_CONFIG
from pathlib import Path




make_apk.make_apk(Path(f"{DEFAULT_CONFIG['mod']['id']}.apk"))




