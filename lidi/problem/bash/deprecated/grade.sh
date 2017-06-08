#!/bin/bash

file=$1;
extension="${file##*.}";
filename="${file%.*}";
problem="${filename%_*}";
user="${filename#*_}";
proglang=$2;

count=0;

problem_dir=$CG_FILES_UPLOADED/$user/$problem;

case $extension in
	c)
	#	echo -e "#define execl \"\"\n#define system \"\"\n#define exec \"\"\n#define execv \"\"\n#define getenv \"\"\n#define getcwd \"\"\n$(cat $problem_dir/$file)" > $problem_dir/$file;

		gcc -o $problem_dir/$filename $problem_dir/$file;
		errors[10]=$?;

		echo $(tail -n +6 $problem_dir/$file) > $problem_dir/$file;

		for i in 0 1 2 3 4 5 6 7 8 9
		do
		        $problem_dir/$filename < $CG_FILES_TESTCASES/$problem/${problem}_${i} > $problem_dir/out_${filename}_${i};
			errors[$i]=$?;

        		cmp --silent $problem_dir/out_${filename}_${i} $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((count++));
		done;;

	cpp)
		echo -e "#define execl \"\"\n#define system \"\"\n#define exec \"\"\n#define execv \"\"\n#define getenv \"\"\n#define getcwd \"\"\n$(cat $problem_dir/$file)" > $problem_dir/$file;

		g++ -o $problem_dir/$filename $problem_dir/$file;
		errors[10]=$?;

		echo $(tail -n + 6 $problem_dir/$file) > $problem_dir/$file;

		for i in 0 1 2 3 4 5 6 7 8 9
		do
		        $problem_dir/$filename < $CG_FILES_TESTCASES/$problem/${problem}_${i} > $problem_dir/out_${filename}_${i};
			errors[$i]=$?;

			cmp --silent $problem_dir/out_${filename}_${i} $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((count++));
		done;;

	py)
		echo -e "import sys\nsys.modules['os'] = None\ndel sys\n$(cat $problem_dir/$file)" > $problem_dir/$file

		if [ "$proglang" == "Python 3" ]
		then
			for i in 0 1 2 3 4 5 6 7 8 9
			do
				python3 $problem_dir/$file < $CG_FILES_TESTCASES/$problem/${problem}_${i} > $program_dir/out_${filename}_${i};
				errors[$i]=$?;
				
				cmp --silent $problem_dir/out_${filename}_${i} $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((count++));
			done;
		else
			for i in 0 1 2 3 4 5 6 7 8 9
                        do
                                python $problem_dir/$file < $CG_FILES_TESTCASES/$problem/${problem}_${i} > $problem_dir/out_${filename}_${i};
				errors[$i]=$?;

                                cmp --silent $problem_dir/out_${filename}_${i} $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((count++));
                        done;
		fi;

		errors[10]=0;

		echo $(tail -n +4 $problem_dir/$file) > $problem_dir/$file;;

	pas)
		fpc $problem_dir/$file;
		errors[10]=$?;

		for i in 0 1 2 3 4 5 6 7 8 9
		do
			$problem_dir/$filename < $CG_FILES_TESTCASES/$problem/${problem}_${i} > $problem_dir/out_${filename}_${i};
			errors[$i]=$?;

			cmp --silent $problem_dir/out_${filename}_${i} $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((count++));
		done;;

	f)
		f77 $problem_dir/$file -o $problem_dir/$filename;
		errors[10]=$?;

		for i in 0 1 2 3 4 5 6 7 8 9
		do
			$problem_dir/$filename < $CG_FILES_TESTCASES/$problem/${problem}_${i} > $problem_dir/out_${filename}_${i};
			errors[$i]=$?;

			cmp --silent $problem_dir/out_${filename}_${i} $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((count++));
		done;;

	java)
		javac $problem_dir/$file;
		errors[10]=$?;

		awk '/class/ {print $2}' $problem_dir/$file > $problem_dir/${filename}_classes;
		main_class=$(head $problem_dir/${filename}_classes);
		rm -f $probem_dir/${filename}_classes;

		for i in 0 1 2 3 4 5 6 7 8 9
		do
			java -cp $problem_dir $main_class < $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} > $problem_dir/out_${filename}_${i};
			errors[$i]=$?;

			cmp --silent $problem_dir/out_${filename}_${i} $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((count++));
		done;;

	cs)
		mcs -out:$problem_dir/${filename}.exe $problem_dir/$file;
		errors[10]=$?;

		for i in 0 1 2 3 4 5 6 7 8 9
		do
			mono $problem_dir/${filename}.exe < $CG_FILES_TESTCASES/$problem/${problem}_${i} > $problem_dir/out_${filename}_${i};
			errors[$i]=$?;

			cmp --silent $problem_dir/out_${filename}_${i} $CG_FILES_TESTCASES_SOL/$problem/${problem}_${i} && ((count++))
		done;;

	*)
		errors[0]=666;;

esac;

echo ${errors[*]};
echo $count;
