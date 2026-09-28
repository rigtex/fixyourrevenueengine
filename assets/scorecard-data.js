/* Revenue Engine Scorecard data. Loaded on demand AFTER the email gate,
   so the questions and result write-ups are not present in the page HTML. */
window.SCORECARD_DATA = {
  lenses: [
    { name: "Pipeline", items: [
      "Pipeline fills on its own. It doesn't wait for me to post, speak, or call a friend.",
      "I can see where deals stall, and why, in one place."
    ] },
    { name: "Planning", items: [
      "We make real decisions on the forecast because we trust it.",
      "Next year's number is built up from what the engine produces, not handed down and hoped for."
    ] },
    { name: "People", items: [
      "Marketing, sales, and customer success each own their piece of the number. No gaps, no overlaps.",
      "The team closes without me in the deal."
    ] },
    { name: "Performance", items: [
      "Our best accounts keep growing after year one.",
      "When we change something, we can tell whether revenue moved."
    ] }
  ],
  bands: [
    { min: 33, label: "Strong, with one soft spot.", read: "Most of what you rated is strong. Your lowest score is {lens}, and that's the first place I'd look under the hood, before it becomes the reason next quarter misses. Book a call and we'll decide the next step together." },
    { min: 25, label: "Working, with friction.", read: "You rated most of the engine as working, with {lens} lagging the rest. I wouldn't guess why from eight answers; I'd look under the hood. Book a call and we'll decide the next step together." },
    { min: 17, label: "More than one weak spot.", read: "Several parts scored low, with {lens} lowest. That's not a verdict, it's a map: it says where to start looking, and then where to look next. Book a call and we'll decide the next step together." },
    { min: 0, label: "Low scores across the board.", read: "Low scores across the entire revenue engine, {lens} lowest. Eight answers can't say why, and I won't pretend they do. They tell us where to look. Book a call and we'll decide the next step together." }
  ]
};
if (typeof window.__scorecardDataReady === "function") window.__scorecardDataReady();
