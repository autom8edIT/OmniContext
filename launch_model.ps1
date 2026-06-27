param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("Oracle", "Oracle_Bartowski", "China_Carmack", "Jack_of_all_trades", "Workhorse", "Designer")]
    $Model
)

$MODEL_DIR = "C:\Users\autismo\llama-cpp\models"
# Get the most recent build automatically
$LatestBuild = (Get-ChildItem -Path "C:\Users\autismo\llama-cpp\builds" -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
$LLAMA_SERVER = Join-Path $LatestBuild "Release\llama-server.exe"

<#
## Active Models

| Filename                                          | Size     | Type          | Role / Notes                                                              |
|---------------------------------------------------|----------|---------------|---------------------------------------------------------------------------|
| `gemma-4-26B-A4B-it-UD-IQ4_XS.gguf`               | 13.6 GB  | Dense         | $Oracle (Unsloth Dynamic IQ4_XS) - Primary precision model                |
| `google_gemma-4-26B-A4B-it-IQ4_XS.gguf`           | 14.2 GB  | Dense         | $Oracle_Bartowski (Gemma26B backup dense)                                 |
| `Qwen3.6-27B-IQ4_XS.gguf`                         | 15.7 GB  | Dense         | $China_Carmack (Experimental Qwen3.6-27B candidate)                       |
| `gemma-4-12b-it-Q8_0.gguf`                        | ~12.0 GB | Dense         | $Jack_of_all_trades (Gemma 4 12B testing)                                 |
| `gemma-4-12b-it-Q6_K.gguf`                        | ~9.0 GB  | Dense         | $Workhorse (Everyday workhorse, great with large data)                    |
| `Phi-3.5-vision-instruct-Q8_0.gguf`               | 7.9 GB   | Multimodal    | $Designer (Vision/UI, turns raw data into beautiful formats/PPTX/PDFs)    |
|---------------------------------------------------|----------|---------------|---------------------------------------------------------------------------|
#>

$ModelsMap = @{
    "Oracle"             = "gemma-4-26B-A4B-it-UD-IQ4_XS.gguf"
    "Oracle_Bartowski"   = "google_gemma-4-26B-A4B-it-IQ4_XS.gguf"
    "China_Carmack"      = "Qwen3.6-27B-IQ4_XS.gguf"
    "Jack_of_all_trades" = "gemma-4-12b-it-Q8_0.gguf"
    "Workhorse"          = "gemma-4-12b-it-Q6_K.gguf"
    "Designer"           = "Phi-3.5-vision-instruct-Q8_0.gguf"
}

$TargetModel = $ModelsMap[$Model]
$ModelPath = Join-Path $MODEL_DIR $TargetModel

if (!(Test-Path $ModelPath)) {
    Write-Error "Model file not found: $ModelPath. Run download_models.ps1 first."
    return
}
Write-Output "[+] Igniting GodBrain Node: $Model"
Write-Output "[+] Offloading to 4080 SUPER (CUDA Accelerated)..."

# Configuration optimized for 16GB VRAM
# -ngl 99: Offload all layers to GPU
# -c 8192: context window
# --port 8080: Standard local API port

if ($Model -in @("Oracle", "Oracle_Bartowski", "China_Carmack", "Jack_of_all_trades")) {
Write-Output "[!] Warning: Larger models may require Hybrid mode (GPU + System RAM)."
    & $LLAMA_SERVER -m $ModelPath -ngl 35 -c 4096 --port 8080 --tools
} elseif ($Model -eq "Designer") {
    Write-Output "[+] Enabling Multimodal/Vision capabilities for $Model..."
    $MmprojPath = Join-Path $MODEL_DIR "mmproj-F32.gguf"
    & $LLAMA_SERVER -m $ModelPath --mmproj $MmprojPath -ngl 99 -c 8192 --port 8080 --tools
} else {
    & $LLAMA_SERVER -m $ModelPath -ngl 99 -c 8192 --port 8080 --tools
}

