import asyncio
from god_brain_core import GodBrainEngine

async def main():
    engine = GodBrainEngine()
    recent = await engine.get_recent(5)
    for t in recent:
        print(f"Content: {t['content']}, Synced: {t['synced_to_graph']}")

if __name__ == "__main__":
    asyncio.run(main())
