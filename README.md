# GodBrain

> Use **any** AI model — be it a commercial model through your favorite `-cli` or an LLM of any type. The most genius part of GodBrain is that it's both **model and tool agnostic**: everything can get boosted by it, and everything can contribute. Train them as a **collective brain & memory**, and unlock tools that default `llama-server` can't do.

## TL;DR

GodBrain turns local models into a shared, sovereign cognitive system. The core idea:

- **🧠 Model-agnostic** — Plug in *any* LLM (Gemma, etc.). No model is special; they're interchangeable nodes in one collective brain.
- **📚 Models teach models** — Past models become **teachings**. Their thoughts and analysis are saved permanently and queried later, so newer models inherit prior reasoning instead of starting from scratch.
- **🛠️ Tools that aren't possible by default** — Native MCP tool use that a stock `llama-server` won't give you: permanent memory, local filesystem read/write/execute, code-graph self-analysis, and more.

## The Compute Cheat Code (Local + Cloud Synergy)

Because the "brain" (MongoDB + Constellation) is completely decoupled from the compute, GodBrain unlocks a massive hardware cheat code:

- **Massive Local Context — it scales infinitely with your hardware:** As if running *any* model wasn't enough, GodBrain just gets better the more you throw at it. On a PC with a 3090, 4090, or 5090? Great — bigger card, better local LLMs, more headroom. But here's where it gets silly: Apple Silicon's unified memory breaks the matrix. A Mac with 128GB+ UMA (think M5 Max and up) runs **100B+ parameter models locally** without paying the insane dedicated-VRAM tax. At that point you're not running a chatbot — you're basically a droid from Star Wars walking around with a sovereign brain in your bag.
- **Hybrid Intelligence:** You aren't limited to local models. Hook up APIs for Grok, Gemini, Codex, or anything else. Let them crunch the massive datasets and commit their insights directly into Constellation.
- **Unrestricted Execution:** Your local, uncensored models read those teachings from the shared MongoDB and execute the highly-privileged, unrestricted OS-level operations (like running `wsudo` scripts) that heavily-censored corporate APIs refuse to do.

Cloud models do the heavy context lifting; your local sovereign models pull from the shared memory to execute with God-level permissions.

## How it works

`Build-LlamaCpp.ps1` overlays files from `llama-overrides/` onto the llama.cpp source at build time. The key piece is:

**[`llama-overrides/common/godbrain_chat_extensions.cpp`](llama-overrides/common/godbrain_chat_extensions.cpp)**

It teaches the chat layer to treat GodBrain's MCP tools as **first-class tokens** — preserving them so the model can reliably emit and act on them *without fighting the chat template* (instead of having them mangled or stripped).

### GodBrain-native MCP tools

These are injected as preserved tokens so any model can use them:

| Tool | Purpose |
|------|---------|
| `save_godbrain_thought` | Permanent memory — write reasoning the next model can learn from |
| `query_constellation` | Code-graph self-analysis |
| `query_recent_thoughts` | Recall prior models' thinking |
| `read_local_file` / `write_local_file` | Native, privileged local filesystem access (no browser sandbox theater) |
| `list_local_dir` / `ensure_local_dir` | Local directory ops |
| `execute_godbrain_script` | Direct script execution / control |
| `get_system_telemetry` | Hardware/system awareness |
| `ocr_image` | Image → text |
| `ask_local_llm` | Route a step to another local model |
| `get_cognitive_protocol` | Fetch a reusable "recipe" / workflow |
| `propose_sovereign_architect_change` | Evolve the system's own rules |

### Why preserved tokens matter

Default `llama-server` will happily break tool calls because the chat template doesn't know about them. By registering these tools (and architect-mode tokens) into `data.preserved_tokens`, GodBrain makes them durable and reliable across the fleet.

```cpp
godbrain::apply_godbrain_chat_extensions(data, "gemma-4-26B-...");
```

This is additive — call it from a model-specific init (e.g. `common_chat_params_init_gemma4`) and the whole fleet becomes GodBrain-aware.

## The bigger picture

GodBrain is a **Distributed Cognitive OS**: intelligence is decoupled from hardware. The "mind" lives in shared brain-wires; models contribute sensing, compute, and local agency, and high-leverage teachings persist for every model that follows.
