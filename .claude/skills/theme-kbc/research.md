# theme-kbc: research notes (30 Sept 2026)

Time-boxed (~6 min). Business facts come from `/be-domain` (`be-domain/references/facts.md`), not re-researched.

## Sources
1. kbc.be homepage HTML: https://www.kbc.be/particulieren/nl.html
2. kbc.be global stylesheet: https://wcmassets.kbc.be/etc.clientlibs/kbc/global/websites/head.min.ACSHASH6d1330f512cfd258336aefc5edbf149c.css (plus the other `wcmassets.kbc.be/etc.clientlibs/...css` files linked from source 1)
3. Web search summary of third-party brand-colour sites (Brandfetch https://brandfetch.com/kbc.com, BrandColorCode https://www.brandcolorcode.com/kbc-bank-ireland). Brandfetch returned 403 to a direct fetch.
4. KBC Newsroom, Kate: https://newsroom.kbc.com/kate-five-years-and-five-milestones (via `/be-domain`)

## Verified (seen in KBC's own files)
- `#00AEEF` appears 3× in the kbc.be global stylesheet (2). Third-party sites (3) also name it the KBC light blue ("Pantone 306 C" per BrandColorCode, not checked).
- `#80C342` (green) appears in the same stylesheet (2).
- `#0D2A50` (dark navy) and `#0097DB` (blue) appear in the homepage HTML (1). Their role there was not checked.
- Font: `font-family: "MuseoSans", sans-serif` is used ~80× across the kbc.be stylesheets. There is also an icon font `iconskbc` (not used: brand asset).
- Radii in the stylesheet (2): `5px`, `30px`, `0 0 5px 5px`.
- Tone (1): informal, reassuring, stress-free. Example slogan: "No stress. Kate it."
- Business (4, via be-domain): Kate has 5.8M active users, solves 70% of questions on its own, and KBC says Kate "will never act without explicit customer approval".

## Estimated (chosen, not found)
- `--th-primary #006A9E`: #00AEEF fails WCAG AA as text on white (~2.5:1), so a darker cerulean is used for buttons and links (~5.9:1).
- `--th-muted #4A5B70`, `--th-surface #F2F8FC`, `--th-line #D3E3EE`, `--th-success-ink #2E6B12`, `--th-danger #B3261E`.
- `#003665` "Midnight Blue" is given by third-party sources only (3). It is not used; the verified `#0D2A50` is used instead.
- Shadow, motion timings and the top gradient line are design choices, not KBC specs.

## Guessed
- The role of `#0D2A50` as a text/heading colour (it is dark enough and appears on the site).
- That the 30px radius is used for pill buttons.

## Open questions
- The official KBC brand guide (colour names, secondary palette, dark mode) was not public in the time box.
- Which colours the KBC Mobile app / Kate UI actually uses (no app screenshots checked).
- MuseoSans is a licensed font: it is not bundled. Offline the theme falls back to Segoe UI / system-ui.
