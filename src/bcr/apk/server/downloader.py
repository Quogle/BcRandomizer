from pathlib import Path
import struct
import zipfile
import requests

from bcr.apk.server.cloudfront import generate_signed_cookie


SERVER_BASE_URL = "https://nyanko-assets.ponosgames.com/iphone"
from ..packs.decrypt import decrypt_packs


def get_server_url(
    country_code: str,
    game_version: int,
    index: int,
) -> str:
    project_name = f"battlecats{country_code}"

    if game_version < 1_000_000:
        str_code = f"{project_name}_{game_version}_{index}"
    else:
        str_code = (
            f"{project_name}_"
            f"{game_version // 100:06d}_"
            f"{index:02d}_"
            f"{game_version % 100:02d}"
        )

    return (
        f"{SERVER_BASE_URL}/"
        f"{project_name}/download/"
        f"{str_code}.zip"
    )


def find_server_versions(
    lib_path: str | Path,
    country_code: str,
    count: int,
) -> list[int]:
    """
    Finds the server versions stored in libnative.so
    """
    lib_data = Path(lib_path).read_bytes()

    if country_code == "jp":
        search_values = [5, 5, 5, 7_000_000]
    elif country_code == "en":
        search_values = [3, 2, 2, 6_100_000]
    elif country_code == "kr":
        search_values = [3, 2, 1, 6_100_000]
    elif country_code == "tw":
        search_values = [2, 3, 1, 6_100_000]
    else:
        raise ValueError(
            f"Unsupported country code: {country_code}"
        )

    pattern = struct.pack("<4I", *search_values)

    start_index = lib_data.find(pattern)

    if start_index == -1:
        raise ValueError(
            "Could not find server game versions in libnative.so"
        )

    end1 = lib_data.find(
        struct.pack("<I", 0xFFFFFFFF),
        start_index,
    )

    end2 = lib_data.find(
        struct.pack("<4I", 0, 0, 0, 0),
        start_index,
    )

    if end1 == -1 and end2 == -1:
        raise ValueError(
            "Could not find end of server versions in libnative.so"
        )

    if end1 == -1:
        end_index = end2
    elif end2 == -1:
        end_index = end1
    else:
        end_index = min(end1, end2)

    length = (end_index - start_index) // 4

    versions = list(
        struct.unpack_from(
            f"<{length}I",
            lib_data,
            start_index,
        )
    )

    if len(versions) < count:
        raise ValueError(
            f"Found only {len(versions)} server versions, "
            f"expected {count}"
        )

    return versions[:count]


def download_server_files(
    lib_path: str | Path,
    tsv_paths: list[str | Path],
    country_code: str,
    output_directory: str | Path,
) -> None:
    """
    Download and extract all server pack zips
    """
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    versions = find_server_versions(
        lib_path=lib_path,
        country_code=country_code,
        count=len(tsv_paths),
    )

    for index, tsv_path in enumerate(tsv_paths):
        print(
            f"Downloading server files "
            f"{index + 1}/{len(tsv_paths)}"
        )

        zip_path = download_server_zip(
            country_code=country_code,
            game_version=versions[index],
            index=index,
            output_directory=output_directory,
        )

        with zipfile.ZipFile(zip_path) as zip_file:
            zip_file.extractall(output_directory)

        zip_path.unlink()

def download_server_zip(
    country_code: str,
    game_version: int,
    index: int,
    output_directory: Path,
) -> Path:
    """
    Download a single server pack zip
    """
    url = get_server_url(
        country_code=country_code,
        game_version=game_version,
        index=index,
    )

    print(url)

    cookie = generate_signed_cookie()

    response = requests.get(
        url,
        headers={
            "accept-encoding": "gzip",
            "connection": "keep-alive",
            "cookie": cookie,
            "range": "bytes=0-",
            "user-agent": (
                "Dalvik/2.1.0 "
                "(Linux; U; Android 9; Pixel 2 "
                "Build/PQ3A.190801.002)"
            ),
        },
    )

    response.raise_for_status()

    zip_path = output_directory / f"server_{index}.zip"
    zip_path.write_bytes(response.content)

    return zip_path

def process_server_files(
    lib_path: str | Path,
    tsv_paths: list[str | Path],
    country_code: str,
    server_directory: str | Path,
    output_directory: str | Path,
    wanted_files: set[str],
) -> None:
    """
    Downloads server pack files one at a time,
    extracting only the requested files and 
    deleting the server files after
    """
    server_directory = Path(server_directory)
    output_directory = Path(output_directory)

    server_directory.mkdir(parents=True, exist_ok=True)
    output_directory.mkdir(parents=True, exist_ok=True)

    # Find the server versions stored in libnative.so
    versions = find_server_versions(
        lib_path=lib_path,
        country_code=country_code,
        count=len(tsv_paths),
    )

    for index, tsv_path in enumerate(tsv_paths):
        print(
            f"Processing server files "
            f"{index + 1}/{len(tsv_paths)}"
        )

        # Download the server zip for this version
        zip_path = download_server_zip(
            country_code=country_code,
            game_version=versions[index],
            index=index,
            output_directory=server_directory,
        )

        # Extract the server pack and list files
        with zipfile.ZipFile(zip_path) as zip_file:
            zip_file.extractall(server_directory)

        zip_path.unlink()

        pack_paths = list(server_directory.glob("*.pack"))

        # Decrypt only the needed files from the packs
        decrypt_packs(
            pack_paths=pack_paths,
            cc=country_code,
            output_directory=output_directory,
            wanted_files=wanted_files,
        )

        # Delete the server pack and list files
        for pack_path in pack_paths:
            pack_path.unlink()
            pack_path.with_suffix(".list").unlink()