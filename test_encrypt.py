from pathlib import Path

from bcr.apk.packs.encrypt import encrypt_pack


# Use the files we already decrypted
game_files_directory = (
    Path("workspace")
    / "decrypted"
    / "DownloadLocal"
)

# Where to put the newly encrypted pack
output_directory = (
    Path("workspace")
    / "encrypted"
)

pack_name = "DownloadLocal"


print(f"Input directory:  {game_files_directory}")
print(f"Output directory: {output_directory}")
print(f"Pack name:         {pack_name}")
print()


if not game_files_directory.is_dir():
    raise RuntimeError(
        f"Game files directory does not exist: "
        f"{game_files_directory}"
    )


files = [
    path
    for path in game_files_directory.iterdir()
    if path.is_file()
]

print(f"Found {len(files)} files:")

for file in files:
    print(f"  {file.name}")

print()

if not files:
    raise RuntimeError(
        f"No files found in {game_files_directory}"
    )


encrypt_pack(
    game_files_dir=game_files_directory,
    pack_name=pack_name,
    output_directory=output_directory,
    cc="en",
)

print()
print("Encryption complete.")