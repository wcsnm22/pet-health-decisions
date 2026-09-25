# Pet Health Decisions

Static site answering pet health questions - online vet visits, pet pharmacies, joint supplements and dog DNA tests - with facts read only from each brand's own official pages.

- Pages: home + one page per brand (Vetster, 1-800-PetMeds, Cosequin, Embark) + editorial guides (`data/articles.json`) + About / Privacy / Contact
- Every fact carries its official source URL and check date
- Zero dependencies: `python build.py` renders `site/` (JSON-LD, canonical, sitemap.xml, robots.txt included)
- Deploy: Cloudflare Pages, project `pet-health-decisions`

## Rules

- No invented prices, terms, promo codes or expiry dates — if the brand's site does not publish it, the page says so.
- No Chinese in output pages.
- A fact without `source_url` or `checked` in `data/brands.json` fails the build.
- Guides in `data/articles.json` obey the same rules: sources must be on the brand's official domains, every comparison cell carries its source (or says `not published on the official site`), unknown block types fail the build.
- `python selfcheck.py` must print `RESULT: PASS` before anything is published.

## Deploy

```bash
python build.py && python selfcheck.py
git add -A && git commit -m "..." && git push
wrangler pages deploy site --project-name=pet-health-decisions --branch=main --commit-dirty=true
```
