from pathlib import Path

from Crypto.Cipher import AES

from bcr.apk.packs.decrypt import (
    get_key_iv,
    md5_str,
)


def add_pkcs7_padding(
    data: bytes,
    block_size: int = 16,
) -> bytes:

    padding = block_size - (len(data) % block_size)

    return data + bytes([padding] * padding)


def encrypt_file(
    file_data: bytes,
    key: bytes | None,
    iv: bytes | None,
) -> bytes:

    if key is None:
        return file_data

    file_data = add_pkcs7_padding(file_data)

    if iv is None:
        cipher = AES.new(
            key,
            AES.MODE_ECB,
        )
    else:
        cipher = AES.new(
            key,
            AES.MODE_CBC,
            iv,
        )

    return cipher.encrypt(file_data)


def create_list(
    game_files_dir: Path,
    key: bytes | None,
    iv: bytes | None,
) -> str:

    files = [
        path
        for path in game_files_dir.iterdir()
        if path.is_file()
    ]

    list_file = f"{len(files)}\n"

    address = 0

    for file_path in files:

        data = file_path.read_bytes()

        encrypted_data = encrypt_file(
            data,
            key,
            iv,
        )

        length = len(encrypted_data)

        list_file += (
            f"{file_path.name},{address},{length}\n"
        )

        address += length

    return list_file


def create_pack(
    game_files_dir: Path,
    list_data: str,
    key: bytes | None,
    iv: bytes | None,
) -> bytes:

    lines = list_data.splitlines()

    entries = []

    for line in lines:

        parts = line.split(",")

        if len(parts) != 3:
            continue

        name = parts[0]
        offset = int(parts[1])
        length = int(parts[2])

        entries.append(
            (name, offset, length)
        )

    if not entries:
        return b""

    total_size = (
        entries[-1][1]
        + entries[-1][2]
    )

    pack_data = bytearray(total_size)

    for name, offset, length in entries:

        file_path = (
            game_files_dir / name
        )

        if not file_path.is_file():
            raise FileNotFoundError(
                f"File listed in pack does not exist: "
                f"{file_path}"
            )

        file_data = file_path.read_bytes()

        encrypted_data = encrypt_file(
            file_data,
            key,
            iv,
        )

        if len(encrypted_data) != length:
            raise ValueError(
                f"Size mismatch for {name}: "
                f"list says {length} bytes, "
                f"encrypted data is "
                f"{len(encrypted_data)} bytes"
            )

        pack_data[
            offset:offset + length
        ] = encrypted_data

    return bytes(pack_data)


def encrypt_list(
    list_data: str,
) -> bytes:

    data = add_pkcs7_padding(
        list_data.encode("utf-8")
    )

    key = md5_str("pack")

    cipher = AES.new(
        key,
        AES.MODE_ECB,
    )

    return cipher.encrypt(data)


def encrypt_pack(
    game_files_dir: str | Path,
    pack_name: str,
    output_directory: str | Path,
    cc: str = "en",
) -> Path:

    game_files_dir = Path(
        game_files_dir
    )

    output_directory = Path(
        output_directory
    )

    if not game_files_dir.is_dir():
        raise FileNotFoundError(
            f"Game files directory not found: "
            f"{game_files_dir}"
        )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Get pack encryption key
    key, iv = get_key_iv(
        pack_name,
        cc,
    )

    # Create list based on the actual
    # encrypted size of every file
    list_data = create_list(
        game_files_dir,
        key,
        iv,
    )

    # Encrypt list
    encrypted_list = encrypt_list(
        list_data
    )

    list_output = (
        output_directory
        / f"{pack_name}.list"
    )

    list_output.write_bytes(
        encrypted_list
    )

    # Create pack
    pack_data = create_pack(
        game_files_dir,
        list_data,
        key,
        iv,
    )

    pack_output = (
        output_directory
        / f"{pack_name}.pack"
    )

    pack_output.write_bytes(
        pack_data
    )

    print(
        f"Successfully created:\n"
        f"  {pack_output}\n"
        f"  {list_output}"
    )

    return pack_output