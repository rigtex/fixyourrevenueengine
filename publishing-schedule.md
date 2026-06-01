# Multi-Surface Publishing Schedule

Single source of truth for what gets mirrored to Medium and Substack on which dates. The daily approvals-digest reads this file every morning and emails the next due item.

**Cadence rule.** Medium publishes Saturdays. Substack the day after (Sunday). One piece per weekend. The week between pieces is for monitoring traction.

**Lead time.** The daily digest reminds 3 days before the `due` date, not on the day. This gives Jason time to draft, paste, and either publish-immediately on Saturday or use the platform's scheduled-publish feature (Substack supports it free; Medium only on paid Membership). Reminder repeats every morning until status flips to `published`.

**Status values:** `pending` (waiting to publish), `published` (live, includes public_url), `skipped` (decided not to mirror).

**To mark something done after publishing:** edit the line, change `status: pending` to `status: published`, paste the public URL on the `public_url:` field. The next morning's digest will skip it.

---

## Active queue

### 1. The 2026 Founder-Led Report
- canonical: https://fixyourrevenueengine.com/insights/founder-led-report-2026.html
- medium:
  - due: 2026-05-30
  - status: published
  - public_url: https://medium.com/@rigtex.inc/the-2026-founder-led-report-harder-money-better-tools-smaller-teams-bb48039113bf
  - docx: multi-surface-publishing/2-founder-led-report-2026-MEDIUM.docx
- substack:
  - due: 2026-05-31
  - status: pending
  - public_url:
  - docx: multi-surface-publishing/2-founder-led-report-2026-SUBSTACK.docx

### 2. More Fuel in a Broken Engine
- canonical: https://fixyourrevenueengine.com/insights/more-fuel-broken-engine.html
- medium:
  - due: 2026-06-06
  - status: pending
  - public_url:
  - docx: multi-surface-publishing/1-more-fuel-broken-engine-MEDIUM.docx
- substack:
  - due: 2026-06-07
  - status: pending
  - public_url:
  - docx: multi-surface-publishing/1-more-fuel-broken-engine-SUBSTACK.docx

### 3. Fractional CRO vs Marketing Agency
- canonical: https://fixyourrevenueengine.com/revenue-engine-rebuild-vs-marketing-agency.html
- medium:
  - due: 2026-06-13
  - status: pending
  - public_url:
  - docx: multi-surface-publishing/3-fractional-cro-vs-marketing-agency-MEDIUM.docx
- substack:
  - due: 2026-06-14
  - status: pending
  - public_url:
  - docx: multi-surface-publishing/3-fractional-cro-vs-marketing-agency-SUBSTACK.docx

---

## On-deck (not yet scheduled)

Decide after the top 3 are live and traction data is in. Strong candidates from the existing 14 insights posts:

- The 2025 Founder-Led Report Part 1 (foundational context for the 2026 report)
- Is SaaS Dead?
- RevOps Metrics That Matter
- Never Promote Your Top Performers
- Preserving Legacy in Founder-Led Succession
- Fractional CRO vs Full-Time CRO (comparison page)
- Fractional CRO vs VP Sales (comparison page)

To queue any of these: copy a block from the active queue above, swap the canonical and docx paths, pick due dates (Sat + Sun pattern), set status to pending.

---

## Inbound from the rockstarr-content workflow

Pieces in pipeline at the AI content workflow (`/rockstarr-ai/`). The website publishing process should pull these from `/rockstarr-ai/04_approved/content/` and render to `/rigtex-site/insights/` when ready. Mirroring to Medium and Substack uses the cadence rule above (Sat + Sun pattern, 7 day window between pieces).

### Inbound 1. The business that runs without you (TL #6)

- status: outline-approved, drafting next
- outline source: `rockstarr-ai/04_approved/content/2026-05-30_thought-leadership_outline_business-runs-without-you.md`
- expected draft source (after drafting + approval): `rockstarr-ai/04_approved/content/<draft-date>_thought-leadership_business-runs-without-you.md`
- thesis: If the playbook for running the business only exists in your head, no #2 will fix that; the problem isn't who you hired, it's where the playbook lives.
- target canonical URL: https://fixyourrevenueengine.com/insights/business-runs-without-you.html
- target publish: 2026-06-08 (Mon) per the rockstarr-content calendar; Medium + Substack mirror windows would slot into the Sat + Sun pattern that follows (target 2026-06-20 + 2026-06-21 if the cadence rule holds).
- voice notes: zero em-dashes (canonical rule); conversation-first CTA pointing to /contact.html; character is "Marcus" (male, $5M B2B services, paralleling Maya in TL #2).

---

## Reminder format the digest uses

Every morning the digest checks for entries where status=pending and `due <= today + 3 days`. Each match becomes one line in the email. Examples:

> **Substack mirror due in 3 days (Sun Jun 7):** More Fuel in a Broken Engine  
> File: multi-surface-publishing/1-more-fuel-broken-engine-SUBSTACK.docx  
> Canonical: https://fixyourrevenueengine.com/insights/more-fuel-broken-engine.html

> **Medium mirror due TODAY:** Fractional CRO vs Marketing Agency  
> File: multi-surface-publishing/3-fractional-cro-vs-marketing-agency-MEDIUM.docx  
> Canonical: https://fixyourrevenueengine.com/revenue-engine-rebuild-vs-marketing-agency.html

> **OVERDUE since Sat Jun 6:** Medium mirror — More Fuel in a Broken Engine  
> File: multi-surface-publishing/1-more-fuel-broken-engine-MEDIUM.docx  
> Canonical: https://fixyourrevenueengine.com/insights/more-fuel-broken-engine.html

Reminder repeats every morning across the 3-day window AND every day after the due date until status flips to `published`.
