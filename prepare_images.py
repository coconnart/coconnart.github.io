"""
CoConnArt Image Preparation Script
====================================
Run this AFTER Casey has finished picking her final images.

REQUIREMENTS:
  pip install Pillow

USAGE:
  1. Put this script in the PARENT folder above your coconnart folder
  2. Run: python prepare_images.py
  3. Optimized images will be saved into coconnart/images/ subfolders

FOLDER STRUCTURE EXPECTED:
  coconnart/
    close-ups/
    drawings/
    paintings/
    screenprints/
    sculptures/
    TL/          <-- time-lapses (videos — this script skips these)
"""

from PIL import Image
import os
import re

# ── CONFIG ──────────────────────────────────────────────
SOURCE_ROOT   = "coconnart"          # your existing folder
OUTPUT_ROOT   = "coconnart/images"   # where web-ready images go
MAX_WIDTH     = 2000                 # pixels — enough for full-screen on retina
JPEG_QUALITY  = 82                   # 82 is a good balance of quality and filesize

# Map your folder names to output subfolder names
FOLDER_MAP = {
    "paintings":    "paintings",
    "drawings":     "drawings",
    "sculptures":   "sculptures",
    "screenprints": "screenprints",
    "close-ups":    "closeups",
    # TL (timelapses) are videos — skip
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".bmp"}
# ─────────────────────────────────────────────────────────


def slugify(name):
    """Turn a filename into a clean web-safe slug."""
    name = os.path.splitext(name)[0]          # remove extension
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)  # replace non-alphanumeric with dash
    name = name.strip('-')
    return name


def prepare_image(src_path, dst_path):
    """Open, resize if needed, and save as optimized JPEG."""
    with Image.open(src_path) as img:
        # Convert to RGB (handles TIFF, PNG with alpha, CMYK, etc.)
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode in ("RGBA","LA") else None)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Resize if wider than MAX_WIDTH (preserve aspect ratio)
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_size = (MAX_WIDTH, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
            print(f"    Resized: {img.width}×{img.height}")

        img.save(dst_path, "JPEG", quality=JPEG_QUALITY, optimize=True)


def main():
    total = 0
    skipped = 0

    for src_folder, dst_folder in FOLDER_MAP.items():
        src_dir = os.path.join(SOURCE_ROOT, src_folder)
        dst_dir = os.path.join(OUTPUT_ROOT, dst_folder)

        if not os.path.isdir(src_dir):
            print(f"⚠  Folder not found, skipping: {src_dir}")
            continue

        os.makedirs(dst_dir, exist_ok=True)
        files = sorted(os.listdir(src_dir))
        img_files = [f for f in files if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]

        print(f"\n📁 {src_folder}/ → images/{dst_folder}/  ({len(img_files)} images)")

        for i, filename in enumerate(img_files, start=1):
            src_path = os.path.join(src_dir, filename)
            slug = slugify(filename)
            if not slug:
                slug = f"{dst_folder}-{i:02d}"
            dst_name = f"{dst_folder}-{i:02d}-{slug}.jpg"
            dst_path = os.path.join(dst_dir, dst_name)

            if os.path.exists(dst_path):
                print(f"  ✓ Already exists, skipping: {dst_name}")
                skipped += 1
                continue

            try:
                print(f"  → {filename}  ⟶  {dst_name}")
                prepare_image(src_path, dst_path)
                total += 1
            except Exception as e:
                print(f"  ✗ Error processing {filename}: {e}")

    print(f"\n✅ Done. {total} images prepared, {skipped} skipped.")
    print(f"   Output: {os.path.abspath(OUTPUT_ROOT)}")
    print("\nNext step: copy the coconnart/images/ folder into your")
    print("GitHub repository and update the gallery.html image src paths.")


if __name__ == "__main__":
    main()
