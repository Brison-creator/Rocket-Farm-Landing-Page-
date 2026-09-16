# Rocket Farm — landing page

A single-file landing page for **Rocket Farm LLC**, a full-hookup RV park in
development at 10729 Farmer Road, Kaplan, Louisiana (Vermilion Parish).

Everything lives in `index.html` — markup, styles and script. No build step, no
dependencies, no framework. Open the file in a browser and it works.

## Sections

1. **Hero** — positioning and the primary calls to action
2. **At a glance** — 17 spaces, $650–700/mo, ~30 mi to the launch campus, 2027
3. **Who it's for** — crews and contractors, launch watchers, sportsmen and families
4. **The spaces** — interactive site map plus a table of all 17 lots and rates
5. **Pricing** — the three rate tiers, what's included, and the terms
6. **The park** — Phase 1 amenities
7. **What's planned** — Phase 1, Phase 2, and the big-pond view deck
8. **Location** — the address and approximate drive times
9. **Waitlist** — interest capture form
10. **Footer** — contact, development disclaimer, non-affiliation notice

## Editing the lot prices

**The lot table in `index.html` is the single source of truth.** The site map is
generated from it at page load, so the map, the tooltips and the filter counts
can never disagree with the table. To change a rate, edit that row and nothing
else:

```html
<tr data-lot="A5" data-row="A" data-amps="50" data-term="monthly" data-price="700">
  <td class="lot-id">A5</td>
  ...
  <td class="rate">$700 <small>/ mo</small></td>
</tr>
```

Change **both** `data-price` (drives the map tooltip) and the `<td class="rate">`
cell (what a visitor reads in the table). The other attributes control behaviour:

| Attribute   | Values                | Effect                                        |
|-------------|-----------------------|-----------------------------------------------|
| `data-lot`  | e.g. `A5`             | Label on the map and in the table             |
| `data-row`  | `A` or `B`            | Which row of the map the space is drawn in    |
| `data-amps` | `50` or `30`          | Colour on the map, service shown in the table |
| `data-term` | `monthly` or `nightly`| Colour, filter grouping, "/mo" vs "/night"    |
| `data-price`| a number              | Price in the map tooltip                      |

Adding or removing a `<tr>` adds or removes a pad on the map automatically — the
row spacing recalculates. If you do, update the hard-coded counts in the filter
chips, the `.tally` line, the tier cards and the stat strip, which are plain text.

### Note on the tiering

The Phase 1 binder underwrites a **flat $700/month** across 14 monthly sites.
This page instead tiers on the only real spec difference between the lots —
electrical service:

- 11 spaces with 50/30/20 amp pedestals → **$700/mo**
- 3 monthly spaces with 30/20 amp pedestals → **$650/mo**
- 3 spaces held back for nightly use → **$55/night**

Against the binder's base case that is **$1,530/year** less monthly tenant
revenue in a stabilised Year 2 ($98,430 vs $99,960), moving Year 2 DSCR from
**3.50x to about 3.44x** — still well above the binder's own $650-flat downside
of 3.24x.

To revert to flat $700, set `data-price="700"` and the rate cell to `$700` on
rows A3, A4 and B2, and update the "30-amp monthly" tier card.

## Before you publish

Two things need your real details. Both are marked `TODO` in `index.html`.

1. **Email address.** Replace `hello@rocketfarm.example` in two places — the
   footer link and the `TO` variable in the script at the bottom.

2. **The waitlist form.** As written, submitting opens a pre-filled email in the
   visitor's mail app. That works, but it loses people who don't have mail set
   up. To collect submissions properly, pick one:

   **Formspree** (free tier, works on any host)
   ```html
   <form id="waitlist-form" action="https://formspree.io/f/YOUR_ID" method="POST">
   ```

   **Netlify Forms** (if you host on Netlify)
   ```html
   <form id="waitlist-form" name="waitlist" method="POST" data-netlify="true">
   ```

   With either one, delete the form-handling block at the end of the `<script>` —
   it calls `preventDefault()` and would stop the real submission.

## Deploying on GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → branch `main`, folder `/ (root)`.
The page goes live at `https://<user>.github.io/<repo>/` within a minute or two.

To use a custom domain, add a `CNAME` file containing just the domain
(e.g. `rocketfarm.com`), then point the DNS at GitHub Pages.

## Accessibility and robustness

- The lot table is real HTML, so the prices work with JavaScript disabled and
  are visible to search engines. The map is a progressive enhancement on top.
- Map pads are keyboard focusable and announce their space, service and rate.
- Scroll-reveal animations only arm when JavaScript runs, so content is never
  stuck invisible, and they are disabled under `prefers-reduced-motion`.
- Verified in Chromium from 320px to 1440px: no horizontal overflow, no console
  errors, and tooltips stay inside the map frame at every lot.

## A note on content

This page is deliberately guest-facing. None of the figures from the Phase 1 or
Phase 2 financing binders — project cost, sources and uses, NOI, DSCR, loan
amounts, pro forma — appear anywhere in it, and they shouldn't. Rates are
labelled as planned opening rates, and the footer carries a development
disclaimer plus a non-affiliation notice regarding SpaceX.
