#!/bin/bash

# Run the program with testcases and save the output of program.

user=$1;
problem=$2;
filename=${problem}_${user};
main_class=$(cat $problem_dir/${filename}_main_class);
problem_dir=$CG_FILES_UPLOADED/$user/$problem;

limit_t=$(cat $CG_FILES_PROBLEMS/$problem/limit_t);
limit_m=$(cat $CG_FILES_PROBLEMS/$problem/limit_m);

cmd_to_exec="/usr/local/bin/timeout -t ${limit_t} -m ${limit_m} bash /lidi_files/runners/run_java.sh ${1} ${2} ${main_class} 2> /lidi_files/out/timeout;";
docker exec -t lidi_container_${user} /bin/bash -c "${cmd_to_exec}";

rm $main_class;
exit 0;
