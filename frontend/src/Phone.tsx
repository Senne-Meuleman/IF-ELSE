import { useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, LayoutGroup, motion, type HTMLMotionProps } from "framer-motion";
import AccountsZoom, { type ZoomOrigin } from "./accounts/AccountsZoom";
import { accountsFor } from "./accounts/accounts";
import { ChevronRight } from "./accounts/glyphs";
import type { Card, Component, Decision, HomeResponse, LayoutPrefState } from "./api";
import { NAV_ICONS } from "./components/icons";
import { resolve } from "./components/registry";
import type { SectionCtx } from "./components/types";
import { longDate, PERSONA_LABEL, pct } from "./format";
import { greeting, themeVars } from "./theme";

interface Props {
  home: HomeResponse;
  asOf: string;
  explain: boolean;
  loading: boolean;
  toast: string | null;
  onFeedback: (card: Card, decision: Decision) => void;
  onCta: (action: string) => void;
  onLayoutPref: (component: Component, state: LayoutPrefState) => void;
}

export default function Phone({ home, asOf, explain, loading, toast, onFeedback, onCta, onLayoutPref }: Props) {
  const theme = home.layout.theme;
  const ctx: SectionCtx = { home, asOf, explain, onFeedback, onCta };
  const mix = home.persona_mix.map((p) => `${pct(p.weight)} ${PERSONA_LABEL[p.persona] ?? p.persona}`).join(" · ");
  const themeExplain = home.layout.explanations["theme"];
  const initials = home.customer.first_name.slice(0, 1).toUpperCase();

  // The hero tile opens the accounts screen with a zoom.
  const phoneRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLElement | null>(null);
  const restoreFocus = useRef(false);
  const [zoom, setZoom] = useState<ZoomOrigin | null>(null);
  const [tileHidden, setTileHidden] = useState(false);
  const heroSection = home.layout.sections.find((s) => s.size === "hero");
  const HeroC = heroSection ? resolve(heroSection.component) : null;
  const accounts = useMemo(() => accountsFor(home, heroSection), [home, heroSection]);

  // A different customer or hero means the tile we zoomed from is gone: close.
  const heroKey = `${home.customer.first_name}|${heroSection?.component ?? ""}`;
  useEffect(() => { setZoom(null); }, [heroKey]);

  // After the zoom closes, hand the keyboard focus back to the tile (it can only take focus once visible again).
  useEffect(() => {
    if (!tileHidden && restoreFocus.current) {
      restoreFocus.current = false;
      triggerRef.current?.focus({ preventScroll: true });
    }
  }, [tileHidden]);

  const openAccounts = (tile: HTMLElement) => {
    const phone = phoneRef.current;
    if (!phone || !accounts) return;
    const p = phone.getBoundingClientRect();
    const k = p.width / phone.offsetWidth || 1; // PhoneScaler shrinks the phone with a CSS transform
    const r = tile.getBoundingClientRect();
    triggerRef.current = tile;
    setZoom({
      x: (r.left - p.left) / k,
      y: (r.top - p.top) / k,
      w: r.width / k,
      h: r.height / k,
      radius: parseFloat(getComputedStyle(tile).borderTopLeftRadius) || 20,
      variant: tile.querySelector<HTMLElement>(".hero")?.className ?? "hero",
      stageW: phone.offsetWidth,
      stageH: phone.offsetHeight,
    });
    setTileHidden(true);
  };

  const tileProps: HTMLMotionProps<"div"> = {
    role: "button",
    tabIndex: 0,
    "aria-label": "Show all accounts",
    onClick: (e) => openAccounts(e.currentTarget),
    onKeyDown: (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openAccounts(e.currentTarget); }
    },
  };

  return (
    <div className="phone-bezel">
      <div className="phone" ref={phoneRef} style={themeVars(theme)}>
        <div className="phone-top">
          <div className="greet">
            <div>
              <h1>{greeting(theme.tone, home.customer.first_name)}</h1>
              <div className="date">{longDate(home.as_of)}</div>
            </div>
            <div className="avatar">{initials}</div>
          </div>
          <AnimatePresence initial={false}>
            {explain && (
              <motion.div
                className="explain-head"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
              >
                <div><b>Composed for:</b> {mix}</div>
                {themeExplain && <div>{themeExplain}</div>}
                <div style={{ opacity: .8 }}>theme: {theme.density} · {theme.tone} · {theme.contrast} contrast</div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {loading && <div className="phone-loading">updating…</div>}

        <div className="phone-scroll">
          <LayoutGroup id="home-sections">
            <div className="sections">
              <AnimatePresence initial={false} mode="popLayout">
                {home.layout.sections.map((s) => {
                  const C = resolve(s.component);
                  if (!C) return null;
                  const why = home.layout.explanations[s.component];
                  const tappable = s.size === "hero" && accounts !== null;
                  return (
                    <motion.div
                      key={s.component}
                      layout
                      layoutId={s.component}
                      className={`section ${s.size}${tappable ? " tappable" : ""}${tappable && tileHidden ? " tile-hidden" : ""}`}
                      initial={{ opacity: 0, scale: 0.96, y: 14 }}
                      animate={{ opacity: 1, scale: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.94, transition: { duration: 0.2 } }}
                      transition={{ type: "spring", stiffness: 300, damping: 30, mass: 0.9 }}
                      {...(tappable ? tileProps : {})}
                    >
                      <C props={s.props} ctx={ctx} />
                      {tappable && <span className="hero-chevron" aria-hidden="true"><ChevronRight /></span>}
                      {explain && (
                        <div className="explain-badge">
                          <span>{why ?? `${s.component}: no explanation provided.`}</span>
                          {s.component !== "ForYouFeed" && s.size !== "hero" && (
                            <span className="tools">
                              <button type="button" title="Pin this section" onClick={() => onLayoutPref(s.component, "pinned")}>📌</button>
                              <button type="button" title="Hide this section" onClick={() => onLayoutPref(s.component, "hidden")}>hide</button>
                            </span>
                          )}
                        </div>
                      )}
                    </motion.div>
                  );
                })}
              </AnimatePresence>
            </div>
          </LayoutGroup>
        </div>

        <AnimatePresence
          onExitComplete={() => {
            restoreFocus.current = true;
            setTileHidden(false);
          }}
        >
          {zoom && accounts && HeroC && heroSection && (
            <AccountsZoom
              key="accounts"
              origin={zoom}
              view={accounts}
              home={home}
              hero={heroSection}
              tile={<HeroC props={heroSection.props} ctx={ctx} />}
              onClose={() => setZoom(null)}
            />
          )}
        </AnimatePresence>

        <AnimatePresence>
          {toast && (
            <motion.div className="toast" key={toast} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 10 }}>
              {toast}
            </motion.div>
          )}
        </AnimatePresence>

        <nav className="bottom-nav" aria-label="Main navigation">
          <div className="active"><NAV_ICONS.home />Home</div>
          <div><NAV_ICONS.pay />Pay</div>
          <div><NAV_ICONS.cards />Cards</div>
          <div><NAV_ICONS.more />More</div>
        </nav>
      </div>
    </div>
  );
}
