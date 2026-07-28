# Genesis Capability Benchmark 01 - AI Product Creation

**Execution Date:** 2026-07-28
**Executing Agents:** CEO, CTO, Product Manager, Market Research, Architect, Coding, QA, Marketing, Sales
**Required Skills:** market-analysis, business-analysis, product-validation, software-engineering, architecture, testing, marketing, sales

---

## Phase 1: Market Intelligence

*Executed by: Market Research Agent, CEO Agent*

**Constraints:** < 5€ budget, 1 person, scalable, highly automated, online sales, faceless.

### Top 10 High-Value Opportunities

1. **AutoSEO: AI Programmatic SEO for Shopify**
   - *Problem:* E-commerce owners lack time for SEO content.
   - *Customer:* Small Shopify store owners.
   - *Current Alternatives:* Expensive SEO agencies, manual ChatGPT usage.
   - *Why AI Helps:* Generates hyper-specific, localized product-led articles at scale.
   - *Difficulty:* Medium
   - *Monetization:* $29/mo SaaS.
   - *Competition:* Medium.

2. **ReviewAgent: Automated Local Business Review Responder**
   - *Problem:* Google My Business reviews go unanswered, hurting local ranking.
   - *Customer:* Plumbers, electricians, local restaurants.
   - *Current Alternatives:* Ignoring reviews, manual generic replies.
   - *Why AI Helps:* Contextually understands the review and writes personalized, professional replies.
   - *Difficulty:* Low (Simple webhook/API wrapper).
   - *Monetization:* $15/mo SaaS.
   - *Competition:* Low.

3. **Receipt2JSON: AI Expense Parser Micro-SaaS**
   - *Problem:* Developers building accounting apps struggle to parse messy receipts.
   - *Customer:* Indie hackers and SMB dev teams.
   - *Current Alternatives:* AWS Textract (complex), manual OCR regex.
   - *Why AI Helps:* Multimodal LLMs extract entities perfectly without regex.
   - *Difficulty:* Low.
   - *Monetization:* API usage ($0.01 per scan).
   - *Competition:* High.

4. **Meeting2Ticket: Linear/Jira Ticket Generator**
   - *Problem:* PMs waste hours turning transcripts into actionable tickets.
   - *Customer:* Remote tech teams, product managers.
   - *Current Alternatives:* Otter.ai (only summarizes), manual copy-paste.
   - *Why AI Helps:* Formats directly into epics, stories, and tasks.
   - *Difficulty:* Medium.
   - *Monetization:* $39/mo team plan.
   - *Competition:* Medium.

5. **CoverLetter API: Mass Application Tailor**
   - *Problem:* Job seekers need custom cover letters for 100s of jobs.
   - *Customer:* Job seekers, bootcamp grads.
   - *Current Alternatives:* Manual writing.
   - *Why AI Helps:* Matches resume JSON to job description text.
   - *Difficulty:* Low.
   - *Monetization:* Pay-per-generation (credits).
   - *Competition:* High.

6. **Faceless Shorts Automation Generator**
   - *Problem:* Creating Reddit/Trivia shorts is tedious.
   - *Customer:* Faceless YouTube channel owners.
   - *Current Alternatives:* CapCut templates, manual editing.
   - *Why AI Helps:* Scripts, TTS, and video assembly can be fully automated.
   - *Difficulty:* High.
   - *Monetization:* $49/mo SaaS.
   - *Competition:* High.

7. **B2B Cold Email Personalizer**
   - *Problem:* Cold outreach is generic and ignored.
   - *Customer:* B2B Sales reps, agencies.
   - *Current Alternatives:* Lemlist (expensive).
   - *Why AI Helps:* Scrapes LinkedIn and writes highly personalized first lines.
   - *Difficulty:* Medium.
   - *Monetization:* $99/mo SaaS.
   - *Competition:* High.

8. **AI RFP Responder (Request for Proposal)**
   - *Problem:* Agencies spend 20+ hours writing RFPs.
   - *Customer:* B2B Agencies, Consultancies.
   - *Current Alternatives:* Manual writing, basic templates.
   - *Why AI Helps:* Vector search over past RFPs + generative completion.
   - *Difficulty:* High.
   - *Monetization:* $199/mo B2B.
   - *Competition:* Low/Medium.

9. **Newsletter Aggregator & Synthesizer**
   - *Problem:* Tech professionals subscribe to too many newsletters and read none.
   - *Customer:* Devs, founders, VCs.
   - *Current Alternatives:* Unroll.me, manual reading.
   - *Why AI Helps:* Reads all emails and sends one concise weekly audio/text digest.
   - *Difficulty:* Medium.
   - *Monetization:* $5/mo premium.
   - *Competition:* Low.

10. **DataCleanse API: Messy CSV to SQL Migrator**
    - *Problem:* Data scientists spend 80% of time cleaning data.
    - *Customer:* Data analysts, BI devs.
    - *Current Alternatives:* Pandas, Trifacta.
    - *Why AI Helps:* Predicts column types, formats dates, fixes typos automatically.
    - *Difficulty:* High.
    - *Monetization:* Usage-based API.
    - *Competition:* Low.

---

## Phase 2: Select Best Opportunity

*Executed by: CEO Agent, CTO Agent, Product Manager Agent*

**Opportunity Scoring:**
| Opportunity | Demand | Competition (Inv) | Difficulty (Inv) | Revenue | Automation | Total |
|---|---|---|---|---|---|---|
| AutoSEO | 8 | 5 | 6 | 8 | 9 | 36 |
| **ReviewAgent** | **9** | **8** | **9** | **7** | **10** | **43** |
| Receipt2JSON | 6 | 3 | 8 | 5 | 10 | 32 |
| Meeting2Ticket | 8 | 6 | 7 | 8 | 8 | 37 |

**Selection:** **ReviewAgent (Automated Local Business Review Responder)**
*Why:* It hits all constraints perfectly. Local business owners lack the time and technical skill to reply to Google reviews. It requires zero human face to market (B2B SaaS). The implementation difficulty is very low (basic webhooks and LLM API calls). Automation potential is 100% post-setup. A single developer can maintain it.

---

## Phase 3: Product Definition

*Executed by: Product Manager Agent*

- **Product Name:** ReviewPilot AI
- **Mission:** Put local business reputation management on autopilot.
- **Target Customer:** Local service businesses (Plumbers, Electricians, Dentists, Salons).
- **Core Problem:** Unanswered reviews hurt Google rankings and deter customers; business owners don't have time to write polite, context-aware replies.
- **Solution:** A set-and-forget tool that connects to Google My Business and auto-replies to reviews based on a pre-defined brand voice.
- **Unique Advantage:** Dead-simple UX. "One click connect". No prompt engineering required from the user.
- **Pricing Model:** Flat rate $15/month for unlimited reviews on 1 location.
- **Customer Acquisition Strategy:** Cold email outreach to businesses with unclaimed or poorly managed Google Maps listings; highly targeted programmatic SEO ("How to reply to a negative review for a dental practice").

---

## Phase 4: Technical Architecture

*Executed by: CTO Agent, Architect Agent*

**Budget Constraints:** Must cost < 5€ to launch.

- **Frontend:** Next.js (App Router), TailwindCSS, Shadcn UI.
  *Cost:* $0 (Hosted on Vercel Free Tier).
- **Backend/API:** Next.js Server Actions + Google Business Profile APIs.
  *Cost:* $0 (Vercel Edge functions).
- **Database:** Supabase (PostgreSQL + Auth).
  *Cost:* $0 (Free Tier).
- **AI Models:** Anthropic Claude 3.5 Haiku. Fast, extremely cheap, excellent at short-form professional text generation.
  *Cost:* Pay-as-you-go (~$0.25 per 1,000 reviews).
- **Payments:** Stripe Payment Links (No upfront cost).
- **Automation/Queues:** Upstash (Serverless Redis/QStash) for processing webhooks reliably.
  *Cost:* $0 (Free Tier).
- **Deployment:** Vercel.

*Total Initial Architecture Cost:* **$0.00**

---

## Phase 5: MVP Development Plan

*Executed by: Architect Agent, Coding Agent, QA Agent*

**Repository Structure:**
```
/review-pilot
  /app (Next.js frontend & backend)
  /components (UI components)
  /lib
    /google (OAuth and API client)
    /ai (Anthropic Claude integration)
    /db (Supabase client)
  /tests
```

**Development Phases:**

1. **Phase 1: Prototyping (Day 1-2)**
   - *Tasks:* Setup Supabase Auth, connect Google OAuth, build the basic dashboard UI.
   - *Agents:* Architect, Coding.
   - *Output:* Working login and connected accounts view.

2. **Phase 2: Core Engine MVP (Day 3-4)**
   - *Tasks:* Write the prompt pipeline for Claude 3.5 Haiku. Setup Google Business webhooks. Implement auto-reply logic.
   - *Agents:* Coding, Prompt Engineering Skill.
   - *Output:* End-to-end flow: Review comes in -> AI generates reply -> Reply posted to Google.

3. **Phase 3: Testing & Hardening (Day 5)**
   - *Tasks:* Write integration tests for the AI safety guardrails (e.g., handling toxic reviews gracefully). Test Stripe webhooks.
   - *Agents:* QA Agent.
   - *Output:* Production-ready, secure application.

4. **Phase 4: Launch Prep (Day 6)**
   - *Tasks:* Deploy to Vercel. Set up domain. Connect Stripe live mode.
   - *Agents:* DevOps Skill, Coding.
   - *Output:* Live accessible SaaS.

---

## Phase 6: Business Launch

*Executed by: Marketing Agent, Sales Agent*

- **Landing Page Concept:** High-contrast, clean design. Headline: "Don't let bad reviews ruin your business. Auto-reply to customers in seconds." Hero section features a side-by-side comparison of a 1-star review getting a calm, professional AI response instantly.
- **Marketing Strategy:**
  - Scraping Google Maps for businesses with rating < 4.0 or unanswered reviews.
  - Using an automation tool (e.g., Apollo or Instantly) to send a cold email showing a screenshot of *their* unanswered review, and what ReviewPilot would have said.
- **SEO Strategy:** Programmatic generation of 1,000+ landing pages: "Auto-reply to reviews for [City] [Niche]" (e.g., Auto-reply to reviews for Miami Plumbers).
- **Content Strategy:** Blog posts on local SEO strategies, how Google Maps ranking works, and reputation management.
- **Automation Opportunities:** The entire lead generation pipeline (scraping maps -> finding email -> generating custom pitch -> sending) can be fully automated using Genesis scripts post-launch.
