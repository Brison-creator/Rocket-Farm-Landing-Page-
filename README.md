# Rocket Farm — landing page

A single-file landing page for **Rocket Farm LLC**, a full-hookup RV park in
development at 10729 Farmer Road, Kaplan, Louisiana (Vermilion Parish).

Everything lives in `index.html` — markup, styles and one small script. No build
step, no dependencies, no framework. Open the file in a browser and it works.

## Sections

1. **Hero** — positioning and the primary waitlist call to action
2. **At a glance** — 17 sites, ~30 mi from the launch campus, targeted 2027, Zone X
3. **Who it's for** — crews and contractors, launch watchers, sportsmen and families
4. **The park** — Phase 1 site amenities
5. **What's planned** — Phase 1, Phase 2, and the big-pond view deck
6. **Location** — the address and approximate drive times
7. **Waitlist** — interest capture form
8. **Footer** — contact, development disclaimer, non-affiliation notice

## Before you publish

Two things need your real details. Both are marked with `TODO` in `index.html`.

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

   With either one, delete the `<script>` block at the bottom of the file — it
   calls `preventDefault()` and would stop the real submission.

## Deploying on GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → branch `main`, folder `/ (root)`.
The page goes live at `https://<user>.github.io/<repo>/` within a minute or two.

To use a custom domain, add a `CNAME` file containing just the domain
(e.g. `rocketfarm.com`), then point the DNS at GitHub Pages.

## Editing copy

All text is plain HTML — search for the phrase you want to change and edit it in
place. Colors, fonts and spacing are CSS custom properties in the `:root` block
at the top of the `<style>` tag; changing `--amber` and `--sunset` restyles the
whole page.

## A note on content

This page is deliberately guest-facing. None of the figures from the Phase 1 or
Phase 2 financing binders — project cost, sources and uses, NOI, DSCR, loan
amounts, pro forma — appear anywhere in it, and they shouldn't. Rates shown are
marked as planned, and the footer carries a development disclaimer plus a
non-affiliation notice regarding SpaceX.
