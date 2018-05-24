#!/bin/bash

# This script compiles a program if necessary. It then runs the grader.
# This is new verions of grader, the one that uses docker.

file=$1;
end="${file##*.}";
filename="${file%.*}";
problem="${filename%_*}";
user="${filename#*_}";
proglang=$2;

problem_dir=$CG_FILES_UPLOADED/$user/$problem;

limit_m=$(cat $CG_FILES_PROBLEMS/$problem/limit_m);
limit_t=$(cat $CG_FILES_PROBLEMS/$problem/limit_t);
echo $limit_m;
echo $limit_t;

grade=0;

# Start user's docker container and copy testcases into it.
docker start lidi_container_${user};
docker cp $CG_FILES_TESTCASES/$problem/. lidi_container_${user}:/lidi_files/testcases/;

case $end in
	c)
		# Disable some functions.
#		echo -e "#define execl \"\"\n#define system \"\"\n#define exec \"\"\n#define execv \"\"\n#define getenv \"\"\n#define getcwd \"\"\n$(cat $problem_dir/$file)" > $problem_dir/$file;

		# Compile the program.
		gcc -o $problem_dir/$filename $problem_dir/$file;
		if [ $? -gt 0 ]
		then
			echo "RTE";
			docker stop lidi_container_${user};
			exit 0;
		fi;

		# Copy program to docker container.
		docker cp $problem_dir/$filename lidi_container_${user}:/lidi_files/prog/$filename;

		# Run the program on limited memory and time.
		#TODO Memory limit.
		timeout $limit_t bash problem/bash/test_docker/grade_c.sh $user $problem $filename $file;
		timeout_error=$?;;

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
		docker cp $problem_dir/$filename lidi_container_${user}:/lidi_files/prog/$filename;

		# Run the program on limited memory and time.
		#TODO Memory limit.
		timeout $limit_t sudo bash problem/bash/test_docker/grade_c.sh $user $problem $filename $file;
		timeout_error=$?;;

	py)
		#TODO Memory limit.
		# Copy program to docker container.
		echo "Copying program to container...";
		docker cp $problem_dir/$file lidi_container_${user}:/lidi_files/prog/$file;
		echo "Done! Python version = $3";

        echo $user $problem $filename $file;
		if [ "$3" == "2" ]
		then
			timeout $limit_t bash problem/bash/test_docker/grade_py.sh $user $problem $filename $file;
			timeout_error=$?;
		else
			timeout $limit_t bash problem/bash/test_docker/grade_py3.sh $user $problem $filename $file;
			timeout_error=$?;
		fi;

		# Check for RTE.
		err_rep=$(cat $problem_dir/errors);
		if [ "$err_rep" != "0 0 0 0 0 0 0 0 0 0" ]
		then
			echo "RTE";
			docker stop lidi_container_${user};
			exit 0;
		fi;;

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
		docker cp $problem_dir/$filename lidi_container_${user}:/lidi_files/prog/$filename;

		# Run the program on limited memory and time.
		#TODO Memory limit.
		timeout $limit_t bash problem/bash/test_docker/grade_c.sh $user $problem $filename $file;
		timeout_error=$?;;

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
		docker cp $problem_dir/$filename lidi_container_${user}:/lidi_files/prog/$filename;

		# Run the program on limited memory and time.
		#TODO Memory limit.
		timeout $limit_t bash problem/bash/test_docker/grade_c.sh $user $problem $filename $file;
		timeout_error=$?;;

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
		main_class=$(head $problem_dir/${filename}_classes);
		rm -f $problem_dir/${filename}_classes;

		# Copy all files produced by javac to docker container.
		docker cp $problem_dir/. lidi_container_${user}/prog/;

		# Run the program on limited memory and time.
		#TODO Memory limit.
		timeout $limit_t bash problem/bash/test_docker/grade_java.sh $user $problem $filename $main_class;
		timeout_error=$?;;

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
		docker cp $problem_dir/$filename lidi_container_${user}:/lidi_files/prog/$filename;

		# Run the program on limited memory and time.
		#TODO Memory limit.
		timeout $limit_t bash problem/bash/test_docker/grade_c.sh $user $problem $filename $file;
		timeout_error=$?;;

	*)
		echo "ERROR";
		docker stop lidi_container_${user};
		exit 1;;
esac;

# Remove all files from container.
docker stop lidi_container_${user};

if [ "$timeout_error" == "124" ]
then
	echo "TLE";
	exit 0;
fi;

# Compare the outputs of program to solutions.
for i in 0 1 2 3 4 5 6 7 8 9
do
	cmp --silent $problem_dir/out_${filename}_${i} \
	    $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((grade++));
done;

echo $grade;
