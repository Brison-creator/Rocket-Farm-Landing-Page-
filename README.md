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

This tiering reduces stabilised monthly tenant revenue slightly against the
binder's flat-$700 base case, by well under a single site's annual rent. The
effect on coverage is marginal and stays comfortably inside the binder's own
downside case. The figures live in the financing binder and the companion
spreadsheet, which are deliberately not in this repository — run the comparison
there before you commit to a rate card.

To revert to flat $700, set `data-price="700"` and the rate cell to `$700` on
rows A3, A4 and B2, and update the "30-amp monthly" tier card.

## Contact address

The site uses a single address, **stay@therocketfarm.com**, in three places:
the footer link, the `TO` variable in the form script, and the `email` field of
the JSON-LD block. Change all three together if it ever moves.

It must be a live mailbox or a forwarder, or waitlist enquiries bounce.
Namecheap's free email forwarding (Domain tab → Redirect Email) covers it; the
MX and SPF records are already in place. Setting a **catch-all** forwarder as
well is worth the extra minute, so mail to `hello@`, `info@` or a typo still
reaches you instead of bouncing.

## Reservations and the deposit

The page now takes reservation requests rather than a waitlist. The form asks
for five things only — name, company, reason for the stay, phone and email —
and opens a pre-filled email (see below); you reply with deposit instructions.
The destination is the `TO` variable in the form-handling script at the bottom
of `index.html`. It currently points at the owner's personal inbox because the
stay@therocketfarm.com forwarder has not been created yet; once it exists at
Namecheap, set `TO` back to `stay@therocketfarm.com` so the branded address is
the only one visitors ever see.

**To take the $250 on the spot:** create a Stripe Payment Link (or Square /
PayPal), then set `PAY_LINK` in the script at the bottom of `index.html`. A
"Pay the $250 deposit" button appears under the form as soon as it is non-empty.

**Deposit terms as published:** $250, credited to the first month, not
refundable if the guest chooses to stay elsewhere, **refunded in full if Rocket
Farm does not open or cannot deliver the reserved space.** Keep that last
clause. A deposit kept when the business fails to deliver is not enforceable,
is the textbook chargeback case, and reads badly to a lender. The terms appear
in three places — hero small print, the Reserve section, and the FAQ — so
change all three together.

## The reservation form

As written, submitting opens a pre-filled email in the visitor's mail app. That
works, but it loses anyone without mail set up. To collect submissions properly,
pick one:

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

## Park rules and the site agreement (sent by email, not published)

The Master Rules, Policies & Monthly Site Agreement is deliberately not on the
site. When someone submits the reservation form, reply with the Word file
attached and the invitation below. Keep the file outside this public repo.

Subject: Your Rocket Farm reservation — next steps

> Hi [name],
>
> Thanks for reaching out about a space at Rocket Farm. We'd be glad to have
> you. I've attached our park rules and monthly site agreement so you can read
> exactly how the park runs before you put down a deposit: rent on the 1st,
> quiet hours 10 PM to 7 AM, keep your site clean, and look out for each other.
> It's plain English and it's the same for everyone.
>
> To hold [space / a 50-amp monthly space] for you, the reservation deposit is
> $250. It's credited to your first month, refunded in full if we can't
> deliver the space, and not refundable if you choose to stay somewhere else.
> [Payment link or instructions.]
>
> If anything in the agreement raises a question, reply here or call me at
> [phone]. Looking forward to seeing you on Farmer Road.
>
> [Your name]
> Rocket Farm LLC · 10729 Farmer Road, Kaplan, LA 70548

The agreement was restructured around Louisiana law (stipulated late charges
capped at 20% of rent, a separately initialed waiver of the notice to vacate,
no self-help removal, a security deposit handled under R.S. 9:3251-3254, no
advance release for physical injury). It is still not legal advice; have a
Louisiana attorney read it once before the first occupant signs.

## Deploying to therocketfarm.com

The repo already contains everything the deploy needs:

| File          | Purpose                                                        |
|---------------|----------------------------------------------------------------|
| `index.html`  | the page                                                       |
| `og.png`      | 1200×630 link preview image (referenced by absolute URL)        |
| `CNAME`       | tells GitHub Pages to serve the site at `therocketfarm.com`      |
| `robots.txt`  | allows crawling, points at the sitemap                          |
| `sitemap.xml` | one entry, the homepage                                         |

### 1. Turn on Pages

Settings → Pages → Source: *Deploy from a branch* → folder `/ (root)`, and pick
the branch this code is on. Because the `CNAME` file is committed, GitHub sets
the custom domain automatically; tick **Enforce HTTPS** once the certificate is
issued (usually a few minutes, sometimes up to an hour).

### 2. Point the DNS

For the apex domain `therocketfarm.com`, create four `A` records and four
`AAAA` records at your registrar, all on the root (`@`):

```
A     @   185.199.108.153
A     @   185.199.109.153
A     @   185.199.110.153
A     @   185.199.111.153
AAAA  @   2606:50c0:8000::153
AAAA  @   2606:50c0:8001::153
AAAA  @   2606:50c0:8002::153
AAAA  @   2606:50c0:8003::153
```

And so `www` works too:

```
CNAME www brison-creator.github.io.
```

Verify those addresses against GitHub's current documentation before you commit
to them — GitHub has changed its Pages IPs before:
<https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site>

DNS can take anywhere from a few minutes to a couple of hours to propagate.

### 3. Make sure the mailbox exists

The page sends waitlist enquiries to **stay@therocketfarm.com**, in the footer
link and in the form script. If that mailbox does not receive mail yet, create
it (or a forwarder) before you share the link, or enquiries will bounce.

## Directions

The Location section links out to the visitor's own maps app rather than
embedding a map, using the documented Google Maps `api=1` URL scheme and an
Apple Maps `daddr` link. That returns a **live** drive time from wherever the
visitor actually is, needs no API key, and adds no third-party tracking to the
page. The "Driving from" chips pre-fill an origin so the route opens ready.

The distances and times printed beside them are approximate planning figures,
labelled as such on the page.

**Two things to check before you promote the directions:**

1. `10729 Farmer Road` is not in OpenStreetMap, and a new rural parcel is often
   missing or mis-pinned in Google Maps too. Open the Directions link yourself
   and confirm it lands at the right gate. If it does not, create a Google
   Business Profile for the park — that gives you a verified pin you control.
2. Once the entrance is surveyed and staked, send the coordinates and they can
   be dropped straight into the links, which removes the geocoding guesswork
   entirely.

## SEO

The page is built mobile-first for search, since that is how Google indexes.

**Head:** title is 56 characters so it survives a mobile SERP; description is
155, down from 208 where it was being truncated. `robots` carries
`max-image-preview:large` so the share image can appear full-width on phones.
Canonical, Open Graph and Twitter titles/descriptions are all set, plus an
apple-touch-icon.

**Fonts do not block first paint.** The Google Fonts stylesheet is fetched as a
`preload` and promoted with `media="print" onload="this.media='all'"`, with a
plain `<link>` in `<noscript>`. That takes a render-blocking request off the
critical path, which is the single biggest lever on mobile LCP here.

**Mobile usability:** form fields are 16px, below which iOS Safari zooms the
viewport on focus. Every touch target is at least 44px high at 320-430px. No
horizontal overflow at any width from 320px up.

**Structured data:** two JSON-LD blocks — a `Campground` with address, price
range, `areaServed`, amenity list and three `Offer` entries carrying the real
per-tier rates, and a `FAQPage` mirroring the visible FAQ. The schema questions
and the on-page questions are generated from one list so they cannot drift;
mismatched FAQ markup is what earns a manual action.

Worth being honest about `FAQPage`: since Google's 2023 change, FAQ rich
results are largely limited to authoritative government and health sites, so
do not expect the accordion to show as stars in the SERP. It earns its place as
real content answering real long-tail queries — "how much is a monthly RV space
in Kaplan", "how far is X from the Starbase Louisiana launch site" — and that
copy is also what AI answer engines quote.

**Not set: `geo` coordinates.** `10729 Farmer Road` is absent from
OpenStreetMap, and a latitude/longitude guessed from the town centre would pin
the business in the wrong field. The postal address is enough for Google.
Create a Google Business Profile for the authoritative pin, or send surveyed
coordinates and `geo` can be added properly.

**After launch, do these three things:** verify the domain in Google Search
Console and submit `sitemap.xml`; create the Google Business Profile (for a
local business this outranks anything on-page for map results); and run the
Rich Results Test on the live URL to confirm both JSON-LD blocks parse.

## Search and social

- `<link rel="canonical">`, `og:url`, `og:image` and `twitter:image` all use
  absolute `https://therocketfarm.com/` URLs — Open Graph requires absolute
  paths, so these must be updated if the domain ever changes.
- `og.png` is generated, not hand-drawn. To regenerate it after a copy change,
  re-render a 1200×630 card and overwrite the file; nothing else references it.
- A JSON-LD `Campground` block in `<head>` carries the address, price range and
  amenities for local search results. Keep its `email`, `priceRange` and address
  in step with the page if you change them.

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
