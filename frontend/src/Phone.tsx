import { AnimatePresence, LayoutGroup, motion } from "framer-motion";
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

  return (
    <div className="phone-bezel">
      <div className="phone" style={themeVars(theme)}>
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
                  return (
                    <motion.div
                      key={s.component}
                      layout
                      layoutId={s.component}
                      className={`section ${s.size}`}
                      initial={{ opacity: 0, scale: 0.96, y: 14 }}
                      animate={{ opacity: 1, scale: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.94, transition: { duration: 0.2 } }}
                      transition={{ type: "spring", stiffness: 300, damping: 30, mass: 0.9 }}
                    >
                      <C props={s.props} ctx={ctx} />
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
