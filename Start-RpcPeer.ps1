<#
.SYNOPSIS
    For your brother/colleague etc. to run on their machine to "lend" GPU VRAM to your GodBrain 4080 for 26B models.

.DESCRIPTION
    Starts the llama.cpp rpc-server exposing their GPU over the network (use with Tailscale).

    They need llama.cpp built with RPC and CUDA.

    Run this, tell you their Tailscale IP, you use in Launch-DistributedLlama.ps1 -RpcPeers their-ip

    They lend e.g. 2-4GB by the main offloading layers to them.

    Slacker: Just run this in their llama.cpp dir after build.
#>

[CmdletBinding()]
param(
    [int]$Port = 50052,
    [int]$Threads = 8
)

Write-Host "Starting RPC server on port $Port for VRAM lending (Tailscale recommended for internet)." -ForegroundColor Cyan
Write-Host "Make sure Tailscale is up and your IP is shared with the main user." -ForegroundColor Yellow
Write-Host "With main's 1Gbit/2ms and your 500Mbit, lending 2GB+ will help the 26B run smooth, avoiding the GC 1tok/s issues." -ForegroundColor Green

# Assume in the build dir of llama.cpp with RPC enabled
$rpcServer = ".\build\bin\Release\rpc-server.exe"  # adjust to their build layout, or use full path

if (-not (Test-Path $rpcServer)) {
    Write-Host "rpc-server not found at $rpcServer. Build llama.cpp with -DGGML_RPC=ON and -DGGML_CUDA=ON first." -ForegroundColor Red
    Write-Host "Example cmake: cmake -B build -DGGML_CUDA=ON -DGGML_RPC=ON ..."
    exit 1
}

& $rpcServer -p $Port -H 0.0.0.0 -t $Threads

Write-Host "RPC server running. Your GPU VRAM is now lendable to the main 4080 via Tailscale IP:$Port" -ForegroundColor Green
Write-Host "Stop with Ctrl+C when done lending." -ForegroundColor Yellow
