"""Measure the label blob a ROM needs, so the payload can reserve exactly that.

The hook reserves a fixed block for the rasterised labels. A ROM whose ITCM is
mostly in use cannot afford the generous default, so the payload build asks
this script how big the blob really is and reserves that much (rounded up).

    py tools/measure_labels.py <rom> <out.txt>
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import ndspy.rom

from onescreen import labels, origin


def blob_size(rom_path):
    rom = ndspy.rom.NintendoDSRom(pathlib.Path(rom_path).read_bytes())
    mf = None
    box = None
    if origin.SHA1 in __import__("hashlib").sha1(
            pathlib.Path(rom_path).read_bytes()).hexdigest():
        mf = labels.MessageFiles(origin.MSG_FILES, origin.FONT_FILE)
        box = labels.ORIGIN_BOX
    blob = labels.build(rom, log=lambda *a, **k: None, mf=mf, box=box)
    return len(blob)


def main():
    rom = sys.argv[1]
    out = sys.argv[2]
    size = blob_size(rom)
    rounded = (size + 15) & ~15
    pathlib.Path(out).write_text(f"{rounded}\n")
    print(f"label blob: {size} bytes, reserving {rounded} -> {out}")


if __name__ == "__main__":
    main()
