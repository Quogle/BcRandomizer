from pathlib import Path
import xml.etree.ElementTree as ET
from config.internal_config import APP_NAME, MOD_ID, PACKAGE

BASE = Path(__file__).resolve().parents[1]
WORKSPACE = BASE / "workspace"
DECOMPILED = WORKSPACE / "decompiled"

MANIFEST = DECOMPILED / "AndroidManifest.xml"

ANDROID_NS = "http://schemas.android.com/apk/res/android"

PERMS_WITHOUT_PREFIX_LIST = [
    "com.google.android.gms.permission.AD_ID",
    "com.applovin.array.apphub.permission.BIND_APPHUB_SERVICE",
    "com.google.android.c2dm.permission.RECEIVE",
    "com.google.android.providers.gsf.permission.READ_GSERVICES",
    "com.google.android.finsky.permission.BIND_GET_INSTALL_REFERRER_SERVICE",
]

PERMS_WITH_PREFIX_LIST = [
    "jp.co.ponos.battlecatsen.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION",
    "jp.co.ponos.battlecatsen.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION"
]

def edit_manifest():
    print("Editing AndroidManifest.xml...")

    ET.register_namespace("android", ANDROID_NS)

    manifest_tree = ET.parse(MANIFEST)  # load the XML file
    manifest_root = manifest_tree.getroot()  # get the <manifest> element

    application_node = manifest_root.find("application")  # find the <application> tag

    # change the app name shown on the launcher
    application_node.set(f"{{{ANDROID_NS}}}label", APP_NAME)  # Set the app name

    # change the APK package name
    manifest_root.set("package", PACKAGE)

    # update <uses-permission> nodes
    for perm in manifest_root.findall("uses-permission"):
        name = perm.get(f"{{{ANDROID_NS}}}name")

        if name in PERMS_WITHOUT_PREFIX_LIST:
            perm.set(
                f"{{{ANDROID_NS}}}name",
                f"{PACKAGE}_{name}"
            )
        elif name in PERMS_WITH_PREFIX_LIST:
            new_name = name.replace("jp.co.ponos.battlecatsen", PACKAGE)
            perm.set(
                f"{{{ANDROID_NS}}}name",
                new_name
            )
    
    # update <permission> nodes
    for perm_node in manifest_root.findall("permission"):
        name = perm_node.get(f"{{{ANDROID_NS}}}name")
        if name in PERMS_WITH_PREFIX_LIST:
            new_name = name.replace("jp.co.ponos.battlecatsen", PACKAGE)
            perm_node.set(f"{{{ANDROID_NS}}}name", new_name)

    # Update provider authorities
    application_node = manifest_root.find("application")
    for provider_node in application_node.findall("provider"):
        authorities = provider_node.get(f"{{{ANDROID_NS}}}authorities")
        if authorities and "ponos" in authorities:
            new_authorities = authorities.replace("ponos", MOD_ID)
            provider_node.set(f"{{{ANDROID_NS}}}authorities", new_authorities)
                   

    # save the updated XML back to the file
    manifest_tree.write(MANIFEST, encoding="utf-8", xml_declaration=True)

    print("Manifest edited.")