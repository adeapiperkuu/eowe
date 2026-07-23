# **EOWE Workspace** 

KI-based All-in-One Workspace — Mini-ERP & E-Commerce 

_Technical Requirements, Sprint Plan & Developer Task Split_ 

**Document type:** Technical requirements & delivery plan (v1.0) **Prepared for:** Development team — Adea Piperku & Lum Meta **Owner:** Arbios Kastrati (Project Lead) **Client:** EOWE **Date:** 16 July 2026 **MVP window:** 20 July 2026 – 9 October 2026 (6 × 2-week sprints) **Kick-off:** Monday, 20 July 2026 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 1 of 18 

## **Contents** 

|**Contents**............................................................................................................................................................... 1|
|---|
|**1. Project Overview**..............................................................................................................................................1|
|**1.1 Objectves**...................................................................................................................................................1|
|**1.2 Delivery Approach**......................................................................................................................................1|
|**1.3 Technology Stack**....................................................................................................................................... 1|
|**2. Team & Responsibilites**...................................................................................................................................1|
|**3. Architecture & Cross-Cutng Requirements**...................................................................................................1|
|**3.1 Non-Functonal Requirements**...................................................................................................................1|
|**3.2 AI / Human-in-the-Loop Principle**..............................................................................................................1|
|**4. Sprint Timeline (MVP)**......................................................................................................................................1|
|**4.1 Sprint-by-Sprint Breakdown**......................................................................................................................1|
|**5. Detailed Technical Requirements by Module**.................................................................................................1|
|**Foundaton & Platorm (Sprint 1)**....................................................................................................................1|
|**Module 1 — Event & Partcipant Management**..............................................................................................1|
|**Module 2 — Contracts & Finance**.................................................................................................................... 1|
|**Module 4 — Marketng & Social Media**..........................................................................................................1|
|**Module 5 — Partner, Sponsoring & Service-Provider CRM**............................................................................1|
|**Module 3 — E-Commerce, Logistcs & Administraton**...................................................................................1|
|**Module 6 — Future Expansion (post-MVP)**.....................................................................................................1|
|**6. Getng Started — Monday 20 July**..................................................................................................................1|
|**6.1 Open Points to Confrm with EOWE**..........................................................................................................1|



EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 2 of 18 

## **1. Project Overview** 

EOWE manages a growing number of open-water swimming events, participants and partners on manual processes and basic SharePoint storage. This project delivers a tailored, AI-assisted “Mini-ERP” plus an integrated e-commerce shop that digitises and automates all event-dependent and event-independent business cases in one platform — a single source of truth. 

### **1.1 Objectives** 

- Replace redundant Excel lists and scattered file storage with one central, always-current database (single source of truth). 

- Reduce recurring manual work for management (GF/Markus) through AI: payment matching, email drafting, size aggregation. 

- Integrate proven external tools (Tiger Timing, RaceResult, Qonto, DATEV) bidirectionally instead of replacing them (API-first). 

- Ship a usable MVP in ~2–3 months, then extend iteratively without re-architecting. 

### **1.2 Delivery Approach** 

**Method:** Agile, 2-week sprints. Each sprint ends with a short review (1–2 h) with GF/Markus (human-in-theloop sign-off). Change requests are scheduled into the next sprint. 

**MVP module order (agreed):** M1 → M2 → M4 → M5 → M3 → M6 (post-MVP). Module 1 (Event & Participant Management) is the operational core and is built first. 

### **1.3 Technology Stack** 

|**Layer**|**Technology**|**Notes**|
|---|---|---|
|**Frontend**|React + TypeScript, React Query, React Hook<br>Form + Zod|SPA app shell, reusable component library / design<br>system.|
|**Backend**|NestJS (Node.js) + TypeScript, REST API|Modular services mirroring the ERP modules.|
|**Database**|PostgreSQL|Single relatonal store; migratons via<br>Prisma/TypeORM.|
|**Auth**|JWT + refresh tokens, RBAC|Roles: Admin, Management (GF), Staf, Read-only.|
|**Storage**|S3-compatble object storage (+ SharePoint sync<br>hook)|Course maps, contracts, photos, assets.|
|**AI / ML**|NLP (email parsing/drafing), matching<br>algorithms, computer vision|Human-in-the-loop for all customer-facing output.|
|**Integratons**|Tiger Timing, RaceResult, Qonto, DATEV,<br>Stripe/PSP|API-frst, bidirectonal where supported.|
|**DevOps**|Docker, CI/CD, staging + producton, monitoring|Auto-deploy to staging on merge to main.|



## **2. Team & Responsibilities** 

The project is delivered by a two-person full-stack team. Ownership is split so each module has a clear primary developer, while the foundation, hardening and go-live are shared. Both developers review each other’s pull requests. 

|**Developer**|**Focus**|**Primary responsibilites**|
|---|---|---|
|**Adea Piperku**|Frontend / Full-stack lead|React app shell & design system, dashboards, e-commerce shop|



EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 3 of 18 

|**Developer**|**Focus**|**Primary responsibilites**|
|---|---|---|
|||frontend, human-in-the-loop & reconciliaton UIs, contracts UI, alert<br>UI, size aggregaton.|
|**Lum Meta**|Backend / Integratons lead|NestJS APIs & data model, Tiger Timing / RaceResult / Qonto / DATEV<br>integratons, AI email intake & payment matching, computer-vision<br>photo tagging, inventory & stock engine.|
|**Adea + Lum**|Shared|Repo & CI/CD, auth/RBAC, notfcaton service, MVP hardening, go-live<br>& handover, cross-cutng pairing.|



_Capacity assumption: a 2-week sprint provides roughly 8–9 ideal engineering days per developer. Estimates below are ideal days; the sprint plan in section 4 keeps each developer within this envelope._ 

## **3. Architecture & Cross-Cutting Requirements** 

The system is modular: each module is an independently deployable feature area on a shared platform (auth, data model, storage, notifications). This enables iterative releases so the team can work with the system early. 

### **3.1 Non-Functional Requirements** 

- Security: RBAC on every endpoint; passwords hashed (argon2/bcrypt); secrets in a vault; audit log on core entities; GDPR-compliant handling of participant data. 

- Reliability: external integrations use retry + exponential backoff; failures are logged and surfaced, never silently dropped. 

- Performance: list/dashboard views respond < 1.5 s for typical data volumes; long jobs (imports, CV tagging) run async. 

- Maintainability: shared lint/format config, typed end-to-end, module boundaries enforced, unit tests on business logic. 

- Observability: centralized logging + error monitoring (e.g. Sentry); health checks on all services. 

- Data integrity: soft-delete + audit trail; migrations reversible; nightly backups in production. 

### **3.2 AI / Human-in-the-Loop Principle** 

All AI output that reaches a customer (email replies, size recommendations) or the books (payment matches) is proposed by the system and approved by a human before it takes effect. The AI accelerates; the person decides. Low-confidence results are always routed for manual review. 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 4 of 18 

## **4. Sprint Timeline (MVP)** 

Six two-week sprints from 20 July to 9 October 2026. M6 (subscriptions, AI course simulation) is prepared in the data model but scheduled after MVP. 

|**Sprint**|**Dates**|**Theme / Goal**|**Adea d**|**Lum d**|
|---|---|---|---|---|
|**S1**|20 Jul – 31 Jul|Foundaton & Platorm<br>Repo, CI/CD, DB, Auth/RBAC, app shell, design system, core<br>data model. Everything M1+ builds on.|4.8|7.3|
|**S2**|3 Aug – 14 Aug|M1 Core – Events & Partcipants<br>Event/Series/Race CRUD, partcipant registry, document store,<br>dashboard skeleton.|7|6|
|**S3**|17 Aug – 28 Aug|M1 Integratons & AI<br>Tiger Timing + RaceResult APIs, real-tme registraton<br>dashboard, AI email assistant (wetsuit), fnisher-shirt<br>aggregaton, camps/foreign events.|6.5|10|
|**S4**|31 Aug – 11 Sep|M2 – Contracts & Finance + AI Matching<br>Digital contracts, all-event tcketng & discounts, Qonto banking,<br>AI payment matching, DATEV export.|6.5|8.5|
|**S5**|14 Sep – 25 Sep|M4 Marketng + M5 Partner/Sponsor CRM<br>Campaign & budget planning, Grid Sports asset approval,<br>sponsoring CRM, service-provider coordinaton, alert engine, AI<br>photo tagging.|6|7.5|
|**S6**|28 Sep – 9 Oct|M3 – E-Commerce, Inventory & MVP Hardening<br>Online/on-site shop, catalog, checkout & payment, returns,<br>inventory & resource planning, auto-reorder, UAT & MVP go-<br>live.|6.5|8|



### **4.1 Sprint-by-Sprint Breakdown** 

#### **S1 · 20 Jul – 31 Jul — Foundation & Platform** 

_Repo, CI/CD, DB, Auth/RBAC, app shell, design system, core data model. Everything M1+ builds on._ 

|**ID**|**Task**|**Owner**|**Prio**|**Days**|
|---|---|---|---|---|
|**F-01**|Provision monorepo (frontend React+TS, backend NestJS+TS),<br>shared ESLint/Preter/tsconfg, commit conventons.|Adea+Lum|Must|1.5|
|**F-02**|CI/CD pipeline: lint + unit tests + build on PR; auto-deploy to staging<br>on merge to main.|Lum|Must|1.5|
|**F-03**|Dockerized local stack (PostgreSQL, API, web) + .env.example +<br>secrets handling.|Lum|Must|1|
|**F-04**|PostgreSQL schema v1 + migraton tooling (Prisma/TypeORM); core<br>enttes: Tenant, User, Role, Event, Partcipant, Product, Partner.|Lum|Must|2|
|**F-05**|Authentcaton (email+password, JWT/refresh) and RBAC with roles:<br>Admin, GF/Management, Staf, Read-only.|Lum|Must|2|
|**F-06**|React app shell: routng, auth guard, layout (nav + module menu),<br>design system (component library, theme, tokens).|Adea|Must|2.5|
|**F-07**|Global data layer: API client, React Query setup, error/toast<br>handling, form validaton (Zod/React Hook Form).|Adea|Must|1.5|



EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 5 of 18 

#### **S2 · 3 Aug – 14 Aug — M1 Core – Events & Participants** 

_Event/Series/Race CRUD, participant registry, document store, dashboard skeleton._ 

|**ID**|**Task**|**Owner**|**Prio**|**Days**|
|---|---|---|---|---|
|**F-08**|Audit log + sof-delete conventon; centralized logging & error<br>monitoring (e.g. Sentry).|Lum|Should|1|
|**F-09**|File/object storage service (S3-compatble) with virus-safe upload,<br>plus optonal SharePoint sync hook.|Lum|Must|1.5|
|**M1-01**|CRUD for Series, Events, Races, Distances, Age/Level categories (e.g.<br>Alpen Open Water Cup).|Adea|Must|2.5|
|**M1-02**|Event capacity & scheduling: slots, dates, venues, status<br>(draf/published/closed).|Adea|Must|1.5|
|**M1-03**|Partcipant registry: profle (name, DOB/age, height, weight, contact,<br>emergency), event enrollments, history.|Lum|Must|2.5|
|**M1-04**|Bulk import/normalizaton of partcipants (CSV) as fallback before<br>Tiger Timing sync.|Lum|Should|1|
|**M1-05**|Central store for course maps / technical buoy drawings, linked to<br>Event/Race; versioning + SharePoint link.|Adea|Must|1.5|
|**M1-06**|Management dashboard skeleton: KPI tles (registratons, capacity,<br>revenue) with placeholder data source.|Adea|Must|1.5|



#### **S3 · 17 Aug – 28 Aug — M1 Integrations & AI** 

_Tiger Timing + RaceResult APIs, real-time registration dashboard, AI email assistant (wetsuit), finisher-shirt aggregation, camps/foreign events._ 

|**ID**|**Task**|**Owner**|**Prio**|**Days**|
|---|---|---|---|---|
|**M1-07**|Bidirectonal API integraton with Tiger Timing (Meldewesen): pull<br>registratons, push/confrm entries.|Lum|Must|3|
|**M1-08**|API integraton with RaceResult (billing/rankings): pull results &<br>rankings, reconcile to partcipants.|Lum|Must|2.5|
|**M1-09**|Real-tme registraton dashboard aggregatng external systems<br>(Tiger Timing) for live capacity monitoring.|Adea|Must|2|
|**M1-10**|AI email intake: parse partcipant emails, match to DB record,<br>classify intent (wetsuit, org queston).|Lum|Must|2.5|
|**M1-11**|Wetsuit recommendaton engine: from age/height/weight →<br>suggested brand/size + live stock check; draf reply.|Lum|Must|2|
|**M1-12**|Human-in-the-loop approval UI: GF reviews/edits AI draf, one-click<br>send, plus reminder (Wiedervorlage) scheduling.|Adea|Must|2|
|**M1-13**|Finisher-shirt / merchandise size aggregaton auto-computed from<br>partcipant enrollments per event.|Adea|Must|1|
|**M1-14**|Management areas for foreign/third-party events and swim camps<br>(hotel + training management).|Adea|Should|1.5|



#### **S4 · 31 Aug – 11 Sep — M2 – Contracts & Finance + AI Matching** 

_Digital contracts, all-event ticketing & discounts, Qonto banking, AI payment matching, DATEV export._ 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 6 of 18 

|**ID**|**Task**|**Owner**|**Prio**|**Days**|
|---|---|---|---|---|
|**M2-01**|Contract templates + automated generaton of partcipant contracts<br>(liability, cancellaton clauses).|Adea|Must|2.5|
|**M2-02**|Contract lifecycle: status (draf/sent/signed), storage, retrieval, audit<br>trail.|Lum|Should|1|
|**M2-03**|All-Event tcket management with automated discount handling &<br>pricing rules.|Adea|Must|2.5|
|**M2-04**|Invoice/fee generaton per partcipant with open-balance tracking.|Lum|Must|1.5|
|**M2-05**|Qonto banking API integraton: pull transactons (Zahlungseingänge)<br>in near real tme.|Lum|Must|2|
|**M2-06**|AI payment matching: match Qonto incoming payments to open<br>partcipant fees via intelligent algorithm.|Lum|Must|2.5|
|**M2-07**|Reconciliaton review UI: confrm/override AI matches, mark paid,<br>handle partal/over-payments.|Adea|Must|1.5|
|**M2-08**|DATEV export for tax advisor (bookings/receipts in DATEV-<br>compatble format).|Lum|Must|1.5|



#### **S5 · 14 Sep – 25 Sep — M4 Marketing + M5 Partner/Sponsor CRM** 

_Campaign & budget planning, Grid Sports asset approval, sponsoring CRM, service-provider coordination, alert engine, AI photo tagging._ 

|**ID**|**Task**|**Owner**|**Prio**|**Days**|
|---|---|---|---|---|
|**M4-01**|Campaign & budget planning: event marketng (posters) + add-ons<br>(partes, meet&greets) with budget vs actual.|Adea|Must|2|
|**M4-02**|Asset library + approval interface for agency 'Grid Sports' to submit<br>Instagram content for central release.|Adea|Must|2|
|**M4-03**|Computer-vision auto-tagging of event photos into categories (start,<br>course, fnish, award, individual athlete).|Lum|Should|2.5|
|**M5-01**|CRM for stakeholders: sponsors, partners, service providers with<br>contacts, agreements, value tracking.|Lum|Must|2.5|
|**M5-02**|Service-provider planning & cost tracking for essental partners (e.g.<br>Wasserwacht) per event.|Lum|Must|1.5|
|**M5-03**|Automated alert system: warn before contract expiry & on<br>outstanding sponsoring payments.|Adea|Must|2|
|**M5-04**|Notfcaton service (in-app + email) shared across modules (alerts,<br>reminders, approvals).|Lum|Should|1|



#### **S6 · 28 Sep – 9 Oct — M3 – E-Commerce, Inventory & MVP Hardening** 

_Online/on-site shop, catalog, checkout & payment, returns, inventory & resource planning, auto-reorder, UAT & MVP go-live._ 

|**ID**|**Task**|**Owner**|**Prio**|**Days**|
|---|---|---|---|---|
|**M3-01**|Product catalog for 50–100 merchandising/swim-gear artcles:<br>variants (size/color), price, stock, images.|Adea|Must|2|
|**M3-02**|Customer-facing online shop: browse, cart, checkout with payment<br>(Stripe/PSP).|Adea|Must|3|



EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 7 of 18 

|**ID**|**Task**|**Owner**|**Prio**|**Days**|
|---|---|---|---|---|
|**M3-03**|On-site (POS-style) sales capture at events, drawing from same<br>inventory.|Lum|Should|1.5|
|**M3-04**|Returns/refund management (Retourenmanagement) ted to orders<br>and stock.|Lum|Should|1.5|
|**M3-05**|Inventory & resource planning: org materials (buoys, Restubes),<br>storage locatons, feet (vans/GF car).|Lum|Must|2|
|**M3-06**|Cloud stock management with min-quantty thresholds + automatc<br>reorder suggestons.|Lum|Must|1.5|
|**M3-07**|MVP hardening: UAT with EOWE, bug-fx pass, performance &<br>security review, documentaton.|Adea+Lum|Must|2|
|**M3-08**|MVP producton deployment + go-live runbook + handover to EOWE<br>key users.|Adea+Lum|Must|1|



EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 8 of 18 

## **5. Detailed Technical Requirements by Module** 

Each requirement below carries an ID (matching the spreadsheet backlog), owner, sprint, priority and acceptance criteria. “Done” means the acceptance criteria are demonstrably met on staging. 

### **Foundation & Platform (Sprint 1)** 

#### **Environment & DevOps** 

**F-01  Provision monorepo (frontend React+TS, backend FastAPI), shared ESLint/Prettier/tsconfig, commit conventions.** 

**Owner:** Adea+Lum **Sprint:** S1 **Priority:** Must **Est:** 1.5 d **Depends on:** - 

**Acceptance:** Repo cloned & bootstrapped by both devs; `npm run dev` starts FE+BE locally; lint passes in CI. 

##### **F-02  CI/CD pipeline: lint + unit tests + build on PR; auto-deploy to staging on merge to main.** 

**Owner:** Lum **Sprint:** S1 **Priority:** Must **Est:** 1.5 d **Depends on:** F-01 

**Acceptance:** PR triggers pipeline; green build auto-deploys to staging URL; failing tests block merge. 

##### **F-03  Dockerized local stack (PostgreSQL, API, web) + .env.example + secrets handling.** 

**Owner:** Lum **Sprint:** S1 **Priority:** Must **Est:** 1 d **Depends on:** F-01 

**Acceptance:** `docker compose up` runs full stack; onboarding doc lets a new dev run it in <15 min. 

#### **Data & Persistence** 

**F-04  PostgreSQL schema v1 + migration tooling (Prisma/TypeORM); core entities: Tenant, User, Role, Event, Participant, Product, Partner.** 

**Owner:** Lum **Sprint:** S1 **Priority:** Must **Est:** 2 d **Depends on:** F-03 

**Acceptance:** Migrations run forward/back cleanly; ER diagram committed; seed script creates demo data. 

#### **Security & Access** 

**F-05  Authentication (email+password, JWT/refresh) and RBAC with roles: Admin, GF/Management, Staff, Read-only.** 

**Owner:** Lum **Sprint:** S1 **Priority:** Must **Est:** 2 d **Depends on:** F-04 

**Acceptance:** User can log in/out; protected routes enforce role; unauthorized returns 403; passwords hashed (bcrypt/argon2). 

#### **UI Platform** 

**F-06  React app shell: routing, auth guard, layout (nav + module menu), design system (component library, theme, tokens).** 

**Owner:** Adea **Sprint:** S1 **Priority:** Must **Est:** 2.5 d **Depends on:** F-01 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 9 of 18 

**Acceptance:** Authenticated shell renders module nav; reusable Button/Input/Table/Modal/Form components documented in Storybook. 

##### **F-07  Global data layer: API client, React Query setup, error/toast handling, form validation (Zod/React Hook Form).** 

**Owner:** Adea **Sprint:** S1 **Priority:** Must **Est:** 1.5 d **Depends on:** F-06 

**Acceptance:** One vertical slice (e.g. Users list) fetches from API with loading/error states and validated form submit. 

#### **Cross-cutting** 

##### **F-08  Audit log + soft-delete convention; centralized logging & error monitoring (e.g. Sentry).** 

**Owner:** Lum **Sprint:** S2 **Priority:** Should **Est:** 1 d **Depends on:** F-04 

**Acceptance:** Create/update/delete on core entities writes audit entries; unhandled errors surface in monitoring. 

##### **F-09  File/object storage service (S3-compatible) with virus-safe upload, plus optional SharePoint sync hook.** 

**Owner:** Lum **Sprint:** S2 **Priority:** Must **Est:** 1.5 d **Depends on:** F-04 

**Acceptance:** File upload/download works with signed URLs; metadata stored in DB; large files stream, not buffered. 

### **Module 1 — Event & Participant Management** 

#### **Competition & Series Mgmt** 

##### **M1-01  CRUD for Series, Events, Races, Distances, Age/Level categories (e.g. Alpen Open Water Cup).** 

**Owner:** Adea **Sprint:** S2 **Priority:** Must **Est:** 2.5 d **Depends on:** F-06 

**Acceptance:** User creates a Series with nested Events → Races → Distances; validation prevents overlaps; list & detail views. 

##### **M1-02  Event capacity & scheduling: slots, dates, venues, status (draft/published/closed).** 

**Owner:** Adea **Sprint:** S2 **Priority:** Must **Est:** 1.5 d **Depends on:** M1-01 

**Acceptance:** Capacity per race enforced; publishing an event makes it visible to registration flow; overbooking blocked. 

#### **Participant Management** 

**M1-03  Participant registry: profile (name, DOB/age, height, weight, contact, emergency), event enrollments, history.** 

**Owner:** Lum **Sprint:** S2 **Priority:** Must **Est:** 2.5 d **Depends on:** F-04 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 10 of 18 

**Acceptance:** Participant can be created/edited/searched; enrollment links participant↔race; body metrics stored for AI use. 

##### **M1-04  Bulk import/normalization of participants (CSV) as fallback before Tiger Timing sync.** 

**Owner:** Lum **Sprint:** S2 **Priority:** Should **Est:** 1 d **Depends on:** M1-03 

**Acceptance:** CSV upload maps columns, validates, reports errors per row, dedupes by email/name+DOB. 

#### **Document & Media Store** 

##### **M1-05  Central store for course maps / technical buoy drawings, linked to Event/Race; versioning + SharePoint link.** 

**Owner:** Adea **Sprint:** S2 **Priority:** Must **Est:** 1.5 d **Depends on:** F-09 

**Acceptance:** Files attach to a race, are previewable, versioned, and searchable by event/type tag. 

#### **Dashboard** 

##### **M1-06  Management dashboard skeleton: KPI tiles (registrations, capacity, revenue) with placeholder data source.** 

**Owner:** Adea **Sprint:** S2 **Priority:** Must **Est:** 1.5 d **Depends on:** M1-01 

**Acceptance:** Dashboard route renders KPI tiles + per-event drill-down; layout responsive; data wired to real API in S3. 

##### **M1-09  Real-time registration dashboard aggregating external systems (Tiger Timing) for live capacity monitoring.** 

**Owner:** Adea **Sprint:** S3 **Priority:** Must **Est:** 2 d **Depends on:** M1-07,M1-06 

**Acceptance:** Dashboard shows live registration counts vs capacity per event; auto-refresh; export to CSV. 

#### **Integration: Tiger Timing** 

##### **M1-07  Bidirectional API integration with Tiger Timing (Meldewesen): pull registrations, push/confirm entries.** 

**Owner:** Lum **Sprint:** S3 **Priority:** Must **Est:** 3 d **Depends on:** M1-03 

**Acceptance:** Registrations sync into participant registry on schedule + on demand; conflicts logged; mapping documented; ret/backoff on failure. 

#### **Integration: RaceResult** 

##### **M1-08  API integration with RaceResult (billing/rankings): pull results & rankings, reconcile to participants.** 

**Owner:** Lum **Sprint:** S3 **Priority:** Must **Est:** 2.5 d **Depends on:** M1-07 

**Acceptance:** Results import per race; rankings visible in event detail; reconciliation flags unmatched entries. 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 11 of 18 

#### **AI – Email Assistant (HITL)** 

**M1-10  AI email intake: parse participant emails, match to DB record, classify intent (wetsuit, org question).** 

**Owner:** Lum **Sprint:** S3 **Priority:** Must **Est:** 2.5 d **Depends on:** M1-03,F-09 

**Acceptance:** Incoming email matched to participant by name; intent classified; low-confidence flagged for manual routing. 

**M1-11  Wetsuit recommendation engine: from age/height/weight → suggested brand/size + live stock check; draft reply.** 

**Owner:** Lum **Sprint:** S3 **Priority:** Must **Est:** 2 d **Depends on:** M1-10,M3-06 

**Acceptance:** Given metrics + stock, system proposes size (e.g. Arena M) with availability; generates draft mail; blocks if out of stock. 

##### **M1-12  Human-in-the-loop approval UI: GF reviews/edits AI draft, one-click send, plus reminder (Wiedervorlage) scheduling.** 

**Owner:** Adea **Sprint:** S3 **Priority:** Must **Est:** 2 d **Depends on:** M1-11 

**Acceptance:** GF sees draft + source data side-by-side; can edit & send; reminder mail scheduled (e.g. 1 day pre-race). 

#### **AI – Aggregation** 

**M1-13  Finisher-shirt / merchandise size aggregation auto-computed from participant enrollments per event.** 

**Owner:** Adea **Sprint:** S3 **Priority:** Must **Est:** 1 d **Depends on:** M1-03 

**Acceptance:** Per-event report totals shirt sizes in real time from registrations; exportable order list per size. 

#### **Additional Events & Camps** 

##### **M1-14  Management areas for foreign/third-party events and swim camps (hotel + training management).** 

**Owner:** Adea **Sprint:** S3 **Priority:** Should **Est:** 1.5 d **Depends on:** M1-01 

**Acceptance:** Camp entity supports hotel nights & training sessions; third-party events tracked separately from own events. 

### **Module 2 — Contracts & Finance** 

#### **Digital Contracts** 

**M2-01  Contract templates + automated generation of participant contracts (liability, cancellation clauses).** 

**Owner:** Adea **Sprint:** S4 **Priority:** Must **Est:** 2.5 d **Depends on:** M1-03 

**Acceptance:** Template merges participant/event data into PDF; legally-safe archival with timestamp; downloadable & emailable. 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 12 of 18 

##### **M2-02  Contract lifecycle: status (draft/sent/signed), storage, retrieval, audit trail.** 

**Owner:** Lum **Sprint:** S4 **Priority:** Should **Est:** 1 d **Depends on:** M2-01 

**Acceptance:** Each contract has status + history; signed copies archived; searchable by participant/event. 

#### **Ticketing & Billing** 

##### **M2-03  All-Event ticket management with automated discount handling & pricing rules.** 

**Owner:** Adea **Sprint:** S4 **Priority:** Must **Est:** 2.5 d **Depends on:** M1-01 

**Acceptance:** Ticket types configurable; rule engine applies discounts; price shown pre/post-discount; combinable rules validated. 

##### **M2-04  Invoice/fee generation per participant with open-balance tracking.** 

**Owner:** Lum **Sprint:** S4 **Priority:** Must **Est:** 1.5 d **Depends on:** M2-03 

**Acceptance:** Fees generated per enrollment/ticket; open vs paid status tracked; invoice PDF produced. 

#### **Integration: Qonto** 

##### **M2-05  Qonto banking API integration: pull transactions (Zahlungseingänge) in near real time.** 

**Owner:** Lum **Sprint:** S4 **Priority:** Must **Est:** 2 d **Depends on:** F-04 

**Acceptance:** Bank transactions imported on schedule; stored with metadata; reconciliation-ready; secure credential storage. 

#### **AI – Payment Matching** 

##### **M2-06  AI payment matching: match Qonto incoming payments to open participant fees via intelligent algorithm.** 

**Owner:** Lum **Sprint:** S4 **Priority:** Must **Est:** 2.5 d **Depends on:** M2-04,M2-05 

**Acceptance:** Incoming payment auto-matched to open fee (amount/name/reference); confidence score; unmatched queued for review. 

##### **M2-07  Reconciliation review UI: confirm/override AI matches, mark paid, handle partial/over-payments.** 

**Owner:** Adea **Sprint:** S4 **Priority:** Must **Est:** 1.5 d **Depends on:** M2-06 

**Acceptance:** User sees suggested matches ranked; can confirm/reassign; balances update; partial payments supported. 

#### **Accounting: DATEV** 

**M2-08  DATEV export for tax advisor (bookings/receipts in DATEV-compatible format).** 

**Owner:** Lum **Sprint:** S4 **Priority:** Must **Est:** 1.5 d **Depends on:** M2-04 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 13 of 18 

**Acceptance:** Export generates valid DATEV CSV/format for a date range; reconciled entries included; downloadable. 

### **Module 4 — Marketing & Social Media** 

#### **Campaign Planning** 

**M4-01  Campaign & budget planning: event marketing (posters) + add-ons (parties, meet&greets) with budget vs actual.** 

**Owner:** Adea **Sprint:** S5 **Priority:** Must **Est:** 2 d **Depends on:** F-06 

**Acceptance:** Create campaigns with budget lines; track planned vs actual spend; link campaigns to events. 

#### **Asset Management** 

**M4-02  Asset library + approval interface for agency 'Grid Sports' to submit Instagram content for central release.** 

**Owner:** Adea **Sprint:** S5 **Priority:** Must **Est:** 2 d **Depends on:** F-09 

**Acceptance:** Agency uploads assets; EOWE reviews/approves/rejects with comments; approved assets flagged ready-to-publish. 

#### **AI – Photo Sorting** 

##### **M4-03  Computer-vision auto-tagging of event photos into categories (start, course, finish, award, individual athlete).** 

**Owner:** Lum **Sprint:** S5 **Priority:** Should **Est:** 2.5 d **Depends on:** F-09 

**Acceptance:** Uploaded photos auto-tagged into configured categories; manual re-tag possible; batch upload supported. 

### **Module 5 — Partner, Sponsoring & Service-Provider CRM** 

#### **Sponsoring Management** 

**M5-01  CRM for stakeholders: sponsors, partners, service providers with contacts, agreements, value tracking.** 

**Owner:** Lum **Sprint:** S5 **Priority:** Must **Est:** 2.5 d **Depends on:** F-04 

**Acceptance:** Partner records with type, contacts, linked events; monetary + in-kind (Sachleistungen) contributions logged. 

#### **Service Provider Coordination** 

**M5-02  Service-provider planning & cost tracking for essential partners (e.g. Wasserwacht) per event.** 

**Owner:** Lum **Sprint:** S5 **Priority:** Must **Est:** 1.5 d **Depends on:** M5-01 

**Acceptance:** Assign providers to events with planned/actual cost; availability & booking status tracked. 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 14 of 18 

#### **Alert Engine** 

##### **M5-03  Automated alert system: warn before contract expiry & on outstanding sponsoring payments.** 

**Owner:** Adea **Sprint:** S5 **Priority:** Must **Est:** 2 d **Depends on:** M5-01 

**Acceptance:** Rules trigger notifications X days before expiry / on overdue payment; alerts shown in-app + email; configurable thresholds. 

##### **M5-04  Notification service (in-app + email) shared across modules (alerts, reminders, approvals).** 

**Owner:** Lum **Sprint:** S5 **Priority:** Should **Est:** 1 d **Depends on:** F-08 

**Acceptance:** Central notification service delivers in-app + email; used by M1 reminders, M5 alerts; user preferences honored. 

### **Module 3 — E-Commerce, Logistics & Administration** 

#### **Product Catalog** 

**M3-01  Product catalog for 50–100 merchandising/swim-gear articles: variants (size/color), price, stock, images.** 

**Owner:** Adea **Sprint:** S6 **Priority:** Must **Est:** 2 d **Depends on:** F-06,M3-06 

**Acceptance:** Products with variants CRUD; images; price & stock per variant; category filtering & search. 

#### **Online Shop** 

##### **M3-02  Customer-facing online shop: browse, cart, checkout with payment (Stripe/PSP).** 

**Owner:** Adea **Sprint:** S6 **Priority:** Must **Est:** 3 d **Depends on:** M3-01 

**Acceptance:** Customer adds to cart, checks out, pays; order created; stock decremented; confirmation email sent. 

#### **On-site Sales** 

##### **M3-03  On-site (POS-style) sales capture at events, drawing from same inventory.** 

**Owner:** Lum **Sprint:** S6 **Priority:** Should **Est:** 1.5 d **Depends on:** M3-01 **Acceptance:** Staff records on-site sale; inventory updates in real time; sale linked to event & payment method. 

#### **Returns** 

##### **M3-04  Returns/refund management (Retourenmanagement) tied to orders and stock.** 

**Owner:** Lum **Sprint:** S6 **Priority:** Should **Est:** 1.5 d **Depends on:** M3-02 

**Acceptance:** Return initiated against an order; refund recorded; stock re-incremented; return status tracked. 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 15 of 18 

#### **Inventory & Resources** 

**M3-05  Inventory & resource planning: org materials (buoys, Restubes), storage locations, fleet (vans/GF car).** 

**Owner:** Lum **Sprint:** S6 **Priority:** Must **Est:** 2 d **Depends on:** M3-01 

**Acceptance:** Assets tracked with quantity, location, assignment to events; fleet bookable per event. 

##### **M3-06  Cloud stock management with min-quantity thresholds + automatic reorder suggestions.** 

**Owner:** Lum **Sprint:** S6 **Priority:** Must **Est:** 1.5 d **Depends on:** M3-05 

**Acceptance:** Stock below min triggers reorder suggestion; suggestion list exportable; feeds wetsuit stock check (M1-11). 

#### **Hardening** 

**M3-07  MVP hardening: UAT with EOWE, bug-fix pass, performance & security review, documentation.** 

**Owner:** Adea+Lum **Sprint:** S6 **Priority:** Must **Est:** 2 d **Depends on:** M3-02 

**Acceptance:** UAT checklist signed off; critical/high bugs closed; smoke tests pass on staging; user & admin docs delivered. 

#### **Go-Live** 

##### **M3-08  MVP production deployment + go-live runbook + handover to EOWE key users.** 

**Owner:** Adea+Lum **Sprint:** S6 **Priority:** Must **Est:** 1 d **Depends on:** M3-07 

**Acceptance:** Production env live; backups & monitoring active; rollback documented; key users onboarded. 

### **Module 6 — Future Expansion (post-MVP)** 

#### **Subscription Model** 

**M6-01  Subscription management: recurring billing, digital+physical service packages (training videos, personalized gear).** 

**Owner:** Adea+Lum **Sprint:** Backlog **Priority:** Could **Est:** 5 d **Depends on:** M2-05 

**Acceptance:** Deferred to post-MVP: recurring payment integration combinable with All-Event ticket. Data model prepared in MVP. 

#### **AI – Course Simulation** 

**M6-02  Geodata-based AI buoy-setting: simulate & propose new courses for additional age/level classes.** 

**Owner:** Adea+Lum **Sprint:** Backlog **Priority:** Could **Est:** 8 d **Depends on:** M1-05 

**Acceptance:** Deferred (advanced): requires geodata processing; MVP only stores course maps/drawings centrally. 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 16 of 18 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 17 of 18 

## **6. Getting Started — Monday 20 July** 

Sprint 1 is foundation work both developers do together so every later module has solid ground. Suggested order for the first two days: 

- Both: clone the monorepo, agree branch/PR conventions, confirm everyone can run FE + BE locally (F-01). 

- Lum: stand up Docker stack + PostgreSQL and the migration tooling; commit the v1 schema and ER diagram (F-03, F-04). 

- Adea: scaffold the React app shell, routing and the first design-system components in Storybook (F-06). 

- Lum: wire CI/CD so PRs run lint + tests and merges deploy to staging (F-02). 

- Both: implement auth + RBAC end-to-end as the first vertical slice, then split into module work from Sprint 2 (F-05, F-07). 

_Definition of Done (every task): acceptance criteria met, code reviewed by the other developer, tests where applicable, deployed to staging, no open critical/high bugs._ 

### **6.1 Open Points to Confirm with EOWE** 

These do not block the start but should be clarified during Sprint 1–2 reviews: 

- API credentials & documentation for Tiger Timing, RaceResult and Qonto (and DATEV export spec / advisor requirements). 

- Payment service provider choice for the shop (Stripe assumed) and legal review of contract templates. 

- Exact discount rules for All-Event tickets and the roster of merchandising SKUs (50–100). 

- SharePoint integration depth (link vs full sync) for course maps and documents. 

EOWE Workspace — Technical Requirements & Delivery Plan   |   Page 18 of 18 

