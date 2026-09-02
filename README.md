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

## Add the weekly message

The `messages` archetype creates the expected front matter for a message. Use a
date-prefixed, descriptive slug so files remain easy to sort:

```sh
hugo new content messages/YYYY-MM-DD-slug.md
```

For example:

```sh
hugo new content messages/2026-09-06-built-to-last.md
```

Hugo uses `archetypes/messages.md` to create the file. Open the new file under
`content/messages/` and complete these fields:

```yaml
---
title: "Built to Last"
date: 2026-09-06T09:00:00-05:00
speaker: "Speaker Name"
series: "Series Name"
description: "A short summary used on message cards and in search previews."
image: "/images/messages/built-to-last.jpg"
video_url: "https://www.youtube.com/watch?v=example"
audio_url: "https://example.org/path/to/audio.mp3"
draft: true
---
```

Then:

1. Add the artwork to `static/images/messages/` and make the `image` value
   match its public `/images/messages/...` path. Leave `image` empty only when
   no artwork is available.
2. Use complete public URLs for `video_url` and `audio_url`. Leave either value
   empty if that format is unavailable.
3. Add any longer notes or supporting links below the front matter in Markdown.
4. Preview the message with the draft-enabled development command above.
5. Check the title, date, speaker, series, media links, artwork crop, and message
   page on both narrow and wide screens.
6. Change `draft` to `false`, run the production build, and deploy the new
   `public/` output.

Do not edit a generated file in `public/messages/`; Hugo will overwrite it on
the next build. Always edit the corresponding source file in
`content/messages/`.

## Pre-deployment check

Before copying a release, run the production build and review its output for
warnings. Check the homepage, navigation at mobile and desktop widths, internal
links, external Church Center actions, and the newest message. Commit source
changes only; generated files in `public/` and `resources/_gen/` should remain
untracked.
