"""
Reformat VIC results JSON to JSONL format (one JSON object per line).

Input: vic_results.json with format:
  [{"vfc": "abc123", "vic": ["def456"], "repo": "openssl", "iteration": 0}, ...]

Output: vic_results_formatted.jsonl with format:
  {"vfc_commit_id": "abc123", "vic_commit_id": "def456"}
  {"vfc_commit_id": "abc123", "vic_commit_id": "ghi789"}
  ...

- One JSON object per line (JSONL format)
- One line per VFC-VIC pair
- Removes duplicate VFC commit IDs (keeps first occurrence)
- Handles multiple VICs per VFC
- Handles empty VIC lists
"""

import json
import sys
import os

def reformat_vic_results(input_file, output_file=None):
    """
    Reformat VIC results from JSON array to JSONL format.
    
    Args:
        input_file: Path to input JSON file
        output_file: Path to output JSONL file (optional, auto-generated if not provided)
    """
    # Auto-generate output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_formatted.jsonl"
    
    # Load the JSON data
    print(f"Loading: {input_file}")
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    print(f"Total entries: {len(data)}")
    
    # Track VFCs we've already seen
    seen_vfcs = set()
    output_lines = []
    duplicate_count = 0
    empty_vic_count = 0
    
    for entry in data:
        vfc = entry['vfc']
        vic_list = entry.get('vic', [])
        
        # Skip if we've already processed this VFC
        if vfc in seen_vfcs:
            duplicate_count += 1
            continue
        
        # Mark this VFC as seen
        seen_vfcs.add(vfc)
        
        # Handle empty VIC lists
        if not vic_list or len(vic_list) == 0:
            empty_vic_count += 1
            continue
        
        # Create one JSON object per VIC
        for vic in vic_list:
            json_obj = {
                "vfc_commit_id": vfc,
                "vic_commit_id": vic
            }
            output_lines.append(json.dumps(json_obj))
    
    # Write to output file (JSONL format - one JSON per line)
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))
    
    # Print statistics
    print(f"\n{'='*60}")
    print(f"REFORMATTING COMPLETE")
    print(f"{'='*60}")
    print(f"Unique VFCs processed: {len(seen_vfcs)}")
    print(f"VFC-VIC pairs written: {len(output_lines)}")
    print(f"Duplicate VFCs skipped: {duplicate_count}")
    print(f"Empty VIC lists skipped: {empty_vic_count}")
    print(f"Output saved to: {output_file}")
    print(f"{'='*60}\n")
    
    return output_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reformat_vic_results.py <input_json_file> [output_jsonl_file]")
        print("\nExample:")
        print("  python reformat_vic_results.py vic_results.json")
        print("  python reformat_vic_results.py vic_results.json vic_output.jsonl")
        print("  python reformat_vic_results.py vic_dev_web_results.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    reformat_vic_results(input_file, output_file)
