#!/usr/bin/env python3
"""
make_meme.py — generate a finished meme image.

Two modes:

1) TEMPLATE mode (default) — captions a known meme template via api.memegen.link
   python3 make_meme.py template <template_id> "line 1" "line 2" [...] -o out.jpg
   Pass "" for a line you want blank. Order of lines follows the template's
   line order (check references/templates.md or the API example).

2) CUSTOM mode — classic Impact-style top/bottom caption on any local image
   python3 make_meme.py custom <image_path> --top "TOP TEXT" --bottom "BOTTOM TEXT" -o out.jpg

Utility:
   python3 make_meme.py search <keyword>     # search memegen templates live
   python3 make_meme.py info <template_id>   # line count + example for a template
"""
import argparse
import json
import sys
import urllib.request
import urllib.parse

API = "https://api.memegen.link"

# memegen URL escaping rules (https://memegen.link)
ESCAPES = [
    ("_", "__"), ("-", "--"),          # literal underscore/dash first
    (" ", "_"),
    ("?", "~q"), ("&", "~a"), ("%", "~p"), ("#", "~h"),
    ("/", "~s"), ("\\", "~b"), ("<", "~l"), (">", "~g"),
    ('"', "''"), ("\n", "~n"),
]


def escape(text: str) -> str:
    if not text:
        return "_"
    for a, b in ESCAPES:
        text = text.replace(a, b)
    return text


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "meme-engine/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def cmd_template(args):
    lines = "/".join(escape(t) for t in args.text)
    url = f"{API}/images/{args.template_id}/{lines}.jpg?width=1200"
    data = fetch(url)
    if not data[:3] == b"\xff\xd8\xff":
        sys.exit(f"ERROR: response is not a JPEG (bad template id or too many lines?)\nURL: {url}")
    with open(args.output, "wb") as f:
        f.write(data)
    print(f"OK {args.output} ({len(data)} bytes)\nsource: {url}")


def cmd_search(args):
    data = json.loads(fetch(f"{API}/templates/?filter={urllib.parse.quote(args.keyword)}"))
    for t in data:
        print(f"{t['id']} | {t['name']} | {t['lines']} lines | e.g. {t['example']['text']}")
    if not data:
        print("no matches")


def cmd_info(args):
    t = json.loads(fetch(f"{API}/templates/{args.template_id}"))
    print(json.dumps({"id": t["id"], "name": t["name"], "lines": t["lines"],
                      "example_text": t["example"]["text"], "blank": t["blank"]}, indent=2))


def cmd_custom(args):
    from PIL import Image, ImageDraw, ImageFont

    img = Image.open(args.image).convert("RGB")
    w, h = img.size
    if w < 800:  # upscale small images so text renders crisp
        img = img.resize((800, int(h * 800 / w)))
        w, h = img.size
    draw = ImageDraw.Draw(img)

    def load_font(size):
        for p in ("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
                  "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
        return ImageFont.load_default(size)

    def draw_caption(text, anchor_top: bool):
        text = text.upper()
        size = max(int(h * 0.09), 28)
        font = load_font(size)
        # wrap: shrink font until longest line fits, then wrap words
        while True:
            words, lines_out, cur = text.split(), [], ""
            for word in words:
                trial = (cur + " " + word).strip()
                if draw.textlength(trial, font=font) <= w * 0.94:
                    cur = trial
                else:
                    lines_out.append(cur)
                    cur = word
            lines_out.append(cur)
            if len(lines_out) <= 3 or size <= 24:
                break
            size -= 4
            font = load_font(size)
        line_h = size * 1.15
        y = h * 0.02 if anchor_top else h - line_h * len(lines_out) - h * 0.02
        for ln in lines_out:
            x = (w - draw.textlength(ln, font=font)) / 2
            draw.text((x, y), ln, font=font, fill="white",
                      stroke_width=max(size // 14, 2), stroke_fill="black")
            y += line_h
    if args.top:
        draw_caption(args.top, True)
    if args.bottom:
        draw_caption(args.bottom, False)
    img.save(args.output, quality=92)
    print(f"OK {args.output}")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("template")
    t.add_argument("template_id")
    t.add_argument("text", nargs="+")
    t.add_argument("-o", "--output", default="meme.jpg")
    t.set_defaults(func=cmd_template)

    s = sub.add_parser("search")
    s.add_argument("keyword")
    s.set_defaults(func=cmd_search)

    i = sub.add_parser("info")
    i.add_argument("template_id")
    i.set_defaults(func=cmd_info)

    c = sub.add_parser("custom")
    c.add_argument("image")
    c.add_argument("--top", default="")
    c.add_argument("--bottom", default="")
    c.add_argument("-o", "--output", default="meme.jpg")
    c.set_defaults(func=cmd_custom)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
