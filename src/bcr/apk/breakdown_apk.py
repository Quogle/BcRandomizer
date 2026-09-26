from bcr.apk.extract import extract_apk
from bcr.apk.packs.decrypt import decrypt_packs
from bcr.apk.server.downloader import download_server_files,process_server_files
import os
from pathlib import Path
import bcr.config.paths as internalPaths
import shutil

SERVER_FILE_TYPES = ["MapServer","NumberServer","UnitServer","ImageServer","ImageDataServer"]
THE_ALPHABET = "abcdefghijklmnopqrstuvwxyz".upper()


def _correctly_order_server_files(server_files:list[Path]):
    """ puts the server files in the correct order """
    correct_order = []
    #first the base ones
    for server_file in server_files:
        if server_file.stem.replace(".pack","") in SERVER_FILE_TYPES:
            correct_order.append(server_file)
    #lettered ones
    for letter in THE_ALPHABET:
        for filetype in SERVER_FILE_TYPES:
            this_filename = letter + filetype
            for server_file in server_files:
                if this_filename in server_file.stem:
                    correct_order.append(server_file)
    #now numbered ones
    server_files.sort()
    for server_file in server_files:
        if server_file not in correct_order:
            correct_order.append(server_file)
    return correct_order

def _decrypt_apk(apk_path):
    """decrypts the apk at specified path"""
    extract_apk(apk_path,internalPaths.DECOMPILED)

def _decrypt_local_packs(henry_style=False,specifics:set=None):
    """ decrypts any packs found in specified directory to the specified directory
    \n if henry style, will instead output each of the packs into their own directory """
    #first get all the pack paths
    all_packs = internalPaths.DECOMPILED.rglob("*.pack")
    pack_paths = []
    for pack in all_packs:
        if "_" not in pack.stem:
            pack_paths.append(pack)
    #get which directory to output to
    output_dir = internalPaths.VANILLAFILES
    if henry_style: output_dir = internalPaths.LOCALFILES
    #now decrypt them
    decrypt_packs(
        pack_paths=pack_paths,
        cc="en",
        output_directory=output_dir,
        use_pack_directory=henry_style,
        wanted_files=specifics,
    )
    
def _download_and_decrypt_server_files(henry_style=False,specifics:set=None,separate_into_versions=False):
    """ decrypts server files, if set is passed to specifics it will only decrpyt those
    \n henry style means it gets put into server/ImageLocal instead of vanilla files
    \n separate into versions leaves the server files in their respective version files, why would you use this? """
    tsv_paths = sorted(internalPaths.DECOMPILED.rglob("download_*.tsv")) #not a fuckin clue how this works
    if not separate_into_versions:
        #get the output dir
        output_dir = internalPaths.VANILLAFILES
        if henry_style: output_dir = internalPaths.SERVERFILES
        #now do process server files
        process_server_files(
            lib_path=internalPaths.LIBPATH,
            tsv_paths=tsv_paths,
            country_code="en",
            server_directory=internalPaths.SERVERDIRECTORY,
            wanted_files=specifics,
            output_directory=output_dir,
            use_pack_directory=henry_style,
        )
    else:
        #start by downloading all the server files
        download_server_files(
            lib_path=internalPaths.LIBPATH,
            tsv_paths=tsv_paths,
            country_code="en",
            output_directory=internalPaths.SERVERDIRECTORY,
        )
        #now get all of them
        server_pack_paths = list(
            internalPaths.SERVERDIRECTORY.rglob("*.pack")
        )
        #now order them correctly
        ordered_server_files = _correctly_order_server_files(server_pack_paths)
        #now decrypt them
        decrypt_packs(
            pack_paths=ordered_server_files,
            cc="en",
            output_directory=internalPaths.SERVERFILES
        )

def _move_all_local_and_server_files_to_vanilla_files(delete_them=True):
    """ copies all files from local and then server into vanilla, deletes them if specified """
    dirs = []
    for each in os.listdir(internalPaths.LOCALFILES):
        dirs.append(internalPaths.LOCALFILES / each)
    for each in os.listdir(internalPaths.SERVERFILES):
        dirs.append(internalPaths.SERVERFILES / each)
    for directory in dirs:
        print("moving " + directory.stem + " to vanilla_files")
        all_files = os.listdir(directory)
        for file in all_files:
            shutil.copy(directory / file,internalPaths.VANILLAFILES / file)
            if delete_them:
                os.remove(directory / file)
        if delete_them:
            os.remove(directory)
    if delete_them:
        os.remove(internalPaths.LOCALFILES)
        os.remove(internalPaths.SERVERFILES)


#working on this still
def breakdown_apk(
        apk_path:str|Path|None,
        specifics:dict[set]=None,
        get_server_files=False,
        henry_style_output=False):
    """ breaks down the apk and decrypts all the pack files
    \n passing none to apk name will make it not decrypt an apk
    \n if move files it will move all the files into vanilla files
    \n if keep local server, when it moves them to vanilla files it wont delete them """
    if apk_path != None:
        _decrypt_apk(apk_path=apk_path)
    local_specifics = None
    server_specifics = None
    if specifics != None:
        if "local" in specifics:
            local_specifics = specifics["local"]
        if "server" in specifics:
            server_specifics = specifics["server"]
    _decrypt_local_packs(henry_style=henry_style_output,specifics=local_specifics)
    if get_server_files:
        _download_and_decrypt_server_files(henry_style=henry_style_output,specifics=server_specifics)
    #if move_files_to_vanilla_files:
    #    _move_all_local_and_server_files_to_vanilla_files((not keep_those_outside_vanilla_files)) #this is largely just a relic (omg thats a bc reference)






