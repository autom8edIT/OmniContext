Place your GodBrain-specific modifications here (e.g. chat.cpp, chat-peg-parser.cpp, or even a patched CMakeLists.txt for the common target).

The Build-LlamaCpp.ps1 script will copy everything under this tree over the llama.cpp source tree before configuring/building.

Example:
  llama-overrides\common\chat.cpp          # your custom Gemma4 + GodBrain MCP handling
  llama-overrides\common\chat-peg-parser.cpp

Files ending in .example* or containing README are ignored during overlay.

After dropping real patched files here, just run .\Build-LlamaCpp.ps1 again.
This keeps your patches inside the GodBrain repo (sovereign + versioned + queryable via constellation) instead of polluting the upstream tree.

See:
- llama-overrides\common\chat.cpp.godbrain-example.patch (idea)
- llama-overrides\common\godbrain_chat_extensions.cpp (real starting point for MCP tool awareness + preserved tokens on the specialist)

After build, the script will remind you how to wire the extensions into the gemma4 init etc.