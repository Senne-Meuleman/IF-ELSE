import { useCallback, useEffect, useRef, useState } from "react";
import { ApiError } from "./api";
import type { Card, Component, Decision, HomeResponse, LayoutPrefState, TimelineResponse } from "./api";
import { data, MOCK } from "./data";
import ControlPanel from "./demo/ControlPanel";
import Login from "./Login";
import Phone from "./Phone";
import PhoneScaler from "./PhoneScaler";

interface Session { role: "customer" | "advisor"; username: string }

const DEMO_PASSWORD = "demo";

export default function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [checked, setChecked] = useState(false);
  const [asOf, setAsOf] = useState<string | null>(null);
  const [home, setHome] = useState<HomeResponse | null>(null);
  const [timeline, setTimeline] = useState<TimelineResponse | null>(null);
  const [explain, setExplain] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<string | null>(null);
  const reqSeq = useRef(0);

  const showToast = useCallback((msg: string) => {
    setToast(msg);
    window.setTimeout(() => setToast((t) => (t === msg ? null : t)), 2200);
  }, []);

  const fail = useCallback((e: unknown) => {
    if (e instanceof ApiError && e.status === 401) {
      setSession(null); setHome(null); setTimeline(null);
      return;
    }
    setError(e instanceof Error ? e.message : String(e));
  }, []);

  const loadHome = useCallback(async (date: string | null) => {
    const seq = ++reqSeq.current;
    setBusy(true); setError(null);
    try {
      const h = await data.home(date ?? undefined);
      if (seq === reqSeq.current) setHome(h);
    } catch (e) { fail(e); } finally { if (seq === reqSeq.current) setBusy(false); }
  }, [fail]);

  const loadAll = useCallback(async (date: string | null) => {
    setBusy(true); setError(null);
    try {
      const [h, t] = await Promise.all([data.home(date ?? undefined), data.timeline()]);
      reqSeq.current++;
      setHome(h); setTimeline(t);
    } catch (e) { fail(e); } finally { setBusy(false); }
  }, [fail]);

  // Initial: is there a session?
  useEffect(() => {
    (async () => {
      try {
        const s = await data.session();
        setSession(s);
        await loadAll(null);
      } catch (e) {
        if (!(e instanceof ApiError && e.status === 401)) fail(e);
      } finally { setChecked(true); }
    })();
  }, [fail, loadAll]);

  const login = useCallback(async (username: string, password: string) => {
    setError(null);
    try {
      const s = await data.login(username, password);
      setSession(s); setAsOf(null);
      await loadAll(null);
    } catch (e) { setError(e instanceof Error ? e.message : String(e)); }
  }, [loadAll]);

  const switchCustomer = useCallback(async (username: string) => {
    setBusy(true); setError(null);
    try {
      if (session) await data.logout().catch(() => undefined);
      const s = await data.login(username, DEMO_PASSWORD);
      setSession(s); setAsOf(null); setHome(null); setTimeline(null);
      await loadAll(null);
    } catch (e) { fail(e); } finally { setBusy(false); }
  }, [session, loadAll, fail]);

  const logout = useCallback(async () => {
    await data.logout().catch(() => undefined);
    setSession(null); setHome(null); setTimeline(null); setAsOf(null);
  }, []);

  const onAsOf = useCallback((date: string | null) => {
    setAsOf(date);
    void loadHome(date);
  }, [loadHome]);

  const apply = useCallback(async (fn: () => Promise<HomeResponse>) => {
    setBusy(true); setError(null);
    try { setHome(await fn()); } catch (e) { fail(e); } finally { setBusy(false); }
  }, [fail]);

  const onFeedback = useCallback((card: Card, decision: Decision) => {
    const label: Record<Decision, string> = { dismiss: "Dismissed", snooze: "Snoozed for 7 days", less: "Fewer cards like this", accept: "Marked as done", reset: "Feedback reset" };
    showToast(label[decision]);
    void apply(() => data.feedback(card.card_key, card.card_type, decision, asOf ?? undefined));
  }, [apply, asOf, showToast]);

  const onResetFeedback = useCallback(() => {
    showToast("Feedback reset");
    void apply(() => data.feedback("reset", "scam_awareness", "reset", asOf ?? undefined));
  }, [apply, asOf, showToast]);

  const onLayoutPref = useCallback((component: Component, state: LayoutPrefState) => {
    showToast(state === "pinned" ? `Pinned ${component}` : state === "hidden" ? `Hidden ${component}` : "Layout reset");
    void apply(() => data.layoutPref(component, state, asOf ?? undefined));
  }, [apply, asOf, showToast]);

  const onConsent = useCallback((v: boolean) => {
    showToast(v ? "Commercial personalisation on" : "Commercial personalisation off");
    void apply(() => data.consent(v, asOf ?? undefined));
  }, [apply, asOf, showToast]);

  const onCta = useCallback((action: string) => showToast(`Simulated: ${action.replace(/_/g, " ")}`), [showToast]);

  return (
    <div className="shell">
      <ControlPanel
        username={session?.username ?? null}
        home={home}
        timeline={timeline}
        asOf={asOf}
        explain={explain}
        busy={busy}
        error={error}
        mock={MOCK}
        onSwitchCustomer={(u) => void switchCustomer(u)}
        onAsOf={onAsOf}
        onExplain={setExplain}
        onConsent={onConsent}
        onResetFeedback={onResetFeedback}
        onLogout={() => void logout()}
      />
      <main className="stage-area">
        <div className="stage-area-bg" />
        {!checked ? null : (
          <PhoneScaler>
            {!session || !home ? (
              <Login onLogin={login} error={error} />
            ) : (
              <Phone
                home={home}
                asOf={asOf ?? home.as_of}
                explain={explain}
                loading={busy}
                toast={toast}
                onFeedback={onFeedback}
                onCta={onCta}
                onLayoutPref={onLayoutPref}
              />
            )}
          </PhoneScaler>
        )}
      </main>
    </div>
  );
}
