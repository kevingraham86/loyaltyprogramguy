#!/bin/sh
# Copy ONLY the publishable site into ./dist for the Cloudflare Worker (run from repo root).
# Allowlist on purpose: anything not listed here is never published.
set -e
rm -rf dist && mkdir dist
for f in index.html favicon.ico robots.txt sitemap.xml llms.txt; do cp "$f" dist/; done
for d in images css js card about guides restaurants retail salons privacy adamsave offer mainstream; do cp -R "$d" dist/; done
rm -f dist/css/tailwind.input.css
find dist -name '.*' -delete
echo "dist ready: $(find dist -type f | wc -l | tr -d ' ') files"
