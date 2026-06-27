<#
.SYNOPSIS
    Slacker helper for "cosplaying as webdev" to launch your GodBrain llama-server with distributed RPC over Tailscale for VRAM lending.

.DESCRIPTION
    Uses llama.cpp's built-in RPC to "lend" VRAM from peers (brother, colleague etc.) over Tailscale VPN.
    Your 4080 SUPER can use remote GPUs' VRAM (e.g. 2GB each) to run 26-27B models by distributing layers.

    This is the closest to "Apple UMA stack but through internet" - pipeline parallel sharding of the model across machines.

    Peers run a lightweight rpc-server exposing their GPU.
    Your machine runs the main server with --rpc list of peer Tailscale IPs:ports.

    Performance note: With your 1Gbit fiber 2ms to core and peers' 500Mbit, this should be *insanely* better than the 1 tok/s GC variance you saw yesterday (models doing garbage collection instead of halting). RPC layer sharding over low-latency fiber should give smooth runs for 26-27B. Still not local UMA, but close for pooled VRAM. Test with small model first. Use -ngl 99 to maximize offload to the lent VRAM.

    Requires: 
    - All machines on same Tailscale network (ACLs allowing TCP 50052).
    - llama.cpp built with -DGGML_RPC=ON (add to your Build-LlamaCpp.ps1 cmake if not already; your custom build should support it now).
    - Peers have NVIDIA GPU with CUDA, enough VRAM to lend (they specify in their rpc-server? The main controls offload).

.PARAMETER Model
    The model alias (specialist, etc.) or direct .gguf path.

.PARAMETER RpcPeers
    Array of Tailscale IPs or hostnames of the lending machines, e.g. "100.64.1.5","100.64.2.10"

.PARAMETER RpcPort
    Port the rpc-servers are listening on (default 50052).

.PARAMETER ExtraArgs
    Additional args for llama-server.

.EXAMPLE
    .\Launch-DistributedLlama.ps1 -Model specialist -RpcPeers "100.64.1.5","100.64.3.7"

    # Peers on those Tailscale IPs must be running the rpc-server.

.NOTES
    For peers (lenders): Run a simple script like Start-RpcPeer.ps1 (create similar) or manually:
    cd to llama.cpp build dir
    ./bin/rpc-server -p 50052 -H 0.0.0.0 

    Then on your machine, the --rpc will offload layers to their GPUs' VRAM.

    To "lend" specific amount: The scheduler uses available, you control with -ngl on main and how many peers.

    Integrate with GodBrain: Use your godbrain_mcp or add a tool to generate this.

    "Lend 2GB each": Feasible for sharding 26B Q4 (~15-20GB total + KV) across 5-10 peers + your 4080.

    If speed sucks over internet, use for LAN or accept the trade-off for fitting the model without cloud.

    Good night (or day) after no sleep - this is the slacker cosplay webdev help (PS "web" for config, simple "UI" via params).
#>

[CmdletBinding()]
param(
    [string]$Model = "specialist",
    [string[]]$RpcPeers = @(),
    [int]$RpcPort = 50052,
    [string]$ExtraArgs = ""
)

$ErrorActionPreference = "Stop"
Set-Location "C:\Users\autismo\Documents\GitHub\GodBrain"

Write-Host "=== Slacker Distributed VRAM Lend Launcher (Tailscale + llama.cpp RPC) ===" -ForegroundColor Cyan
Write-Host "Model: $Model" -ForegroundColor Yellow
if ($RpcPeers.Count -eq 0) {
    Write-Host "No RpcPeers specified - running local only." -ForegroundColor Yellow
} else {
    Write-Host "RPC Peers (Tailscale IPs/hostnames): $($RpcPeers -join ', '):$RpcPort" -ForegroundColor Green
    Write-Host "This will 'borrow' VRAM from them for your 26-27B models. Like distributed UMA over net (not perfect, but works for fitting)." -ForegroundColor Green
}

# Build the rpc arg
$rpcArg = ""
if ($RpcPeers.Count -gt 0) {
    $peerList = $RpcPeers | ForEach-Object { "${_}:$RpcPort" }
    $rpcArg = "--rpc " + ($peerList -join ',')
    Write-Host "Constructed: $rpcArg" -ForegroundColor Magenta
}

# Get the launch command from your existing logic or hardcode for simplicity
# For slacker, we'll call your launch_model or construct basic.
# Assume your custom llama-server is in C:\Users\autismo\llama-cpp\llama-server.exe (from your builds)

$llamaServer = "C:\Users\autismo\llama-cpp\llama-server.exe"
$modelPath = "C:\Users\autismo\llama-cpp\models\gemma-4-26B-A4B-it-UD-IQ4_XS.gguf"  # adjust or use your alias logic

if ($Model -eq "specialist") {
    $modelPath = "C:\Users\autismo\llama-cpp\models\gemma-4-26B-A4B-it-UD-IQ4_XS.gguf"
} elseif ($Model -eq "bartowski") {
    # etc, or extend
}

$baseArgs = @(
    "-m", $modelPath,
    "--port", "8080",
    "--host", "0.0.0.0",
    "-ngl", "99",
    "--cont-batching",
    "--flash-attn"
)

if ($rpcArg) {
    $baseArgs += $rpcArg.Split(' ')
}

if ($ExtraArgs) {
    $baseArgs += $ExtraArgs.Split(' ')
}

Write-Host "Full command (copy for manual):" -ForegroundColor Cyan
$cmdStr = "$llamaServer " + ($baseArgs -join ' ')
Write-Host $cmdStr -ForegroundColor White

Write-Host "`nLaunching..." -ForegroundColor Green
& $llamaServer @baseArgs

Write-Host "If it fails on RPC, make sure peers are running rpc-server and Tailscale allows the port. Check logs for offload to remote devices." -ForegroundColor Yellow
Write-Host "For GodBrain integration: Call your MCP or use query_constellation to manage peer list in future." -ForegroundColor Yellow
Write-Host "Remember: This is the 'lend VRAM' for your organism. Decentralized power, autist style." -ForegroundColor Magenta
# Update: launch_model.ps1 now natively supports -RpcPeers thanks to the edit.
# Prefer: .\launch_model.ps1 -Model specialist -RpcPeers "100.64.1.5","100.64.2.10"
# The distributed wrapper still works for quick use.
