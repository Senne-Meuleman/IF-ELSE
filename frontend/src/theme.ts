// density / tone / contrast → CSS variables applied on the phone root.
import type { CSSProperties } from "react";
import type { Theme, Tone } from "./api";

const DENSITY = {
  compact: { font: "15px", space: "10px", radius: "14px", heroPad: "16px" },
  comfortable: { font: "16px", space: "12px", radius: "16px", heroPad: "20px" },
  large: { font: "19px", space: "16px", radius: "18px", heroPad: "24px" },
} as const;

const TONE_ACCENT: Record<Tone, string> = {
  casual: "#7c3aed",
  neutral: "#0d6fb8",
  warm: "#d97706",
  business: "#0f766e",
  formal: "#1e3a8a",
};

export function themeVars(theme: Theme): CSSProperties {
  const d = DENSITY[theme.density];
  const high = theme.contrast === "high";
  const vars: Record<string, string> = {
    "--font-size": d.font,
    "--space": d.space,
    "--radius": d.radius,
    "--hero-pad": d.heroPad,
    "--accent": TONE_ACCENT[theme.tone],
    "--bg": high ? "#ffffff" : "#eef3f8",
    "--card": "#ffffff",
    "--text": high ? "#000000" : "#0f172a",
    "--muted": high ? "#222222" : "#64748b",
    "--border": high ? "#000000" : "#e2e8f0",
    "--border-w": high ? "2px" : "1px",
    "--shadow": high ? "none" : "0 1px 2px rgba(15,23,42,.05), 0 6px 18px rgba(15,23,42,.06)",
    "--primary": high ? "#003d73" : "#0d6fb8",
    "--primary-2": high ? "#00539c" : "#00a3e0",
  };
  return vars as CSSProperties;
}

export function greeting(tone: Tone, firstName: string): string {
  switch (tone) {
    case "casual": return `Hey ${firstName} 👋`;
    case "neutral": return `Hello ${firstName}`;
    case "warm": return `Hi ${firstName}`;
    case "business": return `Good morning, ${firstName}`;
    case "formal": return `Good morning, ${firstName}.`;
  }
}
