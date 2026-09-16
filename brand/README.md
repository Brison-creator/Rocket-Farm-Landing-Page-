# Rocket Farm — logo & merch kit

Four designs, each supplied in full colour and in single-ink versions for light
and dark garments. All lettering is **converted to outlines**, so nothing here
depends on a font being installed — hand the SVGs to any printer.

## What's in here

| File | Use |
|---|---|
| `rocket-farm-patch.svg` | **Mission patch** — the primary mark. Left chest, hats, stickers, embroidered patches |
| `rocket-farm-icon.svg` | **Icon** — rocket whose plume becomes planted rows. Hats, pocket prints, app icon |
| `rocket-farm-wordmark.svg` | **Wordmark** — site header, invoices, signage, business cards |
| `rocket-farm-stacked.svg` | Stacked lockup for square spaces |
| `rocket-farm-backprint-*.svg` | **Back print** — big arched design with the legal land description |
| `rocket-farm-tee-scrubbed-*.svg` | **Launch status: SCRUBBED** — the joke shirt for launch watchers |

Suffixes: no suffix = full colour · `-1c-light` = one ink, cream (for **dark**
garments) · `-1c-dark` = one ink, navy (for **light** garments).

`png/` holds transparent PNG exports at print resolution (patch 2400px, back
prints 2700px wide) for merch sites that won't take vector.

## Palette

| Colour | Hex | Screen print | Use |
|---|---|---|---|
| Night navy | `#0b1226` | Pantone 296 C (nearest) | Patch field, dark ink |
| Amber | `#f5a524` | Pantone 1235 C (nearest) | Ring, plume, accents |
| Sunset | `#e8623c` | Pantone 1655 C (nearest) | Rocket flame only |
| Cream | `#f4efe6` | Pantone 7527 C (nearest) | Light ink, lettering |
| Marsh green | `#3f9d7f` | Pantone 3295 C (nearest) | The field |

Pantone equivalents are **eyeballed from the hex values, not measured.** Ask your
printer to pull physical chips and confirm before you approve a run.

## Print notes

- **Cheapest good result:** the one-ink patch on a dark shirt. One screen, one
  pass, and it still reads as a mission patch.
- **Full-colour patch** is 4 inks (navy, amber, sunset, cream). Use it for
  embroidered patches and stickers, where colour count costs nothing.
- **Embroidery:** use the one-ink patch as the basis and expect the digitiser to
  simplify the furrows and the rice grains. Don't go below 3 in / 75 mm across,
  or the field rows will fill in.
- **Small sizes:** below about 1 in / 25 mm, drop the patch and use the icon or
  the plain rocket. The ring lettering will not hold.
- Minimum stroke anywhere in these files is about 3 units at a 600-unit
  viewBox — safe for screen print at 3 in and up.
- All knockouts (the porthole, `KAPLAN, LA` in the banner) are `fill-rule`
  holes, not white shapes, so the garment colour shows through. Don't let anyone
  "fix" them by filling them white.

## Regenerating

The art is generated, not hand-drawn, so edits are repeatable:

```bash
pip install fonttools
curl -o brand/sg-bold.ttf \
  "https://fonts.gstatic.com/s/spacegrotesk/v22/V8mQoQDjQSkFtoMM3T6r8E7mF71Q-gOoraIAEj4PVksj.ttf"
python3 brand/generate.py
```

The font (Space Grotesk, SIL Open Font License) is only needed to *build* the
files; it is deliberately not committed. The generated SVGs have no font
dependency.

## One important limit — SpaceX

These designs deliberately evoke **launch culture**: mission-patch layout,
arched type, a rocket, a scrubbed launch. None of that belongs to anybody, and
it's what makes the shirt feel like an insider object.

What you must **not** put on merchandise:

- The names **SpaceX**, **Starship**, **Starbase**, **Falcon**, **Raptor**
- The SpaceX logo, wordmark, or their distinctive typeface
- Anything implying SpaceX endorses, sponsors, or is affiliated with Rocket Farm

Those are registered trademarks, SpaceX enforces them, and merchandise is the
most exposed possible use — you're selling goods that carry the mark, which is
exactly what trademark law covers. A disclaimer does not fix it, because the
problem is customers assuming an association. Shirts also travel and photograph,
so this is the one place where a cheap mistake gets expensive.

What *is* defensible is plain geography, in ordinary descriptive words, on your
own website rather than on goods: "thirty miles north of Louisiana's launch
site." The site copy already does this, and deliberately never names SpaceX.

If you want the association harder than this, get 20 minutes with a Louisiana
trademark attorney before you print. Not legal advice — just where the line
sits and why I drew it here.
