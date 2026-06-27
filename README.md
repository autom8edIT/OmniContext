# GodBrain

> Use **any** LLM model, train them as a **collective brain & memory**, and unlock tools that default `llama-server` can't do.

## TL;DR

GodBrain turns local models into a shared, sovereign cognitive system. The core idea:

- **🧠 Model-agnostic** — Plug in *any* LLM (Gemma, etc.). No model is special; they're interchangeable nodes in one collective brain.
- **📚 Models teach models** — Past models become **teachings**. Their thoughts and analysis are saved permanently and queried later, so newer models inherit prior reasoning instead of starting cold.
- **🛠️ Tools that aren't possible by default** — Native MCP tool use that a stock `llama-server` won't give you: permanent memory, local filesystem read/write/execute, code-graph self-analysis, telemetry, OCR, and more.

## How it works

`Build-LlamaCpp.ps1` overlays files from `llama-overrides/` onto the llama.cpp source at build time. The key piece is:

**[`llama-overrides/common/godbrain_chat_extensions.cpp`](llama-overrides/common/godbrain_chat_extensions.cpp)**

It teaches the chat layer to treat GodBrain's MCP tools as **first-class tokens** — preserving them so the model can reliably emit and act on them *without fighting the chat template* (instead of them being mangled as plain text or stop sequences).

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

Default `llama-server` will happily break tool calls because the chat template doesn't know about them. By registering these tools (and architect-mode tokens) into `data.preserved_tokens`, GodBrain makes tool use **reliable and native** rather than a brittle hack.

```cpp
godbrain::apply_godbrain_chat_extensions(data, "gemma-4-26B-...");
```

This is additive — call it from a model-specific init (e.g. `common_chat_params_init_gemma4`) and the whole fleet becomes GodBrain-aware.

## The bigger picture

GodBrain is a **Distributed Cognitive OS**: intelligence is decoupled from hardware. The "mind" lives in shared brain-wires; models contribute sensing, compute, and local agency, and high-leverage MCP tools (memory, constellation, script execution) are favored over low-leverage busywork.
