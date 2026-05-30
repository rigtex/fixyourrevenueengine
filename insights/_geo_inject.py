#!/usr/bin/env python3
"""
GEO Phase 1 injector: TL;DR block + FAQ block + FAQPage JSON-LD + SpeakableSpecification
Bulk injects across all 14 insights posts. Idempotent: skips files that already have <!-- GEO:TLDR --> marker.
"""

import os
import re
from pathlib import Path

POSTS_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# Content: TL;DR + 3 FAQs per post
# Voice rules: no em-dashes; "founder-led or family-owned"; operator voice.
# ---------------------------------------------------------------------------

CONTENT = {
    "more-fuel-broken-engine.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/more-fuel-broken-engine.html",
        "tldr": "When pipeline stalls, most founders default to more spend or more headcount. Both make the problem worse if the engine itself is broken. The real fix is diagnostic before additive: figure out which stage of the revenue system is leaking, then redesign it. Adding fuel to a broken engine just buys more expensive stagnation.",
        "faqs": [
            ("Why does adding sales or marketing spend often fail to fix stalled pipeline?",
             "Because the bottleneck is rarely the top of the funnel. When conversion, hand-offs, or close rates are broken, more inputs just expose the failure faster. Spend amplifies whatever is already happening, including the leak."),
            ("How do you diagnose a broken revenue engine?",
             "Map the system end to end: lead source quality, MQL-to-SQL conversion, sales cycle by stage, win rate by segment, expansion and churn. The leak almost always lives at a specific stage. Find it, fix it, then add fuel."),
            ("What's the difference between a fractional CRO and a marketing or sales agency?",
             "An agency runs a function for you. A fractional CRO rebuilds the system that connects marketing, sales, and customer success. Agencies optimize their lane. A CRO owns the curve."),
        ],
    },
    "founder-led-exit-success.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/founder-led-exit-success.html",
        "tldr": "An exit isn't an event you plan a year out, it's a system you build for years before. Founders who exit well treat the business as transferable from day one: documented processes, repeatable revenue, a leadership team that runs without them, and clean financials.",
        "faqs": [
            ("How early should a founder start planning for exit?",
             "Three to five years before the desired exit. Buyers pay premiums for businesses that don't depend on the founder. That separation takes years to engineer, not months."),
            ("What kills founder-led exit value the most?",
             "Founder dependency. If revenue, key relationships, or product decisions all route through the founder, the multiple drops. Buyers price in the risk of you walking out the door."),
            ("Does a founder-led or family-owned business need a fractional CRO before exit?",
             "If revenue is concentrated in your hands or unpredictable quarter to quarter, yes. A CRO documents the system, builds the team, and produces the kind of repeatable growth that protects valuation in due diligence."),
        ],
    },
    "is-saas-dead.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/is-saas-dead.html",
        "tldr": "SaaS isn't dead. The lazy version of SaaS is dead. Rising CAC, saturated categories, and skeptical buyers have ended the era of growth at any cost. Companies that win now treat revenue as an integrated system, often with a fractional CRO replacing the old VP Sales hire.",
        "faqs": [
            ("Is SaaS still a viable business model?",
             "Yes, but the rules changed. Efficient growth, expansion revenue, and tight CAC payback now matter more than top-line ARR. The model works; the old playbook for running it does not."),
            ("Why are fractional CROs replacing full-time VP Sales hires in SaaS?",
             "Because the problem in most stalled SaaS companies isn't sales execution, it's the full revenue system. A fractional CRO covers marketing, sales, and customer success integration without the $400K+ comp load of a full-time hire."),
            ("What's the biggest mistake SaaS founders make when growth slows?",
             "Hiring more reps. If close rate, expansion, and onboarding are broken, more reps just compound the cost of the leak. Fix the system first."),
        ],
    },
    "revops-metrics-that-matter.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/revops-metrics-that-matter.html",
        "tldr": "Most revenue dashboards measure activity, not health. The metrics that actually predict whether the engine is working are pipeline coverage, stage conversion rates, sales cycle length, CAC payback, net revenue retention, and forecast accuracy. Everything else is noise.",
        "faqs": [
            ("What are the most important RevOps metrics for a CRO?",
             "Pipeline coverage (3x to 4x of quota by stage), stage-to-stage conversion, sales cycle by segment, CAC payback in months, net revenue retention, and forecast accuracy. These six tell you if the engine is healthy."),
            ("How often should a CEO review revenue metrics?",
             "Weekly for pipeline and forecast. Monthly for conversion, cycle, and CAC. Quarterly for retention and segment performance. Daily metrics usually create noise, not signal."),
            ("What's a healthy CAC payback period?",
             "Under 12 months for SMB, 18 to 24 months for mid-market, up to 36 months for enterprise. Longer than that and growth starts consuming the cash it produces."),
        ],
    },
    "revenue-team-alignment.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/revenue-team-alignment.html",
        "tldr": "Sales, marketing, and customer success fight when their incentives, definitions, and hand-offs are unaligned. Real alignment is structural, not cultural. Shared revenue targets, one definition of a qualified lead, documented hand-off SLAs, and a single source of truth in the CRM.",
        "faqs": [
            ("Why do sales and marketing always fight?",
             "Because they're measured on different things. Marketing on lead volume, sales on closed revenue. Until both teams share a revenue number, the friction is built into the org chart."),
            ("How do you align sales, marketing, and customer success?",
             "Three structural moves. One shared revenue target. One definition of a qualified opportunity. One hand-off process with SLAs and accountability. Skip these and culture-building won't save you."),
            ("Should customer success report to the CRO?",
             "Yes, in any business where expansion and retention drive a meaningful share of revenue. CS reporting to product or operations creates a structural disconnect between acquiring and keeping customers."),
        ],
    },
    "preserving-legacy-succession.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/preserving-legacy-succession.html",
        "tldr": "Most family-owned and founder-led businesses fail succession not because of family dynamics but because of undocumented operations. Successors can't run what isn't written down. Documenting processes, decisions, and relationships is the foundation of a transition that holds.",
        "faqs": [
            ("What's the biggest reason family business succession fails?",
             "Process knowledge that lives only in the founder's head. When daily operations depend on undocumented judgment, successors are set up to fail before they start."),
            ("How do you document a business for succession?",
             "Process maps for every revenue-producing workflow. Decision criteria for the choices the founder currently makes by instinct. Relationship maps for key customers and partners. Financial playbooks for pricing and discounting."),
            ("How long does succession preparation take in a founder-led or family-owned business?",
             "Two to four years for documentation, team building, and live hand-offs. Less than that and the successor is operating on hope."),
        ],
    },
    "never-promote-top-performers.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/never-promote-top-performers.html",
        "tldr": "Promoting your best salesperson to manager usually breaks two things at once: you lose the rep's production and you create a manager who can't manage. Selling and managing are different jobs. Promote for management ability, not for sales numbers.",
        "faqs": [
            ("Should you promote your top salesperson to sales manager?",
             "Only if they show genuine coaching and leadership ability. The skills that make someone a great individual contributor (drive, close rate, personal pipeline discipline) are not the skills of a manager."),
            ("What makes a good sales manager?",
             "Coaching ability, deal strategy thinking, comfort with metrics and forecasting, and the patience to let reps win or lose their own deals. These are different muscles than personal selling."),
            ("How do you reward top performers without promoting them into management?",
             "Senior IC tracks, principal seller titles, account ownership over the most strategic logos, and comp structures that pay senior reps more than first-line managers. Build a path that doesn't require leaving what they're great at."),
        ],
    },
    "founder-led-report-part-1.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/founder-led-report-part-1.html",
        "tldr": "The market founder-led businesses were built for has changed. Capital is more expensive, buyers are more skeptical, and the playbook that produced the first $5M to $15M no longer scales. 2025 demands a new chapter built on systems, not heroics.",
        "faqs": [
            ("Why is 2025 different for founder-led or family-owned businesses?",
             "Capital costs are higher, sales cycles are longer, and buyers expect more proof. The growth tactics that worked in low-rate, high-trust markets no longer return the same results."),
            ("Why won't what got founder-led businesses to $5M get them to $15M?",
             "The first phase rewards founder hustle and personal relationships. The next phase rewards systems, repeatability, and a team that can produce growth without the founder in every meeting."),
            ("What's the first move for a founder facing a stalled engine?",
             "Diagnose before you spend. Map where the leak actually lives in the revenue system. Most stalls aren't a sales problem; they're a system problem."),
        ],
    },
    "founder-led-report-part-2.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/founder-led-report-part-2.html",
        "tldr": "Founder's Syndrome is the moment when the same traits that built the business start to throttle it. Tight control, instinct over process, and resistance to outside expertise are assets at $2M and liabilities at $10M. Recognizing the transition is the first step.",
        "faqs": [
            ("What is Founder's Syndrome?",
             "A pattern where the founder's grip on every decision, hire, and relationship stops scaling with the business. It's not a character flaw; it's a stage-of-growth problem that shows up in nearly every founder-led company."),
            ("How do you know if you have Founder's Syndrome?",
             "Decisions stall when you're unavailable. Senior people defer instead of deciding. Pipeline depends on your personal involvement. Team members say 'let's check with the founder' more often than they decide."),
            ("How does a founder move past Founder's Syndrome?",
             "Document decisions, build a leadership team you actually trust, and accept that some judgment calls will be made differently than you'd make them. The point isn't perfection; it's repeatability."),
        ],
    },
    "founder-led-report-part-3.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/founder-led-report-part-3.html",
        "tldr": "Strategic planning in a founder-led or family-owned business isn't a slide deck. It's a quarterly system for choosing what to do, what to stop doing, and what to measure. Without that rhythm, growth gets reactive and the business runs on the loudest voice in the room.",
        "faqs": [
            ("How is strategic planning different for founder-led or family-owned businesses?",
             "It has to be tight, recurring, and decision-oriented. Big annual offsites don't survive the first market shift. Quarterly cycles with clear owners and measurable outcomes do."),
            ("What should a founder-led strategic plan actually contain?",
             "A short list of priorities (three to five), the metrics that prove progress, the owners for each, the explicit list of things you're not doing, and a quarterly review cadence."),
            ("How often should a founder revisit the plan?",
             "Quarterly for the plan itself, monthly for progress, weekly for metrics. Less frequent than that and you're flying blind in a fast market."),
        ],
    },
    "founder-led-report-part-4.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/founder-led-report-part-4.html",
        "tldr": "Agile growth in a founder-led or family-owned business means short feedback loops, willingness to kill what isn't working, and a small set of bets you can actually run. The trap is mistaking activity for agility. Real agility is structural: how fast you can decide, deploy, and learn.",
        "faqs": [
            ("What does agile growth look like in a small B2B business?",
             "30 to 90 day experiments, each with a clear hypothesis, a measurable outcome, and an explicit kill criterion. If you can't say what would make you stop, you're not running an experiment."),
            ("How many growth bets should a founder-led business run at once?",
             "Three or four max. More than that and nothing gets the attention it needs to produce a clear answer. Focus beats breadth in small companies."),
            ("What's the most common agility mistake founders make?",
             "Confusing busyness with progress. Running ten initiatives at half-effort feels productive and produces nothing measurable. Pick fewer, fund them properly, and read the results."),
        ],
    },
    "founder-led-report-part-5.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/founder-led-report-part-5.html",
        "tldr": "Succession planning is a multi-year build, not a transaction. The founder who exits well starts three to five years out: documenting operations, growing the leadership bench, and stress-testing the business by stepping away in increasing increments before the formal hand-off.",
        "faqs": [
            ("When should a founder start succession planning?",
             "Three to five years before the intended transition. Less than that and you're choosing between a forced exit and a discounted one."),
            ("What's the hardest part of founder succession?",
             "Letting decisions get made differently than you'd make them. The point of succession is to leave a working business, not a perfectly preserved version of your own judgment."),
            ("How does a fractional CRO support founder succession?",
             "By building the revenue system that produces growth without depending on the founder, documenting the playbook, and growing the leadership team that will run it after the transition."),
        ],
    },
    "founder-led-report-part-6.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/founder-led-report-part-6.html",
        "tldr": "When family or founder-led businesses don't have clean role definitions, growth stalls and trust erodes. The fix is structural, not interpersonal. Written role charters, clear decision rights, and explicit escalation paths cut the friction that no amount of family loyalty can.",
        "faqs": [
            ("Why do role conflicts hurt family-owned businesses more than other companies?",
             "Because the conflict follows you home. Unclear decision rights at work become tense family dinners. The cost compounds across both relationships and revenue."),
            ("How do you create role clarity in a family-owned business?",
             "Written role charters covering responsibilities, decision rights, and escalation. A clear org chart that family members are held to like anyone else. Performance reviews that apply equally to family and non-family staff."),
            ("Who should resolve role conflicts in a family-owned business?",
             "A defined leadership process, not the head of the family. The moment role conflicts get resolved at the dinner table, the org chart loses meaning and non-family staff disengage."),
        ],
    },
    "founder-led-report-part-7.html": {
        "page_url": "https://fixyourrevenueengine.com/insights/founder-led-report-part-7.html",
        "tldr": "Future-proofing a founder-led or family-owned business isn't about predicting the market. It's about building systems that absorb shocks: documented operations, a leadership bench that can decide without the founder, diversified revenue, and a culture that adapts faster than the next disruption.",
        "faqs": [
            ("How do you future-proof a founder-led or family-owned business?",
             "Build four resilience layers. Documented operations the team can run. A leadership bench with real decision rights. Revenue diversified across customers, channels, and geographies. Financial reserves to survive a bad quarter."),
            ("What's the biggest threat to founder-led businesses over the next five years?",
             "Concentration risk: one or two customers, one channel, one geography, one founder. Whatever the market does, concentration amplifies the damage."),
            ("What separates founder-led businesses that endure from those that don't?",
             "Systems. The ones that endure build repeatable processes early, grow a team that can operate without the founder, and treat the business as a transferable asset from day one."),
        ],
    },
}


def build_tldr_block(tldr_text):
    return (
        '<!-- GEO:TLDR -->\n'
        '<div class="tldr" data-speakable="tldr">\n'
        '  <div class="tldr-label">TL;DR</div>\n'
        f'  <p>{tldr_text}</p>\n'
        '</div>\n'
    )


def build_faq_block(faqs):
    items = '\n'.join(
        f'  <div class="faq-item">\n'
        f'    <div class="faq-q">{q}</div>\n'
        f'    <div class="faq-a">{a}</div>\n'
        f'  </div>'
        for q, a in faqs
    )
    return (
        '<!-- GEO:FAQ -->\n'
        '<section class="post-faq" aria-labelledby="post-faq-h" data-speakable="faq">\n'
        '  <h2 id="post-faq-h">Frequently asked</h2>\n'
        f'{items}\n'
        '</section>\n'
    )


def build_faqpage_schema(page_url, faqs):
    import json
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "url": page_url,
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }
    return (
        '<!-- GEO:FAQPAGE-SCHEMA -->\n'
        '<script type="application/ld+json">\n'
        + json.dumps(schema, indent=2)
        + '\n</script>\n'
    )


def build_speakable_schema(page_url):
    import json
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": page_url,
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".tldr p", ".lede-quote", ".post-faq .faq-q", ".post-faq .faq-a"],
        },
    }
    return (
        '<!-- GEO:SPEAKABLE-SCHEMA -->\n'
        '<script type="application/ld+json">\n'
        + json.dumps(schema, indent=2)
        + '\n</script>\n'
    )


def inject_file(filename, meta):
    path = POSTS_DIR / filename
    html = path.read_text(encoding='utf-8')

    if '<!-- GEO:TLDR -->' in html:
        return f"SKIP (already injected): {filename}"

    tldr_block = build_tldr_block(meta['tldr'])
    faq_block = build_faq_block(meta['faqs'])
    faq_schema = build_faqpage_schema(meta['page_url'], meta['faqs'])
    speakable_schema = build_speakable_schema(meta['page_url'])

    # 1. Insert TL;DR right after `<div class="post-article">` opening
    article_open_re = re.compile(r'(<div class="post-article">\s*\n)')
    if not article_open_re.search(html):
        return f"FAIL (no post-article): {filename}"
    html = article_open_re.sub(r'\1\n' + tldr_block + '\n', html, count=1)

    # 2. Insert FAQ section right before `<div class="post-cta">` opening
    cta_open_re = re.compile(r'(\s*)(<div class="post-cta">)')
    if not cta_open_re.search(html):
        return f"FAIL (no post-cta): {filename}"
    html = cta_open_re.sub(r'\n' + faq_block + r'\n\1\2', html, count=1)

    # 3. Insert JSON-LD schema blocks right before </head>
    head_close_re = re.compile(r'(\s*</head>)')
    if not head_close_re.search(html):
        return f"FAIL (no </head>): {filename}"
    html = head_close_re.sub('\n' + faq_schema + '\n' + speakable_schema + r'\1', html, count=1)

    path.write_text(html, encoding='utf-8')
    return f"OK: {filename}"


if __name__ == '__main__':
    for filename, meta in CONTENT.items():
        print(inject_file(filename, meta))
