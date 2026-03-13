
# Replication Package
This directory contains the source code, logs generated during execution, and the dataset for our paper "LLM4SZZ: Enhancing the SZZ Algorithm with Context-Enhanced Assessment on Large Language Models," submitted to ISSTA 2025.

## Directories
1.**dataset**: This directory includes the datasets referenced in the paper. The three files correspond to DS_LINUX, DS_APACHE, and DS_GITHUB, respectively. Additionally, a combined dataset comprising all three is available.

2.**save_logs**: This directory contains the logs produced by the LLM.

3.**tmp_dir**: This directory is used to store temporary results during execution.

4.**build**: This directory contains the dependencies built with tree-sitter.

## Files
**_constants.py_**: This file includes constants that must be set before execution, such as the directory containing the repositories.

**_prompts.py_**: This file contains all prompts utilized in the experiments.

**_llm.py_**: This file contains the code for calling the LLM.

**_parse_patch.py_**: This file contains the code for parsing a patch, including the extraction of deleted and added lines.

**_util.py_**: This file includes various utility functions, such as retrieving file content, extracting functions from files, and generating line maps between two versions.

## Environment
Install all packages listed in environment.yml for the Python environment.

## VIC Discovery with `llm4szz_vic.py`
`llm4szz_vic.py` is the pipeline for finding vulnerability-introducing commits (VICs) from a list of vulnerability-fixing commits (VFCs).

### 1. Required setup
1. Install dependencies from `environment.yml`.
2. Clone target repositories into one parent directory.
3. Configure paths using environment variables (recommended):
	 - `LLM4SZZ_CWD`: project root directory.
	 - `LLM4SZZ_REPOS_DIR`: directory that contains cloned repos.
4. Set OpenAI key with `OPENAI_API_KEY` (or `.env`/Kaggle secret).

Example (PowerShell):

```powershell
$env:LLM4SZZ_CWD="C:\Users\minhq\Documents\GitHub\llmszz-replication-package1"
$env:LLM4SZZ_REPOS_DIR="D:\repos"
$env:OPENAI_API_KEY="<your_api_key>"
```

### 2. Input dataset format
`llm4szz_vic.py` expects a JSON array in `dataset/` where each element includes:

```json
[
	{
		"repo_name": "openssl",
		"fix_commit_hash": "<fix_commit_sha>",
		"bug_inducing_commit": []
	}
]
```

Notes:
- `repo_name` must match a folder name under `LLM4SZZ_REPOS_DIR`.
- If your VFC source is JSONL, use `convert_vfc_to_dataset.py` first.

### 3. Run `llm4szz_vic.py`
Use one of these options:

```powershell
python llm4szz_vic.py <dataset_file_name_in_dataset_dir>.json
```

or

```powershell
$env:VFC_DATASET_FILE="<dataset_file_name_in_dataset_dir>.json"
python llm4szz_vic.py
```

### 4. Outputs
After execution:
- `vic_results.json`: VFC to VIC predictions summary.
- `file_statistics.json`: token/time/call statistics.
- `deal_infos.json`, `err_infos.json`: progress and error records.
- `save_logs/`: detailed per-commit logs.

Optional formatting:

```powershell
python reformat_vic_results.py vic_results.json
```

### 5. Change model (not using `gpt-4o-mini`)
Edit `llm.py` in `Client.call_llm`:

```python
completion = client.chat.completions.create(
		model="gpt-4o-mini",
		messages=all_msgs,
		temperature=0.0,
)
```

Replace `"gpt-4o-mini"` with your target model (for example `"gpt-4o"` or another supported OpenAI model).

Also review:
- Tokenizer line in `llm.py`: `tiktoken.encoding_for_model("gpt-4o")`.
- Cost estimate in `llm4szz_vic.py` (currently based on GPT-4o-mini pricing).



