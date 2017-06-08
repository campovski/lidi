#!/bin/bash

# This script compiles a program if necessary. It then runs the grader.
file=$1;
end="${file##*.}";
filename="${file%.*}";
problem="${filename%_*}";
user="${filename#*_}";
proglang=$2;

problem_dir=$CG_FILES_UPLOADED/$user/$problem;

limit_m=$(cat $CG_FILES_PROBLEMS/$problem/limit_m);
limit_t=$(cat $CG_FILES_PROBLEMS/$problem/limit_t);

grade=0;

case $end in
	c)
		# Disable some functions.
#		echo -e "#define execl \"\"\n#define system \"\"\n#define exec \"\"\n#define execv \"\"\n#define getenv \"\"\n#define getcwd \"\"\n$(cat $problem_dir/$file)" > $problem_dir/$file;

		# Compile the program.
		gcc -o $problem_dir/$filename $problem_dir/$file;
		if [ $? -gt 0 ]
		then
			echo "RTE";
			exit 0;
		fi;

		# Run the program on limited memory and time.
		#TODO Memory limit.
		timeout_error=$(timeout $((limit_t)) bash problem/bash/grade_c.sh $user $problem $filename $file);;

	cpp)
		# Compile the program.
		g++ -o $problem_dir/$filename $problem_dir/$file;
		if [ $? -gt 0 ]
		then
			echo "RTE";
			exit 0;
		fi;

		# Run the program on limited memory and time.
		#TODO Memory limit.
		timeout_error=$(timeout $((limit_t)) bash problem/bash/grade_c.sh $user $problem $filename $file);;

	py)
		if [ $proglang == "Python 3" ]
		then
			timeout_error=$(timeout $((limit_t)) bash problem/bash/grade_py3.sh $user $problem $filename $file);
		else
			timeout_error=$(timeout $((limit_t)) bash problem/bash/grade_py.sh $user $problem $filename $file);
		fi;;

	pas)
		# Compile the program.
		fpc $problem_dir/$file;
		if [ $? -gt 0 ]
		then
			echo "RTE";
			exit 0;
		fi;

		# Run the program on limited memory and time.
		timeout_error=$(timeout $((limit_t)) bash problem/bash/grade_c.sh $user $problem $filename $file);;

	f)
		# Compile the program.
		f77 $problem_dir/$file -o $problem_dir/$filename;
		if [ $? -gt 0 ]
		then
			echo "RTE";
			exit 0;
		fi;

		# Run the program on limited memory and time.
		#TODO Memory limit.
		timeout_error=$(timeout $((limit_t)) bash problem/bash/grade_c.sh $user $problem $filename $file);;

	java)
		# Compile the program.
		javac $problem_dir/$file;
		if [ $? -gt 0 ]
		then
			echo "RTE";
			exit 0;
		fi;

		# Find main class.
		awk '/class/ {print $2}' $problem_dir/$file > $problem_dir/${filename}_classes;
		main_class=$(head $problem_dir/${filename}_classes);
		rm -f $problem_dir/${filename}_classes;

		# Run the program on limited memory and time.
		#TODO Memory limit.
		timeout_error=$(timeout $((limit_t)) bash problem/bash/grade_java.sh $user $problem $filename $main_class);;

	cs)
		# Compile the program.
		mcs -out:$problem_dir/${filename}.exe $problem_dir/$file;
		if [ $? -gt 0 ]
		then
			echo "RTE";
			exit 0;
		fi;

		# Run the program on limited memory and time.
		timeout_error=$(timeout $((limit_t)) bash problem/bash/grade_c.sh $user $problem $filename $file);;

	*)
		echo "ERROR";;
esac;

if [ "$timeout_error" = "124" ]
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
