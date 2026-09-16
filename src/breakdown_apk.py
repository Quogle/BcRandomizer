from bcr.apk.extract import extract_apk
from bcr.apk.packs.decrypt import decrypt_packs
from bcr.apk.server.downloader import download_server_files,process_server_files
import os
from pathlib import Path

def _decrypt_apk(apk_path,output_dir):
    """decrypts the apk at specified path to other specified path"""
    extract_apk(apk_path,output_dir)


def _decrypt_local_packs(dir_with_packs,output_dir,henry_style_output=False):
    """ decrypts any packs found in specified directory to the specified directory
    \n if henry style, will instead output each of the packs into their own directory """
    #first get all the pack paths
    all_in_pack_location = os.listdir(dir_with_packs)
    all_packs = []
    for file in all_in_pack_location:
        if ".pack" in file:
            all_packs.append(file)
    print(all_packs)
    #now decrypt them
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not henry_style_output:
        for file in all_packs:
            decrypt_packs(
                pack_paths=os.path.join(dir_with_packs,file),
                cc="en",
                output_directory=output_dir,
                )
    else:
        #for henry style output each one into a dir of its own name
        for file in all_packs:
            this_dir = os.path.join(output_dir,file.replace(".pack",""))
            if not os.path.exists(this_dir):
                os.makedirs(this_dir)
            decrypt_packs(
                pack_paths=os.path.join(dir_with_packs,file),
                cc="en",
                output_directory=this_dir,
            )

def _download_and_decrypt_server_files(decoded_apk_dir:Path,server_packs:Path,decrypted_dir:Path):
    """ if henry it will output each server file into a dir of its own name """
    apk_lib_path = os.path.join(
                        decoded_apk_dir,
                        "lib",
                        "x86_64",
                        "libnative-lib.so",
                    )
    tsv_paths = sorted(decoded_apk_dir.rglob("download_*.tsv")) #not a fuckin clue how this works
    #start by downloading all the server files?
    download_server_files(
        lib_path=apk_lib_path,
        tsv_paths=tsv_paths,
        country_code="en",
        output_directory=server_packs,
    )
    #now get all of them
    server_pack_paths = list(
        server_packs.rglob("*.pack")
    )
    #now decrypt them
    decrypt_packs(
        pack_paths=server_pack_paths,
        cc="en",
        output_directory=os.path.join(decrypted_dir,"server")
    )



def breakdown_apk(apk_path,output_dir,henry_style=False):
    """ breaks down the apk and decrypts all the pack files """
    _decrypt_apk(apk_path=apk_path)





