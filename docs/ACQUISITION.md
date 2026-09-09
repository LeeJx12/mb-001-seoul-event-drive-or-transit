# MB-001 active acquisition sprint

Run date: 2026-09-09 KST  
Scope: the two existing event pages only  
Cost: KRW0

## Audit and observed baseline

All three product URLs return public HTML and have self-referencing canonicals. `robots.txt` allows crawling and names the sitemap. The sitemap contains only the root and two canonical event URLs. Exact public `site:` searches for the product path did not surface either event page on 2026-09-09, so indexing and search impressions are not established.

The reproducible pre-window measurement baseline remains DDP `acquisition_view=1`, Seoripul `acquisition_view=1`, and all meaningful-use/action counters zero. After subtracting those known operator hits, the observed baseline is:

| Metric | Net baseline |
| --- | ---: |
| event-page acquisition visits | 0 |
| meaningful page uses | 0 |
| result actions | 0 |
| attributed search/owned visits | 0 |

This is `NO DISTRIBUTION EVIDENCE`, not a demand verdict. No authorized search-console impression report is available in this repository or execution environment.

## Exact channels and changes

1. **High-intent search surfaces:** retained exactly two leaf pages and strengthened their distinct jobs: `서울라이트 DDP 2026 주차/교통/동대문역사문화공원역` and `서리풀뮤직페스티벌 2026 교통통제/주차/서초역`. Added truthful Event/Festival JSON-LD, visible official-source sections, Open Graph metadata, and accurate sitemap `lastmod` values. No thin or bulk page was added.
2. **Owned internal discovery:** root-to-event links carry `src=owned-home`; the two event pages now cross-link through the genuinely related drive-or-transit job with `src=owned-related`. Canonicals remain parameter-free. Editing a different portfolio product merely to manufacture inbound traffic was outside the target-repository boundary, so no cross-repository placement was made.
3. **Faster account-free discovery:** after deployment, submit only the three significantly changed canonical URLs through IndexNow using the path-scoped public key file. The official protocol requires an 8–128 character key, a UTF-8 key file on the same host, and a matching `keyLocation`; an HTTP 200 means accepted, not indexed or exposed. Google’s unauthenticated sitemap-ping endpoint is deprecated and must not be used. IndexNow is a crawl-discovery action, not a qualified human-exposure denominator.
4. **Attribution:** recognized search referrer hosts are reduced to four coarse enums (Google, Naver, Bing, Daum); explicit owned links use two fixed enums. Only the enum is written to the existing approved aggregate counter. Full referrers, query strings, identifiers, and user values are never sent. Unknown/direct traffic is not guessed.

## Demand, disconfirming, and value evidence

- Seoul’s official DDP event listing confirms a current 11-day free event, 19:30–22:30, at DDP. A Seoul city budget document reports 1.92 million visits across the 2025 Seoul Light DDP program; this supports event attention, not demand for this product.
- The Seocho official notice showed 236 views when checked and the official event material names a roughly 900 m road closure from 2026-09-19 00:00 through 2026-09-21 04:00. This supports the transportation job but is not an exposure to MB-001.
- Public results contain official pages and several current third-party event guides, including pages answering parking and traffic-control questions. This both confirms the query job and shows strong substitutes. MB-001’s exact product URLs did not appear in the observed `site:` searches.
- Admission is free, which is disconfirming evidence for direct event-content willingness to pay. Observable transportation spending is real: Seoul’s official current fare pages list adult subway base fare KRW1,550 and daytime taxi base fare KRW4,800. These are decision-value proxies, not product revenue.
- The existing display-ad hypothesis remains weak: at the control-plane proxy of KRW2,000–5,000 RPM, 5,000 monthly page views imply only about KRW10,000–25,000 gross monthly revenue. No partner or affiliate opportunity was established in this sprint.

## First 100 measurable qualified exposure opportunities

The target is 100 human opportunities-to-see, not 100 IndexNow notifications or crawler hits.

| Tranche | Intended source | Target | Denominator | Current state |
| --- | --- | ---: | --- | --- |
| A | Google/Naver exact event-title + parking/traffic queries | 60 | Search-console impressions for the two canonical leaf URLs | unavailable |
| B | Bing/participating-engine discovery after IndexNow | 20 | Bing Webmaster URL impressions, not submission count | unavailable |
| C | Contextual owned referral, preferably a separately authorized MB-002 drive-vs-transit placement | 20 | rendering page views for that placement plus `owned_*` attributed visits | not authorized in this repo-only work order |

The first-100 denominator is therefore still missing. IndexNow acceptance proves notification only. The highest-information next experiment is one bounded, reciprocal MB-002 placement with its rendering-page denominator and `src` attribution, or read access to one already-verified search console property. Either would distinguish “not seen” from “seen but not clicked” without paid promotion or manual posting.

## Exposure-aware decision logic

- **NO DISTRIBUTION EVIDENCE:** fewer than 100 measurable qualified human impressions, or no authorized impression denominator. Do not issue a demand verdict; run only the highest-information bounded distribution test.
- **ITERATE DISTRIBUTION:** at least 100 qualified impressions but fewer than 30 attributed visits. Change the channel/snippet once; do not label low traffic as product rejection.
- **ITERATE PRODUCT:** 30–99 qualified event-page visits, or at least five meaningful uses with fewer than eight result actions. Make one bounded title/snippet/internal-link or decision-flow revision.
- **PASS / KEEP:** at least 100 qualified event-page visits, at least 20 meaningful uses, at least eight result actions, and result-action rate at least 5%.
- **STOP EXPANSION:** only after at least 100 qualified event-page visits produce fewer than three result actions, or after strong independent disconfirming evidence. Fewer than 30 passive visits is no longer sufficient.
- **MEASUREMENT BLOCKED:** counters or console data cannot be read reliably. Never infer demand from indexing or notification alone.

No event expansion, paid promotion, monetization, privacy expansion, manual Founder posting, or legacy repository cleanup is authorized by this sprint.

## Sources checked

- Seoul official event listing: https://festival.seoul.go.kr/festival/main/festivalView.do?festacode=451
- Seoul DDP economic/attendance release: https://www.seoul.go.kr/news/news_report.do?nttNo=465102&srchCtgry=464
- Seocho official event notice: https://www.seocho.go.kr/site/seocho/ex/bbs/View.do?bcIdx=410908&cbIdx=57
- Seocho official event page: https://www.seocho.go.kr/html/page_20260826/index.html
- Seoul official transport fares: https://english.seoul.go.kr/policy/transportation/modes-of-transport/
- IndexNow implementation requirements: https://www.bing.com/indexnow/getstarted
- Google sitemap guidance and ping deprecation: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap and https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping
- Google Event structured-data guidance: https://developers.google.com/search/docs/appearance/structured-data/event
