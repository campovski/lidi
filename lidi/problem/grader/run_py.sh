#!/bin/bash

# Run the program with testcases and save the output of program.

user=$1;
problem=$2;
filename=${problem}_${user};
file=${filename}.py;
problem_dir=$CG_FILES_UPLOADED/$user/$problem;

for i in 0 1 2 3 4 5 6 7 8 9
do
    cmd_to_exec="{ time python /lidi_files/prog/${file} < /lidi_files/testcases/${problem}_${i}; } 2>> /lidi_files/out/time;";
	docker exec -t lidi_container_${user} /bin/bash -c "${cmd_to_exec}" > ${problem_dir}/out_${filename}_${i};
	errors[$i]=$?;
	dos2unix ${problem_dir}/out_${filename}_${i};
done;

# Copy time file to host.
docker cp lidi_container_${user}:/lidi_files/out/time $problem_dir/time;

echo ${errors[*]} > $problem_dir/errors;
exit 0;