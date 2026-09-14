from bcr.apk.packs.encrypt import encrypt_pack
from bcr.apk.replace_icon import replace_icon
from bcr.apk.edit_xml import edit_manifest
from bcr.apk.build import build_apk
from bcr.apk.zipalign import zipalign_apk
from bcr.apk.sign import sign_apk
from bcr.config.defaults import DEFAULT_CONFIG
import os
def get_path(list):
    the_path = list[0]
    for x in range(1,len(list)):
        the_path = os.path.join(the_path,list[x])
    return the_path

workspace = "workspace"
dl_path_names = [workspace,"decrypted","DownloadLocal"]
decoded_path_names = [workspace,"decoded"]
rebuilt_path_names = [workspace,"rebuilt.apk"]
aligned_path_names = [workspace,"aligned.apk"]
signed_path_names = [workspace,"signed.apk"]
dl_path = get_path(dl_path_names)
decoded_path = get_path(decoded_path_names)
rebuilt_path = get_path(rebuilt_path_names)
aligned_path = get_path(aligned_path_names)
signed_path = get_path(signed_path_names)

encrypt_pack(game_files_dir=dl_path,pack_name=dl_path_names[-1],output_directory=workspace,cc="en")
replace_icon()
edit_manifest(mod_id=DEFAULT_CONFIG["mod"]["id"])
build_apk(decoded_directory=decoded_path,output_apk=rebuilt_path)
zipalign_apk(input_apk=rebuilt_path,output_apk=aligned_path)
sign_apk(input_apk=aligned_path,output_apk=signed_path)



