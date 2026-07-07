from PIL import Image

G1 = (108, 194, 74, 255)
G2 = (60, 135, 58, 255)
G3 = (160, 220, 130, 255)
W  = (255, 255, 255, 255)

D = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,1,3,3,3,3,3,3,3,3,1,0,0,0],
    [0,0,1,3,1,1,1,1,1,1,1,1,3,1,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,1,1,1,2,2,2,2,2,2,1,1,1,0,0],
    [0,1,1,1,2,4,4,4,4,4,4,2,1,1,1,0],
    [0,1,1,1,2,4,2,2,2,2,4,2,1,1,1,0],
    [0,1,1,1,2,4,2,2,2,2,4,2,1,1,1,0],
    [0,1,1,1,2,4,2,2,2,2,4,2,1,1,1,0],
    [0,1,1,1,2,4,4,4,4,4,4,2,1,1,1,0],
    [0,0,1,1,1,2,2,2,2,2,2,1,1,1,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,1,3,1,1,1,1,1,1,1,1,3,1,0,0],
    [0,0,0,1,3,3,3,3,3,3,3,3,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
]

C = {0: None, 1: G1, 2: G2, 3: G3, 4: W}

def render(size):
    scale = size // 16
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    pix = img.load()
    for gy in range(16):
        for gx in range(16):
            c = C[D[gy][gx]]
            if c is None:
                continue
            for dy in range(scale):
                for dx in range(scale):
                    x, y = gx * scale + dx, gy * scale + dy
                    if D[gy][gx] == 2 and (dx in (0, scale-1) or dy in (0, scale-1)):
                        pix[x, y] = (40, 100, 40, 255)
                    else:
                        pix[x, y] = c
    return img

# Build multi-size ICO manually
import struct

sizes = [16, 32, 48, 64]
images = [render(s) for s in sizes]

ico_path = "C:\\Users\\Manutenção\\Documents\\ProjetoPy\\icon.ico"

# ICO header: reserved(2) + type(2) + count(2)
header = struct.pack("<HHH", 0, 1, len(sizes))

# Directory entries + image data
entries = b""
all_image_data = b""
data_offset = 6 + len(sizes) * 16

for i, s in enumerate(sizes):
    img = images[i]
    w, h = s, s
    rgba = list(img.getdata())

    # BMP info header (40 bytes)
    bmp = struct.pack("<I", 40)
    bmp += struct.pack("<ii", w, h * 2)
    bmp += struct.pack("<HH", 1, 32)
    bmp += struct.pack("<IIIIII", 0, w * h * 4, 0, 0, 0, 0)

    # Pixel data bottom-up BGRA
    pixel_data = b""
    for y in range(h - 1, -1, -1):
        for x in range(w):
            r, g, b, a = rgba[y * w + x]
            pixel_data += struct.pack("BBBB", b, g, r, a)

    # AND mask (zero for 32bpp)
    and_row = ((w + 31) // 32) * 4
    and_mask = b"\x00" * (and_row * h)

    image_data = bmp + pixel_data + and_mask

    entries += struct.pack(
        "<BBBBHHII",
        w if w < 256 else 0,
        h if h < 256 else 0,
        0, 0, 1, 32,
        len(image_data),
        data_offset,
    )

    all_image_data += image_data
    data_offset += len(image_data)

with open(ico_path, "wb") as f:
    f.write(header + entries + all_image_data)

# Verify
from PyInstaller.utils.win32 import icon as ico_util
icons = list(map(ico_util.IconFile, [ico_path]))
for f in icons:
    print(f"Images: {len(f.images)}")
    for i, img in enumerate(f.images):
        print(f"  Image {i}: {len(img)} bytes")
print("OK")
