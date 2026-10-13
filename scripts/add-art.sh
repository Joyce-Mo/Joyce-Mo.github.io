#!/usr/bin/env bash
# Add a piece of art to the site.
#
#   scripts/add-art.sh <image> "<Title>" <category> ["<description>"] [--featured]
#
#   scripts/add-art.sh ~/Desktop/IMG_1234.HEIC "Morning Fog" watercolor-ink "Watercolor on cold-press paper."
#   scripts/add-art.sh ~/Desktop/vase.jpg "Blue Vase" sculpture --featured
#
# Accepts JPG, PNG, HEIC, TIFF... Makes a 1600px web copy + an 800px thumbnail
# (macOS `sips`, no installs needed) and adds the entry to _data/art.yml.
# Categories are listed in _data/art_categories.yml. Then commit & push.
set -euo pipefail
cd "$(dirname "$0")/.."

featured=false; args=()
for a in "$@"; do [[ $a == --featured ]] && featured=true || args+=("$a"); done
set -- "${args[@]+"${args[@]}"}"

if [[ $# -lt 3 ]]; then
  sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
  echo; echo "Categories:"; grep -E '^- key:' _data/art_categories.yml | sed 's/- key:/ /'
  exit 1
fi

src=$1 title=$2 cat=$3 desc=${4:-}
[[ -f $src ]] || { echo "No such file: $src" >&2; exit 1; }
grep -qE "^- key: ${cat}\$" _data/art_categories.yml || {
  echo "Unknown category '$cat'. Use one of:" >&2
  grep -E '^- key:' _data/art_categories.yml | sed 's/- key:/ /' >&2; exit 1; }

ascii=$(printf '%s' "$title" | iconv -f utf-8 -t ascii//TRANSLIT 2>/dev/null) || ascii=$title
slug=$(printf '%s' "$ascii" | LC_ALL=C tr '[:upper:]' '[:lower:]' | LC_ALL=C sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g')
[[ -n $slug ]] || slug=art-$(date +%Y%m%d%H%M%S)
base=$slug; n=2
while [[ -e assets/art/$slug.jpg ]]; do slug=$base-$n; n=$((n+1)); done

longest=$(sips -g pixelWidth -g pixelHeight "$src" | awk '/pixel(Width|Height)/{if($2>m)m=$2}END{print m}')
shrink() { (( longest > $1 )) && echo "-Z $1"; }   # never upscale small images
sips -s format jpeg -s formatOptions 82 $(shrink 1600) "$src" --out "assets/art/$slug.jpg" >/dev/null
sips -s format jpeg -s formatOptions 80 $(shrink 800) "$src" --out "assets/art/thumbs/$slug.jpg" >/dev/null
w=$(sips -g pixelWidth  "assets/art/thumbs/$slug.jpg" | awk '/pixelWidth/{print $2}')
h=$(sips -g pixelHeight "assets/art/thumbs/$slug.jpg" | awk '/pixelHeight/{print $2}')

q() { printf '"%s"' "$(printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g')"; }
{
  echo
  echo "- title: $(q "$title")"
  echo "  image: $slug.jpg"
  echo "  category: $cat"
  [[ -n $desc ]] && echo "  description: $(q "$desc")"
  echo "  width: $w"
  echo "  height: $h"
  $featured && echo "  featured: true"
} >> _data/art.yml

echo "Added '$title' -> assets/art/$slug.jpg (${w}x${h} thumb)"
echo "Preview: bundle exec jekyll serve   |   Publish: git add -A && git commit -m 'Add $title' && git push"
