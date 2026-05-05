from ingest_brain import UniversalIngestionEngine


def run_structured_test():
    engine = UniversalIngestionEngine()
    image_path = r"C:\Users\autismo\Downloads\h1470.png"

    # Manually defined entities from LLM-style analysis of the OCR text
    entities = [
        {"label": "Hardware", "name": "PCIE"},
        {"label": "Hardware", "name": "DIMM"},
        {"label": "Brand", "name": "Republic of Gamers"},
        {"label": "Series", "name": "Apex"},
        {"label": "Hardware", "name": "Motherboard"},  # Inferred context
    ]

    try:
        engine.ingest_image(image_path, entities=entities)
        print("[+] Structured ingestion complete.")
    finally:
        engine.close()


if __name__ == "__main__":
    run_structured_test()
