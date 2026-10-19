#!/usr/bin/env python3
"""Draw "Joyce Mo" in a font as an SVG -> _includes/name.svg (the big name on the home page)

Usage:  python3 scripts/make-name-svg.py path/to/BirthstoneBounce-Medium.ttf
Needs:  pip install fonttools uharfbuzz

Font: Birthstone Bounce (SIL Open Font License, free for any use, including commercial):
https://fonts.google.com/specimen/Birthstone+Bounce
The letters become plain vector shapes, so no font file is loaded by the site.
A few stars are sprinkled around the name; they twinkle via .name-art in main.css.
"""
import sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

TEXT = "Joyce Mo"
OUT = "_includes/name.svg"
# stars as (x, y, size) in fractions of the name's width / height
STARS = [(-.04, .1, .045), (.47, .04, .03), (1.0, .2, .04), (.94, .92, .025), (.44, .97, .02)]


def star(cx, cy, r):
    k = r * .18  # four-point sparkle
    return (f"M{cx:.0f} {cy - r:.0f}C{cx + k:.0f} {cy - k:.0f} {cx + k:.0f} {cy - k:.0f} {cx + r:.0f} {cy:.0f}"
            f"C{cx + k:.0f} {cy + k:.0f} {cx + k:.0f} {cy + k:.0f} {cx:.0f} {cy + r:.0f}"
            f"C{cx - k:.0f} {cy + k:.0f} {cx - k:.0f} {cy + k:.0f} {cx - r:.0f} {cy:.0f}"
            f"C{cx - k:.0f} {cy - k:.0f} {cx - k:.0f} {cy - k:.0f} {cx:.0f} {cy - r:.0f}Z")


def main(font_path):
    data = open(font_path, "rb").read()
    font = TTFont(font_path)
    gs, order = font.getGlyphSet(), font.getGlyphOrder()

    # shape with HarfBuzz so the script's kerning and joining alternates apply
    hbfont = hb.Font(hb.Face(data))
    buf = hb.Buffer(); buf.add_str(TEXT); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True, "calt": True})

    sp, bp, x = SVGPathPen(gs), BoundsPen(gs), 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        tf = (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)  # flip y for SVG
        g = gs[order[info.codepoint]]
        g.draw(TransformPen(sp, tf)); g.draw(TransformPen(bp, tf))
        x += pos.x_advance
    x0, y0, x1, y1 = bp.bounds
    w, h = x1 - x0, y1 - y0
    stars = "".join(f'<path class="star" d="{star(x0 + fx * w, y0 + fy * h, s * w)}"/>' for fx, fy, s in STARS)
    # frame the name and the stars, so the drawing lines up with the text below it
    sx = [x0 + fx * w + d * s * w for fx, fy, s in STARS for d in (-1, 1)]
    sy = [y0 + fy * h + d * s * w for fx, fy, s in STARS for d in (-1, 1)]
    x0, x1, y0, y1 = min(x0, *sx), max(x1, *sx), min(y0, *sy), max(y1, *sy)
    w, h = x1 - x0, y1 - y0
    svg = (f'<svg class="name-art" viewBox="{x0:.0f} {y0:.0f} {w:.0f} {h:.0f}" '
           f'role="img" aria-labelledby="name-title" xmlns="http://www.w3.org/2000/svg">\n'
           f'<title id="name-title">{TEXT}</title>\n'
           f'<path fill="currentColor" d="{sp.getCommands()}"/>\n'
           f'<g fill="currentColor">{stars}</g>\n</svg>\n')
    open(OUT, "w").write(svg)
    print(f"wrote {OUT} ({len(svg) // 1024} KB)")


if __name__ == "__main__":
    main(sys.argv[1])
