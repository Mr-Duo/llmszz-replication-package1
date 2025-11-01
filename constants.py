import os

# enter your current working directory, absolute path.
CWD = "C:\\Users\\minhq\\Documents\\GitHub\\llmszz-replication-package1"
# enter your directory which saves all repos
REPOS_DIR = "C:\\Users\\minhq\\Documents\\GitHub"

DATASET_DIR = os.path.join(CWD,'dataset')
SAVE_LOG_DIR = os.path.join(CWD,'save_logs')
TMP_DIR = os.path.join(CWD,'tmp_dir') 
TREE_SITTER_DIR = os.path.join(CWD,'build')

