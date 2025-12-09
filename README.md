# Obfuscrypt

> Research-grade code obfuscation framework — preserve semantics, hide implementation & logic.

## Status

* **Stage:** Prototype / proof-of-concept
* **Language POC:** Python
* **Branches:** `pyparser_development`, `vectorize_poc`

## Project overview

Obfuscrypt is a modular framework of obfuscation primitives and verification pipelines designed to transform source code (and internal logic) while preserving observable program behavior. The project combines AST-level transformations, vectorized program representations, and probabilistic equivalence verification (Monte Carlo sampling) to estimate semantic preservation.

This repository contains experimental tooling and research code; it is **not** production-ready.

## Goals

* Provide a library of **prebuilt + custom obfuscation primitives** (syntax, control-flow, data encoding, opaque predicates, logic rewriting, virtualization-like transformations).
* Offer a modular pipeline where parsers, normalizers, vectorizers, and obfuscation passes can be swapped.
* Verify semantics probabilistically using input sampling and trajectory-comparison metrics.
* Produce a visual/dev UI (optional) for composing pipelines and visualizing AST → vector trajectories.

## High-level approach

1. **Parse:** Convert source into an AST (language-specific parser; Python POC included).
2. **Normalize:** Canonicalize AST (whitespace, short names, deterministic ordering of some constructs) to reduce embedding noise.
3. **Vectorize:** Map AST nodes, edges, and execution traces into a constrained multidimensional coordinate space.
4. **Trajectory:** Represent program execution (or control/data-flow) as a trajectory through that vector space for sampled inputs.
5. **Compare:** Use trajectory similarity metrics and endpoint comparison across Monte Carlo-sampled inputs to estimate functional equivalence.
6. **Obfuscate:** Apply modular transformations that preserve the target equivalence metric — test with the verification pipeline.

> Note: naive embeddings produce high-dimensional noise; constraining dimensions and careful feature selection are critical for meaningful trajectories.

## Technical notes — vectorization & equivalence

* **Vectorization:** multiple approaches are explored (node-type embeddings, structural positional encodings, execution-state vectors). Embeddings must be constrained and normalized across program variants.
* **Trajectory generation:** either static (AST traversal order) or dynamic (instrumented execution traces). Dynamic traces provide stronger behavioral signals but require safe sandboxing and input sampling strategy.
* **Equivalence metric:** combination of trajectory similarity (DTW / cosine on constrained dims), endpoint output equality, and property-based checks. Monte Carlo sampling estimates probability of equivalence; coverage depends on input distribution.
* **Tradeoffs:** probabilistic verification cannot guarantee equivalence for arbitrary inputs — treat outputs as evidence, not absolute proof.

## Obfuscation primitives (examples)

* Identifier renaming & shadowing transformations
* Control-flow flattening and split/join patterns
* Opaque predicates and conditional morphing
* Expression rewriting and algebraic transformations
* Data encoding and packing layers
* Small VM / bytecode virtualization POC (research)

## Usage (quick)

1. Check out `pyparser_development` for parser/normalizer experiments.
2. Check out input.py and output.json in pyparser.
3. Check out testcases.
4. Check out `vectorize_poc` for vectorization & trajectory comparison POC.


## Limitations

* Currently a research prototype with limited language support (Python POC only).
* Equivalence verification is probabilistic and depends on input sampling quality.
* Not intended as a turnkey "one-click obfuscator" — it's a framework for experimentation and composition.

## Roadmap

* Stabilize python parser and AST normalization pipeline.
* Implement and benchmark multiple embedding schemes with controlled dimensionality.
* Build a core set of obfuscation primitives with end-to-end verification tests.
* Prototype a minimal UI for composing pipelines and visualizing trajectories.

## Devlog & updates

Occasional devlog posts may appear at `@kernel_patch` on Instagram. Updates are sporadic.

## Contribution

* Pull requests: **please do not submit PRs** — they will not be reviewed. If you want to help, open an issue describing a focused research contribution first.

## License

TBD — research-use preferred. Check LICENSE file in repo (if present).

## Contact

Repo maintainer: `kernel_patch` (sporadic updates)

---

ANTLR BTW


