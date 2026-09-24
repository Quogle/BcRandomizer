""" please dont delete this dab, let me know if you want it dead and let me hide it """
from bcr.apk.packs.encrypt import encrypt_pack
from bcr.apk.replace_icon import replace_icon
from bcr.apk.edit_xml import edit_manifest
from bcr.apk.build import build_apk
from bcr.apk.zipalign import zipalign_apk
from bcr.apk.sign import sign_apk
from bcr.config.defaults import DEFAULT_CONFIG
import os
from bcr.config.paths import*



def make_apk(output):
    """makes the apk"""
    encrypt_pack(game_files_dir=DOWNLOADLOCAL,pack_name=DOWNLOADLOCAL.stem,output_directory=WORKSPACE/"decoded"/"assets",cc="en")
    replace_icon()
    edit_manifest(mod_id=DEFAULT_CONFIG["mod"]["id"])
    build_apk(decoded_directory=DECOMPILED,output_apk=REBUILTAPK)
    zipalign_apk(input_apk=REBUILTAPK,output_apk=ALIGNEDAPK)
    sign_apk(input_apk=ALIGNEDAPK,output_apk=output)
    #now remove all the extra files
    files_in_workspace = os.listdir(WORKSPACE)
    remove_file_endings = [".apk",".idsig",".list",".pack"]
    for file in files_in_workspace:
        for each in remove_file_endings:
            if each in file and file != output:
                if os.path.exists(os.path.join(WORKSPACE,file)):
                    os.remove(os.path.join(WORKSPACE,file))


make_apk(Path(f"{DEFAULT_CONFIG['mod']['id']}.apk"))
