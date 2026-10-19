# joyce-mo.github.io

Personal site: research, writing, and art. Built with Jekyll and hosted free on GitHub Pages.
Every push to `main` rebuilds the live site in about a minute (no build setup needed).

```
index.html                  home page (intro, book, latest writing, 4 art pieces)
research.html               /research/
writing.html                /writing/   (lists _posts/)
art.html                    /art/       (gallery + lightbox)
about.md                    /about/
_posts/                     blog posts (Markdown)
_posts/pss/                 links to posts I wrote for Princeton Satellite Systems
_drafts/                    unpublished drafts
_data/publications.yml      publication list
_data/art.yml               artwork list
_data/art_categories.yml    art filters / mediums
assets/art/                 artwork images (+ thumbs/)
assets/css/main.css         all styling (colors at the top)
_config.yml                 name, links, email
```

## Write a blog post

**Quickest way (from any browser):** open this link, which starts a new post on github.com with the
template filled in. Change the filename's date and title, write, then click **Commit changes**.
The post is live about a minute later.

[**Start a new post →**](https://github.com/Joyce-Mo/Joyce-Mo.github.io/new/main/_posts?filename=YYYY-MM-DD-my-new-post.md&value=---%0Atitle%3A%20My%20New%20Post%0Adescription%3A%20One%20sentence%20for%20the%20home%20page%20and%20link%20previews.%0Atags%3A%20%5B%5D%0A---%0A%0AStart%20writing%20here%2C%20in%20Markdown.%0A)

(Bookmark it. You'll need to be signed in to GitHub.)

**Or by hand**, create `_posts/YYYY-MM-DD-some-title.md`:

```markdown
---
title: Some Title
description: One sentence for the home-page tile and link previews.
tags: [science, art]
---

Your post in Markdown...
```

Put images in `assets/img/` and use `![alt text](/assets/img/photo.jpg)`.
Not ready yet? Keep it in `_drafts/` (no date in the filename) and it won't be published.
`_drafts/example-post.md` shows the formatting options.

The 4 newest posts show on the home page automatically.

## Link a post you wrote somewhere else

Posts written for Princeton Satellite Systems live in `_posts/pss/`. Each is a tiny file that just
links out (it gets a small **PSS** tag in lists). To add one, create `_posts/pss/YYYY-MM-DD-short-title.md`:

```markdown
---
title: "Post title"
description: "One sentence about it."
external_url: https://psatellite.com/the-post/
---
```

Podcast appearances work the same way: add `source: Podcast` and they get a **Podcast** tag instead.

For a different outlet, put the file in `_posts/` and add `source: Short Name` (the tag) and
`source_name: Full Name` to the front matter as well.

You can do all of this from github.com too: open the repo, then **Add file → Create new file**.

## Add art

**From your Mac** (resizes, makes a thumbnail, and adds the entry for you; HEIC from iPhone works):

```bash
scripts/add-art.sh ~/Desktop/IMG_1234.HEIC "Morning Fog" watercolor-ink "Watercolor on cold-press paper."
scripts/add-art.sh ~/Desktop/vase.jpg "Blue Vase" sculpture --featured   # --featured: show it on the home page
git add -A && git commit -m "Add art" && git push
```

The home page shows the first 4 pieces in `_data/art.yml` marked `featured: true`
(now: Giraffe, Snail Island, Goji Berry, Ram Skull). To swap one, move the `featured: true` line to another piece.

Categories: `painting`, `watercolor-ink`, `botanical`, `drawing`, `sculpture`, `calligraphy`, `graphic-design`.
To add a new one, add it to `_data/art_categories.yml`.

**From github.com**: upload the image to `assets/art/` *and* `assets/art/thumbs/` (or skip the thumb and use
the same image; it's just slower), then edit `_data/art.yml` and add:

```yaml
- title: "Morning Fog"
  image: morning-fog.jpg
  category: watercolor-ink
  description: "Optional caption."
  width: 800      # rough pixel size; only used to avoid layout jumps
  height: 600
  featured: true  # optional
```

To rename, recaption, reorder, or remove pieces, just edit `_data/art.yml`.
Many older pieces had no titles, so they have descriptive placeholder names. Change them freely.

## Add a publication

Add an entry to `_data/publications.yml` (your name is bolded automatically):

```yaml
- title: "Paper title"
  authors: A. Person, Joyce Mo, B. Person
  venue: Journal or Conference
  year: 2027
  type: Paper          # Paper, Preprint, Book, Poster, ...
  url: https://doi.org/...
  pdf: /assets/papers/paper.pdf   # optional
  code: https://github.com/...    # optional
```

## Edit the intro and other text

- Home-page intro and featured book: `index.html`
- The big "Joyce Mo" is a drawing in `_includes/name.svg`, made from the free Birthstone Bounce font
  (Open Font License, OK for any use) by `scripts/make-name-svg.py`; instructions are at the top of that file.
- About page: `about.md`
- Page intros: the `intro:` line at the top of `research.html`, `writing.html`, `art.html`
- Email / GitHub / LinkedIn / Instagram: `_config.yml`

## Preview locally (optional)

Needs Ruby 3.3 (`brew install ruby@3.3`):

```bash
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
bundle config set --local path vendor/bundle
SDKROOT=$(xcrun --show-sdk-path) CPLUS_INCLUDE_PATH=$(xcrun --show-sdk-path)/usr/include/c++/v1 bundle install
bundle exec jekyll serve      # then open http://localhost:4000
```
