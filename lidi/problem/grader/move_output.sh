#!/bin/bash

# If solution was better than the previous, move solution to subdir
# in which the best output is kept. Otherwise delete the output files.
#
# Call the program as 'bash * username task is_better'

move_from=$CG_FILES_UPLOADED/$1/$2;
move_to_best=$move_from/best_out/;
move_to_last=$move_from/last_out/;
move_to_prog=$move_from/prog/;
mkdir -p $move_to_best;
mkdir -p $move_to_last;
mkdir -p $move_to_prog;

rm -f $move_to_prog/*;

for i in 0 1 2 3 4 5 6 7 8 9
do
	if [ $3 -eq 1 ]
	then
		cp $move_from/out_${2}_${1}_${i} $move_to_best;
		cp $move_from/time $move_to_best;
	fi;

	mv $move_from/out_${2}_${1}_${i} $move_to_last;
done;

mv $move_from/errors $move_to_last;
mv $move_from/time $move_to_last;
mv $move_from/${2}_${1}.* $move_to_prog;
find $move_from -maxdepth 1 -type f -delete;
