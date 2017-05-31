#!/bin/bash

file=$1;
extension="${file##*.}";
filename="${file%.*}";
problem="${filename%_*}";
user="${filename#*_}";
proglang=$2;

count=0;

problem_dir=$LIDI_FILES_UPLOADED/$user/$problem;
mkdir -p $problem_dir;
cp $LIDI_FILES_UPLOADED/$file $problem_dir/$file; 

case $extension in
	c)
		echo -e "#define execl \"\"\n#define system \"\"\n#define exec \"\"\n#define execv \"\"\n#define getenv \"\"\n#define getcwd \"\"\n$(cat $problem_dir/$file)" > $problem_dir/$file;

		gcc -o $problem_dir/$filename $problem_dir/$file;

		echo $(tail -n +6 $problem_dir/$file) > $problem_dir/$file;

		for i in 0 1 2 3 4 5 6 7 8 9
		do
		        $problem_dir/$filename < $LIDI_FILES_TESTCASES/${problem}_${i} > $problem_dir/out_${filename}_${i};

        		cmp --silent $problem_dir/out_${filename}_${i} $LIDI_FILES_TESTCASES_SOL/${problem}_${i} && ((count++));
		done;;

	cpp)
		echo -e "#define execl \"\"\n#define system \"\"\n#define exec \"\"\n#define execv \"\"\n#define getenv \"\"\n#define getcwd \"\"\n$(cat $problem_dir/$file)" > $problem_dir/$file;

		g++ -o $problem_dir/$filename $problem_dir/$file;

		echo $(tail -n + 6 $problem_dir/$file) > $problem_dir/$file;

		for i in 0 1 2 3 4 5 6 7 8 9
		do
		        $problem_dir/$filename < $LIDI_FILES_TESTCASES/${problem}_${i} > $problem_dir/out_${filename}_${i};

			cmp --silent $problem_dir/out_${filename}_${i} $LIDI_FILES_TESTCASES_SOL/${problem}_${i} && ((count++));
		done;;

	py)
		echo -e "import sys\nsys.modules['os'] = None\ndel sys\n$(cat $problem_dir/$file)" > $problem_dir/$file

		if [ "$proglang" == "Python 3" ]
		then
			for i in 0 1 2 3 4 5 6 7 8 9
			do
				python3 $problem_dir/$file < $LIDI_FILES_TESTCASES/${problem}_${i} > $program_dir/out_${filename}_${i};
				
				cmp --silent $problem_dir/out_${filename}_${i} $LIDI_FILES_TESTCASES_SOL/${problem}_${i} && ((count++));
			done;
		else
			for i in 0 1 2 3 4 5 6 7 8 9
                        do
                                python $problem_dir/$file < $LIDI_FILES_TESTCASES/${problem}_${i} > $problem_dir/out_${filename}_${i};

                                cmp --silent $problem_dir/out_${filename}_${i} $LIDI_FILES_TESTCASES_SOL/${problem}_${i} && ((count++));
                        done;
		fi;

		echo $(tail -n +4 $problem_dir/$file) > $problem_dir/$file;;

	pas)
		fpc -vw $problem_dir/$file;
		for i in 0 1 2 3 4 5 6 7 8 9
		do
			$problem_dir/$filename < $LIDI_FILES_TESTCASES/${problem}_${i} > $problem_dir/out_${filename}_${i};

			cmp --silent $problem_dir/out_${filename}_${i} $LIDI_FILES_TESTCASES_SOL/${problem}_${i} && ((count++));
		done;;

	f)
		g77 $problem_dir/$file -o $problem_dir/$filename;
		for i in 0 1 2 3 4 5 6 7 8 9
		do
			$problem_dir/$filename < $LIDI_FILES_TESTCASES/${problem}_${i} > $problem_dir/out_${filename}_${i};

			cmp --silent $problem_dir/out_${filename}_${i} $LIDI_FILES_TESTCASES_SOL/${problem}_${i} && ((count++));
		done;;

	java)
		javac $problem_dir/$file;

		awk '/class/ {print $2}' $problem_dir/$file > $problem_dir/${filename}_classes;
		main_class=$(head $problem_dir/${filename}_classes);
		rm -f $probem_dir/${filename}_classes;

		for i in 0 1 2 3 4 5 6 7 8 9
		do
			java -cp $problem_dir $main_class < $LIDI_FILES_TESTCASES_SOL/${problem}_${i} > $problem_dir/out_${filename}_${i};

			cmp --silent $problem_dir/out_${filename}_${i} $LIDI_FILES_TESTCASES_SOL/${problem}_${i} && ((count++));
		done;;

	cs)
		mcs -out:$problem_dir/${filename}.exe $problem_dir/$file;

		for i in 0 1 2 3 4 5 6 7 8 9
		do
			mono $problem_dir/${filename}.exe < $LIDI_FILES_TESTCASES/${problem}_${i} > $problem_dir/out_${filename}_${i};

			cmp --silent $problem_dir/out_${filename}_${i} $LIDI_FILES_TESTCASES_SOL/${problem}_${i} && ((count++))
		done;;

	*)
		echo 'ERROR';;

esac;
echo $?;
echo $count;
