import easyocr
import sys
import os


def run_ocr(image_path):
    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path}")
        return

    print(f"Ingesting: {image_path}")
    reader = easyocr.Reader(["en"], gpu=True)
    result = reader.readtext(image_path, detail=0)

    print("\n--- EXTRACTED CONTEXT ---")
    print("\n".join(result))
    print("-------------------------\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_ocr(sys.argv[1])
    else:
        print("Please provide an image path.")
