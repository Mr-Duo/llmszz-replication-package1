import os

# enter your current working directory, absolute path.
# CWD = "/data/scratch/projects/punim1928/HUST/thesyx/llmszz-replication-package1"
# enter your directory which saves all repos
# REPOS_DIR = "/data/scratch/projects/punim1928/HUST/thesyx"

# Get working directory from environment variable or use current directory
CWD = os.environ.get("LLM4SZZ_CWD", os.getcwd())
# Get repositories directory from environment variable
REPOS_DIR = os.environ.get("LLM4SZZ_REPOS_DIR", "")

DATASET_DIR = os.path.join(CWD,'dataset')
SAVE_LOG_DIR = os.path.join(CWD,'save_logs')
TMP_DIR = os.path.join(CWD,'tmp_dir') 
TREE_SITTER_DIR = os.path.join(CWD,'build')

# Create required directories if they don't exist
for directory in [DATASET_DIR, SAVE_LOG_DIR, TMP_DIR, TREE_SITTER_DIR]:
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

# Print configuration for debugging
print(f"📁 Working Directory: {CWD}")
if REPOS_DIR:
    print(f"📦 Repositories Directory: {REPOS_DIR}")
else:
    print("⚠️  REPOS_DIR not set. Set LLM4SZZ_REPOS_DIR environment variable.")

