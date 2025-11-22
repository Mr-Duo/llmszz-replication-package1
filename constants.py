import os

# enter your current working directory, absolute path.
# CWD = "/data/scratch/projects/punim1928/HUST/thesyx/llmszz-replication-package1"
CWD = ""
# enter your directory which saves all repos
# REPOS_DIR = "/data/scratch/projects/punim1928/HUST/thesyx"
REPOS_DIR = ""

DATASET_DIR = os.path.join(CWD,'dataset')
SAVE_LOG_DIR = os.path.join(CWD,'save_logs')
TMP_DIR = os.path.join(CWD,'tmp_dir') 
TREE_SITTER_DIR = os.path.join(CWD,'build')

