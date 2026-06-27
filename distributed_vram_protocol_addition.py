# Merge this into self_model/agent_instructions.py
# Add after the last CognitiveProtocol in DistributedCognitiveOperatingSystem class.
# Also add to BrainLayer permanent examples, GodBrainSkill, and a new ConstitutionChangeEvent evt-020 or next.
# This makes the specialist aware of the distributed VRAM capability as part of the organism.

    distributed_vram_lending: CognitiveProtocol = field(default_factory=lambda: CognitiveProtocol(
        skill_id="distributed_vram_lending",
        description=(
            "Protocol for 'lending' VRAM over Tailscale using llama.cpp RPC to run 26-27B models by sharding layers across peers' GPUs (e.g. 2GB from brother 500Mbit fiber, colleague). "
            "With 1Gbit/2ms fiber, this should give smooth performance, avoiding the 1 tok/s GC variance from yesterday. "
            "Main on 4080 uses --rpc to peers running rpc-server. "
            "Fits the decentralized organism: peers as compute cells, you control the God node. Private, sovereign. "
            "Use generate_distributed_vram_command MCP tool or Launch-DistributedLlama.ps1 -RpcPeers ... or update launch_model.ps1 with -RpcPeers."
        ),
        workflow=[
            CognitiveProtocolStep(step=1, action="discover_peers", params={"via": "Tailscale status or MCP register_vram_peer", "bandwidth_check": "1Gbit+ ideal for smooth sharding"}),
            CognitiveProtocolStep(step=2, action="prepare_peers", params={"run": "Start-RpcPeer.ps1 on each (build llama.cpp -DGGML_RPC=ON -DGGML_CUDA=ON)", "port": 50052}),
            CognitiveProtocolStep(step=3, action="generate_command", params={"use": "MCP generate_distributed_vram_command(peers=..., model='specialist')", "result": "full llama-server cmd with --rpc list"}),
            CognitiveProtocolStep(step=4, action="launch", params={"script": "Launch-DistributedLlama.ps1 -Model specialist -RpcPeers ... or native in launch_model.ps1", "ngl": "99 to push layers to lent VRAM"}),
            CognitiveProtocolStep(step=5, action="verify_pooling", params={"on_peers": "nvidia-smi to see your model layers using their VRAM", "speed": "expect much better than 1 tok/s, test with small context first"}),
            CognitiveProtocolStep(step=6, action="save_experience", target="shared_brain_layer2", params={"tags": ["distributed", "vram_lending", "tailscale", "organism_compute"]})
        ],
        requirements={
            "network": "Tailscale with high bandwidth low latency (your 1Gbit 2ms + peers 500Mbit should rock for this)",
            "build": "All (main + peers) llama.cpp built with GGML_RPC=ON and CUDA (update Build-LlamaCpp.ps1)",
            "peers": "Trusted, run the rpc-server exposing GPU (lend 2GB+ each)",
            "access": ["generate_distributed_vram_command", "Launch-DistributedLlama.ps1", "Start-RpcPeer.ps1", "query_constellation for peer graphs"]
        },
        version="1.0"
    ))

# Also add to the permanent brain layer examples list:
# "distributed_vram_lending"

# Add to GodBrainSkill as distributed_vram_lending_protocol or similar.

# New evt example:
# ConstitutionChangeEvent(
#     id="evt-020",
#     ...
#     description="Added distributed_vram_lending CognitiveProtocol and MCP tool for VRAM pooling over Tailscale with good fiber. Updated launch_model.ps1 for -RpcPeers native support. Enables organism to borrow VRAM from peers for 26B+ without GC slowdowns.",
#     ...
# )
