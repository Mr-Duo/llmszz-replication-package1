import json
import os

# Configuration
VFC_JSONL_FILE = "C:\\Users\\minhq\\Downloads\\vfc_cvefixes.jsonl"  # Path to your VFC JSONL file
REPO_NAME = "cve"  # e.g., "linux", "FFmpeg", "openssl", etc.
OUTPUT_FILE = "dataset/vfc_dataset.json"

def convert_vfc_to_dataset(vfc_file, repo_name, output_file):
    """
    Convert VFC JSONL file to llm4szz expected format.
    
    Input format (JSONL):
        {"commit_id": "abc123", "branch": "master"}
    
    Output format (JSON array):
        [{"repo_name": "...", "fix_commit_hash": "abc123", "bug_inducing_commit": []}]
    """
    dataset = []
    
    print(f"Reading VFC file: {vfc_file}")
    with open(vfc_file, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                entry = json.loads(line)
                commit_id = entry.get("commit_id")
                
                if not commit_id:
                    print(f"Warning: Line {line_num} missing 'commit_id', skipping")
                    continue
                
                dataset.append({
                    "repo_name": repo_name,
                    "fix_commit_hash": commit_id,
                    "bug_inducing_commit": []  # Unknown - will be found by LLM4SZZ
                })
                
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
                continue
    
    print(f"Processed {len(dataset)} commits")
    
    # Save to output file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Dataset saved to: {output_file}")
    print(f"\nNext steps:")
    print(f"1. Update constants.py with your repository path")
    print(f"2. Update llm.py with your OpenAI API key")
    print(f"3. Ensure the repository '{repo_name}' is cloned in REPOS_DIR")
    print(f"4. Modify llm4szz.py to use '{os.path.basename(output_file)}'")
    print(f"5. Run: python llm4szz.py")

if __name__ == "__main__":
    # Update these values before running
    if VFC_JSONL_FILE == "your_vfc_file.jsonl":
        print("ERROR: Please update the configuration variables in this script:")
        print("  - VFC_JSONL_FILE: Path to your VFC JSONL file")
        print("  - REPO_NAME: Name of the repository (must match folder in REPOS_DIR)")
        print("  - OUTPUT_FILE: Where to save the converted dataset (optional)")
    else:
        convert_vfc_to_dataset(VFC_JSONL_FILE, REPO_NAME, OUTPUT_FILE)
