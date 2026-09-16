# loyaltyprogramguy.com — code repo

**This repo is PUBLIC.** Project state, rules, and history are NOT kept here. Start every session by
reading, in order:

1. `/Users/kevin/Documents/SMB AI Backend/loyaltyprogramguy/STATE.md`
2. `/Users/kevin/Documents/SMB AI Backend/loyaltyprogramguy/STANDING_RULES.md`

End a session with "follow the Loyalty Program Guy WRAP.md" (same folder).

Quick facts (details in STATE.md):
- Live site = Cloudflare Worker. **Deploy: `sh _build/dist.sh && npx wrangler deploy`. A git push does not deploy.**
- Content pages come from `python3 _build/pages.py`; `/card/` is generated from `index.html`.
- `_build/dist.sh` is an allowlist. Never publish anything else.
- Spell it "Sentext". Phone 858-218-6905.
