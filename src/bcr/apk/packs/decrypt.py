from pathlib import Path
import hashlib
import re

from Crypto.Cipher import AES

SERVER_PACK_TYPES = [
    "UnitServer",
    "NumberServer",
    "ImageDataServer",
    "ImageServer",
    "MapServer",
]

EN_KEY = bytes([
    0x0A, 0xD3, 0x9E, 0x4A,
    0xEA, 0xF5, 0x5A, 0xA7,
    0x17, 0xFE, 0xB1, 0x82,
    0x5E, 0xDE, 0xF5, 0x21,
])

EN_IV = bytes([
    0xD1, 0xD7, 0xE7, 0x08,
    0x09, 0x19, 0x41, 0xD9,
    0x0C, 0xDF, 0x8A, 0xA5,
    0xF3, 0x0B, 0xB0, 0xC2,
])

JP_KEY = bytes([
    0xD7, 0x54, 0x86, 0x8D,
    0xE8, 0x9D, 0x71, 0x7F,
    0xA9, 0xE7, 0xB0, 0x6D,
    0xA4, 0x5A, 0xE9, 0xE3,
])

JP_IV = bytes([
    0x40, 0xB2, 0x13, 0x1A,
    0x9F, 0x38, 0x8A, 0xD4,
    0xE5, 0x00, 0x2A, 0x98,
    0x11, 0x8F, 0x61, 0x28,
])

KR_KEY = bytes([
    0xBE, 0xA5, 0x85, 0xEB,
    0x99, 0x32, 0x16, 0xEF,
    0x4D, 0xCB, 0x88, 0xB6,
    0x25, 0xC3, 0xDF, 0x98,
])

KR_IV = bytes([
    0x9B, 0x13, 0xC2, 0x12,
    0x1D, 0x39, 0xF1, 0x35,
    0x3A, 0x12, 0x5F, 0xED,
    0x98, 0x69, 0x66, 0x49,
])

TW_KEY = bytes([
    0x31, 0x3D, 0x98, 0x58,
    0xA7, 0xFB, 0x93, 0x9D,
    0xEF, 0x1D, 0x7D, 0x85,
    0x96, 0x29, 0x08, 0x7D,
])

TW_IV = bytes([
    0x0E, 0x37, 0x43, 0xEB,
    0x53, 0xBF, 0x59, 0x44,
    0xD1, 0xAE, 0x7E, 0x10,
    0xC2, 0xE5, 0x4B, 0xDF,
])


def remove_pkcs7_padding(data: bytes) -> bytes:
    if not data:
        return data

    padding = data[-1]

    return data[:-padding]


def md5_str(string: str, length: int = 8) -> bytes:
    return (
        bytearray(
            hashlib.md5(string.encode("utf-8")).digest()[:length]
        )
        .hex()
        .encode("utf-8")
    )


def unpack_list(list_path: Path) -> bytes:
    data = list_path.read_bytes()

    key = md5_str("pack")

    cipher = AES.new(key, AES.MODE_ECB)

    decrypted = cipher.decrypt(data)

    return remove_pkcs7_padding(decrypted)


def decrypt_pack(
    chunk_data: bytes,
    key: bytes | None,
    iv: bytes | None,
) -> bytes:

    if key is None:
        return chunk_data

    if len(chunk_data) % AES.block_size != 0:
        raise ValueError(
            f"Pack chunk is not AES block aligned: "
            f"{len(chunk_data)} bytes"
        )

    if iv is None:
        cipher = AES.new(key, AES.MODE_ECB)
    else:
        cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = cipher.decrypt(chunk_data)

    return remove_pkcs7_padding(decrypted)


def get_key_iv(
    pack_name: str,
    cc: str,
) -> tuple[bytes | None, bytes | None]:

    pack_name = pack_name.lower()

    if pack_name in (
        "imagedatalocal",
        "imgcutlocal",
        "modellocal",
    ):
        return None, None

    if "server" in pack_name:
        return b"89a0f99078419c28", None

    if cc == "en":
        return EN_KEY, EN_IV

    if cc == "jp":
        return JP_KEY, JP_IV

    if cc == "kr":
        return KR_KEY, KR_IV

    if cc == "tw":
        return TW_KEY, TW_IV

    raise ValueError(f"Unsupported region: {cc}")


def unpack_pack(
    pack_path: Path,
    list_data: bytes,
    key: bytes | None,
    iv: bytes | None,
    output_directory: Path,
    wanted_files: set[str] | None = None,
) -> None:

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    pack_data = pack_path.read_bytes()
    list_data = list_data.decode("utf-8")

    lines = list_data.split("\n")

    for line in lines:

        file = line.split(",")

        if len(file) < 3:
            continue

        name = file[0]

        # Skip files that aren't requested
        if not is_wanted_file(name, wanted_files):
            continue

        start_offset = int(file[1])
        length = int(file[2])

        chunk = pack_data[
            start_offset:start_offset + length
        ]

        decrypted = decrypt_pack(
            chunk,
            key,
            iv,
        )

        output_path = output_directory / name

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_bytes(decrypted)

def is_wanted_file(name, wanted_files):

    if wanted_files is None:
        return True

    if name in wanted_files:
        return True

    return bool(re.fullmatch(r"unit\d+\.csv", name))

def decrypt_packs(
    pack_paths: list[str | Path],
    cc: str,
    output_directory: str | Path,
    wanted_files: set[str] | None = None,
    use_pack_directory: bool = True,
) -> Path:

    output_directory = Path(output_directory)

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    pack_paths = sorted(
        pack_paths,
        key=lambda path: (
            0 if Path(path).stem in SERVER_PACK_TYPES
            else 2 if re.search(r"\d{6}", Path(path).stem)
            else 1,
        )
    )

    for pack_path in pack_paths:

        pack_path = Path(pack_path)

        print(f"\nDecrypting: {pack_path}")

        if not pack_path.is_file():
            raise FileNotFoundError(
                f"Pack file not found: {pack_path}"
            )

        list_path = pack_path.with_suffix(".list")

        print(f"List file: {list_path}")

        if not list_path.is_file():
            raise FileNotFoundError(
                f"List file not found: {list_path}"
            )

        pack_name = pack_path.stem

        if use_pack_directory:
            if "server" in pack_name.lower():
                pack_type = next(
                    (
                        pack_type
                        for pack_type in SERVER_PACK_TYPES
                        if pack_type.lower() in pack_name.lower()
                    ),
                    pack_name,
                )
                pack_output = output_directory / pack_type
            else:
                pack_output = output_directory / pack_name
        else:
            pack_output = output_directory

        print(f"Pack name: {pack_name}")

        key, iv = get_key_iv(
            pack_name,
            cc,
        )

        print("Decrypting list...")
        list_data = unpack_list(list_path)

        print(f"Extracting to: {pack_output}")

        unpack_pack(
            pack_path,
            list_data,
            key,
            iv,
            pack_output,
            wanted_files,
        )

    return output_directory