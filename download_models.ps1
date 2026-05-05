# GodBrain: Model Intelligence Fleet
$MODEL_DIR = "C:\Users\autismo\Models"
if (!(Test-Path $MODEL_DIR)) { New-Item -ItemType Directory -Path $MODEL_DIR }

# 1. The Heavyweight (Qwen 3.6 27B)
echo "[+] Downloading Qwen 3.6 27B Heretic (The Heavyweight)..."
hf download Youssofal/Qwen3.6-27B-Abliterated-Heretic-Uncensored-GGUF --include "*Q4_K_M.gguf" --local-dir $MODEL_DIR

# 2. The Specialist (Huihui 35B MoE)
echo "[+] Downloading Huihui 35B MoE (The Specialist Reasoning)..."
hf download googlecs/Huihui-Qwen3.6-35B-A3B-Claude-4.7-Opus-abliterated-Q4_K_M-GGUF --include "*.gguf" --local-dir $MODEL_DIR

# 3. The Forbidden Coder (GPT-OSS 20B)
echo "[+] Downloading GPT-OSS 20B NEO (The System Architect)..."
hf download DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf --include "*Q4_K_M.gguf" --local-dir $MODEL_DIR

# 4. The Multimodal King (SuperGemma 4 E4B)
echo "[+] Downloading SuperGemma 4 (The Ingestion Brain)..."
hf download mradermacher/supergemma4-e4b-abliterated-i1-GGUF --include "*Q4_K_M.gguf" --local-dir $MODEL_DIR

echo "`n[!] All systems clear. Your 'Abliterated' fleet is ready for ignition."
