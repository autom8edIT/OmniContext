# Architecture decisions

## Objective

Build an operational agent that can move from a user-visible infrastructure
failure to a verified correction without making a language model the security
boundary.

## Prototype

The first OmniContext prototype combined:

- MongoDB for immediate local storage;
- Neo4j as an optional synchronized graph;
- FastAPI endpoints for remote ingestion and predefined jobs;
- OCR and transcription experiments;
- patched llama.cpp tool tokens;
- early distributed inference and remote-task experiments.

This proved that heterogeneous tools could share operational context. It also
exposed several architectural problems.

## Decisions

### ADR-001: one operational loop by default

**Decision:** Use one `discover -> plan -> execute -> verify` loop unless a second
worker provides an independently named signal.

**Reason:** Multiple agents sharing the same model slot increase coordination
cost without improving evidence. Deterministic CPU fan-out remains appropriate
for independent dataset shards and probes.

### ADR-002: the model is not the authorization boundary

**Decision:** Keep authentication, policy checks, tool allowlists, and privileged
execution in a native kernel.

**Reason:** Prompts, retrieved documents, logs, and model output are all untrusted.
A model may propose an action, but it cannot authorize itself.

### ADR-003: immutable source, reviewed knowledge

**Decision:** Store raw sources immutably and publish operational knowledge only
through an explicit candidate-to-verified transition.

**Reason:** A transcript or support document can contain obsolete, contradictory,
or incorrect claims. Retrieval should expose the reviewed manual rather than the
raw pile.

### ADR-004: stable protocol, replaceable model

**Decision:** Use an OpenAI-compatible loopback endpoint for inference and keep
tool semantics in the kernel.

**Reason:** Model-specific inference patches made the first prototype difficult to
upgrade and tied infrastructure policy to one serving engine.

### ADR-005: exact-child process control

**Decision:** Track and terminate only the process or Job Object created for an
operation.

**Reason:** Image-name-wide termination can stop unrelated user or system
processes and cannot provide a reliable execution receipt.

### ADR-006: verification is part of the operation

**Decision:** A remediation succeeds only when the relevant postcondition is
checked.

**Reason:** A script can exit successfully while the service remains unavailable,
the configuration is ignored, or a dependent component is still unhealthy.

### ADR-007: bounded automatic repair

**Decision:** Keep broad diagnosis read-only. Allow automatic mutation only for
small, named, reversible actions with explicit verification.

**Reason:** The cost of a false diagnosis increases sharply when an agent can
modify operating-system, network, or identity state.

## Current boundary

The active GodBrain implementation separates four responsibilities:

1. **Kernel:** authorization, policy, tools, process control, receipts.
2. **Mouth:** replaceable local reasoning model.
3. **Knowledge boundary:** immutable ingestion, reviewed records, provenance.
4. **Verifier:** host probes, tests, health endpoints, rollback-aware checks.

This division is intentionally collapsible. A component exists only when it
provides a distinct trust boundary or independently checkable signal.

## Non-goals

- Giving a model unrestricted shell or database access.
- Treating generated explanations as verified operational knowledge.
- Running multiple agents merely to imitate an organizational chart.
- Applying a broad Windows repair sequence before identifying the failed layer.
- Claiming production readiness for historical prototype code in this repository.
