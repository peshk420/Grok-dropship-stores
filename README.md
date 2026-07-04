# Dropship Store Portfolio

Five professional dropshipping storefronts with **23 products each** (115 total), supplier-sourced product photos, full policy pages, working checkout, and a private admin dashboard.

## Quick Start

```bash
cd ~/dropship-stores
python3 server.py
```

| URL | Purpose |
|-----|---------|
| http://localhost:8080 | Public portfolio dashboard |
| http://localhost:8080/site1-verdant-haven/ | Store 1 |
| http://localhost:8080/admin/ | **Private admin** (orders, messages, subscribers) |

**Admin password:** `admin/config.json` → default is `dropship2026` (change this!)

## Your Stores

| # | Company | Folder | Products | Niche |
|---|---------|--------|----------|-------|
| 1 | Verdant Haven | `site1-verdant-haven/` | 23 | Lawn, pool & home care |
| 2 | Solara Coast | `site2-solara-coast/` | 23 | Summer fashion, beach & pool |
| 3 | ArcticFlow | `site3-arcticflow/` | 23 | AC, fans, coolers |
| 4 | PawNest | `site4-pawnest/` | 23 | Pet summer care (trending) |
| 5 | Summit Trail Co. | `site5-summit-trail/` | 23 | Camping & outdoor (trending) |

## Private Admin Dashboard

The admin site at `/admin/` is **not linked** from any public store. It collects:

- **Orders** — submitted via checkout on any store
- **Messages** — contact form submissions
- **Subscribers** — newsletter signups
- **Revenue stats** — pending order totals

Data is stored in:
- `data/orders.json`
- `data/messages.json`
- `data/subscribers.json`

## Editing Products

Each store's `products.json` controls everything:

```json
{
  "name": "Dog Cooling Vest",
  "price": 34.99,
  "originalPrice": 49.99,
  "cost": 7.49,
  "description": "Short summary",
  "details": "Full product specifications",
  "image": "https://..."
}
```

Regenerate all catalogs after editing `generate_products.py`:
```bash
python3 generate_products.py
python3 fetch_product_images.py   # downloads supplier photos + applies edits
```

### Product Images
Photos are downloaded from **AliExpress supplier CDN** (`supplier_urls.json`), then edited locally (crop, color, studio padding, brand strip) and saved to each site's `images/` folder. Re-run `fetch_product_images.py` after adding products.

## Policy Pages (Low-Risk for You)

Each store has full policy pages at `policies.html`:

- **Returns & Refunds** — 14-day window, customer pays return shipping, RMA required, 15% restocking on large items
- **Shipping** — 7–21 day estimates, not guaranteed
- **Terms** — Dropshipping disclosure, liability capped at purchase price, no medical claims
- **Privacy** — No data selling, 3-year retention

These protect you as a dropshipper by setting clear expectations and limiting liability.

## Pages Per Store

| File | Purpose |
|------|---------|
| `index.html` | Main storefront |
| `product.html?id=X` | Individual product detail page |
| `policies.html?type=returns` | Policy pages |
| `products.json` | All editable content |

## File Structure

```
dropship-stores/
├── server.py              ← Run this (not http.server)
├── admin/
│   ├── index.html         ← Private dashboard
│   └── config.json        ← Admin password
├── data/                  ← Orders, messages, subscribers
├── shared/                ← CSS, JS templates
├── site1-verdant-haven/
├── site2-solara-coast/
├── site3-arcticflow/
├── site4-pawnest/
└── site5-summit-trail/
```

## Next Steps

1. Change admin password in `admin/config.json`
2. Replace placeholder emails/phones in each `products.json`
3. Connect Stripe/PayPal to checkout flow
4. Swap Unsplash images with real supplier product photos
5. Deploy to Netlify/Vercel (use server.py locally; deploy static files + serverless functions for API)