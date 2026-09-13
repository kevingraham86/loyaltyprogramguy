# loyaltyprogramguy.com

Static site served by GitHub Pages from `main`.

## Styles

The page uses Tailwind classes, compiled to `css/site.css` (committed). After adding or
changing any Tailwind classes in `index.html`, rebuild the CSS:

```bash
npx -y tailwindcss@3.4.17 -c tailwind.config.js -i css/tailwind.input.css -o css/site.css --minify
```

Classes that are not in `index.html` when the CSS is built will not work on the live site.
