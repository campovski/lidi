#!/bin/bash

user=$1;
problem=$2;
filename=${problem}_${user};
problem_dir=$CG_FILES_UPLOADED/$user/$problem;

# Copy result of timeout to host.
docker cp lidi_container_${user}:/lidi_files/out/timeout $problem_dir/timeout;

# Check for TLE or memory exceeded.
timeout_output=$(cat $problem_dir/timeout | awk '{print $1; exit;}');
if [ "$timeout_output" != "FINISHED" ]
then
    echo $timeout_output;
    exit 0;
fi;

# Copy outputs to host.
for i in 0 1 2 3 4 5 6 7 8 9
do
    docker cp lidi_container_${user}:/lidi_files/out/out_${filename}_${i} $problem_dir/out_${filename}_${i};
done;

# Copy time and error files to host.
docker cp lidi_container_${user}:/lidi_files/out/time $problem_dir/time;
docker cp lidi_container_${user}:/lidi_files/out/errors $problem_dir/errors;

# Remove all files from container and then stop it.
docker exec -i lidi_container_${user} /bin/bash -c "rm -rf /lidi_files/out/* /lidi_files/prog/* /lidi_files/testcases/*;";
docker stop lidi_container_${user};

err_rep=$(cat $problem_dir/errors);
if [ "$err_rep" != "0 0 0 0 0 0 0 0 0 0" ]
then
    echo "RTE";
    exit 1;
fi;

grade=0;

# Compare the outputs of program to solutions.
for i in 0 1 2 3 4 5 6 7 8 9
do
    dos2unix ${problem_dir}/out_${filename}_${i};
    cmp --silent $problem_dir/out_${filename}_${i} \
        $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((grade++));
done;

echo $grade;