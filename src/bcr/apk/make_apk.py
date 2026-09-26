""" please dont delete this dab, let me know if you want it dead and let me hide it """
from bcr.apk.packs.encrypt import encrypt_pack
from bcr.apk.replace_icon import replace_icon
from bcr.apk.edit_xml import edit_manifest
from bcr.apk.build import build_apk
from bcr.apk.zipalign import zipalign_apk
from bcr.apk.sign import sign_apk
from bcr.config.defaults import DEFAULT_CONFIG
import os
from bcr.config import paths as internalPaths
from pathlib import Path



def make_apk(output:Path,config=DEFAULT_CONFIG):
    """makes the apk"""
    encrypt_pack(game_files_dir=internalPaths.DOWNLOADLOCAL,pack_name=internalPaths.DOWNLOADLOCAL.stem,output_directory=internalPaths.DOWNLOADLOCALPACK.parent,cc="en")
    replace_icon()
    edit_manifest(mod_id=config["mod"]["id"])
    build_apk(decoded_directory=internalPaths.DECOMPILED,output_apk=internalPaths.REBUILTAPK)
    zipalign_apk(input_apk=internalPaths.REBUILTAPK,output_apk=internalPaths.ALIGNEDAPK)
    sign_apk(input_apk=internalPaths.ALIGNEDAPK,output_apk=output)
    #now remove all the extra files
    files_in_workspace = os.listdir(internalPaths.WORKSPACE)
    remove_file_endings = [".apk",".idsig",".list",".pack"]
    for file in files_in_workspace:
        for each in remove_file_endings:
            if each in file and file != output:
                if os.path.exists(os.path.join(internalPaths.WORKSPACE,file)):
                    os.remove(os.path.join(internalPaths.WORKSPACE,file))



