// Thin layer over the API that switches to the mock fixture when the URL has ?mock=1.
import { api } from "./api";
import type { CardType, Component, Decision, HomeResponse, LayoutPrefState, LoginResponse, TimelineResponse } from "./api";
import mockHome from "../mock/home_sara.json";

export const MOCK = typeof window !== "undefined" && new URLSearchParams(window.location.search).get("mock") === "1";

let mockState: HomeResponse = structuredClone(mockHome as unknown as HomeResponse);
let mockHiddenExtra = 0;

const mockTimeline: TimelineResponse = {
  min_date: "2018-09-01",
  max_date: "2026-09-30",
  milestones: [
    { date: "2018-09-15", label: "Student" },
    { date: "2021-07-01", label: "First salary" },
    { date: "2022-04-01", label: "Mortgage" },
    { date: "2024-02-10", label: "Baby" },
    { date: "2026-01-05", label: "Went freelance" },
  ],
};

function withAsOf(asOf?: string): HomeResponse {
  const copy = structuredClone(mockState);
  if (asOf) copy.as_of = asOf;
  copy.feed.hidden_count = (mockHome as unknown as HomeResponse).feed.hidden_count + mockHiddenExtra;
  return copy;
}

export const data = {
  login(username: string, password: string): Promise<LoginResponse> {
    if (MOCK) return Promise.resolve({ role: "customer", username });
    return api.login(username, password);
  },
  session(): Promise<LoginResponse> {
    if (MOCK) return Promise.resolve({ role: "customer", username: "sara" });
    return api.session();
  },
  logout(): Promise<{ ok: boolean }> {
    if (MOCK) return Promise.resolve({ ok: true });
    return api.logout();
  },
  home(asOf?: string): Promise<HomeResponse> {
    if (MOCK) return Promise.resolve(withAsOf(asOf));
    return api.home(asOf);
  },
  timeline(): Promise<TimelineResponse> {
    if (MOCK) return Promise.resolve(mockTimeline);
    return api.timeline();
  },
  feedback(card_key: string, card_type: CardType, decision: Decision, asOf?: string): Promise<HomeResponse> {
    if (MOCK) {
      if (decision === "reset") {
        mockState = structuredClone(mockHome as unknown as HomeResponse);
        mockHiddenExtra = 0;
      } else {
        const before = mockState.feed.cards.length;
        mockState.feed.cards = mockState.feed.cards.filter((c) => c.card_key !== card_key);
        mockHiddenExtra += before - mockState.feed.cards.length;
      }
      return Promise.resolve(withAsOf(asOf));
    }
    return api.feedback(card_key, card_type, decision, asOf);
  },
  layoutPref(component: Component, state: LayoutPrefState, asOf?: string): Promise<HomeResponse> {
    if (MOCK) {
      if (state === "hidden") {
        mockState.layout.sections = mockState.layout.sections.filter((s) => s.component !== component);
        mockState.layout.explanations[component] = "Hidden by you.";
      } else if (state === "pinned") {
        mockState.layout.explanations[component] = "Pinned by you.";
      }
      return Promise.resolve(withAsOf(asOf));
    }
    return api.layoutPref(component, state, asOf);
  },
  consent(consent: boolean, asOf?: string): Promise<HomeResponse> {
    if (MOCK) {
      mockState.customer.consent_personalization = consent;
      if (!consent) mockState.feed.cards = mockState.feed.cards.filter((c) => !c.commercial);
      else mockState = structuredClone(mockHome as unknown as HomeResponse);
      return Promise.resolve(withAsOf(asOf));
    }
    return api.consent(consent, asOf);
  },
};
