# loyaltyprogramguy.com

Static site served by GitHub Pages from `main`.

## Styles

The page uses Tailwind classes, compiled to `css/site.css` (committed). After adding or
changing any Tailwind classes in `index.html`, rebuild the CSS:

```bash
npx -y tailwindcss@3.4.17 -c tailwind.config.js -i css/tailwind.input.css -o css/site.css --minify
```

Classes that are not in `index.html` when the CSS is built will not work on the live site.

## Content pages

Industry pages, guides, the About page, `llms.txt` and `sitemap.xml` are generated from
`_build/pages.py` (plain CSS in `css/pages.css`, no Tailwind). Edit content there, then:

```bash
python3 _build/pages.py
```

Commit the generated files. The `_build` folder is not published by GitHub Pages.
