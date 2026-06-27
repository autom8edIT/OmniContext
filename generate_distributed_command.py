#!/usr/bin/env python3
"""
Mac-side helper (run from your Mac session, since files are on PC).
Generates the Windows PowerShell command for the PC using launch_model.ps1 with -RpcPeers.

Usage from Mac:
python3 generate_distributed_command.py --peers 100.64.1.5 100.64.2.10 --model specialist

Then SSH or copy-paste the command to run on PC.
"""
import argparse
from typing import List

def generate_launch_command(peers: List[str], model: str = "specialist", rpc_port: int = 50052) -> str:
    if not peers:
        return "No peers."
    peers_str = '","'.join(peers)
    cmd = f'pwsh -File .\\launch_model.ps1 -Model {model} -RpcPeers "{peers_str}" -RpcPort {rpc_port}'
    return cmd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate distributed launch command (for PC, run from Mac).")
    parser.add_argument("--peers", nargs="+", required=True, help="Tailscale IPs of peers")
    parser.add_argument("--model", default="specialist")
    parser.add_argument("--port", type=int, default=50052)
    args = parser.parse_args()
    print(generate_launch_command(args.peers, args.model, args.port))
    print("\n# Copy and run the above on your PC (after peers run Start-RpcPeer.ps1).")
    print("# With your fiber, this should give smooth 26B+ runs by pooling VRAM.")
