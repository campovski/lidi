# Main directory for all files.
CG_FILES_DIR=$1/lidi_files;

# Directory with problem tasks.
CG_FILES_PROBLEMS=$CG_FILES_DIR/problems;

# Directory with uploaded problems that need to be revised.
CG_FILES_PROBLEMS_TMP=$CG_FILES_PROBLEMS/tmp;

# Directory with testcases for problems. Each time a new
# problem is submitted, create subdirectory for that problem
# with its problem_id.
CG_FILES_TESTCASES=$CG_FILES_DIR/testcases;

# Directory with solutions to testcases. The same directory
# structure as in $CG_FILES_TESTCASES.
CG_FILES_TESTCASES_SOL=$CG_FILES_TESTCASES/solutions;

# Directory with users subdirectories. In each user subdirectory
# there are subdirectories for each problem. After uploading,
# firejail the execution to only that certain subdirectory.
CG_FILES_SOLUTIONS=$CG_FILES_DIR/solutions;

# Directory where uploaded programs go. Then they get copied to
# CG_FILES_SOLUTION/user and executed.
CG_FILES_UPLOADED=$CG_FILES_DIR/uploaded;

export CG_FILES_DIR;
export CG_FILES_PROBLEMS;
export CG_FILES_PROBLEMS_TMP;
export CG_FILES_TESTCASES;
export CG_FILES_TESTCASES_SOL;
export CG_FILES_SOLUTIONS;
export CG_FILES_UPLOADED;
