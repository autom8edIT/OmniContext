# Skill: Dynamic TLDR Pipeline (Map-Reduce & Validate)

**Description:** 
A methodology for AI agents to process massive datasets, repositories, and logs to extract specific insights without losing context or hallucinating due to truncation. This skill defines a Map-Reduce pipeline combined with a self-validation mechanism.

## When to use this skill
- Processing directories with >100k characters of code or text.
- Generating a "TLDR" or extracting specific scenarios from massive logs (e.g., "Find all database connection logic").
- When a user asks an agent to audit, review, or summarize a massive codebase or folder that exceeds context windows.

## The Architecture & Workflow

### Phase 0: Pre-processing (Filter & Deduplicate)
Never blindly read every file. 
1. **Exclude Binaries & Junk:** Skip known compiled/media formats (`.exe`, `.dll`, `.png`, `.jpg`, `.mp4`, `.pdf`, etc.) and system/junk folders (`.git`, `node_modules`, `__pycache__`).
2. **File Hashing (Deduplication):** Compute an MD5/SHA256 hash of each file. If multiple files have the exact same hash, process it only once to save tokens and time. 
3. **Version Grouping:** If multiple files share the exact same name but different hashes (e.g., historical backups), group them, sort by modified time, and only process the most recent file.

### Phase 1: MAP (Chunk & Extract)
When processing the filtered files, traditional methods truncate the file, losing data.
1. **Chunking:** Split the remaining text into discrete chunks (e.g., 5,000 characters).
2. **Overlap:** Ensure each chunk overlaps the previous one by a margin (e.g., 500 chars) so context isn't lost if a crucial sentence is split across a boundary.
3. **Extraction:** Query the LLM for *each chunk* independently, providing the user's specific **Scenario Constraint** (e.g., *"Extract security vulnerabilities"*). 

### Phase 2: REDUCE (Synthesize)
Combine the disparate insights into a global document.
1. **File-level Reduction:** Take all chunk summaries for a single file and ask the LLM to aggregate them into one cohesive file summary.
2. **Global Reduction:** Take all file-level summaries and ask the LLM to synthesize a master report for the entire directory based on the Scenario Constraint.

### Phase 3: VALIDATE (Agentic Self-Correction)
Never assume the output is perfect. 
1. Provide the LLM with the final Master Summary AND the original **Scenario Constraint**.
2. Ask: *"Review this summary against the original requirement. Did we miss anything? Does this faithfully answer the prompt?"*
3. Append this validation check to the final output, providing a confidence score or highlighting potential blind spots.

## Implementation Details
This methodology is implemented in the `dynamic_tldr_audit.py` script. The script takes arguments for target directory and scenario constraints, executing this pipeline automatically.
