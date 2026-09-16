#!/bin/sh
# Copy the publishable site into ./dist for the Cloudflare Worker (run from repo root).
set -e
rm -rf dist && mkdir dist
rsync -a --exclude .git --exclude dist --exclude _build --exclude worker --exclude node_modules \
  --exclude README.md --exclude tailwind.config.js --exclude css/tailwind.input.css \
  --exclude .nojekyll --exclude CNAME --exclude .gitignore --exclude 'wrangler.jsonc' --exclude .wrangler \
  ./ dist/
echo "dist ready: $(find dist -type f | wc -l | tr -d ' ') files"
