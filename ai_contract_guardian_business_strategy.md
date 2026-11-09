# Strategy & Execution Plan: AI Contract Guardian & Risk Radar (B2B SaaS)

## 0. Triple Purpose of This Project

This project has **three explicit goals**. Every technical phase should advance at least two of them (ideally all three).

| Purpose | What success looks like |
| :--- | :--- |
| **1. Build an AI business** | A paid B2B SaaS (beachhead: UK independent letting agents) that scans AST / tenancy contracts for risk and alerts on renewals. |
| **2. Build in public on LinkedIn** | Cut every build step into small experiments. Document how each change improves (or fails to improve) AI performance. Grow authority + inbound (customers *and* people). |
| **3. Showcase skillset → attract UK employers** | Public proof of applied AI / backend / product judgment that UK hiring managers and tech leads can skim in 60 seconds: evals, RAG, OCR pipelines, cost/latency trade-offs, responsible data use — with GitHub + metrics, not vibes. |

**Rule of thumb:** Prefer work that is (a) product progress, (b) a measurable AI lesson, and (c) a **portfolio signal** UK employers care about (systems thinking, eval discipline, production instincts, communication).

**Target employer signal (examples):** Applied AI Engineer, ML Engineer (LLM/RAG), Backend Engineer (Python), Founding / startup engineer, AI product engineer — especially UK firms in PropTech, LegalTech, fintech, B2B SaaS.

---

## 1. Executive Summary

Initially conceived as a B2C "pay-per-scan" tool for UK tenants, Fermi estimation showed weak LTV, rare usage, and CAC that breaks unit economics.

The pivot: a **B2B Contract Guardian & Risk Radar**. Primary beachhead is **independent letting agents** (AST / tenancy packs), with later expansion to commercial leases and supplier auto-renewals. Parallel track: a public LinkedIn + GitHub build that proves **applied AI performance engineering** to UK employers, while also testing the SaaS.

---

## 2. Fermi Estimation & Business Model Pivot

### 2.1 Why Pure B2C (£8 Pay-Per-Scan Tenant Model) Fails
* **UK Renter Population**: ~24M private renters (~12M tenancy contract renewals/moves per year).
* **1% Penetration Rate**: $12,000,000 \times 1\% = 120,000 \text{ scans/year}$.
* **Revenue**: $120,000 \times £8 = \pounds 960,000 / \text{year}$.
* **The Fatal Flaw**: Extreme **low-frequency usage** (renters move once every 1–3 years). CAC (Google/Meta Ads) easily exceeds £10–£15 per customer → negative unit economics.

### 2.2 The B2B Opportunity (Recurring SaaS)
* **Beachhead ICP**: Independent UK letting agents & rent-to-rent operators (high contract volume, high WTP £49–£99/mo).
* **Broader later**: Micro-SMEs, sole traders, freelancers (£19–£29/mo) once the core AST + renewal radar works.
* **Steady-state ceiling (optimistic Fermi)**: ~4,125 subscribers × £29 ≈ **£1.44M ARR** — a multi-year ceiling, not Year-1 plan.
* **Year-1 realistic Fermi (bootstrapped)**: ~100–250 paying users → roughly **£35k–£90k ARR run-rate** if retention holds via vault + alerts.

### 2.3 Why AST First (Not “All Business Contracts”)
* Agents use tenancy docs weekly → supports subscription.
* One contract family → sharp risk checklist, faster AI eval loops.
* Clear LinkedIn narrative: “UK housing / tenancy AI” beats vague “AI for any contract.”
* Business contracts (commercial leases, supplier auto-renewals) are a **phase-2 niche**, not the v1 scope.

### 2.4 UK Civil / Contract Domains — Where This Model Makes Money（重要對照表）

Money for this product = **who pays repeatedly to catch red flags before a civil dispute**, not which lawsuit has the biggest headline damages.

| # | 領域 | 典型痛 | 買家 | 使用頻率 | 肯俾錢 | AI 紅旗適合度 | 對你嘅賺錢潛力 |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **住宅租約 AST** | 按金、收樓程序、違規收費、通知期 | 獨立租務代理 | **好高** | 高 £49–£99 | 好好（checklist） | **最好起步** |
| **2** | **商業租約** | break clause、維修責任、租務檢討 | SME／業主／經紀 | 中 | **好高**（錯一次幾萬） | 強 | **每個客最賺** |
| **3** | **建築／判頭合約** | 付款、retention、工期罰款 | 判頭、工程公司 | 做工程時高 | 高 | 要專精（如 JCT）先強 | 專精就有肉食 |
| **4** | **僱傭／和解協議** | 競業、不公平條款 | SME／HR | 中 | 中高 | 中（合規風險較高） | 有錢但法律風險大 |
| **5** | **供應商／SaaS 合約** | 自動續約、責任上限、加價 | 微型公司 | 中（到期雷達好用） | 中 £29 | 強 | 量大、客單價低啲 |
| **6** | **特許經營 franchise** | 費用、地區、終止權 | 準加盟主 | **一次過** | 一次高 | 強 | 適合按次收費，唔養得住 SaaS |
| **7** | **股東／投資文件** | 稀釋、拖售權 | Founder | 好少 | 一次高 | 中（最終要律師） | 有面子、冇量 |
| **8** | **租客 B2C** | 同上但租客俾錢 | 個人 | 好少 | 低 | 一般 | **單位經濟最差（舊模型）** |

**Rough ranking for this red-flag SaaS:** AST／代理 → 商業租約 → 建築專精 → 供應商自動續約 → franchise／股東一次過。

**Fermi snapshots**
* AST × agents: 200 × £79/mo ≈ £190k ARR; 1,000 × £79 ≈ £950k ARR.
* Commercial lease: 80 × £149/mo ≈ £143k ARR (fewer buyers, higher ticket).
* Construction niche: 150 × £99/mo ≈ £178k ARR (needs deep domain).
* Franchise pay-per-scan: £149 × 100/mo ≈ £179k/year cash — weak MRR, CAC repeats.

**Sell the fear of the dispute; productise the document that causes it**

| Civil dispute buyers fear | Document we scan |
| :--- | :--- |
| Possession / deposit / disrepair fights | AST + guarantor |
| Catastrophic repairing liability / missed break clause | Commercial lease |
| Non-payment / adjudication | Building subcontract |
| Post-termination non-compete fight | Employment / contractor agreement |
| Locked into bad SaaS for years | Vendor MSA / terms |

### 2.5 UK Indie Agents — Why They Might Pay (And When They Won’t)

**UK agents are not HK-style pure middlemen.** Many manage tenancies, renewals, deposits, and paperwork; errors can trigger landlord blame, redress complaints, PI pressure, and failed possession / deposit penalties.

**Positioning (critical):** do **not** sell “protect tenants from landlords.” Sell: *catch clauses and date issues that blow up possessions, deposit claims, and complaints against the agency / landlord.*

**Template objection (honest):** many agents already use templates and only instruct solicitors for odd deals or disputes — not every tenancy.
* Red-flag scan is **weak** if the pack is locked, solicitor-approved, never edited.
* Red-flag scan is **strong** when staff edit for landlord requests, use outdated versions, or mis-apply templates (HMO / company let / guarantor).
* **Expiry / renewal radar remains valuable even with perfect templates** (ops pain, not legal drafting).

**v1 wedge for indie agents**
1. AST / guarantor red-flag checklist on **edited or uncertain** docs.
2. Portfolio vault + 60/30-day renewal & notice alerts.

**Market note:** HK estate agents as deal middlemen are a poor ICP for this SaaS; if building for HK, sell to document owners (landlords, true managing agents, shop tenants, SMEs) — not high-street introducers. This doc’s beachhead assumes **UK**.

---

## 3. Product Features & Core Value Proposition

v1 is a focused **Tenancy Risk + Renewal Hub** (not a full legal firm in a box):

1. **AI AST / Tenancy Scanner (Risk & Trap Detection)**
   * OCR & parsing of PDFs, Word docs, and scans.
   * Fixed checklist: prohibited fees, deposit red flags, notice/break clauses, repair/access traps, renewal / fixed-term risks, common Housing Act friction points.
2. **Expiry & Renewal Radar (Vault & Monitoring)**
   * Encrypted vault for ASTs, guarantor agreements, renewals.
   * 60-day / 30-day email (WhatsApp later) before end dates / rent reviews.
3. **Case-Law Grounded Explanations (Later)**
   * RAG over public UK judgments / tribunal material to explain *why* a flag matters.
   * Position as risk highlighting + education — not formal legal advice.

---

## 4. Technical Architecture & Data Flywheel

### 4.1 Tech Stack
* **Backend**: Python (FastAPI)
* **Database**: PostgreSQL + `pgvector` (HNSW)
* **PDF / Vision**: `marker-pdf` / AWS Bedrock Vision / EasyOCR
* **RAG**: LangChain / LlamaIndex + custom chunking
* **Hosting**: AWS (S3, ECS / Lambda)

### 4.2 Data Flywheel & Model Improvement
* Public UK civil / housing-related judgments & tribunal precedents (BAILII, Find Case Law) where licensing allows.
* Match clauses → similar “failure” cases via vectors.
* Build eval sets: *[clause → defect → suggested rewrite]* for measuring precision/recall before any fine-tune.
* Optional later: fine-tune SLMs (Qwen / Llama) to cut API cost and deepen moat.

### 4.3 AI Performance Loop (Shared by Product + LinkedIn)
Every model / pipeline change must be scored on a small fixed scorecard:

| Metric | Why it matters |
| :--- | :--- |
| **Risk-flag precision** | Wrong alarms destroy trust |
| **Risk-flag recall** | Missed traps destroy product value |
| **Citation / grounding rate** | % answers tied to clause spans or case snippets |
| **Latency (p50 / p95)** | Agent workflow must feel instant |
| **Cost per scan (£)** | Unit economics for £49–£99 pricing |
| **Hallucination rate** | Legal-adjacent products cannot invent law |

---

## 5. Ideal Target Customer & GTM

| Target Segment | Primary Pain Point | Willingness to Pay | GTM Channel |
| :--- | :--- | :--- | :--- |
| **Independent Letting Agents & Rent-to-Rent (beachhead)** | AST flaws, Housing Act friction, renewals, disputes | **High** (£49–£99/mo) | LinkedIn content + outreach, PropTech forums, direct sales |
| Local trades / contractors | Scope-creep, non-payment | Medium (£19–£29/mo) | Phase 2+ |
| Micro-SME / freelancers | Auto-renewing leases & vendors | Medium–High (£29/mo) | Phase 2+ (commercial lease / supplier niche) |

**LinkedIn is dual-use GTM:** authority content attracts agents *and* AI practitioners; DMs convert the former; followers compound the latter.

---

## 6. Dual-Track Roadmap (Product + LinkedIn)

Each phase ships product work **and** 2–4 LinkedIn posts. Posts follow a fixed template: *problem → experiment → metric before/after → what I’d do next*.

### Phase 1 — Data, Eval Set & Baseline RAG (Weeks 1–3)
**Business**
* Collect / clean public UK housing & contract-related judgments (legal/ToS compliant).
* Chunk + embed into `pgvector`.
* Build a **gold eval set** of 50–100 labelled AST clauses (risk / no-risk / risk type).

**AI performance slices (postable)**
1. Naive chunking vs structure-aware chunking — effect on retrieval hit rate.
2. Embedding model A vs B on legal text — recall@k.
3. Why you need an eval set before “improving the prompt.”
4. Baseline RAG: accuracy vs pure LLM-with-no-docs (hallucination gap).

### Phase 2 — Parsing + Risk Scoring Pipeline (Weeks 4–5)
**Business**
* FastAPI upload → `marker-pdf` / OCR → clause segmentation → risk checklist scoring for AST.

**AI performance slices (postable)**
1. OCR / PDF parse error rate: digital PDF vs scan vs photo.
2. Prompt-only risk detection vs checklist + few-shot — precision/recall.
3. Forcing model to quote clause spans — drop in hallucinated flags.
4. Cost per document: one big LLM call vs router + small model.

### Phase 3 — Vault, Expiry Radar, Notifications (Weeks 6–7)
**Business**
* Store contracts; extract end / renewal dates; cron + email alerts (WhatsApp later).

**AI performance slices (postable)**
1. Date extraction accuracy: regex+rules vs LLM vs hybrid.
2. Confidence thresholds: when to ask the user to confirm a date.
3. Reducing false “renewal in 30 days” alerts (product trust = AI trust).

### Phase 4 — Beta with 10–20 Letting Agents (Week 8+)
**Business**
* Onboard indie agents; price test £49–£99; measure retention & which flags they trust.

**AI performance slices (postable)**
1. Offline eval vs real-agent disagreement — where the model is confidently wrong.
2. Error taxonomy: OCR fail vs retrieval miss vs legal nuance vs prompt drift.
3. What moved the needle most: better data, better eval, better UX, or bigger model.
4. “Build in public” retro: metrics that actually predicted paying-user trust.

### Phase 5+ — Expand Contract Types (Only After Beachhead Works)
* Commercial leases **or** supplier auto-renewal contracts (pick one).
* Optional SLM fine-tune once eval plateau is clear.
* LinkedIn series: transfer learning from AST → new contract family (domain shift story).

---

## 7. LinkedIn Operating System (Customers + UK Employers)

### Content pillars
1. **Building the SaaS** — ICP, Fermi math, pricing, agent interviews (business / product sense).
2. **Improving AI performance** — evals, RAG, OCR, cost/latency (technical depth employers hire for).
3. **Lessons from failure** — experiments that did *not* improve metrics (high trust).
4. **Career-readable portfolio** — each major post links a GitHub artefact (notebook, eval script, architecture diagram, ADR). Soft CTA: open to UK applied-AI / backend roles *or* follow the build.

### What UK employers should “see” in you (map work → signal)

| Skill to show | Do this in the project | Post angle |
| :--- | :--- | :--- |
| Eval discipline | Gold set + precision/recall before prompt tinkering | “I refused to ‘improve’ the model without a scoreboard” |
| RAG systems | pgvector, chunking ablations, citation rate | Before/after retrieval hit rate |
| Production ML sense | Latency p95, cost per scan, failure taxonomy | “Bigger model lost to better parsing” |
| Backend / data | FastAPI upload pipeline, Postgres, job queues | Simple architecture diagram |
| Responsible AI / judgment | Prefer official judgment sources over reckless scraping | “Why I didn’t scrape everything on day 1” |
| Product / domain | AST checklist, agent interviews, Fermi | UK PropTech / LegalTech relevance |
| Communication | Short posts, clear metrics, UK English | Hireable writing |

### Cadence (suggested)
* **2 posts / week** (1 systems/AI-metrics, 1 product/business or career-readable retro).
* Each post = **one experiment** + numbers + link to GitHub when possible.
* Profile: headline aimed at UK search (`Applied AI | RAG/LLM systems | Python` + building Contract Guardian).
* About + featured: 3 pinned posts with metrics; featured GitHub repo.
* CTA mix: waitlist for agents **and** “Building in public — open to UK roles in applied AI / backend.”

### Experiment log (keep in repo or Notion; summarize on LinkedIn)
| Date | Slice | Hypothesis | Metric | Before → After | Ship? | GitHub | Post URL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | | | | | | | |

### Employer-attraction guardrails
* Show **judgment** (evals, ToS-aware data), not only hustle.
* Prefer **reproducible snippets** over screenshot-only flex.
* Don’t overclaim “legal AI that replaces solicitors” — UK employers will distrust it; frame as risk tooling + measurement.
* UK spelling/tone in posts aimed at UK hiring managers.

---

## 8. Near-Term Next Actions
1. Lock beachhead: **UK indie letting agents + AST checklist** (write the 10–15 risk rules).
2. Create **eval set** + **experiment log** + public GitHub repo skeleton (README = portfolio landing).
3. Update LinkedIn headline/About for **UK applied AI / RAG** visibility; pin “build in public” intent.
4. Ship Phase 1 baseline (small legal ingest + eval) and post: *why evals beat vibes for legal-adjacent AI* (employer signal #1).
5. Skip “big scraper service” as the opener; document the responsible-ingest choice as a LinkedIn post.
6. Recruit 5 agent conversations in parallel (product validation) while the GitHub trail builds for employers.
