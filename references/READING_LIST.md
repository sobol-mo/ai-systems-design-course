# Reading list and source plan

Status: planned source allocation. The mapping below guides course development; it does not yet assign mandatory reading to students.

## Primary reference

Chip Huyen. *AI Engineering: Building Applications with Foundation Models*. First edition. O'Reilly Media, 2025. The electronic edition was released on 4 December 2024.

- Print ISBN: `9781098166304`.
- EPUB ISBN: `9781098166267`.
- O'Reilly online ISBN: `9781098166298`.
- Role in the course: the common AI engineering framework, from use-case selection and foundation models through evaluation, prompting, RAG, agents, data, inference, architecture, observability, and feedback.

### Legal access

Downloadable edition:

- [Rakuten Kobo Worldwide](https://www.kobo.com/ww/en/ebook/ai-engineering) sells the English EPUB3 edition, ISBN `9781098166267`.
- Kobo identifies the download as `EPUB3 (DRM-Free)`. Availability and price depend on the purchaser's country and billing address.
- A purchased copy is for the purchaser's licensed use. Keep it in private storage outside the course repository; do not redistribute the book to students.

Online reading:

- [O'Reilly Online Learning](https://www.oreilly.com/library/view/ai-engineering/9781098166298) provides the complete book through an individual or institutional subscription.
- A Kobo purchase can also be read through Kobo applications and the Kobo Web Reader, in addition to downloading the DRM-free EPUB3 file.
- [OverDrive](https://www.overdrive.com/media/11413819/ai-engineering) lists the official ebook for library lending. Actual access depends on whether a reader's participating library has licensed the title.

Official free companion materials:

- [Author's companion repository](https://github.com/chiphuyen/aie-book) contains the table of contents, chapter summaries, study notes, case studies, prompt examples, and other supporting resources.
- The companion repository is useful for navigation and student links, but it is not a substitute for the full book.

## Specialized references

Tomaž Bratanič and Oskar Hane. *Essential GraphRAG: Knowledge Graph-Enhanced RAG*. Manning, 2025. ISBN `9781633436268`.

- Role: embeddings, vector similarity, hybrid retrieval, graph construction, GraphRAG, natural-language-to-Cypher retrieval, agentic RAG, and retrieval evaluation.
- Cheapest legal download: [Neo4j's official book offer](https://neo4j.com/essential-graphrag) provides the complete English PDF free after submitting its access form. Neo4j identifies Manning as the publisher and PDF as the available format.
- Permanent purchase fallback: [Manning](https://www.manning.com/books/essential-graphrag) sells the DRM-free PDF/EPUB ebook with permanent online liveBook access. The displayed promotional price was `$32.99` on 27 August 2026.
- Online reading: [Manning liveBook](https://livebook.manning.com/book/essential-graphrag), a Manning Lite subscription, or [O'Reilly Online Learning](https://www.oreilly.com/library/view/essential-graphrag/9781633436268). The unauthenticated liveBook page is only a free extract; complete access requires purchase or subscription.
- [Official source-code repository](https://github.com/tomasonjo/kg-rag).

Alessandro Negro, Vlastimil Kůs, Giuseppe Futia, and Fabio Montagna. *Knowledge Graphs and LLMs in Action: Build AI Systems Using Connected Data*. Manning, 2025. ISBN `9781633439894`.

- Role: ontology- and taxonomy-driven graph design, knowledge extraction from structured and unstructured data, graph enrichment, reasoning, and knowledge-graph-powered RAG.
- Cheapest permanent acquisition: take one month of [Manning Pro](https://www.manning.com/subscription) for `$24.99`, select this title as the included monthly ebook, download its DRM-free PDF and EPUB files, then cancel renewal if the subscription is no longer needed. Manning states that the selected ebook is kept permanently.
- Direct-purchase fallback: [Manning](https://www.manning.com/books/knowledge-graphs-and-llms-in-action) displayed `$38.99` for the DRM-free PDF/EPUB ebook with permanent liveBook access on 27 August 2026.
- Cheapest online-only access to both Manning books: Manning Lite for `$19.99` per month. [Manning liveBook](https://livebook.manning.com/book/knowledge-graphs-and-llms-in-action) also provides a free extract before purchase.
- Alternative online reading: [O'Reilly Online Learning](https://www.oreilly.com/library/view/knowledge-graphs-and/9781633439894).
- [Official source-code repository](https://github.com/alenegro81/knowledge-graphs-and-llms-in-action).

## Supporting reference

Chip Huyen. *Designing Machine Learning Systems: An Iterative Process for Production-Ready Applications*. O'Reilly Media, 2022.

- Role: durable production ML-system principles where the foundation-model-focused primary book intentionally provides less depth: data engineering, deployment, monitoring, distribution shifts, continual learning, testing in production, and MLOps infrastructure.
- Ebook ISBN: `9781098107918`.
- Cheapest verified permanent download: [Rakuten Kobo Worldwide](https://www.kobo.com/ww/en/ebook/designing-machine-learning-systems) displayed `$41.09` on 27 August 2026 for the English DRM-free EPUB3.
- Purchase fallback: [Helion](https://helion.pl/ksiazki/designing-machine-learning-systems-chip-huyen,e_2r2u.htm) displayed `169.14 PLN` for the English EPUB and MOBI files. Helion uses a personalized watermark rather than DRM and accepts card or PayPal payments for digital products.
- Online reading: [O'Reilly Online Learning](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956), Kobo's applications and Web Reader after purchase, or [OverDrive/Libby](https://www.overdrive.com/media/9005583/designing-machine-learning-systems) when a participating library licenses the title.
- [Official companion repository](https://github.com/chiphuyen/dmls-book).

## Recommended acquisition strategy for the additional references

Prices below were checked on 27 August 2026. They can change by country, tax treatment, promotion, and checkout address. Approximate hryvnia values use the National Bank of Ukraine reference rate of `44.5717 UAH/USD` for that date.

For permanent downloadable copies useful to both the reader and the course-development workflow:

1. Obtain *Essential GraphRAG* as the free official PDF from Neo4j.
2. Subscribe to Manning Pro for one month at `$24.99`, choose *Knowledge Graphs and LLMs in Action* as the included ebook to keep, download PDF and EPUB, and cancel renewal unless continued access is useful.
3. Buy the DRM-free EPUB3 of *Designing Machine Learning Systems* from Kobo Worldwide at the displayed `$41.09` price.

The verified total for these three permanent downloadable sources is approximately `$66.08`, or `2,945 UAH`, before any checkout taxes or currency-conversion fees.

For temporary online reading on one platform, O'Reilly Online Learning contains all three additional books and the primary *AI Engineering* book. Its individual plan was `$49` per month on 27 August 2026. This is the simplest short-term reading option, but it does not provide permanent, unrestricted ebook files.

## Planned topic-to-source allocation

The primary book supplies the shared conceptual spine. Specialized books provide depth where one chapter of the primary book is insufficient. Reference projects supply sanitized engineering cases and laboratory patterns, not required student dependencies. The instructor-only mapping from neutral case labels to actual projects is maintained in `course/PROJECT_SOURCES.md`.

| Course module | Planned topics | Primary source | Specialized or supporting sources | Practical evidence source |
|---|---|---|---|---|
| 01 — AI Engineering Foundations | AI engineering versus ML and software engineering; use-case evaluation; expectations; lifecycle and stack | *AI Engineering*, Chapter 1 | *Designing Machine Learning Systems*, Chapters 1-2 | Personal-assistant case: system boundaries and lifecycle decisions |
| 02 — Foundation Models and AI Application Architecture | model capabilities and limitations; sampling and structured output; prompting; build-versus-buy; adaptation choices; high-level application architecture | *AI Engineering*, Chapters 2, 5, 7, and 10, selected sections | *Designing Machine Learning Systems*, Chapters 2, 7, and 10, selected sections | Personal-assistant case: ports, adapters, model providers, gateways, and data boundaries |
| 03 — Evaluation and Experiment Design | evaluation criteria; exact and model-based evaluation; AI-as-a-judge; model selection; component and end-to-end evaluation; feedback | *AI Engineering*, Chapters 3-4; Chapters 6 and 10, selected evaluation sections | *Designing Machine Learning Systems*, Chapters 6 and 9, selected sections | Multi-agent orchestration case: evaluation boundaries and failure handling |
| 04 — Embeddings and Vector Retrieval | embedding representations; similarity; sparse, dense, and hybrid retrieval; chunking; reranking; retrieval metrics | *AI Engineering*, Chapters 3 and 6, selected sections | *Essential GraphRAG*: embeddings, vector similarity, hybrid retrieval, and pipeline evaluation | Knowledge-system case: derived vector indexes and retrieval over canonical knowledge |
| 05 — RAG and Context Engineering | prompt context; RAG architecture; ingestion and chunking; query rewriting; reranking; contextual and multimodal retrieval; provenance and evaluation | *AI Engineering*, Chapters 5-6; Chapter 8, selected data-quality sections | *Essential GraphRAG*: production RAG construction and evaluation | Knowledge-system and personal-assistant cases: ingestion, provenance, retrieval, and context assembly |
| 06 — Knowledge Graphs and GraphRAG | ontology and taxonomy; graph modeling; knowledge extraction; graph reasoning; vector-plus-graph retrieval; GraphRAG evaluation | *AI Engineering*, Chapter 6 as the RAG baseline | *Essential GraphRAG* and *Knowledge Graphs and LLMs in Action* as the main sources | Knowledge-system and personal-data cases: typed temporal graphs, schemas, and provenance |
| 07 — Agents and Multi-Agent Systems | tools; planning; memory; agent loops; specialization; orchestration; authority boundaries; state coordination; failure modes and evaluation | *AI Engineering*, Chapter 6; Chapter 10, selected agent and orchestration sections | *Essential GraphRAG*, agentic RAG sections | Multi-agent orchestration as the principal sanitized case study |
| 08 — Production AI Systems and Capstone | data quality; inference cost and latency; routing, gateways, caches, guardrails; privacy and safety; observability; feedback loops; deployment and continual improvement | *AI Engineering*, Chapters 8-10; Chapter 4 build-versus-buy criteria | *Designing Machine Learning Systems*, Chapters 7-10 | All four reference projects, with private operational details removed |

## Source-use rules

- Prefer durable concepts and decision frameworks over APIs or framework-specific tutorials.
- Treat chapter selections as provisional until each theory material and laboratory is approved.
- Verify time-sensitive claims, model names, prices, benchmarks, and tool behavior against current official documentation when authoring a module.
- Use official companion repositories for examples and supplementary material; do not imply that they contain the full books.
- Build each module's theory from its allocated source chapters and record a section-to-source map in the theory material. Quote only what is needed and permitted; otherwise paraphrase and add the source reference.
- Never commit purchased ebooks, unauthorized copies, credentials, personal data, or private infrastructure details to the course or student repositories.
