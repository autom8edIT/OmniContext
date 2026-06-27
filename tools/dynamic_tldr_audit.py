import os
import json
import urllib.request
import hashlib
import argparse
from collections import defaultdict

# --- Configuration ---
API_URL = "http://127.0.0.1:8080/v1/chat/completions"
DEFAULT_CHUNK_SIZE = 6000
DEFAULT_OVERLAP = 500

def get_file_hash(filepath):
    """Returns MD5 hash for exact duplication checking."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception:
        return None

def query_llm(system_prompt, user_prompt, temperature=0.1):
    """Handles LLM communication."""
    data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": 2048
    }
    req = urllib.request.Request(API_URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res_body = response.read()
            return json.loads(res_body.decode('utf-8'))['choices'][0]['message']['content']
    except Exception as e:
        return f"[Error querying LLM: {e}]"

def chunk_text(text, chunk_size, overlap):
    """Splits text into overlapping chunks to preserve boundary context."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += (chunk_size - overlap)
    return chunks

def process_file_map_reduce(filepath, scenario, chunk_size, overlap):
    """Phase 1 & 2: Chunk a file, map scenario onto chunks, reduce to one summary."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
    except Exception as e:
        return f"Could not read file: {e}"
        
    if not content:
        return None

    # MAP phase
    chunks = chunk_text(content, chunk_size, overlap)
    chunk_summaries = []
    
    system_map = "You are a precise data extraction agent. Extract facts matching the user's scenario. Be concise."
    
    print(f"  -> Mapping {len(chunks)} chunk(s) for {os.path.basename(filepath)}...")
    for i, chunk in enumerate(chunks):
        prompt = f"SCENARIO TO EVALUATE: {scenario}\n\nCHUNk {i+1}/{len(chunks)}:\n```\n{chunk}\n```\n\nExtract relevant information based ONLY on the scenario above."
        summary = query_llm(system_map, prompt)
        chunk_summaries.append(f"--- Chunk {i+1} ---\n{summary}")

    if len(chunks) == 1:
        return chunk_summaries[0]

    # REDUCE phase (File Level)
    print(f"  -> Reducing chunks into single file summary...")
    system_reduce = "You are an expert technical editor. Combine these fragmented extracts into a single, cohesive file summary."
    reduce_prompt = f"SCENARIO: {scenario}\n\nCOMBINE THESE EXTRACTS:\n" + "\n".join(chunk_summaries)
    file_summary = query_llm(system_reduce, reduce_prompt)
    
    return file_summary

def main():
    parser = argparse.ArgumentParser(description="Map-Reduce-Validate Directory Auditor")
    parser.add_argument("--dir", type=str, required=True, help="Target directory to audit")
    parser.add_argument("--scenario", type=str, required=True, help="What do you want to extract? (e.g., 'Find all DB connection logic')")
    parser.add_argument("--out", type=str, default="audit_report.md", help="Output Markdown report file")
    args = parser.parse_args()

    TARGET_DIR = args.dir
    SCENARIO = args.scenario
    LOG_FILE = args.out

    if not os.path.exists(TARGET_DIR):
        print(f"Directory {TARGET_DIR} not found.")
        return

    print(f"Phase 0: Scanning & Deduplicating {TARGET_DIR}...")
    files_by_name = defaultdict(list)
    exact_duplicates = defaultdict(list)
    
    for root, _, files in os.walk(TARGET_DIR):
        if any(ignored in root for ignored in ['.git', 'node_modules', '__pycache__']):
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.exe', '.dll', '.png', '.jpg', '.jpeg', '.zip', '.tar', '.gz', '.mp4', '.pdf', '.bin']:
                continue
                
            path = os.path.join(root, file)
            # Skip massive files to avoid accidental infinite loops
            try:
                if os.path.getsize(path) > 500000: # 500KB cap
                    continue
            except: pass
            
            files_by_name[file].append(path)
            h = get_file_hash(path)
            if h:
                exact_duplicates[h].append(path)

    processed_hashes = set()
    global_summaries = []

    print("\nPhase 1 & 2: Map & Reduce (Extracting Context)...")
    for name, paths in files_by_name.items():
        # Version grouping: process newest only
        if len(paths) > 1:
            paths.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            target_path = paths[0]
        else:
            target_path = paths[0]
            
        h = get_file_hash(target_path)
        if h in processed_hashes:
            continue
        processed_hashes.add(h)
        
        file_summary = process_file_map_reduce(target_path, SCENARIO, DEFAULT_CHUNK_SIZE, DEFAULT_OVERLAP)
        if file_summary:
            global_summaries.append(f"### File: {target_path}\n{file_summary}\n")

    print("\nPhase 2b: Global Reduction (Synthesizing Report)...")
    system_global = "You are a Lead AI Architect. Synthesize the provided file summaries into a comprehensive global report."
    global_prompt = f"SCENARIO TO SATISFY: {SCENARIO}\n\nFILE REPORTS:\n" + "\n".join(global_summaries)
    global_report = query_llm(system_global, global_prompt)

    print("\nPhase 3: Validation (Self-Check)...")
    system_validate = "You are a strict QA Agent. Evaluate the provided report against the user's intent."
    validate_prompt = f"USER SCENARIO: {SCENARIO}\n\nGENERATED REPORT:\n{global_report}\n\nTASK: Did the report successfully fulfill the user's scenario? What is missing or hallucinatory? Give a short, brutal verdict."
    validation_verdict = query_llm(system_validate, validate_prompt)

    print(f"\nWriting final report to {LOG_FILE}...")
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Dynamic Directory Audit\n**Target:** {TARGET_DIR}\n**Scenario:** {SCENARIO}\n\n")
        f.write("## 1. Global Synthesis\n")
        f.write(global_report + "\n\n")
        f.write("## 2. QA Validation Verdict\n")
        f.write(validation_verdict + "\n\n")
        f.write("## 3. Individual File Extracts\n")
        for s in global_summaries:
            f.write(s + "\n")

    print("Pipeline Complete!")

if __name__ == '__main__':
    main()