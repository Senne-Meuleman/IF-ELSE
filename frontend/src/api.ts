// Typed client. Mirrors backend/app/schemas.py — keep both in sync.

export type Persona = "student" | "young_professional" | "young_family" | "freelancer" | "retiree";
export type Family = "deadline" | "anomaly" | "forecast" | "opportunity" | "milestone" | "protection";
export type Stage = "early" | "soon" | "urgent" | "info";
export type CardType =
  | "insurance_renewal" | "vat_reserve" | "price_increase" | "duplicate_charge"
  | "runway" | "cashflow_squeeze" | "idle_cash" | "life_event" | "scam_awareness";
export type Decision = "dismiss" | "snooze" | "less" | "accept" | "reset";
export type LayoutPrefState = "pinned" | "hidden" | "reset";
export type Component =
  | "BalanceHero" | "RunwayHero" | "FamilyBudgetHero" | "TaxReserveHero" | "PensionHero"
  | "ForYouFeed" | "QuickActions" | "UpcomingBills" | "SplitBills" | "InvoiceTracker"
  | "SavingsGoal" | "ScamShield" | "AdvisorContact" | "SpendingByCategory";
export type Density = "compact" | "comfortable" | "large";
export type Tone = "casual" | "neutral" | "warm" | "business" | "formal";
export type Contrast = "normal" | "high";
export type Size = "hero" | "full" | "half";

export interface PersonaWeight { persona: Persona; weight: number; evidence: string[] }
export interface Cta { label: string; action: string }
export interface Card {
  card_key: string;
  card_type: CardType;
  family: Family;
  stage: Stage;
  title: string;
  body: string;
  eur_impact: number;
  due_date: string | null;
  confidence: number;
  commercial: boolean;
  evidence: string[];
  rank_explanation: string;
  score: number;
  cta: Cta | null;
  details: Record<string, unknown>;
}
export interface Theme { density: Density; tone: Tone; contrast: Contrast }
export interface Section { component: Component; size: Size; props: Record<string, unknown> }
export interface Layout { version: number; theme: Theme; sections: Section[]; explanations: Record<string, string> }
export interface Feed { cards: Card[]; caught_up: boolean; hidden_count: number }
export interface CustomerPublic { first_name: string; language: "nl" | "fr"; consent_personalization: boolean }
export interface HomeResponse {
  as_of: string;
  customer: CustomerPublic;
  persona_mix: PersonaWeight[];
  layout: Layout;
  feed: Feed;
  generated_at: string;
  llm_copy: boolean;
}
export interface Milestone { date: string; label: string }
export interface TimelineResponse { min_date: string; max_date: string; milestones: Milestone[] }
export interface LoginResponse { role: "customer" | "advisor"; username: string }
export interface AdvisorOverview {
  customers_scored: number;
  scoring_ms: number;
  projected_2_3m_seconds: number;
  persona_distribution: Record<string, number>;
  card_volume: Record<string, number>;
  eur_impact_total: number;
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) { super(message); this.status = status; }
}

async function call<T>(method: string, path: string, body?: unknown): Promise<T> {
  const res = await fetch(path, {
    method,
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
    credentials: "same-origin",
  });
  if (!res.ok) {
    let detail = res.statusText;
    try { detail = (await res.json()).detail ?? detail; } catch { /* ignore */ }
    throw new ApiError(res.status, String(detail));
  }
  return res.json() as Promise<T>;
}

export const api = {
  login: (username: string, password: string) => call<LoginResponse>("POST", "/api/login", { username, password }),
  logout: () => call<{ ok: boolean }>("POST", "/api/logout"),
  session: () => call<LoginResponse>("GET", "/api/me/session"),
  home: (asOf?: string) => call<HomeResponse>("GET", asOf ? `/api/me/home?as_of=${asOf}` : "/api/me/home"),
  timeline: () => call<TimelineResponse>("GET", "/api/me/timeline"),
  feedback: (card_key: string, card_type: CardType, decision: Decision, asOf?: string) =>
    call<HomeResponse>("POST", asOf ? `/api/me/feedback?as_of=${asOf}` : "/api/me/feedback", { card_key, card_type, decision }),
  layoutPref: (component: Component, state: LayoutPrefState, asOf?: string) =>
    call<HomeResponse>("POST", asOf ? `/api/me/layout-prefs?as_of=${asOf}` : "/api/me/layout-prefs", { component, state }),
  consent: (consent_personalization: boolean, asOf?: string) =>
    call<HomeResponse>("POST", asOf ? `/api/me/consent?as_of=${asOf}` : "/api/me/consent", { consent_personalization }),
  advisorOverview: () => call<AdvisorOverview>("GET", "/api/advisor/overview"),
};
