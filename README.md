# Django Blog

A learning project: a small blog built with Django 6.1, styled with Tailwind CSS v4.

## Running the site

```bash
.venv/Scripts/python.exe manage.py runserver
```

## Tailwind CSS

Styling uses the **Tailwind standalone CLI** — a single binary, so there is no
Node.js or npm dependency.

| Path | Purpose |
| --- | --- |
| `blog_main/static_src/input.css` | Source: theme tokens, `@source` globs, custom component classes. **Edit this.** |
| `blog_main/static/css/site.css` | Compiled output, served via `{% static 'css/site.css' %}`. **Generated — never edit.** |
| `tools/tailwindcss.exe` | The standalone CLI (git-ignored, ~108 MB). |
| `tailwind-watch.bat` / `tailwind-build.bat` | Convenience wrappers for the two commands below. |

### Development

Run the watcher in its own terminal, next to `runserver`. It rebuilds the
stylesheet whenever a template or `input.css` changes:

```bash
tools/tailwindcss.exe -i blog_main/static_src/input.css -o blog_main/static/css/site.css --watch
```

### Production build

```bash
tools/tailwindcss.exe -i blog_main/static_src/input.css -o blog_main/static/css/site.css --minify
```

Then `python manage.py collectstatic` when deploying.

### First-time setup on a new machine

The CLI binary is git-ignored, so download it once:

```bash
mkdir -p tools && curl -L -o tools/tailwindcss.exe https://github.com/tailwindlabs/tailwindcss/releases/download/v4.3.3/tailwindcss-windows-x64.exe
```

### Changing the accent colour

The palette is slate neutrals plus one accent, defined as `--color-brand-*` in
the `@theme` block of `input.css`. Change those hex values and rebuild — every
`brand-*` utility across the site follows.

## Notes

- Icons come from the Bootstrap **Icons** font (an icon set, not the Bootstrap
  CSS framework). It is still loaded in `base.html` because `SocialLink.icon_class`
  stores values like `bi-github`.
- The nav search bar is markup only. See the `TODO` in
  `templates/blog/includes/search_form.html` for how to wire it to a view.
