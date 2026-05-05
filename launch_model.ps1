param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("heavyweight", "specialist", "coder", "multimodal")]
    $Model
)

$MODEL_DIR = "C:\Users\autismo\Models"
$LLAMA_SERVER = "llama-server.exe" # Assumes it's in PATH via winget/manual

$ModelsMap = @{
    "heavyweight" = "Qwen3.6-27B-Abliterated-Heretic-Uncensored.Q4_K_M.gguf"
    "specialist"  = "Huihui-Qwen3.6-35B-A3B-Claude-4.7-Opus-abliterated-Q4_K_M.gguf"
    "coder"       = "OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-Q4_K_M.gguf"
    "multimodal"  = "supergemma4-e4b-abliterated.Q4_K_M.gguf"
}

$TargetModel = $ModelsMap[$Model]
$ModelPath = Join-Path $MODEL_DIR $TargetModel

if (!(Test-Path $ModelPath)) {
    Write-Error "Model file not found: $ModelPath. Run download_models.ps1 first."
    return
}

echo "[+] Igniting GodBrain Node: $Model"
echo "[+] Offloading to 4080 SUPER (CUDA Accelerated)..."

# Configuration optimized for 16GB VRAM
# -ngl 99: Offload all layers to GPU
# -c 8192: context window
# --port 8080: Standard local API port

if ($Model -eq "specialist") {
    echo "[!] Warning: 35B MoE will require Hybrid mode (GPU + System RAM)."
    & $LLAMA_SERVER -m $ModelPath -ngl 35 -c 4096 --port 8080
} else {
    & $LLAMA_SERVER -m $ModelPath -ngl 99 -c 8192 --port 8080
}
