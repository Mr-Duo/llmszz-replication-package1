import json
import os
import glob

# Configuration - Choose one of the following modes:

# MODE 1: Convert a single VFC file
SINGLE_FILE_MODE = False
VFC_JSONL_FILE = "dataset/VFC/vfc_cvefixes.jsonl"  # Path to your VFC JSONL file
REPO_NAME = "openssl"  # e.g., "linux", "FFmpeg", "openssl", etc.
OUTPUT_FILE = "dataset/vfc_dataset.json"

# MODE 2: Convert all VFC files in the VFC folder (creates separate output files)
BATCH_MODE = True
VFC_FOLDER = "dataset/VFC"
BATCH_OUTPUT_FOLDER = "dataset"  # Output folder for converted files

def convert_vfc_to_dataset(vfc_file, repo_name, output_file):
    """
    Convert VFC JSONL file to llm4szz expected format.
    
    Handles multiple input formats:
    1. {"commit_id": "abc123", "branch": "master"}
    2. {"commit_id": "abc123", "cve_id": "CVE-2015-1792", "project": "openssl"}
    3. {"commit_id": "abc123", "Repository": "openssl"}
    
    Output format (JSON array):
        [{"repo_name": "...", "fix_commit_hash": "abc123", "bug_inducing_commit": []}]
    """
    dataset = []
    
    print(f"Reading VFC file: {vfc_file}")
    with open(vfc_file, "r", encoding="utf-8") as f:
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
                
                # Auto-detect repository name from entry if available
                detected_repo = entry.get("project") or entry.get("Repository") or entry.get("repo_name") or repo_name
                
                # Extract additional metadata if available
                metadata = {
                    "repo_name": detected_repo,
                    "fix_commit_hash": commit_id,
                    "bug_inducing_commit": []  # Unknown - will be found by LLM4SZZ
                }
                
                # Add optional fields if present
                if "cve_id" in entry:
                    metadata["cve_id"] = entry["cve_id"]
                if "cwe_id" in entry:
                    metadata["cwe_id"] = entry["cwe_id"]
                if "branch" in entry:
                    metadata["branch"] = entry["branch"]
                
                dataset.append(metadata)
                
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
                continue
    
    print(f"Processed {len(dataset)} commits")
    
    # Save to output file
    output_dir = os.path.dirname(output_file)
    if output_dir:  # Only create directory if there's a directory component
        os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Dataset saved to: {output_file}")
    return dataset

def convert_all_vfc_files(vfc_folder, output_folder="dataset"):
    """
    Convert all VFC JSONL files in a folder to separate dataset files.
    Each input file gets its own output file.
    """
    file_stats = {}
    output_files = []
    
    # Find all JSONL files in the VFC folder
    vfc_files = glob.glob(os.path.join(vfc_folder, "*.jsonl"))
    
    if not vfc_files:
        print(f"No JSONL files found in {vfc_folder}")
        return
    
    print(f"Found {len(vfc_files)} VFC files to process:")
    for vfc_file in vfc_files:
        print(f"  - {os.path.basename(vfc_file)}")
    
    print("\nProcessing files...")
    print("=" * 60)
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    for vfc_file in vfc_files:
        filename = os.path.basename(vfc_file)
        print(f"\n[{filename}]")
        
        # Create output file for each input file
        output_filename = filename.replace('.jsonl', '_dataset.json')
        output_path = os.path.join(output_folder, output_filename)
        
        # Convert with auto-detection of repo name
        dataset = convert_vfc_to_dataset(vfc_file, "openssl", output_path)
        
        # Track statistics
        repos = set(entry["repo_name"] for entry in dataset)
        file_stats[filename] = {
            "commits": len(dataset),
            "repos": list(repos),
            "output_file": output_path
        }
        
        output_files.append(output_path)
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    total_commits = 0
    all_repos = set()
    
    for filename, stats in file_stats.items():
        print(f"\n{filename}:")
        print(f"  Commits: {stats['commits']}")
        print(f"  Repositories: {', '.join(stats['repos'])}")
        print(f"  Output: {stats['output_file']}")
        total_commits += stats['commits']
        all_repos.update(stats['repos'])
    
    print(f"\n{'=' * 60}")
    print(f"Total files processed: {len(file_stats)}")
    print(f"Total commits: {total_commits}")
    print(f"All repositories: {', '.join(sorted(all_repos))}")
    
    print(f"\n{'=' * 60}")
    print("OUTPUT FILES CREATED:")
    print("=" * 60)
    for output_file in output_files:
        print(f"  {output_file}")
    
    print("\nNext steps:")
    print("1. Update constants.py with your repository path")
    print("2. Update llm.py with your OpenAI API key")
    print(f"3. Ensure all repositories ({', '.join(sorted(all_repos))}) are cloned in REPOS_DIR")
    print(f"4. Choose which dataset file to use and update llm4szz_vic.py VFC_DATASET_FILE")
    print(f"   Example: VFC_DATASET_FILE = '{os.path.basename(output_files[0])}'")
    print(f"5. Run: python llm4szz_vic.py")

if __name__ == "__main__":
    if BATCH_MODE:
        # Process all VFC files in the folder - creates separate output files
        convert_all_vfc_files(VFC_FOLDER, BATCH_OUTPUT_FOLDER)
    elif SINGLE_FILE_MODE:
        # Process a single VFC file
        if not VFC_JSONL_FILE or VFC_JSONL_FILE == "":
            print("ERROR: Please set VFC_JSONL_FILE to your VFC JSONL file path")
        else:
            convert_vfc_to_dataset(VFC_JSONL_FILE, REPO_NAME, OUTPUT_FILE)
            print("\nNext steps:")
            print("1. Update constants.py with your repository path")
            print("2. Update llm.py with your OpenAI API key")
            print(f"3. Ensure the repository '{REPO_NAME}' is cloned in REPOS_DIR")
            print(f"4. Run: python llm4szz_vic.py")
    else:
        print("ERROR: Please enable either SINGLE_FILE_MODE or BATCH_MODE")
        print("\nTo process a single file:")
        print("  Set SINGLE_FILE_MODE = True")
        print("  Set VFC_JSONL_FILE to your file path")
        print("  Set REPO_NAME to your repository name")
        print("\nTo process all files in VFC folder:")
        print("  Set BATCH_MODE = True")
