#!/bin/bash

user=$1;
problem=$2;
filename=${problem}_${user};
problem_dir=$CG_FILES_UPLOADED/$user/$problem;

# Remove all files from container and then stop it.
docker exec -i lidi_container_${user} /bin/bash -c "rm -r /lidi_files/out/* /lidi_files/prog/* /lidi_files/testcases/*;";
docker stop lidi_container_${user};

err_rep=$(cat $problem_dir/errors);
if [ "$err_rep" != "0 0 0 0 0 0 0 0 0 0" ]
then
    echo "RTE";
    docker stop lidi_container_${user};
    exit 0;
fi;

grade=0;

# Compare the outputs of program to solutions.
for i in 0 1 2 3 4 5 6 7 8 9
do
    cmp --silent $problem_dir/out_${filename}_${i} \
        $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((grade++));
done;

echo $grade;