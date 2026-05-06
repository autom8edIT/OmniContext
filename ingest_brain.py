import os
import easyocr
import asyncio
from god_brain_core import GodBrainEngine, logger

class UniversalIngestionEngine:
    """
    GodBrain Universal Ingestion Engine:
    Handles OCR extraction and unified knowledge injection.
    """

    def __init__(self):
        self.engine = GodBrainEngine()
        logger.info("Initializing EasyOCR (GPU-Accelerated: EN, SV)...")
        self.reader = easyocr.Reader(["en", "sv"], gpu=True)

    def _extract_text(self, image_path: str) -> str:
        """Internal helper for OCR extraction."""
        results = self.reader.readtext(image_path, detail=0)
        return " ".join(results).strip()

    async def ingest_image(
        self, image_path: str, source: str = "OCR_Ingestor", entities: list = None
    ):
        """Extracts text from image and injects structured knowledge into Local/Cloud DBs."""
        if not os.path.exists(image_path):
            logger.error(f"File not found: {image_path}")
            return None

        logger.info(f"Ingesting: {image_path}")
        raw_text = self._extract_text(image_path)

        if not raw_text:
            logger.warning("No text extracted.")
            return None

        filename = os.path.basename(image_path)
        
        # Check for Google Auth Migration URL
        if "otpauth-migration://" in raw_text:
            try:
                from google_auth_decoder import decode_google_auth_url
                import re
                # Find the URL in the text
                url_match = re.search(r"otpauth-migration://offline\?data=[a-zA-Z0-9%._-]+", raw_text)
                if url_match:
                    url = url_match.group(0)
                    decoded_secrets = decode_google_auth_url(url)
                    # SECURITY: Do NOT append raw decoded secrets to raw_text
                    if not entities:
                        entities = []
                    for s in decoded_secrets:
                        entities.append({"label": "MFA_Secret", "name": f"{s['issuer']}:{s['name']}"})
                    logger.info(f"[+] Decoded {len(decoded_secrets)} MFA secrets (Redacted from logs)")
            except Exception as e:
                logger.error(f"[-] Failed to decode MFA URL: {e}")

        content = f"[{filename}] {raw_text}"
        
        # Unified save (Mongo + Neo4j)
        thought_id = await self.engine.save_thought(
            content=content,
            source=source,
            entities=entities
        )
        
        if thought_id:
            logger.info(f"[+] Knowledge captured: {thought_id}")
            return thought_id
        return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ingest_brain.py <image_path>")
        sys.exit(1)

    ingestor = UniversalIngestionEngine()
    async def run():
        await ingestor.ingest_image(sys.argv[1])
        # Wait a bit for background sync
        await asyncio.sleep(2)
    
    asyncio.run(run())
