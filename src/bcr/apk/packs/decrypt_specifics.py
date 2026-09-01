from pathlib import Path

from .decrypt import decrypt_packs


def decrypt_specifics(packs_directory,output_directory):
    """
    Decrypt the specific files needed by the randomizer.
    """

    packs_directory = Path(packs_directory)
    output_directory = Path(output_directory)

    cc = "en"

    packs = {
        "DataLocal.pack": {
            "t_unit.csv",
            "itemShopData.tsv",
            "unitbuy.csv",
            "NyancomboData.csv",
            "SkillAcquisition.csv"
        },
        "resLocal.pack": {
            "Nyancombo_en.csv",
        }
    }

    for pack_name, files in packs.items():

        pack_path = packs_directory / pack_name

        decrypt_packs(
            [pack_path],
            cc,
            output_directory,
            files,
            use_pack_directory=False,
        )

    return output_directory