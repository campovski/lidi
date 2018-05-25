#!/bin/bash

# This script compiles a program if necessary and copies files to docker container.


file=$1;
problem=$2;
user=$3;
filename=${problem}/${user};
end="${file##*.}";

problem_dir=$CG_FILES_UPLOADED/$user/$problem;

limit_m=$(cat $CG_FILES_PROBLEMS/$problem/limit_m);
limit_t=$(cat $CG_FILES_PROBLEMS/$problem/limit_t);

# Start user's docker container and copy testcases into it.
docker start lidi_container_${user};
docker cp $CG_FILES_TESTCASES/$problem/. lidi_container_${user}:/lidi_files/testcases/;

case $end in
    c)
        # Compile the program.
        gcc -o $problem_dir/$filename $problem_dir/$file;
        if [ $? -gt 0 ]
        then
            echo "RTE";
            docker stop lidi_container_${user};
            exit 0;
        fi;

        # Copy program to docker container.
        docker cp $problem_dir/$filename lidi_container_${user}:/lidi_files/prog/$filename;;

    cpp)
        # Compile the program.
        g++ -o $problem_dir/$filename $problem_dir/$file;
        if [ $? -gt 0 ]
        then
            echo "RTE";
            docker stop lidi_container_${user};
            exit 0;
        fi;

        # Copy program to docker container.
        docker cp $problem_dir/$filename lidi_container_${user}:/lidi_files/prog/$filename;;

    py)
        #TODO Memory limit.
        # Copy program to docker container.
        docker cp $problem_dir/$file lidi_container_${user}:/lidi_files/prog/$file;;

    pas)
        # Compile the program.
        fpc $problem_dir/$file;
        if [ $? -gt 0 ]
        then
            echo "RTE";
            docker stop lidi_container_${user};
            exit 0;
        fi;
        rm $problem_dir/${filename}.o;

        # Copy program to docker container.
        docker cp $problem_dir/$filename lidi_container_${user}:/lidi_files/prog/$filename;;

    f)
        # Compile the program.
        f77 $problem_dir/$file -o $problem_dir/$filename;
        if [ $? -gt 0 ]
        then
            echo "RTE";
            docker stop lidi_container_${user};
            exit 0;
        fi;

        # Copy program to docker container.
        docker cp $problem_dir/$filename lidi_container_${user}:/lidi_files/prog/$filename;;

    java)
        # Compile the program.
        javac $problem_dir/$file;
        if [ $? -gt 0 ]
        then
            echo "RTE";
            docker stop lidi_container_${user};
            exit 0;
        fi;

        # Find main class.
        awk '/class/ {print $2}' $problem_dir/$file > $problem_dir/${filename}_classes;
        head $problem_dir/${filename}_classes > $problem_dir/${filename}_main_class;
        rm -f $problem_dir/${filename}_classes;

        # Copy all files produced by javac to docker container.
        docker cp $problem_dir/. lidi_container_${user}/prog/;;

    cs)
        # Compile the program.
        mcs -out:$problem_dir/${filename}.exe $problem_dir/$file;
        if [ $? -gt 0 ]
        then
            echo "RTE";
            docker stop lidi_container_${user};
            exit 0;
        fi;

        # Copy program to docker container.
        docker cp $problem_dir/$filename lidi_container_${user}:/lidi_files/prog/$filename;;

    *)
        echo "ERROR";
        docker stop lidi_container_${user};
        exit 1;;
esac;
echo "OK";
exit 0;