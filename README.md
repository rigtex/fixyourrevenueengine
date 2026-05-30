# Revved for Growth

Static, SEO + LLM-friendly marketing site for **Revved for Growth**, embedded revenue engine transformation for founder-led or family-owned B2B firms.

## File structure

```
rigtex-site/
├── index.html # Home (hero, insights teaser, ICP, three ways to work, proof, differentiation, CTA)
├── insights.html # Blog index, Coming Soon, Featured Series, Notes from the Field
├── contact.html # Contact page with embedded Cal.com booking calendar
├── 404.html # Not Found
├── styles.css # Shared styles (Italiana + Helvetica, brand palette)
├── sitemap.xml # Lists home + all 12 insight posts + contact + llms.txt files
├── robots.txt # Allows traditional + AI crawlers
├── llms.txt # Concise LLM-friendly summary
├── llms-full.txt # Full content snapshot for LLM ingestion (includes summaries of all 12 posts)
└── insights/ # 12 mirrored long-form posts
 ├── _generate.py # Generator script, run this if you edit a post body
 ├── never-promote-top-performers.html
 ├── preserving-legacy-succession.html
 ├── revenue-team-alignment.html
 ├── revops-metrics-that-matter.html
 ├── is-saas-dead.html
 ├── founder-led-report-part-1.html
 ├── founder-led-report-part-2.html
 ├── founder-led-report-part-3.html
 ├── founder-led-report-part-4.html
 ├── founder-led-report-part-5.html
 ├── founder-led-report-part-6.html
 └── founder-led-report-part-7.html
```

## Deplo