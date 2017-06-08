#!/bin/bash

# Run the program with testcases and save the output of program.

user=$1;
problem=$2;
filename=$3;
file=$4;
problem_dir=$CG_FILES_UPLOADED/$user/$problem;

for i in 0 1 2 3 4 5 6 7 8 9
do
	{ time mono $problem_dir/${filename}.exe < $CG_FILES_TESTCASES/$problem/${problem}_${i} > $problem_dir/out_${filename}_${i}; } 2>> $problem_dir/time;
	errors[$i]=$?;
done;

echo ${errors[*]} > $problem_dir/errors;
