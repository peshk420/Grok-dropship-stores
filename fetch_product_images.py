#!/usr/bin/env python3
"""Download supplier photos from AliExpress CDN and apply original storefront edits."""

import json
import os
import urllib.request
from io import BytesIO

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.aliexpress.com/"}

with open(os.path.join(ROOT, "supplier_urls.json")) as f:
    CATEGORY_URLS = json.load(f)

CATEGORY_ALIASES = {
    "Cooling Gear": "Pet Cooling",
    "Hydration": "Pet Cooling",
    "Outdoor Comfort": "Pet Cooling",
    "Travel": "Pet Cooling",
    "Sun Protection": "Pet Cooling",
    "Grooming": "Pet Cooling",
    "Safety": "Safety",
}

# Legacy inline fallback (unused when supplier_urls.json present)
_LEGACY = {
    "Pool Care": [
        "https://ae01.alicdn.com/kf/S5e8e7af41e864b6b8fdb8effd1a56521P.jpg",
        "https://ae01.alicdn.com/kf/Se9d263380b37437b9be808d368e08757s.jpg",
        "https://ae01.alicdn.com/kf/Sc8d01191706342ef94476b9f13cca889H.jpg",
        "https://ae01.alicdn.com/kf/Sc71ecd4fa39b466bb5404afa5f78077cQ.jpg",
    ],
    "Lawn Care": [
        "https://ae01.alicdn.com/kf/S2080c1ddceb94e9aa8f774e801f0ec8ct.jpg",
        "https://ae01.alicdn.com/kf/S3eeb319d74ee4ce585d7f9206e5199e2K.jpg",
        "https://ae01.alicdn.com/kf/Sc50d70783d6a4a1ca7b59dbbcdd027e6X.jpg",
    ],
    "Home Care": [
        "https://ae01.alicdn.com/kf/S39716d6cb6954ed48182721fb9834121W.jpg",
        "https://ae01.alicdn.com/kf/Sb52e3bee678b40f3bb1da8943f9fe3a5L.jpg",
        "https://ae01.alicdn.com/kf/S5483274b4d1e4fb896d4005e3d217a9f2.jpg",
    ],
    "Women's Fashion": [
        "https://ae01.alicdn.com/kf/S18ae61460fb54945929e9375849ddb4ex.jpg",
        "https://ae01.alicdn.com/kf/Sc4f70f4ba78d4ef6b8f5326102b682f7A.jpg",
    ],
    "Men's Fashion": [
        "https://ae01.alicdn.com/kf/S18ae61460fb54945929e9375849ddb4ex.jpg",
        "https://ae01.alicdn.com/kf/Sc4f70f4ba78d4ef6b8f5326102b682f7A.jpg",
    ],
    "Kids' Fashion": [
        "https://ae01.alicdn.com/kf/S4026be9e13d74ce4ad346ab3779be429u.jpg",
        "https://ae01.alicdn.com/kf/S18ae61460fb54945929e9375849ddb4ex.jpg",
    ],
    "Accessories": [
        "https://ae01.alicdn.com/kf/S5483274b4d1e4fb896d4005e3d217a9f2.jpg",
        "https://ae01.alicdn.com/kf/Sb52e3bee678b40f3bb1da8943f9fe3a5L.jpg",
    ],
    "Beach Essentials": [
        "https://ae01.alicdn.com/kf/Sc4f70f4ba78d4ef6b8f5326102b682f7A.jpg",
        "https://ae01.alicdn.com/kf/S18ae61460fb54945929e9375849ddb4ex.jpg",
    ],
    "Pool Products": [
        "https://ae01.alicdn.com/kf/S5e8e7af41e864b6b8fdb8effd1a56521P.jpg",
        "https://ae01.alicdn.com/kf/Sc71ecd4fa39b466bb5404afa5f78077cQ.jpg",
    ],
    "Air Conditioning": [
        "https://ae01.alicdn.com/kf/S39716d6cb6954ed48182721fb9834121W.jpg",
        "https://ae01.alicdn.com/kf/Sb52e3bee678b40f3bb1da8943f9fe3a5L.jpg",
    ],
    "Personal Fans": [
        "https://ae01.alicdn.com/kf/S5483274b4d1e4fb896d4005e3d217a9f2.jpg",
        "https://ae01.alicdn.com/kf/Sc50d70783d6a4a1ca7b59dbbcdd027e6X.jpg",
    ],
    "Coolers": [
        "https://ae01.alicdn.com/kf/S3eeb319d74ee4ce585d7f9206e5199e2K.jpg",
        "https://ae01.alicdn.com/kf/Sc8d01191706342ef94476b9f13cca889H.jpg",
    ],
    "Cooling Accessories": [
        "https://ae01.alicdn.com/kf/S39716d6cb6954ed48182721fb9834121W.jpg",
        "https://ae01.alicdn.com/kf/Se9d263380b37437b9be808d368e08757s.jpg",
    ],
    "Cooling Gear": [
        "https://ae01.alicdn.com/kf/S4026be9e13d74ce4ad346ab3779be429u.jpg",
    ],
    "Hydration": [
        "https://ae01.alicdn.com/kf/S4026be9e13d74ce4ad346ab3779be429u.jpg",
        "https://ae01.alicdn.com/kf/Sc4f70f4ba78d4ef6b8f5326102b682f7A.jpg",
    ],
    "Outdoor Comfort": [
        "https://ae01.alicdn.com/kf/S4026be9e13d74ce4ad346ab3779be429u.jpg",
        "https://ae01.alicdn.com/kf/S5e8e7af41e864b6b8fdb8effd1a56521P.jpg",
    ],
    "Travel": [
        "https://ae01.alicdn.com/kf/S5483274b4d1e4fb896d4005e3d217a9f2.jpg",
        "https://ae01.alicdn.com/kf/S3eeb319d74ee4ce585d7f9206e5199e2K.jpg",
    ],
    "Sun Protection": [
        "https://ae01.alicdn.com/kf/S18ae61460fb54945929e9375849ddb4ex.jpg",
    ],
    "Grooming": [
        "https://ae01.alicdn.com/kf/S4026be9e13d74ce4ad346ab3779be429u.jpg",
    ],
    "Safety": [
        "https://ae01.alicdn.com/kf/Sc71ecd4fa39b466bb5404afa5f78077cQ.jpg",
        "https://ae01.alicdn.com/kf/Sc8d01191706342ef94476b9f13cca889H.jpg",
    ],
    "Camping": [
        "https://ae01.alicdn.com/kf/Sc50d70783d6a4a1ca7b59dbbcdd027e6X.jpg",
        "https://ae01.alicdn.com/kf/S3eeb319d74ee4ce585d7f9206e5199e2K.jpg",
        "https://ae01.alicdn.com/kf/Sc71ecd4fa39b466bb5404afa5f78077cQ.jpg",
    ],
    "Bug Protection": [
        "https://ae01.alicdn.com/kf/Sb52e3bee678b40f3bb1da8943f9fe3a5L.jpg",
        "https://ae01.alicdn.com/kf/Se9d263380b37437b9be808d368e08757s.jpg",
    ],
    "Lighting": [
        "https://ae01.alicdn.com/kf/S39716d6cb6954ed48182721fb9834121W.jpg",
        "https://ae01.alicdn.com/kf/Sc8d01191706342ef94476b9f13cca889H.jpg",
    ],
    "Hiking": [
        "https://ae01.alicdn.com/kf/Sc50d70783d6a4a1ca7b59dbbcdd027e6X.jpg",
        "https://ae01.alicdn.com/kf/S2080c1ddceb94e9aa8f774e801f0ec8ct.jpg",
    ],
    "Cooking": [
        "https://ae01.alicdn.com/kf/Sc71ecd4fa39b466bb5404afa5f78077cQ.jpg",
        "https://ae01.alicdn.com/kf/S5e8e7af41e864b6b8fdb8effd1a56521P.jpg",
    ],
    "Power": [
        "https://ae01.alicdn.com/kf/S39716d6cb6954ed48182721fb9834121W.jpg",
        "https://ae01.alicdn.com/kf/Sb52e3bee678b40f3bb1da8943f9fe3a5L.jpg",
    ],
}

# Per-product supplier URL overrides for best accuracy (site_folder -> product_id -> url)
PRODUCT_OVERRIDES = {
    "site1-verdant-haven": {
        1: "https://ae01.alicdn.com/kf/S5e8e7af41e864b6b8fdb8effd1a56521P.jpg",
        6: "https://ae01.alicdn.com/kf/S2080c1ddceb94e9aa8f774e801f0ec8ct.jpg",
    },
    "site4-pawnest": {
        1: "https://ae01.alicdn.com/kf/S4026be9e13d74ce4ad346ab3779be429u.jpg",
    },
}

DEFAULT_URLS = list({u for urls in CATEGORY_URLS.values() for u in urls})


def pool_for(category):
    return CATEGORY_URLS.get(CATEGORY_ALIASES.get(category, category), DEFAULT_URLS)


def download(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read()


def process_image(data, store_name, product_id):
    img = Image.open(BytesIO(data)).convert("RGB")
    img = ImageOps.exif_transpose(img)
    w, h = img.size
    shift = (product_id * 17) % 40
    img = img.crop((shift, shift // 2, w - shift // 2, h - shift // 3))
    w, h = img.size
    ratio = 4 / 3
    if w / h > ratio:
        nw = int(h * ratio)
        img = img.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
    else:
        nh = int(w / ratio)
        img = img.crop((0, (h - nh) // 2, w, (h + nh) // 2))
    img = img.resize((900, 675), Image.Resampling.LANCZOS)
    img = ImageEnhance.Brightness(img).enhance(1.0 + (product_id % 7) * 0.01)
    img = ImageEnhance.Contrast(img).enhance(1.05 + (product_id % 5) * 0.01)
    img = ImageEnhance.Color(img).enhance(1.03 + (product_id % 4) * 0.02)
    if product_id % 3 == 0:
        img = img.filter(ImageFilter.SHARPEN)
    canvas = Image.new("RGB", (960, 720), (248, 250, 252))
    canvas.paste(img, (30, 20))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([(0, 680), (960, 720)], fill=(30, 41, 59))
    draw.text((24, 692), store_name[:28], fill=(226, 232, 240))
    out = BytesIO()
    canvas.save(out, format="JPEG", quality=88, optimize=True)
    return out.getvalue()


def source_url(site, product):
    overrides = PRODUCT_OVERRIDES.get(site, {})
    if product["id"] in overrides:
        return overrides[product["id"]]
    pool = pool_for(product["category"])
    return pool[(product["id"] - 1) % len(pool)]


def main():
    cache = {}
    for site in sorted(d for d in os.listdir(ROOT) if d.startswith("site")):
        products_path = os.path.join(ROOT, site, "products.json")
        with open(products_path) as f:
            data = json.load(f)
        img_dir = os.path.join(ROOT, site, "images")
        os.makedirs(img_dir, exist_ok=True)
        store_name = data["store"]["name"]
        count = 0
        for p in data["products"]:
            rel = f"images/{p['id']}.jpg"
            out_path = os.path.join(img_dir, f"{p['id']}.jpg")
            src = source_url(site, p)
            try:
                if src not in cache:
                    cache[src] = download(src)
                with open(out_path, "wb") as f:
                    f.write(process_image(cache[src], store_name, p["id"]))
                p["image"] = rel
                p["images"] = [rel]
                p["imageSource"] = "AliExpress supplier (edited)"
                count += 1
            except Exception as exc:
                print(f"  ✗ {site} #{p['id']}: {exc}")
        with open(products_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"{site}: {count}/{len(data['products'])} images")


if __name__ == "__main__":
    main()