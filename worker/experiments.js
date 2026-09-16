// A/B experiments. Change the text here, deploy, and results show in /admin.
// To end a test, set every variant's weight to 0 except the winner.
export const EXPERIMENTS = {
  calc_cta: {
    id: "calc_cta",
    description: "Primary button under the calculator result",
    variants: {
      A: { text: "Book my free 15-min walkthrough", weight: 50 },
      B: { text: "Get my free ROI game plan", weight: 50 },
    },
  },
};

export function pickVariant(exp) {
  const entries = Object.entries(exp.variants).filter(([, v]) => v.weight > 0);
  const total = entries.reduce((s, [, v]) => s + v.weight, 0);
  let r = Math.random() * total;
  for (const [k, v] of entries) { if ((r -= v.weight) < 0) return k; }
  return entries[0][0];
}
