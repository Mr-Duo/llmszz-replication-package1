
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

**_llm4szz.py_**: This file implements the llm4szz, records the outputs of the LLM, and saves them.

**_llm4szz_c.py_, _llm4szz_h.py_, _llm4szz_r.py_, _llm4szz_raw.py_, _llm4szz_re.py_**: These files implement the variants of llm4szz, corresponding to RQ2.

## Environment
Install all packages listed in environment.yml for the Python environment.

## How to Get the Results
First, set your current working directory and specify the directories to save repositories in **constants.py**.

Next, enter your API key in **llm.py**.

### RQ1:
To replicate our results for RQ1:
``` py
python llm4szz.py

python cal_statistics.py
```

### RQ2
To replicate our results for RQ2:
```py
python llm4szz_c.py

python llm4szz_h.py

python llm4szz_r.py

python llm4szz_raw.py

python llm4szz_re.py

python cal_statistics.py
```

### RQ3
To replicate our results for RQ3:

simply change the pipeline variable in the files and replace the LLM with llama3-8b and llama3-70b, then:
```py
python llm4szz.py

python cal_statistics.py
```

### disscussion
To replicate our results for disscussion:

adjust the dataset to DS_LINUX_EXTEND and DS_GITHUB_EXTEND in **llm4szz.py**, then:

```py
python llm4szz.py

python diss.py
```

#### Generating Results from Existing Logs
To obtain the results from saved files for RQs:

```py
python cal_statistics.py
```

To obtain the results from saved files for disscussions:

```py
python diss.py
```

