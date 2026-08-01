# Gail Wager — Colorado Artist

Portfolio website for Gail Wager, an artist who has been painting in the mountains of
Colorado for over 50 years. Watercolors, portraits, and recent mixed media collage.

**Live site: <https://gailwager.github.io/art/>**

> **One-time setup:** the repository owner must enable GitHub Pages once —
> repo **Settings → Pages → Source: Deploy from a branch → `main` / `(root)` → Save**.
> The site goes live at the URL above a minute or two later.

## Sections

- **Home** — parallax banner and interactive tiles for each collection
- **Galleries** — nine collections (Wildlife, Birds, Horses & Farm, Dogs & Cats,
  People & Portraits, Flowers & Still Life, Landscapes & Towns, Southwest,
  Mixed Media & Collage), 227 works in all
- **About the Artist** — bio with Instagram / Facebook links
- **Purchase Inquiries** — originals $400–$1,500, with a contact form
- **[Analytics report](https://gailwager.github.io/art/analytics.html)** — visits and
  most-viewed / most-starred artwork

## How it works

- Pure static HTML/CSS/JS — no build step, served by GitHub Pages.
- `data/catalog.js` is the generated catalog: every artwork's title, category,
  code (e.g. `W-07`), image file, and notes.
- Visitors can ⭐ star favorites (stored in their browser); the contact form
  auto-fills their starred pieces. The form delivers to the artist's email via
  FormSubmit without exposing the address in the page source.
- `images/reference/` holds source/reference photos that are not artwork and are
  not shown on the site.

## Analytics

The site records pageviews and artwork views/stars anonymously. Out of the box the
[analytics page](https://gailwager.github.io/art/analytics.html) reports per-device
data. For site-wide totals including visitor regions:

1. Create a free account at [goatcounter.com](https://www.goatcounter.com) (e.g. code `gailwager`).
2. Set `GOATCOUNTER_CODE = "gailwager"` at the top of `js/main.js`.
3. Pageviews (with country breakdown) and star/view events then appear on the
   GoatCounter dashboard, and the weekly workflow in
   `.github/workflows/weekly-report.yml` refreshes `data/analytics-summary.json`
   from its API when a `GOATCOUNTER_TOKEN` repository secret is configured.
