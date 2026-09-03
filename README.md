# Beachside Church Hugo site

This repository contains the source for the Beachside Church website. It is a
static site built with [Hugo](https://gohugo.io/), so the generated site can be
copied to a different web server without running Hugo there.

The site was tested with **Hugo v0.164.0 extended**. Use that version or a newer
compatible extended release when editing or building the site.

## Run the site locally

From the repository root, start Hugo's development server:

```sh
hugo server --disableFastRender
```

Open the local address printed by Hugo, normally
<http://localhost:1313/>. Hugo watches the source files and refreshes the site
as they change. Draft content is hidden by default; include it while reviewing
unpublished work with:

```sh
hugo server --disableFastRender --buildDrafts
```

Stop the server with `Ctrl+C`.

## Build and deploy

Create an optimized production build from the repository root:

```sh
hugo --gc --minify
```

Hugo writes the complete generated website to `public/`. That directory is
ignored by Git because it is build output. Deploy the **contents** of `public/`
to the destination machine's web root, replacing the previous generated site
as one release. The destination only needs to serve static files; it does not
need Hugo, Git, or this source repository.

Before deploying to another hostname, set `baseURL` in `hugo.toml` to the final
public URL. Never deploy the development server or copy `themes/`, `content/`,
or `assets/` into the web root.

## Where site files live

- `content/` contains editable pages written in Markdown. Front matter at the
  top of each file controls its title, description, images, and other template
  options.
- `data/home.yaml` contains the homepage's repeatable content, such as feature
  cards and location details. Keep its YAML indentation intact and follow the
  field names used by the existing entries.
- `static/images/` contains images copied to the site without modification.
  For example, `static/images/pages/visit.jpg` is referenced in content as
  `/images/pages/visit.jpg`.
- `themes/beachside/` contains the site's Hugo templates, reusable partials,
  source styles, and scripts. Theme CSS and JavaScript live under that theme's
  `assets/` directory.
- `hugo.toml` contains the public URL, site-wide settings, navigation, and the
  announcement banner configuration.

Use lowercase, descriptive, hyphen-separated filenames for new Markdown files
and images. Put general page media in `static/images/pages/`, homepage media in
`static/images/home/`, and message artwork in `static/images/messages/`. Avoid
spaces in filenames. If replacing an image whose dimensions or crop differ,
check both desktop and mobile layouts before publishing.

## Edit pages and navigation

Edit an existing Markdown file under `content/` to change a normal page. Keep
the opening and closing front matter delimiters and do not rename fields unless
the matching template is also updated. A page with `draft: true` is available
only when Hugo is run with `--buildDrafts`; change it to `false` when the page
is ready to publish.

The primary navigation is configured in `hugo.toml`. Each menu item has a
label, destination, and weight; lower weights appear first. Use root-relative
URLs such as `/visit/` for pages in this site and complete `https://` URLs for
external destinations.

Links to registration, giving, groups, and other actions hosted by Church
Center must remain external Church Center URLs. Do not replace them with local
paths or attempt to recreate those account-based workflows in Hugo.

The optional announcement banner is controlled by the announcement values in
`hugo.toml` under `[params.announcement]`. Set `enabled` to `true` or `false`,
edit its display `text`, and set its destination `url` and link label
`linkText`. Keep an external destination as a complete `https://` URL. If the
banner is not needed, disable it instead of deleting its configuration.

## Add messages and message series

The message templates support both standalone messages and series with any
number of parts. Each part has its own page and `video_url`. The series page is
also Part 1, matching the structure of the original site.

For a new multi-part series, create a branch bundle. Use a lowercase,
hyphen-separated series slug:

```sh
hugo new content --kind message-series messages/built-to-last/_index.md
```

Hugo uses `archetypes/message-series.md` to create the series page. Edit
`content/messages/built-to-last/_index.md` and replace both instances of
`Series Title`. Complete the Part 1 speaker, description, artwork, video, and
optional resource links. Leave `layout: series` and `part_number: 1` in place.

To add Part 2, or any later weekly part, create a page inside that same series
directory:

```sh
hugo new content --kind message-part messages/built-to-last/built-to-last-part-2.md
```

Hugo uses `archetypes/message-part.md`. Edit the new file, make `series` exactly
match the series page, and set the correct `part_number`. Each part requires its
own `video_url`; this is what makes the related links open a different video.
The series navigation is generated automatically from every Markdown file in
the directory, newest first, and excludes the page currently being viewed.
Also update `lastmod` in the series `_index.md` to the new part's date; keep the
series page's original `date` as the Part 1 date.

For a one-week standalone message that will never have additional parts, use:

```sh
hugo new content messages/YYYY-MM-DD-slug.md
```

The standalone command uses `archetypes/messages.md`. Whether editing a series
or standalone message, complete the applicable fields:

```yaml
---
title: "Built to Last"
date: 2026-09-06T09:00:00-05:00
speaker: "Speaker Name"
series: "Series Name"
part_number: 2 # Multi-part series only
description: "A short summary used on message cards and in search previews."
image: "/images/messages/built-to-last.jpg"
video_url: "https://www.youtube.com/watch?v=example"
audio_url: "https://example.org/path/to/audio.mp3"
guide_url: "/discipleship-guide/built-to-last-part-2/"
draft: true
---
```

Then:

1. Add the artwork to `static/images/messages/` and make the `image` value
   match its public `/images/messages/...` path. Leave `image` empty only when
   no artwork is available.
2. Use complete public URLs for `video_url` and `audio_url`. A YouTube watch URL
   or `youtu.be` URL is converted to a privacy-enhanced embed. For a guide in
   this site, use its root-relative URL, such as
   `/discipleship-guide/built-to-last-part-2/`. An externally hosted guide may
   still use a complete `https://` URL. Leave optional URLs empty when they are
   unavailable.
3. Add any longer notes or supporting links below the front matter in Markdown.
4. Preview the message with the draft-enabled development command above.
5. Check the title, date, speaker, series, media links, artwork crop, and message
   page on both narrow and wide screens.
6. Follow every link under **Messages in This Series** and confirm that each
   page loads its own title and video.
7. Change `draft` to `false`, run the production build, and deploy the new
   `public/` output.

Do not edit a generated file in `public/messages/`; Hugo will overwrite it on
the next build. Always edit the corresponding source file in
`content/messages/`.

## Add a discipleship guide

The guide archive is generated at `/discipleship-guides/`. Individual guides
live at `/discipleship-guide/<guide-slug>/`; they are intentionally not added to
the homepage or primary navigation. Create a guide with:

```sh
hugo new content discipleship-guide/built-to-last-part-2.md
```

This uses `archetypes/discipleship-guide.md`, which contains the same reusable
sections as the live guides: message recap, main idea, discussion questions,
five daily devotions, spiritual practice, prayer prompts, next steps, and
resources. Open the new file under `content/discipleship-guide/` and:

1. Set `title`, `date`, `speaker`, `series`, and a short `description` in the
   front matter. The archive sorts by `date` and creates series filters from the
   exact `series` values. Add `display_series: true` only when the series name
   should also appear in the guide's dark title panel; omit it otherwise.
2. Replace the placeholder copy inside each HTML content block. Keep the
   existing `dg-...` class names because they provide the card layout and
   responsive styling.
3. In the devotion tabs, keep each button's `data-day` matched to its panel ID,
   such as `data-day="monday"` and `id="devo-monday"`. The theme handles tab
   switching and keyboard focus without page-specific scripts.
4. Change `draft` to `false` when ready.
5. Set the corresponding message's `guide_url` to the guide's root-relative
   path, preview both directions, and verify every devotion tab on desktop and
   mobile.

To omit a section, delete its entire enclosing `<section>...</section>` block.
For a new guide with a structure similar to an existing one, copying the
existing source file and replacing its text is often faster than starting from
the archetype. Never paste analytics scripts or page-level `<style>` elements
into a guide; those behaviors already belong to the Hugo theme.

Do not edit generated files under `public/discipleship-guide/` or
`public/discipleship-guides/`; they are overwritten by Hugo.

## Pre-deployment check

Before copying a release, run the production build and review its output for
warnings. Check the homepage, navigation at mobile and desktop widths, internal
links, external Church Center actions, and the newest message. Commit source
changes only; generated files in `public/` and `resources/_gen/` should remain
untracked.
