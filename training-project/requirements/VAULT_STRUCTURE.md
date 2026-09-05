# Learning Knowledge System — Markdown Vault Structure

> **Status:** Work in Progress — supplied vault contract for instructor review
>
> **Decision owner:** Course instructor
>
> **Scope:** Student-owned canonical Markdown vault

## Purpose

This document defines the durable organization rules for the external Markdown vault used by the learning knowledge system. It states where canonical records belong, how subject areas are classified, and which forms of organization are prohibited. It is a supplied project contract, not a taxonomy or folder-design assignment for each student.

The contract distinguishes four mechanisms that serve different purposes:

- a record type states what a record is;
- a tag supplies a cross-cutting classification facet such as subject domain;
- a typed relation states how two knowledge entities are semantically connected;
- a folder provides a stable physical location for one record type.

These mechanisms must not be treated as interchangeable.

## Core organization rule

Folders represent record type, not subject domain.

A record is placed according to what it is: a source, concept, question, proposal, decision, or operation record. A record is not placed according to what it is about. The vault therefore must not contain parallel subject trees such as `artificial-intelligence/`, `software-engineering/`, `economics/`, or a student-selected personal domain.

Subject and domain grouping is expressed through tags. A record may belong to several domains without being copied, moved, or forced into one privileged branch. Meaning-bearing hierarchy and other semantic connections are expressed through typed relations rather than through folder nesting or tag spelling.

## Required root structure

The cumulative vault uses the following record-type directories. A directory is created when its first permitted record is introduced; empty placeholder directories are not required.

```text
ai-systems-learning-vault/
  README.md
  sources/
  concepts/
  questions/
  proposals/
  decisions/
  operations/
```

The root entries have these responsibilities:

| Path | Record class | Responsibility |
|---|---|---|
| `README.md` | Vault orientation | States that the vault is student-controlled canonical learning state outside the course Git repository. |
| `sources/` | Source records | Preserves primary evidence or a version-resolving reference and its provenance. |
| `concepts/` | Concept records | Preserves accepted normalized interpretations and, when relations exist, their typed semantic relations. |
| `questions/` | Question records | Preserves accepted unresolved gaps, ambiguities, and learning needs. |
| `proposals/` | Candidate change records | Externalizes AI-generated semantic changes before canonical knowledge mutation. |
| `decisions/` | Decision records | Preserves the student's approval or rejection of exact candidate content. |
| `operations/` | Knowledge-operation records | Preserves application and post-application verification results. |

`README.md` is a retrieval and orientation surface, not a semantic knowledge entity. Proposal, decision, and operation records are retained canonical audit state, but they are not source, concept, or question entities.

Laboratory 01 creates only `README.md`, `sources/`, and the required Module 01 source record. It must not create empty directories merely to imitate the final tree.

## Folder invariants

Every canonical record must satisfy the following placement rules:

1. A record is stored directly in the root directory assigned to its declared record type.
2. A subject, course module, project, profession, or personal extension must not create another directory level.
3. The same record must not be copied into several directories to represent several classifications.
4. Moving a record between subject folders must not be used to represent a change in meaning.
5. A new root record-type directory requires an instructor-approved change to this contract and the applicable schema.
6. Derived embeddings, vector indexes, compiled graph views, caches, and generated exports remain outside the canonical vault structure.

Examples:

```text
# Accepted: type determines the folder
concepts/foundation-model.md
concepts/taxonomy.md
concepts/ontology.md
sources/module-01-ai-engineering-foundations.md

# Rejected: subject determines the folder
artificial-intelligence/concepts/foundation-model.md
computer-science/artificial-intelligence/foundation-model.md
personal-domain/notes/example.md
```

The accepted layout does not claim that all concepts form one flat semantic structure. It only keeps physical placement independent of subject classification. Hierarchies and networks remain explicit data.

## Domain and topic tags

Tags provide faceted classification: one record can carry several independent labels used for filtering, browsing, and retrieval. Domain membership is one such facet.

Domain tags use the following form:

```yaml
tags:
  - domain/ai-engineering
  - domain/software-engineering
```

The `domain/` prefix identifies the facet. The value after the slash uses lowercase kebab-case. The slash scopes the tag vocabulary; it does not by itself assert that one domain is broader, narrower, part of, or equivalent to another domain.

The following rules apply:

- reuse an existing domain tag when it has the intended meaning;
- assign more than one domain tag when a record genuinely crosses subject boundaries;
- do not create or move a folder to represent a domain tag;
- do not encode source provenance, record type, approval state, or semantic relations only as domain tags;
- expose a proposed new controlled tag for student review instead of silently creating spelling variants;
- keep non-sensitive personal-extension records in the same record-type directories as shared course records.

A tag is classificatory metadata. It helps retrieve a set of records, but it does not explain why two concepts are related.

## Taxonomy, faceted classification, and ontology

These terms describe different organization mechanisms and must be distinguished from the beginning of structured knowledge work.

**Taxonomy** is a controlled classification whose concepts are usually arranged through broader and narrower categories. A folder tree can imitate one taxonomy, but a taxonomy is a semantic classification, not a filesystem requirement. In this vault, a domain taxonomy is represented through concept records and approved typed relations. It is not encoded as nested subject folders.

**Faceted classification** assigns several independent dimensions to the same record. Domain tags are one facet. Later schemas may define other controlled facets, but adding a facet does not change the record's type or physical location.

**Ontology** defines the kinds of entities and relations that exist in a domain and the constraints on their valid use. The course uses a deliberately small educational ontology: supplied record types, a controlled relation vocabulary, and validation rules. An ontology is richer than either a folder tree or a tag list.

**Typed relations** carry meaning that must be traversable and reviewable, including prerequisite, class, part-whole, contrast, support, and source relationships. Names such as `requires` or `is-a` in this paragraph are pedagogical examples. They are not the closed course vocabulary. That vocabulary is supplied with the relation schema when relation validation becomes a student requirement. Tags must not replace these relations. For example, tagging two records with `domain/ai-engineering` groups them for retrieval; it does not establish that one `requires`, `is-a`, `part-of`, `contrasts-with`, `supported-by`, or is `about` the other.

The operational distinction among folders, tags, and relations is required from vault creation so that the first source record is not placed in a subject tree. The course may name taxonomy, ontology, and typed relation so that students recognize the terms. Naming a term does not require the corresponding system behavior yet. Laboratory 01 does not create concept records.

## Record names and identity

Markdown filenames use lowercase kebab-case and remain stable after references to the record exist. The filename is a readable locator; the identifier declared by the applicable record schema is the stable identity.

Examples:

```text
sources/module-01-ai-engineering-foundations.md
concepts/faceted-classification.md
questions/how-should-domain-tags-be-governed.md
```

Renaming a title does not automatically require changing a stable identifier. A file rename must preserve or update every affected reference through an approved change.

The common fields and type-specific fields for structured records belong to later schemas. This structure contract does not invent those schemas. The minimal Laboratory 01 source record remains defined by `SYSTEM_BRIEF.md`.

## Agent interpretation rules

An agent operating on the vault must interpret this contract as follows:

- reject a proposed subject-domain directory tree;
- place a proposed record only in the directory matching its declared record type;
- use tags for cross-cutting domain grouping;
- use typed relations for meaning-bearing hierarchy and semantic connections;
- reconcile existing tags and entities before proposing new ones;
- externalize changes through the applicable proposal and decision workflow;
- never reorganize accepted canonical records merely because a different topical hierarchy appears convenient.

A student may propose a better tag, relation, or entity interpretation. The agent may help formulate that proposal, but it must not bypass the student's semantic decision authority.

## Module 01 minimum

The Laboratory 01 vault contains this minimum observable structure:

```text
ai-systems-learning-vault/
  README.md
  sources/
    module-01-ai-engineering-foundations.md
```

The source record path and front matter are defined in `SYSTEM_BRIEF.md`. The Laboratory 01 vault contains no `concepts/` records, proposals for semantic ingest, graph index, or vector index.

## Verification

The structure contract is satisfied when the applicable laboratory demonstrates all of the following that it actually uses:

- every canonical record is located under the directory for its declared record type;
- no subject or personal-domain folder tree exists;
- a cross-domain fixture remains one record with multiple domain tags rather than duplicate files;
- tag values follow the controlled naming convention and do not imply unrecorded semantic relations;
- when typed relations exist, meaning-bearing connections are represented as approved typed relations rather than folders or tags;
- derived runtime artifacts can be removed without deleting canonical Markdown records;
- the vault remains usable with a plain text editor when Obsidian is unavailable.

## Design rationale and references

This layout prevents an early physical hierarchy from binding the knowledge base to one subject decomposition. The underlying method is known as **Zettelkasten** (German for "slip box") and is frequently cited in modern note-taking and knowledge-management systems. Niklas Luhmann, who developed the method, chose an open organization for his slip-box and rejected systematic placement by topics and subtopics because such placement commits a growing system to a long-lived order. The course does not reproduce Luhmann's physical numbering system or the full personal Zettelkasten workflow; it adopts the separation between stable physical placement and evolving semantic connections. Popular descriptions of Zettelkasten differ considerably, so the course cites the original essay rather than derivative blog interpretations.

The W3C SKOS Primer distinguishes concept schemes, labels, and semantic relations in knowledge-organization systems such as taxonomies. This course uses a smaller Markdown-native contract rather than requiring SKOS, Resource Description Framework, or Web Ontology Language tooling.

- Niklas Luhmann, “Communicating with Slip Boxes”: https://luhmann.surge.sh/communicating-with-slip-boxes
- W3C, “SKOS Simple Knowledge Organization System Primer”: https://www.w3.org/TR/skos-primer

## Review gate

This contract remains `Work in Progress` until the course instructor confirms the root record types, tag convention, and distinction between taxonomy, faceted classification, ontology, and typed relations. Later schemas and laboratory instructions must conform to this contract or record an explicit instructor-approved change.
