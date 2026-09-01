from pathlib import Path

from bcr.apk.packs.decrypt import decrypt_packs


decoded_directory = Path("workspace") / "decoded"

pack_paths = [
    path
    for path in decoded_directory.rglob("*.pack")
    if "_" not in path.stem
]

print(f"Found {len(pack_paths)} pack files:")

for pack in pack_paths:
    print(f"  {pack}")

if not pack_paths:
    raise RuntimeError("No .pack files found")


decrypt_packs(
    pack_paths=pack_paths,
    cc="en",
    output_directory=Path("workspace") / "decrypted",
)