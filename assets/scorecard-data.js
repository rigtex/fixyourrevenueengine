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
    { min: 33, label: "The engine is producing.", read: "Most of it works. The one or two statements you rated low are where the next stall usually starts. If you want a second set of eyes on that spot, grab a working call." },
    { min: 25, label: "Friction, not failure.", read: "The engine runs, but revenue costs more effort than it should. A hand-off or two is quietly dragging on the number. Find them before you hire or spend against them." },
    { min: 17, label: "Real gaps.", read: "Several parts aren't producing reliably, and you're probably still the thread holding deals together. Fixable, but not with another tactic or another hire. It needs someone inside the engine." },
    { min: 0, label: "It's the engine, not the people.", read: "Your answers say the system is the constraint, not effort or talent. New people, tactics, and tools won't move the line until the engine is rebuilt. That's the work I do." }
  ]
};
if (typeof window.__scorecardDataReady === "function") window.__scorecardDataReady();
