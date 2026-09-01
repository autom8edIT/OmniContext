# OmniContext

## SRE automation architecture case study

OmniContext documents the early prototype and the engineering decisions behind a
Windows-first, closed-loop SRE agent:

```text
detect -> diagnose -> propose -> authorize -> remediate -> verify
```

The prototype explored shared operational memory, multimodal ingestion, local
models, and host tooling. Its most important result was not a larger agent graph.
It was identifying which responsibilities must remain outside the language model:
authentication, policy, process control, provenance, rollback, and verification.

The active implementation of those lessons is
[GodBrain](https://github.com/usrname1git/GodBrain).

## Why this problem matters

Infrastructure incidents rarely fit inside one tool:

- a client failure may originate in DNS, routing, identity, policy, a service, or
  the operating system;
- raw logs and configuration dumps are too large and noisy to place directly in a
  model prompt;
- a plausible repair is not useful unless the system can prove that it fixed the
  original symptom;
- a model with direct database or shell access turns untrusted output into an
  operational security boundary.

OmniContext began as an attempt to give multiple tools a shared memory. The
project evolved toward a stricter objective: give one bounded SRE loop the minimum
evidence required to distinguish the failed layer, apply an allowlisted action,
and verify the outcome.

## Architecture evolution

| Prototype assumption | Finding | Current design |
|---|---|---|
| More model nodes improve reliability | Coordination adds latency and does not create evidence | One loop by default; add a node only for a distinct signal |
| A shared database can be model memory | Raw and reviewed claims have different trust levels | Immutable sources, candidate claims, explicit verification |
| The model can call infrastructure directly | Prompt content and model output are untrusted | Native kernel owns authorization and execution |
| A successful command means a successful repair | Commands can succeed while the incident remains | Verify the original symptom after every change |
| Model-specific tool patches are acceptable | They are brittle and couple policy to the inference engine | OpenAI-compatible model endpoint behind a stable kernel protocol |
| More context is always better | Unfiltered context hides the relevant signal | Bounded retrieval with provenance and failure-closed behavior |

See [ARCHITECTURE.md](ARCHITECTURE.md) for the detailed engineering decisions.

## What the repository contains

This repository preserves the prototype artifacts for engineering review:

- `memory_engine.py` - experimental MongoDB/Neo4j shared-memory layer;
- `Build-LlamaCpp.ps1` and `llama-overrides/` - model-specific tool experiments;
- `tools/` - early analysis and retrieval utilities;
- early API, ingestion, distributed inference, and presentation experiments.

These files are historical design evidence, not a supported production
deployment. Several contain machine-specific assumptions and predate the current
security model. They must not be used with real credentials or production data.

## Active implementation

GodBrain replaces the prototype's direct model-to-infrastructure relationships
with explicit boundaries:

```text
operator
   |
   v
C++ loopback kernel
   |-- authentication and policy
   |-- bounded tools and exact-child process control
   |-- audit, receipts, rollback and verification
   |
   +--> replaceable OpenAI-compatible local model
   |
   +--> Go memory-store and retrieval service
           |-- immutable raw sources
           |-- candidate knowledge
           |-- reviewed Golden Records
           +-- provenance and generation-addressed retrieval
```

Current engineering evidence is available in:

- [GodBrain README](https://github.com/usrname1git/GodBrain)
- [C++ kernel](https://github.com/usrname1git/GodBrain/tree/main/godbrain_core/cpp_kernel)
- [Memory Store](https://github.com/usrname1git/GodBrain/tree/main/godbrain_core/memory_store)
- [Windows SRE Surgeon](https://github.com/usrname1git/GodBrain/tree/main/godbrain_core/sre_agent)

## Reliability and security principles

1. **Diagnose before repair.** Start with read-only probes that distinguish the
   failed layer.
2. **Fail closed.** Missing authorization, retrieval, validation, or verification
   must not become a success-shaped fallback.
3. **Treat content as data.** Logs, web text, database records, and model output do
   not grant execution authority.
4. **Control the exact process created.** Timeouts and termination target the
   child or Job Object, never every process with a matching image name.
5. **Separate candidates from reviewed knowledge.** Repetition does not turn an
   unverified claim into truth.
6. **Verify the user-visible outcome.** A command exit code is only one piece of
   evidence.
7. **Keep remediation reversible.** High-impact changes require an explicit gate,
   a bounded action, and rollback where possible.

## Example SRE decision path

For a client reporting that an internal service cannot be reached:

```text
1. Reproduce the failure and capture the exact endpoint.
2. Test loopback and local TCP/IP health.
3. Resolve the hostname and compare expected records.
4. Test the route and destination port.
5. Identify the owning process or missing listener.
6. Select the smallest allowlisted correction supported by the evidence.
7. Repeat the original request and dependent health checks.
8. Record the observation, action, and verification result.
```

This avoids the traditional "repair cocktail" where DNS, Winsock, adapters,
services, and the operating system are reset without first proving which layer
failed.

## What this case study demonstrates

- Cross-layer Windows, Linux, networking, identity, and infrastructure reasoning.
- The ability to evolve a prototype after identifying unsafe assumptions.
- Security-conscious process execution and authorization design.
- Operational knowledge ingestion with provenance and explicit review.
- A verifier-first approach to agentic automation.
- Practical integration across C++, Go, PowerShell, Python, MongoDB, and local
  inference engines.

## Status

OmniContext is maintained as an architecture case study. New runtime development
continues in GodBrain. Keeping the prototype public makes the design evolution
inspectable instead of rewriting history around the final architecture.

## Author

[Joel Larsson](https://autom8ed.it) - Senior SRE and Infrastructure Automation
Engineer based in Sweden.
