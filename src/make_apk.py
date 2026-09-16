""" please dont delete this dab, let me know if you want it dead and let me hide it """
from bcr.apk.packs.encrypt import encrypt_pack
from bcr.apk.replace_icon import replace_icon
from bcr.apk.edit_xml import edit_manifest
from bcr.apk.build import build_apk
from bcr.apk.zipalign import zipalign_apk
from bcr.apk.sign import sign_apk
from bcr.config.defaults import DEFAULT_CONFIG
import os


workspace = "workspace"
decrypted = "decrypted"
downloadlocal = "DownloadLocal"
decoded = "decoded"
output_apk = "complete.apk"

dl_path = os.path.join(workspace,decrypted,downloadlocal)
decoded_path = os.path.join(workspace,decoded)
rebuilt_path = os.path.join(workspace,"rebuilt.apk")
aligned_path = os.path.join(workspace,"aligned.apk")
signed_path = os.path.join(workspace,output_apk)

def make_apk():
    """makes the apk"""
    encrypt_pack(game_files_dir=dl_path,pack_name=downloadlocal,output_directory=workspace,cc="en")
    replace_icon()
    edit_manifest(mod_id=DEFAULT_CONFIG["mod"]["id"])
    build_apk(decoded_directory=decoded_path,output_apk=rebuilt_path)
    zipalign_apk(input_apk=rebuilt_path,output_apk=aligned_path)
    sign_apk(input_apk=aligned_path,output_apk=signed_path)
    #now remove all the extra files
    files_in_workspace = os.listdir(workspace)
    remove_file_endings = [".apk",".idsig",".list",".pack"]
    for file in files_in_workspace:
        for each in remove_file_endings:
            if each in file and file != output_apk:
                if os.path.exists(os.path.join(workspace,file)):
                    os.remove(os.path.join(workspace,file))


make_apk()
