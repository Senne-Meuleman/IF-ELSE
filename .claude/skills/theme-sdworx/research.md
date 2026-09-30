# theme-sdworx: research notes (30 Sept 2026)

Time-boxed (~6 min). Business facts come from `/be-domain` (`be-domain/references/facts.md`), not re-researched.

## Sources
1. SD Worx homepage: https://www.sdworx.com/en-en
2. SD Worx "Ignite" design-system CSS, linked from source 1: https://cdn.sdworx.com/ignite/styling/v2/2.2.0/website/system.css and https://cdn.sdworx.com/ignite/assets/v2/fonts/all.css
3. SD Worx AI page: https://www.sdworx.com/en-en/about-sd-worx/artificial-intelligence
4. Web search summary of third-party brand-colour sites (Brandfetch https://brandfetch.com/sdworx.com returned 403; GitHub https://github.com/EuphoriaxCode/SDWorx_brand). This is not an official source.

## Verified (from SD Worx's own files)
- Ignite tokens (2): text-primary `#005BBF`, primary hover `#006DD8`, primary-strong `#000D3A`,
  primary-subtle bg `#EFFAFF` / `#D9F1FF`, dark-mode tokens `#9ED2FF` / `#0087F3`.
  Most frequent neutrals: `#F4F5F6`, `#212223`, `#444547`, `#323334`, `#D9DBDD`, `#FBFCFC`.
  Accent-0 `#DA3300` (pressed `#C42600`), accent-1 `#FFA659`.
- The CSS uses `light-dark()`, so Ignite supports dark mode.
- Fonts (1, 2): `Inter` (body), `SD Worx Display` / `SD Worx Display VF` (display, proprietary).
- Radius: `border-radius: 4px` in the system CSS (2), found once.
- Homepage colours (1): `#1D2830`, `#575757`, `#040D14`, `#F4F5F8`.
- Tone (1): "Built for how Europe works", "from complexity to confidence",
  "the backbone of work in Europe", "let's talk about your people, pay & time".
- AI stance (3): "humans manage exceptions, nuanced decisions, and interactions that require insight and empathy".
- Business (via be-domain): pays 6M+ employees a month for 100,000+ organisations. The June 2026
  multi-agent payroll model is supervised by humans.

## Estimated (chosen, not found)
- `#006DD8` as *the* primary button colour. In Ignite it is the text-primary hover, and the
  third-party source (4) calls it the logo blue. It passes AA on white.
- 8px card radius, shadow, `--th-success #1E8E3E`, `--th-success-ink #1B6E31`, and
  `#C42600` used as a danger colour (Ignite uses it as a pressed accent).
- Motion timings and the navy → blue → warm top line are design choices.

## Guessed
- Logo colours red `#F1002F` and yellow `#FFBE00` (third-party only, source 4). They are not used.
- The "human" look (people-first copy, a warm accent used sparingly) is our reading of the tone, not a published SD Worx rule.

## Open questions
- The official brand guide and the logo colour roles were not public in the time box.
- What mysdworx (the customer platform) looks like in the app: no screenshots checked.
- The Inter font is not bundled. Offline the theme falls back to Segoe UI / system-ui unless Inter is installed.
